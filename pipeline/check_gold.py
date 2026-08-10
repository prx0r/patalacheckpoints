#!/usr/bin/env python3
"""Gold-fixture regression check — does the current published translation satisfy
the expert-reviewed gold expectations?

This is the scholarly regression gate (the nirānanda lesson): it catches when a
pipeline/prompt change silently turns an OPEN crux into CONSTRAINED, or drops an
alternative, or ungrounds a decision's evidence. It proves the EVALUATION, not the
software contract.
"""
from __future__ import annotations
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_gold() -> list[dict]:
    txt = open(os.path.join(BASE, "data", "corpus", "gold.ts"), encoding="utf-8").read()
    golds = []
    for m in re.finditer(r'\{\s*id:\s*"([^"]+)",\s*\n\s*passage:\s*"([^"]+)",\s*\n\s*source_span:\s*"([^"]+)",', txt):
        golds.append({"id": m.group(1), "passage": m.group(2), "source_span": m.group(3)})
    return golds


def load_published() -> str:
    return open(os.path.join(BASE, "data", "corpus", "units", "kramasadbhava-1.8-published.ts"), encoding="utf-8").read()


def check() -> list[str]:
    problems = []
    golds = load_gold()
    pub = load_published()
    for g in golds:
        if "nirānanda" in g["source_span"] or "nirananda" in g["source_span"]:
            # the nirānanda decision must be OPEN (not CONSTRAINED)
            m = re.search(r'id:\s*"(pt:decision:krs:1.8:LEX:2)"[^{}]*?status:\s*"([^"]+)"', pub)
            status = m.group(2) if m else "?"
            if status != "OPEN":
                problems.append(f"GOLD nirānanda: expected OPEN, got {status} (must not be falsely settled)")
            # must keep the technical alternative
            if "bliss at rest" not in pub and "stillness" not in pub:
                problems.append("GOLD nirānanda: technical alternative missing")
            # evidence_state must be partially_grounded
            em = re.search(r'id:\s*"(pt:decision:krs:1.8:LEX:2)"[^{}]*?evidence_state:\s*"([^"]+)"', pub)
            es = em.group(1) if em else "?"
            if es != "partially_grounded":
                problems.append(f"GOLD nirānanda: expected partially_grounded evidence_state, got {es}")
        if "devadeveśi" in g["source_span"] or "devadevesi" in g["source_span"]:
            m = re.search(r'id:\s*"(pt:decision:krs:1.8:LEX:1)"[^{}]*?status:\s*"([^"]+)"', pub)
            status = m.group(1) if m else "?"
            if status == "OPEN":
                problems.append("GOLD devadeveśi: expected not-OPEN (compound resolved)")
    # all evidence references resolve (no dangling)
    evidence_ids = set(re.findall(r'id:\s*"(pt:evidence:[^"]+)"', pub))
    for m in re.finditer(r'evidence_id:\s*"(pt:evidence:[^"]+)"', pub):
        if m.group(1) not in evidence_ids:
            problems.append(f"dangling evidence reference {m.group(1)}")
    return problems


def report() -> str:
    problems = check()
    lines = [f"Gold-fixture regression: {len(problems)} failures"]
    for p in problems:
        lines.append(f"  [FAIL] {p}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(report())
