#!/usr/bin/env python3
"""tests/test_gold.py — validate ARGUMENT GOLD v0 (the first substantive benchmark).

The gold object must be honest and internally consistent:
  1. every node has a real resolvable passage id (chunkV2-O-...)
  2. every inference's premises + conclusion reference real nodes
  3. the kind taxonomy is respected (textual ≠ interpretive ≠ inference ≠ conclusion)
  4. explicit vs reconstructed vs implicit is distinguished
  5. the boundary is present + honest (does not overclaim)
  6. it is NOT reported as 'scholarship verified' — it's a MACHINE_PROPOSED gold candidate

Run: cd research && . .venv/bin/activate && python tests/test_gold.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.gold import build_gold_v0

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
    gold = build_gold_v0()
    nodes = {n["id"]: n for n in gold["nodes"]}

    # 1. real resolvable passage ids
    print("== resolvable source support ==")
    real_ids = set()
    for n in gold["nodes"]:
        for pid in n["source_support"]["passage_ids"]:
            real_ids.add(pid)
    check("passage ids use the real chunk format",
          all(pid.startswith("pt:passage:ipvv:chunk") for pid in real_ids),
          real_ids)
    check("V2-O passage id is the real one",
          "pt:passage:ipvv:chunkV2-O-saptamo-vimarsa.md" in real_ids)

    # 2. inference integrity
    print("\n== inference integrity ==")
    for inf in gold["inferences"]:
        check(f"{inf['id']} premises exist", all(p in nodes for p in inf["premise_ids"]),
              inf["premise_ids"])
        check(f"{inf['id']} conclusion exists", inf["conclusion_id"] in nodes,
              inf["conclusion_id"])

    # 3. kind taxonomy
    print("\n== kind taxonomy ==")
    kinds = {n["kind"] for n in gold["nodes"]}
    check("has TEXTUAL_CLAIM", "TEXTUAL_CLAIM" in kinds, kinds)
    check("has INTERPRETIVE_CLAIM", "INTERPRETIVE_CLAIM" in kinds)
    check("has CONCLUSION", "CONCLUSION" in kinds)
    check("has IMPLICIT_PREMISE", "IMPLICIT_PREMISE" in kinds)
    check("the conclusion is NOT a textual claim",
          next(n for n in gold["nodes"] if n["id"] == "G-CONC")["kind"] != "TEXTUAL_CLAIM")

    # 4. explicitness distinguished
    print("\n== explicitness ==")
    exp = {n["explicitness"] for n in gold["nodes"]}
    check("EXPLICIT present", "EXPLICIT" in exp)
    check("RECONSTRUCTED present", "RECONSTRUCTED" in exp)
    check("IMPLICIT present", "IMPLICIT" in exp)

    # 5. boundary honest
    print("\n== boundary ==")
    b = gold["boundary"]
    check("boundary has text", bool(b["text"]))
    check("boundary not_claiming present", len(b["not_claiming"]) >= 1)
    check("boundary does not overclaim",
          "does NOT by itself establish" in b["text"])

    # 6. honest status (not 'scholarship verified')
    print("\n== honest status ==")
    check("gold is MACHINE_PROPOSED (not editor-accepted)", gold["status"] == "MACHINE_PROPOSED")
    check("not claimed as verified", "VERIFIED" not in gold["status"])
    check("philological status honest", b["philological"]["status"] == "P0")

    print(f"\n=== RESULT: {PASS} pass / {FAIL} fail ===")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
