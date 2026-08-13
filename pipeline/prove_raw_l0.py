#!/usr/bin/env python3
"""pipeline/prove_raw_l0.py — drive REAL autonomous RAW→L0 through the controller, once.

Commit actual canonical L0 objects for kramasadbhava verses to the durable registry, then write a
JSON report (the CP2 evidence). Run DETACHED (nohup/setsid), do NOT monitor; read the report later:
    setsid nohup python3 pipeline/prove_raw_l0.py --work kramasadbhava --max 6 \
        > /tmp/opencode/raw-l0-prove.log 2>&1 < /dev/null &
"""
from __future__ import annotations
import argparse, json, sys, time
from pathlib import Path
sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import autonomy as A
from l0_worker import source_objects
from agent3_batch import load_raw_source

REPORT = Path("/root/projects/patala/factory-certificates/L0-v1/raw-l0-v1.json")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="kramasadbhava")
    ap.add_argument("--max", type=int, default=6)
    a = ap.parse_args()

    R.REG_DIR = Path("/root/projects/patala/data/corpus/registries")
    R.REG_DIR.mkdir(parents=True, exist_ok=True)

    src = load_raw_source(a.work)
    objs = source_objects(a.work, src)[: a.max]
    for o in objs:
        if not R.is_committed("SOURCE", o["object_id"], o["input_hash"]):
            R.commit("SOURCE", o["object_id"], o["input_hash"], created_by="raw-l0")
    todo = [o for o in objs if not R.is_committed("L0", o["object_id"], o["input_hash"])]
    print(f"work={a.work} source={len(objs)} already_committed={len(objs)-len(todo)} to_run={len(todo)}", flush=True)

    t0 = time.time()
    rep = A.tick(layers=["L0"], max_batch=max(8, len(todo)), dry_run=False, inputs={"L0": todo})
    wall = round(time.time() - t0, 1)

    committed = [o["object_id"] for o in todo if R.is_committed("L0", o["object_id"], o["input_hash"])]

    # inspect one committed object's records for the honest report
    n_records = n_parsed = n_glossed = n_amb = 0
    for oid in committed:
        cur = R.current("L0", oid)
        if not cur:
            continue
        recs = cur.get("payload", {}).get("records", [])
        n_records += len(recs)
        n_parsed += sum(1 for r in recs if r.get("status") == "PARSED")
        n_amb += sum(1 for r in recs if r.get("status") == "AMBIGUOUS")
        n_glossed += sum(1 for r in recs if r.get("literal_gloss"))

    report = {
        "checkpoint": "CP2 AUTONOMOUS RAW-L0 v1",
        "work": a.work, "attempted": len(todo), "committed": len(committed),
        "failed": rep.get("failed", 0), "wall_s": wall,
        "records_committed": n_records, "parsed": n_parsed, "ambiguous": n_amb, "glossed": n_glossed,
        "ts": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps(report, indent=2, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
