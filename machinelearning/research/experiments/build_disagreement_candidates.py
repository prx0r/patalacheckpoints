#!/usr/bin/env python3
"""build_disagreement_candidates.py — extract commitment-sensitive cross-argument tension CANDIDATES.

The graph-aware viruddha NOMINATES cross-argument tension candidates. These are NOT settled
disagreements — they are candidates requiring semantic review. We classify them by the commitment
types of the two sides and NEVER emit settled fact.

Commitment pools:
  TEXTUALLY_COMMITTED : ASSERTS, SIDDHANTA        (the text's own asserted position)
  DERIVED             : DERIVES                   (derived, but from the text)
  RECONSTRUCTED       : RECONSTRUCTED             (our reconstruction — NOT independently established)

Candidate classes:
  ASSERTS <-> ASSERTS      -> STRONG_DISAGREEMENT_CANDIDATE
  ASSERTS <-> DERIVES      -> DISAGREEMENT_CANDIDATE
  DERIVES <-> DERIVES      -> INFERENCE_TENSION_CANDIDATE
  anything <-> RECONSTRUCTED -> RECONSTRUCTION_TENSION_CANDIDATE

This scans ALL eligible established proposition pairs (not just conclusions) and deduplicates
symmetric pairs, so ASSERTS<->ASSERTS / DERIVES<->DERIVES classes are reachable.

Eligibility for T3/T4 benchmark status is a SEPARATE gate; this only produces detector findings
(candidates, never fixtures). The output goes to benchmarks/v0/disagreements/.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from patala_ml.gold import build_gold_v0
from patala_ml.gold002 import build_gold_002
from patala_ml.gold003 import build_gold_003
from patala_ml.gold004 import build_gold_004
from patala_ml.gold005 import build_gold_005
from patala_ml.nyayagate import check_viruddha_graph, VIRUDDHA_GRAPH_VERSION

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))

GOLDS = {"ARG-GOLD-001": build_gold_v0, "ARG-GOLD-002": build_gold_002,
         "ARG-GOLD-003": build_gold_003, "ARG-GOLD-004": build_gold_004,
         "ARG-GOLD-005": build_gold_005}

POOL = {"ASSERTS": "TEXTUALLY_COMMITTED", "SIDDHANTA": "TEXTUALLY_COMMITTED",
        "DERIVES": "DERIVED", "RECONSTRUCTED": "RECONSTRUCTED",
        "ASSERTS_FOR_ARGUMENT": "RECONSTRUCTED", "ATTRIBUTES_TO_OPPONENT": None}


def txt(n):
    return n.get("proposition") or n.get("text") or ""


def comm(n):
    return (n.get("commitment") or n.get("speaker") or "").upper()


def classify(left_pool, right_pool) -> str:
    if left_pool == "RECONSTRUCTED" or right_pool == "RECONSTRUCTED":
        return "RECONSTRUCTION_TENSION_CANDIDATE"
    if left_pool == "TEXTUALLY_COMMITTED" and right_pool == "TEXTUALLY_COMMITTED":
        return "STRONG_DISAGREEMENT_CANDIDATE"
    if left_pool == "DERIVED" and right_pool == "DERIVED":
        return "INFERENCE_TENSION_CANDIDATE"
    return "DISAGREEMENT_CANDIDATE"


def main() -> int:
    impl_sha = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True,
                              cwd=ROOT).stdout.strip() or "unknown"

    # gather ALL eligible propositions (any commitment in a pool), keyed by (arg_id, prop_id)
    all_established = {}  # (arg, prop) -> (node, pool)
    for gid, fn in GOLDS.items():
        for n in fn()["nodes"]:
            c = comm(n)
            pool = POOL.get(c)
            if pool is None:
                continue  # opponent-attributed / unknown -> not the text's position
            pid = n.get("proposition_id", n.get("id"))
            all_established[(gid, pid)] = (n, c, pool)

    # scan ALL eligible proposition pairs (both directions, dedup symmetric)
    seen_pairs = set()
    candidates = []
    keys = list(all_established)
    for i in range(len(keys)):
        for j in range(len(keys)):
            if i == j:
                continue
            (lg, lp), (rg, rp) = keys[i], keys[j]
            if (lg, lp, rg, rp) in seen_pairs or (rg, rp, lg, lp) in seen_pairs:
                continue
            # only cross-argument (different golds) pairs
            if lg == rg:
                continue
            left, lc, lpool = all_established[(lg, lp)]
            right, rc, rpool = all_established[(rg, rp)]
            claim = {"claim_id": f"{lg}:{lp}", "claim_text": txt(left), "pramana": "anumana"}
            hits = check_viruddha_graph(claim, [right])
            if hits:
                seen_pairs.add((lg, lp, rg, rp))
                h = hits[0]
                md = h.defeater_metadata or {}
                candidates.append({
                    "candidate_id": f"VIR-CAND-{len(candidates)+1:03d}",
                    "status": "MACHINE_DISCOVERED_CANDIDATE",
                    "left": {"argument_id": lg, "proposition_id": lp, "commitment": lc,
                             "pool": lpool, "text": txt(left)},
                    "right": {"argument_id": rg, "proposition_id": rp, "commitment": rc,
                              "pool": rpool, "text": txt(right)},
                    "detected_relation": "VIRUDDHA_CANDIDATE",
                    "candidate_class": classify(lpool, rpool),
                    "detector": {"id": "PATALA.VIRUDDHA.GRAPH.v2",
                                 "name": VIRUDDHA_GRAPH_VERSION,
                                 "implementation_sha": impl_sha},
                    "semantic_status": "UNRESOLVED",
                    "overlap_basis": md.get("overlap_basis", []),
                    "possible_defeaters": md.get("possible_defeaters", []),
                    "note": "machine-discovered tension CANDIDATE, not a settled disagreement; requires "
                            "semantic review + the T3/T4 eligibility gate before it can become a fixture",
                })

    out_dir = os.path.join(ROOT, "benchmarks/v0/disagreements")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "cross-gold-candidates.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"candidates": candidates}, f, indent=2)

    from collections import Counter
    by_class = Counter(c["candidate_class"] for c in candidates)
    print(f"DISAGREEMENT CANDIDATES (machine-discovered, NOT settled): {len(candidates)}")
    for cls, cnt in by_class.items():
        print(f"  {cls}: {cnt}")
    print(f"\nwritten: {out} (detector {VIRUDDHA_GRAPH_VERSION}, sha {impl_sha[:8]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
