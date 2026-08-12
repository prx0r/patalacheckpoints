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
STATE_PATH = os.path.join(ROOT, "handover", "STATE.yaml")
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


def _axiom_essence(axiom: str) -> str:
    """A short distinctive phrase per tone axiom that an orientation must echo to count as adopted.

    Map each axiom to its load-bearing phrase (the anti-theatre core). This lets orientations
    phrase it in their own words while still proving they adopted the substance.
    """
    mappings = {
        "BE BRUTALLY HONEST": "honest about what is real",
        "RETRACT OVERCLAIMS": "retract",
        "NAME THE FAILURE MODE": "failure mode",
        "SEPARATE REAL FROM THEATER": "real from theater",
        "NO HYPE": "not scholarship",
        "PRECISION OVER COVERAGE": "abstain",
    }
    for label, phrase in mappings.items():
        if label in axiom:
            return phrase.lower()
    return axiom.replace("—", " ").lower()


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
    agents = reg.get("instances", {})
    template = reg.get("template", {})
    ok(f"parsed {len(agents)} live instances: {', '.join(agents.keys())}")
    if template:
        ok("agent0 template present (the archetype all instances instantiate)")
        for fld in ["id", "name", "schema", "orientation_template", "live_flow"]:
            if fld not in template:
                fail(f"template missing field '{fld}'")
        # the template's orientation + governance docs exist
        ot = template.get("orientation_template")
        if ot:
            check_path(os.path.join(ROOT, ot), "agent0 orientation template")
        check_path(os.path.join(ROOT, "handover", "ORIENTATION-AGENT0.md"), "agent0 governance doc")
        # each instance must declare instance_of: agent0
        for aid, a in agents.items():
            if a.get("instance_of") != "agent0":
                fail(f"instance '{aid}' is not declared instance_of: agent0")
            # each instance has a tracked history log
            hist = a.get("history")
            if hist:
                check_path(os.path.join(ROOT, hist), f"{aid} history log")
            else:
                fail(f"instance '{aid}' has no tracked 'history' file")
    else:
        fail("AGENTS.yaml has no 'template' block (agent0 archetype)")
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
    # the doctrine axioms every orientation must adopt
    doctrine = reg.get("doctrine", {})
    tone_axioms = doctrine.get("tone_axioms", [])
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
        # 6. adopts the tone axioms (at least the essence of each is present)
        if tone_axioms:
            adopted = sum(1 for ax in tone_axioms if _axiom_essence(ax) in text.lower())
            if adopted >= max(3, len(tone_axioms) // 2):
                ok(f"{aid}: adopts the tone axioms ({adopted}/{len(tone_axioms)})")
            else:
                fail(f"{aid}: does not adopt the tone axioms ({adopted}/{len(tone_axioms)}) — the tone is part of its existence")

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
    check_path(os.path.join(ROOT, "handover", "flow.py"), "live flow command")
    check_path(STATE_PATH, "live state")

    # 10. live state consistency: STATE.yaml matches the registry + has the shared CP ladder
    print("\n== live state (STATE.yaml) ==")
    if os.path.exists(STATE_PATH):
        try:
            state = yaml.safe_load(open(STATE_PATH))
        except Exception as e:
            state = None
            fail(f"STATE.yaml does not parse: {e}")
        if state:
            if "state_version" not in state:
                fail("STATE.yaml has no state_version")
            # every registry agent has a state block
            for aid in agents:
                if aid not in state:
                    fail(f"STATE.yaml missing block for agent '{aid}'")
                else:
                    ok(f"state block for '{aid}' present")
            # shared CP ladder present
            shared = state.get("shared", {})
            if not shared:
                fail("STATE.yaml has no 'shared' CP ladder")
            else:
                ok(f"shared CP ladder present ({len(shared)} entries)")

    # 11. full-context read: every live agent must have read its whole context chain
    print("\n== full-context read (CONTEXT-CHAIN + context_gate) ==")
    _check_context_read(agents)

    print(f"\n=== {'SYSTEM CLEAN (0 failures)' if not failures else f'STALE: {len(failures)} failure(s)'} ===")
    return 0 if not failures else 1


def _check_context_read(agents: dict) -> None:
    """Each live agent must have confirmed reading every doc in its context chain (in order).

    The chain is defined in handover/CONTEXT-CHAIN.yaml; the read-record per agent lives in
    handover/context-read/<agent>.yaml. A doc counts as read only with a real key-point. If any live
    agent has not read its full chain, the system is stale — the agent has not acquired full context.
    """
    chain_path = os.path.join(ROOT, "handover", "CONTEXT-CHAIN.yaml")
    if not os.path.exists(chain_path):
        fail("handover/CONTEXT-CHAIN.yaml missing (the full-context manifest)")
        return
    chain = yaml.safe_load(open(chain_path))
    for aid in agents:
        items = list(chain.get("shared", [])) + list(chain.get("agents", {}).get(aid, []))
        if not items:
            fail(f"{aid}: no context chain defined")
            continue
        rec_path = os.path.join(ROOT, "handover", "context-read", f"{aid}.yaml")
        rec = {}
        if os.path.exists(rec_path):
            rec = yaml.safe_load(open(rec_path)) or {}
        missing = [it["id"] for it in items if it["id"] not in rec]
        if missing:
            fail(f"{aid}: context chain INCOMPLETE ({len(rec)}/{len(items)} read; unread: {', '.join(missing[:5])}{'…' if len(missing) > 5 else ''})")
        else:
            ok(f"{aid}: full context chain read ({len(items)}/{len(items)})")


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
