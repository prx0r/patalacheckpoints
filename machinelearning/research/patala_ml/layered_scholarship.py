#!/usr/bin/env python3
"""patala_ml/layered_scholarship.py — the layered scholarship object (devpath13 / the user's framing).

The user's insight: "essays can be loose vs logical synthesis — we can have hard data and then
interpretations of that, so there are multiple layers at play."

Pāṭala must NEVER collapse these. An essay is not the same epistemic kind of object as the logical
synthesis it rests on. This module models the layering explicitly:

    LAYER 0  SOURCE        the Sanskrit / the primary text        (authoritative witness)
    LAYER 1  LOGICAL       the reconstructed argument: propositions, inferences, warrants, cruxes,
                           attacks/replies — the HARD data. Textually anchored, reviewable.
    LAYER 2  SYNTHESIS     the higher-order reading over L1 (ArgumentSynthesis): positions, crux,
                           counterevidence, scope. Still reasoned (derived from L1).
    LAYER 3  ESSAY         the loose, editorial interpretation: thesis, framing, comparison with
                           other scholars, rhetorical choices. MAY exceed L1/L2 (that is its job) —
                           but every such exceedance is LABELLED an interpretation, not a fact.
    LAYER 4  EDUCATION     the projection of L1-L3 into exercises (separate: teaches the structure).

KEY LAW (the anti-collapse): an object may borrow from a lower layer, but it can NEVER silently
convert a lower layer's openness into its own certainty. The essay can say "some read X as Y, but the
text only licenses Z" — it cannot say "the text establishes X" when L1 marked X UNRESOLVED.

    INTERPRETATION ≠ EVIDENCE
    A claim's truth lives at L1/L2; L3 adds perspective, not proof.
"""
from __future__ import annotations

import hashlib
import json

LAYERS = ("SOURCE", "LOGICAL", "SYNTHESIS", "ESSAY", "EDUCATION")

# how each layer may relate to the layer below
ALLOWED_RELATION = {
    "LOGICAL": ("CONSERVATIVE_PARAPHRASE", "GROUNDS", "ATTRIBUTES", "RECONSTRUCTS"),
    "SYNTHESIS": ("AGGREGATES", "BRIDGES", "QUALIFIES", "CONSERVATIVE_PARAPHRASE"),
    "ESSAY": ("INTERPRETS", "FRAMES", "COMPARES", "SPECULATES", "QUALIFIES"),
    "EDUCATION": ("PROJECTS", "EXERCISES", "DIAGNOSES"),
}


def _sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def make_layered_object(*, object_id, source, logical=None, synthesis=None, essay=None,
                        education=None) -> dict:
    """Assemble a LayeredScholarlyObject carrying the hard-data layers + the loose interpretation layers.

    `source` = {span_id, text, status}
    `logical` = {propositions, inferences, warrants, cruxes, attacks}  (HARD data)
    `synthesis` = {research_question, positions, crux, counterevidence, boundary}
    `essay` = {thesis, claims[], interpretation_claims[]}
    `education` = {skills, interactions}

    Returns the object with each layer + its relation to the layer below.
    """
    layers = {"SOURCE": source or {}}
    rels = {}
    if logical:
        layers["LOGICAL"] = logical
        rels["LOGICAL"] = "GROUNDS"          # logical grounds the source
    if synthesis:
        layers["SYNTHESIS"] = synthesis
        rels["SYNTHESIS"] = "BRIDGES"        # synthesis bridges the logical propositions
    if essay:
        layers["ESSAY"] = essay
        rels["ESSAY"] = "INTERPRETS"         # essay interprets the synthesis
    if education:
        layers["EDUCATION"] = education
        rels["EDUCATION"] = "PROJECTS"       # education projects the structure

    return {
        "object_id": object_id,
        "object_kind": "LayeredScholarlyObject",
        "layers": layers,
        "layer_relations": rels,
        "design_law": "INTERPRETATION != EVIDENCE; truth lives at LOGICAL/SYNTHESIS; ESSAY adds perspective not proof",
        "hash": _sha256({"id": object_id, "logical": logical, "essay": essay}),
    }


