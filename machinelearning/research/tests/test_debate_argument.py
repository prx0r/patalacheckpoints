#!/usr/bin/env python3
"""test_debate_argument.py — the DebateArgument gold standard (the reflexion debate).

The end-goal structure for logical arguments/essays (from research-library LOGICAL-ARGUMENT-1 +
PAPER-FRAME): a live dialectic where candidates contend through rounds, each round a unit with a
syllogism core + support + falsifier + verdict, resolving honestly.

Validates that the imported DEBATE-REFLEXIVITY gold is a sound DebateArgument:
  - gold_kind, >=2 candidates, >=3 rounds, resolution
  - every round has pratijna + hetu + a valid verdict
  - the resolution is present and honest
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "experiments"))
from check_debate_argument import check_debate

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


print("== DEBATE-REFLEXIVITY is a valid DebateArgument gold standard ==")
path = os.path.join(ROOT, "benchmarks/v0/structure/DEBATE-REFLEXIVITY.json")
check("gold exists", os.path.exists(path))
if os.path.exists(path):
    r = check_debate(path)
    check("validator passes (candidates/rounds/verdicts/resolution)", r["ok"], str(r["problems"]))
    d = json.load(open(path))
    check("is a DebateArgument", d.get("gold_kind") == "DebateArgument")
    check("has >=2 candidates", r["n_candidates"] >= 2, str(r["n_candidates"]))
    check("has >=3 rounds (a real dialectic)", r["n_rounds"] >= 3, str(r["n_rounds"]))
    check("resolution present", bool(d.get("resolution")))
    # each round has the syllogism spine + honesty
    for rnd in d["rounds"]:
        check(f"round {rnd['round']} has pratijna + hetu + verdict",
              bool(rnd.get("pratijna")) and bool(rnd.get("hetu")) and bool(rnd.get("verdict")))
    # verdicts are all from the honest set
    valid = {"accepted", "accepted-with-risk", "open", "refuted"}
    bad = [rnd["verdict"] for rnd in d["rounds"] if rnd["verdict"] not in valid]
    check("all verdicts are honest (accepted/open/refuted)", not bad, str(bad))

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (DebateArgument gold standard valid)"))
sys.exit(1 if failures else 0)
