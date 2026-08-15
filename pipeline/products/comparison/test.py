#!/usr/bin/env python3
"""products/comparison/test.py — Comparison proof on REAL IPVV.
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/products/comparison/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "pipeline"))

from products.comparison.engine import compare_between  # noqa: E402
from products.argument.engine import arguments  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("COMPARISON (#13) — proof on REAL IPVV\n")
    args = arguments()
    a, b = args[0]["argument_id"], args[1]["argument_id"]
    cmp = compare_between(a, b)
    gate("comparison classified", cmp["classification"] in ("AGREEMENT", "REAL CRUX"),
         f"classification={cmp['classification']}")
    gate("both positions resolved", cmp["a"] == a and cmp["b"] == b, f"{a} vs {b}")
    gate("divergence reported", "a_asserts" in cmp["divergent"] and "b_asserts" in cmp["divergent"],
         f"a_asserts={len(cmp['divergent']['a_asserts'])}, b_asserts={len(cmp['divergent']['b_asserts'])}")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
