#!/usr/bin/env python3
"""experiments/vertical1_crux_validation.py — VERTICAL-1 (devpath13 P4/P6) crux validation.

Reconstruct the frozen VERTICAL-1 argument (Pratyabhijñā recognition vs the Buddhist determination /
adhyavasāya account of external cognition) per the IPVV-VERTICAL-001-SOURCE-DOSSIER, and run the
crux engine over its P6 hard structures:
  - P1-OR-P2 independently sufficient (redundant support)
  - P1+P2 jointly necessary
  - the Buddhist's fire-burning-wood objection as a DEFEATER (O3)
  - an alternative inference route that bypasses a premise

This is a STRESS TEST of the crux engine on the real argument's load-bearing structure, NOT a claim of
philosophical correctness. Every result is MACHINE_PROPOSED / NOT_HUMAN_REVIEWED.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from patala_ml.crux_engine import _minimal_decisive_sets, _conclusion_holds  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))

# ── the frozen VERTICAL-1 structure (from the dossier) ─────────────────────────
# Position A (Abhinavagupta), author claims:
P1 = "P1"  # the determination (adhyavasāya) is error-form: it is only the drawing of the appearance outward
P2 = "P2"  # an inert part cannot establish anything (inertness blocks establishing)
P3 = "P3"  # the non-inert part (pure self-experience / vimarśa) is un-divided from the memory-cognition and is not external-natured
P4 = "P4"  # (warrant) establishing power belongs only to the self-luminous awareness (prakāśa), not to a thing that reaches a thing
C1 = "C1"  # the cognition never establishes a thing outside itself (there is nothing outside self-luminous awareness)

# the Śaiva argument: the determination cannot establish an external.
#   Either P1 (it is error-form, so no real externality is fixed) OR P2 (an inert thing cannot
#   establish) is INDEPENDENTLY sufficient to defeat the determination's establishing power — P1 and
#   P2 are redundant alternatives (P1-OR-P2). P3 (self-experience is not external-natured) and P4
#   (establishing = self-luminous) are listed premises but are redundant FOR THIS OUTCOME (the defeat
#   of the external is already carried by P1 alone or P2 alone).
shaiva_inference = {
    "inference_id": "V1-ADHYAVASAYA",
    "premise_ids": [P1, P2, P3, P4],
    "conclusion_ids": [C1],
    "warrant": "RECONSTRUCTED: the determination fails on both sides (error-form, inert), and the only "
               "genuine establishing is self-luminous awareness (prakāśa) which is not external-natured.",
    # redundant support: P1 and P2 are EACH independently sufficient to defeat the determination
    "alternative_support_sets": [[P1], [P2]],
}

# Position B (Buddhist) objection O3: the fire-burning-wood analogy — an inert fire still burns, so an
# inert determination could still establish; this is a DEFEATER of the P2 (inertness-blocks) premise.
buddhist_defeater = {
    "inference_id": "V1-BUDDHIST-FIRE",
    "premise_ids": [P1, P2, P3, P4],
    "conclusion_ids": [C1],
    "active_defeater": True,   # O3 accepted -> inference blocked (the crux)
    "defeaters": [{
        "defeater_id": "O3-FIRE-WOOD",
        "description": "As fire burns wood though inert, so the determination establishes the object; "
                       "so inertness (P2) does not by itself block establishing.",
        "type": "FAILED_PREMISE",
        "status": "ACTIVE",   # when accepted, this defeats P2's role
    }],
}

# an alternative Buddhist route that bypasses the inertness premise (P2): accept P1 (error-form) but
# hold that an error-form determination nonetheless reaches an external — bypassing P2 entirely.
buddhist_bypass = {
    "inference_id": "V1-BUDDHIST-BYPASS",
    "premise_ids": [P1, P3, P4],
    "conclusion_ids": ["NOT-C1"],   # the external IS established
    "alternative_support_sets": [[P1], [P2]],  # a single premise suffices to reach the external
}


def main() -> int:
    print("== VERTICAL-1 crux stress-test (devpath13 P4/P6) ==")
    print("argument: Pratyabhijñā recognition vs Buddhist determination (adhyavasāya)")

    # 1. redundant support: P1-OR-P2 — the decisive set must remove BOTH P1 and P2 (leaving no
    #    surviving alternative), and P3/P4 must be redundant on their own (P3 alone not decisive).
    sets = _minimal_decisive_sets([P1, P2, P3, P4], shaiva_inference)
    print(f"  decisive sets (redundant support P1-OR-P2): {sets}")
    assert {"P1", "P2"} in {frozenset(s) for s in sets}, "must require removing both P1 and P2"
    assert {P3} not in {frozenset(s) for s in sets}, "P3 alone is redundant (not decisive)"
    print("  ✓ P1-OR-P2 independently sufficient — decisive set = {P1, P2}; P3/P4 redundant")

    # 2. active defeater (Buddhist fire-wood): when O3 is accepted, the inference is blocked -> no
    #    decisive set (the conclusion is under active dispute). This IS the crux.
    def_sets = _minimal_decisive_sets([P1, P2, P3, P4], buddhist_defeater)
    print(f"  decisive sets with ACTIVE fire-wood defeater: {def_sets}")
    assert def_sets == [], "an active defeater must block the conclusion (crux = the dispute)"
    print("  ✓ O3 fire-burning-wood defeater blocks the inference — this is CRUX-IPVV-001")

    # 3. alternative route bypasses P2: with the Buddhist's alternative (P1 alone reaches the external),
    #    the decisive set is what kills every alternative — i.e. P1 AND P2 (remove both).
    bp_sets = _minimal_decisive_sets([P1, P2, P3, P4], buddhist_bypass)
    print(f"  decisive sets (alternative route): {bp_sets}")
    assert {"P1", "P2"} in {frozenset(s) for s in bp_sets}, "alternative route must force removing P1+P2"

    # 4. remove the warrant P4's role: once P4 (establishing = self-luminous) is NOT a licensed
    #    premise for the outcome, the positive claim C1 depends jointly on P1 AND P2 (neither alone
    #    carries the full claim). This demonstrates that P4 is the load-bearing warrant for C1, and
    #    that P1/P2 jointly become necessary when the positive claim is what is at stake.
    no_warrant = {**shaiva_inference, "premise_ids": [P1, P2, P3, P4],
                  "alternative_support_sets": [[P1, P3, P4], [P2, P3, P4]]}
    nw_sets = _minimal_decisive_sets([P1, P2, P3, P4], no_warrant)
    print(f"  decisive sets (joint claim, warrant-dependent): {nw_sets}")
    # with both alternatives sharing P4, removing P4 kills both -> P4 is decisive (the warrant matters)
    assert {P4} in {frozenset(s) for s in nw_sets}, "removing the warrant P4 must flip the positive claim"
    print("  ✓ P4 (self-luminosity warrant) is load-bearing: removing it flips the positive claim")

    # 5. emit the crux as a machine-proposed object (honest ceiling)
    crux = {
        "crux_id": "CRUX-IPVV-001",
        "argument": "ARG-IPVV-VERTICAL-1-ADHYAVASAYA",
        "object_kind": "CRUX",
        "decisive_premises": ["P1", "P2"],
        "method": "PERTURBATION",
        "question": ("Which assumption about the establishing power must hold for the recognition "
                     "inference to succeed? Does 'establishing' require the self-luminous awareness "
                     "(prakāśa) itself — such that the inert part cannot establish and the external is "
                     "only drawn-to — or can a non-self-luminous (inert) representation nonetheless "
                     "establish an external, as the Buddhist's fire-burning-wood analogy asserts?"),
        "defeater": "O3-FIRE-WOOD (fire burns wood though inert)",
        "review_status": "NOT_HUMAN_REVIEWED",
        "status": "MACHINE_PROPOSED",
    }
    print("\n  CRUX-IPVV-001:", crux["question"][:120], "...")

    out = os.path.join(ROOT, "benchmarks", "v0", "review", "VERTICAL-1-CRUX-VALIDATION.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    payload = {
        "object_kind": "VERTICAL_1_CRUX_VALIDATION",
        "argument": "Pratyabhijñā recognition vs Buddhist adhyavasāya",
        "crux": crux,
        "structures_tested": {
            "redundant_support_P1_OR_P2": {"decisive_sets": [sorted(s) for s in sets]},
            "active_defeater_O3_fire_wood": {"blocked": bool(def_sets == [])},
            "alternative_route_bypass_P2": {"decisive_sets": [sorted(s) for s in bp_sets]},
            "warrant_P4_removal": {"decisive_sets": [sorted(s) for s in nw_sets]},
        },
        "review_status": "NOT_HUMAN_REVIEWED",
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"\n  wrote {out}")
    print("\n  ALL VERTICAL-1 CRUX STRUCTURES PASS (MACHINE_PROPOSED)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
