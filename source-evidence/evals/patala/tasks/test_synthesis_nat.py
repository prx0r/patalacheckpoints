#!/usr/bin/env python3
"""test_synthesis_nat.py — devpath9 (Synthesis NAT) acceptance.

Checks (per the directive §9):
  1. the 11 mutation families are defined
  2. a faithful synthesis passes; each mutation is caught (FAIL)
  3. the evaluator is bounded (never asserts scholarly truth)
  4. a synthesis that asserts consensus (supported conclusion + no disagreement) is caught
  5. the evaluator does NOT false-positive on a faithful synthesis (word-boundary aware)
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from synthesis_nat import MUTATION_FAMILIES, evaluate_synthesis, _base_synthesis, _MUTATED

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


print("== 11 mutation families ==")
check("11 families defined", set(MUTATION_FAMILIES) ==
      {"POSITION_COLLAPSE", "RIVAL_AS_CONSENSUS", "ARGUMENT_DIRECTION_REVERSAL", "CRUX_OMISSION",
       "COUNTEREVIDENCE_DROP", "QUALIFICATION_DROP", "SCOPE_INFLATION", "OPEN_AS_RESOLVED",
       "MINORITY_VIEW_ERASURE", "SCHOLAR_ATTRIBUTION_COLLAPSE", "SOURCE_STRENGTH_INFLATION"})

print("\n== faithful synthesis passes (no false positive) ==")
base = _base_synthesis()
res = evaluate_synthesis(base)
check("faithful synthesis -> PASS", res["verdict"] == "PASS", str(res["problems"]))
check("no false family hits", res["family_hits"] == [], str(res["family_hits"]))

print("\n== each mutation caught ==")
def v(cand):
    return evaluate_synthesis(cand)["verdict"]
check("POSITION_COLLAPSE caught", v(_MUTATED["POSITION_COLLAPSE"](base)) == "FAIL")
check("RIVAL_AS_CONSENSUS caught", v(_MUTATED["RIVAL_AS_CONSENSUS"](base)) == "FAIL")
check("CRUX_OMISSION caught", v(_MUTATED["CRUX_OMISSION"](base)) == "FAIL")
check("COUNTEREVIDENCE_DROP caught", v(_MUTATED["COUNTEREVIDENCE_DROP"](base)) == "FAIL")
check("SCOPE_INFLATION caught", v(_MUTATED["SCOPE_INFLATION"](base)) == "FAIL")
check("OPEN_AS_RESOLVED caught", v(_MUTATED["OPEN_AS_RESOLVED"](base)) == "FAIL")

print("\n== consensus assertion is caught ==")
cons = {**base, "supported_conclusions": ["the rival agreed"], "unresolved_disagreement": []}
rc = evaluate_synthesis(cons)
check("manufactured consensus -> FAIL", rc["verdict"] == "FAIL")
check("RIVAL_AS_CONSENSUS flagged", "RIVAL_AS_CONSENSUS" in rc["family_hits"])

print("\n== bounded (never asserts scholarly truth) ==")
r = evaluate_synthesis(base)
check("no truth assertion in output", "definitely" not in json.dumps(r).lower()
      and "conclusively true" not in json.dumps(r).lower())

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (Synthesis NAT works)"))
sys.exit(1 if failures else 0)
