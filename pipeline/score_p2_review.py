#!/usr/bin/env python3
"""score_p2_review_fixed.py — score a completed genuinely blind P2 review.

This scorer does NOT trust a machine category in the review file.
It joins the completed review to the separate unblinding key.

Outputs:
1. human label distribution by ensemble cell
2. Vidyut-vs-human agreement on decidable SUPPORTED/CONFLICT cases
3. Heritage-vs-human agreement on decidable cases
4. BOTH_SUPPORT human-support rate
5. DOUBLE_CONFLICT human-conflict rate
6. unclear/abstention rates

Mismatch cells are NOT collapsed into a bogus single "correct/wrong" verdict:
V-/H+ and V+/H- contain two different machine judgments and must be scored
per witness.

Usage:
  python3 pipeline/score_p2_review_fixed.py \
    --review <completed review.jsonl> \
    --key <review_key.jsonl> \
    --out <matrix.json>
"""
from __future__ import annotations
import argparse, json, sys
from collections import Counter, defaultdict

VALID = {"SUPPORTED","PLAUSIBLE_ALTERNATIVE","CONFLICT","CANNOT_DECIDE"}

SIGNS = {
    "BOTH_SUPPORT": (True, True),
    "VIDYUT_MISMATCH": (False, True),
    "HERITAGE_MISMATCH": (True, False),
    "DOUBLE_CONFLICT": (False, False),
}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--review", required=True)
    ap.add_argument("--key", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    key = {}
    for l in open(args.key, encoding="utf-8"):
        r = json.loads(l)
        key[r["review_id"]] = r

    by_cell = defaultdict(Counter)
    witness = {
        "vidyut": Counter(),
        "heritage": Counter(),
    }
    reviewed = 0

    for l in open(args.review, encoding="utf-8"):
        r = json.loads(l)
        h = str(r.get("human_analysis","")).strip().upper()
        if not h:
            continue
        if h not in VALID:
            raise ValueError(f"invalid human_analysis {h!r} in {r.get('review_id')}")
        k = key.get(r["review_id"])
        if not k:
            raise KeyError(f"review_id absent from unblinding key: {r['review_id']}")
        cell = k["cell"]
        by_cell[cell][h] += 1
        reviewed += 1

        # Only SUPPORTED and CONFLICT give an unambiguous binary human verdict
        if h in {"SUPPORTED","CONFLICT"}:
            human_support = (h == "SUPPORTED")
            v_support, h_support = SIGNS[cell]
            for name, machine_support in (("vidyut",v_support),("heritage",h_support)):
                witness[name]["n_decidable"] += 1
                if machine_support == human_support:
                    witness[name]["agree"] += 1
                else:
                    witness[name]["disagree"] += 1
        else:
            witness["vidyut"]["human_unclear"] += 1
            witness["heritage"]["human_unclear"] += 1

    result = {
        "reviewed": reviewed,
        "by_cell_human_labels": {k: dict(v) for k,v in by_cell.items()},
        "witness_vs_human": {},
        "cell_diagnostics": {}
    }
    for name, c in witness.items():
        n = c["n_decidable"]
        result["witness_vs_human"][name] = {
            **dict(c),
            "agreement_rate_decidable": (c["agree"]/n if n else None)
        }

    for cell, counts in by_cell.items():
        n = sum(counts.values())
        result["cell_diagnostics"][cell] = {
            "n": n,
            "human_supported_rate": counts["SUPPORTED"]/n if n else None,
            "human_conflict_rate": counts["CONFLICT"]/n if n else None,
            "human_unclear_rate": (counts["PLAUSIBLE_ALTERNATIVE"]+counts["CANNOT_DECIDE"])/n if n else None,
        }

    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, ensure_ascii=False)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main())
