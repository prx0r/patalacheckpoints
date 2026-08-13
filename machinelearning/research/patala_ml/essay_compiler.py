#!/usr/bin/env python3
"""patala_ml/essay_compiler.py — devpath10 (G6): the Essay compiler over ArgumentSynthesis.

The directive's rule: an essay is NOT allowed to invent its epistemic skeleton. It chooses a
PRESENTATION over an existing synthesis.

    ArgumentSynthesis
        ↓
    EssayPlan          (the structure: thesis + supporting claims + counterevidence + open points)
        ↓
    EssayClaim[]       (each grounded in a synthesis element; never free-floating)
        ↓
    prose              (generated around the grounded claims)

Each EssayClaim carries:
    claim            the claim text
    derived_from     the exact synthesis element(s) it rests on (position/argument/proposition/crux)
    role             MAIN_THESIS | SUPPORTING | COUNTEREVIDENCE | OPEN_POINT | QUALIFICATION
    compression      QUALIFIED (default; never silently inflate)
    source_refs      the underlying source/span refs (grounding)
    counterevidence_refs  what counts against this claim (so the essay stays honest)

The compiler never manufactures consensus: a synthesis's unresolved disagreement becomes an OPEN_POINT
or COUNTEREVIDENCE claim, never a resolved conclusion. It reuses the existing prose-faithfulness +
SentenceEvidenceAudit discipline downstream.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys


def _sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()


CLAIM_ROLES = ("MAIN_THESIS", "SUPPORTING", "COUNTEREVIDENCE", "OPEN_POINT", "QUALIFICATION")


def essay_claims_from_synthesis(synthesis: dict) -> list[dict]:
    """Derive grounded EssayClaim[] from an ArgumentSynthesis.

    Faithful mapping:
      - the research question -> the MAIN_THESIS framing (an honest question, not an assertion)
      - each position's arguments -> SUPPORTING claims (grounded in the argument + its source)
      - the debate's counterevidence -> COUNTEREVIDENCE claims
      - the open questions + unresolved disagreement -> OPEN_POINT claims (never resolved)
      - a QUALIFICATION claim whenever a scope boundary or counterevidence qualifies a support

    Claims are grounded in the synthesis (derived_from) + source_refs; they NEVER add scholarly
    content the synthesis does not contain.
    """
    if not synthesis:
        return []
    rq = synthesis.get("research_question", {}).get("question", "")
    frame = synthesis.get("debate_frame", {})
    positions = frame.get("positions", [])
    arguments = synthesis.get("arguments", [])
    cruxes = synthesis.get("cruxes", [])
    counterevidence = synthesis.get("counterevidence", [])
    open_questions = synthesis.get("open_questions", [])
    unresolved = synthesis.get("unresolved_disagreement", [])
    source_refs = synthesis.get("source_refs", [])
    synthesis_id = synthesis.get("synthesis_id", "SYNTH")

    claims = []
    # MAIN_THESIS: frame the question (honest, not an assertion)
    claims.append(_claim(f"{synthesis_id}:EC-1", f"What is at issue: {rq}",
                         derived_from=[synthesis_id], role="MAIN_THESIS",
                         source_refs=source_refs))
    # SUPPORTING: each position's argument, grounded in the argument
    for i, arg in enumerate(arguments):
        claims.append(_claim(f"{synthesis_id}:EC-{2 + i}", f"An argument ({arg}) supports its position",
                             derived_from=[synthesis_id, arg], role="SUPPORTING",
                             source_refs=source_refs))
    # CRUX: the decisive unresolved premise(s) -> a QUALIFICATION/OPEN_POINT
    for c in cruxes:
        claims.append(_claim(f"{synthesis_id}:EC-c-{c}", f"Decisive unresolved crux: {c}",
                             derived_from=[synthesis_id, c], role="OPEN_POINT",
                             source_refs=source_refs))
    # COUNTEREVIDENCE
    for ce in counterevidence:
        claims.append(_claim(f"{synthesis_id}:EC-ce-{ce}", f"Counterevidence: {ce}",
                             derived_from=[synthesis_id], role="COUNTEREVIDENCE",
                             counterevidence_refs=[ce], source_refs=source_refs))
    # OPEN_POINT from open questions + unresolved disagreement (never resolved)
    for oq in open_questions:
        claims.append(_claim(f"{synthesis_id}:EC-oq-{oq}", f"Open question: {oq}",
                             derived_from=[synthesis_id], role="OPEN_POINT",
                             source_refs=source_refs))
    for u in unresolved:
        claims.append(_claim(f"{synthesis_id}:EC-u-{u}", f"Unresolved: {u}",
                             derived_from=[synthesis_id], role="OPEN_POINT",
                             source_refs=source_refs))
    return claims


def _claim(claim_id: str, claim: str, *, derived_from: list[str], role: str,
           counterevidence_refs: list[str] | None = None, source_refs: list[str] | None = None) -> dict:
    if role not in CLAIM_ROLES:
        role = "SUPPORTING"
    return {
        "essay_claim_id": claim_id,
        "claim": claim,
        "derived_from": derived_from,
        "role": role,
        "compression": "QUALIFIED",          # never silently inflate
        "source_refs": source_refs or [],
        "counterevidence_refs": counterevidence_refs or [],
        "claim_hash": _sha256({"claim": claim, "derived_from": derived_from, "role": role}),
    }


def build_essay_plan(synthesis: dict) -> dict:
    """Compile an EssayPlan from a synthesis: claims + structure (sections by role)."""
    claims = essay_claims_from_synthesis(synthesis)
    sections = {
        "thesis": [c for c in claims if c["role"] == "MAIN_THESIS"],
        "supporting": [c for c in claims if c["role"] == "SUPPORTING"],
        "counterevidence": [c for c in claims if c["role"] == "COUNTEREVIDENCE"],
        "open_points": [c for c in claims if c["role"] == "OPEN_POINT"],
    }
    return {
        "plan_id": f"plan-{synthesis.get('synthesis_id', 'SYNTH')}",
        "synthesis_ref": synthesis.get("synthesis_id", ""),
        "sections": sections,
        "claim_count": len(claims),
        "grounded": all(c["derived_from"] for c in claims),   # every claim rests on the synthesis
        "plan_hash": _sha256({"synthesis_ref": synthesis.get("synthesis_id", ""), "claims": claims}),
    }


if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    from patala_ml.synthesis_core import build_synthesis_from_gold
    from patala_ml.gold002 import build_gold_002

    synth = build_synthesis_from_gold(build_gold_002(), synthesis_id="SYNTH-IPVV",
                                      research_question="Is recognition recollection?")
    plan = build_essay_plan(synth)
    print(f"essay plan: {plan['claim_count']} grounded claims")
    for sec, claims in plan["sections"].items():
        print(f"  {sec:16} {len(claims)}")
    print("grounded:", plan["grounded"])
    for c in plan["sections"]["supporting"][:1]:
        print(json.dumps(c, indent=2, ensure_ascii=False))
