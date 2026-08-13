"""contracts/human_authority.py — ReviewEvent / ReviewProposal / Adjudication / PromotionEvent (G3).

The four human objects — SEPARATE semantics (G3 R2). The central rule:

    ReviewEvent ≠ status mutation.

A ReviewEvent is EVIDENCE ABOUT the target; it never changes the target. Only the chain
ReviewProposal → Adjudication → (new version, supersession) → PromotionEvent changes `review_status`.

Constitutional rules (G3):
- R1: machine may set generation/evidence authority; only an H witness may raise the review axis.
- R2: a review never mutates its target; disagreement is preserved.
- R3: authority is a vector; epistemic_ceiling is DERIVED (see derived_scholarly_object.py).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any


def sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()


# decision vocabulary (G3)
REVIEW_DECISIONS = (
    "ACCEPT",
    "ACCEPT_WITH_QUALIFICATION",
    "DISPUTE",
    "PROPOSE_ALTERNATIVE",
    "ABSTAIN",
    "OUT_OF_SCOPE",
)


@dataclass
class ReviewerIdentity:
    person_ref: str = ""
    orcid: str = ""
    identity_state: str = "UNVERIFIED"      # VERIFIED by admin, not self-attested
    display_name: str = ""
    # domain scoping (never a global "scholar score"): authority attaches to the review relationship
    domains: list[str] = field(default_factory=list)   # e.g. ["Śaiva textual history", "Sanskrit philology"]
    target_domain_match: str = "UNKNOWN"    # HIGH / MEDIUM / LOW / UNKNOWN


@dataclass
class ReviewTarget:
    object_ref: str = ""      # e.g. pt:translation-decision:TD-81
    version: str = ""         # EXACT version
    hash: str = ""            # payload hash (review is invalid if detached from the exact artifact)
    layer: str = ""           # TRANSLATION_DECISION | PROPOSITION | ARGUMENT | SOURCE_ASSERTION | ...


@dataclass
class ReviewEvent:
    """One scholar's scoped judgment on an EXACT version. EVIDENCE, never a mutation (G3 R2)."""
    review_id: str            # pt:review:REV-XXXX
    schema_version: str = "ReviewEvent-v1"
    review_target: ReviewTarget = field(default_factory=ReviewTarget)
    reviewer: ReviewerIdentity = field(default_factory=ReviewerIdentity)
    decision: str = "ACCEPT"
    review_scope: str = "LOCAL_PASSAGE"    # LOCAL_PASSAGE | LOCAL_SECTION | SAME_WORK | SYSTEMATIC
    evidence_refs: list[str] = field(default_factory=list)   # pt:span / pt:sourceassertion
    reasoning: str = ""
    conflict_of_interest: str = "NONE"
    alternative_object_ref: str = ""       # for PROPOSE_ALTERNATIVE
    defeaters: list[str] = field(default_factory=list)
    created_at: str = ""

    def emit(self) -> dict[str, Any]:
        body = asdict(self)
        body["event_hash"] = sha256({k: v for k, v in body.items() if k != "event_hash"})
        return body

    @classmethod
    def verify(cls, cert: dict[str, Any]) -> bool:
        expected = sha256({k: v for k, v in cert.items() if k != "event_hash"})
        return expected == cert.get("event_hash")


@dataclass
class ReviewProposal:
    """A proposed SUCCESSOR to the reviewed target (a correction). Separate from the ReviewEvent."""
    proposal_id: str
    schema_version: str = "ReviewProposal-v1"
    review_ref: str = ""                # the ReviewEvent that motivated this
    target_ref: str = ""                # the object it proposes to replace
    target_version: str = ""
    proposed_successor_ref: str = ""    # the new object version (not yet committed)
    proposed_content: dict[str, Any] = field(default_factory=dict)
    status: str = "PENDING"             # PENDING | ACCEPTED | REJECTED | SUPERSEDED

    def emit(self) -> dict[str, Any]:
        body = asdict(self)
        body["proposal_hash"] = sha256({k: v for k, v in body.items() if k != "proposal_hash"})
        return body


@dataclass
class Adjudication:
    """A formal resolution over one+ reviews. Records unresolved dissent (G3 R2)."""
    adjudication_id: str
    schema_version: str = "Adjudication-v1"
    reviews_considered: list[str] = field(default_factory=list)
    evidence_considered: list[str] = field(default_factory=list)
    decision: str = "ACCEPT_PROPOSAL"   # ACCEPT_PROPOSAL | REJECT_PROPOSAL | SEND_BACK
    unresolved_dissent: list[str] = field(default_factory=list)  # reviews that remain in disagreement
    adjudicator: ReviewerIdentity = field(default_factory=ReviewerIdentity)
    reasoning: str = ""

    def emit(self) -> dict[str, Any]:
        body = asdict(self)
        body["adjudication_hash"] = sha256({k: v for k, v in body.items() if k != "adjudication_hash"})
        return body


@dataclass
class PromotionEvent:
    """The MECHANICAL authority transition (review_status change), explicitly justified."""
    promotion_id: str
    schema_version: str = "PromotionEvent-v1"
    object_ref: str = ""
    object_version: str = ""
    from_status: str = "NOT_REVIEWED"
    to_status: str = "INDEPENDENT_REVIEWED"    # NOT_REVIEWED -> INDEPENDENT_REVIEWED -> ADJUDICATED
    basis: list[str] = field(default_factory=list)   # review_refs / adjudication_refs that justify it
    reason: str = ""

    def emit(self) -> dict[str, Any]:
        body = asdict(self)
        body["promotion_hash"] = sha256({k: v for k, v in body.items() if k != "promotion_hash"})
        return body
