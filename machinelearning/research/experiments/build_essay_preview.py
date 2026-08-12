#!/usr/bin/env python3
"""build_essay_preview.py — the machine pre-review of the reflexion-core essay (essay depends on the gate).

Consumes the connected pipeline (per the hermes PEER-REVIEW §7 'machine pre-review' + the Review
API 'review dossier'): an EssayPlan whose claims resolve to real ARG-002/004 propositions, with the
Nyāya gate run on each claim. The output is a 'review dossier':

  claim → grounded-in(gold proposition) → gate outcome → grounded / needs-review / underdetermined

This makes an essay actually DEPEND on the argument layer + the gate, instead of being disconnected
prose. Every claim points to a real gold proposition (proposition_id) and gets a gate verdict.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from patala_ml.gold002 import build_gold_002
from patala_ml.gold004 import build_gold_004
from patala_ml.essayplan import EssayPlan, EssayClaim
from patala_ml.nyayagate import gate_claim

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))


def txt(n):
    return n.get("proposition") or n.get("text") or ""


def main() -> int:
    g2 = build_gold_002()
    g4 = build_gold_004()
    props = {}
    for n in g2["nodes"]:
        props[n["proposition_id"]] = (txt(n), "ARG-GOLD-002", n.get("commitment"))
    for n in g4["nodes"]:
        props[n["proposition_id"]] = (txt(n), "ARG-GOLD-004", n.get("commitment"))

    plan = EssayPlan(
        plan_id="PLAN-REFLEXION-CORE", work_id="ipvv",
        theme="the reflexion-core / self-luminosity",
        thesis="The determination cannot establish externality; self-experience is self-luminous and self-contained.",
    )

    # the reflexion-core essay's load-bearing claims, each pointing to a REAL gold proposition
    plan.add_claim(
        "The determination (adhyavasāya) cannot establish an external object.",
        argument_id="ARG-GOLD-002", passage_ids=["pt:passage:ipvv:chunkM-jnanadhikara-reflexion-core.md"],
        role="supporting")
    plan.add_claim(
        "The I-reflexive-awareness is not a conceptual construction.",
        argument_id="ARG-GOLD-002", passage_ids=["pt:passage:ipvv:chunkV2-L-sastho-vimarsa-smrti-apohana.md"],
        role="supporting")
    plan.add_claim(
        "Manifestation without reflexive awareness (vimarśa) would be inert, like crystal.",
        argument_id="ARG-GOLD-004", passage_ids=["pt:passage:ipvv:chunkV2-H-pancamo-vimarsa-k11-13.md"],
        role="supporting")
    plan.add_claim(
        "What makes the light conscious is that it is aware of itself in manifesting.",
        argument_id="ARG-GOLD-004", passage_ids=["pt:passage:ipvv:chunkV2-H-pancamo-vimarsa-k11-13.md"],
        role="conclusion")

    # map each plan claim to the gold proposition it is grounded in, then run the gate
    claim_to_prop = {
        "PLAN-REFLEXION-CORE:c1": "G2-CONC",
        "PLAN-REFLEXION-CORE:c2": "G2-TC2",
        "PLAN-REFLEXION-CORE:c3": "G4-CRYSTAL",
        "PLAN-REFLEXION-CORE:c4": "G4-CONC",
    }

    dossier = []
    for claim in plan.claims:
        prop_id = claim_to_prop.get(claim.id)
        prop_text, arg_id, commitment = props.get(prop_id, ("(no gold prop)", "", ""))
        claim.grounded_in = {"proposition_id": prop_id, "argument_id": arg_id, "commitment": commitment}
        # run the gate on the claim (deterministic admissibility)
        gate = gate_claim({"claim_id": claim.id, "claim_text": claim.text,
                           "pramana": "anumana", "falsifier": {"type": "structural"},
                           "log_bayes_factor": 0.0}).to_dict()
        dossier.append({
            "claim_id": claim.id, "claim_text": claim.text, "role": claim.role,
            "grounded_in": {"proposition_id": prop_id, "argument_id": arg_id, "commitment": commitment},
            "gate_outcome": gate.get("outcome"),
            "can_update_posterior": gate.get("can_update_posterior"),
            "gate_failures": [f.get("fallacy") for f in gate.get("failures", [])],
        })

    result = {
        "plan_id": plan.plan_id,
        "thesis": plan.thesis,
        "review_dossier": dossier,
        "summary": {
            "grounded_claims": sum(1 for d in dossier if d["grounded_in"]["proposition_id"]),
            "gate_accepted": sum(1 for d in dossier if d["gate_outcome"] in ("accepted", "accepted_with_penalty")),
            "gate_needs_review": sum(1 for d in dossier if d["gate_outcome"] == "needs_review"),
            "note": "machine pre-review (hermes PEER-REVIEW §7). Claims resolve to real gold propositions; "
                    "gate decides admissibility. NOT scholarly validation.",
        },
    }

    out = os.path.join(ROOT, "benchmarks/v0/review/REFLEXION-CORE-ESSAY-PREVIEW.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("MACHINE PRE-REVIEW — the reflexion-core essay (claims depend on the golds + gate)")
    for d in dossier:
        print(f"  {d['claim_id']}: grounded={d['grounded_in']['proposition_id']} "
              f"gate={d['gate_outcome']} fails={d['gate_failures']}")
    print(f"  summary: {result['summary']['grounded_claims']} grounded, "
          f"{result['summary']['gate_accepted']} accepted, "
          f"{result['summary']['gate_needs_review']} needs-review")
    print(f"\nwritten: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
