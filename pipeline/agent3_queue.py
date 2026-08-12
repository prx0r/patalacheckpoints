#!/usr/bin/env python3
"""pipeline/agent3_queue.py — the Agent 3 work QUEUE (the autonomous factory loop).

Per handover/hermes/AUTOTRANSLATE-NORTHSTAR.md, the endgame is "a queue-processing problem":
  CORPUS LEDGER → NEXT_VALID_ACTION → Agent3 → RAW-L0 → AUDIT → COMMIT VERSION → next

This scans the corpus-state ledger for works whose next action is RAW-L0-eligible
(RAW_SANSKRIT / BUILD_L0_SOURCE_MODE / ELIGIBLE), and for each, processes the next
untranslated passage(s), committing each L0 version to the version registry + updating
the ledger. One work at a time; a failing work halts (does not corrupt the queue).

This is the missing "queue raw works + track L0 versions" piece.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent3_batch import load_raw_source, split_verses
from raw_l0 import raw_l0
from l0_registry import commit_l0, l0_versions, summary as registry_summary
from corpus_state import next_valid_action, WorkState
from translation_targets import order_queue, priority_label, all_targets, priority, tier, status

LEDGER_PATH = "/root/projects/patala/data/corpus/downloads/translation-state-ledger.json"
QUEUE_STATE_PATH = "/root/projects/patala/data/corpus/downloads/agent3-queue-state.json"


def eligible_works() -> list[str]:
    """Works in the ledger whose next action is RAW-L0-eligible (a queue candidate).

    Ordered by the translation-target priority (expansion docs): the Krama packet first,
    then tier-1 complete-Sanskrit corpora, then tier-0/2, then tier-3 flagships.
    """
    ledger = json.load(open(LEDGER_PATH))
    eligible = []
    for wid, w in ledger["works"].items():
        src = w.get("source") or {}
        fmt = src.get("format", "UNKNOWN")
        if fmt == "RAW_SANSKRIT":
            eligible.append(wid)
    return order_queue(eligible)


def load_queue_state() -> dict:
    if os.path.exists(QUEUE_STATE_PATH):
        return json.load(open(QUEUE_STATE_PATH))
    return {"by_work": {}}


def save_queue_state(st: dict) -> None:
    with open(QUEUE_STATE_PATH, "w") as fh:
        json.dump(st, fh, indent=2, ensure_ascii=False)


def next_passage(work_id: str, state: dict) -> tuple[str, int] | None:
    """The next untranslated verse index for a work (resume-after-failure)."""
    verses = split_verses(load_raw_source(work_id))
    done = state.get("by_work", {}).get(work_id, {}).get("done_verses", set())
    for i, v in enumerate(verses):
        if i not in done:
            return v, i
    return None


def process_next(work_id: str, committed_by: str = "agent3", max_verses: int = 5) -> dict:
    """Process the next untranslated passage(s) for a work, committing each L0 version."""
    state = load_queue_state()
    work_state = state.setdefault("by_work", {}).setdefault(work_id, {"done_verses": [], "commits": []})
    verses = split_verses(load_raw_source(work_id))
    done = set(work_state["done_verses"])   # JSON round-trips sets -> lists; coerce back

    processed = []
    count = 0
    for i, verse in enumerate(verses):
        if i in done or count >= max_verses:
            continue
        passage_id = f"{work_id}:v{i+1}"
        res = raw_l0(work_id, passage_id, verse)
        # commit the L0 version (immutable, superseding)
        commit = commit_l0(work_id, res["records"], committed_by, n_verses=1)
        work_state["commits"].append({"passage_id": passage_id, "commit": commit,
                                      "proof_pass": res["proof"].get("PASS")})
        done.add(i)
        count += 1
        processed.append({"passage_id": passage_id, "commit": commit,
                          "proof_pass": res["proof"].get("PASS")})

    # persist queue state (done_verses as list for JSON)
    work_state["done_verses"] = sorted(done)
    save_queue_state(state)

    # reflect in the corpus ledger
    ledger = json.load(open(LEDGER_PATH))
    if work_id in ledger["works"]:
        ledger["works"][work_id]["l0"]["status"] = "ELIGIBLE"
        ledger["works"][work_id]["l0"]["version"] = registry_summary().get(work_id, {}).get("current")
        with open(LEDGER_PATH, "w") as fh:
            json.dump(ledger, fh, indent=2, ensure_ascii=False)

    return {"work_id": work_id, "processed": processed, "remaining": len(verses) - len(done),
            "queue": list(eligible_works())}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Agent 3 work queue: process next RAW-L0 passage(s)")
    ap.add_argument("--work", default=None, help="specific work, else first eligible")
    ap.add_argument("--max-verses", type=int, default=5)
    ap.add_argument("--by", default="agent3")
    ap.add_argument("--list", action="store_true", help="list eligible works")
    ap.add_argument("--registry", action="store_true", help="show the full prioritized target registry (the huge queue)")
    a = ap.parse_args()

    if a.registry:
        reg = all_targets()
        rows = [{"work_id": wid, **meta, "label": priority_label(wid)} for wid, meta in reg.items()]
        print(json.dumps({"registry_size": len(rows), "targets": rows}, indent=2))
        sys.exit(0)

    if a.list:
        print(json.dumps({"eligible_raw_l0_works": eligible_works()}, indent=2))
        sys.exit(0)

    work = a.work or (eligible_works()[0] if eligible_works() else None)
    if not work:
        print("no eligible RAW-L0 works")
        sys.exit(1)
    r = process_next(work, a.by, a.max_verses)
    print(json.dumps(r, indent=2, ensure_ascii=False))
