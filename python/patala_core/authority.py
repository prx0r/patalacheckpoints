"""patala_core.authority — the AuthorityVector (the biggest P0 schema fix).

Implements technical-architecture-v1 §28: do NOT derive one misleading scalar authority.
The canonical form is a vector of FOUR independent axes:

    generation   — how the object was produced   (ENGINEERING_VALIDATED / MACHINE_PROPOSED / ...)
    evidence     — independent scholarly support (SCHOLARLY_CORROBORATED / NONE / ...)
    review       — human review state            (NOT_REVIEWED / SINGLE_REVIEWED / ADJUDICATED / ...)
    publication  — publication/rights posture    (PUBLIC / PRIVATE / ...)

These axes are NOT ordered onto one rank. Gates are explicit predicates, never `ceiling >= 3`.
"""
from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field


class GenerationStatus(str, Enum):
    MACHINE_PROPOSED = "MACHINE_PROPOSED"
    ENGINEERING_VALIDATED = "ENGINEERING_VALIDATED"
    EDITORIAL = "EDITORIAL"


class EvidenceStatus(str, Enum):
    NONE = "NONE"
    SCHOLARLY_CORROBORATED = "SCHOLARLY_CORROBORATED"
    DISPUTED = "DISPUTED"
    CORROBORATION_OPEN = "CORROBORATION_OPEN"


class ReviewStatus(str, Enum):
    NOT_REVIEWED = "NOT_REVIEWED"
    SINGLE_REVIEWED = "SINGLE_REVIEWED"
    ADJUDICATED = "ADJUDICATED"


class PublicationStatus(str, Enum):
    PRIVATE = "PRIVATE"
    INTERNAL = "INTERNAL"
    PUBLIC = "PUBLIC"


class AuthorityVector(BaseModel):
    """Four independent axes. There is deliberately NO total order across them."""
    generation: GenerationStatus = GenerationStatus.MACHINE_PROPOSED
    evidence: EvidenceStatus = EvidenceStatus.NONE
    review: ReviewStatus = ReviewStatus.NOT_REVIEWED
    publication: PublicationStatus = PublicationStatus.PRIVATE

    # ── explicit gate predicates (never a scalar rank) ────────────────────────
    def eligible_for_publication(self) -> bool:
        return (
            self.review in (ReviewStatus.ADJUDICATED, ReviewStatus.SINGLE_REVIEWED)
            and self.generation in (GenerationStatus.ENGINEERING_VALIDATED, GenerationStatus.EDITORIAL)
        )

    def eligible_for_scholar_review(self) -> bool:
        return self.generation in (GenerationStatus.MACHINE_PROPOSED, GenerationStatus.ENGINEERING_VALIDATED)

    def eligible_for_education(self) -> bool:
        return self.publication == PublicationStatus.PUBLIC and self.review != ReviewStatus.NOT_REVIEWED

    def display_badge(self) -> str:
        """A human display string derived from the vector — NOT a single rank."""
        parts = []
        if self.generation == GenerationStatus.ENGINEERING_VALIDATED:
            parts.append("machine-validated")
        elif self.generation == GenerationStatus.MACHINE_PROPOSED:
            parts.append("machine-generated")
        if self.evidence == EvidenceStatus.SCHOLARLY_CORROBORATED:
            parts.append("scholarly evidence available")
        if self.review == ReviewStatus.ADJUDICATED:
            parts.append("adjudicated")
        elif self.review == ReviewStatus.SINGLE_REVIEWED:
            parts.append("single-reviewed")
        else:
            parts.append("not human-reviewed")
        if self.publication == PublicationStatus.PUBLIC:
            parts.append("public")
        return " · ".join(parts) or "no authority recorded"
