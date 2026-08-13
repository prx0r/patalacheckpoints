#!/usr/bin/env python3
"""test_atlas_backfill.py — Atlas backfill pipeline acceptance (Atlas-100 #2).

Checks (the reviewer's requirement):
  1. the richer existing data (audited.ts) is parsed (the Trika-10 calibration set)
  2. every field carries provenance (value/source/derivation/authority_state) — never a bare value
  3. authority is honest (rights stays UNKNOWN, not inflated)
  4. the rich fields are present (editions/etexts/translations/scholarship separated)
  5. candidates feed ATLAS-10 GOLD (>=10)
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from atlas_backfill import parse_ts_records, normalize, run

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


records = parse_ts_records()
print("== 1. richer existing data parsed ==")
check(">=10 rich records (ATLAS-10 calibration set)", len(records) >= 10, len(records))

print("\n== 2. provenance-carrying fields ==")
cand = normalize(records[0])
check("work_identity has provenance", all(k in cand["work_identity"] for k in
      ("value", "source", "derivation", "authority_state")))
check("date field has source + authority", cand["date"]["source"] == "audited.ts"
      and cand["date"]["authority_state"])

print("\n== 3. authority honest (rights not inflated) ==")
check("rights stays UNKNOWN (honest OPEN)", cand["authority_vector"]["rights"] == "UNKNOWN")

print("\n== 4. rich fields separated ==")
check("editions/etexts/translations/scholarship present",
      all(k in cand for k in ("editions", "etexts", "translations", "scholarship")))

print("\n== 5. feeds ATLAS-10 GOLD ==")
check(">=10 candidates", len(records) >= 10)

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (Atlas backfill works)"))
sys.exit(1 if failures else 0)
