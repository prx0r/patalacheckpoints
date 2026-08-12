#!/usr/bin/env python3
"""test_graph_determinism.py — P3: deterministic canonical structural graph baseline.

Asserts a deterministic decomposition is invariant under:
    D1 same-process repeat
    D2 cross-process (fresh subprocess -> same canonical hash)
    D3 input-order permutation (f(G) == f(pi(G)) for semantic-preserving reorders)
    D4 canonical serialization (endpoint-sorted edges, sorted nodes/keys, normalized floats)

Narrow claim: at least one reproducible canonical structural graph baseline exists.
This is NOT a claim that the decomposition is semantically correct (DETERMINISM != SEMANTIC_VALIDITY).
"""
from __future__ import annotations

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "experiments"))

from benchmark_graph_determinism import build_graph, canonical_hash, decompose, permuted_graph

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


print("== D1 same-process repeatability ==")
g = build_graph()
base = canonical_hash(g, decompose(g))
check("same graph, same hash across two calls", canonical_hash(g, decompose(g)) == base)

print("\n== D2 cross-process repeatability ==")
sub = subprocess.run([sys.executable, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "experiments",
    "benchmark_graph_determinism.py"), "--hash"], capture_output=True, text=True)
check("fresh process produces identical canonical hash", sub.stdout.strip() == base and sub.returncode == 0)

print("\n== D3 input-order invariance ==")
d3 = all(canonical_hash(permuted_graph(g, s), decompose(permuted_graph(g, s))) == base
         for s in range(5))
check("hash invariant under node/edge insertion-order permutation", d3)

print("\n== D4 canonical serialization (endpoint-sorted undirected edges) ==")
# (a,b) and (b,a) must hash identically (undirected edge canonicalization)
g2 = build_graph()
swap = __import__("networkx").Graph()
for a, b in g2.edges():
    swap.add_edge(b, a, weight=g2[a][b]["weight"])
check("undirected edge (a,b) == (b,a) hashes identically",
      canonical_hash(swap, decompose(swap)) == base)

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (deterministic baseline: repeat/cross-process/input-order/canonical all stable)"))
sys.exit(1 if failures else 0)
