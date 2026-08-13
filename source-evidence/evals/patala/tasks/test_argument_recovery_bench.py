#!/usr/bin/env python3
"""test_argument_recovery_bench.py — ARGUMENT-RECOVERY-BENCH-v1 acceptance (Agent 1 P0).

Checks (per the directive):
  1. the gold schema is frozen (propositions/inferences/attacks/open_questions/cruxes with speaker,
     commitment, explicitness, warrant status)
  2. proposition precision/recall are computed
  3. UNSUPPORTED_BRIDGE_RATE (THE metric) flags a candidate that invents B between A and C
  4. a faithful candidate scores bridge=0; an invented-bridge candidate scores bridge>0
  5. crux recall + open-question preservation are measured
  6. scoring is NON-CIRCULAR: it never reads a gold 'expected' verdict
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from argument_recovery_bench import GOLD_SCHEMA, score_recovery, aggregate, _overlap

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


GOLD = {
    "case_id": "IPVV-V2L",
    "propositions": [
        {"pid": "P1", "text": "the determination is error-form", "speaker": "author",
         "commitment": "ASSERTS", "explicitness": "EXPLICIT", "source_span": "S1"},
        {"pid": "P2", "text": "an inert part cannot establish", "speaker": "author",
         "commitment": "ASSERTS", "explicitness": "EXPLICIT", "source_span": "S2"},
        {"pid": "O1", "text": "as fire burns wood though inert so the determination establishes",
         "speaker": "opponent", "commitment": "REPORTS", "explicitness": "EXPLICIT", "source_span": "S3"},
    ],
    "inferences": [{"iid": "I1", "premises": ["P1", "P2"], "conclusion": "nothing external is established",
                    "warrant": "inertness blocks establishing", "warrant_status": "RATIONAL_RECONSTRUCTION",
                    "warrant_constraints": ["S2"]}],
    "attacks": [{"attacker": "O1", "target_premise": "P2", "type": "UNDERMINE"}],
    "open_questions": [{"text": "does establishing require the self-luminous awareness", "status": "OPEN"}],
    "cruxes": [{"crux_id": "C1", "decisive_premises": ["P2"],
                "question": "does establishing require the self-luminous awareness"}],
}

print("== 1. gold schema ==")
check("gold has all 5 structures", all(k in GOLD for k in
      ("propositions", "inferences", "attacks", "open_questions", "cruxes")))
check("propositions carry speaker/commitment/explicitness/span",
      all(p["speaker"] and p["commitment"] and p["explicitness"] and p["source_span"]
          for p in GOLD["propositions"]))
check("inferences carry warrant + warrant_status + constraints",
      all(i["warrant"] and i["warrant_status"] in ("TEXT_EXPLICIT", "RATIONAL_RECONSTRUCTION",
                                                   "EDITORIAL_RECONSTRUCTION") and i["warrant_constraints"]
          for i in GOLD["inferences"]))

print("\n== 2. scoring is non-circular (no gold 'expected' verdict consumed) ==")
import inspect
src = inspect.getsource(score_recovery)
check("scorer never reads 'expected'", "expected" not in src)

print("\n== 3. faithful vs invented-bridge candidate ==")
good = {"argument_steps": ["the determination is error-form", "an inert part cannot establish",
                           "therefore nothing external is established (lines 10-12)"],
        "decision_for_l2": "render per-act",
        "open_items": [{"text": "does establishing require the self-luminous awareness", "status": "OPEN"}]}
bad = {"argument_steps": ["therefore the whole world is an illusion",  # invented bridge, no anchor
                          "the determination is error-form"],
       "decision_for_l2": "render universally",
       "open_items": []}
rg = score_recovery(GOLD, good)
rb = score_recovery(GOLD, bad)
check("faithful candidate: unsupported_bridge_rate == 0", rg["unsupported_bridge_rate"] == 0.0, rg["unsupported_bridge_rate"])
check("invented candidate: unsupported_bridge_rate > 0", rb["unsupported_bridge_rate"] > 0.0, rb["unsupported_bridge_rate"])
check("faithful candidate recovers propositions", rg["proposition_recall"] >= 0.6, rg["proposition_recall"])
check("invented candidate lower recall", rb["proposition_recall"] <= rg["proposition_recall"])

print("\n== 4. crux recall + open-question preservation ==")
check("faithful candidate preserves crux", rg["crux_recall"] >= 0.5, rg["crux_recall"])
check("faithful candidate preserves open question", rg["open_question_preservation"] >= 0.5, rg["open_question_preservation"])
check("invented candidate drops open question", rb["open_question_preservation"] <= rg["open_question_preservation"])

print("\n== 5. aggregate ==")
agg = aggregate([rg, rb])
check("aggregate reports corpus means + case count", agg["cases"] == 2 and "unsupported_bridge_rate" in agg)

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (ARGUMENT-RECOVERY-BENCH-v1 works)"))
sys.exit(1 if failures else 0)
