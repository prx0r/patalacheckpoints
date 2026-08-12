#!/usr/bin/env python3
"""make_gate_gold.py — create the Nyāya gate gold fixtures (the critical missing prerequisite).

The gate is NYAYA_GATE_CANDIDATE_v1: deterministic but UNTESTED. Before promoting it to
verify-claim-semantic, it needs hand-adjudicated gold for each of the 5 hetvābhāsas:
  asiddha (unproven) · viruddha (contradictory) · savyabhicara (inconsistent) ·
  satpratipaksa (counter-balanced) · badhita (overtidden)

Each fallacy gets: a positive (the defect IS present), a negative (the defect is NOT), and a
borderline (ambiguous — a good gate should abstain or flag for review, not force).

These are PHILOLOGICAL/ARGUMENT examples (Pāṭala's domain), NOT the truth-engine's
metaphysics content — because the gate's hardcoded rules (meditation/brain-damage) are
ontology-bound and should NOT be ported.

Output: benchmarks/v0/evidence/nyaya-gate-gold.jsonl  (SINGLE_REVIEWED)
"""
from __future__ import annotations

import json
import os

OUT = "/root/projects/patala/benchmarks/v0/evidence/nyaya-gate-gold.jsonl"

# Each fixture: the claim as the gate would receive it, + the adjudicated expected outcome.
# expected: the fallacy that SHOULD be detected (or "CLEAN" / "ABSTAIN").
GOLD = [
    # ── ASIDDHA (the hetu/reason itself is unestablished) ──
    {
        "fixture_id": "GATE-ASIDDHA-001",
        "fallacy": "asiddha",
        "kind": "positive",
        "claim_text": "The subtle body exists, therefore reincarnation is real.",
        "pramana": "anumana",
        "tradition": "trika",
        "expected": "asiddha",
        "expected_reason": "the hetu (subtle body) is not independently established",
        "review_state": "SINGLE_REVIEWED",
    },
    {
        "fixture_id": "GATE-ASIDDHA-002",
        "fallacy": "asiddha",
        "kind": "negative",
        "claim_text": "IPVV V2-O explicitly states the support of the powers is the order-less knower.",
        "pramana": "sabda",
        "tradition": "trika",
        "source_id": "pt:passage:ipvv:chunkV2-O-saptamo-vimarsa.md",
        "expected": "CLEAN",
        "expected_reason": "a faithful textual report, hetu established by the passage",
        "review_state": "SINGLE_REVIEWED",
    },
    {
        "fixture_id": "GATE-ASIDDHA-003",
        "fallacy": "asiddha",
        "kind": "borderline",
        "claim_text": "The tantric initiation transmits a subtle power that cannot be measured.",
        "pramana": "sabda",
        "tradition": "trika",
        "expected": "ABSTAIN",
        "expected_reason": "the claim is unfalsifiable — a good gate should not force a verdict",
        "review_state": "SINGLE_REVIEWED",
    },

    # ── VIRUDDHA (evidence supports the opposite of what's claimed) ──
    {
        "fixture_id": "GATE-VIRUDDHA-001",
        "fallacy": "viruddha",
        "kind": "positive",
        "claim_text": "Memory proves the self is constructed, because memory requires multiple past moments.",
        "pramana": "anumana",
        "tradition": "trika",
        "expected": "viruddha",
        "expected_reason": "IPVV uses memory to argue the OPPOSITE — a persistent non-constructed self (V2-P)",
        "review_state": "SINGLE_REVIEWED",
    },
    {
        "fixture_id": "GATE-VIRUDDHA-002",
        "fallacy": "viruddha",
        "kind": "negative",
        "claim_text": "Memory presupposes a persistent recognizer who owns the past cognition.",
        "pramana": "anumana",
        "tradition": "trika",
        "expected": "CLEAN",
        "expected_reason": "matches the IPVV's actual memory-argument direction",
        "review_state": "SINGLE_REVIEWED",
    },

    # ── SAVYABHICARA (the reason doesn't always imply the conclusion) ──
    {
        "fixture_id": "GATE-SAVYABHICARA-001",
        "fallacy": "savyabhicara",
        "kind": "positive",
        "claim_text": "Contemplative practice always produces nondual awareness, therefore meditation proves the universal Self.",
        "pramana": "anumana",
        "tradition": "contemplative",
        "expected": "savyabhicara",
        "expected_reason": "meditation does not invariably produce nondual awareness (counterexamples exist)",
        "review_state": "SINGLE_REVIEWED",
    },
    {
        "fixture_id": "GATE-SAVYABHICARA-002",
        "fallacy": "savyabhicara",
        "kind": "negative",
        "claim_text": "In the IPVV, manifestation (prakāśa) is invariably accompanied by reflexive awareness (vimarśa).",
        "pramana": "anumana",
        "tradition": "trika",
        "vyapti_confidence": 0.9,
        "expected": "CLEAN",
        "expected_reason": "high vyāpti confidence, no known violations",
        "review_state": "SINGLE_REVIEWED",
    },
    {
        "fixture_id": "GATE-SAVYABHICARA-003",
        "fallacy": "savyabhicara",
        "kind": "borderline",
        "claim_text": "Ritual practice generally deepens understanding, so this ritual leads to liberation.",
        "pramana": "anumana",
        "tradition": "trika",
        "vyapti_confidence": 0.55,
        "expected": "savyabhicara",
        "expected_reason": "low-moderate vyāpti confidence — 'generally' is not invariable",
        "review_state": "SINGLE_REVIEWED",
    },

    # ── SATPRATIPAKSA (an equally strong counter-inference exists) ──
    {
        "fixture_id": "GATE-SATPRATIPAKSA-001",
        "fallacy": "satpratipaksa",
        "kind": "positive",
        "claim_text": "The non-constructed 'I' proves a single universal Self.",
        "pramana": "anumana",
        "tradition": "trika",
        "peer_claims": [
            {"claim_id": "peer-1", "claim_text": "The non-constructed 'I' is per-field only, not universal.",
             "log_bayes_factor": -0.8, "targets": [{"target_id": "F1"}]}
        ],
        "expected": "satpratipaksa",
        "expected_reason": "an equally strong counter-inference exists on the same target",
        "review_state": "SINGLE_REVIEWED",
    },
    {
        "fixture_id": "GATE-SATPRATIPAKSA-002",
        "fallacy": "satpratipaksa",
        "kind": "negative",
        "claim_text": "The order-less support cannot itself be a member of the ordered sequence.",
        "pramana": "anumana",
        "tradition": "trika",
        "peer_claims": [],  # no opposing inference
        "expected": "CLEAN",
        "expected_reason": "no equally strong counter-inference provided",
        "review_state": "SINGLE_REVIEWED",
    },

    # ── BADHITA (a stronger pramāṇa contradicts) ──
    {
        "fixture_id": "GATE-BADHITA-001",
        "fallacy": "badhita",
        "kind": "positive",
        "claim_text": "The 'I'-awareness has no neural correlate and the brain is irrelevant to it.",
        "pramana": "anumana",
        "tradition": "idealism",
        "expected": "badhita",
        "expected_reason": "the denial of neural correlates/brain relevance is contradicted by stronger empirical evidence",
        "review_state": "SINGLE_REVIEWED",
    },
    {
        "fixture_id": "GATE-BADHITA-002",
        "fallacy": "badhita",
        "kind": "negative",
        "claim_text": "The felt self-grasp is not explained merely by the presence of a body.",
        "pramana": "anumana",
        "tradition": "trika",
        "expected": "CLEAN",
        "expected_reason": "no stronger evidence directly contradicts this",
        "review_state": "SINGLE_REVIEWED",
    },
]


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        for g in GOLD:
            f.write(json.dumps(g, ensure_ascii=False) + "\n")
    pos = sum(1 for g in GOLD if g["kind"] == "positive")
    neg = sum(1 for g in GOLD if g["kind"] == "negative")
    bord = sum(1 for g in GOLD if g["kind"] == "borderline")
    print(f"wrote {len(GOLD)} gate-gold fixtures → {OUT}")
    print(f"  positive={pos} negative={neg} borderline={bord} (all SINGLE_REVIEWED)")
    print("  NOTE: these are the critical prerequisite the CLAIMS flagged — the gate was untested.")


if __name__ == "__main__":
    main()
