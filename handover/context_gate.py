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
  python3 handover/context_gate.py --begin agent           start a FRESH agent-instance session (required
                                                           for a new agent; invalidates inherited traces)
  python3 handover/context_gate.py --confirm <id> --by <agent> -k "<key point>"
                                                           mark a doc read (ordered; needs a key-point)
  python3 handover/context_gate.py --reset agent [--all]   clear an agent's read record

SESSION BOUNDING (the anti-hallucination rule): a read trace only counts toward PASS if it was
confirmed by the CURRENT agent instance (tagged with that instance's session token). Traces left by a
previous instance are shown as INHERITED and do NOT pass the gate — a new agent MUST run `--begin` and
then re-read + re-confirm every doc. This prevents a fresh agent from seeing `--status` PASS based on
traces it never wrote.

Exit codes: 0 = COMPLETE/clean, 1 = incomplete (or error). `--status` returns 0 ONLY when the
requested chain is fully read by the current instance.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import secrets
import sys
from datetime import datetime, timezone

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAIN_PATH = os.path.join(ROOT, "handover", "CONTEXT-CHAIN.yaml")
READ_DIR = os.path.join(ROOT, "handover", "context-read")

MIN_KEY_POINT = 20  # a real trace, not a blank checkmark


def _session_path(agent: str) -> str:
    return os.path.join(READ_DIR, f"{agent}.session")


def _read_session(agent: str) -> dict | None:
    p = _session_path(agent)
    if os.path.exists(p):
        with open(p) as f:
            return yaml.safe_load(f) or {}
    return None


def _write_session(agent: str, token: str, started: str) -> None:
    os.makedirs(READ_DIR, exist_ok=True)
    with open(_session_path(agent), "w") as f:
        yaml.safe_dump({"session_token": token, "started": started}, f, sort_keys=False)


def _current_token(agent: str) -> str | None:
    s = _read_session(agent)
    return (s or {}).get("session_token")


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
    cur = _current_token(agent)
    read_count = 0
    inherited = 0
    started = (_read_session(agent) or {}).get("started", "")
    print(f"CONTEXT CHAIN — {agent} ({len(items)} docs)")
    if cur:
        print(f"  session: {cur[:8]}… started {started}  (only reads tagged THIS session count toward PASS)")
    else:
        print("  session: NONE — run `--begin agent1` first; no trace can count until you start an instance session")
    for i, it in enumerate(items, 1):
        e = rec.get(it["id"])
        fresh = bool(e and cur and e.get("session_token") == cur)
        if fresh:
            read_count += 1
            mark = "✓"
        elif e:
            inherited += 1
            mark = "⬒"  # inherited from a previous instance — does NOT count
        else:
            mark = " "
        print(f"  [{mark}] {i:2}. {it['id']:<22} {it['path']}")
        if fresh:
            print(f"         key-point: {e.get('key_point')}")
        elif e:
            print(f"         INHERITED (confirmed {e.get('at')}) — re-read + --confirm to count")
        else:
            print(f"         why: {it['why']}")
    complete = read_count == len(items)
    print(f"\n  read this session: {read_count}/{len(items)}  · inherited (not counted): {inherited}")
    if not complete:
        nxt = next((it["id"] for it in items if not (rec.get(it["id"]) and cur and rec[it["id"]].get("session_token") == cur)), None)
        print(f"  next to read+confirm: {nxt}")
    print(f"\n  {'CONTEXT GATE: PASS (full context read + confirmed by THIS agent instance — you may build)' if complete else 'CONTEXT GATE: FAIL (a fresh agent must run --begin, then actually read + confirm every doc in order)'}")
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
    # a trace only counts if it is tagged with the CURRENT instance's session token
    cur = _current_token(agent)
    if not cur:
        print(f"✗ no session for {agent}. A fresh agent must first run: python3 handover/context_gate.py --begin {agent}")
        print("  (This stops an agent from claiming reads it did not perform in this instance.)")
        return 1
    # ordered: all earlier ids must already be confirmed (you must learn gradually)
    idx = next(i for i, it in enumerate(items) if it["id"] == doc_id)
    missing_earlier = [it["id"] for it in items[:idx]
                       if not (rec.get(it["id"]) and rec[it["id"]].get("session_token") == cur)]
    if missing_earlier:
        print(f"✗ ordered read: confirm {missing_earlier[0]} before {doc_id} (you must learn gradually).")
        return 1
    rec[doc_id] = {
        "by": agent,
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "session_token": cur,
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
                if fn.endswith(".session"):
                    os.remove(os.path.join(READ_DIR, fn))
        print("context read-records cleared for all agents.")
    else:
        p = _record_path(agent)
        if os.path.exists(p):
            os.remove(p)
        sp = _session_path(agent)
        if os.path.exists(sp):
            os.remove(sp)
        print(f"{agent}: read-record cleared (traces + session).")
    return 0


def cmd_begin(agent: str) -> int:
    """Start a fresh agent-instance session. A new agent MUST call this before confirming reads.

    Generates a new session token, so traces written by any previous instance no longer count toward
    this agent's context gate — forcing a genuinely fresh full read. Returns 1 if a session is already
    active (to avoid silently re-claiming an in-progress read); pass a fresh token only for a NEW instance.
    """
    cur = _current_token(agent)
    if cur:
        print(f"✗ {agent} already has an active session ({cur[:8]}…).")
        print(f"  A fresh instance must run `--reset {agent}` (or --all) to start over, then `--begin {agent}`.")
        return 1
    token = secrets.token_hex(16)
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    _write_session(agent, token, started)
    print(f"✓ {agent}: fresh instance session begun (token {token[:8]}…, started {started}).")
    print(f"  Inherited read-traces no longer count. Read + confirm every doc in order, e.g.:")
    print(f"    python3 handover/context_gate.py --confirm <id> --by {agent} -k \"<what you actually learned>\"")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Pāṭala full-context read gate")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--status", nargs="?", const="__all__", metavar="agent",
                   help="show read/unread for one agent (default all); exit 0 only when complete")
    g.add_argument("--validate", action="store_true", help="every manifest path exists")
    g.add_argument("--pending", metavar="agent", help="list what an agent still must read")
    g.add_argument("--begin", metavar="agent", help="start a FRESH agent-instance session (required for a new agent)")
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
    if args.begin:
        return cmd_begin(args.begin)
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
