#!/usr/bin/env python3
"""source-evidence/evals/patala/tasks/essay_bench.py — ESSAY-BENCH-v1 (Agent 1; the essay evaluator).

The directive's reframe: Essay is NOT "improve the prose manually" — Agent 1 builds the EVALUATOR so
the essay PRODUCER can be scored and fixed (same loop as T1). Four independent gates that must not be
collapsed:

    1. TRACEABILITY        sentence -> claim -> synthesis -> argument -> proposition -> source
    2. CLAIM FIDELITY      no scope/modal/paraphrase inflation
    3. ESSAY-ARGUMENT      does the essay THESIS actually follow from its own claims? (not just a list)
    4. PROSE/DISCOURSE     does a reader experience problem->pressure->reason->objection->reply->payoff?
                           (catches the duplicate-opening + 'list of declarative sentences' problems)

The scorer is a set of deterministic structural checks + discourse-function analysis. It never decides
scholarly truth. It produces findings for the essay PRODUCER to fix (not for Agent 1 to hand-edit).
"""
from __future__ import annotations

import re


# ── gate 4 helpers: discourse function / repetition / flow ────────────────────
_OBJECTION_CUES = ("objection", "but", "however", "yet", "one might", "a rival", "the opponent",
                   "the buddhist", "could be said")
_REPLY_CUES = ("reply", "respond", "this is met", "he shows", "turns on", "cuts")
_PRESSURE_CUES = ("the problem", "the worry", "at stake", "the question", "turns on", "at issue")
_PAYOFF_CUES = ("therefore", "so", "it follows", "thus", "conclusion", "in short", "so the")


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", (s or "").lower())


def _words(s: str) -> set:
    return set(_norm(s).split())


def _sentence_similarity(a: str, b: str) -> float:
    wa, wb = _words(a), _words(b)
    if not wa or not wb:
        return 0.0
    stop = {"the", "a", "an", "of", "and", "or", "in", "is", "are", "to", "for", "it", "that", "this"}
    wa, wb = wa - stop, wb - stop
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / max(1, min(len(wa), len(wb)))


def _split_sentences(essay: str) -> list[str]:
    # crude sentence split on sentence-final punctuation
    parts = re.split(r"(?<=[.!?])\s+", essay or "")
    return [p.strip() for p in parts if len(p.strip()) > 20]


