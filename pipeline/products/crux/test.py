#!/usr/bin/env python3
"""products/crux/test.py — Crux proof on REAL IPVV.
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/products/crux/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "pipeline"))

from products.crux.engine import crux_between  # noqa: E402
from products.argument.engine import arguments  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("CRUX (#6) — proof on REAL IPVV\n")
    args = arguments()
    a, b = args[0]["argument_id"], args[1]["argument_id"]
    cx = crux_between(a, b)
    gate("crux computes divergence", "crux_a_asserts" in cx and "crux_b_asserts" in cx,
         f"crux_count={cx['crux_count']}")
    gate("positions resolved", cx["position_a"] == a and cx["position_b"] == b, f"{a} vs {b}")
    gate("shared reported", "shared_premises" in cx, f"{len(cx['shared_premises'])} shared")
    gate("interpretation present", bool(cx["interpretation"]), "actionable interpretation")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
