#!/usr/bin/env python3
"""build_kcore_structure.py — P-019 v2: deterministic STRUCTURAL k-core hierarchy proposal (write artifact).

Runs the k-core decomposition over the real C1 evidence graph (representation preserved from cluster.py),
writes the CoreStructureProposal, and records the Louvain baseline for comparison. The output is a
STRUCTURAL PROPOSAL (graph statistic), NOT an AcceptedTheme.

Run:  python3 experiments/build_kcore_structure.py [--out <path>] [--hash]
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patala_ml.c1corpus import load_c1_nodes
from patala_ml.kcore import core_hierarchy, louvain_baseline

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
OUT = os.path.join(ROOT, "benchmarks/v0/structural/kcore-ipvv-c1-v0.json")


def _comparison(kc: dict, louvain: dict) -> dict:
    """Juxtapose the two clusterings so their outcomes can be compared and synthesized for comprehensiveness.

    Neither is authoritative: k-core = structural embeddedness (deterministic fact); Louvain = modularity
    community (heuristic). A 'synthesis' is an inspection aid, never an AcceptedTheme.
    """
    kc_roles = {}
    for n, v in kc["core_numbers"].items():
        kc_roles.setdefault(v["structural_role"], []).append(n)
    louvain_comms = louvain.get("communities", {})
    return {
        "method_note": ("k-core = STRUCTURAL embeddedness (deterministic fact); Louvain = modularity "
                        "community (heuristic). Both are PROPOSALS; compare, do not conflate with theme."),
        "k_core": {
            "max_core": kc.get("max_core"),
            "core_distribution": kc.get("core_distribution"),
            "top_core_c1s": sorted(kc_roles.get("CORE", [])),
            "n_shells": len(kc.get("levels", [])),
        },
        "louvain": {
            "n_communities": len(louvain_comms),
            "status": louvain.get("status", "OK"),
            "communities": louvain_comms,
        },
        "synthesis": {
            "which_c1s_are_most_densely_embedded": sorted(kc_roles.get("CORE", [])),
            "which_louvain_communities_exist": [sorted(m) for m in louvain_comms.values()],
            "note": ("Cross-check which k-core shells and Louvain communities overlap; the overlap is "
                     "an inspection aid only. High core_number == density under representation R, "
                     "NOT 'philosophically central'."),
        },
    }


def build() -> dict:
    c1nodes = load_c1_nodes()
    r = core_hierarchy(c1nodes)
    lb = louvain_baseline(c1nodes)
    r["louvain_baseline"] = lb
    r["comparison"] = _comparison(r, lb)
    return r


def main() -> int:
    out = OUT
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    r = build()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(r, f, indent=2)
    print(f"P-019 v2 K-CORE structural proposal over {len(r['core_numbers'])} C1s")
    print(f"  max_core: {r['max_core']} | core_distribution: {r['core_distribution']}")
    print(f"  graph_hash: {r['graph_hash'][:16]}…")
    print(f"  written: {out}")
    if "--hash" in sys.argv:
        print(f"  CANONICAL_HASH={r['graph_hash']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
