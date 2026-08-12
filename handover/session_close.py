#!/usr/bin/env python3
"""session_close.py — the SMOOTH, repeatable session-end runner (encodes the ORIENTATION loop).

The ORIENTATION's session-update loop (do EVERY session end) is 5 steps. Steps 1, 4, 5 and the
derived-artifact regen are MECHANICAL; steps 2 & 3 need prose. This command does the mechanical parts
and prints the checklist for the prose parts, so nothing rots.

  python3 handover/session_close.py --agent agent1 --cp CP4 --status IN_PROGRESS \
      --note "independent gold review is next" \
      [--summary "multi-line text appended to SESSION-<date>.md"] \
      [--handoff "TO <agent> :: <what> :: <file> :: <schema snippet>"]

It:
  1. runs the gates (check_staleness, context gate, theatre_check) and reports,
  2. updates live state via flow.py,
  3. regenerates derived artifacts (ARG-GOLD review packet),
  4. appends a dated SESSION note (summary + a snapshot of the live state),
  5. appends a cross-lane handoff to handover/LOG.md (if --handoff),
  6. prints the PROSE checklist (INDEX / CHECKPOINTS / CORE-BIBLE / CLAIMS) to update, then re-verify.
"""
from __future__ import annotations

import argparse
import datetime
import os
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def agent_handover_dir(agent: str) -> str:
    """Look up the agent's handover dir from the registry (AGENTS.yaml) — the single source of truth."""
    with open(os.path.join(ROOT, "handover", "AGENTS.yaml")) as f:
        reg = yaml.safe_load(f)
    return reg["instances"][agent]["handover_dir"].rstrip("/")


def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def flow_status() -> str:
    _, out = run(["python3", "handover/flow.py", "status"])
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Pāṭala session-close runner (the smooth loop)")
    ap.add_argument("--agent", required=True, help="agent id (agent1/agent2)")
    ap.add_argument("--cp", required=True, help="checkpoint id (e.g. CP4)")
    ap.add_argument("--status", required=True, help="new status (DONE/PARTIAL/IN_PROGRESS)")
    ap.add_argument("--note", required=True, help="short what-changed note for flow state")
    ap.add_argument("--summary", default="", help="multi-line summary appended to SESSION-<date>.md")
    ap.add_argument("--handoff", default="", help="cross-lane handoff: 'TO <agent> :: what :: file :: schema'")
    ap.add_argument("--session-note-file", default="", help="optional file with the SESSION note body")
    args = ap.parse_args()

    date = datetime.date.today().isoformat()
    print("== SESSION CLOSE — gates ==")
    rc1, out1 = run(["python3", "handover/check_staleness.py"])
    print(out1.strip().splitlines()[-1] if out1.strip() else "staleness: no output")
    rc2, out2 = run(["python3", "handover/context_gate.py", "--status", args.agent])
    print("context gate:", "PASS" if rc2 == 0 else "INCOMPLETE")
    rc3, out3 = run(["python3", "machinelearning/theatre_check.py", "--status"])
    print("theatre_check:", "ok" if rc3 == 0 else "see output")

    print("\n== SESSION CLOSE — live state ==")
    _, fr = run(["python3", "handover/flow.py", "update", args.agent, args.cp, args.status,
                 "-n", args.note, "--by", args.agent])
    print(fr.strip().splitlines()[-1] if fr.strip() else "flow update done")

    print("\n== SESSION CLOSE — derived artifacts ==")
    # regenerate the reviewer-facing packet (keeps it in sync with the golds)
    pkt = os.path.join(ROOT, "machinelearning/research/experiments/build_review_packet.py")
    if os.path.exists(pkt):
        rc, o = run(["bash", "-c", f"cd {ROOT}/machinelearning/research && . .venv/bin/activate && python experiments/build_review_packet.py"])
        print(o.strip().splitlines()[-1] if o.strip() else "review packet regenerated")

    print("\n== SESSION CLOSE — session note ==")
    handover_dir = agent_handover_dir(args.agent)
    session_path = os.path.join(ROOT, handover_dir, f"SESSION-{date}.md")
    if not os.path.exists(session_path):
        session_path = os.path.join(ROOT, handover_dir, "SESSION-2026-08-12.md")
    body = args.summary
    if args.session_note_file and os.path.exists(args.session_note_file):
        body = open(args.session_note_file).read()
    with open(session_path, "a", encoding="utf-8") as f:
        f.write(f"\n\n---\n\n## SESSION UPDATE ({date}, via session_close)\n\n")
        f.write(body.strip() + "\n\n")
        f.write("**Live state snapshot:**\n```\n" + flow_status()[:800] + "\n```\n")
    print(f"appended session note -> {os.path.relpath(session_path, ROOT)}")

    if args.handoff:
        print("\n== SESSION CLOSE — cross-lane handoff ==")
        # format: "TO <agent> :: what :: file :: schema"
        parts = [p.strip() for p in args.handoff.split("::")]
        log_path = os.path.join(ROOT, "handover", "LOG.md")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"\n## Handoff ({date}) — {args.agent} → {parts[0] if parts else '?'}\n\n")
            f.write(f"- **What:** {parts[1] if len(parts) > 1 else ''}\n")
            f.write(f"- **File:** {parts[2] if len(parts) > 2 else ''}\n")
            f.write(f"- **Schema:** {parts[3] if len(parts) > 3 else ''}\n")
        print(f"logged handoff -> handover/LOG.md")

    print("\n== PROSE CHECKLIST (update these next, then re-run the gate) ==")
    hdir = agent_handover_dir(args.agent)
    print(f"  [ ] {hdir}/INDEX.md  — move done->done, name current work at top")
    print(f"  [ ] handover/CHECKPOINTS.md — 'ACTIVE NOW' line, if it changed")
    print(f"  [ ] docs/vision/CORE-BIBLE.md — Layer 3 for {args.cp}, if the status text changed")
    print(f"  [ ] machinelearning/_ACTIVE/CLAIMS.md — update honestly as you claim")
    print("\nThen: python3 handover/check_staleness.py  (must be 0 failures)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
