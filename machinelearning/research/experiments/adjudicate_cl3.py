#!/usr/bin/env python3
"""adjudicate_cl3.py — build the CL-3 adjudication package (human review → accepted).

The gold chain (CL-3) currently demonstrates AUTOMATION (machine proposals). To make it
SCHOLARSHIP, a human must ACCEPT (or modify) the theme + argument. This produces a decision
record that a human reviews and signs:

  data/published/ipvv/adjudication-cl3.json

It assembles everything the reviewer needs: the cluster → proposed theme → proposed argument →
the certificate → the load-bearing passages with their L0 proof status → the specific ACCEPT/
MODIFY decisions.

This is the 'human-in-the-loop' step the zoom-out review identified as the real next milestone.
"""
from __future__ import annotations
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.c1corpus import load_c1_nodes
from patala_ml.builders import build_struct
from patala_ml.essayplan import plan_from_argument


def main():
    themes = json.load(open("/root/projects/patala/data/published/ipvv/clusters.json"))["clusters"]
    theme = next(t for t in themes if t["cluster_id"] == "CL-3")
    members = theme["member_c1_ids"]
    c1nodes = load_c1_nodes()

    # the winning builder's argument + the EssayPlan
    arg = build_struct(members, c1nodes, "pt:argument:ipvv:CL-3", "ipvv", "Order-less Support")
    plan = plan_from_argument(arg, "Order-less Support", "ipvv")

    # load the gold-chain certificate
    gc = json.load(open("/root/projects/patala/data/published/ipvv/goldchain-cl3.json"))
    cert = gc["certificate"]

    # per-member C1 one-liners (what the reviewer is asked to validate)
    by_id = {c.c1_id: c for c in c1nodes}
    member_cards = []
    for m in members:
        c = by_id.get(m)
        member_cards.append({
            "c1_id": m,
            "title": c.c1_id if c else m,
            "key_terms": (c.terms[:4] if c else []),
            "see_also": (c.see_also[:4] if c else []),
        })

    # the decision record
    record = {
        "adjudication_id": "adj:ipvv:cl3",
        "theme_id": "CL-3",
        "proposed_theme": {
            "label": "Order-less Support / the order-less knower",
            "members": members,
            "core_claim": "The powers have an order-less, infinite-consciousness support, which is the great Lord.",
            "certificate": cert,
        },
        "proposed_argument": {
            "argument_id": arg.argument_id,
            "title": arg.title,
            "kind": arg.kind,
            "inference_scheme": arg.inference_scheme,
            "n_premises": len(arg.members),
            "aggregate_strength": arg.aggregate_strength,
        },
        "essay_plan": {
            "plan_id": plan.plan_id,
            "thesis": plan.thesis,
            "n_claims": len(plan.claims),
            "claim_previews": [c.text[:70] for c in plan.claims[:5]],
        },
        "member_cards": member_cards,
        "decisions_required": [
            {
                "id": "D-THEME-ACCEPT",
                "question": "Accept CL-3 as the theme 'Order-less Support'?",
                "options": ["ACCEPT", "MODIFY (rename / adjust members)", "REJECT"],
                "default": "ACCEPT",
            },
            {
                "id": "D-ARG-ACCEPT",
                "question": "Accept the B-STRUCT argument (9 premises, scheme entailment)?",
                "options": ["ACCEPT", "MODIFY (edit premises)", "REJECT"],
                "default": "ACCEPT",
            },
            {
                "id": "D-LEXICAL-OPEN",
                "question": "LEXICAL_SENSE is OPEN (V2-O has 134 ambiguous tokens). Approve proceeding with this as a known crux?",
                "options": ["APPROVE_AS_OPEN", "RESOLVE_FIRST"],
                "default": "APPROVE_AS_OPEN",
            },
        ],
        "status": "AWAITING_REVIEW",
        "reviewed_by": None,
        "reviewed_at": None,
        "created_at": datetime.utcnow().isoformat(),
    }

    out = "/root/projects/patala/data/published/ipvv/adjudication-cl3.json"
    with open(out, "w") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    print(f"wrote {out}")
    print(f"\n=== CL-3 ADJUDICATION PACKAGE (AWAITING HUMAN REVIEW) ===")
    print(f"proposed theme: {record['proposed_theme']['label']} ({len(members)} members)")
    print(f"argument: {arg.title} [{arg.kind}] {len(arg.members)} premises")
    print(f"essay thesis: {plan.thesis[:80]}...")
    print(f"\ncertificate: {json.dumps(cert, separators=(',', ':'))}")
    print(f"\ndecisions required: {[d['id'] for d in record['decisions_required']]}")
    print("\nA human reviews + signs this → the gold chain becomes scholarship, not automation.")


if __name__ == "__main__":
    main()
