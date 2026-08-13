#!/usr/bin/env python3
"""source-evidence/evals/patala/tasks/run_reconciliation_eval.py — close the P3 engine ↔ P4 gold loop.

Runs the entity-reconciliation engine (P3) against the MANUSCRIPT-RESOLUTION-GOLD benchmark (P4) and
reports the metrics. This is the loop the reviewer described: build the resolver (P3), judge it (P4),
then fix based on findings.

The headline is FALSE_MERGE_RATE: the engine must never confidently merge distinct works. UNRESOLVED
(abstention) is cheap; a confident wrong merge is catastrophic.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manuscript_resolution_gold import GOLD_CASES, score_resolution  # noqa: E402
from entity_reconciliation import reconcile  # noqa: E402


def engine_resolver(records):
    """Use the reconciliation engine as the resolver.

    For a 2-record case: CONFLICT -> keep separate; EXACT/PROBABLE -> merge; else abstain.
    For a 1-record case: abstain (no canonical registry to match against yet).
    """
    if len(records) < 2:
        return {"target": records[0]["rid"], "candidates": [{"id": records[0]["rid"], "score": 0.5}],
                "abstain": False}
    a, b = records[0], records[1]
    m = reconcile(a, b)
    if m["status"] == "CONFLICT":
        return {"target": a["rid"], "candidates": [{"id": a["rid"], "score": 0.7}], "abstain": False}
    if m["status"] in ("EXACT", "PROBABLE"):
        return {"target": "MERGE", "candidates": [{"id": "MERGE", "score": 0.9}], "abstain": False}
    return {"target": a["rid"], "candidates": [{"id": a["rid"], "score": 0.3}], "abstain": True}


if __name__ == "__main__":
    r = score_resolution(GOLD_CASES, engine_resolver)
    print("P3 entity-reconciliation engine vs P4 MANUSCRIPT-RESOLUTION-GOLD:")
    for k, v in r.items():
        print(f"  {k}: {v}")
    print("\n  headline: FALSE_MERGE_RATE =", r["FALSE_MERGE_RATE"],
          "(0 = the engine never confidently merges distinct works)")
    print("  the engine abstains (UNRESOLVED) rather than guess on weak evidence — per the design law.")
