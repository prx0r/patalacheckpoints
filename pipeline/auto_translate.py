#!/usr/bin/env python3
"""pipeline/auto_translate.py — the AI translation factory driver (8-hour autonomous run).

Consumes committed L0 objects (the 687 already built) and drives the model through
GENERATE_TRANSLATION: committed L0 -> bounded model batch -> L1/L2 MACHINE_PROPOSED ->
validate provenance -> commit -> advance ledger -> next passage. Runs unattended for hours.

Guarantees:
  - idempotent (committed L1L2 skipped; replay = 0 new)
  - fail-closed (wrong passage / empty / malformed / hash mismatch -> FAIL, never commit)
  - bounded batches (PATALA_BC) so one bad/timeout passage never blocks neighbors
  - MACHINE_PROPOSED (never ACCEPTED); provenance recorded
  - L0 is never overwritten by model output
  - writes a per-run report + a durable checkpoint so it can resume

Run DETACHED (do NOT monitor):
    setsid nohup python3 pipeline/auto_translate.py --works kramasadbhava > /tmp/opencode/auto-translate.log 2>&1 < /dev/null &
"""
from __future__ import annotations
import argparse, json, sys, time
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import autonomy as A

LEDGER = Path("/root/projects/patala/data/corpus/downloads/translation-state-ledger.json")
REPORT_DIR = Path("/root/projects/patala/data/corpus/downloads/autonomy-reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)
CKPT = Path("/root/projects/patala/data/corpus/downloads/auto-translate-checkpoint.json")


def committed_l0_for(work_id: str) -> list[dict]:
    """All committed L0 objects for a work (input hash + object_id), newest per object."""
    seen = {}
    for line in (R.REG_DIR / "l0-registry.jsonl").open(encoding="utf-8"):
        rec = json.loads(line)
        if rec.get("object_id", "").startswith(f"{work_id}:") and not rec.get("superseded"):
            seen[rec["object_id"]] = rec["input_hash"]
    return [{"object_id": oid, "input_hash": h} for oid, h in seen.items()]


def run_work(work_id: str, max_passages: int) -> dict:
    l0objs = committed_l0_for(work_id)
    if max_passages:
        l0objs = l0objs[:max_passages]
    # idempotency: skip already-translated (L1L2 committed for the same input hash)
    todo = [o for o in l0objs if not R.is_committed("L1L2", o["object_id"], o["input_hash"])]
    print(f"  {work_id}: L0_eligible={len(l0objs)} already_translated={len(l0objs)-len(todo)} to_run={len(todo)}", flush=True)
    if not todo:
        return {"work": work_id, "eligible": len(l0objs), "committed": 0, "failed": 0, "skipped": len(l0objs)}

    t0 = time.time()
    # bounded per-tick batches so the controller loops through the whole set unattended
    rep = A.tick(layers=["L1L2"], max_batch=int(__import__("os").environ.get("PATALA_BC", "6")),
                 dry_run=False, inputs={"L1L2": todo})
    wall = round(time.time() - t0, 1)
    committed = len([o for o in todo if R.is_committed("L1L2", o["object_id"], o["input_hash"])])
    return {"work": work_id, "eligible": len(todo), "committed": committed,
            "failed": rep["failed"], "wall_s": wall}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--works", nargs="*", default=None)
    ap.add_argument("--max-passages", type=int, default=0)
    ap.add_argument("--loops", type=int, default=1, help="controller passes over the set (0=forever)")
    a = ap.parse_args()

    R.REG_DIR = Path("/root/projects/patala/data/corpus/registries")
    R.REG_DIR.mkdir(parents=True, exist_ok=True)

    # resume checkpoint
    if CKPT.exists():
        prev = json.loads(CKPT.read_text())
        print(f"resuming from checkpoint: committed_so_far={prev.get('committed_total')}", flush=True)

    # derive default work set from committed L0 in the registry
    works = a.works
    if not works:
        seen = set()
        for line in (R.REG_DIR / "l0-registry.jsonl").open(encoding="utf-8"):
            rec = json.loads(line)
            oid = rec.get("object_id", "")
            if ":" in oid and not rec.get("superseded"):
                seen.add(oid.split(":")[0])
        works = sorted(seen)

    print(f"auto-translate start: works={len(works)} loops={a.loops or 'forever'} ts={time.strftime('%H:%M:%S')}", flush=True)
    t_all = time.time()
    grand_committed = 0
    grand_failed = 0
    all_results = []
    loop = 0
    while True:
        loop += 1
        print(f"-- loop {loop} --", flush=True)
        for wid in works:
            try:
                r = run_work(wid, a.max_passages)
                all_results.append(r)
                grand_committed += r["committed"]
                grand_failed += r["failed"]
                print(f"   {wid}: committed={r['committed']} failed={r['failed']} wall={r['wall_s']}s", flush=True)
            except Exception as e:
                print(f"   {wid}: ERROR {str(e)[:160]}", flush=True)
                all_results.append({"work": wid, "error": str(e)[:160]})
        if a.loops and loop >= a.loops:
            break
        # between unattended loops, persist checkpoint (crash-safe resume)
        CKPT.write_text(json.dumps({"committed_total": grand_committed, "last_loop": loop}))
        time.sleep(2)

    report = {"ts": time.strftime('%Y-%m-%dT%H:%M:%S'), "loops": loop,
              "total_wall_s": round(time.time() - t_all, 1),
              "committed_total": grand_committed, "failed_total": grand_failed,
              "works": all_results}
    out = REPORT_DIR / f"auto-translate-{int(time.time())}.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps(report, indent=2, ensure_ascii=False), flush=True)
    print("auto-translate done", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
