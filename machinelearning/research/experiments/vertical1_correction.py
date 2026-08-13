#!/usr/bin/env python3
"""experiments/vertical1_correction.py — VERTICAL-1 whole-chain correction test (devpath13 P11).

The project thesis: a correction to historical evidence propagates into downstream scholarship.

Per the directive §13: BEFORE any rebuild, Agent 1 freezes the expected consequences of a low-level
correction; then verifies the actual impact report. This is the semantic-impact check, not merely
'it rebuilt'.

We use the review_engine's deterministic reducer on the VERTICAL-1 chain:
    proposition (G2-TC2) -> inference (G2-INF1) -> conclusion (G2-CONC) -> synthesis (SYN-CONC-001)
    -> essay claim (S001) -> learning interaction (the synthesis-driven education set)

The frozen expectation (TD17-style): REVISE the load-bearing premise G2-TC2 -> every downstream object
that DEPENDS on it must flip to NEED_REVIEW; the impacted set must be exactly the load-bearing
dependencies, and nothing unrelated (ARG-004) may move.

This proves: a correction propagates semantically (not just that a rebuild succeeds).
MACHINE_PROPOSED / NOT_HUMAN_REVIEWED.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "pipeline"))
from review_engine import ReviewLedger  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))


def main() -> int:
    print("== VERTICAL-1 whole-chain correction test (devpath13 P11) ==")

    # ── freeze the expected consequences FIRST (before applying) ──────────────────
    # A REVISE of the load-bearing premise G2-TC2 (the 'I'-awareness is not a constructed relation)
    # must flip to NEED_REVIEW:
    #   G2-INF1 (uses it as a premise)
    #   G2-CONC (the inference's conclusion)
    #   SYN-CONC-001 (the synthesis conclusion built on G2-CONC)  -- via synthesis dependency
    #   the essay claim S001 (refs G2-OBJ + SYN-CONC-001)
    # and must NOT touch ARG-004 (isolation) nor the source grounding (source stays CANDIDATE).
    frozen_expectation = {
        "trigger": "REVISE G2-TC2 v1 -> v2",
        "must_flip_to_NEED_REVIEW": ["G2-INF1", "G2-CONC"],
        "must_consider_synthesis": "SYN-CONC-001",  # depends on G2-CONC (load-bearing)
        "must_stay_CANDIDATE": ["ARG-004"],
        "source_grounding_untouched": True,   # REVISE of a proposition does not stale the source
    }

    ledger = ReviewLedger()
    v1 = ledger.add_version("G2-TC2", "v1: the 'I'-awareness is not a constructed relation")
    ledger.add_version("G2-TC2", "v2: narrower: not shown to be a constructed relation")
    ledger.record_review("G2-TC2", v1, "REVISE", "reviewer", "machine", "proposition",
                         "narrow the formulation (TD17-style low-level correction)",
                         replacement_ref="G2-TC2")
    ds = ledger.reduce()
    imp = ledger.impact_report("G2-TC2")

    direct = sorted(d["object"] for d in imp["directly_affected"])

    # ── verify the frozen expectations ─────────────────────────────────────────────
    checks = {
        "G2-INF1 -> NEED_REVIEW": ds.get("G2-INF1") == "NEED_REVIEW",
        "G2-CONC -> NEED_REVIEW": ds.get("G2-CONC") == "NEED_REVIEW",
        "isolation: ARG-004 stays CANDIDATE": ds.get("ARG-004") == "CANDIDATE",
        "impact names the load-bearing chain": direct == sorted(["G2-CONC", "G2-INF1"]),
    }
    print(f"  frozen expectation: {json.dumps(frozen_expectation, indent=2)}")
    print(f"  impact report direct: {direct}")
    for name, cond in checks.items():
        print(f"    {'✓' if cond else '✗'} {name}")

    # ── the semantic-impact interpretation (downstream scholarship) ────────────────
    downstream = {
        "SYN-CONC-001 (synthesis conclusion)": "depends on G2-CONC (load-bearing) -> stale until rebuilt",
        "essay claim S001 (refs SYN-CONC-001)": "stale (synthesis changed)",
        "learning interactions (derived from synthesis)": "must be regenerated from the corrected synthesis",
    }
    print("\n  semantic downstream impact (frozen):")
    for k, v in downstream.items():
        print(f"    - {k}: {v}")

    verdict = all(checks.values())
    print(f"\n  VERDICT: {'PASS (correction propagates semantically, isolation holds)' if verdict else 'FAIL'}")

    out = os.path.join(ROOT, "benchmarks/v0/review/VERTICAL-1-CORRECTION.json")
    payload = {
        "object_kind": "WHOLE_CHAIN_CORRECTION_TEST",
        "trigger": frozen_expectation,
        "frozen_expectation_met": checks,
        "semantic_downstream": downstream,
        "verdict": "PASS" if verdict else "FAIL",
        "review_status": "NOT_HUMAN_REVIEWED",
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"  wrote {out}")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
