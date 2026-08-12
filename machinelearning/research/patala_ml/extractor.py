"""patala_ml/extractor.py — a PRIMITIVE, GENERIC proposition extractor (the CP4 baseline).

This is the intentionally-WEAK baseline that extraction must beat (per DEVPLAN Phase C / NEXT-STEPS
Build 4). It is deliberately generic: sentence-split + surface-marker role heuristics. It does NOT
know the gold, does NOT read any fixture, and is NOT tuned to the 5 gold arguments. If it were tuned
to recover them, the evaluation would be circular — the exact failure the doctrine bans.

Input : a C1 body (the `> ` quote lines) + a resolvable passage_id.
Output: a list of `ExtractionProposal` (proposition text, role, explicitness, grounding) + an
        optional abstention signal (`NO_UNIQUE_ARGUMENT`).

Honest expectation: proposition recall will be modest, role/explicitness F1 low, inference recovery 0
(a sentence-level baseline produces no inference graph). Grounding is trivially to the input passage.
This is a BASELINE, not a capability. See CLAIMS P-003: auto-reconstruction is NOT_ESTABLISHED.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

ROLES = {"TEXTUAL_CLAIM", "INTERPRETIVE_CLAIM", "IMPLICIT_PREMISE",
         "CONCLUSION", "OBJECTION", "QUALIFICATION"}

# surface markers (generic, English — the C1/L2 are English readings)
_QUESTION = re.compile(r"\?")
_OBJECTION = re.compile(r"\b(if|but|how|why|what if|yet)\b", re.I)
_CONCLUSION = re.compile(r"\b(therefore|hence|thus|so|cannot be|must be|is not|is real|in fact)\b", re.I)
_REDUCTIO = re.compile(r"\b(if|were|would|regress|infinite|absurd|otherwise)\b", re.I)
_IMPLICIT = re.compile(r"\b(must|requires|presupposes|implies|would|if)\b", re.I)
_INTERPRETIVE = re.compile(r"\b(Abhinavagupta|Abhinava|identif|is the|means that|the Lord|the knower)\b", re.I)


@dataclass
class ExtractionProposal:
    proposition_id: str
    text: str
    kind: str = "TEXTUAL_CLAIM"       # a role from ROLES
    explicitness: str = "RECONSTRUCTED"
    grounding: dict = field(default_factory=dict)
    abstain: bool = False             # True => this unit was 'NO_UNIQUE_ARGUMENT'


def _split_sentences(text: str) -> list[str]:
    """Split a body into sentence-like units (generic; keeps the C1's prose clauses)."""
    text = re.sub(r"\s+", " ", text or "")
    units = [u.strip() for u in re.split(r"(?<=[.!?])\s+", text) if len(u.strip()) > 15]
    return units


def _classify(unit: str) -> tuple[str, str]:
    """Generic role + explicitness from surface markers. Weak on purpose."""
    if _QUESTION.search(unit):
        return "OBJECTION", "EXPLICIT"
    if _REDUCTIO.search(unit) and (_IMPLICIT.search(unit) or "would" in unit):
        return "IMPLICIT_PREMISE", "IMPLICIT"
    if _CONCLUSION.search(unit):
        return "CONCLUSION", "RECONSTRUCTED"
    if _INTERPRETIVE.search(unit):
        return "INTERPRETIVE_CLAIM", "RECONSTRUCTED"
    return "TEXTUAL_CLAIM", "EXPLICIT"


def extract_propositions(c1_body: str, passage_id: str, limit: int | None = None) -> list[ExtractionProposal]:
    """Run the primitive extractor on a C1 body.

    Returns proposals grounded to `passage_id`. If the body has no claim-like unit, the extractor
    ABSTAINS (emits a single `NO_UNIQUE_ARGUMENT` proposal) rather than inventing one.
    """
    units = _split_sentences(c1_body)
    # drop the markdown blockquote markers + headers
    units = [u.lstrip("> ").lstrip("# ") for u in units]
    proposals: list[ExtractionProposal] = []
    for i, u in enumerate(units[:limit] if limit else units):
        kind, exp = _classify(u)
        proposals.append(ExtractionProposal(
            proposition_id=f"X{i:03d}",
            text=u,
            kind=kind,
            explicitness=exp,
            grounding={"passage_id": passage_id},
        ))
    if not proposals:
        # abstention: no safe reconstruction
        proposals.append(ExtractionProposal(
            proposition_id="X-ABSTAIN",
            text="NO_UNIQUE_ARGUMENT RECOVERABLE",
            kind="TEXTUAL_CLAIM", explicitness="RECONSTRUCTED",
            grounding={"passage_id": passage_id}, abstain=True,
        ))
    return proposals
