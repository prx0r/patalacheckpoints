"""patala_ml/gold002.py — ARG-GOLD-002: the objection→reply argument (V2-L, the non-constructed "I").

The second hand-constructed gold argument, deliberately a DIFFERENT structure from ARG-GOLD-001:
an OBJECTION → REPLY dialectic (the IPVV's nanu→āha move). It carries the full
Proposition/Inference/Defeater shape + the DebateFrame/SemanticAlignment wrapper.

Source: c1_V2L-nonconstructed-I.md — "if reflexive awareness is joined to linguistic form, why is
it not simply a conceptual construction (vikalpa)?" → Abhinavagupta replies by examining what
construction does, and denying the "I"-awareness is one of those relations.

Real resolvable passage id: pt:passage:ipvv:chunkV2-L-sastho-vimarsa-smrti-apohana.md
"""
from __future__ import annotations

V2L_PASSAGE_ID = "pt:passage:ipvv:chunkV2-L-sastho-vimarsa-smrti-apohana.md"
V2L_C1_ID = "V2L-nonconstructed-I"
V2L_L200_ID = "l200/V2L-sastho-vimarsa-smrti-apohana.md"
V2L_PROOF_ID = "pp:ipvv:v2l:p0"


def build_gold_002() -> dict:
    """ARG-GOLD-002 — the objection→reply (non-constructed I, V2-L)."""

    # ── proposition nodes (TEXTUAL vs INTERPRETIVE, EXPLICIT vs RECONSTRUCTED vs IMPLICIT) ──
    nodes = [
        # OBJECTION (the pūrvapakṣa)
        {"proposition_id": "G2-OBJ",
         "text": "If reflexive awareness is joined to linguistic form, why is it not simply a conceptual construction (vikalpa)?",
         "kind": "OBJECTION", "explicitness": "EXPLICIT",
         "grounding": {"passage_id": V2L_PASSAGE_ID, "c1_id": V2L_C1_ID,
                       "l200_assertion_id": V2L_L200_ID},
         "boundary": "the objection presupposes that linguistic articulation implies conceptual construction",
         "status": "MACHINE_PROPOSED"},
        # the reply's first step: what construction does
        {"proposition_id": "G2-TC1",
         "text": "Conceptual construction (vikalpa) operates by combining, differentiating, or determining contents.",
         "kind": "TEXTUAL_CLAIM", "explicitness": "EXPLICIT",
         "grounding": {"passage_id": V2L_PASSAGE_ID, "c1_id": V2L_C1_ID,
                       "l200_assertion_id": V2L_L200_ID},
         "boundary": "", "status": "MACHINE_PROPOSED"},
        # the key move: the I-awareness is not one of those relations
        {"proposition_id": "G2-TC2",
         "text": "The awareness expressed as 'I' (ahaṃ-pratyavamarśa) is not treated as one more relation constructed between independently given elements.",
         "kind": "TEXTUAL_CLAIM", "explicitness": "EXPLICIT",
         "grounding": {"passage_id": V2L_PASSAGE_ID, "c1_id": V2L_C1_ID,
                       "l200_assertion_id": V2L_L200_ID},
         "boundary": "", "status": "MACHINE_PROPOSED"},
        # the conclusion of the reply
        {"proposition_id": "G2-CONC",
         "text": "Linguistic articulation does not show that the underlying self-awareness is itself produced by conceptual determination.",
         "kind": "CONCLUSION", "explicitness": "RECONSTRUCTED",
         "grounding": {"passage_id": V2L_PASSAGE_ID, "c1_id": V2L_C1_ID,
                       "l200_assertion_id": V2L_L200_ID},
         "boundary": "this passage preserves reflexive awareness DISTINCT from conceptual construction; it does NOT by itself establish a universal subject",
         "dialectical_role": "REPLY", "responds_to": ["G2-OBJ"],
         "status": "MACHINE_PROPOSED"},
         # (G2-IMPL node REMOVED per REVIEW-2026-08-12-MODEL-1: the reconstructed warrant 'articulation !=
         #  construction' belongs on the InferenceRule, not as an ordinary Proposition. It is carried by
         #  G2-INF1.warrant and projected into ASPIC as the reply rule r_reply.)
        # an interpretive claim: what the distinction preserves
        {"proposition_id": "G2-IC1",
         "text": "Abhinavagupta preserves a distinction between reflexive self-awareness and the conceptual operations that articulate it.",
         "kind": "INTERPRETIVE_CLAIM", "explicitness": "RECONSTRUCTED",
         "grounding": {"passage_id": V2L_PASSAGE_ID, "c1_id": V2L_C1_ID,
                       "l200_assertion_id": V2L_L200_ID},
         "boundary": "", "status": "MACHINE_PROPOSED"},
    ]

    # ── inference nodes (the reply's moves) ────────────────────────────────────
    inferences = [
        {"inference_id": "G2-INF1",
         "premise_ids": ["G2-TC1", "G2-TC2"],
         "conclusion_ids": ["G2-CONC"],
         "scheme": "CONCEPTUAL_DISTINCTION",
         "warrant": "RECONSTRUCTED_WARRANT: being expressible in language does not entail being a product of conceptual determination (articulation ≠ construction) — carried on the InferenceRule, not a Proposition node (per REVIEW-2026-08-12-MODEL-1 / IR-F-04).",
         "rationale": "The objection is answered by showing what construction does (G2-TC1) and that the 'I'-awareness is not one of those constructed relations (G2-TC2) — so the 'I' is not shown to be a construction.",
         "defeaters": [
             {"defeater_id": "G2-DEF1", "description": "The reply relies on the reconstructed warrant (articulation ≠ construction). If language-use were itself a construction, the reply would fail.",
              "type": "FAILED_PREMISE", "candidate_evidence_ids": [], "status": "PROPOSED"},
         ],
         "status": "MACHINE_PROPOSED"},
    # (G2-INF2 removed per REVIEW-2026-08-12-MODEL-1 / IR-F-02: G2-IC1 states a distinction the passage
    #  makes; it is a TEXTUAL/INTERPRETIVE grounding, not an inference derived from G2-CONC.)
    ]

    # ── the honest boundary ───────────────────────────────────────────────────
    boundary = {
        "text": "The passage establishes that the 'I'-awareness is not shown to be a conceptual construction. It does NOT by itself establish the stronger Śaiva claim that this self-awareness belongs to a single universal subject — that depends on arguments elsewhere.",
        "not_claiming": ["a universal single subject", "that the 'I'-awareness is entirely non-linguistic"],
        "philological": {"proof_id": V2L_PROOF_ID, "status": "P0"},
    }

    # ── the DebateFrame / SemanticAlignment wrapper (the anti-fake-contradiction layer) ──
    debate_frame = {
        "question": "Is reflexive self-awareness ('I') a conceptual construction, given it is linguistically expressed?",
        "object_of_dispute": "the nature of the 'I'-awareness (ahaṃ-pratyavamarśa) vs conceptual construction (vikalpa)",
        "concept_refs": ["vikalpa", "ahaṃ-pratyavamarśa", "apohana"],
        "shared_ground": ["self-awareness is linguistically expressed"],
        "disputed_ground": ["whether linguistic articulation implies conceptual construction"],
        "semantic_alignments": [
            {"left_term": "vikalpa", "right_term": "conceptual construction",
             "relation": "SAME_SENSE", "context": [V2L_C1_ID], "rationale": "the C1 uses vikalpa for conceptual construction",
             "status": "MACHINE_PROPOSED"},
            {"left_term": "ahaṃ-pratyavamarśa", "right_term": "'I'-awareness",
             "relation": "SAME_SENSE", "context": [V2L_C1_ID], "rationale": "reflexive apprehension as 'I'",
             "status": "MACHINE_PROPOSED"},
        ],
    }

    return {
        "gold_id": "ARG-GOLD-002",
        "work_id": "ipvv",
        "passage": V2L_PASSAGE_ID,
        "title": "The Non-constructed I (objection → reply, V2-L)",
        "structure": "OBJECTION_REPLY",
        "nodes": nodes,
        "inferences": inferences,
        "boundary": boundary,
        "debate_frame": debate_frame,
        "status": "MACHINE_PROPOSED",
    }
