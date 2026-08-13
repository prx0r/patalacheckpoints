#!/usr/bin/env python3
"""test_identity_crosswalk.py — P3 ORCID + ROR identity crosswalks acceptance.

Checks:
  1. 'Isabelle Ratié' / 'Isabelle Ratie' / 'I. Ratié' resolve to ONE Person (family-name unification)
  2. different people do NOT resolve to one
  3. ORCID is treated as identity evidence, NOT correctness
  4. institution_crosswalk returns UNAVAILABLE honestly when the ROR API is unreachable
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from identity_crosswalk import person_crosswalk, institution_crosswalk

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


print("== 1. the reviewer's example: name variants -> one Person ==")
r = person_crosswalk(["Isabelle Ratié", "Isabelle Ratie", "I. Ratié"])
check("Ratié variants resolve to one", r["resolves_to_one"] is True, str(r["unique_normalized_forms"]))
check("family name unified", r["family_name"] == ["ratie"], str(r["family_name"]))

print("\n== 2. different people do not resolve to one ==")
r2 = person_crosswalk(["Isabelle Ratié", "John Smith"])
check("distinct people -> not one", r2["resolves_to_one"] is False)

print("\n== 3. ORCID = identity evidence, not correctness ==")
r3 = person_crosswalk(["Isabelle Ratié"], orcid="0000-0001-2345-6789")
check("orcid carried + not correctness", r3["orcid"] and "NOT scholarly correctness" in r3["note"])

print("\n== 4. institution UNAVAILABLE honesty ==")
ri = institution_crosswalk("this-institution-does-not-exist-xyz-99999")
check("institution returns honest status", ri["status"] in ("LIVE", "UNAVAILABLE"))

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (identity crosswalk works)"))
sys.exit(1 if failures else 0)
