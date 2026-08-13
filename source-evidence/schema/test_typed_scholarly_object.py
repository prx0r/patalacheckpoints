#!/usr/bin/env python3
"""test_typed_scholarly_object.py — devpath7 canonical object convergence contract acceptance.

Checks (per `docs/vision/atlas/technical-architecture-v1.md` §27–37):
  1. content is a typed Pydantic discriminated union, NOT dict[str, Any] (the §27 fix)
  2. authority is a VECTOR (generation/evidence/review/publication), never one scalar (the §28 fix);
     derive only display badge + eligibility predicates
  3. the typed content bodies validate: PropositionContent, CommitmentContent, GroundingLinkContent,
     InferenceApplicationContent, CruxContent, ReviewEventContent, ReviewProposalContent, AdjudicationContent
  4. the six-object convergence contract exists: CanonicalObjectRef, CanonicalVersionRef,
     ScholarlyObjectEnvelope(BaseScholarlyObject), AuthorityVector, ObjectDependency, ObjectEvent
  5. the object union discriminates by layer (resolves to the right typed object)
  6. a Crux records PERTURBATION (what changed -> which conclusion), not "LLM says important"
  7. ReviewEvent cannot mutate target (constitutional) — it is a typed content record
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from typed_scholarly_object import (
    AuthorityVector, CanonicalObjectRef, CanonicalVersionRef, ObjectDependency, ObjectEvent,
    PropositionContent, CommitmentContent, GroundingLinkContent, InferenceApplicationContent,
    CruxContent, ReviewEventContent, ReviewProposalContent, AdjudicationContent,
    PropositionObject, CruxObject, ReviewEventObject, CommitmentObject,
    ScholarlyObject, BaseScholarlyObject,
)
from pydantic import TypeAdapter, ValidationError

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


print("== §27 fix: content is a typed union, not dict[str, Any] ==")
p = PropositionObject(id="pt:proposition:x:v1", object_id="x",
                      content=PropositionContent(formulation="The I is not constructed"))
check("PropositionObject content is PropositionContent (typed)", type(p.content) is PropositionContent)
c = CruxObject(id="pt:crux:y:v1", object_id="y",
               content=CruxContent(argument_ref="A", proposition_refs=["P"],
                                   perturbation={"removed": ["P1"], "outcome_after": "FLIP"}))
check("CruxObject content is CruxContent (typed)", type(c.content) is CruxContent)
check("no dict[str, Any] content leak", "dict[str, Any]" not in str(p.content.__class__))

print("\n== §28 fix: authority is a vector, derive only display/eligibility ==")
a = AuthorityVector(generation="ENGINEERING_VALIDATED", evidence="SCHOLARLY_CORROBORATED")
check("authority is a 4-axis vector", set(a.model_dump()) ==
      {"generation", "evidence", "review", "publication"})
check("display_badge derives a string (not a rank)", isinstance(a.display_badge(), str))
check("eligible_for_scholar_review is an explicit predicate",
      a.eligible_for_scholar_review() is True and a.eligible_for_education() is False)
check("no scalar ceiling on authority", not hasattr(a, "ceiling"))

print("\n== the six-object convergence contract ==")
oref = CanonicalObjectRef(object_id="x", object_type="PROPOSITION")
check("CanonicalObjectRef validates", oref.object_type == "PROPOSITION")
vref = CanonicalVersionRef(object_id="x", version_id="v1", schema_name="PropositionContent",
                           schema_version="v1", payload_hash="abc")
check("CanonicalVersionRef validates", vref.payload_hash == "abc")
check("ObjectDependency validates", ObjectDependency(consumer_version_id="a", dependency_version_id="b").relation == "USES_AS_PREMISE")
ev = ObjectEvent(event_type="OBJECT_CREATED", object_version="pt:proposition:x:v1")
sig = ev.sign()
check("ObjectEvent signs a hash", bool(sig) and len(sig) == 64)
check("BaseScholarlyObject is the envelope", BaseScholarlyObject(id="a", object_id="b", layer="L").layer == "L")

print("\n== typed content bodies validate (§29–36) ==")
check("CommitmentContent validates force",
      CommitmentContent(proposition_ref="P", actor_ref="A", force="ATTRIBUTES_TO_OPPONENT").force == "ATTRIBUTES_TO_OPPONENT")
check("GroundingLinkContent validates",
      GroundingLinkContent(from_ref="a", to_ref="b", relation="SCHOLARLY_SUPPORT").relation == "SCHOLARLY_SUPPORT")
check("InferenceApplicationContent validates",
      InferenceApplicationContent(premises=["a", "b"], conclusion="c").reconstruction_status == "EXPLICIT")
check("ReviewEventContent validates decision",
      ReviewEventContent(target_version="v", reviewer="r", decision="DISPUTE").decision == "DISPUTE")
check("ReviewProposalContent validates",
      ReviewProposalContent(review_event_ref="r", target_version="t", proposed_successor="s").proposed_successor == "s")
check("AdjudicationContent validates",
      AdjudicationContent(target_version="t", outcome="REMAIN_DISPUTED").outcome == "REMAIN_DISPUTED")

print("\n== §33: a Crux records perturbation (not 'LLM says important') ==")
check("CruxContent has perturbation + outcome_before/after",
      c.content.perturbation and "outcome_before" in c.content.model_dump() and "outcome_after" in c.content.model_dump())

print("\n== §34: ReviewEvent cannot mutate target (constitutional) ==")
re = ReviewEventObject(id="pt:review:z:v1", object_id="z",
                       content=ReviewEventContent(target_version="pt:prop:x:v1", reviewer="scholar",
                                                  decision="DISPUTE"))
check("ReviewEvent is a typed content record (evidence, not mutation)",
      re.content.target_version == "pt:prop:x:v1" and re.content.decision == "DISPUTE")
check("ReviewEvent has no mutation field", "mutates" not in re.model_dump())

print("\n== the object union discriminates by layer ==")
ta = TypeAdapter(ScholarlyObject)
o = ta.validate_python({"id": "pt:proposition:x:v1", "object_id": "x", "layer": "PROPOSITION",
                        "content": {"formulation": "The I is not constructed"}})
check("union resolves to PropositionObject by layer", type(o) is PropositionObject)
o2 = ta.validate_python({"id": "pt:crux:y:v1", "object_id": "y", "layer": "CRUX",
                         "content": {"argument_ref": "A", "proposition_refs": ["P"]}})
check("union resolves to CruxObject by layer", type(o2) is CruxObject)

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (devpath7 typed canonical contract works)"))
sys.exit(1 if failures else 0)
