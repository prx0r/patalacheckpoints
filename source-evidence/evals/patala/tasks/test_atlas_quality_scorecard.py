#!/usr/bin/env python3
"""test_atlas_quality_scorecard.py — the ATLAS quality scorecard acceptance (Atlas-100 #3/#5).

Checks:
  1. per-dimension PASS/OPEN/FAIL, not a single confidence score
  2. a completeness vector (identity/authorship/date/editions/translations/scholarship)
  3. rights stays OPEN (honest) when unknown
  4. consumes the backfill candidates (>=10 works)
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from atlas_quality_scorecard import run, score_work

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


r = run()
print("== 1. per-dimension, not one score ==")
s0 = r["per_work"][0]
dims = s0["dimensions"]
check("per-dimension dimensions", all(k in dims for k in
      ("IDENTITY", "AUTHORSHIP", "DATE", "EDITION_COVERAGE", "TRANSLATION", "RIGHTS")))

print("\n== 2. completeness vector ==")
cv = s0["completeness_vector"]
check("completeness vector has the ATLAS-100 fields", all(k in cv for k in
      ("identity", "authorship", "date", "editions", "translations", "scholarship")))

print("\n== 3. rights honest (OPEN when unknown) ==")
check("rights OPEN (not inflated)", dims["RIGHTS"] == "OPEN")

print("\n== 4. consumes >=10 works ==")
check("works >= 10", r["works"] >= 10, r["works"])

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (Atlas quality scorecard works)"))
sys.exit(1 if failures else 0)
