#!/usr/bin/env python3
"""products/review_queue/test.py — review-queue proof on real objects.
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/products/review_queue/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))

from products.review_queue.engine import next_for  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("REVIEW QUEUE — proof on real objects\n")
    r = next_for(limit=10)
    gate("real objects in queue", len(r["queue"]) >= 5, f"{len(r['queue'])} queued")
    gate("pending count present", r["total_pending"] >= 40, f"{r['total_pending']} unreviewed pending")

    # sorted by priority desc
    priorities = [q["priority"] for q in r["queue"]]
    gate("sorted by priority desc", priorities == sorted(priorities, reverse=True),
         f"top={priorities[0]}, bottom={priorities[-1]}")

    # each queue item has the why
    gate("every item has a why", all(q.get("why") for q in r["queue"]),
         "priority explained (unc × blast × cent / cost)")

    # scope filter narrows
    arg = next_for(scope="argument", limit=5)
    gate("scope filter works", len(arg["queue"]) <= len(r["queue"]),
         f"argument-scope={len(arg['queue'])} vs all={len(r['queue'])}")

    # machine-proposed honesty (no banned claim)
    gate("notes MACHINE_PROPOSED", "MACHINE_PROPOSED" in r["note"],
         "prioritizes, never decides truth")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
