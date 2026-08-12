"""patala_ml/kcore.py — P-019 v2: deterministic STRUCTURAL k-core hierarchy over the C1 evidence graph.

This is NOT a semantic clustering replacement. It is a deterministic structural decomposition that answers
"how deeply embedded is each C1 in a densely connected graph region?" — a graph statistic, not a claim about
philosophical similarity.

  k-core != theme.
  core_number == structural fact.   (not "this is the central philosophical concept")
  cluster proposal == MACHINE PROPOSAL.
  theme interpretation == INTERPRETIVE CLAIM.
  AcceptedTheme == ADJUDICATED OBJECT.

Representation is preserved EXACTLY from cluster.py (curated see_also w=1.0 + KEY-TERM overlap w=0.5*Jaccard,
min 0.3, body-text excluded, edge_evidence persisted) so the Louvain-vs-k-core ablation is a clean one
(identical graph G, different algorithm).

Output is deterministic: same graph (up to node/edge insertion order and separate processes) ->
byte-identical canonical proposal (ignoring run-id/timestamps). Verified by canonical_hash + a cross-process /
order-perturbation test.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

import networkx as nx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patala_ml.cluster import build_hybrid_graph_c1, c1_id_from_chunk


REPRESENTATION_VERSION = "see_also_1.0+key_term_0.5xjaccard_min0.3_nobody"
METHOD = "K_CORE"
DETECTOR_ID = "PATALA.GRAPH.STRUCTURAL_K_CORE.v1"


def canonical_serialization(g: nx.Graph) -> str:
    """A canonical, insertion-order-independent serialization of the graph.

    - nodes sorted lexicographically
    - edges sorted, each undirected edge represented endpoint-sorted
    - weights normalized (float -> rounded) so cross-platform float noise is absorbed
    """
    nodes = sorted(g.nodes)
    edges = []
    for a, b, data in g.edges(data=True):
        ea, eb = (a, b) if a <= b else (b, a)
        edges.append((ea, eb, round(float(data.get("weight", 1.0)), 6)))
    edges.sort()
    blob = json.dumps({"nodes": nodes, "edges": edges}, sort_keys=True, separators=(",", ":"))
    return blob


def canonical_hash(g: nx.Graph) -> str:
    """SHA-256 of the canonical serialization. H(G1)=H(G2) => f(G1)=f(G2) for the structural decomposition."""
    return hashlib.sha256(canonical_serialization(g).encode("utf-8")).hexdigest()


def _structural_role(n: str, core: dict, g: nx.Graph) -> str:
    """CORE if n is at its component's max core number; PERIPHERAL if core==1; else SHELL."""
    comp = next(cc for cc in nx.connected_components(g) if n in cc)
    max_in_comp = max(core[m] for m in comp)
    if core[n] == max_in_comp:
        return "CORE"
    if core[n] <= 1:
        return "PERIPHERAL"
    return "SHELL"


def core_hierarchy(c1nodes, *, w_seealso: float = 1.0, w_terms: float = 0.5,
                   min_term_jaccard: float = 0.3) -> dict:
    """Deterministic structural k-core hierarchy over the C1 evidence graph (representation preserved).

    Returns a CoreStructureProposal: graph_hash, core_distribution, nested levels (k-cores + components),
    per-C1 {core_number, shell, component_id, structural_role}, edge_evidence, and the Louvain baseline.
    """
    g = build_hybrid_graph_c1(c1nodes, w_seealso=w_seealso, w_terms=w_terms,
                              min_term_jaccard=min_term_jaccard)
    if len(g.nodes) == 0:
        return {"method": METHOD, "deterministic": True, "graph_hash": canonical_hash(g),
                "core_distribution": {}, "levels": [], "core_numbers": {}, "edge_evidence": []}

    core = nx.core_number(g)
    max_core = max(core.values(), default=0)

    # nested k-core hierarchy: level k = induced subgraph on nodes with core_number >= k
    levels = []
    for k in range(1, max_core + 1):
        nodes_k = [n for n, c in core.items() if c >= k]
        comps = [sorted(cc) for cc in nx.connected_components(g.subgraph(nodes_k))]
        levels.append({"level": k, "n_nodes": len(nodes_k), "components": comps})

    # per-C1 record: core_number, shell, component_id (in the full graph), structural_role
    # component ids are made INSERTION-ORDER-INVARIANT by sorting components by their smallest node
    comps = [sorted(cc) for cc in nx.connected_components(g)]
    comps_sorted = sorted(comps, key=lambda c: (c[0], tuple(c)))
    comp_id = {c: i for i, comp in enumerate(comps_sorted) for c in comp}
    core_numbers = {}
    for n in g.nodes:
        core_numbers[n] = {
            "core_number": core[n],
            "shell": core[n],
            "component_id": comp_id[n],
            "structural_role": _structural_role(n, core, g),
        }

    # edge_evidence (persisted reasons) — within-core edges for the max core level
    evidence = []
    core_nodes = {n for n, c in core.items() if c == max_core} if max_core > 0 else set()
    for a, b, data in g.edges(data=True):
        if a in core_nodes and b in core_nodes:
            evidence.append({"a": a, "b": b, "type": data.get("type", "edge"),
                             "weight": round(float(data.get("weight", 1.0)), 6)})
    evidence.sort(key=lambda e: (e["a"], e["b"]))

    return {
        "method": METHOD,
        "deterministic": True,
        "detector_id": DETECTOR_ID,
        "representation_version": REPRESENTATION_VERSION,
        "graph_hash": canonical_hash(g),
        "core_distribution": {str(k): sum(1 for c in core.values() if c == k)
                              for k in sorted(set(core.values()))},
        "max_core": max_core,
        "levels": levels,
        "core_numbers": core_numbers,
        "edge_evidence": evidence,
        "note": ("k-core is a STRUCTURAL FACT (embeddedness); it is NOT a theme. It is a proposal, "
                 "not an AcceptedTheme. Do not infer 'high core_number => philosophically central'."),
    }


def louvain_baseline(c1nodes, *, seed: int = 42) -> dict:
    """Louvain partition over the SAME evidence graph — kept as the ablation/comparison baseline (not deleted).

    Requires python-louvain (`community`); if it is not installed, returns an explicit
    UNAVAILABLE record so the deterministic k-core result does not depend on it.
    """
    try:
        import community
    except ImportError:
        return {"method": "LOUVAIN", "seed": seed, "status": "UNAVAILABLE",
                "reason": "python-louvain (community) not installed in this python"}
    g = build_hybrid_graph_c1(c1nodes)
    partition = community.best_partition(g, random_state=seed, weight="weight")
    comms = {}
    for n, c in partition.items():
        comms.setdefault(c, []).append(n)
    return {"method": "LOUVAIN", "seed": seed, "status": "OK",
            "communities": {str(k): sorted(v) for k, v in comms.items()}}


if __name__ == "__main__":
    from patala_ml.c1corpus import load_c1_nodes
    nodes = load_c1_nodes()
    r = core_hierarchy(nodes)
    print(f"P-019 v2 K-CORE over {len(nodes)} C1s: max_core={r['max_core']}")
    print(f"  graph_hash: {r['graph_hash'][:12]}…")
    print(f"  core_distribution: {r['core_distribution']}")
    print(f"  structural roles: CORE={sum(1 for v in r['core_numbers'].values() if v['structural_role']=='CORE')} "
          f"SHELL={sum(1 for v in r['core_numbers'].values() if v['structural_role']=='SHELL')} "
          f"PERIPHERAL={sum(1 for v in r['core_numbers'].values() if v['structural_role']=='PERIPHERAL')}")
