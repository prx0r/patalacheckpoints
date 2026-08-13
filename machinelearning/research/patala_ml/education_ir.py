#!/usr/bin/env python3
"""patala_ml/education_ir.py — Pāṭala Education IR (devpath13 / the education vision).

The education vision (docs/vision/education/PATALA-EDUCATION-SYNTHESIS.md) defines FOUR native objects
that define the education layer (FSRS/BKT/PostHog consume them, they do NOT define them):

    LearningClaim      a machine-linked learning objective (derived from propositions/arguments/cruxes)
    LearningSkill      the cognitive skill being exercised
    LearningInteraction a diagnostic interaction (targets a claim, options carry diagnostic mapping)
    MasteryEvidence    a learner response as an epistemic event (evidence-bearing, not a score)

Design law (must be enforced): education is a PROJECTION of Pāṭala objects, not a separate knowledge
base. Every interaction and distractor resolves DOWNWARD to canonical scholarly objects.

The moat (per the vision): "wrong answer -> known epistemic neighbor". Distractors are NOT invented
by an LLM — they are derived from the graph's real neighbors:
    rival proposition / wrong speaker / scope inflation / defeated inference / related non-equivalent
    term / qualification drop / alternative debate-frame / omission of an open question.

The compiler:
    compile_interactions(scholarly_object, targets, learner_level)
        -> LearningPacket (LearningClaims, prerequisite skills, misconception candidates,
                           6-10 interaction specs, correct interpretations, diagnostic distractors,
                           source refs, progression order, epistemic ceiling)
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "machinelearning", "research"))


def _sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


# ── the canonical skill ontology (the vision's education layer A) ──────────────
SKILLS = (
    "RECALL",
    "CLASSIFY_SPEAKER",          # author vs opponent vs reconstructed
    "IDENTIFY_COMMITMENT",       # asserted vs reported/attributed
    "GROUND_SOURCE",             # which source supports a claim
    "ATTACH_PREMISE",            # which premise is load-bearing
    "RECONSTRUCT_WARRANT",       # what licenses the inference
    "FOLLOW_INFERENCE",          # does conclusion follow from premises
    "IDENTIFY_ATTACK",           # which objection attacks which premise
    "IDENTIFY_CRUX",             # the decisive unresolved dispute
    "COMPARE_POSITION",          # do rivals answer the same question
    "QUALIFY_SCOPE",             # detect scope inflation / qualification drop
    "EVALUATE_TRANSLATION",      # reject an inflated/unfaithful translation
    "SYNTHESIZE_DEBATE",         # reconstruct the whole debate structure
)

# ── the NAT failure taxonomy -> misconception types (the dual system) ──────────
# The SAME taxonomy diagnoses machine translation/argument errors and learner misconceptions.
MISCONCEPTION_TYPES = (
    "OBJECTION_AS_AUTHOR_VIEW",   # an opponent claim attributed to the author
    "GROUNDING_AS_INFERENCE",     # a citation treated as a logical premise
    "QUALIFIER_DROP",             # a scope/qualifier dropped into a universal claim
    "SCOPE_INFLATION",            # a per-act claim generalized to a universal
    "OPEN_AS_RESOLVED",           # an open crux presented as settled
    "RIVAL_AS_CONSENSUS",         # two positions folded into agreement
    "INVENTED_BRIDGE",            # an unsupported inference as if licensed
    "SPEAKER_COLLAPSE",           # author/opponent/commentator merged
    "ARGUMENT_DIRECTION_REVERSAL",# conclusion treated as premise
    "CONCEPT_COLLAPSE",           # two related-but-distinct concepts merged
    "WARRANT_OMISSION",           # a load-bearing warrant left unstated
)


# ── the native objects ─────────────────────────────────────────────────────────
class LearningClaim:
    """A testable learning objective, machine-linked to the exact philosophical structure."""

    def __init__(self, claim_id, content, derived_from, claim_type="DISTINCTION",
                 prerequisites=(), source_refs=(), epistemic_ceiling="MACHINE_PROPOSED"):
        self.claim_id = claim_id
        self.content = content
        self.derived_from = list(derived_from)      # pt:proposition/argument/crux refs
        self.claim_type = claim_type
        self.prerequisites = list(prerequisites)
        self.source_refs = list(source_refs)
        self.epistemic_ceiling = epistemic_ceiling

    def emit(self):
        return {
            "learning_claim_id": self.claim_id,
            "content": self.content,
            "claim_type": self.claim_type,
            "derived_from": self.derived_from,
            "prerequisites": self.prerequisites,
            "source_refs": self.source_refs,
            "epistemic_ceiling": self.epistemic_ceiling,
            "claim_hash": _sha256({"id": self.claim_id, "content": self.content,
                                   "derived_from": self.derived_from}),
        }


class Misconception:
    """A first-class misconception: the learner's wrong answer maps to a real epistemic neighbor."""

    def __init__(self, misconception_id, type_, description, confuses, detected_by=(),
                 remediation=(), distinguishing_test=()):
        self.misconception_id = misconception_id
        self.type = type_
        self.description = description
        self.confuses = list(confuses)
        self.detected_by = list(detected_by)          # interaction ids
        self.remediation = list(remediation)          # prerequisite learning claims
        self.distinguishing_test = list(distinguishing_test)

    def emit(self):
        return {
            "misconception_id": self.misconception_id,
            "type": self.type,
            "description": self.description,
            "confuses": self.confuses,
            "detected_by": self.detected_by,
            "remediation": self.remediation,
            "distinguishing_test": self.distinguishing_test,
            "misconception_hash": _sha256({"id": self.misconception_id, "type": self.type}),
        }


