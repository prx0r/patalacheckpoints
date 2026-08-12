"""patala_ml/gold005.py — ARG-GOLD-005: the ambiguous case (V3-I, "the difference is real").

The fifth hand-constructed gold argument, deliberately AMBIGUOUS: two defensible reconstructions of what
"the difference is real" means in V3-I. This is the case that trains viruddha to NOT manufacture a
contradiction — the two readings affirm the same proposition but answer different questions (what the
passage *refutes* vs what it *positively affirms*).

  - **Reading A (NEGATIVE):** "the difference is real" means the illusion/ignorance thesis is REFUTED —
    the difference cannot be dismissed as an 'un-explainable' (anirvācya) ignorance (reductio: of whom?
    no separate jīvas; anirvācya is a refusal to answer). Difference is real = not merely apparent.
  - **Reading B (POSITIVE):** "the difference is real" means difference is the SELF'S OWN MANIFESTATION —
    a positive feature of consciousness's freedom (the full positive account developed in V3-G/H, V2-S).

Built WITH the philosophical-IR shape (per ARGUMENT-IR-VISION.md / Deep Research 10-11):
  - `commitment` on every node · derivational `Proposition` · `research_question`
  - TWO `positions` (Position A / Position B) under the frame
  - THREE-LEVEL `SemanticAlignment` (LEXICAL / CONCEPTUAL / PROPOSITIONAL) — the anti-fake-contradiction layer

Source: c1_V3I-difference-real.md + pilot_V3I_L2_read.md.
Real resolvable passage id: pt:passage:ipvv:chunkV3-I-kriya-caturtho-close-k20-21.md
"""
from __future__ import annotations

V3I_PASSAGE_ID = "pt:passage:ipvv:chunkV3-I-kriya-caturtho-close-k20-21.md"
V3I_C1_ID = "V3I-difference-real"
V3I_L200_ID = "l200/V3I-kriya-caturtho-close-k20-21.md"
V3I_PROOF_ID = "pp:ipvv:v3i:p0"


def _grounding():
    return {"passage_id": V3I_PASSAGE_ID, "c1_id": V3I_C1_ID, "l200_assertion_id": V3I_L200_ID}


