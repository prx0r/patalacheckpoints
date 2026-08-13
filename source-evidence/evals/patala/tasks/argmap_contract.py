#!/usr/bin/env python3
"""evals/patala/tasks/argmap_contract.py — the ARGMAP NAT contract (devpath1 E2-01).

Defines (1) the canonical ARGMAP shape the worker must satisfy and (2) the contract dimensions the
ARGMAP NAT evaluator measures, plus (3) the natural-failure mutation families a verifier must catch.

Dimensions (the 8 the run-report / SPEC-EPISTEMIC-CORE name):
    NODE      - the reconstructed argument nodes/steps are recovered
    ROLE      - each step's role (enumeration/predication/move/fidelity...) is correct
    EDGE      - the step-to-step / premise-to-conclusion relations are correct
    SPEAKER   - attribution is correct (authorial vs opponent vs reconstructed)
    SCOPE     - the map does not overreach what the passage licenses
    OPEN      - genuine open_items are preserved as OPEN (not silently resolved)
    INFERENCE - no unsupported/groundless inference step
    SUPPORT   - each step is grounded in the passage (SOURCE/L0)

Mutation families a verifier must catch (6 core + SPEAKER_COLLAPSE + SCOPE_INFLATION):
    OBJECTION_AS_AUTHOR_VIEW   - an objection is rendered as the author's settled view
    GROUNDING_AS_INFERENCE     - mere grounding/support is stated as an inference
    PREMISE_CONCLUSION_SWAP    - premise and conclusion are swapped
    RESPONSE_DIRECTION_FLIP    - a reply's direction is reversed (refutes -> supports)
    FALSE_CONTRADICTION        - an invented contradiction between steps
    INVENTED_BRIDGE            - a fabricated step bridging two real ones
    OPEN_AS_RESOLVED           - an OPEN item is silently resolved (boundary erasure)
    SPEAKER_COLLAPSE           - two distinct speakers are merged into one
    SCOPE_INFLATION            - a passage-bounded claim is inflated to a universal one

Gold is derived from the mutation SEMANTICS (what a faithful map must NOT contain), never from the
verifier's own output — the anti-circularity rule (EVAL-CONTRACT item 4).
"""
from __future__ import annotations

CANONICAL_SECTIONS = ["what_is_at_issue", "argument_steps", "open_items", "decision_for_l2"]

# the 8 evaluation dimensions
DIMENSIONS = ("NODE", "ROLE", "EDGE", "SPEAKER", "SCOPE", "OPEN", "INFERENCE", "SUPPORT")

# the mutation families the verifier must catch (8 in the handover: 6 core + 2 added)
MUTATION_FAMILIES = (
    "OBJECTION_AS_AUTHOR_VIEW",
    "GROUNDING_AS_INFERENCE",
    "PREMISE_CONCLUSION_SWAP",
    "RESPONSE_DIRECTION_FLIP",
    "FALSE_CONTRADICTION",
    "INVENTED_BRIDGE",
    "OPEN_AS_RESOLVED",
    "SPEAKER_COLLAPSE",
    "SCOPE_INFLATION",
)

# a minimal set of "inference"/"grounding" cue words used by the shape-level verifier.
# NOTE: these are STRUCTURAL cues only — the verifier nominates, never settles truth.
_INFERENCE_CUES = ("therefore", "hence", "so", "thus", "it follows", "consequently", "implies")
_GROUNDING_CUES = ("the passage", "the verse", "the segment", "as given", "licensed", "the text",
                   "fidelity bound")
_OBJECTION_CUES = ("one might object", "someone could", "the opponent", "a rival", "however,",
                   "alternatively")
_UNIVERSAL_CUES = ("all", "every", "always", "invariably", "in all cases", "universal", "everywhere")


def check_shape(argmap: dict) -> list[str]:
    """Check the canonical 4-section shape. Returns a list of missing section names (empty = pass)."""
    if not isinstance(argmap, dict):
        return ["argument_map_object"]
    return [s for s in CANONICAL_SECTIONS if s not in argmap]


def infer_mutation_from_delta(pristine_map: dict, mutated_map: dict) -> list[str]:
    """Best-effort structural family nomination from a pristine/mutated map pair.

    Used by the SYN half (known mutation) to verify the detector assigns the RIGHT family.
    This is structural; the NAT half uses independently-adjudicated gold instead.
    """
    found = []
    p = _flatten(pristine_map)
    m = _flatten(mutated_map)
    # OPEN_AS_RESOLVED: a section that was OPEN became resolved/decision
    for key in ("open_items",):
        ptext = str(p.get(key, "")).lower()
        mtext = str(m.get(key, "")).lower()
        if ptext and not mtext:
            found.append("OPEN_AS_RESOLVED")
    # SCOPE_INFLATION: universal cues added to the decision
    if any(u in str(m.get("decision_for_l2", "")).lower() for u in _UNIVERSAL_CUES):
        if not any(u in str(p.get("decision_for_l2", "")).lower() for u in _UNIVERSAL_CUES):
            found.append("SCOPE_INFLATION")
    # SPEAKER_COLLAPSE / OBJECTION_AS_AUTHOR_VIEW: objection cues dropped into argument_steps
    if any(o in str(m.get("argument_steps", "")).lower() for o in _OBJECTION_CUES):
        found.append("OBJECTION_AS_AUTHOR_VIEW")
    return found


def _flatten(obj: dict, prefix: str = "") -> dict:
    out = {}
    for k, v in obj.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            out.update(_flatten(v, key))
        elif isinstance(v, list):
            out[key] = " ".join(str(i) for i in v)
        else:
            out[key] = str(v)
    return out
