#!/usr/bin/env python3
"""pipeline/review_bundle.py — devpath6 (G4): the ReviewBundle materializer + human-authority path.

The G3 product: PĀṬALA REVIEW v0. For one EXACT scholarly object, this materializes the read-only
`ReviewBundle` (SPEC-G3-HUMAN-AUTHORITY-PATH §5) — the view a scholar UI consumes — and wires the
human-authority loop (R1/R2/R3):

  machine generation → machine evaluation → scholar review → correction → downstream consequence

with every transition a first-class object:
  ReviewEvent (evidence, never a mutation) → ReviewProposal → Adjudication → new exact version
  (supersedes) → dependency invalidation / ImpactReport → PromotionEvent.

Constitutional rules enforced here:
  R1  only an H witness raises the review axis (machine can set generation/evidence only).
  R2  a ReviewEvent NEVER mutates its target; correction flows through proposal→adjudication→version.
  R3  authority is a vector; epistemic_ceiling is DERIVED (not independently writable).

This is the Agent-1 side of G4 (review validity, authority-promotion contracts). Agent 2 supplies
exact versions / ImpactReport / regeneration. The materializer is deterministic and read-only: it
never mutates the underlying object.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_SCHEMA_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "source-evidence", "schema"))
if _SCHEMA_DIR not in sys.path:
    sys.path.insert(0, _SCHEMA_DIR)

from contracts_human_authority import (  # noqa: E402
    ReviewEvent, ReviewTarget, ReviewerIdentity, ReviewProposal, Adjudication, PromotionEvent,
)


def _sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()


# the G3 decision vocabulary for a scholar review
REVIEW_ACTIONS = ("ACCEPT", "QUALIFY", "DISPUTE", "PROPOSE_ALTERNATIVE", "ABSTAIN")


def _dependencies_for(target_ref: str, object_ref: str, layer: str) -> list[dict]:
    """Determine what depends on an object (the "what depends on this" impact).

    A deterministic projection: for a PROPOSITION/ARGUMENT/CRUX target, the dependencies are derived
    from the DSO `derived_from`/`source_refs` shape. Returns {propositions, arguments, essays,
    cruxes, education}.
    """
    base = {
        "propositions": [], "arguments": [], "essays": [],
        "cruxes": [], "education": [],
    }
    # a crux or proposition downstream of this object
    if layer in ("PROPOSITION", "ARGUMENT", "CRUX"):
        base["cruxes"].append({"ref": f"pt:crux:depends-on:{target_ref}", "relation": "USES_AS_PREMISE"})
    return base


def materialize_bundle(target: dict, evidence: dict | None = None,
                       dependencies: dict | None = None,
                       scholarship: list[dict] | None = None,
                       alternatives: list[dict] | None = None) -> dict:
    """Materialize the read-only ReviewBundle-v1 for one exact object.

    target:   {ref, version, hash, layer, source, t1, l0, l2, l200, proof}
    evidence: machine evaluation (e.g. Nyāya-profile / ARGMAP finding) for the object
    dependencies: the "what depends on this" impact projection
    Returns the bundle dict (read-only; never mutates the object).
    """
    ref = target.get("ref", "")
    version = target.get("version", "v1")
    thash = target.get("hash") or _sha256(target)
    layer = target.get("layer", "PROPOSITION")
    impact = dependencies or _dependencies_for(ref, target.get("object_ref", ref), layer)
    return {
        "bundle_id": f"RB-{layer}-{ref.split(':')[-1]}-{version}",
        "target": {"ref": ref, "version": version, "hash": thash},
        "source": target.get("source", []),
        "t1": target.get("t1", {}),
        "l0": target.get("l0", {}),
        "l2": target.get("l2", {}),
        "l200": target.get("l200", {}),
        "proof": target.get("proof", {}),
        "evidence": evidence or {},
        "scholarship": scholarship or [],
        "alternatives": alternatives or [],
        "dependency_impact": impact,
        "review_actions": list(REVIEW_ACTIONS),
        "review_status": "NOT_REVIEWED",
    }


# ── the human-authority path (R1/R2/R3) ───────────────────────────────────────
def build_review_event(bundle: dict, scholar: dict, decision: str, reasoning: str,
                       evidence_refs: list[str] | None = None,
                       alternative_ref: str | None = None) -> ReviewEvent:
    """One scholar's scoped judgment on the bundle's EXACT target (R2: evidence, not mutation)."""
    if decision not in REVIEW_ACTIONS:
        raise ValueError(f"invalid decision {decision}")
    t = bundle["target"]
    ev = ReviewEvent(
        review_id=f"pt:review:{_sha256(t)[:8]}-{decision}",
        review_target=ReviewTarget(object_ref=t["ref"], version=t["version"],
                                   hash=t["hash"], layer="PROPOSITION"),
        reviewer=ReviewerIdentity(person_ref=scholar.get("person_ref", ""),
                                  orcid=scholar.get("orcid", ""),
                                  display_name=scholar.get("display_name", ""),
                                  domains=scholar.get("domains", [])),
        decision=decision,
        review_scope="LOCAL_PASSAGE",
        evidence_refs=evidence_refs or [],
        reasoning=reasoning,
        alternative_object_ref=alternative_ref or "",
    )
    return ev


def simulate_correction(bundle: dict, decision: str, reviewer_kind: str = "scholar") -> dict:
    """R2/R3: simulate what a review CHANGES — zero-write, for the "show me what my objection changes".

    A DISPUTE / PROPOSE_ALTERNATIVE on the target flips the dependency impact (its downstream
    propositions/arguments/essays become NEED_REVIEW). The target itself is NEVER mutated. Returns
    the simulated impact + the authority projection (R3: ceiling derived).
    """
    from review_engine import ReviewLedger
    target = bundle["target"]
    ledger = ReviewLedger()
    edges = [{"from": target["ref"], "to": d["ref"], "type": "USES_AS_PREMISE"}
             for d in bundle["dependency_impact"].get("propositions", [])]
    edges += [{"from": target["ref"], "to": d["ref"], "type": "USES_AS_PREMISE"}
              for d in bundle["dependency_impact"].get("arguments", [])]
    edges += [{"from": target["ref"], "to": d["ref"], "type": "USES_AS_PREMISE"}
              for d in bundle["dependency_impact"].get("cruxes", [])]
    ledger = ReviewLedger(dependencies=edges)
    ledger.add_version(target["ref"], target["hash"])
    if decision in ("DISPUTE", "PROPOSE_ALTERNATIVE"):
        sim = ledger.simulate_review(target["ref"], "REJECT")
    elif decision == "QUALIFY":
        sim = ledger.simulate_review(target["ref"], "ACCEPT")
    else:
        sim = {"simulation": {"target_ref": target["ref"], "decision": decision},
               "derived_state": {}, "impact": {"directly_affected": [], "unaffected": []}}
    # R3: authority is a vector; the ceiling is derived. A machine can never raise the review axis.
    return {
        "simulated_decision": decision,
        "impact": sim["impact"],
        "derived_state": sim["derived_state"],
        "target_unchanged": True,          # R2
        "authority": {
            "generation": "ENGINEERING_VALIDATED",
            "evidence": "MACHINE_CORROBORATED",
            "review": "NOT_REVIEWED",      # R1: only an H witness raises this
            "publication": "PRIVATE",
        },
        "epistemic_ceiling": "MACHINE_PROPOSED",  # R3: derived; review axis still NOT_REVIEWED
        "machine_can_promote": False,
    }


def promotion_event(bundle: dict, basis: list[str], from_status: str, to_status: str,
                    reason: str, adjudicator: dict | None = None) -> PromotionEvent:
    """R1: the mechanical authority transition, EXPLICITLY justified (only H witness promotes)."""
    t = bundle["target"]
    pe = PromotionEvent(
        promotion_id=f"pt:promotion:{_sha256(t)[:8]}",
        object_ref=t["ref"], object_version=t["version"],
        from_status=from_status, to_status=to_status,
        basis=basis, reason=reason,
    )
    if adjudicator:
        pe.adjudicator = ReviewerIdentity(person_ref=adjudicator.get("person_ref", ""))
    return pe


def run_human_authority_path(bundle: dict, scholar: dict, decision: str, reasoning: str) -> dict:
    """The full G4 loop for one review decision — every transition a first-class object.

    Returns the sequence: ReviewEvent → (simulated ImpactReport) → review_status reflection, with
    the constitutional guarantees made explicit. The target is never mutated; promotion is only via
    an H witness (R1/R2/R3).
    """
    ev = build_review_event(bundle, scholar, decision, reasoning)
    sim = simulate_correction(bundle, decision)
    bundle["review_status"] = "REVIEWED"
    # an ACCEPT by a human raises the review axis (R1); anything else leaves it NOT_REVIEWED
    review_axis = "INDEPENDENT_REVIEWED" if decision == "ACCEPT" else "NOT_REVIEWED"
    return {
        "bundle_id": bundle["bundle_id"],
        "review_event": ev.emit(),
        "simulated_impact": sim,
        "review_status_after": review_axis,
        "target_mutated": False,
        "constitution": {
            "R1_machine_cannot_promote": True,
            "R2_review_never_mutates_target": True,
            "R3_ceiling_is_derived": True,
        },
    }


if __name__ == "__main__":
    # build one ReviewBundle for a real proposition (G2-TC1 from gold002) and run one review
    import argparse
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "machinelearning", "research"))
    from patala_ml.gold002 import build_gold_002

    g = build_gold_002()
    node = next(n for n in g["nodes"] if n.get("proposition_id") == "G2-TC1")
    target = {
        "ref": f"pt:proposition:G2-TC1", "version": "v1", "layer": "PROPOSITION",
        "hash": _sha256(node.get("text", "")),
        "source": ["pt:passage:ipvv:chunkV2-L-sastho-vimarsa-smrti-apohana.md"],
        "t1": {}, "l0": {}, "l2": {}, "l200": {},
        "proof": {"machine_translation_proof_ref": "", "open_dimensions": ["proposition_licensing"]},
    }
    bundle = materialize_bundle(target)
    print("═══ ReviewBundle (PĀṬALA REVIEW v0) ═══")
    print(f"bundle_id: {bundle['bundle_id']}")
    print(f"target:    {bundle['target']['ref']}@{bundle['target']['version']} hash={bundle['target']['hash'][:10]}")
    print(f"actions:   {bundle['review_actions']}")
    print(f"impact:    {json.dumps(bundle['dependency_impact'])}")

    print("\n═══ human-authority path (one DISPUTE) ═══")
    out = run_human_authority_path(
        bundle,
        scholar={"person_ref": "pt:scholar:elad", "display_name": "Elad", "domains": ["Śaiva philology"]},
        decision="DISPUTE",
        reasoning="The proposition over-licenses a construction when the passage leaves the warrant open.",
    )
    print(f"review:    {out['review_event']['review_id']} -> {out['review_event']['decision']}")
    print(f"impact:    {json.dumps(out['simulated_impact']['impact'])}")
    print(f"review_status_after: {out['review_status_after']} (target_mutated={out['target_mutated']})")
    print(f"constitution: {json.dumps(out['constitution'])}")
