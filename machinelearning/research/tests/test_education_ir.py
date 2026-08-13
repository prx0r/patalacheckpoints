#!/usr/bin/env python3
"""test_education_ir.py — devpath13 Education IR acceptance.

Checks (per the education vision / PATALA-EDUCATION-SYNTHESIS.md):
  1. four native objects exist: LearningClaim, LearningSkill, LearningInteraction, MasteryEvidence
  2. education is a PROJECTION: every interaction/option resolves downward to canonical objects
  3. the moat: distractors come from real graph neighbors (not LLM-invented) and encode the NAT
     failure taxonomy (wrong answer -> known epistemic neighbor)
  4. compile_interactions(scholarly_object, targets, level) -> LearningPacket
  5. every distractor carries a misconception type (proof-carrying multiple choice)
  6. MasteryEvidence is evidence-bearing (has response/correctness/conditions), not a bare score
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from patala_ml.education_ir import (
    compile_interactions, LearningClaim, Misconception, MasteryEvidence,
    SKILLS, MISCONCEPTION_TYPES,
)

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


OBJ = {
    "object_id": "VERTICAL-1",
    "research_question": "Can the determination establish an external object?",
    "propositions": [
        {"id": "P1", "commitment": "the determination is error-form", "speaker": "author"},
        {"id": "P2", "commitment": "an inert part cannot establish", "speaker": "author"},
        {"id": "P3", "commitment": "the pure self-experience is not external-natured", "speaker": "author"},
        {"id": "O3", "commitment": "as fire burns wood though inert, so the determination establishes",
         "speaker": "opponent"},
    ],
    "arguments": [{"inferences": [{"inference_id": "INF-1", "premise_ids": ["P1", "P2", "P3"],
                                    "conclusion_ids": ["C1"]}]}],
    "cruxes": [{"crux_id": "CRUX-1", "question": "Does establishing require the self-luminous awareness?"}],
    "boundary": {"does_not_establish": ["a universal Self"]},
    "source_refs": ["pt:passage:ipvv:chunkM"],
    "epistemic_ceiling": "UNRESOLVED",
}

print("== 1. four native objects ==")
pkt = compile_interactions(OBJ, ["CLASSIFY_SPEAKER", "ATTACH_PREMISE", "IDENTIFY_CRUX",
                                 "QUALIFY_SCOPE", "RECONSTRUCT_WARRANT"])
check("LearningClaim emitted", all("learning_claim_id" in c and "derived_from" in c for c in pkt["learning_claims"]))
check("LearningSkill (from SKILLS)", set(pkt["learning_skills"]).issubset(set(SKILLS)),
      str(pkt["learning_skills"]))
check("LearningInteraction emitted", all("interaction_id" in it and "skill" in it for it in pkt["interactions"]))
check("MasteryEvidence object", MasteryEvidence("u", "CLASSIFY_SPEAKER", "LC-1", "LI-1", "P1", "PASS").emit()["correctness"] == "PASS")

print("\n== 2. education is a projection (options derive from graph objects) ==")
all_options = [o for it in pkt["interactions"] for o in it["options"]]
check("every distractor has a misconception type (proof-carrying)",
      all(o["misconception"] in MISCONCEPTION_TYPES for o in all_options if not o["correct"]),
      str([(o.get("misconception")) for o in all_options if not o["correct"]]))
check("correct options carry no misconception", all(not o.get("misconception") for o in all_options if o["correct"]))
check("options derive from real graph neighbors (derives_from set)",
      all(o.get("derives_from") for o in all_options))

print("\n== 3. the moat: wrong answer -> known epistemic neighbor ==")
mc_types = {o["misconception"] for o in all_options if not o["correct"]}
check("distractors encode >=3 NAT misconception families",
      len(mc_types) >= 3, str(mc_types))
check("SPEAKER_COLLAPSE encoded", "SPEAKER_COLLAPSE" in mc_types)
check("OPEN_AS_RESOLVED encoded", "OPEN_AS_RESOLVED" in mc_types)

print("\n== 4. LearningPacket shape ==")
check("packet has interaction_count", pkt["interaction_count"] >= 4)
check("packet has misconceptions list", len(pkt["misconceptions"]) >= 4)
check("packet honors design law", "projection of Pāṭala objects" in pkt["design_law"])
check("packet moat declared", "epistemic neighbor" in pkt["moat"])

print("\n== 5. Misconception first-class ==")
m = Misconception("MC-1", "SCOPE_INFLATION", "generalizing per-act to universal",
                  confuses=["per-act", "universal"], detected_by=["LI-1"])
em = m.emit()
check("misconception has type + confuses + detected_by",
      em["type"] == "SCOPE_INFLATION" and em["confuses"] and em["detected_by"])

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (Education IR works)"))
sys.exit(1 if failures else 0)
