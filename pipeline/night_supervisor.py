#!/usr/bin/env python3
"""pipeline/night_supervisor.py — the unattended "translate while I sleep" worker.

Drives the ledger-driven RAW-L0 factory over eligible works in a loop, all night,
fail-closed, logging every verdict + a reviewable per-run record. Run via nohup:
  nohup python3 pipeline/night_supervisor.py > data/corpus/downloads/night-run.log 2>&1 &

Design (per AUTOTRANSLATE-NORTHSTAR Build 6):
  query ledger → pick top eligible RAW_SANSKRIT work → run RAW-L0 + batch gloss +
  validate + commit (auto_run.run_work) → log → advance. One bad work/verse halts +
  logs, never blocks the queue. A work with too many consecutive failures stops the loop.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auto_run import eligible_works, run_work, LEDGER_PATH, LOG_PATH

REVIEW_LOG = Path("/root/projects/patala/data/corpus/downloads/night-review.jsonl")


def log_review(record: dict) -> None:
    record["ts"] = datetime.now(timezone.utc).isoformat()
    with open(REVIEW_LOG, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(json.dumps(record, ensure_ascii=False), flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-verses", type=int, default=50, help="verses per work per run")
    ap.add_argument("--max-works", type=int, default=3, help="works before re-scanning")
    ap.add_argument("--rounds", type=int, default=0, help="0 = run until no eligible work")
    ap.add_argument("--consec-fail-limit", type=int, default=3, help="stop if this many consecutive works hard-fail")
    ap.add_argument("--sleep", type=int, default=30, help="seconds between works")
    a = ap.parse_args()

    log_review({"event": "NIGHT_START", "config": vars(a)})
    consec_fail = 0
    rounds_done = 0
    try:
        while a.rounds == 0 or rounds_done < a.rounds:
            works = eligible_works("smallest")[: a.max_works]
            if not works:
                log_review({"event": "QUEUE_EMPTY", "rounds_done": rounds_done})
                break
            progressed = False
            for wid in works:
                log_review({"event": "WORK_START", "work_id": wid})
                try:
                    s = run_work(wid, a.max_verses)
                except Exception as e:
                    log_review({"event": "WORK_ERROR", "work_id": wid, "error": str(e)[:300]})
                    consec_fail += 1
                    if consec_fail >= a.consec_fail_limit:
                        log_review({"event": "HALT_TOO_MANY_FAILURES", "work_id": wid})
                        return 1
                    continue
                log_review({"event": "WORK_SUMMARY", "work_id": wid, "summary": s})
                if s.get("verses_committed", 0) > 0:
                    progressed = True
                    consec_fail = 0
                else:
                    consec_fail += 1
                if consec_fail >= a.consec_fail_limit:
                    log_review({"event": "HALT_TOO_MANY_FAILURES", "work_id": wid})
                    return 1
                time.sleep(a.sleep)
            if not progressed and a.rounds != 0:
                # in bounded mode, don't spin forever on no progress
                pass
            rounds_done += 1
    except KeyboardInterrupt:
        log_review({"event": "NIGHT_STOPPED", "reason": "interrupt"})
    finally:
        log_review({"event": "NIGHT_END", "rounds_done": rounds_done})
    return 0


if __name__ == "__main__":
    sys.exit(main())