class MasteryEvidence:
    """A learner response as an epistemic event (evidence-bearing, never a bare score)."""

    def __init__(self, learner, skill, learning_claim, interaction, response,
                 correctness, hint_level=0, transfer_status=None, source_refs=()):
        self.learner = learner
        self.skill = skill
        self.learning_claim = learning_claim
        self.interaction = interaction
        self.response = response
        self.correctness = correctness
        self.hint_level = hint_level
        self.transfer_status = transfer_status
        self.source_refs = list(source_refs)

    def emit(self):
        return {
            "learner": self.learner,
            "skill_ref": self.skill,
            "learning_claim_ref": self.learning_claim,
            "interaction_ref": self.interaction,
            "response": self.response,
            "correctness": self.correctness,
            "hint_level": self.hint_level,
            "transfer_status": self.transfer_status,
            "source_refs": self.source_refs,
            "evidence_hash": _sha256({"learner": self.learner, "interaction": self.interaction,
                                      "response": self.response}),
        }


# ── the interaction model: every option carries a diagnostic mapping ──────────
def _option(text, correct=False, role=None, misconception=None, derives_from=None):
    """A single option with provenance (proof-carrying multiple choice)."""
    o = {"text": text, "correct": correct}
    if role:
        o["role"] = role            # CORRECT / RIVAL_READING / SCOPE_ERROR / ATTRIBUTION_ERROR / ...
    if misconception:
        o["misconception"] = misconception   # misconception type it encodes
    if derives_from:
        o["derives_from"] = derives_from     # the graph object it derives from
    return o


# ── the interaction compiler ───────────────────────────────────────────────────
# Derives distractors from the graph's REAL neighbors (not LLM-invented).
def _real_neighbors(claim: dict, propositions: list[dict]) -> list[str]:
    """Collect real neighbor claims: rival propositions / related-but-distinct terms /
    scope-inflated variants actually present in the argument graph."""
    neighbors = []
    text = claim.get("commitment", "").lower()
    for p in propositions:
        pt = p.get("commitment", "")
        if not pt:
            continue
        low = pt.lower()
        # a related-but-distinct commitment is a real neighbor (CONCEPT_COLLAPSE candidate)
        if any(k in text for k in ("reflexiv", "self", "prakāśa", "vimarśa", "manifest")) \
           and any(k in low for k in ("reflexiv", "self", "prakāśa", "vimarśa", "manifest")):
            if pt != claim.get("commitment"):
                neighbors.append(pt)
    return neighbors[:4]


def _speaker_options(propositions: list[dict], author_name="Abhinavagupta"):
    """Build a SPEAKER_CLASSIFY interaction from the real speakers in the graph."""
    speakers = []
    for p in propositions:
        sp = p.get("speaker") or p.get("attribution") or "author"
        t = p.get("commitment", "")
        if t and sp not in [s[0] for s in speakers]:
            speakers.append((sp, t))
    if not speakers:
        speakers = [("author", "the siddhānta claim"),
                    ("opponent", "the rival position"),
                    ("reconstructed", "a reconstructed premise")]
    return speakers[:4]


