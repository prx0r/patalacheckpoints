#!/usr/bin/env python3
"""ingest_debate_argument.py — import the reflexivity debate as a DebateArgument gold standard.

The end-goal structure for logical arguments/essays (from research-library LOGICAL-ARGUMENT-1 +
PAPER-FRAME): a claim is a unit with the five-member Nyaaya syllogism + support + commentary +
falsifier + verdict + grade, and arguments PLAY OUT as a live dialectic that resolves.

This ingests LOGICAL-ARGUMENT-1 (the reflexivity debate) as a machine-readable DebateArgument —
the GOLD STANDARD for the debate-argument shape that the Nyaya gate + golds feed. Each round is
a unit with PRATIJNA/HETU/UDAHARANA/UPANAYA/NIGAMANA + SUPPORT + FALSIFIER + VERDICT.
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
SRC = "/root/projects/research-library/LOGICAL-ARGUMENT-1-reflexivity-debate.md"


def parse_round(text: str, round_no: int) -> dict:
    """Parse one debate round into a DebateArgument unit (best-effort from the source structure)."""
    def grab(label):
        # the source uses several forms:
        #   '**THE CLAIM:** value'  (asterisks around label, value after colon+space)
        #   '**THE CLAIM:**value'   (no space)
        #   '**HETU:** value'
        #   '**HETU — value'       (label then em-dash, no colon)
        # 'THE CLAIM' also appears as a section header ('## THE CLAIM' then body).
        patterns = [
            rf"\*\*{label}:\*\*\s*(.+)",          # **LABEL:** value
            rf"\*\*{label}:\s*(.+)",              # **LABEL: value
            rf"\*\*{label}\s*[—-]\s*(.+)",        # **LABEL — value
        ]
        for p in patterns:
            m = re.search(p, text)
            if m:
                return m.group(1).strip().strip("*").strip()
        # fallback: a section header '## THE CLAIM' followed by body on the next non-empty line
        m = re.search(rf"^## {label}\s*$([\s\S]*?)(?=^## |\Z)", text, re.MULTILINE)
        if m:
            body = m.group(1).strip()
            if body:
                return body.splitlines()[0].strip()
        return ""
    verdict = re.search(r"\*\*VERDICT:\*\*\s*\[([a-z-]+)\]", text)
    falsifier = re.search(r"\*\*FALSIFIER:\*\*\s*(.+)", text)
    support = re.search(r"\*\*SUPPORT:\*\*\s*(.+)", text)
    return {
        "round": round_no,
        "title": text.splitlines()[1].replace("**", "").strip() if len(text.splitlines()) > 1 else f"Round {round_no}",
        "pratijna": grab("THE CLAIM"),
        "hetu": grab("HETU"),
        "udaharana": grab("UDAHARANA"),
        "upanaya": grab("UPANAYA"),
        "nigamana": grab("NIGAMANA"),
        "support": support.group(1).strip() if support else "",
        "falsifier": falsifier.group(1).strip() if falsifier else "",
        "verdict": verdict.group(1) if verdict else "open",
    }


def main() -> int:
    text = open(SRC, encoding="utf-8").read()

    # the four candidates
    candidates = []
    cand_rows = re.findall(r"\| `([a-z0-9-]+)` \| (\w+) \(([^)]+)\) \| (.+?) \|", text)
    for cid, trad, author, pos in cand_rows:
        candidates.append({"id": cid, "tradition": trad, "author": author, "position": pos})

    # the seven rounds (split on '## THE DEBATE — ROUND')
    round_chunks = re.split(r"## THE DEBATE — ROUND", text)[1:]
    rounds = [parse_round(c, i + 1) for i, c in enumerate(round_chunks)]

    # the resolution
    res = re.search(r"## THE RESOLUTION.*?NIGAMANA — (.*?)(?:\n\s*\n|\Z)", text, re.DOTALL)
    resolution = re.sub(r"[>#*]", "", res.group(1)).strip() if res else ""

    gold = {
        "gold_id": "DEBATE-REFLEXIVITY",
        "gold_kind": "DebateArgument",
        "title": "The Reflexivity Debate (live dialectic that resolves)",
        "source": "research-library/LOGICAL-ARGUMENT-1-reflexivity-debate.md",
        "question": "Is reflexive awareness intrinsic to experience or a constructed higher-order operation?",
        "candidates": candidates,
        "rounds": rounds,
        "resolution": resolution,
        "review_state": "CANDIDATE",   # machine-imported gold; not independently reviewed
        "status": "MACHINE_PROPOSED",
    }

    out = os.path.join(ROOT, "benchmarks/v0/structure/DEBATE-REFLEXIVITY.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(gold, f, indent=2)

    print(f"IMPORTED DebateArgument gold: {gold['gold_id']}")
    print(f"  candidates: {len(candidates)} | rounds: {len(rounds)}")
    print(f"  resolution: {resolution[:120]}...")
    print(f"\nwritten: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
