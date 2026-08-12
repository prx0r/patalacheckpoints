#!/usr/bin/env python3
"""pipeline/run_autonomous_l0.py — one unattended autonomous RAW-L0 batch (background runner).

Registers a work's passages in the SOURCE registry, then runs the controller tick for L0 through the
real l0_worker (Direct model adapter) — committing only validator-passing canonical L0 objects. Writes
a run report. Run via nohup so it doesn't block the session:
  nohup python3 pipeline/run_autonomous_l0.py --work kramasadbhava --max 40 > data/corpus/downloads/autonomous-l0.log 2>&1 &
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import autonomy as A
from l0_worker import source_objects
from agent3_batch import load_raw_source

REPORT = Path("/root/projects/patala/factory-certificates/L0-v1/autonomous-run.json")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="kramasadbhava")
    ap.add_argument("--max", type=int, default=30)
    a = ap.parse_args()

    # use the REAL registry (durable, canonical)
    R.REG_DIR = Path("/root/projects/patala/data/corpus/registries")
    R.REG_DIR.mkdir(parents=True, exist_ok=True)

    src = load_raw_source(a.work)
    objs = source_objects(a.work, src)[: a.max]
    # register SOURCE objects (idempotent: commit is a no-op shape, but ensure present)
    for o in objs:
        if not R.is_committed("SOURCE", o["object_id"], o["input_hash"]):
            R.commit("SOURCE", o["object_id"], o["input_hash"], created_by="autonomous")
    # skip already-committed L0 (registry-derived idempotency)
    todo = [o for o in objs if not R.is_committed("L0", o["object_id"], o["input_hash"])]
    print(f"work={a.work} source={len(objs)} already_committed={len(objs)-len(todo)} to_run={len(todo)}", flush=True)

    t0 = time.time()
    rep = A.tick(layers=["L0"], max_batch=max(8, len(todo)), dry_run=False, inputs={"L0": todo})
    wall = round(time.time() - t0, 1)

    committed = [o["object_id"] for o in todo if R.is_committed("L0", o["object_id"], o["input_hash"])]
    report = {
        "run_id": f"autonomous-l0-{int(t0)}", "work": a.work,
        "source": len(objs), "attempted": len(todo), "committed": len(committed),
        "failed": rep["failed"], "wall_s": wall, "ts": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps(report, indent=2, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
