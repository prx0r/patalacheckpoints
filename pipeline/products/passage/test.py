#!/usr/bin/env python3
"""products/passage/test.py — Passage/Reading (#3) proof on REAL IPVV.
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/products/passage/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))

from products.passage.engine import make_query, canonical_passage  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("PASSAGE / READING (#3) — proof on REAL IPVV\n")
    q = make_query()

    # resolve by fragment
    pid = q.resolve("chunkD")
    gate("resolve by fragment", pid is not None, f"chunkD -> {pid}")
    p = q.get("chunkD")
    gate("canonical passage", bool(p) and bool(p["source_sanskrit"]),
         f"{p['passage_id']} work={p['work_id']}" if p else "none")
    gate("has real content", bool(p and p["l2_translation"] and p["c1_commentary"]),
         "source + L2 + C1 all present")

    # neighbors
    nb = q.neighbors("chunkD")
    gate("neighbors resolve", len(nb) >= 1, f"{len(nb)} neighbors")

    # path between two real passages
    paths = q.path("chunkA", "chunkD", max_hops=4)
    gate("path exists", len(paths) >= 1, f"{len(paths)} path(s)")

    # evidence
    ev = q.evidence("chunkD")
    gate("evidence resolves", bool(ev and ev["immutable_id"]), f"immutable={ev['immutable_id'] if ev else None}")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