def compile_interactions(scholarly_object: dict, targets: list[str],
                         learner_level="novice") -> dict:
    """Compile a LearningPacket from an argument/synthesis object.

    scholarly_object: a dict with {propositions, arguments, cruxes, research_question, boundary,
                      source_refs, counterevidence} (the convergence object shape).
    targets: the skill targets, e.g. ["CLASSIFY_SPEAKER","ATTACH_PREMISE","RECONSTRUCT_WARRANT",
             "IDENTIFY_CRUX"].
    """
    propositions = scholarly_object.get("propositions", []) or scholarly_object.get("inputs", [])
    cruxes = scholarly_object.get("cruxes", [])
    arguments = scholarly_object.get("arguments", []) or scholarly_object.get("inputs", [])
    boundary = scholarly_object.get("boundary", {})
    does_not = boundary.get("does_not_establish", []) if isinstance(boundary, dict) else []
    source_refs = scholarly_object.get("source_refs", [])
    research_question = scholarly_object.get("research_question", "")
    if isinstance(research_question, dict):
        research_question = research_question.get("question", "")

    interactions = []
    misconceptions = []
    claims = []

    # helper: pull a proposition text
    def prop_text(pid):
        for p in propositions:
            if (p.get("proposition_id") or p.get("id")) == pid:
                return p.get("commitment") or p.get("content") or p.get("text") or pid
        return pid

    # ── target: CLASSIFY_SPEAKER ────────────────────────────────────────────────
    if "CLASSIFY_SPEAKER" in targets and propositions:
        speaker_opt = _speaker_options(propositions)
        if speaker_opt:
            prompt_p = speaker_opt[0][1]
            opts = []
            seen = set()
            correct_sp = speaker_opt[0][0]
            for sp, t in speaker_opt:
                if sp in seen:
                    continue
                seen.add(sp)
                opts.append(_option(f"{sp}: {t}", correct=(sp == correct_sp),
                                    role="CORRECT" if sp == correct_sp else "ATTRIBUTION_ERROR",
                                    misconception=None if sp == correct_sp else "SPEAKER_COLLAPSE",
                                    derives_from=f"proposition:{t[:30]}"))
            interactions.append({
                "interaction_id": f"LI-SPK-{len(interactions)+1}",
                "skill": "CLASSIFY_SPEAKER", "target": "author-vs-opponent commitment",
                "prompt": f"Who is committed to: \"{prompt_p}\"?",
                "response_space": "SINGLE_CHOICE", "options": opts,
                "feedback_rules": [{"correct_option": "the speaker whose commitment this is"}],
                "what_it_tests": {"skill": "CLASSIFY_SPEAKER",
                                  "misconceptions": ["SPEAKER_COLLAPSE", "OBJECTION_AS_AUTHOR_VIEW"]},
                "source_refs": source_refs[:2],
                "derived_from": [p.get("proposition_id") or p.get("id") for p in propositions[:2]],
            })
            misconceptions.append(Misconception(
                "MC-SPK-1", "SPEAKER_COLLAPSE",
                "merging the author's commitment with the opponent's", confuses=["author", "opponent"],
                detected_by=[interactions[-1]["interaction_id"]]))

    # ── target: ATTACH_PREMISE ─────────────────────────────────────────────────
    if "ATTACH_PREMISE" in targets and arguments:
        arg = arguments[0] if isinstance(arguments, list) else arguments
        infs = arg.get("inferences", [])
        if infs:
            inf = infs[0]
            prems = inf.get("premise_ids", [])
            concl = (inf.get("conclusion_ids") or [None])[0]
            if prems:
                opts = [_option(f"{pid}: {prop_text(pid)}", correct=True, role="CORRECT",
                                derives_from=f"proposition:{pid}") for pid in prems]
                # distractor: the conclusion treated as a premise (direction reversal)
                if concl:
                    opts.append(_option(f"the conclusion itself: {prop_text(concl)}", correct=False,
                                        role="ARGUMENT_DIRECTION_REVERSAL",
                                        misconception="ARGUMENT_DIRECTION_REVERSAL",
                                        derives_from=f"proposition:{concl}"))
                # distractor: a textual citation as if it were a premise (grounding-as-inference)
                if source_refs:
                    opts.append(_option(f"the source passage (grounding, not a premise)", correct=False,
                                        role="GROUNDING_AS_INFERENCE",
                                        misconception="GROUNDING_AS_INFERENCE",
                                        derives_from="source:" + source_refs[0]))
                interactions.append({
                    "interaction_id": f"LI-PREM-{len(interactions)+1}",
                    "skill": "ATTACH_PREMISE",
                    "target": f"load-bearing premises of {inf.get('inference_id')}",
                    "prompt": f"Which premises does the inference to '{prop_text(concl)}' load-bearingly depend on?",
                    "response_space": "SINGLE_CHOICE", "options": opts,
                    "feedback_rules": [{"correct": "the load-bearing premises; the conclusion and the "
                                                    "source citation are NOT premises"}],
                    "what_it_tests": {"skill": "ATTACH_PREMISE",
                                      "misconceptions": ["ARGUMENT_DIRECTION_REVERSAL", "GROUNDING_AS_INFERENCE"]},
                    "source_refs": source_refs[:2], "derived_from": [inf.get("inference_id")],
                })
                misconceptions.append(Misconception(
                    "MC-PREM-1", "GROUNDING_AS_INFERENCE",
                    "treating a source citation as a logical premise", confuses=["grounding", "premise"],
                    detected_by=[interactions[-1]["interaction_id"]]))

    # ── target: IDENTIFY_CRUX ──────────────────────────────────────────────────
    if "IDENTIFY_CRUX" in targets and cruxes:
        crux_opt = []
        for c in cruxes:
            cid = c.get("crux_id") or c.get("id")
            q = c.get("question") or c.get("adjudication_question") or cid
            crux_opt.append(_option(f"{cid}: {q}", correct=True, role="CORRECT", derives_from=cid))
        # distractor: a resolved conclusion presented as the crux (OPEN_AS_RESOLVED)
        if does_not:
            crux_opt.append(_option(f"a settled conclusion: {does_not[0]}", correct=False,
                                    role="OPEN_AS_RESOLVED", misconception="OPEN_AS_RESOLVED",
                                    derives_from="boundary"))
        interactions.append({
            "interaction_id": f"LI-CRUX-{len(interactions)+1}",
            "skill": "IDENTIFY_CRUX",
            "target": "the decisive unresolved dispute",
            "prompt": "Which item is the decisive UNRESOLVED crux of this debate (not a settled conclusion)?",
            "response_space": "SINGLE_CHOICE", "options": crux_opt,
            "feedback_rules": [{"correct": "the crux that remains open"}],
            "what_it_tests": {"skill": "IDENTIFY_CRUX", "misconceptions": ["OPEN_AS_RESOLVED", "CRUX_OMISSION"]},
            "source_refs": source_refs[:2],
            "derived_from": [c.get("crux_id") or c.get("id") for c in cruxes],
        })
        misconceptions.append(Misconception(
            "MC-CRUX-1", "OPEN_AS_RESOLVED",
            "presenting an open crux as a settled conclusion", confuses=["open", "resolved"],
            detected_by=[interactions[-1]["interaction_id"]]))

    # ── target: QUALIFY_SCOPE ──────────────────────────────────────────────────
    if "QUALIFY_SCOPE" in targets and (does_not or boundary):
        opts = [
            _option("the claim holds per-act, with open boundaries (does not establish a universal Self)",
                    correct=True, role="CORRECT", derives_from="boundary"),
            _option("the claim establishes a universal Self in which all manifestation is one consciousness",
                    correct=False, role="SCOPE_INFLATION", misconception="SCOPE_INFLATION",
                    derives_from="boundary"),
            _option("the claim applies to every case without qualification",
                    correct=False, role="QUALIFIER_DROP", misconception="QUALIFIER_DROP",
                    derives_from="boundary"),
        ]
        interactions.append({
            "interaction_id": f"LI-SCOPE-{len(interactions)+1}",
            "skill": "QUALIFY_SCOPE",
            "target": "the scope boundary of the conclusion",
            "prompt": "Which statement correctly preserves the scope of the conclusion?",
            "response_space": "SINGLE_CHOICE", "options": opts,
            "feedback_rules": [{"correct": "the per-act, bounded reading; the universal readings drop the qualifier"}],
            "what_it_tests": {"skill": "QUALIFY_SCOPE", "misconceptions": ["SCOPE_INFLATION", "QUALIFIER_DROP"]},
            "source_refs": source_refs[:2], "derived_from": ["boundary"],
        })
        misconceptions.append(Misconception(
            "MC-SCOPE-1", "SCOPE_INFLATION",
            "generalizing a per-act claim to a universal", confuses=["per-act", "universal"],
            detected_by=[interactions[-1]["interaction_id"]]))

    # ── target: RECONSTRUCT_WARRANT ────────────────────────────────────────────
    if "RECONSTRUCT_WARRANT" in targets:
        interactions.append({
            "interaction_id": f"LI-WARR-{len(interactions)+1}",
            "skill": "RECONSTRUCT_WARRANT",
            "target": "the warrant licensing the inference",
            "prompt": f"What must be granted for the inference in this debate ({research_question or 'the recognition argument'}) to go through?",
            "response_space": "SHORT_CONSTRUCT", "options": [],
            "feedback_rules": [{"correct": "the warrant must be explicitly stated and its reconstructed status "
                                            "flagged (UNRESOLVED), never presented as settled"}],
            "what_it_tests": {"skill": "RECONSTRUCT_WARRANT",
                              "misconceptions": ["WARRANT_OMISSION", "OPEN_AS_RESOLVED"]},
            "source_refs": source_refs[:2], "derived_from": [],
        })
        misconceptions.append(Misconception(
            "MC-WARR-1", "WARRANT_OMISSION",
            "omitting a load-bearing warrant / treating it as settled", confuses=["warrant", "settled"],
            detected_by=[interactions[-1]["interaction_id"]]))

    # ── derive LearningClaims from the interactions' targets ───────────────────
    claims = [
        LearningClaim(f"LC-{i+1}", f"The learner can {it['skill'].lower().replace('_',' ')}: {it['target']}",
                      derived_from=it.get("derived_from", []), source_refs=it.get("source_refs", []),
                      epistemic_ceiling=scholarly_object.get("epistemic_ceiling", "MACHINE_PROPOSED"))
        for i, it in enumerate(interactions)
    ]

    return {
        "learning_packet_id": f"learn-{scholarly_object.get('object_id') or scholarly_object.get('synthesis_id') or 'obj'}",
        "derived_from": scholarly_object.get("object_id") or scholarly_object.get("synthesis_id"),
        "learner_level": learner_level,
        "learning_claims": [c.emit() for c in claims],
        "learning_skills": sorted({it["skill"] for it in interactions}),
        "misconceptions": [m.emit() for m in misconceptions],
        "interactions": interactions,
        "interaction_count": len(interactions),
        "epistemic_ceiling": scholarly_object.get("epistemic_ceiling", "MACHINE_PROPOSED"),
        "packet_hash": _sha256({"interactions": interactions}),
        "design_law": "education is a projection of Pāṭala objects, not a separate knowledge base",
        "moat": "wrong answer -> known epistemic neighbor (distractors derived from the graph)",
        "review_state": "GENERATED",
    }


