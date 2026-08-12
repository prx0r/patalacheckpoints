#!/usr/bin/env python3
"""tests/test_essayplan.py — the AIF graph + EssayPlan end-to-end (structural soundness).

Builds the winning B-STRUCT argument on a real theme, converts to an AIF-informed argument
graph, derives an EssayPlan, and validates REAL invariants (resolvability, node integrity,
no orphan claims) — NOT invented numeric scores.

Run: cd research && . .venv/bin/activate && python tests/test_essayplan.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.builders import build_struct
from patala_ml.c1corpus import load_c1_nodes
from patala_ml.aifgraph import ArgumentGraph, InfoNode, InferenceNode, ConflictNode
from patala_ml.essayplan import EssayPlan, plan_from_argument

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
    # the real theme CL-3 (order-less support / unity) — the ground-truth family
    themes = json.load(open("/root/projects/patala/data/published/ipvv/clusters.json"))["clusters"]
    theme = next(t for t in themes if t["cluster_id"] == "CL-3")
    members = theme["member_c1_ids"]

    # 1. build the winning B-STRUCT argument
    print("== B-STRUCT argument on CL-3 ==")
    arg = build_struct(members, c1nodes, "pt:argument:ipvv:CL-3", "ipvv", "Order-less Support")
    check("argument built", bool(arg.title))
    check("has premises", len(arg.members) >= 3, len(arg.members))

    # 2. convert to AIF-informed graph
    print("\n== AIF-informed argument graph ==")
    g = ArgumentGraph(argument_id=arg.argument_id, work_id="ipvv")
    # info nodes for each premise + the conclusion
    id_map = {}
    for i, m in enumerate(arg.members):
        nid = g.add_info(id=f"{arg.argument_id}:n{i}", text=m.text, role="premise",
                         passage_ids=[p for p in m.passage_ids if p])
        id_map[m.role or "premise"] = nid
    # the conclusion (NIGAMANA)
    conc_id = g.add_info(id=f"{arg.argument_id}:conc", text=arg.conclusion.text if arg.conclusion else arg.title,
                         role="conclusion", passage_ids=[])
    # one inference: the premises entail the conclusion via the scheme
    premise_ids = [n.id for n in g.info_nodes if n.role == "premise"]
    g.add_inference(scheme=arg.inference_scheme, premise_ids=premise_ids, conclusion_id=conc_id)
    # a conflict: the universalization is challenged (the honest boundary)
    g.add_conflict("QUALIFICATION", conc_id, conc_id,
                   text="The passage establishes the per-field support, not the universal identity.",
                   passage_ids=[])

    report = g.check()
    check("graph is structurally sound", report["ok"], report["problems"])
    check("has info + inference + conflict nodes",
          report["n_info"] >= 4 and report["n_inference"] >= 1 and report["n_conflict"] >= 1,
          report)
    # resolvability: premise nodes carry passage_ids
    resolved = [n for n in g.info_nodes if n.passage_ids]
    check("premises resolve to passages", len(resolved) >= 3, len(resolved))

    # 3. derive the EssayPlan
    print("\n== EssayPlan (the essay as a decision) ==")
    plan = plan_from_argument(arg, "Order-less Support", "ipvv")
    check("plan derived", plan.thesis.strip() != "")
    pcheck = plan.check()
    check("plan is sound", pcheck["ok"], pcheck["problems"])
    check("plan has claims", pcheck["n_claims"] >= 3, pcheck["n_claims"])
    check("plan claims trace to evidence or argument",
          all(c.passage_ids or c.argument_id for c in plan.claims))

    # 4. serialization (the in-system record)
    print("\n== serialization ==")
    d = plan.to_dict()
    for k in ["plan_id", "work_id", "theme", "thesis", "claims", "objections", "evidence_sets"]:
        check(f"to_dict has {k}", k in d)
    gd = g.to_dict()
    check("graph serializes 3 node kinds",
          "info_nodes" in gd and "inference_nodes" in gd and "conflict_nodes" in gd)

    print(f"\n=== RESULT: {PASS} pass / {FAIL} fail ===")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
