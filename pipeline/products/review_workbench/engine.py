"""products/review_workbench/engine.py — the review workbench (the actual peer-review surface).

One object's FULL review context on one screen — what a scholar sees when they open something to review:
  - the object itself + its current state/authority
  - its context (evidence, argument, cruxes) — from context_bundle
  - its downstream impact ("what changes if I reject this?") — from scholar_review.impact
  - the decision surface (ACCEPT/REVISE/REJECT/ABSTAIN + rationale) — the scholar's action

This is the composition the vision calls "show me exactly what changes if I reject this" (globalplan
Phase 11). It composes my already-built engines; no new capability, one review surface.

CPU-only, deterministic, read-mostly. The DECISION is the only mutation, and it goes through the review
gate (authorized scholar only).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(_ROOT / "pipeline"))

from products.scholar_review.engine import ScholarProduct  # noqa: E402
from products.scholar_identity.engine import authorize  # noqa: E402


def open_workbench(target_ref: str, identity: dict, scope: str = "all") -> dict:
    """Open a review workbench for one object: state + context + impact + the decision surface."""
    sp = ScholarProduct()
    # 1. the object + its current state/authority
    obj = sp.object_state(target_ref)
    # 2. downstream impact ("what changes if I reject/revise this?")
    try:
        impact = sp.impact(target_ref)
    except Exception:
        impact = {"note": "no impact graph for this object"}
    # 3. the decision surface: what this scholar is allowed to do
    auth = authorize(identity, scope)
    decisions = ["ACCEPT", "REVISE", "REJECT", "ABSTAIN"] if auth["allowed"] else []
    return {
        "target_ref": target_ref,
        "object": obj,
        "downstream": impact,
        "scholar": {"id": identity.get("scholar_id"), "name": identity.get("name"),
                    "authorized": auth["allowed"], "scope": scope,
                    "scope_reason": auth.get("reason")},
        "decision_surface": {"decisions": decisions,
                             "note": "a machine actor may propose; only an authorized scholar submits"},
        "view": "review-workbench-v1",
    }


def decide(target_ref: str, identity: dict, decision: str, rationale: str,
           scope: str = "all", sign: bool = True) -> dict:
    """A scholar submits a decision from the workbench (goes through the review gate)."""
    sp = ScholarProduct()
    auth = authorize(identity, scope)
    if not auth["allowed"]:
        return {"submitted": False, "error": auth.get("reason")}
    if decision not in ("ACCEPT", "REVISE", "REJECT", "ABSTAIN"):
        return {"submitted": False, "error": f"invalid decision {decision}"}
    sub = sp.submit_review(identity["scholar_id"], "scholar", "*", target_ref, decision,
                           rationale, scope=scope)
    result = {"submitted": True, "review": sub["review"], "derived_state": sub["derived_state"]}
    if sign and identity.get("_private_key"):
        from products.scholar_review.signing import make_signed_attestation
        att = {"attestation_id": f"SA-{target_ref}", "target_ref": target_ref,
               "verdict": decision, "reviewer": identity["scholar_id"]}
        signed = make_signed_attestation(att, identity["_private_key"])
        result["attestation"] = signed
        # persist the attestation to the ledger so the scholar profile accumulates it
        try:
            p = Path(__file__).resolve().parents[3] / "data/scholar/attestations.jsonl"
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(signed, ensure_ascii=False) + "\n")
        except Exception:
            pass
    return result


def run_demo() -> dict:
    """A scholar opens a workbench on a real object, then decides (ACCEPT)."""
    from products.scholar_identity.engine import register, verify_orcid, _new_ed25519_keypair
    sp = ScholarProduct()
    ref = sp.list_objects(layer="C1")[0]["id"]
    priv, pub = _new_ed25519_keypair()
    ident = verify_orcid(register("0000-0000-0000-0000", "Scholar X", ["all"],
                                  public_key=pub.decode()))
    ident["_private_key"] = priv
    wb = open_workbench(ref, ident)
    dec = decide(ref, ident, "ACCEPT", "sound", sign=True)
    return {"workbench": wb, "decision": dec}


if __name__ == "__main__":
    import sys as _s
    verb = _s.argv[1] if len(_s.argv) > 1 else "demo"
    if verb == "demo":
        print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
    else:
        print(json.dumps({"error": f"unknown verb {verb}"}))
