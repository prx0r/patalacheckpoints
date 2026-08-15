"""products/review_policy/engine.py — the review policy (what each review kind GRANTS).

The authority semantics behind peer review. When a scholar ACCEPTs/REJECTs/REVISEs an object, what does
that DO to its epistemic ceiling? The reviewer reducer (`_advance_ladder`) advances a ladder, but the
POLICY mapping — which decisions by which authority grant which ceiling — is declared here.

Policy = a declared mapping, never a hidden rule:
  - ACCEPT  by a scholar   -> SINGLE_REVIEWED (raises MACHINE_PROPOSED -> ENGINEERING_VALIDATED floor)
  - ACCEPT  by 2 scholars  -> DOUBLE_REVIEWED (-> SCHOLARLY_CORROBORATED for corroborated objects)
  - ACCEPT  by adjudicator -> ADJUDICATED (the human-authority top)
  - REJECT  by any         -> REJECTED (set back, never deleted)
  - REVISE  by a scholar   -> SUPERSEDED + a new CANDIDATE version
  - ABSTAIN by any         -> no change (honest abstention)

The invariant: authority(projection) <= authority(parent) is preserved — a review never raises an
object above what its parents' evidence supports. CPU-only, deterministic.

The policy is MACHINE_DECLARED; only a human/adjudicator can reach the top rungs. This is the explicit
"what does my review grant" a scholar needs to trust the system.
"""
from __future__ import annotations

import json
import sys

# the review ladder (from scholar_review.engine DERIVED, restated here as the policy target)
LADDER = ["CANDIDATE", "SINGLE_REVIEWED", "DOUBLE_REVIEWED", "ADJUDICATED", "SPECIALIST_REVIEWED"]

# the canonical G3 REVIEW_DECISIONS (source-evidence/schema/contracts_human_authority.py) + the
# core-reducer decisions — the scholar product speaks BOTH so it is one system with the canonical
# human-authority layer.
G3_DECISIONS = ["ACCEPT", "ACCEPT_WITH_QUALIFICATION", "DISPUTE", "PROPOSE_ALTERNATIVE",
                "ABSTAIN", "OUT_OF_SCOPE"]
CORE_DECISIONS = ["ACCEPT", "REVISE", "REJECT", "ABSTAIN"]

# map each G3 decision -> the core-reducer action it triggers + its grant semantics
G3_TO_CORE = {
    "ACCEPT": "ACCEPT",
    "ACCEPT_WITH_QUALIFICATION": "ACCEPT",     # a qualified accept still advances the review ladder
    "DISPUTE": "REVISE",                        # a dispute proposes the object be revised
    "PROPOSE_ALTERNATIVE": "REVISE",            # an alternative proposes a new version
    "ABSTAIN": "ABSTAIN",
    "OUT_OF_SCOPE": "ABSTAIN",                  # out-of-scope abstains (no promotion, honest)
}


def g3_decision(decision: str) -> dict:
    """Is this a canonical G3 decision, and what core action does it map to?"""
    if decision in G3_DECISIONS:
        return {"canonical": True, "decision": decision,
                "maps_to_core": G3_TO_CORE[decision]}
    if decision in CORE_DECISIONS:
        return {"canonical": False, "decision": decision, "maps_to_core": decision,
                "note": "core-reducer decision (backward-compatible)"}
    return {"canonical": False, "decision": decision, "maps_to_core": None,
            "error": f"unknown decision {decision}"}


# DECISION -> the ladder rung a single decision grants, given the actor kind
# (a scholar ACCEPT -> SINGLE_REVIEWED; DISPUTE/PROPOSE_ALTERNATIVE -> REVISE semantics; etc.)
DECISION_GRANT = {
    "ACCEPT": {
        "machine": 0,      # a machine never promotes (may propose only)
        "scholar": 1,      # SINGLE_REVIEWED
        "editor": 2,       # DOUBLE_REVIEWED
        "adjudicator": 3,  # ADJUDICATED
    },
    "REVISE": {"machine": None, "scholar": "SUPERSEDED", "editor": "SUPERSEDED",
               "adjudicator": "SUPERSEDED"},
    "REJECT": {"machine": None, "scholar": "REJECTED", "editor": "REJECTED",
               "adjudicator": "REJECTED"},
    "ABSTAIN": {"machine": "NO_CHANGE", "scholar": "NO_CHANGE", "editor": "NO_CHANGE",
                "adjudicator": "NO_CHANGE"},
}


