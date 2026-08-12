#!/usr/bin/env python3
"""build_vertical_object.py — build ONE vertical object v0 (the reviewer's gate #3, hardened).

Serializes a single gold proposition with every edge TYPED and every resolution level honest.
GOLD grounding uses EXACT L0 ids (no fuzzy search); broad term search is only `candidate_context`.
Proof resolution is real (artifact looked up by chunk), not a caller-supplied id treated as resolved.

Run: cd research && . .venv/bin/activate && python experiments/build_vertical_object.py
"""
from __future__ import annotations
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.gold import build_gold_v0, V2O_PROOF_ID
from patala_ml.vertical import build_vertical


def main():
    gold = build_gold_v0()
    chunk = "chunkV2-O-saptamo-vimarsa"
    # EXACT gold grounding: the specific L0 records that ground G-TC2 (no search).
    grounding_refs = [
        f"{chunk}:L32:T114",  # pratibhā
        f"{chunk}:L32:T115",  # tattatpadārthakramarūṣitā (bears the order)
        f"{chunk}:L33:T116",  # akramānantacidrūpaḥ (order-less infinite form)
        f"{chunk}:L44:T181",  # rūṣitā (seasoned)
    ]
    key_terms = ["pratibhā", "rūṣitā", "akrama"]  # discovery/context only, not evidence
    l2_name = "pilot_V2O_L2_read.md"
    # EXACT C1/L2 spans (manually selected for this case) — upgrade those edges to SPAN_LEVEL.
    c1_span = "the flashing that runs through the ordered word-objects, seasoned with their order, touched by it — but itself not ordered."
    l2_span = "The flashing itself is not ordered."

    v = build_vertical(gold, "G-TC2", grounding_refs, l2_name, V2O_PROOF_ID,
                       key_terms=key_terms, c1_span=c1_span, l2_span=l2_span,
                       authoritative_proof_version="P0 35/35 (frozen)")

    print("VERTICAL OBJECT v0 — one proposition, every edge typed\n")
    print(f"object: {v['object_id']}  version={v['version']}")
    print(f"RESEARCH QUESTION: {v['research_question']}")
    print(f"ARGUMENT: {v['argument']['title']} [{v['argument']['structure']}]")
    print(f"INFERENCE(S): {[(i['inference_id'], i['proposition_role']) for i in v['inferences_using_proposition']]}")
    p = v["proposition"]
    print(f"PROPOSITION {p['proposition_id']}: {p['text']}  [commitment={p['commitment']} task_level={p['task_level']}]")
    print(f"C1: resolution={v['c1']['resolution']}  exact_span={v['c1']['exact_span']!r}")
    print(f"L2: resolution={v['l2']['resolution']}  exact_span={v['l2']['exact_span']!r}")
    print(f"DIRECT GROUNDING (exact refs):")
    for a in v["direct_grounding"]:
        print(f"   {a['l0_id']:<34} {a['sanskrit']}")
    print(f"UNRESOLVED ground refs: {v['unresolved_grounding_refs']}")
    print(f"CANDIDATE CONTEXT (discovery only): " +
          ", ".join(f"{t}:{len(a)}" for t, a in v["candidate_context"].items()))
    pp = v["philological_proof"]
    print(f"PROOF {pp['proof_id']}: resolution={pp['resolution']} status={pp['status']} "
          f"authoritative={pp['authoritative_version']} on_disk_PASS={pp['on_disk_PASS']}")
    print("\nLINKS (typed GroundingLinks):")
    for l in v["links"]:
        print(f"   {l['from']:<12} -[{l['relation']}/{l['resolution']}]-> {l['to']}" +
              (f"  ({l.get('status')})" if l.get("status") else ""))
    print(f"\nRESOLVED resolutions: {v['resolved_resolutions']}")
    print(f"UNRESOLVED resolutions: {v['unresolved_resolutions']}")

    os.makedirs("/root/projects/patala/benchmarks/v0/vertical", exist_ok=True)
    out = "/root/projects/patala/benchmarks/v0/vertical/vertical-v2o-g-tc2.json"
    json.dump(v, open(out, "w"), indent=2, ensure_ascii=False)
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
