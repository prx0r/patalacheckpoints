#!/usr/bin/env python3
"""test_atlas_qa_audit.py — P5 continuous semantic QA on Atlas work objects.

Checks:
  1. the audit reads real Atlas work records
  2. it computes field completeness (the ATLAS-100 milestone fields)
  3. it flags authority inflation (verified/strong authority with no text source)
  4. it flags rights honesty (restricted/unknown rights but a translation claimed)
  5. it aggregates (works_audited, inflation_rate)
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from atlas_qa_audit import audit_work, audit_all, REQUIRED_FIELDS

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


print("== 1. audits real Atlas records ==")
res = audit_all()
check("reads real records", res["works_audited"] > 0, res["works_audited"])

print("\n== 2. field completeness (ATLAS-100 milestone) ==")
check("computes completeness over required fields",
      0 <= res["avg_field_completeness"] <= len(REQUIRED_FIELDS), res["avg_field_completeness"])

print("\n== 3. authority inflation flag ==")
# a record claiming verified with no source -> inflated
inflated = audit_work({"id": "x", "title": "X", "verified": True})
check("verified-without-source flagged", any("AUTHORITY_INFLATION" in f for f in inflated["findings"]))
# a rich record with a real source -> not inflated
rich = audit_work({"id": "y", "title": "Y", "verified": True, "textSources": [{"type": "edition"}]})
check("verified-with-source not inflated", not any("AUTHORITY_INFLATION" in f for f in rich["findings"]))

print("\n== 4. rights honesty ==")
r = audit_work({"id": "z", "title": "Z", "rights": {"status": "restricted"}, "translation_status": "complete"})
check("restricted-rights-with-translation flagged", any("RIGHTS_HONESTY" in f for f in r["findings"]))

print("\n== 5. aggregation ==")
check("aggregate reports count + rate", res["works_audited"] > 0 and 0 <= res["authority_inflation_rate"] <= 1)

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (P5 Atlas QA audit works)"))
sys.exit(1 if failures else 0)
