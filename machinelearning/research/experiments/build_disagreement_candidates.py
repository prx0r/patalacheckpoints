#!/usr/bin/env python3
"""build_disagreement_candidates.py — extract commitment-sensitive disagreement CANDIDATES.

The graph-aware viruddha NOMINATES cross-argument tension candidates. These are NOT settled
disagreements — they are candidates requiring semantic review. We classify them by the commitment
types of the two sides (so a reconstruction vs an assertion is NOT the same as two assertions), and
NEVER emit settled fact.

Commitment pools:
  TEXTUALLY_COMMITTED : ASSERTS, SIDDHANTA        (the text's own asserted position)
  DERIVED             : DERIVES                   (derived, but from the text)
  RECONSTRUCTED       : RECONSTRUCTED             (our reconstruction — NOT independently established)

Candidate classes (the relation type):
  ASSERTS <-> ASSERTS      -> STRONG_DISAGREEMENT_CANDIDATE
  ASSERTS <-> DERIVES      -> DISAGREEMENT_CANDIDATE
  DERIVES <-> DERIVES      -> INFERENCE_TENSION_CANDIDATE
  anything <-> RECONSTRUCTED -> RECONSTRUCTION_TENSION_CANDIDATE

Eligibility for T3/T4 benchmark status is a SEPARATE gate (source spans resolve + commitment known +
scope/modality/speaker compared + independent published evidence if available). This extractor only
produces detector findings (candidates), never fixtures. The output goes to benchmarks/v0/disagreements/.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from patala_ml.gold import build_gold_v0
from patala_ml.gold002 import build_gold_002
from patala_ml.gold003 import build_gold_003
from patala_ml.gold004 import build_gold_004
from patala_ml.gold005 import build_gold_005
from patala_ml.nyayagate import check_viruddha_graph

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))

GOLDS = {"ARG-GOLD-001": build_gold_v0, "ARG-GOLD-002": build_gold_002,
         "ARG-GOLD-003": build_gold_003, "ARG-GOLD-004": build_gold_004,
         "ARG-GOLD-005": build_gold_005}

# commitment -> pool
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
    if "DERIVED" in (left_pool, right_pool):
        # one side derived -> weaker
        if left_pool == "DERIVED" and right_pool == "DERIVED":
            return "INFERENCE_TENSION_CANDIDATE"
        return "DISAGREEMENT_CANDIDATE"
    return "DISAGREEMENT_CANDIDATE"


def main() -> int:
    all_nodes = {}
    for gid, fn in GOLDS.items():
        all_nodes[gid] = [(n, comm(n)) for n in fn()["nodes"]]

    findings = []
    for gid, nodes in all_nodes.items():
        for n, c in nodes:
            if n.get("kind") != "CONCLUSION":
                continue
            if POOL.get(c) is None:
                continue  # opponent-attributed / unknown commitments are not the text's position
            claim = {"claim_id": f"{gid}:{n.get('proposition_id', n.get('id'))}",
                     "claim_text": txt(n), "pramana": "anumana"}
            for other_gid, other_nodes in all_nodes.items():
                if other_gid == gid:
                    continue
                for p, pc in other_nodes:
                    if POOL.get(pc) is None:
                        continue
                    hits = check_viruddha_graph(claim, [p])
                    if hits:
                        hit = hits[0]
                        md = (hit.defeater_metadata or {})
                        findings.append({
                            "fixture_id": f"T3-DISAGREE-{len(findings)+1:03d}",
                            "status": "MACHINE_DISCOVERED_CANDIDATE",
                            "left": {
                                "argument_id": gid,
                                "proposition_id": n.get("proposition_id", n.get("id")),
                                "commitment": c,
                                "pool": POOL.get(c),
                                "text": txt(n),
                                "source_refs": [],
                            },
                            "right": {
                                "argument_id": other_gid,
                                "proposition_id": p.get("proposition_id", p.get("id")),
                                "commitment": pc,
                                "pool": POOL.get(pc),
                                "text": txt(p),
                                "source_refs": [],
                            },
                            "detected_relation": "VIRUDDHA_CANDIDATE",
                            "candidate_class": classify(POOL.get(c), POOL.get(pc)),
                            "detector": {"name": "check_viruddha_graph", "version": "graph-v1"},
                            "semantic_status": "UNRESOLVED",
                            "overlap_basis": md.get("overlap_basis", []),
                            "possible_defeaters": md.get("possible_defeaters", []),
                            "note": "machine-discovered tension CANDIDATE, not a settled disagreement; "
                                    "requires semantic review + the T3/T4 eligibility gate before it can "
                                    "become a benchmark fixture",
                        })

    out_dir = os.path.join(ROOT, "benchmarks/v0/disagreements")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "cross-gold-candidates.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"candidates": findings}, f, indent=2)

    # summary by class
    from collections import Counter
    by_class = Counter(f["candidate_class"] for f in findings)
    print(f"DISAGREEMENT CANDIDATES (machine-discovered, NOT settled): {len(findings)}")
    for cls, cnt in by_class.items():
        print(f"  {cls}: {cnt}")
    print(f"\nwritten: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
