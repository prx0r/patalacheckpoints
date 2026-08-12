#!/usr/bin/env python3
"""louvain_stability.py — P-019 v2 ablation: is Louvain's modularity partition stable, and how does it
relate to the deterministic k-core hierarchy?

Requires python-louvain (`community`) — run with the venv that has it, e.g.
  .venv/bin/python experiments/louvain_stability.py

The research question the coordinator framed:
> Are Louvain's semantic-looking divisions supported by stable graph structure, or are some of them
> artifacts of modularity degeneracy (sparse KGs admit exponentially many near-optimal modularity
> partitions)?

Metrics:
  1. Louvain partition stability across seeds + fresh processes + insertion-order permutations
     (n_communities distribution; the pairwise co-membership stability S(u,v) below is the killer metric).
  2. Pairwise co-membership stability  S(u,v) = #{runs where u,v co-cluster} / #runs
        S ~ 1.0 robust relationship · S ~ 0.5 unstable boundary · S ~ 0 consistently separate
     We then compare unstable boundaries (0.4 < S < 0.6) against the k-shell structure.
  3. k-core x Louvain contingency: the k-core-number distribution inside each Louvain community.

Honesty: k-core = STRUCTURAL FACT; Louvain community = heuristic proposal. Neither is a theme, and none of
this makes any claim about philosophical centrality.
"""
from __future__ import annotations

import json
import os
import random
import sys

import networkx as nx

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import community
from patala_ml.c1corpus import load_c1_nodes
from patala_ml.cluster import build_hybrid_graph_c1
from patala_ml.kcore import core_hierarchy

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
OUT = os.path.join(ROOT, "benchmarks/v0/structural/louvain-stability-ipvv-c1-v0.json")

N_SEEDS = 20


def run_partition(nodes, seed: int, permute: bool = False):
    """Return the Louvain partition (node -> community) for one seed over the frozen evidence graph."""
    if permute:
        nodes = list(nodes)
        random.Random(seed).shuffle(nodes)
    g = build_hybrid_graph_c1(nodes)
    return community.best_partition(g, random_state=seed, weight="weight")


def pairwise_stability(partitions: list[dict], nodes) -> dict:
    """S(u,v) = co-cluster fraction across runs. Returns the low/high/robust sets + the matrix summary."""
    ids = sorted(n.c1_id for n in nodes)
    co = {i: {} for i in ids}
    runs = len(partitions)
    for part in partitions:
        # map each node's community once; then co-occurrence per pair
        for a in ids:
            for b in ids:
                if a < b and part.get(a) == part.get(b):
                    co[a][b] = co[a].get(b, 0) + 1
    unstable = []   # 0.4 < S < 0.6 (boundary)
    robust = []     # S >= 0.9
    separate = []   # S == 0
    for a in ids:
        for b in co[a]:
            s = co[a][b] / runs
            if s >= 0.9:
                robust.append((a, b, round(s, 2)))
            elif 0.4 < s < 0.6:
                unstable.append((a, b, round(s, 2)))
            elif s == 0:
                separate.append((a, b, 0.0))
    return {"runs": runs, "n_robust_pairs": len(robust), "n_unstable_pairs": len(unstable),
            "n_separate_pairs": len(separate),
            "robust": robust[:40], "unstable": unstable[:40], "separate_count": len(separate)}


def contingency(partition: dict, kc: dict) -> dict:
    """For each Louvain community, the k-core-number distribution of its members."""
    comms = {}
    for n, c in partition.items():
        comms.setdefault(c, []).append(n)
    out = {}
    for c, members in comms.items():
        dist = {}
        for m in members:
            k = kc["core_numbers"].get(m, {}).get("core_number", 0)
            dist[str(k)] = dist.get(str(k), 0) + 1
        out[str(c)] = {"members": sorted(members), "core_distribution": dist}
    return out


def main() -> int:
    nodes = load_c1_nodes()
    kc = core_hierarchy(nodes)

    # 1) stability across seeds (in-process)
    parts = [run_partition(nodes, s) for s in range(N_SEEDS)]
    n_comms = [len({c for c in p.values()}) for p in parts]
    stab = pairwise_stability(parts, nodes)

    # 2) one representative partition for the contingency + a couple of insertion-order runs
    rep = parts[0]
    perm_parts = [run_partition(nodes, s, permute=True) for s in (3, 11, 23)]
    perm_stab = pairwise_stability(perm_parts, nodes)

    result = {
        "experiment": "PATALA.GRAPH.LOUVAIN_STABILITY.v0",
        "representation": "see_also_1.0+key_term_0.5xjaccard_min0.3_nobody (frozen, same as k-core)",
        "k_core_graph_hash": kc["graph_hash"],
        "louvain": {
            "seeds": N_SEEDS,
            "n_communities_min": min(n_comms), "n_communities_max": max(n_comms),
            "n_communities_set": sorted(set(n_comms)),
        },
        "pairwise_co_membership_stability": stab,
        "insertion_order_stability": perm_stab,
        "k_core_x_louvain_contingency": contingency(rep, kc),
        "note": ("k-core = STRUCTURAL embeddedness (deterministic). Louvain = modularity heuristic; "
                 "S(u,v) unstable (~0.5) pairs mark modularity-degenerate boundaries to compare against "
                 "the k-shell structure. Neither is a theme; none of this claims philosophical centrality."),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"LOUVAIN STABILITY (P-019 v2 ablation) over {len(nodes)} C1s, {N_SEEDS} seeds")
    print(f"  n_communities: min={result['louvain']['n_communities_min']} "
          f"max={result['louvain']['n_communities_max']} set={result['louvain']['n_communities_set']}")
    s = stab
    print(f"  pairwise co-membership: robust(S>=0.9)={s['n_robust_pairs']} "
          f"unstable(0.4<S<0.6)={s['n_unstable_pairs']} separate(S==0)={s['n_separate_pairs']}")
    print(f"  unstable boundaries (first 10): {[(a,b,v) for a,b,v in s['unstable'][:10]]}")
    print(f"  k_core_x_louvain contingency: {len(result['k_core_x_louvain_contingency'])} communities")
    print(f"  written: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
