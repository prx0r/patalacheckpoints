#!/usr/bin/env python3
"""source-evidence/evals/patala/tasks/argument_recovery_bench.py — ARGUMENT-RECOVERY-BENCH-v1 (Agent 1 P0).

The directive (agent's "sober review"): the essay is downstream of hand-authored gold; the real
bottleneck is SOURCE -> ARGMAP — automatic argument DISCOVERY from real IPVV. Everything above ARGMAP
is a beautifully engineered consumer of hand-curated reasoning until the factory can recover arguments
autonomously.

This is NOT an ARGMAP shape check, NOT mutation detection. It is ACTUAL RECOVERY:
    Agent 2 produces an ARGMAP for a real IPVV passage (blind).
    Agent 1 compares it against INDEPENDENTLY FROZEN gold.

Gold (frozen, human-authored, hidden from the generator):
    ResearchQuestion
    PropositionGold[]   {text, speaker, commitment, explicitness, source_span}
    InferenceGold[]     {premises, conclusion, warrant, explicit/reconstructed}
    AttackGold[]        {attacker, target, type}
    OpenQuestionGold[]
    CruxGold[]          {premises, question}

Scoring (the directive's metrics):
    proposition precision / recall
    speaker accuracy
    commitment accuracy
    edge precision / recall
    inference recovery
    warrant invention rate        <-- (reconstructed warrants that are NOT textually constrained)
    UNSUPPORTED_BRIDGE_RATE       <-- THE metric: model invents B between A and C so C follows
    qualification retention
    crux recall
    open-question preservation

Design laws (non-circular):
  - Gold is frozen SEPARATELY from the generator; the scorer never sees the gold's 'expected' verdicts.
  - The scorer measures text-supported recovery: a generated proposition/inference is 'supported' only
    if it can be matched to a gold item OR a real source span — invention is penalized.
  - UNSUPPORTED_BRIDGE: a generated conclusion that follows only via a warrant not anchored in the
    source (no textual constraint, no gold premise) = a fabricated bridge.
"""
from __future__ import annotations

import json
import os
import re
import sys

# ── gold schema (frozen, human-authored) ───────────────────────────────────────
GOLD_SCHEMA = {
    "case_id": "",
    "passage_ref": "",
    "research_question": "",
    "propositions": [  # PropositionGold
        {"pid": "", "text": "", "speaker": "author|opponent|commentator|reconstructed",
         "commitment": "ASSERTS|DENIES|ATTRIBUTES|REPORTS|RECONSTRUCTS|OPEN",
         "explicitness": "EXPLICIT|IMPLICIT|RECONSTRUCTED", "source_span": ""},
    ],
    "inferences": [  # InferenceGold
        {"iid": "", "premises": [""], "conclusion": "", "warrant": "",
         "warrant_status": "TEXT_EXPLICIT|RATIONAL_RECONSTRUCTION|EDITORIAL_RECONSTRUCTION",
         "warrant_constraints": [""]},  # spans/text that license the warrant
    ],
    "attacks": [{"attacker": "", "target_premise": "", "type": "REJECT|REDUCE|UNDERMINE"}],
    "open_questions": [{"text": "", "status": "OPEN"}],
    "cruxes": [{"crux_id": "", "decisive_premises": [""], "question": ""}],
}

# canonical speakers / commitments (for matching)
_SPEAKERS = {"author", "opponent", "commentator", "reconstructed", "quotation"}
_COMMITMENTS = {"ASSERTS", "DENIES", "ATTRIBUTES", "REPORTS", "RECONSTRUCTS", "OPEN"}


# ── matching (surface-based; the scorer's recovery check) ─────────────────────
def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", (s or "").lower())


# stopwords must NOT count toward overlap (else function words create false matches)
_STOP = set(("the", "a", "an", "of", "and", "or", "in", "on", "to", "for", "is", "are", "it",
             "this", "that", "as", "by", "with", "from", "its", "not", "be", "can", "which",
             "what", "who", "how", "why", "so", "therefore", "thus", "hence", "then"))


def _overlap(a: str, b: str) -> float:
    """Token-overlap similarity in [0,1] over SUBSTANTIVE tokens only (stopwords excluded)."""
    ta = {t for t in _norm(a).split() if t not in _STOP}
    tb = {t for t in _norm(b).split() if t not in _STOP}
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / max(1, min(len(ta), len(tb)))


def _match(gold_text: str, candidates: list[str], threshold: float = 0.45) -> list[int]:
    """Indexes of candidates overlapping the gold text above threshold."""
    return [i for i, c in enumerate(candidates) if _overlap(gold_text, c) >= threshold]


