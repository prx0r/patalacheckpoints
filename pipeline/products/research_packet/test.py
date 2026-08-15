#!/usr/bin/env python3
"""products/research_packet/test.py — Research Packet proof on REAL IPVV.
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/products/research_packet/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "pipeline"))

from products.research_packet.engine import research_packet  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("RESEARCH PACKET (#9) — proof on REAL IPVV\n")
    pkt = research_packet("eternal self memory")
    gate("real graph built", pkt["retrieval"]["graph_nodes"] >= 40,
         f"{pkt['retrieval']['graph_nodes']} nodes, {pkt['retrieval']['graph_edges']} edges")
    gate("method is PathRAG", "PathRAG" in pkt["retrieval"]["method"], pkt["retrieval"]["method"])
    gate("packet matches real passages", pkt["count"] >= 1, f"{pkt['count']} passages")
    if pkt["matched_passages"]:
        gate("entries source-bound", bool(pkt["matched_passages"][0]["immutable_id"]),
             pkt["matched_passages"][0]["passage_id"])

    # a flow-only query should still surface graph-ranked passages
    pkt2 = research_packet("prostration eligibility jaya")
    gate("flow-only query surfaces graph neighbors", pkt2["count"] >= 1, f"{pkt2['count']} via PathRAG")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
