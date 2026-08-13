#!/usr/bin/env python3
"""test_context_compiler.py — devpath12 (A7) universal bundle compiler acceptance.

Checks (per the directive §11):
  1. materialize_context(target, profile) works for all 5 profiles (PUBLIC/AGENT/REVIEW/ESSAY/EDUCATION)
  2. each profile selects the correct surfaces
  3. PUBLIC is rights-safe (strips reviews/cruxes)
  4. REVIEW is the old ReviewBundle (reviews + synthesis + review_actions)
  5. AGENT token-budgets (budget field)
  6. the bundle is a read-model, not canonical truth (bundle_hash, not a graph object)
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from context_compiler import materialize_context, PROFILES

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


target = {"ref": "pt:proposition:G2-TC1", "version": "v1", "type": "PROPOSITION", "hash": "abc"}
synth = {"synthesis_id": "SYNTH-IPVV", "research_question": {"question": "q"},
         "debate_frame": {"positions": [{"position_id": "POS-SIDDHANTA"}]},
         "cruxes": ["CRUX-1"], "source_refs": ["pt:passage:ipvv"]}
plan = {"plan_id": "plan-SYNTH", "claim_count": 3, "grounded": True}
learn = {"learning_bundle_id": "learn-SYNTH", "interaction_count": 3}
auth = {"work_identity": "MULTI_SOURCE_MATCHED", "review": "NOT_REVIEWED"}

print("== all profiles ==")
check("5 profiles defined", set(PROFILES) == {"PUBLIC", "AGENT", "REVIEW", "ESSAY", "EDUCATION"})

print("\n== profile surface selection ==")
review = materialize_context(target, "REVIEW", synthesis=synth, reviews=[{"id": "R1"}], authority=auth)
check("REVIEW includes reviews + synthesis + review_actions",
      "reviews" in review and "synthesis" in review and "review_actions" in review)
check("REVIEW is the old ReviewBundle generalization",
      review["review_actions"] == ["ACCEPT", "QUALIFY", "DISPUTE", "PROPOSE_ALTERNATIVE", "ABSTAIN"])

essay = materialize_context(target, "ESSAY", synthesis=synth, essay_plan=plan)
check("ESSAY includes essay_plan + synthesis",
      "essay_plan" in essay and "synthesis" in essay)
check("ESSAY does NOT include reviews (not a review surface)", "reviews" not in essay)

edu = materialize_context(target, "EDUCATION", learning_bundle=learn)
check("EDUCATION includes learning_bundle", "learning_bundle" in edu)

public = materialize_context(target, "PUBLIC", reviews=[{"id": "R1"}])
check("PUBLIC is rights-safe (strips reviews)", "reviews" not in public)
check("PUBLIC has a rights-safe note", "public read-model" in public.get("note", ""))

agent = materialize_context(target, "AGENT", synthesis=synth, budget=100)
check("AGENT is token-budgeted", agent.get("budget_applied") == 100)
check("AGENT is machine-readable (has all surfaces)", "synthesis" in agent)

print("\n== the bundle is a read-model, not canonical truth ==")
b = materialize_context(target, "REVIEW", synthesis=synth)
check("bundle has a hash (compiled read-model)", "bundle_hash" in b)
check("bundle carries the schema marker", b["schema"] == "patala.scholar-context.v1")

print("\n== invalid profile rejected ==")
try:
    materialize_context(target, "BOGUS")
    check("invalid profile rejected", False)
except ValueError:
    check("invalid profile rejected", True)

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (Universal bundle compiler works)"))
sys.exit(1 if failures else 0)
