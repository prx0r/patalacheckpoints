#!/usr/bin/env python3
"""build_vertical_object.py — build ONE vertical object (the reviewer's gate #3).

Serializes a single gold proposition all the way down:
    ResearchQuestion → Argument → Inference → Proposition → C1 → L2 → L0 anchor
    → SourceSpan → Sanskrit → PhilologicalProof
with every arrow resolved to real data (or honestly flagged UNRESOLVED).

This is also the `PHILOSOPHY-ENGINE-ARGUMENT-UNDER-INTERPRETATION.md` §23 task: it records where the
current IR schema can/cannot represent the scholarship cleanly. It CONSUMES the L0 floor; it does not
build or edit it (Agent 2's lane).

Run: cd research && . .venv/bin/activate && python experiments/build_vertical_object.py
"""
from __future__ import annotations
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.gold import build_gold_v0, V2O_PASSAGE_ID, V2O_PROOF_ID
from patala_ml.vertical import build_vertical


def main():
    gold = build_gold_v0()
    # G-TC2: "pratibhā is not itself constituted by that order (akrama — order-less)."
    # The key Sanskrit terms that ground this proposition:
    key_terms = ["pratibhā", "rūṣitā", "akrama"]
    l2_name = "pilot_V2O_L2_read.md"

    v = build_vertical(gold, "G-TC2", key_terms, l2_name, V2O_PROOF_ID)

    print("VERTICAL OBJECT — one proposition resolved downward\n")
    print(f"object: {v['object_id']}  (gold {v['gold_id']})\n")
    print(f"RESEARCH QUESTION: {v['research_question']}")
    print(f"ARGUMENT: {v['argument']['title']} [{v['argument']['structure']}]")
    print(f"INFERENCE(S) using G-TC2: {[i['inference_id'] for i in v['inferences_using_proposition']]}")
    p = v["proposition"]
    print(f"PROPOSITION {p['proposition_id']} [{p['kind']}/{p['explicitness']}/{p['commitment']}/{p['task_level']}]: {p['text']}")
    print(f"C1: {v['c1']['c1_id']}  excerpt: {v['c1']['excerpt'][:140]}...")
    print(f"L2: {v['l2']['l2_id']}  excerpt: {v['l2']['excerpt'][:140]}...")
    print("L0 ANCHORS (term -> Sanskrit spans):")
    for term, anchors in v["l0_anchors"].items():
        for a in anchors:
            print(f"   {term:<10} {a['l0_id']:<28} lemma={a['lemma_iast']:<40} span=[{a['source_span']['line']}:{a['source_span']['char_start']}-{a['source_span']['char_end']}]  Skt={a['sanskrit']}")
    print("SANSKRIT SPANS:", v["sanskrit_spans"])
    pp = v["philological_proof"]
    sha = (pp["source_sha256"] or "n/a")[:12] if pp["source_sha256"] else "n/a"
    print(f"PHILOLOGICAL PROOF {pp['proof_id']}: sha={sha}... unknown={pp['coverage_unknown']} roundtrip={pp['roundtrip']} PASS={pp['PASS']}")
    print(f"\nRESOLVED: {v['resolved_arrows']}")
    print(f"UNRESOLVED: {v['unresolved_arrows']}")

    # record the schema-gap notes (per §23)
    gaps = []
    if not v["research_question"]:
        gaps.append("research_question not first-class on ARG-001 (only on 003/004/005)")
    if not v["l0_anchors"].get("akrama"):
        gaps.append("'akrama' has no standalone L0 lemma token — it lives inside the compound kramākramādi; a term→L0 matcher must handle compounds (or the proposition needs explicit l0_anchor refs)")
    if not v["philological_proof"]["PASS"]:
        gaps.append("on-disk proof for this chunk is not the frozen 35/35 P0 (older record); authoritative proof_id referenced")
    v["schema_gaps"] = gaps
    print("\nSCHEMA GAPS (where the IR doesn't yet represent this cleanly):")
    for g in gaps:
        print(f"  - {g}")

    os.makedirs("/root/projects/patala/benchmarks/v0/vertical", exist_ok=True)
    out = "/root/projects/patala/benchmarks/v0/vertical/vertical-v2o-g-tc2.json"
    json.dump(v, open(out, "w"), indent=2, ensure_ascii=False)
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