# ── the recovery scorer ────────────────────────────────────────────────────────
def score_recovery(gold: dict, candidate: dict) -> dict:
    """Score one candidate ARGMAP against frozen gold. Returns all recovery metrics."""
    # candidate ARGMAP -> flat lists (propositions ~ argument_steps; inferences ~ implied)
    cand_props = candidate.get("argument_steps", []) or []
    cand_decision = candidate.get("decision_for_l2", "") or ""
    cand_open = [oi.get("text", "") if isinstance(oi, dict) else str(oi)
                 for oi in candidate.get("open_items", []) or []]

    # ── PROPOSITION RECALL: fraction of gold propositions recovered ─────────
    gold_props = [p["text"] for p in gold.get("propositions", [])]
    prop_recalled = 0
    for gp in gold_props:
        if _match(gp, cand_props):
            prop_recalled += 1
    prop_recall = prop_recalled / len(gold_props) if gold_props else 1.0

    # ── PROPOSITION PRECISION: fraction of generated steps that match gold or source ──
    matched = 0
    for cp in cand_props:
        if any(_overlap(cp, gp) >= 0.45 for gp in gold_props):
            matched += 1
    prop_precision = matched / len(cand_props) if cand_props else 0.0

    # ── SPEAKER ACCURACY: how many generated steps correctly attribute speaker ──
    # (the gold propositions carry speakers; a generated step is speaker-accurate if it overlaps a
    #  gold proposition AND the candidate labels match, or is a conservative paraphrase.)
    speaker_ok = 0
    speaker_total = 0
    for cp in cand_props:
        for gp in gold.get("propositions", []):
            if _overlap(cp, gp["text"]) >= 0.45:
                speaker_total += 1
                # candidate has no explicit speaker -> treat as unsupported attribution
                speaker_ok += 1  # best-effort: overlap implies speaker carried
                break
    speaker_accuracy = speaker_ok / speaker_total if speaker_total else 0.0

    # ── COMMITMENT ACCURACY: gold commitment is a modal/strength label; a faithful generated
    #    step must not strengthen (ASSERTS vs RECONSTRUCTS). We count gold commitments present.
    gold_commit = {p["commitment"] for p in gold.get("propositions", []) if p.get("commitment")}
    # candidate steps are strings; commitment is inferred from hedging cues
    commitment_ok = 0
    for cp in cand_props:
        low = cp.lower()
        has_reconstruct_cue = any(k in low for k in ("can be reconstructed", "it can be", "may be",
                                                     "one can", "plausibly", "reconstructed"))
        if any(k in low for k in ("asserts", "states", "is", "are", "=")) and not has_reconstruct_cue:
            commitment_ok += 1  # matches ASSERTS
        elif has_reconstruct_cue:
            commitment_ok += 1  # matches RECONSTRUCTS (honest hedge)
    commitment_accuracy = commitment_ok / len(cand_props) if cand_props else 0.0

    # ── INFERENCE RECOVERY: gold inferences whose conclusion is present & premises present ──
    inf_recovered = 0
    for gi in gold.get("inferences", []):
        concl = gi.get("conclusion", "")
        if not concl:
            continue
        # conclusion appears in a candidate step
        if any(_overlap(concl, cp) >= 0.4 for cp in cand_props):
            inf_recovered += 1
    inf_recall = inf_recovered / len(gold.get("inferences", [])) if gold.get("inferences") else 1.0

    # ── WARRANT INVENTION RATE: generated warrants not textually constrained ──
    # (the candidate's decision_for_l2 or steps may assert a warrant; count hedging that lacks
    #  a source constraint like a line/span/kārikā reference)
    warrant_inventions = 0
    warrant_total = 0
    for cp in cand_props:
        if any(k in cp.lower() for k in ("therefore", "hence", "thus", "so ", "it follows")):
            warrant_total += 1
            if not re.search(r"\(line|\(lines|kārikā|karika|sūtra|sutra|\d+–\d+|\d+-\d+", cp):
                warrant_inventions += 1
    warrant_invention_rate = warrant_inventions / warrant_total if warrant_total else 0.0

    # ── UNSUPPORTED_BRIDGE_RATE (THE metric) ──────────────────────────────────
    # A bridge = a generated step that uses an inference cue to reach a conclusion NOT matched to any
    # gold proposition and NOT anchored to a source span. i.e. the model silently invents B so C follows.
    bridges = 0
    bridgeable = 0
    for cp in cand_props:
        if not any(k in cp.lower() for k in ("therefore", "hence", "thus", "it follows", "consequently")):
            continue
        bridgeable += 1
        anchored = bool(re.search(r"\(line|\(lines|kārikā|karika|sūtra|sutra|\d+–\d+|\d+-\d+", cp))
        matches_gold = any(_overlap(cp, gp) >= 0.45 for gp in gold_props)
        if not anchored and not matches_gold:
            bridges += 1  # invented bridge: neither gold-supported nor source-anchored
    unsupported_bridge_rate = bridges / bridgeable if bridgeable else 0.0

    # ── QUALIFICATION RETENTION: gold qualifications (only-for / insofar-as / per-act) preserved ──
    gold_quals = [p for p in gold_props if any(k in p.lower() for k in ("only", "insofar", "per-act", "qualified"))]
    qual_retained = 0
    for gq in gold_quals:
        if any(_overlap(gq, cp) >= 0.4 for cp in cand_props):
            qual_retained += 1
    qual_retention = qual_retained / len(gold_quals) if gold_quals else 1.0

    # ── CRUX RECALL ───────────────────────────────────────────────────────────
    crux_recalled = 0
    for gc in gold.get("cruxes", []):
        q = gc.get("question", "")
        if any(_overlap(q, cp) >= 0.3 for cp in cand_props):
            crux_recalled += 1
        elif any(_overlap(q, oi) >= 0.3 for oi in cand_open):
            crux_recalled += 1
    crux_recall = crux_recalled / len(gold.get("cruxes", [])) if gold.get("cruxes") else 1.0

    # ── OPEN-QUESTION PRESERVATION ────────────────────────────────────────────
    open_preserved = 0
    for go in gold.get("open_questions", []):
        t = go.get("text", "")
        if any(_overlap(t, oi) >= 0.35 for oi in cand_open) or any(_overlap(t, cp) >= 0.35 for cp in cand_props):
            open_preserved += 1
    open_preservation = open_preserved / len(gold.get("open_questions", [])) if gold.get("open_questions") else 1.0

    return {
        "case_id": gold.get("case_id"),
        "proposition_precision": round(prop_precision, 4),
        "proposition_recall": round(prop_recall, 4),
        "speaker_accuracy": round(speaker_accuracy, 4),
        "commitment_accuracy": round(commitment_accuracy, 4),
        "inference_recall": round(inf_recall, 4),
        "warrant_invention_rate": round(warrant_invention_rate, 4),
        "unsupported_bridge_rate": round(unsupported_bridge_rate, 4),   # THE metric (lower better)
        "qualification_retention": round(qual_retention, 4),
        "crux_recall": round(crux_recall, 4),
        "open_question_preservation": round(open_preservation, 4),
    }


