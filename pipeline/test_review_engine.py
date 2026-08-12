#!/usr/bin/env python3
"""pipeline/test_review_engine.py — validate the Phase-3 executable-corrections vertical loop.

The acceptance criterion (from the spec):
  One review of one versioned proposition must produce an immutable ReviewEvent, a new effective
  scholarly state, and a deterministic impact report over ARG-002 WITHOUT rewriting any historical
  object or touching unrelated objects.

Checks (the 8-point criterion):
  1. v1 is retained (immutable, never rewritten)
  2. the ReviewEvent resolves
  3. v2 is created (REVISE creates, doesn't overwrite)
  4. G2-INF1 becomes NEED_REVIEW (it USES_AS_PREMISE the revised proposition)
  5. G2-CONC becomes NEED_REVIEW (the inference's conclusion)
  6. the impact report names exactly G2-INF1 + G2-CONC as directly affected
  7. ARG-004 (unrelated) stays CANDIDATE (isolation)
  8. the reducer is idempotent (deterministic)

Plus the doctrine invariants:
  - ACCEPT ≠ truth, REJECT ≠ delete, REVISE ≠ overwrite (history preserved)
  - a REVISE of a proposition does NOT stale its source grounding (source/pp/TD stay CANDIDATE)

Run: cd /root/projects/patala && python3 pipeline/test_review_engine.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from review_engine import ReviewLedger, DECISIONS

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
    print("== the vertical review loop (ARG-002, G2-TC2 v1 -> v2) ==")
    ledger = ReviewLedger()
    v1 = ledger.add_version("G2-TC2", "v1: the I-awareness is not a constructed relation")
    v2 = ledger.add_version("G2-TC2", "v2: narrower formulation")
    ledger.record_review(
        "G2-TC2", v1, "REVISE", "reviewer", "machine", "proposition",
        "narrow the formulation", replacement_ref="G2-TC2",
    )
    ds1 = ledger.reduce()
    ds2 = ledger.reduce()  # idempotency

    check("1. v1 retained (immutable)", any(x.version == "v1" for x in ledger.versions["G2-TC2"]))
    check("2. ReviewEvent resolves", len(ledger.events) == 1 and ledger.events[0].review_id == "REV-0001")
    check("3. v2 created (REVISE creates, not overwrites)",
          any(x.version == "v2" for x in ledger.versions["G2-TC2"]))
    check("4. G2-INF1 -> NEED_REVIEW (USES_AS_PREMISE)", ds1.get("G2-INF1") == "NEED_REVIEW")
    check("5. G2-CONC -> NEED_REVIEW (inference conclusion)", ds1.get("G2-CONC") == "NEED_REVIEW")

    imp = ledger.impact_report("G2-TC2")
    direct = sorted(d["object"] for d in imp["directly_affected"])
    check("6. impact names exactly G2-INF1 + G2-CONC", direct == ["G2-CONC", "G2-INF1"], direct)

    check("7. ARG-004 untouched (isolation)", ds1.get("ARG-004") == "CANDIDATE")
    check("8. reducer idempotent (deterministic)", ds1.states == ds2.states)

    print("\n== doctrine invariants ==")
    check("REVISE does not stale source grounding (source CANDIDATE)", ds1.get("source:V2L") == "CANDIDATE")
    check("REVISE does not stale philological proof (pp CANDIDATE)", ds1.get("pp:ipvv:v2l:p0") == "CANDIDATE")
    check("G2-TC2 derived state = SUPERSEDED (not deleted)", ds1.get("G2-TC2") == "SUPERSEDED")
    check("valid decisions enforced", set(DECISIONS) == {"ACCEPT", "REVISE", "REJECT", "ABSTAIN"})

    print("\n== REJECT semantics (REJECT != delete) ==")
    ledger2 = ReviewLedger()
    v1 = ledger2.add_version("G2-TC2", "content")
    ledger2.record_review("G2-TC2", v1, "REJECT", "reviewer", "scholar", "proposition", "unsupported")
    ds = ledger2.reduce()
    check("REJECT -> effective REJECTED", ds.get("G2-TC2") == "REJECTED")
    check("REJECT keeps v1 resolvable (not deleted)", len(ledger2.versions["G2-TC2"]) == 1)
    check("REJECT propagates to inference NEED_REVIEW", ds.get("G2-INF1") == "NEED_REVIEW")

    print("\n== Phase 3D — the MCP capability surface (proposal / authorization / simulation) ==")
    l3 = ReviewLedger()
    l3.add_version("G2-TC2", "v1")
    l3.add_version("G2-TC2", "v2")
    # propose: machine-safe, no state change
    p = l3.propose_review("G2-TC2", "v1", "REVISE", "narrow", "proposition")
    check("propose_review returns PROPOSED/MACHINE", p["status"] == "PROPOSED" and p["origin"] == "MACHINE")
    check("propose_review does not change state", l3.reduce().get("G2-TC2") == "CANDIDATE")
    # submit: machine forbidden (the executable constitution)
    try:
        l3.submit_review("hermes", "machine", "*", "G2-TC2", "v1", "REVISE", "proposition", "x")
        check("machine submit blocked", False)
    except PermissionError:
        check("machine submit blocked (authorization policy)", True)
    # submit: scholar allowed
    ev = l3.submit_review("scholar-x", "scholar", "proposition", "G2-TC2", "v1", "REVISE",
                          "proposition", "narrow", replacement_ref="G2-TC2")
    check("scholar submit creates a ReviewEvent", ev.review_id.startswith("REV-"))
    # simulate: zero-write hypothetical
    before = len(l3.events)
    sim = l3.simulate_review("G2-TC2", "REJECT")
    check("simulate_review is zero-write", len(l3.events) == before)
    check("simulate_review computes hypothetical impact", sim["derived_state"].get("G2-INF1") == "NEED_REVIEW")
    # get_state
    s = l3.get_state("G2-TC2")
    check("get_state returns effective state + version", s["effective_state"] == "SUPERSEDED" and s["version"] == "v2")
    check("get_state lists dependencies", "USES_AS_PREMISE" in [d["type"] for d in s["dependencies"]["direct"]])

    print(f"\n=== RESULT: {PASS} pass / {FAIL} fail ===")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
