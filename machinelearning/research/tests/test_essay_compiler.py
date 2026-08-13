#!/usr/bin/env python3
"""test_essay_compiler.py — devpath10 (G6) Essay compiler acceptance.

Checks (per the directive §10 + the globalplan Phase 12):
  1. EssayPlan + EssayClaim[] are derived from an ArgumentSynthesis (not invented)
  2. every claim is grounded: derived_from a synthesis element + has source_refs
  3. claims are role-typed (MAIN_THESIS/SUPPORTING/COUNTEREVIDENCE/OPEN_POINT/QUALIFICATION)
  4. compression is QUALIFIED by default (never silently inflated)
  5. an unresolved synthesis does NOT become a resolved essay (disagreement -> OPEN_POINT)
  6. the plan is grounded by construction
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from patala_ml.essay_compiler import essay_claims_from_synthesis, build_essay_plan, CLAIM_ROLES
from patala_ml.synthesis_core import build_synthesis_from_gold
from patala_ml.gold002 import build_gold_002

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


synth = build_synthesis_from_gold(build_gold_002(), synthesis_id="SYNTH-IPVV",
                                  research_question="Is recognition recollection?")

print("== essay claims derived from the synthesis ==")
claims = essay_claims_from_synthesis(synth)
check("produced >= 1 claim", len(claims) >= 1, len(claims))
check("every claim grounded (derived_from non-empty)",
      all(c["derived_from"] for c in claims))
check("every claim has source refs", all(c["source_refs"] for c in claims))
check("every claim has a valid role", all(c["role"] in CLAIM_ROLES for c in claims))
check("compression is QUALIFIED by default", all(c["compression"] == "QUALIFIED" for c in claims))

print("\n== essay plan ==")
plan = build_essay_plan(synth)
check("plan is grounded by construction", plan["grounded"] is True)
check("plan has all sections", set(plan["sections"]) ==
      {"thesis", "supporting", "counterevidence", "open_points"})
check("thesis section has the question-framing claim",
      len(plan["sections"]["thesis"]) == 1 and "What is at issue" in plan["sections"]["thesis"][0]["claim"])

print("\n== unresolved disagreement is NOT resolved in the essay ==")
open_pts = plan["sections"]["open_points"]
check("open_points section non-empty (disagreement preserved)",
      len(open_pts) >= 1, len(open_pts))
check("no claim asserts a resolved consensus conclusion",
      not any("conclusively" in c["claim"] or "the rival agreed" in c["claim"] for c in claims))

print("\n== grounded: no free-floating claim ==")
check("no claim with empty derived_from", not any(not c["derived_from"] for c in claims))
check("every claim's derived_from references the synthesis", 
      all(synth["synthesis_id"] in c["derived_from"] for c in claims))

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (Essay compiler works)"))
sys.exit(1 if failures else 0)
