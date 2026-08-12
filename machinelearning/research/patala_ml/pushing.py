"""patala_ml/pushing.py — parse the PUSHING sessions into typed PushingRecords.

The PUSHING sessions (research-library/pushing/_source/ + recognition/pushing-*/) are ALREADY
a supervised reasoning dataset in prose: question → distinctions → theorem → boundary →
next-pressure → passages. This extracts them into machine records (the DNA as data).

Two extractors:
  - sessions_gems():    the "Q## ... → GEM: ..." pattern in the PUSHING-IPVV/-TANTRALOKA scaffolds
  - session_blocks():   the structured markers (Point of Contention / theorem / boundary /
                        frontier) in the LOGICVID sessions

Every record is MACHINE_DRAFT until human review. passage_ids are resolved via the store where
possible (the deterministic floor) — never guessed.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

from .corpus import PassageDoc, load_passages


@dataclass
class PushingRecord:
    id: str
    work_id: str
    source_file: str
    question: str = ""
    question_shape: str = "UNKNOWN"  # MECHANISM_GAP|CRUX|SUBVERSION|QUANTIFIER|REGISTER|ROOT
    theorem: str = ""
    boundary: str = ""
    next_pressure: str = ""
    passage_ids: list[str] = field(default_factory=list)
    strength: str = "MACHINE_DRAFT"  # PROVED|REVIEWED|WELL_SUPPORTED|PLAUSIBLE|PARTIAL|SILENT
    status: str = "MACHINE_DRAFT"

    def to_dict(self) -> dict:
        return {
            "id": self.id, "work_id": self.work_id, "source_file": self.source_file,
            "question": self.question, "question_shape": self.question_shape,
            "theorem": self.theorem, "boundary": self.boundary,
            "next_pressure": self.next_pressure, "passage_ids": self.passage_ids,
            "strength": self.strength, "status": self.status,
        }


# ── the Q## → GEM extractor (PUSHING scaffolds) ──────────────────────────────
GEM_RE = re.compile(r"###\s+(Q\d+)\s*[—-]\s*(.*?)\s*→\s*GEM:\s*(.*?)(?=\n###\s|\Z)", re.S)


def extract_gems(text: str, work_id: str, source_file: str) -> list[PushingRecord]:
    """Extract the Q##→GEM pairs from a PUSHING scaffold."""
    records = []
    for qid, question, gem in GEM_RE.findall(text):
        # the gem is the first line (the headline) + the body
        lines = [l.strip() for l in gem.split("\n") if l.strip()]
        headline = lines[0] if lines else ""
        theorem = f"{headline} — {' '.join(lines[1:]).strip()}" if len(lines) > 1 else headline
        # heuristic question-shape from the question text
        shape = classify_shape(question)
        records.append(PushingRecord(
            id=f"pt:pushing:{work_id}:{qid}",
            work_id=work_id, source_file=source_file,
            question=question.strip(), question_shape=shape,
            theorem=theorem[:500], strength="WELL_SUPPORTED",
        ))
    return records


# ── the structured-marker extractor (LOGICVID sessions) ──────────────────────
def extract_blocks(text: str, work_id: str, source_file: str) -> list[PushingRecord]:
    """Extract title / contention / boundary / frontier from a LOGICVID session."""
    def sec(pat: str) -> str:
        m = re.search(pat, text, re.S)
        return m.group(1).strip()[:500] if m else ""

    title = sec(r"^#\s+(.+)")
    boundary = sec(r"# What has actually been established\s*\n(.*?)(?=\n# |\Z)")
    frontier = sec(r"# The frontier\s*\n(.*?)(?=\n# |\Z)")
    theorem = sec(r"# The theorem\s*\n(.*?)(?=\n# |\Z)")
    if not (title and (theorem or boundary)):
        return []
    return [PushingRecord(
        id=f"pt:pushing:{work_id}:{re.sub(r'[^A-Za-z0-9]+', '-', title).lower()}",
        work_id=work_id, source_file=source_file,
        question=title, theorem=theorem, boundary=boundary,
        next_pressure=frontier, question_shape=classify_shape(title),
    )]


# ── question-shape classification (heuristic DNA) ────────────────────────────
def classify_shape(q: str) -> str:
    """Classify a question into the DNA shapes by its interrogative/lexical structure."""
    ql = q.lower()
    if re.search(r"\bwhy (must|does|cannot|can|is|should)\b", ql) or "necessarily" in ql:
        return "MECHANISM_GAP"
    if re.search(r"\b(does|is) .*\b(every|all|always|itself)\b", ql) or "every cognition" in ql:
        return "SUBVERSION"
    if re.search(r"\b(how does|why does|how)\b.*\b(become|universal|every|all)\b", ql):
        return "QUANTIFIER"
    if re.search(r"\b(suffering|impurity|error|grief|fear|pain)\b", ql):
        return "CRUX"
    if re.search(r"\b(felt|experience|actually do|practice)\b", ql):
        return "REGISTER"
    if re.search(r"\btime\b|\bone.?and.?many\b", ql):
        return "ROOT"
    return "MECHANISM_GAP"  # default: the "why is X necessarily Y" family


# ── resolve passage mentions against the store ───────────────────────────────
def resolve_passages(records: list[PushingRecord], docs: list[PassageDoc]) -> list[PushingRecord]:
    """Try to resolve cited passage-ids (V2L, V3C...) to real store passages (deterministic)."""
    # build a map from chunk/id token to store doc id
    token_to_id = {}
    for d in docs:
        for tok in (d.locator, d.id):
            for m in re.findall(r"[Vv]?\d[A-Z]|[A-Za-z]\d[a-z].\d", d.locator):
                token_to_id.setdefault(m.upper(), d.id)
    for r in records:
        for m in re.findall(r"\b(V[0-9]-?[A-Z]|V[0-9][A-Z]|k[0-9].?[0-9]*)\b", r.question + " " + r.theorem):
            key = m.upper().replace("V2-", "V2")
            if key in token_to_id and token_to_id[key] not in r.passage_ids:
                r.passage_ids.append(token_to_id[key])
    return records


def extract_all(session_files: list[str], work_id: str) -> list[PushingRecord]:
    """Extract records from a list of session files."""
    records = []
    for f in session_files:
        try:
            text = open(f, encoding="utf-8").read()
        except Exception:
            continue
        records += extract_gems(text, work_id, f)
        records += extract_blocks(text, work_id, f)
    return records


if __name__ == "__main__":
    import glob, os
    base = os.environ.get("PUSHING_DIR", "/root/projects/research-library/pushing/_source")
    files = sorted(glob.glob(os.path.join(base, "*.md")))
    records = extract_all(files, "ipvv")
    docs = load_passages()
    records = resolve_passages(records, docs)
    print(f"extracted {len(records)} PushingRecords from {len(files)} session files")
    shapes = {}
    for r in records:
        shapes[r.question_shape] = shapes.get(r.question_shape, 0) + 1
    print("question-shapes:", shapes)
    print("with resolved passages:", sum(1 for r in records if r.passage_ids))
    for r in records[:5]:
        print(f"  {r.id} [{r.question_shape}] {r.question[:60]}")
