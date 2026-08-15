#!/usr/bin/env python3
"""products/timeline/test.py — Timeline proof on REAL data.
Run: cd patala && python3 pipeline/products/timeline/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))

from products.timeline.engine import schools, school, lineage, era_breakdown, timeline  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("TIMELINE — proof on REAL data\n")
    tl = timeline()
    gate("real timeline loaded", tl["n_schools"] >= 10, f"{tl['n_schools']} schools")

    ss = schools()
    gate("schools have period + era", all(s.get("period") and s.get("era") for s in ss),
         "each school is period/era-anchored")

    eras = era_breakdown()
    gate("eras present", set(eras) >= {"textual", "comparative", "archaeological"}, f"eras={list(eras)}")

    trika = school("trika")
    gate("trika resolves", bool(trika), f"trika={trika.get('name') if trika else 'none'}")
    chain = lineage("trika")
    gate("lineage resolves ancestors", len(chain) >= 5, f"{len(chain)} ancestors: {' <- '.join(s['id'] for s in chain)}")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