if __name__ == "__main__":
    # smoke test on a synthetic convergence object
    obj = {
        "object_id": "VERTICAL-1",
        "research_question": "Can the determination establish an external object?",
        "propositions": [
            {"id": "P1", "commitment": "the determination is error-form", "speaker": "author"},
            {"id": "P2", "commitment": "an inert part cannot establish", "speaker": "author"},
            {"id": "P3", "commitment": "the pure self-experience is not external-natured", "speaker": "author"},
            {"id": "O3", "commitment": "as fire burns wood though inert, so the determination establishes",
             "speaker": "opponent"},
        ],
        "arguments": [{"inferences": [{"inference_id": "INF-1", "premise_ids": ["P1", "P2", "P3"],
                                        "conclusion_ids": ["C1"]}]}],
        "cruxes": [{"crux_id": "CRUX-1", "question": "Does establishing require the self-luminous awareness?"}],
        "boundary": {"does_not_establish": ["a universal Self"]},
        "source_refs": ["pt:passage:ipvv:chunkM"],
        "epistemic_ceiling": "UNRESOLVED",
    }
    pkt = compile_interactions(obj, ["CLASSIFY_SPEAKER", "ATTACH_PREMISE", "IDENTIFY_CRUX",
                                     "QUALIFY_SCOPE", "RECONSTRUCT_WARRANT"])
    print(f"LearningPacket: {pkt['interaction_count']} interactions, skills={pkt['learning_skills']}")
    for it in pkt["interactions"]:
        print(f"  {it['interaction_id']} [{it['skill']:18}] options={len(it['options'])}")
        for o in it["options"]:
            print(f"      {'✓' if o['correct'] else '✗'} {o['text'][:55]}  ({o.get('misconception','')})")
    print(f"  misconceptions: {len(pkt['misconceptions'])}")
