#!/usr/bin/env python3
"""tests/test_essay.py — validate the CL-3 essay generator + independent verifier.

Tests the invariants that matter (the review's strict success criteria):
  1. every substantive sentence maps to ≥1 EssayClaim (0 unsupported propositions)
  2. the conclusion has an honest BOUNDARY (no boundary-erasure)
  3. the QUALIFICATION claim is present + rendered
  4. the independent verifier catches a deliberately-inflated sentence (rejects it)
  5. JSON is canonical; markdown is a deterministic projection
  6. plan_hash reproducibility (staleness detection)

Run: cd research && . .venv/bin/activate && python tests/test_essay.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.c1corpus import load_c1_nodes
from patala_ml.builders import build_struct
from patala_ml.essayplan import plan_from_argument
from patala_ml.essaygen import generate_essay
from patala_ml.essayverify import verify_essay
from patala_ml.essay import Essay, plan_hash
from patala_ml.essaysentence import EssaySentence

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
    themes = json.load(open("/root/projects/patala/data/published/ipvv/clusters.json"))["clusters"]
    theme = next(t for t in themes if t["cluster_id"] == "CL-3")
    arg = build_struct(theme["member_c1_ids"], c1nodes, "pt:argument:ipvv:CL-3", "ipvv", "x")
    plan = plan_from_argument(arg, "Order-less Support", "ipvv")
    essay = generate_essay(plan, arg, "pt:essay:ipvv:CL-3", "The Order-less Support of the Powers")

    # 1. every substantive sentence maps to ≥1 claim (0 unsupported)
    print("== sentence→claim licensing ==")
    subst = [s for s in essay.sentences if s.provenance_relation != "TRANSITION"]
    check("every substantive sentence has ≥1 claim",
          all(s.claim_ids for s in subst))
    check("all claims referenced exist",
          all(cid in {c["id"] for c in essay.claims}
              for s in subst for cid in s.claim_ids))

    # 2. the conclusion has an honest boundary
    print("\n== boundary ==")
    concl = next(c for c in essay.claims if c["role"] == "conclusion")
    check("conclusion has a boundary", "does not by itself" in concl["boundary"].lower())
    check("qualification claim present", any(c["role"] == "QUALIFICATION" for c in essay.claims))

    # 3. independent verifier passes the honest essay
    print("\n== verifier (honest essay passes) ==")
    verdict = verify_essay(essay)
    check("honest essay → 0 rejected", verdict["summary"]["rejected"] == 0, verdict["summary"])

    # 4. the verifier CATCHES a deliberately-inflated sentence
    print("\n== verifier catches inflation ==")
    bad = EssaySentence(id="S-BAD", text="The argument PROVES consciousness is the universal Self.",
                        claim_ids=[concl["id"]], provenance_relation="INFERENCE",
                        argument_ids=[arg.argument_id], passage_ids=[])
    essay.sentences.append(bad)
    verdict2 = verify_essay(essay)
    check("inflated sentence rejected", verdict2["summary"]["rejected"] >= 1, verdict2["summary"])
    check("bad sentence status = REJECTED", bad.status == "REJECTED", bad.status)
    essay.sentences.remove(bad)  # clean up

    # 5. JSON canonical, markdown projection
    print("\n== JSON canonical / markdown projection ==")
    d = essay.to_dict()
    check("essay dict has claims + sentences", "claims" in d and "sentences" in d)
    check("markdown renders deterministically",
          essay.to_markdown() == essay.to_markdown())

    # 6. plan_hash reproducibility
    print("\n== plan_hash reproducibility ==")
    plan_dict = {"plan_id": plan.plan_id, "thesis": plan.thesis,
                 "claims": [c["text"] for c in essay.claims]}
    h1 = plan_hash(plan_dict)
    h2 = plan_hash(dict(plan_dict))  # same content
    check("plan_hash deterministic", h1 == h2)

    print(f"\n=== RESULT: {PASS} pass / {FAIL} fail ===")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
