#!/usr/bin/env python3
"""tests/test_goldutil.py — validate the gold-fixture tooling (Builds 1 & 3).

Checks:
  1. wrap_fixture produces a valid CP0 BenchmarkFixture envelope
  2. validate_gold passes on the hand-built golds (ARG-001, ARG-002)
  3. the validator catches a real defect (a broken passage id / orphan premise)
  4. every inference's premises + conclusions exist as nodes

Run: cd research && . .venv/bin/activate && python tests/test_goldutil.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.gold import build_gold_v0
from patala_ml.gold002 import build_gold_002
from patala_ml.goldutil import wrap_fixture, validate_gold

PASS = 0
FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        print(f"  ✓ {name}")
        PASS += 1
    else:
        print(f"  ✗ {name} {detail}")
        FAIL += 1


def main():
    # 1. ARG-001 + ARG-002 are internally consistent
    print("== hand-built golds are consistent ==")
    for builder in (build_gold_v0, build_gold_002):
        gold = builder()
        r = validate_gold(gold)
        check(f"{gold['gold_id']} consistent", r["ok"], r["problems"])
        check(f"{gold['gold_id']} has boundary", bool(gold.get("boundary")))

    # 2. inference integrity (premises + conclusions exist as nodes)
    print("\n== inference integrity ==")
    gold = build_gold_002()
    node_ids = {n.get("proposition_id") or n.get("id") for n in gold["nodes"]}
    for inf in gold["inferences"]:
        check(f"{inf['inference_id']} premises exist",
              all(p in node_ids for p in inf["premise_ids"]), inf["premise_ids"])
        check(f"{inf['inference_id']} conclusions exist",
              all(c in node_ids for c in inf["conclusion_ids"]), inf["conclusion_ids"])

    # 3. wrap_fixture produces a valid envelope
    print("\n== fixture envelope ==")
    fx = wrap_fixture(build_gold_002())
    for k in ["fixture_id", "task_family", "task", "source_ids", "gold_version",
              "authoring_method", "review_state", "allowed_training_use", "split_class",
              "input", "expected"]:
        check(f"envelope has {k}", k in fx)
    check("task = argument_extraction", fx["task"] == "argument_extraction")
    check("EVALUATION_ONLY split", fx["split_class"] == "EVALUATION_ONLY")
    check("allowed_training_use = false", fx["allowed_training_use"] is False)
    check("SINGLE_EDITOR_GOLD", fx["review_state"] == "SINGLE_EDITOR_GOLD")
    check("source_ids has a real passage", any(s.startswith("pt:passage:ipvv:chunk") for s in fx["source_ids"]))

    # 4. the validator CATCHES a real defect
    print("\n== validator catches defects ==")
    bad = build_gold_002()
    # break a passage id
    bad["nodes"][0]["grounding"]["passage_id"] = "pt:passage:ipvv:NONEXISTENT.md"
    r = validate_gold(bad)
    check("catches unresolved passage", not r["ok"], r["problems"])
    # break an inference (missing premise)
    bad2 = build_gold_002()
    bad2["inferences"][0]["premise_ids"].append("GHOST")
    r2 = validate_gold(bad2)
    check("catches missing premise", not r2["ok"], r2["problems"])

    print(f"\n=== RESULT: {PASS} pass / {FAIL} fail ===")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
