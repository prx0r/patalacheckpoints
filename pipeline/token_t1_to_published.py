"""token_t1_to_published.py — build publishable translation objects from the NEW
token-gloss T1 format.

The IPVV T1 chunks (translations/_stack/ipvv/02_t1/) use the token-gloss format:

    [and]-GLOSS (IAST)            normal lemma+gloss
    [and]-"GLOSS (IAST)"          quoted (verbatim pratīka / root-text quotation)
    [and]-and                     bare supplied connective, no IAST
    [and]-and (ca)                "and" with a lemma

This is strictly better than the old prose-gloss T1 (141 legacy files) because every
word carries a lemma + IAST, so it can be aligned token-by-token to source spans.

This module turns one token-T1 chunk into a pāṭala PublishedTranslation object
(see data/corpus/translation.ts): source_spans, target_spans, alignments,
decisions, evidence, provenance. Deterministic — no model calls.

Usage:
  python3 token_t1_to_published.py <chunk.md> <work_id> <locator> [--out <prefix>]
"""

from __future__ import annotations
import json
import re
import sys
from pathlib import Path

# ── token grammar (mirrors t1_extract.py) ────────────────────────────────────
# Token: [and]-GLOSS (IAST) | [and]-"GLOSS (IAST)" | [and]-and | [and]-and (ca)
_ANCHOR = re.compile(r"\[and\]-")


def parse_tokens(text: str) -> list[dict]:
    """Split a chunk's body into token records {gloss, iast, quoted, raw}."""
    toks = []
    parts = _ANCHOR.split(text)[1:]  # everything after each [and]- anchor
    for p in parts:
        p = p.strip()
        quoted = p.startswith('"')
        p = p.lstrip('"').rstrip('"')
        m = re.search(r"^(.*?)\(([^)]*)\)", p)  # gloss = before first '('
        if m:
            gloss = m.group(1).strip().rstrip(",;.:| ")
            iast = m.group(2).strip()
        else:
            gloss = p.rstrip(",;.:| ").strip()
            iast = ""
        if not gloss:
            continue
        toks.append({
            "gloss": gloss,
            "iast": iast,
            "quoted": bool(quoted),
            "raw": f"[and]-{p}",
        })
    return toks


def split_source_spans(sanskrit: str) -> list[str]:
    """Split a Sanskrit surface into word spans (pada-level), keeping sandhi surface."""
    return [w for w in re.split(r"[\s,;|·]+", sanskrit.strip()) if w]


def split_target_spans(translation: str) -> list[str]:
    """Split the English into phrase spans (clauses)."""
    parts = re.split(r"(?<=[.;:])\s+", translation.strip())
    return [p.strip() for p in parts if p.strip()]


def build_published(tokens: list[dict], passage_id: str, work_id: str,
                    sanskrit: str, edition: str, translation_version_id: str) -> dict:
    """Assemble the PublishedTranslation object from parsed tokens."""
    # source spans = the IAST lemmas that carry content
    src_words = split_source_spans(sanskrit)
    source_spans = [
        {"id": f"pt:srcspan:{work_id}:{n}", "passage_id": passage_id, "text": w}
        for n, w in enumerate(src_words, 1)
    ]
    # target spans = the glosses (one per token with a gloss)
    glosses = [t for t in tokens if t["gloss"]]
    target_spans = [
        {"id": f"pt:tgtspan:{work_id}:{n}", "translation_version_id": translation_version_id,
         "text": t["gloss"]}
        for n, t in enumerate(glosses, 1)
    ]
    # align each content token to a source span (token with IAST → a source word)
    alignments = []
    decs = []
    src_used = 0
    for n, t in enumerate(tokens, 1):
        if not t["iast"]:
            continue  # supplied connective — no source alignment
        if src_used < len(source_spans):
            src_id = source_spans[src_used]["id"]
            src_used += 1
        else:
            src_id = source_spans[-1]["id"] if source_spans else ""
        tgt_id = f"pt:tgtspan:{work_id}:{n}"  # may not exist if gloss skipped; align by index
        # find the matching target span (gloss == this token's gloss)
        tgt = next((s["id"] for s in target_spans if s["text"] == t["gloss"]), tgt_id)
        alignments.append({
            "id": f"pt:align:{work_id}:{n}",
            "source_span_ids": [src_id],
            "target_span_ids": [tgt],
            "type": "direct",
            "decision_ids": [f"pt:decision:{work_id}:LEX:{n}"] if t["iast"] else [],
            "method": "lexical_rule",
        })
        decs.append({
            "id": f"pt:decision:{work_id}:LEX:{n}",
            "passage_id": passage_id,
            "claim": t["gloss"],
            "surface_rendering": t["gloss"],
            "adjudicated_reading": t["gloss"],
            "alternatives": [],
            "status": "CONSTRAINED",
            "evidence_state": "grounded",
            "editorial_status": "proposed",
            "method": "lexical_rule",
            "reason": f"token {t['iast']} → {t['gloss']}",
            "evidence": [],
            "source_span_ids": [src_id],
            "target_span_ids": [tgt],
        })
    return {
        "passage_id": passage_id,
        "work_id": work_id,
        "text": " ".join(t["gloss"] for t in tokens),
        "source_spans": source_spans,
        "target_spans": target_spans,
        "alignments": alignments,
        "decisions": decs,
        "evidence": [],
        "review_state": "proposed",
        "provenance": {"edition": edition, "base_source": work_id, "translation_version_id": translation_version_id},
        "token_count": len(tokens),
    }


def validate(pub: dict) -> list[str]:
    """Invariant check: every span/decision reference resolves."""
    problems = []
    sid = {s["id"] for s in pub["source_spans"]}
    tid = {s["id"] for s in pub["target_spans"]}
    did = {d["id"] for d in pub["decisions"]}
    for a in pub["alignments"]:
        for s in a["source_span_ids"]:
            if s and s not in sid:
                problems.append(f"align {a['id']}: source {s} missing")
        for t in a["target_span_ids"]:
            if t and t not in tid:
                problems.append(f"align {a['id']}: target {t} missing")
        for d in a["decision_ids"]:
            if d and d not in did:
                problems.append(f"align {a['id']}: decision {d} missing")
    return problems


def main() -> None:
    args = sys.argv[1:]
    if len(args) < 3:
        print(__doc__)
        return
    chunk_path, work_id, locator = args[0], args[1], args[2]
    out = f"published_{Path(chunk_path).stem}"
    if "--out" in args:
        out = args[args.index("--out") + 1]

    text = Path(chunk_path).read_text(encoding="utf-8")
    tokens = parse_tokens(text)
    # build the Sanskrit surface from the tokens' IAST lemmas (joined by space)
    sanskrit = " ".join(t["iast"] for t in tokens if t["iast"])
    passage_id = f"pt:passage:{work_id}:{locator}"
    pub = build_published(tokens, passage_id, work_id, sanskrit,
                          f"our T1 ({Path(chunk_path).name})", f"{work_id}:{locator}:v1")
    problems = validate(pub)
    Path(out + ".json").write_text(json.dumps(pub, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"tokens: {len(tokens)} · source_spans: {len(pub['source_spans'])} · "
          f"target_spans: {len(pub['target_spans'])} · alignments: {len(pub['alignments'])} · "
          f"decisions: {len(pub['decisions'])}")
    print(f"validation problems: {len(problems)}")
    for p in problems[:10]:
        print("  ", p)
    print(f"wrote {out}.json")


if __name__ == "__main__":
    main()
