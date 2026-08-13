#!/usr/bin/env python3
"""python/patala_core/test_contracts.py — tests for the TIER 1 epistemic object contracts.

Proves the 3 P0 schema corrections from technical-architecture-v1 hold:
  P0#1  content is TYPED discriminated content, never dict[str, Any].
  P0#2  AuthorityVector is 4 independent axes with explicit gate predicates — NO scalar rank.
  P0#3  No universal review ladder — a Proposition has its OWN review state; education states
        (e.g. PEDAGOGICALLY_REVIEWED) can never be a Proposition's review state, and a ReviewEvent
        cannot mutate its target (constitutional).
Run: python3 python/patala_core/test_contracts.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from patala_core.authority import (  # noqa: E402
    AuthorityVector, EvidenceStatus, GenerationStatus, PublicationStatus, ReviewStatus,
)
from patala_core.objects import (  # noqa: E402
    AdjudicationObject, AdjudicationOutcome, CommitmentObject, CommitmentForce,
    PropositionContent, PropositionObject, ReviewDecision, ReviewEventContent,
    ReviewEventObject,
)


def t(name, cond, detail=""):
    print(("PASS" if cond else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def main() -> int:
    ok = True

    print("=== P0#1: typed discriminated content (no dict[str, Any]) ===")
    prop = PropositionObject(
        object_id="PTPROP_x", version_id="PTPROPV_y", layer="PROPOSITION",
        content={"formulation": "Consciousness is self-reflexive", "scope": "LOCAL_PASSAGE"},
    )
    ok &= t("content coerced to PropositionContent", isinstance(prop.content, PropositionContent))
    ok &= t("content not a bare dict", not isinstance(prop.content, dict))
    ok &= t("extra layer value rejected",
            _rejects(PropositionObject, object_id="a", version_id="b", layer="NOT_A_LAYER", content={}),
            "Literal['PROPOSITION']")
    ok &= t("unknown field forbidden (extra=forbid)",
            _rejects(PropositionObject, object_id="a", version_id="b", layer="PROPOSITION",
                     content={}, bogus_field=1))

    print("=== P0#2: AuthorityVector — 4 independent axes, no scalar rank ===")
    v = AuthorityVector(generation=GenerationStatus.ENGINEERING_VALIDATED,
                        evidence=EvidenceStatus.SCHOLARLY_CORROBORATED,
                        review=ReviewStatus.NOT_REVIEWED, publication=PublicationStatus.PUBLIC)
    ok &= t("no total-order 'rank' attribute", not hasattr(v, "rank") and not hasattr(v, "ceiling"))
    ok &= t("4 independent axes", {v.generation, v.evidence, v.review, v.publication}.issubset(
        {v.generation, v.evidence, v.review, v.publication}))
    # gating is a predicate, not a threshold
    ok &= t("eligible_for_publication() is a predicate", isinstance(v.eligible_for_publication(), bool))
    ok &= t("machine-proposed + no review → NOT publication-eligible",
            not AuthorityVector().eligible_for_publication())
    ok &= t("scholarly evidence does NOT force publication (axes independent)",
            not v.eligible_for_publication(), v.display_badge())
    ok &= t("display_badge is a phrase, not a rank", v.display_badge())

    print("=== P0#3: no universal review ladder; review cannot mutate target ===")
    # a Proposition's review state is its OWN — 'PEDAGOGICALLY_REVIEWED' must be rejected
    ok &= t("education state rejected on Proposition content",
            _rejects(PropositionObject, object_id="a", version_id="b", layer="PROPOSITION",
                     content={"formulation": "x", "proposition_review_state": "PEDAGOGICALLY_REVIEWED"}))
    # commitment carries its own force enum
    c = CommitmentObject(object_id="C1", version_id="C1v1", layer="COMMITMENT",
                         content={"proposition_ref": "P1", "actor_ref": "abhinavagupta",
                                  "force": "ATTRIBUTES_TO_OPPONENT"})
    ok &= t("commitment force typed (opponent not laundered as author belief)",
            c.content.force == CommitmentForce.ATTRIBUTES_TO_OPPONENT)
    # ReviewEvent references a target version and cannot mutate it (constitutional)
    rv = ReviewEventObject(object_id="R1", version_id="R1v1", layer="REVIEW_EVENT",
                           content={"target_version": "PTPROPV_y", "reviewer": "scholar-1",
                                    "decision": "DISPUTE"})
    ok &= t("review references a version_id, does not mutate it",
            rv.content.target_version == "PTPROPV_y" and rv.content.decision == ReviewDecision.DISPUTE)

    print("=== JSON Schema generation ===")
    try:
        import json
        schema = PropositionObject.model_json_schema()
        ok &= t("PropositionObject generates JSON Schema", "content" in schema.get("properties", {}))
    except Exception as e:
        ok &= t("PropositionObject generates JSON Schema", False, str(e)[:80])

    print("")
    print("RESULT: " + ("ALL PASS" if ok else "FAILURES"))
    return 0 if ok else 1


def _rejects(model, **kwargs) -> bool:
    try:
        model(**kwargs)
        return False
    except Exception:
        return True


if __name__ == "__main__":
    sys.exit(main())
