#!/usr/bin/env python3
"""products/tension_finder/test.py — tension-finder proof on real IPVV.
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/products/tension_finder/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))

from products.tension_finder.engine import find_tensions  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("TENSION FINDER — proof on real IPVV\n")
    d = find_tensions()
    gate("real tensions found", d["count"] >= 20, f"{d['count']} tensions")
    gate("multiple kinds", len(d["kinds_found"]) >= 4, f"kinds={d['kinds_found']}")

    # each tension has kind + quote/why + score
    gate("tensions carry kind + score", all(t.get("kind") and t.get("score") for t in d["tensions"]),
         "every tension is typed + scored")
    gate("sorted by score desc", [t["score"] for t in d["tensions"]] ==
         sorted([t["score"] for t in d["tensions"]], reverse=True), "highest-interest first")

    # min_score filter
    high = find_tensions(min_score=0.9)
    gate("min_score filters", high["count"] < d["count"], f"high-score={high['count']} vs all={d['count']}")

    # honest boundary (MACHINE_PROPOSED, never a truth claim)
    gate("MACHINE_PROPOSED honesty", "MACHINE_PROPOSED" in d["note"], "surfaces possibilities, never decides truth")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
