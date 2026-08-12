#!/usr/bin/env python3
"""check_research_pack.py — validate a ResearchPack: it is a composition/projection layer.

Every ResearchPack must:
  1. be inquiry-specific (has a research_question + thesis)
  2. reference existing objects by ref (argument/theme/proposition/evidence), NOT copy content
  3. have a dependency graph (so revisions can propagate)
  4. carry an honest review_summary (composition/source_grounding/argument_review/themes/scholarly_review)
  5. NOT claim scholarly validity (scholarly_validated must be false unless genuinely reviewed)

A pack may be useful while provisional — that is the point. It is a coherent reconstruction of the
evidence/reasoning we currently have, not the accepted interpretation.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

REQUIRED_TOP = ["pack_id", "research_question", "thesis", "scope", "theme_refs",
                "argument_refs", "evidence_refs", "dependency_graph", "review_summary"]


def check_pack(path: str) -> dict:
    problems = []
    with open(path, encoding="utf-8") as f:
        p = json.load(f)

    for k in REQUIRED_TOP:
        if k not in p:
            problems.append(f"missing top-level '{k}'")

    rs = p.get("review_summary", {})
    if not rs.get("composition") or not rs.get("scholarly_review"):
        problems.append("review_summary must state composition + scholarly_review")
    if rs.get("scholarly_validated") is True:
        problems.append("scholarly_validated=true is not allowed unless a genuine review is recorded")

    # evidence refs: each must be a ref object, not copied content
    for e in p.get("evidence_refs", []):
        if isinstance(e, dict) and not (e.get("ref") or e.get("kind")):
            problems.append(f"evidence ref malformed: {e}")

    # dependency graph: each edge has child/edge/parent
    for e in p.get("dependency_graph", []):
        for k in ("child", "edge", "parent"):
            if k not in e:
                problems.append(f"dependency edge missing '{k}': {e}")

    return {"ok": len(problems) == 0, "problems": problems}


def main() -> int:
    packs_dir = os.path.join(ROOT, "benchmarks/v0/packs")
    any_fail = False
    for fn in sorted(os.listdir(packs_dir)):
        if not fn.endswith(".json"):
            continue
        r = check_pack(os.path.join(packs_dir, fn))
        print(f"{'✓' if r['ok'] else '✗'} {fn}" + (f" — {r['problems']}" if not r["ok"] else ""))
        if not r["ok"]:
            any_fail = True
    print("\nRESULT: " + ("FAIL" if any_fail else "PASS (all ResearchPacks well-formed)"))
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