def audit_layer_honesty(obj: dict) -> dict:
    """Check no layer silently converts a lower layer's openness into its own certainty.

    Rules:
      - if a LOGICAL crux/attack is OPEN, the SYNTHESIS and ESSAY must not present it as settled.
      - the ESSAY layer must carry a separate `interpretation_claims` list (its speculations), distinct
        from any factual/derived claims — the essay cannot smuggle interpretation as evidence.
    """
    findings = []
    logical = obj.get("layers", {}).get("LOGICAL", {})
    essay = obj.get("layers", {}).get("ESSAY", {})
    synthesis = obj.get("layers", {}).get("SYNTHESIS", {})

    # 1. an OPEN logical crux must not be 'resolved' upward
    open_cruxes = [c for c in logical.get("cruxes", []) if str(c.get("status", "OPEN")).upper() == "OPEN"]
    if open_cruxes:
        # the synthesis must carry it as open, not resolved (accept both 'cruxes' list and 'crux' dict)
        syn_cruxes = synthesis.get("cruxes") or ([synthesis["crux"]] if synthesis.get("crux") else [])
        syn_open = any(str(c.get("status", "OPEN")).upper() in ("OPEN", "UNRESOLVED")
                       for c in syn_cruxes) if syn_cruxes else False
        if not syn_open:
            findings.append("LOGICAL_OPEN_COLLAPSED: an open logical crux was not preserved as open in SYNTHESIS")
        # the essay must not assert it as settled
        essay_low = json.dumps(essay, ensure_ascii=False).lower()
        if any(k in essay_low for k in ("definitively", "proves that", "establishes conclusively", "settles the debate")):
            findings.append("LOGICAL_OPEN_COLLAPSED_IN_ESSAY: the essay asserts an open crux as settled")

    # 2. the essay must separate interpretation from any derived claim
    interp = essay.get("interpretation_claims", [])
    derived = essay.get("derived_claims", [])
    if not interp and essay:
        # an essay with no labelled interpretation but with claims that are not grounded is dishonest
        findings.append("ESSAY_NO_INTERPRETATION_LAYER: the essay has no 'interpretation_claims' field — "
                        "its speculative moves are unlabelled (risk: speculation presented as evidence)")

    ok = len(findings) == 0
    return {"ok": ok, "findings": findings,
            "law": "INTERPRETATION != EVIDENCE; a lower layer's OPEN must stay OPEN upward"}


if __name__ == "__main__":
    # honest layered object: open crux preserved upward, essay labels its interpretations
    honest = make_layered_object(
        object_id="VERTICAL-1",
        source={"span_id": "chunkM", "text": "...", "status": "WITNESS"},
        logical={"propositions": [{"id": "P1", "text": "inert cannot establish", "status": "LICENSED"}],
                 "inferences": [], "warrants": [],
                 "cruxes": [{"id": "CRUX-1", "status": "OPEN",
                             "question": "does establishing require self-luminosity"}],
                 "attacks": [{"attacker": "O3", "target": "P2", "type": "UNDERMINE"}]},
        synthesis={"research_question": "Can the determination establish an external?",
                   "positions": [], "crux": {"id": "CRUX-1", "status": "OPEN"},
                   "counterevidence": [], "boundary": {"does_not_establish": ["a universal Self"]}},
        essay={"thesis": "reflexivity is intrinsic",
               "derived_claims": ["the inert part cannot establish (L1)"],
               "interpretation_claims": ["some read the crystal analogy as a full idealism, but the text "
                                          "only licenses per-act self-luminosity"]},
        education={"skills": ["IDENTIFY_CRUX"], "interactions": []})
    ah = audit_layer_honesty(honest)
    print("honest layered object:", ah)

    # dishonest: essay presents an open crux as settled, no interpretation layer
    bad = make_layered_object(
        object_id="BAD", source={"text": "..."},
        logical={"cruxes": [{"id": "C", "status": "OPEN"}]},
        essay={"thesis": "the text proves the universal Self",
               "derived_claims": ["the text proves the universal Self"]})
    ab = audit_layer_honesty(bad)
    print("dishonest layered object:", ab)
    assert ah["ok"] is True
    assert ab["ok"] is False
    print("SELF-TEST PASS (layered scholarship separates hard data from interpretation)")
