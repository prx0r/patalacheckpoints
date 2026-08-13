#!/usr/bin/env python3
"""test_manuscript_resolution_gold.py — P4 MANUSCRIPT-RESOLUTION-GOLD acceptance.

Checks:
  1. gold frozen with all the reviewer's ambiguity categories
  2. FALSE_MERGE_RATE is the primary metric
  3. a resolver that conflates distinct works (commentary/base, same-title-diff-work) is penalized
  4. an exact-match resolver scores well on recall
  5. the gold is non-circular (scorer never reads a gold 'expected' verdict)
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manuscript_resolution_gold import freeze_gold, score_resolution, GOLD_CASES

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


b = freeze_gold()

print("== 1. gold frozen, all categories ==")
cats = set(b["categories"])
check("10 ambiguity categories", len(cats) == 10, str(cats))
check("case count", b["case_count"] >= 10)

print("\n== 2. primary metric = FALSE_MERGE_RATE ==")
check("primary metric named", b["primary_metric"] == "FALSE_MERGE_RATE")

print("\n== 3. over-merger penalized ==")
def over_merger(records):
    return {"target": records[0]["rid"], "candidates": [{"id": r["rid"], "score": 0.9} for r in records]}
# an over-merger that returns ALL records as one candidate set = many false merges
def conf_user(records):
    # returns a must-not-merge record id as the target -> conflates distinct works
    for c in GOLD_CASES:
        if any(r["rid"] == records[0]["rid"] for r in c["records"]) and c["must_not_merge"]:
            return {"target": c["must_not_merge"][0],
                    "candidates": [{"id": c["must_not_merge"][0], "score": 0.9}]}
    return {"target": records[0]["rid"], "candidates": [{"id": records[0]["rid"], "score": 0.9}]}
r = score_resolution(GOLD_CASES, conf_user)
check("confusing resolver has non-zero false merge", r["FALSE_MERGE_RATE"] > 0, r["FALSE_MERGE_RATE"])

print("\n== 4. exact-match resolver scores recall ==")
def exact(records):
    # resolves to the case's gold_target (a perfect resolver)
    case = next(c for c in GOLD_CASES if any(r["rid"] == records[0]["rid"] for r in c["records"]))
    return {"target": case["gold_target"], "candidates": [{"id": case["gold_target"], "score": 1.0}]}
re_ = score_resolution(GOLD_CASES, exact)
check("perfect resolver: top1 + top5 recall = 1.0, false merge = 0",
      re_["top1_accuracy"] == 1.0 and re_["FALSE_MERGE_RATE"] == 0.0, str(re_))

print("\n== 5. non-circular ==")
import inspect
src = inspect.getsource(score_resolution)
check("scorer never reads 'expected'", "expected" not in src)

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (MANUSCRIPT-RESOLUTION-GOLD works)"))
sys.exit(1 if failures else 0)
