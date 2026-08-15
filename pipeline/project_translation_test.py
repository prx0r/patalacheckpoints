#!/usr/bin/env python3
"""pipeline/project_translation_test.py — proof for the ingestion-ROI projector.
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/project_translation_test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "pipeline"))

import project_translation as PT  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("PROJECTOR — proof (ingestion-ROI estimator)\n")

    # whole-corpus projection
    p = PT.project()
    gate("corpus projection has rows", len(p["rows"]) > 0, f"{len(p['rows'])} works")
    gate("corpus totals present", p["total_verses"] > 0 and p["total_calls"] > 0,
         f"{p['total_verses']} verses, {p['total_calls']} calls")
    gate("costs are sane (miss >= hit)", p["total_cost_miss_usd"] >= p["total_cost_hit_usd"],
         f"miss=${p['total_cost_miss_usd']} hit=${p['total_cost_hit_usd']}")

    # single work
    w = PT.project("matrkabhedatantra")
    gate("single-work projection", len(w["rows"]) == 1 and w["rows"][0]["work"] == "matrkabhedatantra")
    r = w["rows"][0]
    gate("calls = verses × 5", r["calls"] == r["verses"] * 5, f"{r['verses']}×5={r['calls']}")
    gate("cost scales with verses", r["cost_miss_usd"] > 0 and r["cost_hit_usd"] < r["cost_miss_usd"],
         f"${r['cost_miss_usd']} miss / ${r['cost_hit_usd']} hit")

    # scenario: batch + parallel cut calls/time
    p1 = PT.project(batch=16, parallel=3)
    p0 = PT.project(batch=1, parallel=1)
    gate("batch+parallel cuts calls", p1["total_calls"] <= p0["total_calls"],
         f"{p0['total_calls']} -> {p1['total_calls']}")
    gate("batch+parallel cuts hours", p1["total_hours"] < p0["total_hours"],
         f"{p0['total_hours']} -> {p1['total_hours']} hrs")

    # unknown model rejected
    try:
        PT.project(model="nope")
        gate("unknown model rejected", False, "should raise")
    except ValueError:
        gate("unknown model rejected", True)

    # assess integration (the projection field)
    try:
        import assess
        r = assess.assess("matrkabhedatantra")
        gate("assess carries projection", r.get("projection") is not None,
             f"{r['projection']['verses']} verses, ${r['projection']['cost_miss_usd']} miss")
    except Exception as e:
        gate("assess carries projection", False, str(e)[:60])

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