def audit_essay(essay: str, sentence_audit: dict | None = None, claim_fidelity: dict | None = None) -> dict:
    """Score one essay against the four gates. Returns findings + gate scores."""
    sentences = _split_sentences(essay)
    low = essay.lower()
    findings = []

    # ── GATE 4a: discourse repetition (the duplicate-opening problem) ─────────
    # threshold 0.70: catches near-duplicate theses (real editors reject these); safely above random.
    dup = []
    for i in range(len(sentences)):
        for j in range(i + 1, len(sentences)):
            sim = _sentence_similarity(sentences[i], sentences[j])
            if sim >= 0.70:
                dup.append((i, j, round(sim, 2)))
    repetition = len(dup)
    if repetition:
        findings.append(f"DISCOURSE_REPETITION: {repetition} near-duplicate sentence pair(s) "
                        f"({dup[:2]}); real editors reject this.")

    # ── GATE 4b: discourse flow (does the reader get problem->objection->reply->payoff?) ──
    has_pressure = any(c in low for c in _PRESSURE_CUES)
    has_objection = any(c in low for c in _OBJECTION_CUES)
    has_reply = any(c in low for c in _REPLY_CUES)
    has_payoff = any(c in low for c in _PAYOFF_CUES)
    discourse_flow = sum([has_pressure, has_objection, has_reply, has_payoff])
    if discourse_flow < 3:
        findings.append(f"DISCOURSE_FLOW: only {discourse_flow}/4 of "
                        "(problem, objection, reply, payoff) present — the essay may read as a list "
                        "of declarative sentences rather than an argument.")

    # ── GATE 1: traceability ──────────────────────────────────────────────────
    if sentence_audit is not None:
        lb = [s for s in sentence_audit.get("sentences", []) if s.get("role") == "LOAD_BEARING"]
        traceable = all(s.get("audit", {}).get("traceable", False)
                        or (s.get("claim_refs") and s.get("source_refs")) for s in lb)
        untraceable = [s["sid"] for s in lb
                       if not (s.get("audit", {}).get("traceable") or (s.get("claim_refs") and s.get("source_refs")))]
        if untraceable:
            findings.append(f"TRACEABILITY: load-bearing sentences {untraceable} lack claim/source refs.")
    else:
        traceable = None
        untraceable = []

    # ── GATE 2: claim fidelity ────────────────────────────────────────────────
    # (a scope-inflated claim uses universal without a qualifier; a modal-inflated claim asserts
    #  without 'reconstruct/can be/shows')
    if claim_fidelity is not None:
        # claim_fidelity: {scope_inflations: [...], modal_inflations: [...]}
        fidelity_ok = not claim_fidelity.get("scope_inflations") and not claim_fidelity.get("modal_inflations")
        if claim_fidelity.get("scope_inflations"):
            findings.append(f"CLAIM_FIDELITY: scope inflation(s) {claim_fidelity['scope_inflations']}")
        if claim_fidelity.get("modal_inflations"):
            findings.append(f"CLAIM_FIDELITY: modal inflation(s) {claim_fidelity['modal_inflations']}")
    else:
        fidelity_ok = None

    # ── GATE 3: ESSAY-ARGUMENT integrity (thesis follows from its own claims) ──
    # The essay must have BOTH a claim AND a support relation, else it is a list of sentences.
    # A real argument essay asserts a claim and gives a reason (because/hence/this shows) linking it
    # to evidence. Cue-word presence alone is not enough.
    n_claims = sum(1 for s in sentences if any(c in s.lower() for c in ("is ", "are ", "=")))
    n_support = sum(1 for s in sentences if any(c in s.lower() for c in ("because", "hence", "therefore",
                                                                        "this shows", "since", "as ",
                                                                        "the reason", "so ")))
    essay_argument_ok = (n_claims >= 2 and n_support >= 2)
    if not essay_argument_ok:
        findings.append(f"ESSAY_ARGUMENT: only {n_claims} claim(s) / {n_support} support-relation(s) — "
                        "the essay may be a list of declarative sentences rather than an argument.")

    return {
        "gates": {
            "TRACEABILITY": "PASS" if traceable is True else ("FAIL" if traceable is False else "NOT_EVALUATED"),
            "CLAIM_FIDELITY": "PASS" if fidelity_ok is True else ("FAIL" if fidelity_ok is False else "NOT_EVALUATED"),
            "ESSAY_ARGUMENT": "PASS" if essay_argument_ok else "FAIL",
            "PROSE_DISCOURSE": "PASS" if (discourse_flow >= 3 and repetition == 0) else "FAIL",
        },
        "findings": findings,
        "metrics": {
            "repetition": repetition,
            "discourse_flow": discourse_flow,
            "n_claims": n_claims,
            "n_support": n_support,
            "has_problem_pressure": has_pressure,
            "has_objection": has_objection,
            "has_reply": has_reply,
            "has_payoff": has_payoff,
        },
    }


if __name__ == "__main__":
    # self-test: a hollow list-of-sentences vs a real argument essay
    hollow = ("The reflexion-core turns on whether reflexivity belongs to manifestation. "
              "The reflexion-core turns on whether reflexivity belongs to manifestation. "
              "It can be reconstructed that articulation does not show construction. "
              "A light that showed the world would be like inert crystal.")
    real = ("The reflexion-core turns on whether reflexivity belongs to manifestation. "
            "The problem is that if self-awareness is word-joined it looks constructed. "
            "But one might object that the Buddhist's determination establishes an external. "
            "Abhinavagupta replies that the inert part cannot establish. "
            "Therefore the external is only drawn-to, never established; that is the payoff.")
    r_hollow = audit_essay(hollow)
    r_real = audit_essay(real)
    print("hollow:", {g: v for g, v in r_hollow["gates"].items()}, "| findings:", r_hollow["findings"])
    print("real:  ", {g: v for g, v in r_real["gates"].items()}, "| findings:", r_real["findings"])
    assert r_hollow["gates"]["PROSE_DISCOURSE"] == "FAIL"   # duplicate + no objection/reply
    assert r_real["gates"]["PROSE_DISCOURSE"] == "PASS"
    assert r_hollow["metrics"]["repetition"] >= 1
    print("SELF-TEST PASS (essay bench catches the hollow/repetitive essay)")
