#!/usr/bin/env python3
"""test_aspic_adapter.py — validation of the ARG-002 v2 -> ASPIC+ projection + pilot semantics."""
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.aspic_adapter import project_arg002, run_arg002_aspic, _build_af, grounded_acceptable

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)

print("== projection (representational fidelity) ==")
proj = project_arg002()
check("has the three atoms + not_constructed", set(proj["propositions"]) == {"art","constructed","vikalpa","not_constructed"})
check("objection enters only as the defeasible rule r_opp (not a fact)",
      proj["rules"][0]["label"] == "r_opp" and proj["rules"][0]["strict"] is False and "art" in proj["facts"])
check("reconstructed warrant is NOT a fact",
      all("IMPL" not in p for p in proj["facts"]) and any("blocking" in n for n in proj["fidelity_notes"]))
check("contraries on constructed", ("constructed","not_constructed") in proj["contraries"])

print("\n== abstract AF construction (no infinite regen) ==")
af0 = _build_af(proj, include_defeater=False)
af1 = _build_af(proj, include_defeater=True)
check("no-defeater AF is finite", len(af0["arguments"]) == 3, str(len(af0["arguments"])))  # art, constructed, vikalpa
check("with-defeater AF is finite", len(af1["arguments"]) == 4, str(len(af1["arguments"])))  # + not_constructed

print("\n== pilot semantics match the expected result ==")
ra = run_arg002_aspic(False)
check("Run A (no defeater): vikalpa acceptable", ra["vikalpa_acceptable"] is True, str(ra["acceptable_conclusions"]))
rb = run_arg002_aspic(True)
check("Run B (with defeater): vikalpa NOT acceptable", rb["vikalpa_acceptable"] is False, str(rb["acceptable_conclusions"]))
check("Run B: not_constructed acceptable", "not_constructed" in rb["acceptable_conclusions"])
check("Run B: art still acceptable (shared ground)", "art" in rb["acceptable_conclusions"])

print(f"\n=== RESULT: {len(failures)} fail ===")
sys.exit(1 if failures else 0)
