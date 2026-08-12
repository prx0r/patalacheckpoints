#!/usr/bin/env python3
"""flow.py — the live orchestration interface for the agent system.

The single command agents use to update the LIVE progress state. It reads the agent
registry (AGENTS.yaml), updates the live state (STATE.yaml), bumps the state version,
and appends to an immutable history log (history.log). It keeps CHECKPOINTS.md + the
per-lane INDEX consistent by reporting the delta (the docs are kept consistent by the
staleness checker / coordinator).

Usage:
  python3 handover/flow.py status                      show all agents + checkpoints
  python3 handover/flow.py status --agent agent1        show one agent
  python3 handover/flow.py update <agent> <cp> <status> [-n note]
        e.g. flow.py update agent1 CP4 IN_PROGRESS -n "built ARG-003"
  python3 handover/flow.py add-agent <agent>            scaffold a new agent's state block
  python3 handover/flow.py history                      show the versioned change log

Exit 0 on success, 1 on invalid input.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.join(HERE, "AGENTS.yaml")
STATE = os.path.join(HERE, "STATE.yaml")
HISTORY = os.path.join(HERE, "history.log")

STATUSES = {"NOT_STARTED", "IN_PROGRESS", "PARTIAL", "DONE", "FROZEN", "BLOCKED", "VALIDATED"}


def _load() -> tuple[dict, dict]:
    reg = yaml.safe_load(open(REG)) if os.path.exists(REG) else {}
    state = yaml.safe_load(open(STATE)) if os.path.exists(STATE) else {"state_version": 0, "last_update": ""}
    return reg, state


def _save_state(state: dict) -> None:
    state["state_version"] = int(state.get("state_version", 0)) + 1
    state["last_update"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with open(STATE, "w") as f:
        yaml.safe_dump(state, f, sort_keys=False, allow_unicode=True)


def _history(msg: str) -> None:
    with open(HISTORY, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {msg}\n")


def cmd_status(args) -> int:
    reg, state = _load()
    agents = reg.get("agents", {})
    if args.agent:
        agents = {args.agent: agents.get(args.agent, {})}
    print(f"state_version: {state.get('state_version', 0)}   last_update: {state.get('last_update', '')}\n")
    for aid in sorted(agents):
        a = agents.get(aid, {})
        cp = a.get("checkpoints", [])
        block = state.get(aid, {}).get("checkpoints", {})
        print(f"== {aid}  ({a.get('name','?')}) — checkpoints: {cp if isinstance(cp,list) else cp}")
        # per-agent checkpoint states
        for k, v in block.items():
            s = v.get("status", "?") if isinstance(v, dict) else "?"
            print(f"    {k:6}  {s:15} {v.get('note','')[:70] if isinstance(v,dict) else ''}")
        if not block:
            print("    (no live state yet)")
    # shared / vision-level
    print("\n== shared (vision coordinate system) ==")
    for k, v in (state.get("shared", {}) or {}).items():
        print(f"    {k:6}  {str(v):15}")
    return 0


def cmd_update(args) -> int:
    if args.status not in STATUSES:
        print(f"invalid status '{args.status}'. valid: {sorted(STATUSES)}")
        return 1
    reg, state = _load()
    if args.agent not in reg.get("agents", {}):
        print(f"unknown agent '{args.agent}'. known: {', '.join(reg.get('agents', {}))}")
        return 1
    agent_cps = reg["agents"][args.agent].get("checkpoints", [])
    if args.cp not in (agent_cps if isinstance(agent_cps, list) else [agent_cps]):
        print(f"agent '{args.agent}' has no checkpoint '{args.cp}'. its checkpoints: {agent_cps}")
        return 1

    state.setdefault(args.agent, {}).setdefault("checkpoints", {})
    state[args.agent]["checkpoints"][args.cp] = {
        "status": args.status, "note": args.note or "", "updated_by": args.by, "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    _save_state(state)
    _history(f"{args.by} | {args.agent} {args.cp} -> {args.status} | {args.note or ''} | v{state['state_version']}")
    print(f"updated {args.agent} {args.cp} -> {args.status} (state_version {state['state_version']})")
    print("NOTE: keep CHECKPOINTS.md + the lane INDEX consistent, then run check_staleness.py.")
    return 0


def cmd_add_agent(args) -> int:
    reg, state = _load()
    agents = reg.setdefault("agents", {})
    if args.agent in agents:
        print(f"agent '{args.agent}' already exists in AGENTS.yaml — edit the registry to modify it.")
        return 1
    # scaffold: user is expected to complete AGENTS.yaml entry; add an empty state block
    state.setdefault(args.agent, {"checkpoints": {}})
    _save_state(state)
    _history(f"orchestrator | add-agent {args.agent} | scaffolded state block | v{state['state_version']}")
    print(f"scaffolded state block for '{args.agent}'.")
    print(f"NOW: add the full entry to AGENTS.yaml (direction, lane, question, checkpoints, owns, orientation),")
    print(f"     then generate its orientation, then run check_staleness.py.")
    return 0


def cmd_history(args) -> int:
    if not os.path.exists(HISTORY):
        print("(no history yet)")
        return 0
    print(open(HISTORY).read().rstrip())
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Pāṭala agent-system live flow")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("status", help="show live state")
    sp.add_argument("--agent")
    sp.set_defaults(func=cmd_status)

    up = sub.add_parser("update", help="update a checkpoint's status")
    up.add_argument("agent")
    up.add_argument("cp")
    up.add_argument("status")
    up.add_argument("-n", "--note", default="")
    up.add_argument("--by", default="agent")
    up.set_defaults(func=cmd_update)

    ap = sub.add_parser("add-agent", help="scaffold a new agent's state block")
    ap.add_argument("agent")
    ap.set_defaults(func=cmd_add_agent)

    hp = sub.add_parser("history", help="show the versioned change log")
    hp.set_defaults(func=cmd_history)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
