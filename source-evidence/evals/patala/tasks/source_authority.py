#!/usr/bin/env python3
"""evals/patala/tasks/source_authority.py — multidimensional source authority (Atlas NAT §4).

The directive's correction: do NOT expose a single scalar `authority_state: EDITION_VERIFIED` as the
whole truth. Source authority is MULTIDIMENSIONAL. Each axis is an independent evidentiary claim:

    work_identity       is the Work identity matched across catalogues?
    authorship          is the author attribution supported?
    edition_identity    is the printed edition correctly identified?
    etext_derivation    is the e-text's derivation from the edition established?
    witness_basis       is a manuscript witness basis established?
    rights              what is actually allowed (not just discoverable)?

Convenience gates derive from the vector (never a scalar rank):
    factory_eligible        can the factory use this as a translation source?
    publication_eligible    can it be published?
    scholar_review_eligible can a scholar review this exact object?

The multidimensional vector prevents a huge class of provenance theatre (a discoverable-but-not-
redistributable source being treated as fully "verified"; an e-text "probably based on X" being
treated as "verified transcription of X").
"""
from __future__ import annotations

from pydantic import BaseModel, Field

# each axis is an evidentiary claim, with an honest OPEN (never silently resolved)
_AXES = ("work_identity", "authorship", "edition_identity", "etext_derivation",
         "witness_basis", "rights")

# valid ladder per axis (best -> weakest); UNKNOWN is always a valid, honest state
# The literal producer vocabulary (peer-review authority-inflation fix): an internal crosswalk is
# INTERNAL_IDENTITY_BOUND, a single external search hit is EXTERNAL_CANDIDATE_FOUND, and
# MULTI_SOURCE_MATCHED requires >=2 epistemically independent sources + field agreement.
WORK_IDENTITY_LADDER = ("UNKNOWN", "DISCOVERED", "INTERNAL_IDENTITY_BOUND", "EXTERNAL_CANDIDATE_FOUND",
                        "CATALOG_MATCHED", "MULTI_SOURCE_MATCHED")
AUTHORSHIP_LADDER = ("UNKNOWN", "SELF_ATTRIBUTED", "CATALOG_SUPPORTED", "MULTI_SOURCE_CONFIRMED")
EDITION_IDENTITY_LADDER = ("UNKNOWN", "DISCOVERED", "INTERNAL_IDENTITY_BOUND", "EXTERNAL_CANDIDATE_FOUND",
                           "CATALOG_MATCHED", "COPY_INSPECTED", "EDITION_VERIFIED")
ETEXT_DERIVATION_LADDER = ("UNKNOWN", "OPEN", "PROBABLE_BASIS", "TRANSCRIPTION_VERIFIED")
WITNESS_BASIS_LADDER = ("UNKNOWN", "UNRESOLVED", "SINGLE_WITNESS", "MULTI_WITNESS")
RIGHTS_LADDER = ("UNKNOWN", "DISCOVERABLE", "PROCESSING_ALLOWED", "REDISTRIBUTABLE", "OPEN_LICENSE")


def _rank(ladder: tuple[str, ...], value: str) -> int:
    return ladder.index(value) if value in ladder else 0


class SourceAuthority(BaseModel):
    """The multidimensional source-authority vector (NEVER one scalar rank)."""
    work_identity: str = "UNKNOWN"
    authorship: str = "UNKNOWN"
    edition_identity: str = "UNKNOWN"
    etext_derivation: str = "UNKNOWN"
    witness_basis: str = "UNKNOWN"
    rights: str = "UNKNOWN"

    def display(self) -> str:
        """A human/UI badge — derived, never an ontological rank."""
        parts = []
        if _rank(WORK_IDENTITY_LADDER, self.work_identity) >= 2:
            parts.append("work identity multi-matched")
        if _rank(EDITION_IDENTITY_LADDER, self.edition_identity) >= 3:
            parts.append("edition copy-inspected")
        if self.etext_derivation == "TRANSCRIPTION_VERIFIED":
            parts.append("etext transcription verified")
        elif self.etext_derivation == "OPEN":
            parts.append("etext derivation OPEN")
        if _rank(RIGHTS_LADDER, self.rights) >= 2:
            parts.append(f"rights={self.rights.lower()}")
        if not parts:
            parts.append("source authority UNKNOWN")
        return " · ".join(parts)

    # convenience gates — explicit predicates, never a scalar `authority >= 3`
    def factory_eligible(self) -> bool:
        return (_rank(EDITION_IDENTITY_LADDER, self.edition_identity) >= 2
                and _rank(RIGHTS_LADDER, self.rights) >= 2)

    def publication_eligible(self) -> bool:
        return (_rank(RIGHTS_LADDER, self.rights) >= 3
                and _rank(EDITION_IDENTITY_LADDER, self.edition_identity) >= 3)

    def scholar_review_eligible(self) -> bool:
        return _rank(WORK_IDENTITY_LADDER, self.work_identity) >= 1


# ── the honest-ladder validator ───────────────────────────────────────────────
# OPEN / UNSUPPORTED are always valid honest states (per the peer review: UNKNOWN -> OPEN is cheap;
# UNKNOWN -> VERIFIED is dangerous). They must never be rejected as invalid.
_HONEST_OPEN = ("OPEN", "UNSUPPORTED")


def validate_authority(auth: dict) -> dict:
    """Validate a SourceAuthority dict against the ladders; returns {ok, problems}.

    OPEN / UNSUPPORTED are accepted on every axis (honest unresolved states, never inflated).
    A value is invalid only if it is NOT in the ladder AND NOT an honest-open state.
    """
    problems = []
    try:
        obj = SourceAuthority(**auth)
    except Exception as e:
        return {"ok": False, "problems": [f"invalid authority: {e}"]}
    for axis, ladder in (("work_identity", WORK_IDENTITY_LADDER),
                         ("authorship", AUTHORSHIP_LADDER),
                         ("edition_identity", EDITION_IDENTITY_LADDER),
                         ("etext_derivation", ETEXT_DERIVATION_LADDER),
                         ("witness_basis", WITNESS_BASIS_LADDER),
                         ("rights", RIGHTS_LADDER)):
        val = getattr(obj, axis)
        if val not in ladder and val not in _HONEST_OPEN:
            problems.append(f"{axis} value '{val}' not in ladder {ladder}")
    # provenance-aware corroboration: MULTI_SOURCE_MATCHED must not be claimed on echo
    return {"ok": not problems, "problems": problems, "authority": obj.model_dump()}
