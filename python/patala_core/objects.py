"""patala_core.objects — the typed epistemic scholarly objects (TIER 1).

Implements technical-architecture-v1 §27, §29–36: the P0 correction that
`DerivedScholarlyObject.content` must be TYPED discriminated content, never `dict[str, Any]`.

Every object is a `BaseScholarlyObject` carrying stable identity + provenance + an
`AuthorityVector`, with a layer-specific `content` selected by Pydantic discriminated union.

P0 correction #3 is enforced here: the review states available to a Proposition are its OWN
(review ladder), NOT the universal review_state ladder that included education states like
`PEDAGOGICALLY_REVIEWED`. Each object type has its own state machine; education states can never
apply to a Proposition.
"""
from __future__ import annotations

from enum import Enum
from typing import Literal, Union

from pydantic import BaseModel, Field
from pydantic import ConfigDict

from .authority import AuthorityVector
from .ids import ObjectId, ObjectVersionId


# ── shared enums ─────────────────────────────────────────────────────────────────
class Scope(str, Enum):
    LOCAL_PASSAGE = "LOCAL_PASSAGE"
    LOCAL_SECTION = "LOCAL_SECTION"
    SAME_WORK = "SAME_WORK"
    CROSS_WORK = "CROSS_WORK"
    SYSTEMATIC_RECONSTRUCTION = "SYSTEMATIC_RECONSTRUCTION"


class Modality(str, Enum):
    ASSERTED = "ASSERTED"
    POSSIBLE = "POSSIBLE"
    NECESSARY = "NECESSARY"
    PROBABLE = "PROBABLE"
    OBLIGATORY = "OBLIGATORY"


class Explicitness(str, Enum):
    EXPLICIT = "EXPLICIT"
    IMPLIED = "IMPLIED"
    RECONSTRUCTED = "RECONSTRUCTED"


class CommitmentForce(str, Enum):
    ASSERTS = "ASSERTS"
    DENIES = "DENIES"
    PRESUPPOSES = "PRESUPPOSES"
    ASSUMES_FOR_ARGUMENT = "ASSUMES_FOR_ARGUMENT"
    ATTRIBUTES_TO_OPPONENT = "ATTRIBUTES_TO_OPPONENT"
    QUOTES = "QUOTES"
    RECONSTRUCTED = "RECONSTRUCTED"


class GroundingRelation(str, Enum):
    TEXTUAL_GROUNDING = "TEXTUAL_GROUNDING"
    LEXICAL_GROUNDING = "LEXICAL_GROUNDING"
    TRANSLATION_DEPENDENCY = "TRANSLATION_DEPENDENCY"
    SCHOLARLY_SUPPORT = "SCHOLARLY_SUPPORT"


class ReconstructionStatus(str, Enum):
    EXPLICIT = "EXPLICIT"
    IMPLICIT = "IMPLICIT"
    EDITORIAL_RECONSTRUCTION = "EDITORIAL_RECONSTRUCTION"


class ReviewDecision(str, Enum):
    ACCEPT = "ACCEPT"
    ACCEPT_WITH_QUALIFICATION = "ACCEPT_WITH_QUALIFICATION"
    DISPUTE = "DISPUTE"
    PROPOSE_ALTERNATIVE = "PROPOSE_ALTERNATIVE"
    ABSTAIN = "ABSTAIN"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"


class AdjudicationOutcome(str, Enum):
    ACCEPT_CURRENT = "ACCEPT_CURRENT"
    ACCEPT_PROPOSED_SUCCESSOR = "ACCEPT_PROPOSED_SUCCESSOR"
    REVISE = "REVISE"
    REMAIN_DISPUTED = "REMAIN_DISPUTED"


