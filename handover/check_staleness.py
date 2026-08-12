#!/usr/bin/env python3
"""check_staleness.py — the agent-system staleness checker.

Detects when the agent system's docs have drifted from the registry / vision / checkpoints / gold /
tests. Run at every session start AND end. A failing check means the SYSTEM is stale — fix the doc,
not the checker.

Checks:
  1. AGENTS.yaml parses; every agent has the required fields
  2. every `orientation` + `handover_dir` + `owns` path in AGENTS.yaml exists on disk
  3. the canonical vision + shared checkpoints exist (VISION_AND_NAVIGATION.md, handover/CHECKPOINTS.md)
  4. each agent's ORIENTATION mentions its own question + checkpoints (drift from registry)
  5. no agent ORIENTATION contains a verbatim copy of the vision (must link, not copy)
  6. each lane has a live INDEX.md (the "current state" pointer)
  7. every pt:passage:ipvv:chunk id in benchmarks/v0/structure/ resolves against data/published/ipvv/index.json
  8. every PAT-STRUCT fixture passes the gold-consistency validator
  9. required system paths exist (SYSTEM.md, check_staleness.py itself)

Usage: python3 handover/check_staleness.py   (exit 0 = clean, 1 = stale)
"""
from __future__ import annotations
import glob
import json
import os
import re
import sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YAML_PATH = os.path.join(ROOT, "handover", "AGENTS.yaml")
VISION = os.path.join(ROOT, "VISION_AND_NAVIGATION.md")
CHECKPOINTS = os.path.join(ROOT, "handover", "CHECKPOINTS.md")
STRUCTURE_DIR = os.path.join(ROOT, "benchmarks", "v0", "structure")
INDEX_PATH = os.path.join(ROOT, "data", "published", "ipvv", "index.json")

# a verbatim vision snippet to detect copying (agents must LINK to it, not embed it)
VISION_SNIPPET = "We are building a **computable scholarly tradition**"

failures = []


def fail(msg: str) -> None:
    failures.append(msg)
    print(f"  ✗ {msg}")


def ok(msg: str) -> None:
    print(f"  ✓ {msg}")


def check_path(p: str, what: str) -> None:
    if os.path.exists(p):
        ok(f"{what}: {os.path.relpath(p, ROOT)}")
    else:
        fail(f"{what} missing: {os.path.relpath(p, ROOT)}")


