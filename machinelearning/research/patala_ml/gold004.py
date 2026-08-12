"""patala_ml/gold004.py — ARG-GOLD-004: the conceptual distinction (V2-H, prakāśa vs vimarśa).

The fourth hand-constructed gold argument, a CONCEPTUAL_DISTINCTION: the essence of light (prakāśa) is
NOT the bare showing of objects but the reflexive-awareness (vimarśa) — a light that merely showed the
world without knowing it showed it would be no different from inert crystal. The distinguishing mark is
self-awareness in the very act of manifesting; this self-knowing is the parā-vāk (supreme speech) and
the Lord's freedom/lordship.

Built WITH the philosophical-IR shape (per ARGUMENT-IR-VISION.md / Deep Research 10-11):
  - `commitment` on every node · derivational `Proposition` (`derived_from` + `explicitness`)
  - `research_question` · `Attack`/`Defeat` split · three-level `SemanticAlignment` (LEXICAL/CONCEPTUAL)

Source: c1_V2H-vimarsa-paravak.md + pilot_V2H_L2_read.md.
Real resolvable passage id: pt:passage:ipvv:chunkV2-H-pancamo-vimarsa-k11-13.md
"""
from __future__ import annotations

V2H_PASSAGE_ID = "pt:passage:ipvv:chunkV2-H-pancamo-vimarsa-k11-13.md"
V2H_C1_ID = "V2H-vimarsa-paravak"
V2H_L200_ID = "l200/V2H-pancamo-vimarsa-k11-13.md"
V2H_PROOF_ID = "pp:ipvv:v2h:p0"


def _grounding():
    return {"passage_id": V2H_PASSAGE_ID, "c1_id": V2H_C1_ID, "l200_assertion_id": V2H_L200_ID}


