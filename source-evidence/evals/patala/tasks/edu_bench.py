#!/usr/bin/env python3
"""source-evidence/evals/patala/tasks/edu_bench.py — EDU-BENCH-v1 (Agent 1; the education evaluator).

The directive: education is even less mature than essay. Eight interactions prove the graph can be
projected into exercises, but education quality has almost no empirical evidence. The four unsolved
problems:

    1. SKILL VALIDITY        does an exercise test CRUX_IDENTIFICATION, not 'recognize wording seen
                             20 seconds ago'? (a skill-tag is not a valid exercise)
    2. MISCONCEPTION DIAGNOSIS  does a wrong answer tell us WHY the learner failed? (every option
                             must map to a misconception, not just be a wrong label)
    3. LEARNING PROGRESSION  are exercises a sequence (read->choose->classify->attach->manipulate->
                             construct->transfer) with prerequisites, not a random set?
    4. TRANSFER              is the skill tested on UNSEEN material, not the memorized example?

The scorer is deterministic + structural. It never asserts a lesson 'works'; it measures whether the
interaction OBJECTS are valid (epistemic), whether the sequence has progression (pedagogical), and
whether transfer is representable.
"""
from __future__ import annotations

import json
import re

# the progression ladder (from the education vision): increasing evidential strength
PROGRESSION = ["read", "choose", "classify", "attach", "manipulate", "construct", "transfer"]

# skills that are 'valid' if the interaction actually requires discriminating structure
_STRUCTURAL_SKILLS = {"CLASSIFY_SPEAKER", "ATTACH_PREMISE", "RECONSTRUCT_WARRANT", "IDENTIFY_CRUX",
                      "IDENTIFY_ATTACK", "QUALIFY_SCOPE", "GROUND_SOURCE", "FOLLOW_INFERENCE",
                      "COMPARE_POSITION", "EVALUATE_TRANSLATION", "SYNTHESIZE_DEBATE"}


def _has_discriminating_structure(interaction: dict) -> bool:
    """An interaction is structurally valid if its options encode real misconceptions, not just
    right/wrong wording. I.e. there are distractors that violate a structural fact."""
    opts = interaction.get("options", [])
    distractors = [o for o in opts if not o.get("correct")]
    # a valid diagnostic interaction has >=1 distractor that carries a misconception mapping
    return any(o.get("misconception") for o in distractors)


def audit_interactions(interactions: list[dict], *, skill_field="skill",
                       misconception_field="misconception") -> dict:
    """Score a set of education interactions.

    Returns per-interaction validity + aggregate + findings.
    """
    findings = []
    per_int = []
    for it in interactions:
        skill = it.get(skill_field, "")
        opts = it.get("options", [])
        # 1. SKILL VALIDITY: the skill is a real structural skill, and the interaction discriminates
        skill_valid = skill in _STRUCTURAL_SKILLS
        discriminating = _has_discriminating_structure(it)
        # 2. MISCONCEPTION DIAGNOSIS: at least one distractor carries a misconception mapping
        diag = any(o.get(misconception_field) for o in opts if not o.get("correct"))
        # the interaction must have exactly one correct option (else not a diagnostic)
        n_correct = sum(1 for o in opts if o.get("correct"))
        per_int.append({
            "interaction_id": it.get("interaction_id", "?"),
            "skill": skill,
            "skill_valid": skill_valid,
            "discriminating": discriminating,
            "misconception_diagnostic": diag,
            "single_correct": n_correct == 1,
            "epistemic_valid": skill_valid and discriminating and diag and n_correct == 1,
        })

    # 3. LEARNING PROGRESSION: do the interactions, in order, follow the progression ladder?
    steps = [it.get("step", "").lower() for it in interactions if it.get("step")]
    progress_score = 0
    last = -1
    for s in steps:
        if s in PROGRESSION:
            idx = PROGRESSION.index(s)
            if idx >= last:
                progress_score += 1
                last = idx
    has_progression = progress_score >= min(3, len([s for s in steps if s in PROGRESSION]))

    # 4. TRANSFER representability: is there a transfer interaction or a declared transfer target?
    has_transfer = any(it.get("step", "").lower() == "transfer" or it.get("transfer")
                       for it in interactions)

    if not any(i["epistemic_valid"] for i in per_int):
        findings.append("EDU_SKILL_VALIDITY: no interaction is epistemically valid (must test a real "
                        "structural skill, discriminate structure, diagnose a misconception, one correct).")
    if not has_progression:
        findings.append("EDU_PROGRESSION: interactions do not follow the read->choose->classify->"
                        "attach->manipulate->construct->transfer ladder (may be a random set, not a lesson).")
    if not has_transfer:
        findings.append("EDU_TRANSFER: no transfer interaction/target — mastery may be memorized example "
                        "recognition, not a reasoning skill.")

    return {
        "interactions": per_int,
        "aggregate": {
            "n": len(interactions),
            "epistemic_valid_rate": round(sum(i["epistemic_valid"] for i in per_int) / len(per_int), 4) if per_int else None,
            "skill_valid_rate": round(sum(i["skill_valid"] for i in per_int) / len(per_int), 4) if per_int else None,
            "misconception_diagnostic_rate": round(sum(i["misconception_diagnostic"] for i in per_int) / len(per_int), 4) if per_int else None,
            "has_progression": has_progression,
            "has_transfer": has_transfer,
        },
        "findings": findings,
    }


if __name__ == "__main__":
    # valid: a diagnostic interaction that discriminates structure and diagnoses a misconception
    good = [
        {"interaction_id": "LI-1", "skill": "IDENTIFY_CRUX", "step": "choose",
         "options": [
             {"text": "the self-luminosity of the establishing act", "correct": True},
             {"text": "a settled conclusion", "correct": False, "misconception": "OPEN_AS_RESOLVED"},
         ]},
        {"interaction_id": "LI-2", "skill": "ATTACH_PREMISE", "step": "attach",
         "options": [
             {"text": "P2: inert cannot establish", "correct": True},
             {"text": "the conclusion", "correct": False, "misconception": "ARGUMENT_DIRECTION_REVERSAL"},
         ]},
        {"interaction_id": "LI-3", "skill": "CLASSIFY_SPEAKER", "step": "transfer",
         "transfer": "classify speaker on an unseen Nyāya passage",
         "options": [
             {"text": "the opponent", "correct": True},
             {"text": "Abhinavagupta", "correct": False, "misconception": "SPEAKER_COLLAPSE"},
         ]},
    ]
    bad = [
        {"interaction_id": "Q1", "skill": "RECALL", "step": "read",
         "options": [{"text": "vimarśa", "correct": True}, {"text": "apoha", "correct": False}]},
        {"interaction_id": "Q2", "skill": "RECALL", "step": "read",
         "options": [{"text": "spanda", "correct": True}, {"text": "mala", "correct": False}]},
    ]
    rg = audit_interactions(good)
    rb = audit_interactions(bad)
    print("good set:", json.dumps(rg["aggregate"]))
    print("bad set: ", json.dumps(rb["aggregate"]))
    print("good findings:", rg["findings"])
    print("bad findings: ", rb["findings"])
    assert rg["aggregate"]["epistemic_valid_rate"] == 1.0
    assert rg["aggregate"]["has_transfer"] is True
    assert rb["aggregate"]["epistemic_valid_rate"] == 0.0
    assert rb["aggregate"]["has_transfer"] is False
    print("SELF-TEST PASS (edu bench separates valid diagnostic interactions from recall quizzes)")