def main() -> int:
    print("PĀṬALA AGENT-SYSTEM STALENESS CHECK\n")

    # 1+2. registry parses + paths exist
    print("== registry ==")
    if not os.path.exists(YAML_PATH):
        fail("AGENTS.yaml missing")
        print("\nSTALE: 1 failure. Fix, don't bypass.")
        return 1
    with open(YAML_PATH) as f:
        reg = yaml.safe_load(f)
    agents = reg.get("agents", {})
    ok(f"parsed {len(agents)} agents: {', '.join(agents.keys())}")
    for aid, a in agents.items():
        for field in ["id", "name", "question", "checkpoints", "orientation", "handover_dir", "owns"]:
            if field not in a:
                fail(f"agent {aid}: missing registry field '{field}'")
        check_path(os.path.join(ROOT, a["orientation"]), f"{aid} orientation")
        check_path(os.path.join(ROOT, a["handover_dir"]), f"{aid} handover dir")
        for own in a.get("owns", []):
            if not own.startswith(("benchmarks/", "machinelearning/", "handover/", "VISION", "AGENTS")):
                continue
            check_path(os.path.join(ROOT, own.rstrip("/")), f"{aid} owns")

    # 3. vision + checkpoints
    print("\n== canonical vision + shared checkpoints ==")
    check_path(VISION, "canonical vision")
    check_path(CHECKPOINTS, "shared checkpoints")

    # 4+5. each orientation mentions its own question/checkpoints, does not copy the vision
    print("\n== orientations (derived, not copied) ==")
    for aid, a in agents.items():
        ori = os.path.join(ROOT, a["orientation"])
        if not os.path.exists(ori):
            continue
        text = open(ori).read()
        # 4. mentions its own question (a fragment of it)
        q_frag = a["question"][:30]
        if q_frag in text:
            ok(f"{aid}: orientation states its own question")
        else:
            fail(f"{aid}: orientation does not state its own question (drift from registry)")
        # mentions its checkpoints
        cp_txt = " ".join(a["checkpoints"])
        for cp in a["checkpoints"]:
            if cp == "all":
                continue
            if cp not in text:
                fail(f"{aid}: orientation does not mention {cp}")
        # 5. does not copy the vision verbatim
        if VISION_SNIPPET in text:
            fail(f"{aid}: orientation contains a VERBATIM copy of the vision (must link, not copy)")

    # 6. each lane has a live INDEX
    print("\n== lane INDEX pointers ==")
    for aid, a in agents.items():
        idx = os.path.join(ROOT, a["handover_dir"], "INDEX.md")
        check_path(idx, f"{aid} INDEX")

    # 7. passage ids resolve
    print("\n== benchmark passage resolution ==")
    if os.path.exists(INDEX_PATH):
        index_ids = {p["id"] for p in json.load(open(INDEX_PATH))["passages"]}
    else:
        index_ids = set()
        fail("data/published/ipvv/index.json missing")
    for fx in sorted(glob.glob(os.path.join(STRUCTURE_DIR, "PAT-STRUCT-*.json"))):
        data = json.load(open(fx))
        gold = data.get("expected", data)
        pids = [gold.get("passage")] + [
            n.get("grounding", {}).get("passage_id") for n in gold.get("nodes", [])
            if n.get("grounding", {}).get("passage_id")]
        unresolved = [p for p in pids if p and p.startswith("pt:passage:ipvv:") and p not in index_ids]
        if unresolved:
            fail(f"{os.path.basename(fx)}: unresolved passage(s) {set(unresolved)}")
        else:
            ok(f"{os.path.basename(fx)}: passages resolve")

    # 8. gold-consistency (reuse the validator without importing the venv)
    print("\n== gold consistency ==")
    for fx in sorted(glob.glob(os.path.join(STRUCTURE_DIR, "PAT-STRUCT-*.json"))):
        data = json.load(open(fx))
        gold = data.get("expected", data)
        probs = _gold_problems(gold, index_ids)
        if probs:
            fail(f"{os.path.basename(fx)}: {'; '.join(probs)}")
        else:
            ok(f"{os.path.basename(fx)}: consistent")

    # 9. system paths
    print("\n== system ==")
    check_path(os.path.join(ROOT, "handover", "SYSTEM.md"), "agent-system meta-doc")

    print(f"\n=== {'SYSTEM CLEAN (0 failures)' if not failures else f'STALE: {len(failures)} failure(s)'} ===")
    return 0 if not failures else 1


def _gold_problems(gold: dict, known_ids: set) -> list[str]:
    """Inline copy of the gold-consistency validator (no venv needed)."""
    probs = []
    nodes = {n.get("proposition_id") or n.get("id"): n for n in gold.get("nodes", [])}
    used = set(nodes)
    for nid, n in nodes.items():
        g = n.get("grounding", {})
        pid = g.get("passage_id", "")
        if pid and pid.startswith("pt:passage:ipvv:") and pid not in known_ids:
            probs.append(f"{nid}: passage {pid} unresolved")
    if gold.get("passage") and gold["passage"].startswith("pt:passage:") and gold["passage"] not in known_ids:
        probs.append(f"gold passage {gold['passage']} unresolved")
    referenced = set()
    for inf in gold.get("inferences", []):
        for p in inf.get("premise_ids", []):
            if p not in used:
                probs.append(f"{inf.get('inference_id')}: premise {p} missing")
            referenced.add(p)
        for c in inf.get("conclusion_ids", []):
            if c not in used:
                probs.append(f"{inf.get('inference_id')}: conclusion {c} missing")
            referenced.add(c)
    for nid, n in nodes.items():
        if nid not in referenced and n.get("kind") == "TEXTUAL_CLAIM":
            probs.append(f"unused textual claim {nid}")
    if not gold.get("boundary"):
        probs.append("no boundary")
    return probs


if __name__ == "__main__":
    sys.exit(main())
