"""patala_ml/corpus.py — load the actual Pāṭala IPVV corpus for ML baselines.

Reads the published lazy-JSON store (data/published/ipvv/*.json) and the C1 bodies, so the
baselines run over REAL scholarship, not test fixtures. CPU-only.

Document = one passage. Each document carries:
  id (pt:passage:...) · locator (chunk) · l2_text · c1 (verse_commentary[] bodies) ·
  c1_source (structured) · source (Sanskrit) · vol
"""
from __future__ import annotations

import glob
import json
import os
from dataclasses import dataclass, field


@dataclass
class PassageDoc:
    id: str
    locator: str
    l2_text: str = ""
    c1_body: str = ""
    source_sanskrit: str = ""
    vol: str = ""
    key_terms: list[str] = field(default_factory=list)
    see_also: list[str] = field(default_factory=list)

    def full_text(self) -> str:
        """The combined searchable text: L2 + C1 (the scholarly surface)."""
        return f"{self.l2_text}\n\n{self.c1_body}"


def load_passages(store_dir: str | None = None) -> list[PassageDoc]:
    """Load all IPVV passages from the lazy-JSON store."""
    if store_dir is None:
        store_dir = os.environ.get(
            "PATALA_STORE", "/root/projects/patala/data/published/ipvv"
        )
    docs = []
    for f in sorted(glob.glob(os.path.join(store_dir, "pt-passage-*.json"))):
        try:
            r = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        pid = r.get("id", "")
        c1 = r.get("c1") or {}
        verse = c1.get("verse_commentary") or []
        c1_body = " ".join(v.get("commentary", "") for v in verse)
        c1src = r.get("c1_source") or {}
        terms = c1src.get("key_terms") or c1src.get("terms") or ""
        # key_terms may be a list, a comma string, or markdown bullets ("- **term** — gloss")
        if isinstance(terms, str):
            bullets = [t for t in terms.split("\n") if t.strip()]
            terms = []
            for b in bullets:
                b = b.strip().lstrip("-* ").strip()
                if "**" in b:
                    # "- **term** — gloss" -> "term"
                    parts = b.split("**")
                    if len(parts) >= 3 and parts[1].strip():
                        b = parts[1].strip()
                    else:
                        b = parts[0].strip().rstrip("*").strip()
                elif " — " in b or " - " in b:
                    b = b.split(" — ")[0].split(" - ")[0]
                if b:
                    terms.append(b.strip())
        see_also = c1src.get("see_also") or c1src.get("related_passages") or []
        if isinstance(see_also, str):
            see_also = see_also.split("\n")
        out_see = []
        for s in see_also:
            s = str(s).strip().lstrip("-* ").strip()
            if "**" in s:
                parts = s.split("**")
                if len(parts) >= 3 and parts[1].strip():
                    s = parts[1].strip()
                else:
                    s = parts[0].strip().rstrip("*").strip()
            if s:
                out_see.append(s)
        see_also = out_see
        docs.append(PassageDoc(
            id=pid,
            locator=r.get("chunk", ""),
            l2_text=r.get("l2_text", "") or "",
            c1_body=c1_body,
            source_sanskrit=(r.get("source") or {}).get("text", "") or "",
            vol=r.get("vol", "") or "",
            key_terms=terms,
            see_also=see_also,
        ))
    return docs


def load_from_tsv(path: str) -> list[PassageDoc]:
    """Optional: load from a TSV (id<TAB>text) for arbitrary corpora (transfer eval)."""
    docs = []
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line or "\t" not in line:
            continue
        pid, text = line.split("\t", 1)
        docs.append(PassageDoc(id=pid, locator=pid, l2_text=text))
    return docs


if __name__ == "__main__":
    docs = load_passages()
    print(f"loaded {len(docs)} passages from the Pāṭala IPVV store")
    for d in docs[:3]:
        print(f"  {d.locator} | L2={len(d.l2_text)}c | C1={len(d.c1_body)}c | terms={len(d.key_terms)}")
