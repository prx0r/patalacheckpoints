#!/usr/bin/env python3
"""build_essay.py — generate the CL-3 gold-chain essay (JSON canonical + markdown projection).

Pipeline: CL-3 accepted argument → EssayPlan → frozen EssayClaims → model-drafted sentences
(each licensed) → independent adversarial verification → JSON + markdown.

Run: cd research && . .venv/bin/activate && python experiments/build_essay.py
"""
from __future__ import annotations
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.c1corpus import load_c1_nodes
from patala_ml.builders import build_struct
from patala_ml.essayplan import plan_from_argument
from patala_ml.essaygen import generate_essay
from patala_ml.essayverify import verify_essay


def main():
    c1nodes = load_c1_nodes()
    themes = json.load(open("/root/projects/patala/data/published/ipvv/clusters.json"))["clusters"]
    theme = next(t for t in themes if t["cluster_id"] == "CL-3")
    members = theme["member_c1_ids"]

    # the accepted argument (B-STRUCT) + the EssayPlan
    arg = build_struct(members, c1nodes, "pt:argument:ipvv:CL-3", "ipvv", "Order-less Support")
    plan = plan_from_argument(arg, "Order-less Support", "ipvv")

    # generate the essay (JSON canonical)
    essay = generate_essay(plan, arg, "pt:essay:ipvv:CL-3", "The Order-less Support of the Powers")

    # independent adversarial verification
    verdict = verify_essay(essay)

    # write JSON (canonical) + markdown (projection)
    base = "/root/projects/patala/data/published/ipvv"
    with open(os.path.join(base, "essay-cl3.json"), "w") as f:
        json.dump(essay.to_dict(), f, indent=2, ensure_ascii=False)
    with open(os.path.join(base, "essay-cl3.md"), "w") as f:
        f.write(essay.to_markdown())

    print(f"=== CL-3 ESSAY ({len(essay.sentences)} sentences) ===")
    print(f"claims frozen: {len(essay.claims)} (incl. 1 conclusion + 1 QUALIFICATION)")
    print(f"plan_hash: {essay.plan_hash}")
    print(f"verification: {json.dumps(verdict['summary'])}")
    print("\n--- essay prose ---")
    for s in essay.sentences:
        tag = f"[{s.provenance_relation}]"
        print(f"{tag:14} {s.text[:80]}")
    print(f"\nwrote {base}/essay-cl3.json + essay-cl3.md")


if __name__ == "__main__":
    main()