# ── layer-specific content (typed — the P0 fix) ────────────────────────────────
class PropositionContent(BaseModel):
    formulation: str
    subject: str | None = None
    scope: Scope = Scope.LOCAL_PASSAGE
    modality: Modality = Modality.ASSERTED
    temporal_scope: str | None = None
    explicitness: Explicitness = Explicitness.EXPLICIT
    speaker_ref: str | None = None
    assumptions: list[str] = Field(default_factory=list)
    support_scope: Scope = Scope.LOCAL_PASSAGE
    # proposition has its OWN review state (P0 correction #3): a strict Literal means
    # education states (PEDAGOGICALLY_REVIEWED, etc.) can NEVER be a Proposition's review state.
    proposition_review_state: Literal["UNREVIEWED", "SINGLE_REVIEWED", "ADJUDICATED"] = "UNREVIEWED"


class CommitmentContent(BaseModel):
    proposition_ref: str
    actor_ref: str
    force: CommitmentForce = CommitmentForce.ASSERTS


class GroundingLinkContent(BaseModel):
    from_ref: str
    to_ref: str
    relation: GroundingRelation = GroundingRelation.TEXTUAL_GROUNDING
    scope: str = ""


class InferenceApplicationContent(BaseModel):
    premises: list[str] = Field(default_factory=list)
    conclusion: str
    rule_ref: str | None = None
    reconstruction_status: ReconstructionStatus = ReconstructionStatus.EXPLICIT
    evaluator_results: list[str] = Field(default_factory=list)


class CruxContent(BaseModel):
    argument_ref: str
    proposition_refs: list[str] = Field(default_factory=list)
    perturbation: str
    outcome_before: str
    outcome_after: str


class ReviewEventContent(BaseModel):
    target_version: str
    reviewer: str
    decision: ReviewDecision
    scope: str = ""
    reasoning: str = ""
    evidence_refs: list[str] = Field(default_factory=list)
    alternative_ref: str | None = None
    conflict_of_interest: str | None = None


class ReviewProposalContent(BaseModel):
    review_event_ref: str
    target_version: str
    proposed_successor: str
    change_summary: str = ""
    evidence_refs: list[str] = Field(default_factory=list)


class AdjudicationContent(BaseModel):
    target_version: str
    considered_reviews: list[str] = Field(default_factory=list)
    adjudicator_refs: list[str] = Field(default_factory=list)
    outcome: AdjudicationOutcome
    reasoning: str = ""
    dissent_refs: list[str] = Field(default_factory=list)


# ── the discriminated union (the P0 fix: typed content, not dict[str, Any]) ────
ContentUnion = Union[
    PropositionContent,
    CommitmentContent,
    GroundingLinkContent,
    InferenceApplicationContent,
    CruxContent,
    ReviewEventContent,
    ReviewProposalContent,
    AdjudicationContent,
]


class BaseScholarlyObject(BaseModel):
    """The universal envelope. content is a TYPED discriminated union."""
    model_config = ConfigDict(extra="forbid")

    object_id: str
    version_id: str
    layer: str
    derived_from: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    authority: AuthorityVector = Field(default_factory=AuthorityVector)
    schema_version: str = "1.0"


class PropositionObject(BaseScholarlyObject):
    layer: Literal["PROPOSITION"]
    content: PropositionContent


class CommitmentObject(BaseScholarlyObject):
    layer: Literal["COMMITMENT"]
    content: CommitmentContent


class GroundingLinkObject(BaseScholarlyObject):
    layer: Literal["GROUNDING_LINK"]
    content: GroundingLinkContent


class InferenceApplicationObject(BaseScholarlyObject):
    layer: Literal["INFERENCE_APPLICATION"]
    content: InferenceApplicationContent


class CruxObject(BaseScholarlyObject):
    layer: Literal["CRUX"]
    content: CruxContent


class ReviewEventObject(BaseScholarlyObject):
    layer: Literal["REVIEW_EVENT"]
    content: ReviewEventContent


class ReviewProposalObject(BaseScholarlyObject):
    layer: Literal["REVIEW_PROPOSAL"]
    content: ReviewProposalContent


class AdjudicationObject(BaseScholarlyObject):
    layer: Literal["ADJUDICATION"]
    content: AdjudicationContent
