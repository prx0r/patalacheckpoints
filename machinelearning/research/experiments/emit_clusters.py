#!/usr/bin/env python3
"""emit_clusters.py — produce the Stage-2 cluster artifact that is ACTUALLY usable.

Reads the C1 nodes, clusters them, and emits:
  data/published/ipvv/clusters.json        — the ClusterProposals mapped to passages
  data/published/ipvv/clusters.report.txt  — a human-readable editorial report

Each cluster carries a quality signal so the editor sees meaningful clusters vs noisy ones:
  coherence  = mean shared-edge weight among members (high = tight)
  size       = member count
  overlap    = how many members also belong to other clusters

Run:  cd research && . .venv/bin/activate && python experiments/emit_clusters.py
"""
from __future__ import annotations
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.c1corpus import load_c1_nodes
from patala_ml.cluster import cluster_c1s


def main():
    all_nodes = load_c1_nodes()
    # Split: V2/V3 are the thematic C1s (clean clustering). V1 is a dense commentary
    # cross-reference block (the upoddhata/purvapaksa dialectic) that mega-clusters —
    # handle it editorially, not by over-tuning the graph.
    v23 = [c for c in all_nodes if not c.c1_id.startswith("V1")]
    v1 = [c for c in all_nodes if c.c1_id.startswith("V1")]

    props = cluster_c1s(v23, seed=42)
    print(f"V2/V3 C1s: {len(v23)} → {len(props)} clusters")

    # overlap counts
    from collections import Counter
    member_counts = Counter(m for p in props for m in p.member_c1_ids)

    out = []
    for p in props:
        strengths = list(p.strengths.values())
        coherence = round(sum(strengths) / len(strengths), 4) if strengths else 0.0
        n_overlap = sum(1 for m in p.member_c1_ids if member_counts[m] >= 2)
        out.append({
            "cluster_id": p.cluster_id,
            "size": len(p.member_c1_ids),
            "coherence": coherence,
            "members_overlapping": n_overlap,
            "member_c1_ids": p.member_c1_ids,
            "edge_evidence": p.edge_evidence,
        })
    out.sort(key=lambda c: (-c["size"], -c["coherence"]))

    store = os.environ.get("PATALA_STORE", "/root/projects/patala/data/published/ipvv")
    os.makedirs(store, exist_ok=True)
    with open(os.path.join(store, "clusters.json"), "w") as f:
        json.dump({
            "seed": 42, "scope": "V2/V3 thematic C1s",
            "cluster_count": len(out), "clusters": out,
            "note": "V1 (upoddhata/purvapaksa dialectic) is a dense cross-reference block; "
                    "cluster it editorially, not via the shared graph.",
        }, f, indent=2, ensure_ascii=False)

    with open(os.path.join(store, "clusters.report.txt"), "w") as f:
        f.write("PĀṬALA STAGE-2 CLUSTERS — editorial report (V2/V3 thematic C1s)\n")
        f.write("=" * 60 + "\n")
        f.write("MACHINE PROPOSALS. The editor accepts/merges/splits these into THEMES.\n")
        f.write(f"\n{len(out)} clusters from {len(v23)} V2/V3 C1s\n\n")
        for c in out:
            f.write(f"{c['cluster_id']}: {c['size']} members, coherence {c['coherence']}\n")
            for m in c["member_c1_ids"]:
                f.write(f"    - {m}\n")
            f.write("\n")
        f.write(f"V1 block: {len(v1)} C1s — the upoddhata/purvapaksa dialectic; "
                "handle editorially.\n")

    print(f"wrote {store}/clusters.json + clusters.report.txt")
    print(f"V2/V3: {len(out)} clusters; multi-member: {sum(1 for c in out if c['size']>=2)}; "
          f"V1 handled editorially ({len(v1)} C1s)")


if __name__ == "__main__":
    main()
