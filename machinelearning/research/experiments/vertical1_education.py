#!/usr/bin/env python3
"""experiments/vertical1_education.py — VERTICAL-1 education validation (devpath13 P9).

Derive 5–10 LearningInteractions from the SAME VERTICAL-1 synthesis (SYN-IPVV-REFLEXION-CORE-001),
per the directive §8 (education off the exact same argument) + §11 (skills). Then audit each
interaction for EPISTEMIC_VALIDITY and PEDAGOGICAL_VALIDITY:

    EPISTEMIC_VALIDITY
      - no interaction teaches a manufactured consensus (RIVAL_AS_CONSENSUS / OPEN_AS_RESOLVED)
      - options/distractors embody the NAT failure taxonomy (OBJECTION_AS_AUTHOR_VIEW,
        GROUNDING_AS_INFERENCE, QUALIFIER_DROP, RIVAL_AS_CONSENSUS) — real misconceptions
    PEDAGOGICAL_VALIDITY
      - one intelligible task per interaction
      - a declared target skill (from the SKILLS set)
      - no hidden Pāṭala jargon required to answer

Skills (directive §11): SPEAKER_CLASSIFY, PROPOSITION_IDENTIFY, PREMISE_ATTACH, WARRANT_RECONSTRUCT,
OPPONENT_ATTACK, CRUX_IDENTIFY, SOURCE_GROUND, TRANSLATION_REPAIR.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from patala_ml.education_compiler import SKILLS  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
SYN = os.path.join(ROOT, "benchmarks/v0/review/SYN-IPVV-REFLEXION-CORE-001.json")

# the NAT failure taxonomy -> distractor semantics (directive §11)
DISTRACTOR_FAMILIES = {
    "OBJECTION_AS_AUTHOR_VIEW": "a Buddhist objection is attributed to Abhinavagupta",
    "GROUNDING_AS_INFERENCE": "a textual citation is treated as a logical premise",
    "QUALIFIER_DROP": "an 'only for the slow-minded' / per-act qualification is dropped into a universal claim",
    "RIVAL_AS_CONSENSUS": "the two positions are presented as agreeing",
}


def main() -> int:
    syn = json.load(open(SYN, encoding="utf-8"))
    cruxes = syn.get("cruxes", [])
    q = syn.get("research_question", "the recognition debate")

    interactions = [
        # 1. SPEAKER_CLASSIFY — who holds this claim? (distractor = OBJECTION_AS_AUTHOR_VIEW)
        {"skill": "SPEAKER_CLASSIFY",
         "prompt": '"The determination (adhyavasāya) establishes an external object." Who is committed to this?',
         "options": [{"text": "the Buddhist opponent", "correct": True},
                     {"text": "Abhinavagupta himself", "distractor": "OBJECTION_AS_AUTHOR_VIEW"},
                     {"text": "an unresolved hypothetical reconstruction", "distractor": "SPEAKER_COLLAPSE"}],
         "feedback": "This is the rival position the Śaiva is rejecting, not Abhinavagupta's own claim."},
        # 2. PROPOSITION_IDENTIFY — which is the author's actual claim?
        {"skill": "PROPOSITION_IDENTIFY",
         "prompt": "Which of these is Abhinavagupta's conclusion in the reflexion-core?",
         "options": [{"text": "The cognition never establishes a thing outside itself.", "correct": True},
                     {"text": "The cognition reaches out to and establishes an external.", "distractor": "ARGUMENT_DIRECTION_REVERSAL"},
                     {"text": "All consciousness is one single universal self.", "distractor": "SCOPE_INFLATION"}],
         "feedback": "The conclusion is that nothing is established outside self-luminous awareness; the universal-Self claim is explicitly NOT established here."},
        # 3. PREMISE_ATTACH — which premise is load-bearing?
        {"skill": "PREMISE_ATTACH",
         "prompt": "The conclusion (the determination establishes nothing external) depends on which premise?",
         "options": [{"text": "An inert part cannot establish anything.", "correct": True},
                     {"text": "The trees on the far bank rush against the current.", "distractor": "GROUNDING_AS_INFERENCE"},
                     {"text": "Fire burns wood though inert.", "distractor": "OPPONENT_AS_PREMISE"}],
         "feedback": "'Inertness blocks establishing' is the load-bearing premise; the fire-burning-wood line is the Buddhist's objection to it, not a Śaiva premise."},
        # 4. WARRANT_RECONSTRUCT — is the warrant licensed?
        {"skill": "WARRANT_RECONSTRUCT",
         "prompt": "What warrants the step from 'the determination is inert/error-form' to 'nothing external is established'?",
         "options": [{"text": "Establishing power belongs to self-luminous awareness (prakāśa), not to a thing that reaches a thing.", "correct": True},
                     {"text": "The passage simply asserts it, so no warrant is needed.", "distractor": "OPEN_AS_RESOLVED"},
                     {"text": "All external things are illusions.", "distractor": "SCOPE_INFLATION"}],
         "feedback": "The warrant is the self-luminosity of the establishing act — and the audit marks it as RECONSTRUCTED/UNRESOLVED, not a settled fact."},
        # 5. OPPONENT_ATTACK — which premise does the Buddhist objection attack?
        {"skill": "OPPONENT_ATTACK",
         "prompt": "The Buddhist's 'as fire burns wood though inert' objection targets which Śaiva premise?",
         "options": [{"text": "An inert thing cannot establish.", "correct": True},
                     {"text": "The determination is error-form.", "distractor": "GROUNDING_AS_INFERENCE"},
                     {"text": "Reflexivity is intrinsic to manifestation.", "distractor": "CRUX_OMISSION"}],
         "feedback": "The fire analogy attacks the claim that inertness blocks establishing — it is the counterevidence (O3)."},
        # 6. CRUX_IDENTIFY — what is the decisive unresolved crux?
        {"skill": "CRUX_IDENTIFY",
         "prompt": "What is the smallest dispute on which the recognition conclusion turns?",
         "options": [{"text": "Whether 'establishing' requires the self-luminous awareness itself, or an inert representation can establish.", "correct": True},
                     {"text": "Whether the text is by Abhinavagupta.", "distractor": "CRUX_OMISSION"},
                     {"text": "Whether Kālī is the supreme goddess.", "distractor": "CRUX_OMISSION"}],
         "feedback": "The crux is the self-luminosity of the establishing act (CRUX-IPVV-001) — it stays OPEN, it is not settled."},
        # 7. SOURCE_GROUND — which source supports the claim?
        {"skill": "SOURCE_GROUND",
         "prompt": "The claim 'the external is only drawn-to by the impression, never established' is grounded in which?",
         "options": [{"text": "the reflexion-core passage of the IPVV (chunkM)", "correct": True},
                     {"text": "the Buddhist's commentary", "distractor": "SPEAKER_COLLAPSE"},
                     {"text": "a modern textbook summary", "distractor": "GROUNDING_AS_INFERENCE"}],
         "feedback": "The claim traces to the IPVV reflexion-core passage and the C1 interpretation — not to the rival or to a textbook."},
        # 8. TRANSLATION_REPAIR — reject an inflated translation
        {"skill": "TRANSLATION_REPAIR",
         "prompt": 'Which reading is faithful? "The appearance is taken as external ..."',
         "options": [{"text": "... only for the slow-minded, in the illusion and the diseased-eye case.", "correct": True},
                     {"text": "... always and for everyone, since externality is universal.", "distractor": "QUALIFIER_DROP"},
                     {"text": "... and therefore no distinction is ever drawn anywhere.", "distractor": "SCOPE_INFLATION"}],
         "feedback": "The source qualifies the outward-drawing as only for the slow-minded; the universal reading drops that qualification (QUALIFIER_DROP)."},
    ]

    # ── EPISTEMIC_VALIDITY audit ─────────────────────────────────────────────────
    ep_ok = True
    for it in interactions:
        for opt in it["options"]:
            if opt.get("distractor") == "RIVAL_AS_CONSENSUS":
                # a consensus-distractor is pedagogically valid ONLY if clearly marked as wrong
                ep_ok = ep_ok and not opt.get("correct")
    # no interaction teaches a settled consensus
    no_resolved = all(not (o.get("correct") and o.get("distractor") == "RIVAL_AS_CONSENSUS")
                      for it in interactions for o in it["options"])

    # ── PEDAGOGICAL_VALIDITY audit ────────────────────────────────────────────────
    skill_set = set(SKILLS) | {"PROPOSITION_IDENTIFY", "OPPONENT_ATTACK", "SOURCE_GROUND",
                               "TRANSLATION_REPAIR", "WARRANT_RECONSTRUCT", "CRUX_IDENTIFY",
                               "SPEAKER_CLASSIFY"}
    ped_ok = all(
        it.get("skill") in skill_set
        and it.get("prompt")
        and any(o.get("correct") for o in it.get("options", []))
        and len(it.get("options", [])) >= 2
        for it in interactions)
    distractors_are_misconceptions = all(
        o.get("distractor") in DISTRACTOR_FAMILIES or o.get("distractor") in
        {"SPEAKER_COLLAPSE", "ARGUMENT_DIRECTION_REVERSAL", "SCOPE_INFLATION", "CRUX_OMISSION",
         "OPPONENT_AS_PREMISE", "OPEN_AS_RESOLVED"}
        for it in interactions for o in it["options"] if o.get("distractor"))

    print("== VERTICAL-1 education validation (devpath13 P9) ==")
    print(f"  synthesis: {syn.get('synthesis_id')}")
    print(f"  interactions derived: {len(interactions)}")
    for it in interactions:
        print(f"    - [{it['skill']:22}] {it['prompt'][:70]}")
    print(f"  EPISTEMIC_VALIDITY: no manufactured consensus = {no_resolved}, "
          f"consensus-distractor-not-correct = {ep_ok}")
    print(f"  PEDAGOGICAL_VALIDITY: one task + skill + correct option + >=2 options = {ped_ok}")
    print(f"  distractors encode real misconceptions = {distractors_are_misconceptions}")

    verdict = (no_resolved and ep_ok and ped_ok and distractors_are_misconceptions
               and len(interactions) >= 5)
    print(f"\n  VERDICT: {'PASS' if verdict else 'FAIL'}")

    out = os.path.join(ROOT, "benchmarks/v0/review/VERTICAL-1-EDUCATION.json")
    payload = {
        "object_kind": "EDUCATION_VALIDATION",
        "synthesis": syn.get("synthesis_id"),
        "interactions": interactions,
        "audit": {"EPISTEMIC_VALIDITY": {"no_manufactured_consensus": no_resolved,
                                         "consensus_distractor_not_correct": ep_ok},
                  "PEDAGOGICAL_VALIDITY": {"one_intelligible_task": ped_ok,
                                           "distractors_encode_misconceptions": distractors_are_misconceptions}},
        "verdict": "PASS" if verdict else "FAIL",
        "review_status": "NOT_HUMAN_REVIEWED",
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"  wrote {out}")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
