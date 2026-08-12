#!/usr/bin/env python3
"""context_gate.py — the mechanical gate that forces the FULL-context read.

The orientation used to be a passive reading list with self-assessed gates ("you must be able to
state X"). Nothing verified that the agent actually READ all the docs, so agents stopped early and
never built full-system understanding. This gate makes full context LOAD-BEARING: an agent cannot
proceed to work until every doc in its chain is read, in order, each leaving a real trace (a
key-point summary, not a checkmark).

Commands:
  python3 handover/context_gate.py --status [agent]        show read/unread for a chain (default all)
  python3 handover/context_gate.py --validate              every manifest path exists
  python3 handover/context_gate.py --pending agent         list what an agent still must read
  python3 handover/context_gate.py --confirm <id> --by <agent> -k "<key point>"
                                                           mark a doc read (ordered; needs a key-point)
  python3 handover/context_gate.py --reset agent [--all]   clear an agent's read record

Exit codes: 0 = COMPLETE/clean, 1 = incomplete (or error). `--status` returns 0 ONLY when the
requested chain is fully read.
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAIN_PATH = os.path.join(ROOT, "handover", "CONTEXT-CHAIN.yaml")
READ_DIR = os.path.join(ROOT, "handover", "context-read")

MIN_KEY_POINT = 20  # a real trace, not a blank checkmark


def _chain() -> dict:
    with open(CHAIN_PATH) as f:
        return yaml.safe_load(f)


def _record_path(agent: str) -> str:
    return os.path.join(READ_DIR, f"{agent}.yaml")


def _load_record(agent: str) -> dict:
    p = _record_path(agent)
    if os.path.exists(p):
        with open(p) as f:
            return yaml.safe_load(f) or {}
    return {}


def _full_chain(agent: str) -> list[dict]:
    c = _chain()
    items = list(c.get("shared", []))
    items += c.get("agents", {}).get(agent, [])
    return items


def cmd_validate() -> int:
    c = _chain()
    bad = []
    for item in c.get("shared", []):
        if not os.path.exists(os.path.join(ROOT, item["path"])):
            bad.append(f"shared/{item['id']}: {item['path']}")
    for aid, items in c.get("agents", {}).items():
        for item in items:
            if not os.path.exists(os.path.join(ROOT, item["path"])):
                bad.append(f"{aid}/{item['id']}: {item['path']}")
    if bad:
        print("CONTEXT CHAIN VALIDATION: MISSING FILES (fix the manifest, not the gate)\n")
        for b in bad:
            print(f"  ✗ {b}")
        print(f"\n{len(bad)} missing. Every context path must exist.")
        return 1
    print(f"CONTEXT CHAIN VALIDATION: {len(c.get('shared', [])) + sum(len(v) for v in c.get('agents', {}).values())} paths present, all resolve.")
    return 0


def cmd_status(agent: str | None) -> int:
    c = _chain()
    if agent:
        return _status_one(agent)
    overall = 0
    for aid in c.get("agents", {}):
        rc = _status_one(aid)
        overall = max(overall, rc)
    return overall


def _status_one(agent: str) -> int:
    items = _full_chain(agent)
    rec = _load_record(agent)
    read_count = 0
    print(f"CONTEXT CHAIN — {agent} ({len(items)} docs)")
    for i, it in enumerate(items, 1):
        done = it["id"] in rec
        if done:
            read_count += 1
            mark = "✓"
        else:
            mark = " "
        print(f"  [{mark}] {i:2}. {it['id']:<22} {it['path']}")
        if done:
            print(f"         key-point: {rec[it['id']].get('key_point', '(none)')}")
        else:
            print(f"         why: {it['why']}")
    complete = read_count == len(items)
    print(f"\n  read {read_count}/{len(items)} {'COMPLETE' if complete else 'INCOMPLETE'}")
    if not complete:
        nxt = next((it["id"] for it in items if it["id"] not in rec), None)
        print(f"  next to read: {nxt}")
    print(f"\n  {'CONTEXT GATE: PASS (full context acquired — you may build)' if complete else 'CONTEXT GATE: FAIL (read every doc in order, then confirm each with a key-point)'}")
    return 0 if complete else 1


def cmd_pending(agent: str) -> int:
    items = _full_chain(agent)
    rec = _load_record(agent)
    pending = [it for it in items if it["id"] not in rec]
    if not pending:
        print(f"{agent}: nothing pending — full context acquired.")
        return 0
    print(f"{agent}: {len(pending)} unread (in order):")
    for it in pending:
        print(f"  - {it['id']}: {it['path']}  ({it['why']})")
    print(f"\nconfirm each: python3 handover/context_gate.py --confirm <id> --by {agent} -k '<key point>'")
    return 1


def cmd_confirm(agent: str, doc_id: str, key_point: str) -> int:
    items = _full_chain(agent)
    by_id = {it["id"]: it for it in items}
    if doc_id not in by_id:
        print(f"✗ '{doc_id}' is not in {agent}'s context chain. Use --status to see the valid ids.")
        return 1
    if not key_point or len(key_point.strip()) < MIN_KEY_POINT:
        print(f"✗ key-point too short (need >= {MIN_KEY_POINT} chars). Reading must leave a real trace, not a checkmark.")
        return 1
    rec = _load_record(agent)
    # ordered: all earlier ids must already be confirmed (you must learn gradually)
    idx = next(i for i, it in enumerate(items) if it["id"] == doc_id)
    missing_earlier = [it["id"] for it in items[:idx] if it["id"] not in rec]
    if missing_earlier:
        print(f"✗ ordered read: confirm {missing_earlier[0]} before {doc_id} (you must learn gradually).")
        return 1
    rec[doc_id] = {
        "by": agent,
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "key_point": key_point.strip(),
    }
    os.makedirs(READ_DIR, exist_ok=True)
    with open(_record_path(agent), "w") as f:
        yaml.safe_dump(rec, f, sort_keys=False)
    print(f"✓ {agent}: confirmed '{doc_id}' ({by_id[doc_id]['path']})")
    remaining = sum(1 for it in items if it["id"] not in rec)
    print(f"  {remaining} docs remain in the chain.")
    return 0 if remaining == 0 else 0


def cmd_reset(agent: str, all_agents: bool) -> int:
    if all_agents:
        if os.path.isdir(READ_DIR):
            for fn in os.listdir(READ_DIR):
                if fn.endswith(".yaml"):
                    os.remove(os.path.join(READ_DIR, fn))
        print("context read-records cleared for all agents.")
    else:
        p = _record_path(agent)
        if os.path.exists(p):
            os.remove(p)
        print(f"{agent}: read-record cleared.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Pāṭala full-context read gate")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--status", nargs="?", const="__all__", metavar="agent",
                   help="show read/unread for one agent (default all); exit 0 only when complete")
    g.add_argument("--validate", action="store_true", help="every manifest path exists")
    g.add_argument("--pending", metavar="agent", help="list what an agent still must read")
    g.add_argument("--confirm", metavar="id", help="mark a doc read (needs --by and -k)")
    g.add_argument("--reset", metavar="agent", help="clear an agent's read record")
    ap.add_argument("--by", metavar="agent", help="agent confirming the read")
    ap.add_argument("-k", "--key-point", metavar="TEXT", help="the trace: what you actually learned")
    ap.add_argument("--all", action="store_true", help="with --reset: clear all agents")
    args = ap.parse_args()

    if args.validate:
        return cmd_validate()
    if args.status:
        return cmd_status(None if args.status == "__all__" else args.status)
    if args.pending:
        return cmd_pending(args.pending)
    if args.confirm:
        if not args.by:
            print("✗ --confirm requires --by <agent>")
            return 1
        return cmd_confirm(args.by, args.confirm, args.key_point or "")
    if args.reset:
        return cmd_reset(args.reset, args.all)
    return 1


if __name__ == "__main__":
    sys.exit(main())
