#!/usr/bin/env python3
"""check_debate_argument.py — validate a DebateArgument gold standard.

A DebateArgument (the end-goal structure for logical arguments, from the reflexion debate) is a
live dialectic: candidates contend through rounds, each round is a unit with a syllogism core
(pratijna/hetu) + support + falsifier + verdict, and the debate resolves.

What is REQUIRED (the validator enforces):
  - gold_kind == DebateArgument
  - >=2 candidates (the contenders)
  - >=3 rounds (the dialectic)
  - each round has: round number, pratijna, hetu, verdict (the syllogism spine + honesty)
  - a resolution (the debate ends honestly)

What is REPORTED (not fabricated): how many rounds state all five members vs only the core
(udaharana/upanaya/nigamana may be implied in some rounds — reported, not required).
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
VALID_VERDICTS = {"accepted", "accepted-with-risk", "open", "refuted"}


def check_debate(path: str) -> dict:
    problems = []
    with open(path, encoding="utf-8") as f:
        d = json.load(f)

    if d.get("gold_kind") != "DebateArgument":
        problems.append("gold_kind != DebateArgument")
    if len(d.get("candidates", [])) < 2:
        problems.append("need >= 2 candidates")
    rounds = d.get("rounds", [])
    if len(rounds) < 3:
        problems.append("need >= 3 rounds")
    for r in rounds:
        if not r.get("round"):
            problems.append(f"round missing 'round': {r}")
        if not r.get("pratijna"):
            problems.append(f"round {r.get('round')}: missing pratijna")
        if not r.get("hetu"):
            problems.append(f"round {r.get('round')}: missing hetu")
        if r.get("verdict") not in VALID_VERDICTS:
            problems.append(f"round {r.get('round')}: invalid verdict {r.get('verdict')}")
    if not d.get("resolution"):
        problems.append("missing resolution")

    full_members = sum(1 for r in rounds
                       if r.get("udaharana") and r.get("upanaya") and r.get("nigamana"))
    return {"ok": len(problems) == 0, "problems": problems,
            "n_candidates": len(d.get("candidates", [])),
            "n_rounds": len(rounds),
            "full_syllogism_rounds": full_members}


def main() -> int:
    path = os.path.join(ROOT, "benchmarks/v0/structure/DEBATE-REFLEXIVITY.json")
    r = check_debate(path)
    print("DEBATE-REFLEXIVITY gold standard:")
    print(f"  candidates: {r['n_candidates']} | rounds: {r['n_rounds']} "
          f"| full-syllogism rounds: {r['full_syllogism_rounds']}")
    if r["ok"]:
        print("  VALID: live dialectic with candidates, rounds, verdicts, resolution.")
    else:
        print("  INVALID:")
        for p in r["problems"]:
            print(f"    ✗ {p}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
