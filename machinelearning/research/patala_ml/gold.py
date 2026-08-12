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
    # (ARG-001 v2 after REVIEW-2026-08-12-MODEL-1: the regress/transcendental layer is removed —
    #  it was not licensed by the source. The identification with the knower/Lord is grounding, not
    #  an inference. Conclusion narrowed.)
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
            id="G-BRIDGE",
            proposition="In this kārikā, pratibhā characterizes / is the form of the support (āśraya) under discussion.",
            kind="IMPLICIT_PREMISE", explicitness="RECONSTRUCTED"),
        GoldNode(
            id="G-DIST",
            proposition="Bearing / presenting an order is not the same as being constituted by that order.",
            kind="TEXTUAL_CLAIM", explicitness="RECONSTRUCTED"),
        GoldNode(
            id="G-CONC",
            proposition="The pratibhā that bears ordered presentation is itself characterized as akrama (order-less); the passage characterizes the relevant support/knower accordingly as order-less.",
            kind="CONCLUSION", explicitness="RECONSTRUCTED"),
        GoldNode(
            id="G-IC1",
            proposition="Abhinavagupta identifies this order-less support with the knower (pramātṛ), the great Lord.",
            kind="INTERPRETIVE_CLAIM", explicitness="RECONSTRUCTED"),
    ]

    # ── the inference nodes (the actual argumentative moves — no regress) ──────
    inferences = [
        GoldInference(
            id="G-INF1",
            premise_ids=["G-TC1", "G-TC2"],
            conclusion_id="G-DIST",
            scheme="CONCEPTUAL_DISTINCTION",
            rationale="If X bears an order but is itself not ordered (G-TC1 + G-TC2), then bearing/presenting an order is not the same as being constituted by that order (G-DIST)."),
        GoldInference(
            id="G-INF2",
            premise_ids=["G-DIST", "G-BRIDGE"],
            conclusion_id="G-CONC",
            scheme="CONCEPTUAL_DISTINCTION",
            rationale="Since pratibhā (which characterizes the support under discussion, G-BRIDGE) is not constituted by the order it bears (G-DIST), the support is characterized as order-less (G-CONC)."),
    ]

    # ── the honest boundary ───────────────────────────────────────────────────
    boundary = {
        "text": ("This passage establishes that the pratibhā which bears ordered presentation is itself "
                 "characterized as akrama (order-less), and that the relevant support/knower is accordingly "
                 "order-less. It does NOT establish an infinite-regress/transcendental necessity, nor the "
                 "stronger claim that all such order-less supports are numerically one universal Self "
                 "(argued later, V2-S)."),
        "not_claiming": ["an infinite-regress argument",
                         "that any ordered presentation necessarily requires an order-transcending foundation",
                         "numerical identity of all order-less supports",
                         "that the support is Śiva/the universal subject"],
        "philological": {"proof_id": V2O_PROOF_ID, "status": "P0"},
    }

    # ── IR enrichment (ARGUMENT-IR-VISION.md): derivational + commitment per node ──
    # Per-proposition commitment / derivation (Sanskrit span in V2-O): the derivational provenance
    # that makes the gold representable in the 14-object IR without loss.
    node_ir = {
        "G-TC1": {"commitment": "ASSERTS", "derived_from": "SANSKRIT_EXPLICIT",
                  "span_id": "chunkV2-O-saptamo-vimarsa:L32:T115"},
        "G-TC2": {"commitment": "ASSERTS", "derived_from": "SANSKRIT_SUPPORTED",
                  "span_id": "chunkV2-O-saptamo-vimarsa:L44:T168"},
        "G-BRIDGE": {"commitment": "RECONSTRUCTED", "derived_from": "INTERPRETIVE_RECONSTRUCTION",
                     "span_id": "chunkV2-O-saptamo-vimarsa:L26:T52"},
        "G-DIST": {"commitment": "ASSERTS", "derived_from": "SANSKRIT_SUPPORTED",
                   "span_id": "chunkV2-O-saptamo-vimarsa:L44:T168"},
        "G-CONC": {"commitment": "RECONSTRUCTED", "derived_from": "INTERPRETIVE_RECONSTRUCTION",
                   "span_id": "chunkV2-O-saptamo-vimarsa:L44:T168"},
        "G-IC1": {"commitment": "INTERPRETIVE_EXTENSION", "derived_from": "C1_INTERPRETIVE",
                  "span_id": "chunkV2-O-saptamo-vimarsa:L30:T108"},
    }
    node_dicts = []
    for n in nodes:
        d = n.to_dict()
        ir = node_ir.get(n.id, {})
        d["commitment"] = ir.get("commitment", "RECONSTRUCTED")
        d["derived_from"] = ir.get("derived_from", "RECONSTRUCTED")
        d["grounding"] = {"passage_id": V2O_PASSAGE_ID, "c1_id": V2O_C1_ID,
                          "l200_assertion_id": V2O_L200_ID,
                          "span_id": ir.get("span_id", "")}
        node_dicts.append(d)

    return {
        "gold_id": "ARG-GOLD-001",
        "work_id": "ipvv",
        "passage": V2O_PASSAGE_ID,
        "title": "The Order-less Support of the Powers (V2-O)",
        "research_question": "Is the support (āśraya) of ordered presentation itself ordered, or order-less (akrama)?",
        "debate_frame": {
            "question": "Is the support of ordered presentation itself ordered, or order-less (akrama)?",
            "object_of_dispute": "whether the support/background that bears ordered presentation is itself ordered",
            "concept_refs": ["pratibhā", "krama", "akrama", "āśraya"],
            "positions": [
                {"position_id": "P-ordered", "holder": "opponent",
                 "commitment_ids": ["G-BRIDGE-as-ordered"], "argument_ids": []},
                {"position_id": "P-akrama", "holder": "siddhānta",
                 "commitment_ids": ["G-TC2", "G-CONC"], "argument_ids": ["G-INF1", "G-INF2"]},
            ],
            "semantic_alignments": [
                {"left_term": "pratibhā", "right_term": "the support (āśraya) of the powers",
                 "relation": "SAME_SENSE", "level": "CONCEPTUAL",
                 "context": [V2O_C1_ID], "status": "MACHINE_PROPOSED"},
                {"left_term": "akrama", "right_term": "order-less / not constituted by order",
                 "relation": "SAME_SENSE", "level": "LEXICAL",
                 "context": [V2O_C1_ID], "status": "MACHINE_PROPOSED"},
            ],
        },
        "nodes": node_dicts,
        "inferences": [i.to_dict() for i in inferences],
        "boundary": boundary,
        "status": "MACHINE_PROPOSED",   # the hand-construction is a gold candidate, not yet editor-accepted
    }