def build_gold_004() -> dict:
    """ARG-GOLD-004 — the conceptual distinction (V2-H): prakāśa ≠ vimarśa."""
    nodes = [
        {"proposition_id": "G4-TC1",
         "task_level": "A_PROPOSITION_EXTRACTION",
         "text": "Manifestation (prakāśa) is not a passive, inert light; it shows the world.",
         "kind": "TEXTUAL_CLAIM", "explicitness": "EXPLICIT",
         "commitment": "ASSERTS", "derived_from": "L2/C1 (the manifestation is not inert)",
         "grounding": _grounding(), "boundary": "", "status": "MACHINE_PROPOSED"},
        {"proposition_id": "G4-CRYSTAL",
         "task_level": "A_PROPOSITION_EXTRACTION",
         "text": "A light that merely showed the world without knowing that it showed it would be no different from crystal — it would reflect, but be inert.",
         "kind": "TEXTUAL_CLAIM", "explicitness": "EXPLICIT",
         "commitment": "ASSERTS", "derived_from": "C1 (the crystal contrast)",
         "grounding": _grounding(),
         "boundary": "the crystal is the inert contrast, not the subject of the doctrine",
         "status": "MACHINE_PROPOSED"},
        {"proposition_id": "G4-DIST",
         "task_level": "B_ARGUMENT_RECONSTRUCTION",
         "text": "Bare showing (prakāśa alone) is distinct from self-aware manifesting; the distinguishing mark is self-awareness in the act (vimarśa).",
         "kind": "TEXTUAL_CLAIM", "explicitness": "RECONSTRUCTED",
         "commitment": "ASSERTS", "derived_from": "L2 (showing ≠ knowing-it-shows)",
         "grounding": _grounding(), "boundary": "", "status": "MACHINE_PROPOSED"},
        {"proposition_id": "G4-TC2",
         "task_level": "A_PROPOSITION_EXTRACTION",
         "text": "The essence of light is the reflexive-awareness (vimarśa) — the light's own grasp of itself in the act of manifesting.",
         "kind": "TEXTUAL_CLAIM", "explicitness": "EXPLICIT",
         "commitment": "ASSERTS", "derived_from": "C1/L2 (vimarśa as the essence)",
         "grounding": _grounding(),
         "boundary": "the reflexivity claim is established; the full powers/lordship account is developed in later vimarśas",
         "status": "MACHINE_PROPOSED"},
        {"proposition_id": "G4-CONC",
         "task_level": "A_PROPOSITION_EXTRACTION",
         "text": "What makes the light conscious (rather than a thing) is that it is aware of itself in the very act of manifesting.",
         "kind": "CONCLUSION", "explicitness": "RECONSTRUCTED",
         "commitment": "ASSERTS", "derived_from": "CONCEPTUAL_DISTINCTION over G4-DIST + G4-TC2",
         "grounding": _grounding(), "boundary": "", "status": "MACHINE_PROPOSED"},
        {"proposition_id": "G4-IC1",
         "task_level": "C_SYSTEMATIC_INTERPRETATION",
         "text": "Abhinavagupta identifies this self-knowing with the supreme speech (parā-vāk) and with the Lord's freedom (svātantrya) and lordship (aiśvarya).",
         "kind": "INTERPRETIVE_CLAIM", "explicitness": "RECONSTRUCTED",
         "commitment": "ASSERTS", "derived_from": "C1 (the identification with the Word)",
         "grounding": _grounding(),
         "boundary": "the identification with parā-vāk is the C1's extension, not a bare textual assertion",
         "status": "MACHINE_PROPOSED"},
    ]

    inferences = [
        # the distinguishing case: showing ≠ knowing-it-shows
        {"inference_id": "G4-INF-DIST",
         "premise_ids": ["G4-TC1", "G4-CRYSTAL"],
         "conclusion_ids": ["G4-DIST"],
         "scheme": "CONCEPTUAL_DISTINCTION",
         "rationale": "If manifestation were only bare showing (G4-TC1), it would be like crystal — it would reflect but not know it reflected (G4-CRYSTAL). Hence bare showing is distinct from self-aware manifesting (G4-DIST).",
         "defeaters": [], "status": "MACHINE_PROPOSED"},
        # the conclusion (G4-TC2 is TEXTUALLY asserted by the C1, not derived here)
        {"inference_id": "G4-INF-CONC",
         "premise_ids": ["G4-TC2", "G4-DIST"],
         "conclusion_ids": ["G4-CONC"],
         "scheme": "CONCEPTUAL_DISTINCTION",
         "rationale": "The distinguishing mark of consciousness is self-awareness in manifesting (G4-TC2 + G4-DIST); that is what makes the light conscious rather than a thing (G4-CONC).",
         "defeaters": [], "status": "MACHINE_PROPOSED"},
        # the interpretive identification
        {"inference_id": "G4-INF-IC",
         "premise_ids": ["G4-CONC"],
         "conclusion_ids": ["G4-IC1"],
         "scheme": "INTERPRETIVE_CLAIM",
         "rationale": "The C1 identifies the self-knowing light with the parā-vāk and the Lord's freedom/lordship — an interpretive identification, not a bare textual assertion.",
         "defeaters": [], "status": "MACHINE_PROPOSED"},
    ]

    boundary = {
        "text": ("The passage establishes that the essence of light is reflexive-awareness (vimarśa), not the bare "
                 "showing of objects. It does NOT by itself establish the full account of the powers and the Lordship "
                 "(developed in the following vimarśas, V2-I / V2-S), nor that language produces the self-grasp."),
        "not_claiming": ["the full account of the powers and the Lordship",
                         "that language produces the self (language is its form, not its producer)"],
        "philological": {"proof_id": V2H_PROOF_ID, "status": "P0"},
    }

    research_question = "Is the essence of light bare showing (prakāśa) or reflexive awareness (vimarśa)?"

    review_note = {
        "ESSENCE_IS_TEXTUAL": "G4-TC2 (vimarśa is the essence) is TEXTUALLY asserted by the C1 ('the claim is that the essence of light is the reflexive awareness... it is the manifestation's own nature'), NOT inferred from G4-DIST. So no exhaustiveness premise (a third feature accounting for non-inert manifestation) is smuggled in. If a reviewer disagrees that the C1 asserts the essence, G4-TC2 should be demoted to task_level B and its warrant re-examined.",
        "status": "MACHINE_PROPOSED",
    }

    debate_frame = {
        "question": research_question,
        "object_of_dispute": "the nature of light: bare manifestation (prakāśa) vs reflexive awareness (vimarśa)",
        "concept_refs": ["prakāśa", "vimarśa", "parā-vāk", "svātantrya", "aiśvarya"],
        "shared_ground": ["the light manifests the world", "a merely-inert showing would be unconscious"],
        "disputed_ground": ["whether the essence of light is the bare showing or the self-awareness"],
        "semantic_alignments": [
            {"left_term": "prakāśa", "right_term": "manifestation / bare showing",
             "relation": "SAME_SENSE", "level": "CONCEPTUAL", "context": [V2H_C1_ID],
             "rationale": "prakāśa = the light's showing of objects",
             "status": "MACHINE_PROPOSED"},
            {"left_term": "vimarśa", "right_term": "reflexive awareness / self-grasping",
             "relation": "SAME_SENSE", "level": "CONCEPTUAL", "context": [V2H_C1_ID],
             "rationale": "vimarśa = the light's self-awareness in manifesting (the heart of the doctrine)",
             "status": "MACHINE_PROPOSED"},
            {"left_term": "prakāśa", "right_term": "vimarśa",
             "relation": "DIFFERENT", "level": "CONCEPTUAL", "context": [V2H_C1_ID],
             "rationale": "the whole distinction: showing ≠ self-aware showing; vimarśa is the essence, not an added quality",
             "status": "MACHINE_PROPOSED"},
        ],
    }

    return {
        "gold_id": "ARG-GOLD-004",
        "work_id": "ipvv",
        "passage": V2H_PASSAGE_ID,
        "title": "The Essence of Light: prakāśa vs vimarśa (V2-H)",
        "structure": "CONCEPTUAL_DISTINCTION",
        "review_note": review_note,
        "research_question": research_question,
        "nodes": nodes,
        "inferences": inferences,
        "boundary": boundary,
        "debate_frame": debate_frame,
        "status": "MACHINE_PROPOSED",
    }
