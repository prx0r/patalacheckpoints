#!/usr/bin/env python3
"""build_p2_review.py — create the blind P2 manual-review set.

Samples the major ensemble cells, enriches each case with L0 source context + gloss + locator, and
emits a review file with the MACHINE VERDICTS CONCEALED (the reviewer sees only the source evidence and
answers the philological question independently).

Cells (40 each, or as many as available):
  DOUBLE_CONFLICT  (V-/H-)
  VIDYUT_MISMATCH  (V-/H+)
  HERITAGE_MISMATCH(V+/H-)
  BOTH_SUPPORT     (V+/H+ control)

Reviewer answers per case:
  human_analysis:   SUPPORTED | PLAUSIBLE_ALTERNATIVE | CONFLICT | CANNOT_DECIDE
  preferred_lemma:  (if different)
  material_to_translation:  true | false
  reason:           (short)

Usage:
  python3 pipeline/build_p2_review.py --ensemble <p2_disagreements.jsonl> --l0dir <l0> --out <review.jsonl>
      [--per-cell 40] [--seed 42]
"""
from __future__ import annotations
import argparse
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

CELLS = {
    "DOUBLE_CONFLICT": "V-/H-",
    "VIDYUT_MISMATCH": "V-/H+",
    "HERITAGE_MISMATCH": "V+/H-",
    "BOTH_SUPPORT": "V+/H+",
}


def load_l0_index(l0dir: str) -> dict:
    """Index L0 records by id → {gloss, source_text, line_id, chunk_id, raw_fragment, lemma_iast}."""
    idx = {}
    for f in Path(l0dir).glob("*.l0.jsonl"):
        chunk = f.name[: -len(".l0.jsonl")]
        for line in f.open(encoding="utf-8"):
            r = json.loads(line)
            idx[r["id"]] = {
                "chunk_id": chunk, "line_id": r.get("line_id"),
                "gloss": r.get("literal_gloss"), "source_text": r.get("source_text"),
                "raw_fragment": r.get("raw_fragment"), "lemma_iast": r.get("lemma_iast"),
            }
    return idx


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ensemble", required=True, help="p2_disagreements.jsonl")
    ap.add_argument("--l0dir", required=True, help="l0 dir for context enrichment")
    ap.add_argument("--out", required=True, help="output review .jsonl")
    ap.add_argument("--per-cell", type=int, default=40)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    random.seed(args.seed)

    rows = [json.loads(l) for l in open(args.ensemble, encoding="utf-8")]
    l0idx = load_l0_index(args.l0dir)
    print(f"ensemble rows: {len(rows)}, L0 index: {len(l0idx)}")

    by_cell = defaultdict(list)
    for r in rows:
        by_cell[r["agreement_class"]].append(r)

    out = []
    for cell_name, sign in CELLS.items():
        pool = by_cell.get(sign, [])
        sample = random.sample(pool, min(args.per_cell, len(pool)))
        for r in sample:
            l0 = l0idx.get(r.get("l0_id"), {})
            # CONCEAL machine verdicts — reviewer sees only source evidence
            case = {
                "review_id": f"{cell_name}:{r.get('l0_id','?')}",
                "cell": cell_name,  # NOTE: cell is shown in the review file for the human; the machine
                                    # verdict is concealed in a SEPARATE key file, not here.
                "source_form": r.get("surface"),
                "lemma_iast": l0.get("lemma_iast") or r.get("lemma_iast"),
                "literal_gloss": l0.get("gloss"),
                "source_context": l0.get("source_text"),
                "passage_locator": f"{l0.get('chunk_id','?')}:L{l0.get('line_id','?')}",
                "raw_fragment": l0.get("raw_fragment"),
                # answer fields (blank for the reviewer)
                "human_analysis": "",
                "preferred_lemma": "",
                "material_to_translation": "",
                "reason": "",
            }
            out.append(case)

    with open(args.out, "w", encoding="utf-8") as fh:
        for c in out:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"wrote {len(out)} review cases to {args.out}")
    from collections import Counter
    print("by cell:", dict(Counter(c["cell"] for c in out)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
