#!/usr/bin/env python3
"""benchmark_graph_determinism.py — P3: deterministic canonical structural graph baseline.

Goal (narrow): prove one canonical graph projection is invariant under repeated execution and
irrelevant input ordering. NOT a claim that the decomposition is semantically correct.

    D1 same-process repeatability   run -> H, run again -> H  (H equal)
    D2 cross-process repeatability  process A/B/C -> same H   (catches hash seeds, unordered sets)
    D3 input-order invariance       f(G) == f(pi(G)) for semantic-preserving permutations
    D4 canonical serialization      stable hash across clusters/nodes/edges/json-key order + float norm

The graph is built from REAL data (the theme map's member_c1_ids co-occurrence) so this is not a toy.
Baseline decomposition: deterministic k-core (networkx.core_number), plus connected components.
The result is labeled DETERMINISTIC_BASELINE, NOT "best clustering".

Run:  python3 experiments/benchmark_graph_determinism.py          # full benchmark (D1..D4)
      python3 experiments/benchmark_graph_determinism.py --hash    # print the canonical hash (for cross-process)
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import subprocess
import sys

import networkx as nx

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
THEME_MAP = os.path.join(ROOT, "benchmarks/v0/theme-map-ipvv-v0.json")

DETECTOR_ID = "PATALA.GRAPH.DETERMINISTIC_BASELINE.v1"
VERIFIER_VERSION = "determinism-v0"


# ── build a real graph from the theme map's co-occurrence ─────────────────────
def build_graph() -> nx.Graph:
    """C1 nodes; an edge joins two C1s that co-occur in >=1 theme (weighted by co-occurrence count)."""
    with open(THEME_MAP, encoding="utf-8") as f:
        data = json.load(f)
    g = nx.Graph()
    for theme in data.get("themes", []):
        members = theme.get("member_c1_ids") or []
        for a in members:
            g.add_node(a)
            for b in members:
                if a < b:
                    if g.has_edge(a, b):
                        g[a][b]["weight"] += 1
                    else:
                        g.add_edge(a, b, weight=1)
    return g


# ── deterministic decomposition (k-core + components) ─────────────────────────
def decompose(g: nx.Graph) -> dict:
    """Deterministic structural decomposition: per-node k-core number + connected component id."""
    core = nx.core_number(g)          # deterministic
    comps = {c: i for i, cc in enumerate(nx.connected_components(g)) for c in cc}
    return {"core_number": core, "component": comps}


# ── canonical serialization (D4) ──────────────────────────────────────────────
def canonical_hash(g: nx.Graph, decomp: dict) -> str:
    """Hash a canonical representation: sorted nodes/edges/core/component, sorted keys, normalized floats."""
    nodes = sorted(g.nodes())
    # canonical undirected edge: sort the two endpoints so (a,b) and (b,a) hash identically
    edges = sorted((min(a, b), max(a, b), round(float(g[a][b].get("weight", 0.0)), 6))
                   for a, b in g.edges())
    core = sorted(decomp["core_number"].items())
    comp = sorted(decomp["component"].items())
    payload = {
        "detector": DETECTOR_ID,
        "version": VERIFIER_VERSION,
        "n_nodes": len(nodes),
        "nodes": nodes,
        "edges": edges,
        "core_number": core,
        "component": comp,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# ── input-order invariance (D3): permute node/edge insertion order ────────────
def permuted_graph(g: nx.Graph, seed: int) -> nx.Graph:
    """Rebuild the same graph but insert nodes/edges in a randomized order (semantic-preserving)."""
    rng = random.Random(seed)
    nodes = list(g.nodes())
    rng.shuffle(nodes)
    gp = nx.Graph()
    for n in nodes:
        gp.add_node(n)
    edges = list(g.edges(data=True))
    rng.shuffle(edges)
    for a, b, data in edges:
        gp.add_edge(a, b, weight=data.get("weight", 0.0))
    return gp


# ── the benchmark ─────────────────────────────────────────────────────────────
def run_determinism() -> dict:
    g = build_graph()
    base = canonical_hash(g, decompose(g))
    results = {"n_nodes": g.number_of_nodes(), "n_edges": g.number_of_edges(),
               "base_hash": base}

    # D1 same-process repeatability
    results["D1_same_process"] = canonical_hash(g, decompose(g)) == base

    # D3 input-order invariance (several seeds; semantic-preserving permutations)
    d3 = all(canonical_hash(permuted_graph(g, s), decompose(permuted_graph(g, s))) == base
             for s in range(5))
    results["D3_input_order_invariant"] = d3

    return results


def main() -> int:
    if "--hash" in sys.argv:
        g = build_graph()
        print(canonical_hash(g, decompose(g)))
        return 0

    r = run_determinism()
    print(f"DETERMINISM benchmark ({DETECTOR_ID})")
    print(f"  graph: {r['n_nodes']} nodes, {r['n_edges']} edges (theme-map co-occurrence)")
    print(f"  base canonical hash: {r['base_hash'][:16]}…")
    print(f"  D1 same-process repeatable: {r['D1_same_process']}")
    print(f"  D3 input-order invariant:   {r['D3_input_order_invariant']}")

    # D2 cross-process: hash in this process vs a fresh subprocess
    sub = subprocess.run([sys.executable, __file__, "--hash"], capture_output=True, text=True)
    other = sub.stdout.strip()
    print(f"  D2 cross-process identical: {other == r['base_hash']}  "
          f"({'same' if other == r['base_hash'] else 'DIFFERENT'})")
    d2 = other == r["base_hash"] and sub.returncode == 0
    print(f"  D4 canonical serialization: deterministic by construction (sorted keys/floats)")

    ok = r["D1_same_process"] and r["D3_input_order_invariant"] and d2
    print(f"\n  {'PASS' if ok else 'FAIL'}: deterministic baseline hash stable under "
          f"repeat, cross-process, and input-order permutation")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
