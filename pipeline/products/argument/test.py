#!/usr/bin/env python3
"""products/argument/test.py — Argument proof on REAL IPVV.
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/products/argument/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "pipeline"))

from products.argument.engine import arguments  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("ARGUMENT (#5) — proof on REAL IPVV\n")
    args = arguments()
    gate("real arguments derived", len(args) >= 40, f"{len(args)} from real C1s")
    a = args[0]
    gate("thesis from real C1", bool(a["thesis"]), f"{a['argument_id']}")
    gate("premises derived", len(a["premises"]) >= 1, f"{len(a['premises'])} premises")
    gate("inference structure", a["inference"].get("conclusion_id") == "C0", "premises -> conclusion")
    gate("source-backed", len(a["source_refs"]) >= 1, f"source_ref={a['source_refs']}")
    gate("defeaters recorded", len(a["defeaters"]) >= 1, f"defeater present")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