def build_gold_005() -> dict:
    """ARG-GOLD-005 — the ambiguous case (V3-I): two defensible reconstructions."""
    nodes = [
        # the objection (attributed to the monist/illusionist opponent, NOT Abhinava's own view)
        {"proposition_id": "G5-OBJ",
         "task_level": "A_PROPOSITION_EXTRACTION",
         "text": "If consciousness is one and the difference of things is mere ignorance, how is action possible — for action needs a distinct agent and object?",
         "kind": "OBJECTION", "explicitness": "EXPLICIT",
         "commitment": "ATTRIBUTES_TO_OPPONENT", "derived_from": "C1/L2 (the sharpest objection)",
         "grounding": _grounding(),
         "boundary": "the objection presupposes that a unified consciousness leaves no distinct object for action",
         "status": "MACHINE_PROPOSED"},
        # the shared textual basis both readings accept
        {"proposition_id": "G5-TC1",
         "task_level": "A_PROPOSITION_EXTRACTION",
         "text": "The single re-recollection marked by the will-to-do (cikīrṣālakṣaṇa parāmarśa) joins the agent and the object; action is possible in the one consciousness.",
         "kind": "CONCLUSION", "explicitness": "EXPLICIT",
         "dialectical_role": "REPLY", "responds_to": ["G5-OBJ"],
         "commitment": "ASSERTS", "derived_from": "L2 (the will-to-do joins agent and object)",
         "grounding": _grounding(), "boundary": "", "status": "MACHINE_PROPOSED"},
        # the reductio against the illusion thesis (shared basis for Reading A)
        {"proposition_id": "G5-TC2",
         "task_level": "A_PROPOSITION_EXTRACTION",
         "text": "The difference cannot be an 'un-explainable' (anirvācya) ignorance: of whom would it be? The one-form reality cannot have it; the separate souls cannot bear it; 'un-explainable' is a refusal to answer.",
         "kind": "TEXTUAL_CLAIM", "explicitness": "EXPLICIT",
         "commitment": "ASSERTS", "derived_from": "C1/L2 (the reductio against anirvācya)",
         "grounding": _grounding(),
         "boundary": "this refutes the illusion-thesis; it does not by itself give the positive account of difference",
         "status": "MACHINE_PROPOSED"},
        # Reading A (NEGATIVE) conclusion
        {"proposition_id": "G5-CONC-A",
         "task_level": "A_PROPOSITION_EXTRACTION",
         "text": "The difference is real — cognition rests in difference as it does not rest in non-difference.",
         "kind": "CONCLUSION", "explicitness": "RECONSTRUCTED",
         "commitment": "ASSERTS", "derived_from": "REDUCTIO over G5-TC2",
         "reading": "A_NEGATIVE",
         "grounding": _grounding(),
         "boundary": "Reading A: difference-real = the illusion thesis is refuted; NOT a full positive metaphysics of difference",
         "status": "MACHINE_PROPOSED"},
        # Reading B (POSITIVE) conclusion
        {"proposition_id": "G5-CONC-B",
         "task_level": "C_SYSTEMATIC_INTERPRETATION",
         "text": "The difference is real as the self's own manifestation — the positive account of difference (developed in V3-G/H, V2-S).",
         "kind": "CONCLUSION", "explicitness": "RECONSTRUCTED",
         "commitment": "ASSERTS", "derived_from": "OTHER over G5-TC1 + G5-TC2 (positive extension)",
         "reading": "B_POSITIVE",
         "support_scope": ["LOCAL_TEXT", "SAME_WORK"],
         "cross_passage_grounding": ["V3-G", "V3-H", "V2-S"],
         "derivation": "SYSTEMATIC_INTERPRETATION (NOT a local inference from G5-TC1+G5-TC2)",
         "grounding": _grounding(),
         "boundary": "Reading B: difference-real = the self's own manifestation; the full positive account is developed elsewhere (V3-G/H, V2-S)",
         "status": "MACHINE_PROPOSED"},
    ]

    inferences = [
        # (G5-INF-ANS removed per REVIEW-2026-08-12-MODEL-1: the objection is answered by G5-TC1
        #  via a DIALECTICAL RESPONDS_TO edge, not an inference. Kept as dialectical_role on G5-TC1.)

        # Reading A: the reductio establishes difference-real negatively
        {"inference_id": "G5-INF-NEG",
         "premise_ids": ["G5-TC2"],
         "conclusion_ids": ["G5-CONC-A"],
         "scheme": "REDUCTIO",
         "rationale": "The 'un-explainable ignorance' account collapses (G5-TC2) — so the difference is real in the sense of not being mere ignorance (G5-CONC-A).",
         "defeaters": [], "status": "MACHINE_PROPOSED"},
    # (G5-INF-POS removed per REVIEW-2026-08-12-MODEL-1: G5-CONC-B is a SYSTEMATIC interpretation
    #  grounded in cross-passage material (V3-G/H, V2-S), NOT a local inference from G5-TC1+G5-TC2.)
    ]

    boundary = {
        "text": ("The passage establishes that the difference cannot be an 'un-explainable' (anirvācya) ignorance. "
                 "Whether 'the difference is real' is read negatively (refuting the illusion thesis) or positively "
                 "(difference as the self's manifestation) is a genuine crux — two defensible reconstructions. The "
                 "full positive account of the difference is developed elsewhere (V3-G/H, V2-S)."),
        "not_claiming": ["a full positive metaphysics of difference (developed elsewhere)",
                         "that absolute monism with ignorance is endorsed (the passage is not an absolute monism either)",
                         "that Reading A and Reading B contradict one another"],
        "philological": {"proof_id": V3I_PROOF_ID, "status": "P0"},
    }

    research_question = "What does 'the difference is real' mean — does the passage positively affirm difference as the self's manifestation, or negatively establish it by refuting the 'un-explainable ignorance' thesis?"

    debate_frame = {
        "question": research_question,
        "object_of_dispute": "the force of 'the difference is real' in V3-I",
        "concept_refs": ["anirvācya", "bheda", "cikīrṣālakṣaṇa parāmarśa", "sva-rūpa"],
        "shared_ground": ["the difference cannot be dismissed as anirvācya ignorance",
                          "action is the one will-to-do joining agent and object"],
        "disputed_ground": ["whether 'the difference is real' is a negative (refutation) or positive (self-manifestation) claim"],
        "positions": [
            {"position_id": "G5-POS-A", "label": "Reading A — MINIMAL / LOCAL",
             "question": "What does the passage itself establish?",
             "commitment": "the difference is real = the illusion/ignorance thesis is refuted (locally entailed)",
             "proposition_ids": ["G5-CONC-A"],
             "support_scope": ["LOCAL_TEXT"]},
            {"position_id": "G5-POS-B", "label": "Reading B — STRONGER / SYSTEMATIC",
             "question": "What stronger interpretation becomes supportable with wider corpus context?",
             "commitment": "the difference is real = difference is the self's own manifestation (contextually supported extension)",
             "proposition_ids": ["G5-CONC-B"],
             "support_scope": ["LOCAL_TEXT", "SAME_WORK"]},
        ],
        "semantic_alignments": [
            # LEXICAL level
            {"left_term": "anirvācya", "right_term": "'un-explainable' / refusal to answer",
             "relation": "SAME_SENSE", "level": "LEXICAL", "context": [V3I_C1_ID],
             "rationale": "anirvācya = 'that which cannot be spoken of'; the C1 treats it as a refusal to answer (yakṣa-speech)",
             "status": "MACHINE_PROPOSED"},
            # CONCEPTUAL level — the key term differs in mode across the two readings
            {"left_term": "the difference (A_NEGATIVE)", "right_term": "the difference (B_POSITIVE)",
             "relation": "OVERLAPPING", "level": "CONCEPTUAL", "context": [V3I_C1_ID],
             "rationale": "Both readings affirm difference is real; they differ in the MODE — A = refuted-illusion status, B = the self's manifestation. Overlapping, not contradictory.",
             "status": "MACHINE_PROPOSED"},
            # PROPOSITIONAL level — the two conclusions answer different questions
            {"left_term": "G5-CONC-A (difference is not ignorance)",
             "right_term": "G5-CONC-B (difference is the self's manifestation)",
             "relation": "OVERLAPPING", "level": "PROPOSITIONAL", "context": [V3I_C1_ID],
             "rationale": "CONC-A answers 'what does the passage refute'; CONC-B answers 'what does it positively affirm'. Same shared ground, different question — NOT a VIRUDDHA (opposition) pair.",
             "status": "MACHINE_PROPOSED"},
        ],
    }

    return {
        "gold_id": "ARG-GOLD-005",
        "work_id": "ipvv",
        "passage": V3I_PASSAGE_ID,
        "title": "The Difference is Real: local vs systematic scope (V3-I)",
        "structure": "INTERPRETIVE_SCOPE",
        "review_note": {
            "NOT_AMBIGUITY": "This is NOT a genuine 'two meanings' ambiguity. The two readings are different INFERENTIAL STRENGTHS: Reading A is LOCALLY ENTAILED (this passage refutes the anirvācya-ignorance thesis); Reading B is a CONTEXTUALLY SUPPORTED EXTENSION (difference as the self's manifestation) that relies on broader doctrine (V3-G/H, V2-S). The crux is not 'which reading is true' but: does THIS passage itself license the positive metaphysical interpretation, or does that require importing the broader doctrine?",
            "SUPPORT_SCOPE_FIRST_CLASS": "This gold case is exactly the kind that forces support_scope (LOCAL_TEXT / LOCAL_CONTEXT / SAME_WORK / CROSS_WORK / SYSTEMATIC_RECONSTRUCTION) to be considered first-class in the IR — not yet added to the ontology, but flagged.",
            "status": "MACHINE_PROPOSED",
        },
        "research_question": research_question,
        "nodes": nodes,
        "inferences": inferences,
        "boundary": boundary,
        "debate_frame": debate_frame,
        "status": "MACHINE_PROPOSED",
    }
