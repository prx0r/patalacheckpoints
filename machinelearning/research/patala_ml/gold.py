"""patala_ml/gold.py — ARGUMENT GOLD v0: the hand-constructed, honest gold fixture.

The first substantive benchmark object. Built from the ACTUAL V2-O C1 + L2, with:
  - actual propositional nodes (TEXTUAL_CLAIM / INTERPRETIVE_CLAIM / IMPLICIT_PREMISE / CONCLUSION)
  - explicit/reconstructed/implicit status
  - real resolvable source support
  - inference nodes with real schemes
  - an honest BOUNDARY

This is ONE genuinely correct ArgumentPacket — deliberately more valuable than 1,000 shells.
Automatic extractors are evaluated against THIS object (not passage-title overlap).

The distinction (from the review):
  textual proposition ≠ interpretive proposition ≠ inference ≠ conclusion
"""
from __future__ import annotations

from dataclasses import dataclass, field


V2O_PASSAGE_ID = "pt:passage:ipvv:chunkV2-O-saptamo-vimarsa.md"
V2O_C1_ID = "V2O-orderless-support"
V2O_L200_ID = "l200/V2O-saptamo-vimarsa.md"
V2O_PROOF_ID = "pp:ipvv:v2o:p0"


@dataclass
class GoldNode:
    id: str
    proposition: str
    kind: str          # TEXTUAL_CLAIM | INTERPRETIVE_CLAIM | IMPLICIT_PREMISE | CONCLUSION
    explicitness: str  # EXPLICIT | RECONSTRUCTED | IMPLICIT
    source_support: dict = field(default_factory=lambda: {
        "passage_ids": [V2O_PASSAGE_ID], "c1_ids": [V2O_C1_ID],
        "l200_assertion_ids": [V2O_L200_ID],
    })
    status: str = "MACHINE_PROPOSED"

    def to_dict(self) -> dict:
        return {"id": self.id, "proposition": self.proposition, "kind": self.kind,
                "explicitness": self.explicitness, "source_support": self.source_support,
                "status": self.status}


@dataclass
class GoldInference:
    id: str
    premise_ids: list[str]
    conclusion_id: str
    scheme: str        # DEDUCTIVE | REDUCTIO | ABDUCTIVE | TRANSCENDENTAL | CONCEPTUAL_DISTINCTION | OBJECTION_REPLY | OTHER
    rationale: str
    status: str = "MACHINE_PROPOSED"

    def to_dict(self) -> dict:
        return {"id": self.id, "premise_ids": self.premise_ids,
                "conclusion_id": self.conclusion_id, "scheme": self.scheme,
                "rationale": self.rationale, "status": self.status}


def build_gold_v0() -> dict:
    """The hand-constructed Argument Gold v0 for V2-O (the order-less support)."""

    # ── the propositional nodes ────────────────────────────────────────────────
    nodes = [
        GoldNode(
            id="G-TC1",
            proposition="pratibhā (the flashing) runs through / bears the order of the word-objects (tattatpadārthakramarūṣitā).",
            kind="TEXTUAL_CLAIM", explicitness="EXPLICIT"),
        GoldNode(
            id="G-TC2",
            proposition="pratibhā is not itself constituted by that order (akrama — order-less).",
            kind="TEXTUAL_CLAIM", explicitness="EXPLICIT"),
        GoldNode(
            id="G-TC3",
            proposition="The support (āśraya) of the powers is not itself a member of the ordered sequence.",
            kind="TEXTUAL_CLAIM", explicitness="RECONSTRUCTED",
            # TC3 is a reconstruction: the C1 says the support is not ordered, licensing this
            source_support={"passage_ids": [V2O_PASSAGE_ID], "c1_ids": [V2O_C1_ID],
                            "l200_assertion_ids": [V2O_L200_ID]}),
        GoldNode(
            id="G-IC1",
            proposition="Abhinavagupta locates this order-less basis in the knower / support (pramātṛ), which is the great Lord.",
            kind="INTERPRETIVE_CLAIM", explicitness="RECONSTRUCTED"),
        GoldNode(
            id="G-CONC",
            proposition="Ordered presentation in awareness requires a support not exhausted by that presented order.",
            kind="CONCLUSION", explicitness="RECONSTRUCTED"),
        GoldNode(
            id="G-IMPLICIT",
            proposition="A genuine support of order must be such that its own nature does not presuppose the order it grounds (else regress).",
            kind="IMPLICIT_PREMISE", explicitness="IMPLICIT"),
    ]

    # ── the inference nodes (the actual argumentative moves) ──────────────────
    inferences = [
        GoldInference(
            id="G-INF1",
            premise_ids=["G-TC1", "G-TC2"],
            conclusion_id="G-TC3",
            scheme="CONCEPTUAL_DISTINCTION",
            rationale="If X bears order but is not itself ordered, then X is not a member of the ordered series (order-bearing ≠ ordered)."),
        GoldInference(
            id="G-INF2",
            premise_ids=["G-TC3", "G-IMPLICIT"],
            conclusion_id="G-CONC",
            scheme="TRANSCENDENTAL",
            rationale="Ordered presentation presupposes a support whose nature is not itself a further ordered member — otherwise an infinite regress of ordered supports."),
        GoldInference(
            id="G-INF3",
            premise_ids=["G-TC3"],
            conclusion_id="G-IC1",
            scheme="INTERPRETIVE_CLAIM",
            rationale="The C1 identifies this order-less support with the knower (pramātṛ) / great Lord — an interpretive identification, not a bare textual assertion."),
    ]

    # ── the honest boundary ───────────────────────────────────────────────────
    boundary = {
        "text": ("This passage establishes the structural requirement that the support of ordered "
                 "presentation is itself order-less. It does NOT by itself establish the stronger "
                 "claim that all such supports are numerically one universal Self — that unity is "
                 "argued later (V2-S) and is a further commitment."),
        "not_claiming": ["numerical identity of all order-less supports",
                         "that the support is Śiva/the universal subject"],
        "philological": {"proof_id": V2O_PROOF_ID, "status": "P0", "note": "verify_l0 proof for V2-O"},
    }

    return {
        "gold_id": "ARG-GOLD-001",
        "work_id": "ipvv",
        "passage": V2O_PASSAGE_ID,
        "title": "The Order-less Support of the Powers (V2-O)",
        "nodes": [n.to_dict() for n in nodes],
        "inferences": [i.to_dict() for i in inferences],
        "boundary": boundary,
        "status": "MACHINE_PROPOSED",   # the hand-construction is a gold candidate, not yet editor-accepted
    }
