"""patala_ml/gold003.py — ARG-GOLD-003: the reductio (V2-O, ordered-support regress).

The third hand-constructed gold argument, deliberately a REDUCTIO: "if the support of the powers were
itself ordered (a member of the ordered sequence), it would in turn require a further support — an
infinite regress — which is absurd; therefore the support is not ordered." Drawn from the SAME passage
as ARG-001 (V2-O) but as a different argumentative MOVE.

Built WITH the philosophical-IR shape (per ARGUMENT-IR-VISION.md / Deep Research 10-11):
  - `commitment` (who asserts vs assumes-for-argument vs attributes) on every node
  - derivational `Proposition` (`derived_from` + `explicitness`)
  - a `research_question` at the top
  - `Attack`/`Defeat` split on defeaters

Source: c1_V2O-orderless-support.md + pilot_V2O_L2_read.md.
Real resolvable passage id: pt:passage:ipvv:chunkV2-O-saptamo-vimarsa.md
"""
from __future__ import annotations

V2O_PASSAGE_ID = "pt:passage:ipvv:chunkV2-O-saptamo-vimarsa.md"
V2O_C1_ID = "V2O-orderless-support"
V2O_L200_ID = "l200/V2O-saptamo-vimarsa.md"
V2O_PROOF_ID = "pp:ipvv:v2o:p0"


def _grounding():
    return {"passage_id": V2O_PASSAGE_ID, "c1_id": V2O_C1_ID, "l200_assertion_id": V2O_L200_ID}