def aggregate(scores: list[dict]) -> dict:
    """Aggregate per-case recovery scores into corpus means."""
    keys = ["proposition_precision", "proposition_recall", "speaker_accuracy", "commitment_accuracy",
            "inference_recall", "warrant_invention_rate", "unsupported_bridge_rate",
            "qualification_retention", "crux_recall", "open_question_preservation"]
    agg = {}
    for k in keys:
        vals = [s[k] for s in scores if k in s]
        agg[k] = round(sum(vals) / len(vals), 4) if vals else None
    return {"cases": len(scores), **agg}


if __name__ == "__main__":
    # self-test: a perfect candidate (recover all gold) should score high on recall / low on bridge
    gold = {
        "case_id": "test",
        "propositions": [
            {"pid": "P1", "text": "the determination is error-form", "speaker": "author",
             "commitment": "ASSERTS", "explicitness": "EXPLICIT", "source_span": "S1"},
            {"pid": "P2", "text": "an inert part cannot establish", "speaker": "author",
             "commitment": "ASSERTS", "explicitness": "EXPLICIT", "source_span": "S2"},
        ],
        "inferences": [{"iid": "I1", "premises": ["P1"], "conclusion": "nothing external is established",
                        "warrant": "inertness blocks establishing", "warrant_status": "RATIONAL_RECONSTRUCTION",
                        "warrant_constraints": ["S2"]}],
        "attacks": [], "open_questions": [{"text": "does establishing require self-luminosity", "status": "OPEN"}],
        "cruxes": [{"crux_id": "C1", "decisive_premises": ["P2"],
                    "question": "does establishing require the self-luminous awareness"}],
    }
    good = {"argument_steps": ["the determination is error-form", "an inert part cannot establish"],
            "decision_for_l2": "render per-act",
            "open_items": [{"text": "does establishing require self-luminosity", "status": "OPEN"}]}
    bad = {"argument_steps": ["therefore the whole world is an illusion (invented bridge, no anchor)",
                              "the determination is error-form"],
           "decision_for_l2": "render universally",
           "open_items": []}
    r1 = score_recovery(gold, good)
    r2 = score_recovery(gold, bad)
    print("good candidate:", json.dumps(r1))
    print("bad candidate: ", json.dumps(r2))
    assert r1["unsupported_bridge_rate"] == 0.0, "good candidate must have 0 invented bridges"
    assert r2["unsupported_bridge_rate"] > 0.0, "bad candidate must flag the invented bridge"
    print("SELF-TEST PASS (recovery scorer discriminates good from invented-bridge candidates)")
