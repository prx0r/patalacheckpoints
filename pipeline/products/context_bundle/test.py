#!/usr/bin/env python3
"""products/context_bundle/test.py — Agent Context Bundle (#16) proof on REAL IPVV.
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/products/context_bundle/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))

from products.context_bundle.engine import build_bundle, BUDGETS  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("AGENT CONTEXT BUNDLE (#16) — proof on REAL IPVV\n")
    micro = build_bundle("eternal self", variant="micro")
    std = build_bundle("eternal self", variant="standard")
    deep = build_bundle("eternal self", variant="deep")

    gate("real entity", bool(micro["entity"]["work_id"]), f"work={micro['entity']['work_id']}")
    gate("content-addressed", len(micro["bundle_hash"]) == 16, f"hash={micro['bundle_hash']}")
    gate("budget respected", all(
        (b["tokens_used"] <= BUDGETS[b["variant"]]) for b in (micro, std, deep)),
        f"micro={micro['tokens_used']}, std={std['tokens_used']}, deep={deep['tokens_used']}")
    gate("micro < deep tokens", micro["tokens_used"] < deep["tokens_used"],
         f"{micro['tokens_used']} < {deep['tokens_used']}")
    gate("deep has all sections", len(deep["sections"]) >= len(micro["sections"]),
         f"deep={len(deep['sections'])} sections, micro={len(micro['sections'])}")
    gate("has claim/argument", bool(micro.get("argument_id")), f"argument={micro.get('argument_id')}")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
