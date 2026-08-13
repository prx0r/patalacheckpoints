#!/usr/bin/env python3
"""pipeline/auto_raw_l0.py — unattended RAW→L0 across the RAW_SANSKRIT backlog.

The 8-hour autonomy runner: iterate the works in the ledger whose next_action is
BUILD_L0_SOURCE_MODE, drive each through the controller L0 (deterministic floor, no
model), commit canonical L0 to the durable registry, and advance the ledger. Crash-safe,
idempotent, fail-closed, and writes a per-run report.

Run DETACHED (do NOT monitor):
    setsid nohup python3 pipeline/auto_raw_l0.py > /tmp/opencode/auto-raw-l0.log 2>&1 < /dev/null &
"""
from __future__ import annotations
import argparse, json, sys, time, hashlib
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import autonomy as A
from l0_worker import source_objects
from agent3_batch import load_raw_source

LEDGER = Path("/root/projects/patala/data/corpus/downloads/translation-state-ledger.json")
REPORT_DIR = Path("/root/projects/patala/data/corpus/downloads/autonomy-reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# only these (RAW_SANSKRIT, source available) are actionable for RAW-L0 now
ACTIONABLE_ACTION = "BUILD_L0_SOURCE_MODE"


def actionable_works() -> list[str]:
    d = json.loads(LEDGER.read_text(encoding="utf-8"))
    return [wid for wid, w in d["works"].items()
            if w["next_action"]["action"] == ACTIONABLE_ACTION and w["source"]["available"]]


def advance_ledger(work_id: str, committed: int, total: int, blocked: int) -> None:
    d = json.loads(LEDGER.read_text(encoding="utf-8"))
    w = d["works"].setdefault(work_id, {})
    w["l0"] = {
        "status": "VERIFIED" if committed > 0 else "ELIGIBLE",
        "reason": f"autonomous RAW-L0: {committed}/{total} committed, {blocked} source-blocked",
    }
    w["next_action"] = {
        "action": "GENERATE_TRANSLATION" if committed > 0 else "BUILD_L0_SOURCE_MODE",
        "eligible_for_agent3": committed > 0,
        "reason": w["l0"]["reason"],
    }
    d["works"][work_id] = w
    LEDGER.write_text(json.dumps(d, indent=2, ensure_ascii=False))


def run_work(work_id: str, max_passages: int) -> dict:
    src = load_raw_source(work_id)
    objs = source_objects(work_id, src)
    if max_passages:
        objs = objs[:max_passages]
    for o in objs:
        if not R.is_committed("SOURCE", o["object_id"], o["input_hash"]):
            R.commit("SOURCE", o["object_id"], o["input_hash"], created_by="auto-raw-l0")
    todo = [o for o in objs if not R.is_committed("L0", o["object_id"], o["input_hash"])]
    # skip genuine lacuna/OCR verses (SOURCE_BLOCKED) without spending effort
    to_run = [o for o in todo if "*" not in o["verse"]]
    blocked = len(todo) - len(to_run)

    t0 = time.time()
    rep = A.tick(layers=["L0"], max_batch=max(8, len(to_run) or 1), dry_run=False, inputs={"L0": to_run})
    wall = round(time.time() - t0, 1)
    committed = len([o for o in to_run if R.is_committed("L0", o["object_id"], o["input_hash"])])
    advance_ledger(work_id, committed, len(objs), blocked)
    return {"work": work_id, "passages": len(objs), "committed": committed,
            "blocked": blocked, "failed": rep["failed"], "wall_s": wall}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--works", nargs="*", default=None, help="specific work_ids (default: all actionable)")
    ap.add_argument("--max-passages", type=int, default=0, help="cap passages per work (0=all)")
    a = ap.parse_args()

    works = a.works or actionable_works()
    R.REG_DIR = Path("/root/projects/patala/data/corpus/registries")
    R.REG_DIR.mkdir(parents=True, exist_ok=True)

    print(f"auto-raw-l0 start: works={len(works)} max_passages={a.max_passages or 'all'} ts={time.strftime('%H:%M:%S')}", flush=True)
    results = []
    t_all = time.time()
    for wid in works:
        print(f"-- work {wid} start {time.strftime('%H:%M:%S')}", flush=True)
        try:
            r = run_work(wid, a.max_passages)
            results.append(r)
            print(f"   {wid}: committed={r['committed']} blocked={r['blocked']} failed={r['failed']} wall={r['wall_s']}s", flush=True)
        except Exception as e:
            print(f"   {wid}: ERROR {str(e)[:200]}", flush=True)
            results.append({"work": wid, "error": str(e)[:200]})

    report = {"ts": time.strftime('%Y-%m-%dT%H:%M:%S'), "total_wall_s": round(time.time() - t_all, 1),
              "works": results,
              "committed_total": sum(r.get("committed", 0) for r in results),
              "blocked_total": sum(r.get("blocked", 0) for r in results)}
    out = REPORT_DIR / f"auto-raw-l0-{int(time.time())}.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps(report, indent=2, ensure_ascii=False), flush=True)
    print("auto-raw-l0 done", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
