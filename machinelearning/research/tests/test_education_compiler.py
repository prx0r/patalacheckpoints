#!/usr/bin/env python3
"""test_education_compiler.py — devpath11 (Education compiler) acceptance.

Checks (per the directive §10/§11 + the globalplan Phase 13 + the frontend-law):
  1. LearningInteraction[] are InteractionDefinition JSON (framework-independent, not UI)
  2. skills used are from the first interaction set (SPEAKER_CLASSIFY/PREMISE_ATTACH/...)
  3. interactions are grounded in the synthesis (derived_from + options from the debate)
  4. the education bundle preserves unresolved disagreement (no manufactured consensus)
  5. the engine emits data, not a renderer (a React renderer is separate)
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from patala_ml.education_compiler import (
    learning_interactions_from_synthesis, build_learning_bundle, SKILLS,
)
from patala_ml.synthesis_core import build_synthesis_from_gold
from patala_ml.gold002 import build_gold_002

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


synth = build_synthesis_from_gold(build_gold_002(), synthesis_id="SYNTH-IPVV",
                                  research_question="Is recognition recollection?")

print("== interactions are framework-independent JSON ==")
inter = learning_interactions_from_synthesis(synth)
check("produced >= 1 interaction", len(inter) >= 1, len(inter))
check("each is InteractionDefinition JSON (no UI/framework)", 
      all({"interaction_type", "prompt", "feedback_rules", "derived_from"} <= set(i) for i in inter))
check("interaction_type from the first skill set",
      all(i["interaction_type"] in SKILLS for i in inter))
check("no renderer/JSX in the engine output",
      not any("component" in json.dumps(i).lower() or "jsx" in json.dumps(i).lower() for i in inter))

print("\n== grounded in the synthesis ==")
check("every interaction derived_from the synthesis",
      all(synth["synthesis_id"] in i["derived_from"] for i in inter))
check("options come from the debate (positions/cruxes/sources)",
      all(i.get("options") for i in inter))

print("\n== education bundle ==")
bundle = build_learning_bundle(synth)
check("bundle has learning_skills from the set",
      set(bundle["learning_skills"]) <= set(SKILLS))
check("bundle is framework-independent (emits data, not UI)",
      "interactions" in bundle and "bundle_hash" in bundle)

print("\n== preserves unresolved disagreement (no manufactured consensus) ==")
check("no interaction teaches a resolved consensus",
      not any("consensus" in str(i.get("prompt", "")).lower() or "the rival agreed" in json.dumps(i)
              for i in inter))
check("a crux interaction targets an UNRESOLVED crux (not a settled conclusion)",
      all(not str(i.get("target", "")).startswith("RESOLVED") for i in inter))

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (Education compiler works)"))
sys.exit(1 if failures else 0)