def grants(decision: str, actor_kind: str, current_rung: int = 0) -> dict:
    """What does this decision by this actor grant? Returns the resulting effective state.

    Accepts BOTH the core decisions (ACCEPT/REVISE/REJECT/ABSTAIN) and the canonical G3 decisions
    (ACCEPT_WITH_QUALIFICATION/DISPUTE/PROPOSE_ALTERNATIVE/OUT_OF_SCOPE), mapping G3 onto the core
    action so the scholar product shares the canonical human-authority vocabulary.
    """
    g3 = g3_decision(decision)
    if g3.get("error"):
        return {"decision": decision, "error": g3["error"]}
    core_decision = g3["maps_to_core"]
    d = DECISION_GRANT.get(core_decision)
    if not d:
        return {"decision": decision, "error": f"unknown decision {decision}"}
    grant = d.get(actor_kind)
    if grant is None:
        return {"decision": decision, "actor_kind": actor_kind,
                "grant": "BLOCKED", "note": f"{actor_kind} may not {core_decision}"}
    if grant in ("REJECTED", "SUPERSEDED", "NO_CHANGE"):
        return {"decision": decision, "actor_kind": actor_kind, "grant": grant,
                "resulting_state": grant, "canonical": g3["canonical"],
                "maps_to_core": core_decision}
    # numeric grant -> the new ladder rung (never below the object's type floor)
    new_rung = max(grant, current_rung)
    return {"decision": decision, "actor_kind": actor_kind,
            "grant": LADDER[new_rung] if new_rung < len(LADDER) else "SPECIALIST_REVIEWED",
            "resulting_state": LADDER[new_rung] if new_rung < len(LADDER) else "SPECIALIST_REVIEWED",
            "from_rung": LADDER[current_rung] if current_rung < len(LADDER) else "SPECIALIST_REVIEWED",
            "canonical": g3["canonical"], "maps_to_core": core_decision}


def can_promote(actor_kind: str, target_ceiling: str) -> dict:
    """Can this actor kind promote an object to target_ceiling? (the eligibility predicate)"""
    # the authority ladder: machine < scholar < editor < adjudicator
    power = {"machine": 0, "scholar": 1, "editor": 2, "adjudicator": 3}
    required = {
        "MACHINE_PROPOSED": 0, "ENGINEERING_VALIDATED": 1, "SCHOLARLY_CORROBORATED": 2,
        "INDEPENDENT_REVIEWED": 3, "ADJUDICATED": 3,
    }
    need = required.get(target_ceiling, 0)
    return {"actor_kind": actor_kind, "target_ceiling": target_ceiling,
            "allowed": power.get(actor_kind, 0) >= need,
            "note": f"{actor_kind} {'CAN' if power.get(actor_kind,0) >= need else 'CANNOT'} promote to {target_ceiling}"}


def policy_summary() -> dict:
    """The declared policy, one table a scholar reads to know what a review grants."""
    rows = []
    for decision in ("ACCEPT", "REVISE", "REJECT", "ABSTAIN"):
        rows.append({decision: {
            k: ("BLOCKED" if DECISION_GRANT[decision].get(k) is None else DECISION_GRANT[decision][k])
            for k in ("machine", "scholar", "editor", "adjudicator")}})
    return {
        "policy": rows,
        "invariant": "authority(projection) <= authority(parent) — a review never raises an object "
                     "above what its parents' evidence supports",
        "top_rungs_require_human": True,
        "note": "MACHINE_DECLARED policy; only a human/adjudicator reaches ADJUDICATED",
    }


if __name__ == "__main__":
    import sys as _s
    verb = _s.argv[1] if len(_s.argv) > 1 else "summary"
    if verb == "summary":
        print(json.dumps(policy_summary(), indent=2, ensure_ascii=False))
    elif verb == "grants":
        print(json.dumps(grants(_s.argv[2], _s.argv[3]), indent=2, ensure_ascii=False))
    else:
        print(json.dumps(can_promote(_s.argv[2], _s.argv[3]), indent=2, ensure_ascii=False))
