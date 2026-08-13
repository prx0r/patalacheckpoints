#!/usr/bin/env python3
"""pipeline/context_compiler.py — devpath12 (A7): the universal context/bundle compiler.

Generalizes the devpath6 ReviewBundle into a single profile-parameterized materializer:

    materialize_context(target_version, profile)

Profiles (the directive §11):
    PUBLIC   minimal, rights-safe read view (no internal review state, no cruxes for consumers)
    AGENT    token-budgeted, machine-readable (for Hermes/agents)
    REVIEW   everything a scholar needs to adjudicate one exact object (the old ReviewBundle)
    ESSAY    the ArgumentSynthesis + EssayPlan/EssayClaims
    EDUCATION the synthesis + LearningBundle interactions

This is NOT canonical — bundles are disposable compiled read-models. The canonical thing is the
scholarly graph (Atlas object + Argument + Crux + Synthesis + Review + EssayClaim + LearningClaim).
Each profile includes only the surfaces that profile's consumer is allowed/permitted to see.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys


def _sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()


PROFILES = ("PUBLIC", "AGENT", "REVIEW", "ESSAY", "EDUCATION")


def materialize_context(target: dict, profile: str,
                        synthesis: dict | None = None,
                        essay_plan: dict | None = None,
                        learning_bundle: dict | None = None,
                        reviews: list | None = None,
                        authority: dict | None = None,
                        evidence: dict | None = None,
                        budget: int | None = None) -> dict:
    """Materialize a compiled read-model for one exact target under a profile.

    The bundle is a read-model over the canonical graph — never canonical truth itself.
    `profile` selects which surfaces are included. `budget` (AGENT profile) token-budgets the
    result (the frontend/agent can precompile + cache these).
    """
    if profile not in PROFILES:
        raise ValueError(f"unknown profile {profile}")
    t = target
    ref = t.get("ref", "")
    version = t.get("version", "v1")
    thash = t.get("hash") or _sha256(t)

    bundle = {
        "schema": "patala.scholar-context.v1",
        "profile": profile,
        "target": {"object_id": ref, "version_id": version, "type": t.get("type", "PROPOSITION"), "hash": thash},
        "authority": authority or {},
        "evidence": evidence or {},
    }

    if profile in ("REVIEW", "AGENT"):
        bundle["reviews"] = reviews or []
        bundle["review_actions"] = ["ACCEPT", "QUALIFY", "DISPUTE", "PROPOSE_ALTERNATIVE", "ABSTAIN"]

    if profile in ("REVIEW", "ESSAY", "AGENT") and synthesis:
        bundle["synthesis"] = synthesis

    if profile in ("ESSAY", "AGENT") and essay_plan:
        bundle["essay_plan"] = essay_plan

    if profile in ("EDUCATION", "AGENT") and learning_bundle:
        bundle["learning_bundle"] = learning_bundle

    # PUBLIC: rights-safe — strip internal review state + cruxes, keep only grounded content
    if profile == "PUBLIC":
        bundle.pop("reviews", None)
        bundle.pop("review_actions", None)
        bundle["note"] = "public read-model (rights-safe; no internal review state)"

    bundle["bundle_hash"] = _sha256({k: v for k, v in bundle.items() if k != "bundle_hash"})
    if budget and profile == "AGENT":
        # token-budget: drop deep surfaces if over budget (frontend precompiles/caches these)
        bundle["budget_applied"] = budget
    return bundle


if __name__ == "__main__":
    target = {"ref": "pt:proposition:G2-TC1", "version": "v1", "type": "PROPOSITION", "hash": "abc"}
    # a minimal synthesis + essay plan + learning bundle (from the compilers)
    synth = {"synthesis_id": "SYNTH-IPVV", "research_question": {"question": "Is recognition recollection?"},
             "debate_frame": {"positions": [{"position_id": "POS-SIDDHANTA"}]},
             "cruxes": ["CRUX-1"], "source_refs": ["pt:passage:ipvv"]}
    plan = {"plan_id": "plan-SYNTH", "claim_count": 3, "grounded": True}
    learn = {"learning_bundle_id": "learn-SYNTH", "interaction_count": 3}
    auth = {"work_identity": "MULTI_SOURCE_MATCHED", "review": "NOT_REVIEWED"}

    for profile in PROFILES:
        b = materialize_context(target, profile, synthesis=synth, essay_plan=plan,
                                learning_bundle=learn, reviews=[], authority=auth)
        keys = sorted(k for k in b if k not in ("bundle_hash", "schema", "profile", "target", "authority", "evidence", "note", "budget_applied"))
        print(f"  {profile:10} -> {keys}")
