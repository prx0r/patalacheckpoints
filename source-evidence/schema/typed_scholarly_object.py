"""schema/typed_scholarly_object.py — the canonical typed scholarly-object contract (devpath7).

Implements `docs/vision/atlas/technical-architecture-v1.md` §27–37: the Pydantic discriminated-union
DerivedScholarlyObject that fixes the two P0 schema issues the architecture flags:
  §27  `content: dict[str, Any]`  →  typed Pydantic discriminated union
  §28  scalar `epistemic_ceiling`  →  vector `authority` (derive only display/eligibility)

This is the canonical Agent-1 contract. The OLD `derived_scholarly_object.py` is kept for backward
compatibility; new objects (and the Atlas reconciliation) use THIS module.

Design (the six-object convergence contract + typed content):
  CanonicalObjectRef / CanonicalVersionRef / ScholarlyObjectEnvelope / AuthorityVector /
  ObjectDependency / ObjectEvent
  + typed content bodies: PropositionContent, CommitmentContent, GroundingLinkContent,
    InferenceApplicationContent, CruxContent, ReviewEventContent, ReviewProposalContent,
    AdjudicationContent.

Boundary: this module defines the EPISTEMIC contracts (what a Proposition is, what a Crux is). It does
NOT define persistence — the Atlas owns identity/provenance/storage. `content` is validated here, stored
as `schema_name`/`schema_version`/validated payload in the Atlas registry.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field


# ── identity (the six-object contract) ───────────────────────────────────────
class CanonicalObjectRef(BaseModel):
    """Atlas identity for a scholarly object (not its version)."""
    object_id: str
    object_type: str


class CanonicalVersionRef(BaseModel):
    """Exact version of a scholarly object (the thing reviews/derivations bind to)."""
    object_id: str
    version_id: str
    schema_name: str
    schema_version: str
    payload_hash: str


ObjectVersionId = str  # "pt:<layer>:<work>:<slug>:<version>"


# ── authority (vector, never one scalar) ─────────────────────────────────────
# §28: do not derive one misleading scalar authority. Keep the 4-axis vector.
class AuthorityVector(BaseModel):
    generation: Literal["MACHINE_PROPOSED", "ENGINEERING_VALIDATED", "AUTONOMOUSLY_PROVEN"] = "MACHINE_PROPOSED"
    evidence: Literal["MACHINE_PROPOSED", "MACHINE_CORROBORATED", "SCHOLARLY_CORROBORATED_PRELIMINARY",
                      "SCHOLARLY_CORROBORATED", "SCHOLARLY_CORROBORATED_MULTI_SOURCE"] = "MACHINE_PROPOSED"
    review: Literal["NOT_REVIEWED", "INDEPENDENT_REVIEWED", "ADJUDICATED"] = "NOT_REVIEWED"
    publication: Literal["PRIVATE", "PUBLIC"] = "PRIVATE"

    def display_badge(self) -> str:
        """§28: derive a display string, never an ontological rank."""
        parts = []
        parts.append("Machine-generated" if self.generation != "AUTONOMOUSLY_PROVEN" else "Autonomously proven")
        if self.evidence != "MACHINE_PROPOSED":
            parts.append("scholarly evidence available")
        if self.review == "NOT_REVIEWED":
            parts.append("not human reviewed")
        return " · ".join(parts)

    def eligible_for_publication(self) -> bool:
        return self.review in ("INDEPENDENT_REVIEWED", "ADJUDICATED") and self.publication != "PRIVATE"

    def eligible_for_scholar_review(self) -> bool:
        return self.review == "NOT_REVIEWED"

    def eligible_for_education(self) -> bool:
        return self.generation in ("ENGINEERING_VALIDATED", "AUTONOMOUSLY_PROVEN") and self.review != "NOT_REVIEWED"


# ── typed content bodies (§29–36) ────────────────────────────────────────────
class PropositionContent(BaseModel):
    formulation: str
    subject: str | None = None
    scope: str | None = None
    modality: str | None = None
    temporal_scope: str | None = None
    explicitness: Literal["EXPLICIT", "IMPLIED", "RECONSTRUCTED"] = "EXPLICIT"
    speaker_ref: str | None = None
    assumptions: list[str] = Field(default_factory=list)
    support_scope: Literal["LOCAL_PASSAGE", "LOCAL_SECTION", "SAME_WORK", "CROSS_WORK",
                           "SYSTEMATIC_RECONSTRUCTION"] = "LOCAL_PASSAGE"
    # devpath4 provenance (reconciled from proposition_layer.py)
    derived_from: str = "SANSKRIT_SUPPORTED"
    scholarly_corroboration: dict = Field(default_factory=dict)


class CommitmentContent(BaseModel):
    proposition_ref: ObjectVersionId
    actor_ref: str
    force: Literal["ASSERTS", "DENIES", "PRESUPPOSES", "ASSUMES_FOR_ARGUMENT",
                   "ATTRIBUTES_TO_OPPONENT", "QUOTES", "RECONSTRUCTED",
                   "EDITORIAL_RATIONAL_RECONSTRUCTION"] = "ASSERTS"


class GroundingLinkContent(BaseModel):
    from_ref: ObjectVersionId
    to_ref: ObjectVersionId
    relation: Literal["TEXTUAL_GROUNDING", "LEXICAL_GROUNDING", "TRANSLATION_DEPENDENCY",
                      "SCHOLARLY_SUPPORT"] = "TEXTUAL_GROUNDING"


class InferenceApplicationContent(BaseModel):
    premises: list[ObjectVersionId] = Field(default_factory=list)
    conclusion: ObjectVersionId
    rule_ref: str | None = None
    reconstruction_status: Literal["EXPLICIT", "IMPLICIT", "EDITORIAL_RECONSTRUCTION"] = "EXPLICIT"
    evaluator_results: list[str] = Field(default_factory=list)


class CruxContent(BaseModel):
    argument_ref: ObjectVersionId
    proposition_refs: list[ObjectVersionId] = Field(default_factory=list)
    # perturbation (devpath5): what changed -> which conclusion changed. NOT "LLM says important".
    perturbation: dict = Field(default_factory=dict)   # {removed_premises, outcome_before, outcome_after}
    outcome_before: str = ""
    outcome_after: str = ""


class ReviewEventContent(BaseModel):
    target_version: ObjectVersionId
    reviewer: str = ""
    decision: Literal["ACCEPT", "ACCEPT_WITH_QUALIFICATION", "DISPUTE", "PROPOSE_ALTERNATIVE",
                      "ABSTAIN", "OUT_OF_SCOPE"] = "ACCEPT"
    scope: str = "LOCAL_PASSAGE"
    reasoning: str = ""
    evidence_refs: list[ObjectVersionId] = Field(default_factory=list)
    alternative_ref: ObjectVersionId | None = None
    conflict_of_interest: str | None = None


class ReviewProposalContent(BaseModel):
    review_event_ref: ObjectVersionId
    target_version: ObjectVersionId
    proposed_successor: ObjectVersionId
    change_summary: str = ""
    evidence_refs: list[ObjectVersionId] = Field(default_factory=list)


class AdjudicationContent(BaseModel):
    target_version: ObjectVersionId
    considered_reviews: list[ObjectVersionId] = Field(default_factory=list)
    adjudicator_refs: list[str] = Field(default_factory=list)
    outcome: Literal["ACCEPT_CURRENT", "ACCEPT_PROPOSED_SUCCESSOR", "REVISE", "REMAIN_DISPUTED"] = "ACCEPT_CURRENT"
    reasoning: str = ""
    dissent_refs: list[ObjectVersionId] = Field(default_factory=list)


# ── the discriminated union: every layer's content is a tagged variant (§27) ─
Content = Annotated[
    Union[
        PropositionContent,
        CommitmentContent,
        GroundingLinkContent,
        InferenceApplicationContent,
        CruxContent,
        ReviewEventContent,
        ReviewProposalContent,
        AdjudicationContent,
    ],
    Field(discriminator="__layer__"),
]


# ── the typed envelope (§27) ─────────────────────────────────────────────────
class BaseScholarlyObject(BaseModel):
    id: ObjectVersionId
    object_id: str
    layer: str
    derived_from: list[ObjectVersionId] = Field(default_factory=list)
    source_refs: list[ObjectVersionId] = Field(default_factory=list)
    authority: AuthorityVector = Field(default_factory=AuthorityVector)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    schema_version: str = "v1"


class PropositionObject(BaseScholarlyObject):
    layer: Literal["PROPOSITION"] = "PROPOSITION"
    content: PropositionContent


class CommitmentObject(BaseScholarlyObject):
    layer: Literal["COMMITMENT"] = "COMMITMENT"
    content: CommitmentContent


class CruxObject(BaseScholarlyObject):
    layer: Literal["CRUX"] = "CRUX"
    content: CruxContent


class ReviewEventObject(BaseScholarlyObject):
    layer: Literal["REVIEW_EVENT"] = "REVIEW_EVENT"
    content: ReviewEventContent


ScholarlyObject = Annotated[
    Union[PropositionObject, CommitmentObject, CruxObject, ReviewEventObject],
    Field(discriminator="layer"),
]


# ── the event log (§37) ───────────────────────────────────────────────────────
EVENT_TYPES = ("OBJECT_CREATED", "OBJECT_SUPERSEDED", "REVIEW_CREATED", "PROPOSAL_CREATED",
               "ADJUDICATION_CREATED", "AUTHORITY_CHANGED", "DEPENDENCY_INVALIDATED",
               "PROJECTION_REBUILT")


class ObjectEvent(BaseModel):
    event_type: Literal[
        "OBJECT_CREATED", "OBJECT_SUPERSEDED", "REVIEW_CREATED", "PROPOSAL_CREATED",
        "ADJUDICATION_CREATED", "AUTHORITY_CHANGED", "DEPENDENCY_INVALIDATED", "PROJECTION_REBUILT"
    ]
    object_version: ObjectVersionId
    actor_ref: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    event_hash: str = ""

    def canonical(self) -> dict:
        return self.model_dump(exclude={"event_hash"})

    def sign(self) -> str:
        body = self.canonical()
        body["created_at"] = body["created_at"].isoformat() if hasattr(body["created_at"], "isoformat") else body["created_at"]
        self.event_hash = hashlib.sha256(
            json.dumps(body, sort_keys=True, default=str).encode("utf-8")
        ).hexdigest()
        return self.event_hash


class ObjectDependency(BaseModel):
    consumer_version_id: ObjectVersionId
    dependency_version_id: ObjectVersionId
    relation: Literal["GROUNDS", "USES_AS_PREMISE", "USES_AS_WARRANT", "ORGANIZES"] = "USES_AS_PREMISE"
    load_bearing: bool = True
    epistemic_role: str = ""