def build_gold_003() -> dict:
    """ARG-GOLD-003 — the reductio (V2-O): if the support were ordered, infinite regress."""
    nodes = [
        # the reductio hypothesis (assumed for argument, NOT asserted as Abhinava's own view)
        {"proposition_id": "G3-ASSUM",
         "task_level": "B_ARGUMENT_RECONSTRUCTION", "candidate_reconstruction": True,
         "text": "The support (āśraya) of the powers is itself a member of the ordered sequence — it is ordered.",
         "kind": "IMPLICIT_PREMISE", "explicitness": "RECONSTRUCTED",
         "commitment": "ASSUMES_FOR_ARGUMENT", "derived_from": "implicit",
         "grounding": _grounding(),
         "boundary": "this is the assumption to be refuted, not Abhinavagupta's own assertion",
         "status": "MACHINE_PROPOSED"},
        # the textual basis: pratibhā bears the order
        {"proposition_id": "G3-TC1",
         "task_level": "A_PROPOSITION_EXTRACTION",
         "text": "pratibhā (the flashing) runs through / bears the order of the word-objects (tattatpadārthakramarūṣitā).",
         "kind": "TEXTUAL_CLAIM", "explicitness": "EXPLICIT",
         "commitment": "ASSERTS", "derived_from": "Sanskrit (kārikā 1)",
         "grounding": _grounding(), "boundary": "", "status": "MACHINE_PROPOSED"},
        # the textual basis: pratibhā is itself not ordered
        {"proposition_id": "G3-TC2",
         "task_level": "A_PROPOSITION_EXTRACTION",
         "text": "pratibhā is not itself constituted by that order (akrama — order-less).",
         "kind": "TEXTUAL_CLAIM", "explicitness": "EXPLICIT",
         "commitment": "ASSERTS", "derived_from": "Sanskrit (kārikā 1)",
         "grounding": _grounding(), "boundary": "", "status": "MACHINE_PROPOSED"},
        # the regress principle (the reductio's engine — suppressed)
        {"proposition_id": "G3-REG",
         "task_level": "B_ARGUMENT_RECONSTRUCTION", "candidate_reconstruction": True,
         "text": "If a support of order were itself ordered, it would require a further support of its own ordering — an infinite regress.",
         "kind": "IMPLICIT_PREMISE", "explicitness": "IMPLICIT",
         "commitment": "ASSERTS", "derived_from": "implicit (the regress argument)",
         "grounding": _grounding(), "boundary": "", "status": "MACHINE_PROPOSED"},
        # the absurd consequence drawn from the hypothesis
        {"proposition_id": "G3-ABS",
         "task_level": "B_ARGUMENT_RECONSTRUCTION", "candidate_reconstruction": True,
         "text": "If the support were ordered, an infinite regress of ordered supports would follow — which is absurd.",
         "kind": "CONCLUSION", "explicitness": "RECONSTRUCTED",
         "commitment": "ASSERTS", "derived_from": "REDUCTIO over G3-ASSUM + G3-REG",
         "grounding": _grounding(), "boundary": "", "status": "MACHINE_PROPOSED"},
        # the textual conclusion the C1 states (support is not a member of the order)
        {"proposition_id": "G3-TC3",
         "task_level": "A_PROPOSITION_EXTRACTION",
         "text": "The support (āśraya) of the powers is not itself a member of the ordered sequence.",
         "kind": "TEXTUAL_CLAIM", "explicitness": "RECONSTRUCTED",
         "commitment": "ASSERTS", "derived_from": "C1 (the support is not ordered)",
         "grounding": _grounding(),
         "boundary": "the C1 says the support is not ordered; the unity of all such supports is argued later (V2-S)",
         "status": "MACHINE_PROPOSED"},
        # the final conclusion of the reductio
        {"proposition_id": "G3-CONC",
         "task_level": "A_PROPOSITION_EXTRACTION",
         "text": "The support of ordered presentation is itself order-less (akrama) — the order-less, infinite-consciousness-form knower.",
         "kind": "CONCLUSION", "explicitness": "RECONSTRUCTED",
         "commitment": "ASSERTS", "derived_from": "source + REDUCTIO",
         "grounding": _grounding(),
         "boundary": "establishes the order-less support structurally; does NOT by itself establish one universal Self (that is V2-S)",
         "status": "MACHINE_PROPOSED"},
        # the interpretive identification
        {"proposition_id": "G3-IC1",
         "task_level": "C_SYSTEMATIC_INTERPRETATION",
         "text": "Abhinavagupta identifies this order-less support with the knower (pramātṛ), the great Lord.",
         "kind": "INTERPRETIVE_CLAIM", "explicitness": "RECONSTRUCTED",
         "commitment": "ASSERTS", "derived_from": "C1 (interpretive identification)",
         "grounding": _grounding(), "boundary": "", "status": "MACHINE_PROPOSED"},
    ]

    inferences = [
        # the reductio step: assume the support is ordered → regress
        {"inference_id": "G3-INF-RED",
         "task_level": "B_ARGUMENT_RECONSTRUCTION", "candidate_reconstruction": True,
         "premise_ids": ["G3-ASSUM", "G3-REG"],
         "conclusion_ids": ["G3-ABS"],
         "scheme": "REDUCTIO",
         "rationale": "Assume the support is itself ordered (G3-ASSUM); by the regress principle (G3-REG) it then requires a further ordered support, ad infinitum — the absurdity (G3-ABS).",
         "defeaters": [], "status": "MACHINE_PROPOSED"},
        # the textual basis + the reductio jointly establish that the support is not ordered
        {"inference_id": "G3-INF-RES",
         "task_level": "A_PROPOSITION_EXTRACTION",
         "premise_ids": ["G3-TC1", "G3-TC2", "G3-ABS"],
         "conclusion_ids": ["G3-TC3"],
         "scheme": "REDUCTIO",
         "rationale": "pratibhā bears the order (G3-TC1) but is not itself ordered (G3-TC2); if its support were a member of the order, regress would follow (G3-ABS) — therefore the support is not a member of the sequence (G3-TC3).",
         "defeaters": [], "status": "MACHINE_PROPOSED"},
        # the general conclusion
        {"inference_id": "G3-INF-CONC",
         "task_level": "A_PROPOSITION_EXTRACTION",
         "premise_ids": ["G3-TC3", "G3-ABS"],
         "conclusion_ids": ["G3-CONC"],
         "scheme": "REDUCTIO",
         "rationale": "The support is not a member of the ordered sequence (G3-TC3); hence ordered presentation requires an order-less support (G3-CONC).",
         "defeaters": [], "status": "MACHINE_PROPOSED"},
        # the interpretive step
        {"inference_id": "G3-INF-IC",
         "task_level": "C_SYSTEMATIC_INTERPRETATION",
         "premise_ids": ["G3-TC3"],
         "conclusion_ids": ["G3-IC1"],
         "scheme": "INTERPRETIVE_CLAIM",
         "rationale": "The C1 identifies the order-less support with the knower / great Lord — an interpretive identification, not a bare textual assertion.",
         "defeaters": [], "status": "MACHINE_PROPOSED"},
    ]

    boundary = {
        "text": ("The passage establishes, by reductio, that the support of ordered presentation cannot itself be "
                 "a member of the ordered sequence — it is order-less. It does NOT by itself establish the stronger "
                 "claim that all such order-less supports are numerically one universal Self (argued later, V2-S)."),
        "not_claiming": ["numerical identity of all order-less supports",
                         "that the support is Śiva / the universal subject"],
        "philological": {"proof_id": V2O_PROOF_ID, "status": "P0"},
    }

    research_question = "Can the support of the ordered powers itself be ordered?"

    review_note = {
        "SAFE_GOLD": "pratibhā bears order + pratibhā is akrama -> the support is not exhausted by the order it supports. This is the extraction target (task_level A).",
        "STRONG_RECONSTRUCTION": "if the support itself belonged to the order -> a further support would be required -> regress -> therefore the support is akrama. The regress warrant (G3-REG, G3-ABS, G3-INF-RED) is marked candidate_reconstruction and is NOT a required extraction target until a specialist confirms the regress is the intended warrant.",
        "status": "MACHINE_PROPOSED",
    }

    review_note = {
        "SAFE_GOLD": "pratibhā bears order + pratibhā is akrama -> the support is not exhausted by the order it supports. This is the extraction target (task_level A).",
        "STRONG_RECONSTRUCTION": "if the support itself belonged to the order -> a further support would be required -> regress -> therefore the support is akrama. The regress warrant (G3-REG, G3-ABS, G3-INF-RED) is marked candidate_reconstruction and is NOT a required extraction target until a specialist confirms the regress is the intended warrant.",
        "status": "MACHINE_PROPOSED",
    }

    debate_frame = {
        "question": research_question,
        "object_of_dispute": "whether the support (āśraya) of the powers is itself a member of the ordered sequence",
        "concept_refs": ["āśraya", "akrama", "pratibhā", "krama", "maheśvara"],
        "shared_ground": ["the powers require a support", "pratibhā bears the order of the word-objects"],
        "disputed_ground": ["whether the support is itself ordered / a member of the sequence"],
        "semantic_alignments": [
            {"left_term": "krama", "right_term": "ordered member of the sequence",
             "relation": "SAME_SENSE", "context": [V2O_C1_ID],
             "rationale": "the reductio's 'ordered' = 'a member of the ordered sequence'",
             "status": "MACHINE_PROPOSED"},
            {"left_term": "akrama", "right_term": "order-less support",
             "relation": "SAME_SENSE", "context": [V2O_C1_ID],
             "rationale": "the conclusion's 'order-less' = the support not exhausted by the order it grounds",
             "status": "MACHINE_PROPOSED"},
        ],
    }

    return {
        "gold_id": "ARG-GOLD-003",
        "work_id": "ipvv",
        "passage": V2O_PASSAGE_ID,
        "title": "The Order-less Support by Reductio (V2-O)",
        "structure": "REDUCTIO",
        "review_note": review_note,
        "research_question": research_question,
        "nodes": nodes,
        "inferences": inferences,
        "boundary": boundary,
        "debate_frame": debate_frame,
        "status": "MACHINE_PROPOSED",
    }
