#!/usr/bin/env python3
"""tests/test_cluster.py — validate the Stage-2 clusterer against the SPEC.

Run:  cd research && . .venv/bin/activate && python tests/test_cluster.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.cluster import c1_id_from_chunk, cluster_c1s, build_hybrid_graph_c1
from patala_ml.c1corpus import load_c1_nodes

PASS = 0
FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        print(f"  ✓ {name}")
        PASS += 1
    else:
        print(f"  ✗ {name} {detail}")
        FAIL += 1


def main():
    c1nodes = load_c1_nodes()
    print(f"loaded {len(c1nodes)} C1 nodes")

    # 1. C1 id extraction
    print("\n== C1 loading ==")
    check("63 C1 nodes loaded", len(c1nodes) == 63, f"got {len(c1nodes)}")
    v1_nodes = [c for c in c1nodes if c.c1_id.startswith("V1")]
    check("V1 fine-grained C1s present (upoddhata/purvapaksa)", len(v1_nodes) >= 10,
          f"got {len(v1_nodes)}")
    check("every node has a body", all(c.body for c in c1nodes))

    # 2. hybrid graph builds
    print("\n== hybrid graph ==")
    g = build_hybrid_graph_c1(c1nodes)
    check("graph has nodes", len(g.nodes) > 0)
    check("graph has edges", len(g.edges) > 0)
    edge_types = set(g[u][v].get("type") for u, v in g.edges)
    print(f"     edge types: {edge_types}")

    # 3. clustering produces proposals
    print("\n== clustering ==")
    props = cluster_c1s(c1nodes, seed=42)
    check("proposals produced", len(props) > 0, f"got {len(props)}")
    all_members = [c for p in props for c in p.member_c1_ids]
    covered = set(all_members)
    all_ids = {c.c1_id for c in c1nodes}
    print(f"     covered: {len(covered & all_ids)}/{len(all_ids)} distinct C1 ids")
    multi = [p for p in props if len(p.member_c1_ids) > 1]
    print(f"     multi-member clusters: {len(multi)}")

    # 4. known clusters recovered (memory, causal, pramāṇa, vimarśa)
    print("\n== known-cluster recovery ==")
    def in_prop(short_id, prop):
        return any(m.startswith(short_id) or short_id in m for m in prop.member_c1_ids)
    mem = {"V2A", "V2B", "V2C"}
    caus = {"V3G", "V3H", "V3I"}
    pram = {"V2D", "V2E", "V3C"}
    vim = {"V2H", "V2I"}
    # each known neighborhood should have ≥2 of its members co-located in some cluster
    check("memory C1s co-locate (≥2 of V2A/B/C in one cluster)",
          any(sum(in_prop(x, p) for x in mem) >= 2 for p in props))
    check("causal C1s co-locate (≥2 of V3G/H/I in one cluster)",
          any(sum(in_prop(x, p) for x in caus) >= 2 for p in props))
    check("pramāṇa C1s co-locate (≥2 of V2D/E, V3C in one cluster)",
          any(sum(in_prop(x, p) for x in pram) >= 2 for p in props))
    check("vimarśa C1s co-locate (≥2 of V2H/I in one cluster)",
          any(sum(in_prop(x, p) for x in vim) >= 2 for p in props))

    # 5. overlap: at least 3 C1s appear in ≥2 clusters (multi-theme is real, not rare)
    print("\n== overlap (multi-theme) ==")
    from collections import Counter
    member_counts = Counter(m for p in props for m in p.member_c1_ids)
    multi = {m: c for m, c in member_counts.items() if c >= 2}
    print(f"     {len(multi)} C1s appear in ≥2 clusters: {list(multi)[:8]}")
    check("some C1s appear in ≥2 clusters (overlap)", len(multi) >= 3)
    v2o = [p for p in props if any(m.startswith("V2O") for m in p.member_c1_ids)]
    v2l = [p for p in props if any(m.startswith("V2L") for m in p.member_c1_ids)]
    print(f"     V2O in {len(v2o)} cluster(s); V2L in {len(v2l)} cluster(s)")
    check("V2L in ≥2 clusters (overlap)", len(v2l) >= 2)

    # 6. determinism
    print("\n== determinism ==")
    props2 = cluster_c1s(c1nodes, seed=42)
    check("same seed → same proposals", [p.cluster_id for p in props] == [p.cluster_id for p in props2])

    # 7. evidence trace
    print("\n== evidence trace ==")
    multi_props = [p for p in props if len(p.member_c1_ids) > 1]
    multi_w_ev = [p for p in multi_props if p.edge_evidence]
    check("multi-member clusters carry edge evidence", len(multi_w_ev) > 0)

    print(f"\n=== RESULT: {PASS} pass / {FAIL} fail ===")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
