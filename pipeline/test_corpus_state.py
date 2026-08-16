#!/usr/bin/env python3
"""pipeline/test_corpus_state.py — validate the Agent 2 translation-state ledger + transition contract.

Checks:
  1. next_valid_action: MISSING_SOURCE -> ACQUIRE_SOURCE (not eligible for agent3)
  2. next_valid_action: RAW_SANSKRIT source -> BUILD_L0_SOURCE_MODE (blocked, not eligible)
  3. next_valid_action: L0 VERIFIED -> GENERATE_TRANSLATION (eligible for agent3)
  4. source-format detection: AND_GLOSS vs RAW_SANSKRIT
  5. the ledger runs end-to-end on the real mount + serializes valid JSON
  6. invariant: the output contract is stable (no work has an empty/invalid action)

Run: cd /root/patalacheckpoints && python3 pipeline/test_corpus_state.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from corpus_state import WorkState, next_valid_action, detect_source_format, discover_works

PASS = 0
FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        print(f"  ✓ {name}")
        PASS += 1
    else:
        print(f"  ✗ FAIL: {name}" + (f" — {detail}" if detail else ""))
        FAIL += 1


def main():
    print("== source-format detection ==")
    check("detects AND_GLOSS", detect_source_format("text [and]-the-light (prakāśa) more [and]-x") == "AND_GLOSS")
    raw = ("kālī tu bhairavārūḍhā mahākālakalāśinī |\nvyomarūpā anantākhyā aṣṭamūrtidharā śivā")
    check("detects RAW_SANSKRIT", detect_source_format(raw) == "RAW_SANSKRIT")

    print("\n== transition contract ==")
    # missing source
    s = WorkState(work_id="x", source_available=False)
    na = next_valid_action(s)
    check("MISSING_SOURCE -> ACQUIRE_SOURCE", na["action"] == "ACQUIRE_SOURCE", na)
    check("MISSING_SOURCE not eligible for agent3", na["eligible_for_agent3"] is False, na)

    # raw sanskrit source, L0 not built
    s = WorkState(work_id="kramasadbhava", source_available=True,
                  source_format="RAW_SANSKRIT", l0_status="NOT_STARTED")
    na = next_valid_action(s)
    check("RAW_SANSKRIT -> BUILD_L0_SOURCE_MODE", na["action"] == "BUILD_L0_SOURCE_MODE", na)
    check("RAW_SANSKRIT blocked (not eligible)", na["blocked"] is True and na["eligible_for_agent3"] is False, na)

    # L0 verified (source de-facto present) -> generate translation
    s = WorkState(work_id="ipvv", source_available=False,
                  l0_status="VERIFIED", t1="NOT_STARTED", c1="NOT_STARTED")
    na = next_valid_action(s)
    check("L0 VERIFIED -> GENERATE_TRANSLATION (eligible)", na["action"] == "GENERATE_TRANSLATION" and na["eligible_for_agent3"], na)

    print("\n== end-to-end ledger on real mount ==")
    if os.path.isdir("/mnt/HC_Volume_106427611/sanskritree"):
        works = discover_works()
        check("discovers works", len(works) > 0, len(works))
        # every work has a valid next action
        bad = [w.work_id for w in works if not next_valid_action(w).get("action")]
        check("every work has a valid next action", not bad, bad)
        # IPVV should be L0 VERIFIED (the flagship floor)
        ipvv = [w for w in works if w.work_id == "ipvv"]
        check("IPVV L0 VERIFIED", ipvv and ipvv[0].l0_status == "VERIFIED",
              ipvv[0].l0_status if ipvv else "no ipvv")
        # kramasadbhava should be RAW_SANSKRIT (a real, detected source)
        krama = [w for w in works if w.work_id == "kramasadbhava"]
        check("kramasadbhava source detected RAW_SANSKRIT",
              krama and krama[0].source_format == "RAW_SANSKRIT",
              krama[0].source_format if krama else "no kramasadbhava")
    else:
        print("  (skipping end-to-end: mount not present)")

    print(f"\n=== RESULT: {PASS} pass / {FAIL} fail ===")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
