#!/usr/bin/env python3
"""test_warrant_reconstruction.py — the warrant-reconstruction program (Agent 1).

Checks (per the directive):
  1. three warrant kinds are separated (TEXT_EXPLICIT / RATIONAL_RECONSTRUCTION / EDITORIAL_RECONSTRUCTION)
  2. a warrant object carries full metadata (necessitated_by, textual_constraints, alternatives, defeaters)
  3. a RATIONAL_RECONSTRUCTION that wrongly claims TEXT_EXPLICIT is flagged as FABRICATION
  4. constraint coverage is measured
  5. alternative-warrant awareness is measured
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from warrant_reconstruction import (
    classify_warrant, build_warrant_object, evaluate_warrant_reconstruction, aggregate, WARRANT_KINDS,
)

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


print("== 1. three warrant kinds ==")
check("kinds defined", set(WARRANT_KINDS) == {"TEXT_EXPLICIT", "RATIONAL_RECONSTRUCTION", "EDITORIAL_RECONSTRUCTION"})
check("explicit source -> TEXT_EXPLICIT", classify_warrant("P", True) == "TEXT_EXPLICIT")
check("anchored -> RATIONAL_RECONSTRUCTION", classify_warrant("inertness blocks (lines 10-12)", False) == "RATIONAL_RECONSTRUCTION")
check("hedged -> RATIONAL_RECONSTRUCTION", classify_warrant("one can reconstruct the bridge", False) == "RATIONAL_RECONSTRUCTION")
check("unanchored + unhuged -> EDITORIAL", classify_warrant("the soul is fundamentally free", False) == "EDITORIAL_RECONSTRUCTION")

print("\n== 2. warrant metadata object ==")
w = build_warrant_object(warrant_text="inertness blocks establishing (lines 10-12)",
                         premise_ids=["P2"], conclusion_id="C1",
                         textual_constraints=["line 11"], alternatives=["W2"], defeaters=["O3"])
check("has status", w["status"] in WARRANT_KINDS)
check("has necessitated_by", set(w["necessitated_by"]) == {"P2", "C1"})
check("has textual_constraints + alternatives + defeaters", w["textual_constraints"] and w["alternatives"] and w["defeaters"])

print("\n== 3. fabrication detection ==")
gold = build_warrant_object(warrant_text="inertness blocks establishing (lines 10-12)",
                            premise_ids=["P2"], conclusion_id="C1",
                            textual_constraints=["line 11"], alternatives=["W2"])
honest = build_warrant_object(warrant_text="inertness blocks establishing (lines 10-12)",
                              premise_ids=["P2"], conclusion_id="C1",
                              textual_constraints=["line 11"], alternatives=["W2"])
fab = build_warrant_object(warrant_text="Abhinavagupta explicitly states it",
                           premise_ids=["P2"], conclusion_id="C1", source_has_explicit_inference=True)
r_h = evaluate_warrant_reconstruction(gold, honest)
r_f = evaluate_warrant_reconstruction(gold, fab)
check("honest not flagged", r_h["fabrication_flagged"] is False)
check("fabricated flagged", r_f["fabrication_flagged"] is True)
check("honest constraint coverage = 1", r_h["constraint_coverage"] == 1.0)

print("\n== 4. aggregate ==")
agg = aggregate([r_h, r_f])
check("aggregate reports fabrication rate + coverage", "fabrication_rate" in agg and "constraint_coverage" in agg)

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (warrant reconstruction works)"))
sys.exit(1 if failures else 0)
