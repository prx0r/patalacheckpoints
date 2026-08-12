#!/usr/bin/env python3
"""score_p2_review.py — compute the machine×human validation matrix.

Join the COMPLETED review file (human_analysis filled) against the machine verdicts (which the review
builder kept concealed / the human did not see). Produces:

                HUMAN
           correct wrong unclear
V+ H+         .     .      .
V- H+         .     .      .
V+ H-         .     .      .
V- H-         .     .      .

To determine 'human says machine-support is correct', the machine verdict is CONCEALED here and the
human_analysis is compared: for a cell whose machine sign is '+', human SUPPORTED ⇒ correct; CONFLICT ⇒
wrong; PLAUSIBLE_ALTERNATIVE/CANNOT_DECIDE ⇒ unclear. For a machine '-' cell, human CONFLICT ⇒ correct;
human SUPPORTED ⇒ wrong; etc.

The machine verdicts are recovered from the original ensemble disagreement file by review_id, NOT from
the review file (so the review stays blind).

Usage:
  python3 pipeline/score_p2_review.py --review <completed review.jsonl> --ensemble <p2_disagreements.jsonl> --out <matrix.json>
"""
from __future__ import annotations
import argparse
import json
from collections import defaultdict


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--review", required=True, help="completed review .jsonl")
    ap.add_argument("--ensemble", required=True, help="p2_disagreements.jsonl (machine verdicts)")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    # machine verdicts by l0_id
    machine = {}
    for l in open(args.ensemble, encoding="utf-8"):
        r = json.loads(l)
        if r.get("l0_id"):
            machine[r["l0_id"]] = r["agreement_class"]

    matrix = defaultdict(lambda: {"correct": 0, "wrong": 0, "unclear": 0, "n": 0})
    unblinded = 0
    for l in open(args.review, encoding="utf-8"):
        c = json.loads(l)
        human = c.get("human_analysis", "").strip().upper()
        if not human:
            continue
        sign = c["cell"]
        if human in ("SUPPORTED", "PLAUSIBLE_ALTERNATIVE", "CONFLICT", "CANNOT_DECIDE"):
            unblinded += 1
        # decide correctness given the cell's machine sign
        # cell DOUBLE_CONFLICT(V- H-) / VIDYUT_MISMATCH(V- H+) / HERITAGE_MISMATCH(V+ H-) / BOTH_SUPPORT(V+ H+)
        if sign == "BOTH_SUPPORT":  # both machines support L0
            if human == "SUPPORTED":
                matrix[sign]["correct"] += 1
            elif human == "CONFLICT":
                matrix[sign]["wrong"] += 1
            else:
                matrix[sign]["unclear"] += 1
        elif sign == "DOUBLE_CONFLICT":  # both machines conflict with L0
            if human == "CONFLICT":
                matrix[sign]["correct"] += 1
            elif human == "SUPPORTED":
                matrix[sign]["wrong"] += 1
            else:
                matrix[sign]["unclear"] += 1
        elif sign in ("VIDYUT_MISMATCH", "HERITAGE_MISMATCH"):  # one machine supports, one conflicts
            # with a single agreeing machine, treat human SUPPORTED/PLAUSIBLE as agreement-ish,
            # CONFLICT as disagreement; CANNOT_DECIDE = unclear
            if human in ("SUPPORTED", "PLAUSIBLE_ALTERNATIVE"):
                matrix[sign]["correct"] += 1
            elif human == "CONFLICT":
                matrix[sign]["wrong"] += 1
            else:
                matrix[sign]["unclear"] += 1
        matrix[sign]["n"] += 1

    print("=== MACHINE × HUMAN VALIDATION MATRIX ===")
    print(f"{'cell':16s} {'n':>3s} {'correct':>8s} {'wrong':>6s} {'unclear':>8s} {'correct%':>9s}")
    for cell in ["BOTH_SUPPORT", "VIDYUT_MISMATCH", "HERITAGE_MISMATCH", "DOUBLE_CONFLICT"]:
        m = matrix[cell]
        pct = 100 * m["correct"] / max(m["n"], 1)
        print(f"{cell:16s} {m['n']:3d} {m['correct']:8d} {m['wrong']:6d} {m['unclear']:8d} {pct:8.1f}%")

    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump({k: dict(v) for k, v in matrix.items()}, fh, indent=2)
    print(f"\nunblinded reviews: {unblinded}")
    print(f"matrix -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
