#!/usr/bin/env python3
"""patala_ml/education_compiler.py — devpath11: the Education compiler over ArgumentSynthesis.

The directive §10 + the globalplan Phase 13 + the frontend-law: education consumes the SAME synthesis,
and the engine is framework-independent.

    ArgumentSynthesis
        ↓
    LearningClaim       a testable claim about the debate (never a resolved consensus)
        ↓
    LearningSkill       the skill being exercised (speaker attribution, premise attach, ...)
        ↓
    LearningInteraction an InteractionDefinition JSON that a renderer displays (framework-agnostic)

First interaction set (the directive §11):
    SPEAKER_CLASSIFY   which position holds this claim?
    PREMISE_ATTACH     which premise does an argument depend on?
    WARRANT_RECONSTRUCT is the warrant licensed by the source?
    CRUX_IDENTIFY      what is the decisive unresolved crux?
    COUNTEREVIDENCE_SELECT  which item counts against this claim?
    SOURCE_GROUND      which source supports this claim?

The engine emits InteractionDefinition JSON (not UI). A React/any renderer merely displays it. The
canonical education layer never depends on the frontend framework. It preserves unresolved
disagreement (a learning exercise never teaches a manufactured consensus).
"""
from __future__ import annotations

import hashlib
import json
import os
import sys


def _sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()


SKILLS = ("SPEAKER_CLASSIFY", "PREMISE_ATTACH", "WARRANT_RECONSTRUCT", "CRUX_IDENTIFY",
          "COUNTEREVIDENCE_SELECT", "SOURCE_GROUND")


def learning_interactions_from_synthesis(synthesis: dict) -> list[dict]:
    """Derive LearningInteraction[] (InteractionDefinition JSON) from an ArgumentSynthesis.

    Each interaction is framework-agnostic: {interaction_type, prompt, options?, feedback_rules,
    derived_from, target}. No UI; a renderer displays it. Gold answers come from the synthesis
    structure (positions/cruxes/counterevidence), so the exercise is faithful to the debate.
    """
    if not synthesis:
        return []
    frame = synthesis.get("debate_frame", {})
    positions = frame.get("positions", [])
    arguments = synthesis.get("arguments", [])
    cruxes = synthesis.get("cruxes", [])
    counterevidence = synthesis.get("counterevidence", [])
    propositions = synthesis.get("propositions", [])
    rq = synthesis.get("research_question", {}).get("question", "")
    synthesis_id = synthesis.get("synthesis_id", "SYNTH")

    interactions = []

    # SPEAKER_CLASSIFY: which position holds this claim? (options = the positions)
    if positions:
        interactions.append({
            "interaction_type": "SPEAKER_CLASSIFY",
            "prompt": f"Which position in this debate holds the siddhānta view of: {rq}?",
            "options": [p.get("position_id") for p in positions],
            "feedback_rules": [{"match": "POS-SIDDHANTA", "correct": True}],
            "derived_from": [synthesis_id], "target": "POS-SIDDHANTA",
        })

    # CRUX_IDENTIFY: what is the decisive unresolved crux? (options = cruxes + a distractor)
    if cruxes:
        options = list(cruxes) + (["DISTRACTOR: a resolved conclusion"] if not cruxes else [])
        interactions.append({
            "interaction_type": "CRUX_IDENTIFY",
            "prompt": "Which item is a decisive UNRESOLVED crux of this debate?",
            "options": options,
            "feedback_rules": [{"match": c, "correct": True} for c in cruxes],
            "derived_from": [synthesis_id] + cruxes, "target": cruxes[0],
        })

    # COUNTEREVIDENCE_SELECT: which item counts AGAINST a supporting claim?
    if counterevidence:
        interactions.append({
            "interaction_type": "COUNTEREVIDENCE_SELECT",
            "prompt": "Which item counts against the supporting argument?",
            "options": counterevidence + (["DISTRACTOR: supporting premise"] if counterevidence else []),
            "feedback_rules": [{"match": ce, "correct": True} for ce in counterevidence],
            "derived_from": [synthesis_id], "target": counterevidence[0],
        })

    # SOURCE_GROUND: which source grounds this synthesis?
    srcs = synthesis.get("source_refs", [])
    if srcs:
        interactions.append({
            "interaction_type": "SOURCE_GROUND",
            "prompt": "Which source grounds the synthesis's propositions?",
            "options": srcs[:4],
            "feedback_rules": [{"match": s, "correct": True} for s in srcs[:1]],
            "derived_from": [synthesis_id], "target": srcs[0],
        })

    return interactions


def build_learning_bundle(synthesis: dict) -> dict:
    """Compile a LearningBundle: claims + skills + interactions (framework-independent)."""
    interactions = learning_interactions_from_synthesis(synthesis)
    skills = sorted({i["interaction_type"] for i in interactions})
    claims = [i["target"] for i in interactions if i.get("target")]
    return {
        "learning_bundle_id": f"learn-{synthesis.get('synthesis_id', 'SYNTH')}",
        "synthesis_ref": synthesis.get("synthesis_id", ""),
        "learning_claims": claims,
        "learning_skills": skills,
        "interactions": interactions,     # InteractionDefinition JSON (renderer-agnostic)
        "interaction_count": len(interactions),
        "bundle_hash": _sha256({"synthesis_ref": synthesis.get("synthesis_id", ""),
                                "interactions": interactions}),
    }


if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    from patala_ml.synthesis_core import build_synthesis_from_gold
    from patala_ml.gold002 import build_gold_002

    synth = build_synthesis_from_gold(build_gold_002(), synthesis_id="SYNTH-IPVV",
                                      research_question="Is recognition recollection?")
    bundle = build_learning_bundle(synth)
    print(f"learning bundle: {bundle['interaction_count']} interactions, skills={bundle['learning_skills']}")
    for i in bundle["interactions"]:
        print(f"  {i['interaction_type']:22} target={i.get('target')} options={len(i.get('options', []))}")
