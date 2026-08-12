#!/usr/bin/env python3
"""build_p2_review_blind_fixed.py — create a genuinely blind P2 manual-review set.

Fixes the 70f237b workflow:
- machine cell/category is NEVER placed in the reviewer-facing JSONL/CSV
- opaque review IDs are used
- selected cases are shuffled across strata
- a separate secret unblinding key is emitted
- reviewer fields contain only source/L0 evidence + blank human judgments

Usage:
  python3 pipeline/build_p2_review_blind_fixed.py \
    --ensemble <p2_disagreements.jsonl> \
    --l0dir <l0> \
    --out <review.jsonl> \
    --key-out <review_key.jsonl> \
    [--per-cell 40] [--seed 42]
"""
from __future__ import annotations
import argparse, csv, hashlib, json, random, sys
from collections import defaultdict
from pathlib import Path

CELLS = {
    "DOUBLE_CONFLICT": "V-/H-",
    "VIDYUT_MISMATCH": "V-/H+",
    "HERITAGE_MISMATCH": "V+/H-",
    "BOTH_SUPPORT": "V+/H+",
}

def load_l0_index(l0dir: str) -> dict:
    idx = {}
    for f in Path(l0dir).glob("*.l0.jsonl"):
        chunk = f.name[:-len(".l0.jsonl")]
        for line in f.open(encoding="utf-8"):
            r = json.loads(line)
            idx[r["id"]] = {
                "chunk_id": chunk,
                "line_id": r.get("line_id"),
                "literal_gloss": r.get("literal_gloss"),
                "source_text": r.get("source_text"),
                "raw_fragment": r.get("raw_fragment"),
                "lemma_iast": r.get("lemma_iast"),
            }
    return idx

def opaque_id(seed: int, l0_id: str) -> str:
    h = hashlib.sha256(f"{seed}:{l0_id}".encode()).hexdigest()[:12]
    return f"P2R-{h}"

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ensemble", required=True)
    ap.add_argument("--l0dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--key-out", required=True)
    ap.add_argument("--per-cell", type=int, default=40)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    rows = [json.loads(l) for l in open(args.ensemble, encoding="utf-8")]
    l0idx = load_l0_index(args.l0dir)

    by_cell = defaultdict(list)
    for r in rows:
        by_cell[r.get("agreement_class")].append(r)

    review_rows, key_rows = [], []
    for cell_name, sign in CELLS.items():
        pool = by_cell.get(sign, [])
        sample = rng.sample(pool, min(args.per_cell, len(pool)))
        for r in sample:
            l0_id = r.get("l0_id")
            l0 = l0idx.get(l0_id, {})
            rid = opaque_id(args.seed, str(l0_id))
            review_rows.append({
                "review_id": rid,
                "l0_id": l0_id,
                "source_form": r.get("surface"),
                "lemma_iast": l0.get("lemma_iast") or r.get("lemma_iast"),
                "literal_gloss": l0.get("literal_gloss"),
                "source_context": l0.get("source_text"),
                "passage_locator": f"{l0.get('chunk_id','?')}:L{l0.get('line_id','?')}",
                "raw_fragment": l0.get("raw_fragment"),
                "human_analysis": "",
                "preferred_lemma": "",
                "material_to_translation": "",
                "reason": "",
            })
            key_rows.append({
                "review_id": rid,
                "l0_id": l0_id,
                "cell": cell_name,
                "agreement_class": sign,
            })

    rng.shuffle(review_rows)

    with open(args.out, "w", encoding="utf-8") as fh:
        for row in review_rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    csv_path = str(Path(args.out).with_suffix("")) + "_blind.csv"
    fields = list(review_rows[0].keys()) if review_rows else []
    with open(csv_path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(review_rows)

    with open(args.key_out, "w", encoding="utf-8") as fh:
        for row in key_rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"review cases: {len(review_rows)} -> {args.out}")
    print(f"blind CSV: {csv_path}")
    print(f"SECRET unblinding key: {args.key_out}")
    print("Do not provide the key file to the reviewer before review completion.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
