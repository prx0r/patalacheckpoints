#!/usr/bin/env python3
"""pipeline/factory_scheduler.py — A2-8/A2-9: the backlog scheduler + multi-work execution.

The Era B controller: advances ALL registered works through the canonical stack automatically, one
layer at a time, using the failure/retry queue + the progress dashboard. This turns the factory into
the autonomous corpus compiler — the Era B exit (continuously turn a backlog into SOURCE→C1 objects).

Strategy per pass (bounded, unattended-safe):
  1. enumerate works with committed SOURCE (the backlog)
  2. for each work, find its FRONTIER via factory_status (the first layer not fully done)
  3. advance that one layer (a bounded batch), then move to the next work (fair, one layer each pass)
  4. record retryable failures (A2-11) for a later pass
This keeps the system advancing without ever wedging on one work.

Usage:
  python3 pipeline/factory_scheduler.py [--max-works N] [--per-layer N] [--layers T1,ARGMAP,L0,L2,L200,C1]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import factory_batch as FB
import factory_status as FS

LAYER_ORDER = ["T1", "ARGMAP", "L0", "L2", "L200", "C1"]
# model-bound layers (need rate limiting); L0 is deterministic (no model)
MODEL_LAYERS = {"T1", "ARGMAP", "L2", "L200", "C1"}


def _registered_works() -> list[str]:
    works = set()
    for oid in R._load("SOURCE")["objects"]:
        if ":" in oid:
            works.add(oid.split(":")[0])
    return sorted(works)


def _frontier(work_id: str) -> str | None:
    """The first layer whose done count < its upstream count (the work's next action)."""
    try:
        view = FS.work_status(work_id)
    except Exception:
        return None
    layers = view["layers"]
    for L in LAYER_ORDER:
        d = layers.get(L, {})
        done, of = d.get("done", 0), d.get("of", 0)
        if of and done < of:
            return L
    return None


def _upstream_inputs(work_id: str, layer: str, limit: int) -> list[dict]:
    """Inputs for a layer: the committed upstream objects of the dependency chain, up to limit."""
    # determine the upstream layer
    upstream = {"T1": "SOURCE", "ARGMAP": "T1", "L0": "T1",
                "L2": "L1", "L200": "L2", "C1": "L200"}[layer]
    ids = [oid for oid, vs in R._load(upstream)["objects"].items()
           if not vs[-1].get("superseded") and oid.startswith(work_id)][:limit]
    out = []
    for o in ids:
        cur = R.current(upstream, o)
        if not cur:
            continue
        item = {"object_id": o, "input_hash": cur["input_hash"]}
        # T1 consumes the SOURCE verse directly (the generator needs the verse text)
        if upstream == "SOURCE":
            verse = (cur.get("payload", {}) or {}).get("verse") or \
                    (cur.get("payload", {}) or {}).get("source_text", "")
            if not verse:
                # fall back to the live-runner translations file (some SOURCE payloads are empty)
                verse = _verse_from_runner(work_id, cur["input_hash"])
            item["verse"] = verse
        out.append(item)
    return out


def _verse_from_runner(work_id: str, source_sha: str) -> str:
    tpath = Path(f"/root/projects/patala/data/corpus/downloads/translations/{work_id}.jsonl")
    if not tpath.exists():
        return ""
    for line in tpath.open(encoding="utf-8"):
        try:
            r = json.loads(line)
            if r.get("source_sha256") == source_sha:
                return r.get("sanskrit", "")
        except Exception:
            pass
    return ""


def scheduler_pass(work_ids: list[str], layers: list[str], per_layer: int,
                   max_model_calls: int = 20, throttle_s: float = 0.0) -> dict:
    """One bounded pass over the works: advance each work's frontier by one layer.

    A2-10 (resource/rate limiting): model-bound layers are paced — a global budget of model calls per
    pass (max_model_calls) + an optional throttle between model-bound batches (throttle_s) so the
    factory doesn't starve the shared model API (the live runner) or hit rate limits. L0 (deterministic)
    is never throttled."""
    advanced, done, errors, model_calls = 0, 0, [], 0
    for wid in work_ids:
        if model_calls >= max_model_calls:
            break  # budget exhausted this pass — a later pass continues
        frontier = _frontier(wid)
        if frontier is None or frontier not in layers:
            done += 1
            continue
        inputs = _upstream_inputs(wid, frontier, per_layer)
        if not inputs:
            done += 1
            continue
        try:
            r = FB._produce_layer(frontier, inputs, batch_size=2)
            advanced += 1
            n_retry = len(r.get("retryable", []))
            print(f"  {wid}: advanced {frontier} "
                  f"({len(r['committed'])} committed, {len(r['rejected'])} rejected, "
                  f"{n_retry} retryable)", flush=True)
            if frontier in MODEL_LAYERS:
                model_calls += len(inputs)
                if throttle_s:
                    time.sleep(throttle_s)
        except Exception as e:
            errors.append({"work": wid, "layer": frontier, "error": str(e)[:120]})
    return {"works_scanned": len(work_ids), "advanced": advanced, "fully_done": done,
            "model_calls": model_calls, "errors": errors}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-works", type=int, default=0, help="0=all registered works")
    ap.add_argument("--per-layer", type=int, default=3, help="passages per layer per work per pass")
    ap.add_argument("--layers", default=",".join(LAYER_ORDER))
    ap.add_argument("--works", default=None, help="comma-separated work ids (else all)")
    ap.add_argument("--max-model-calls", type=int, default=20,
                    help="A2-10: global model-call budget per pass (rate limiting)")
    ap.add_argument("--throttle", type=float, default=0.0,
                    help="A2-10: seconds to sleep between model-bound batches")
    ap.add_argument("--retry", action="store_true",
                    help="retry durable retryable failures for all works first (A2-11)")
    a = ap.parse_args()
    layers = [l.strip() for l in a.layers.split(",") if l.strip()]

    if a.retry:
        for L in layers:
            n = FB._retry_failures("", L)
            if n:
                print(f"retried {n} {L} failure(s) from the queue", flush=True)

    works = [w.strip() for w in a.works.split(",") if w.strip()] if a.works else _registered_works()
    if a.max_works:
        works = works[:a.max_works]
    print(f"scheduler pass: works={len(works)} layers={layers} per-layer={a.per_layer} "
          f"max-model-calls={a.max_model_calls} throttle={a.throttle}", flush=True)
    r = scheduler_pass(works, layers, a.per_layer,
                       max_model_calls=a.max_model_calls, throttle_s=a.throttle)
    print(f"pass done: advanced={r['advanced']} fully_done={r['fully_done']} "
          f"model_calls={r['model_calls']} errors={len(r['errors'])}", flush=True)
    for e in r["errors"]:
        print("  ERROR:", e, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
