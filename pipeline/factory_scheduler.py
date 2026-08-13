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
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import factory_batch as FB
import factory_status as FS

LAYER_ORDER = ["T1", "ARGMAP", "L0", "L2", "L200", "C1"]


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
            item["verse"] = verse
        out.append(item)
    return out


def scheduler_pass(work_ids: list[str], layers: list[str], per_layer: int) -> dict:
    """One bounded pass over the works: advance each work's frontier by one layer."""
    advanced, done, errors = 0, 0, []
    for wid in work_ids:
        frontier = _frontier(wid)
        if frontier is None:
            done += 1  # fully advanced
            continue
        if frontier not in layers:
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
        except Exception as e:
            errors.append({"work": wid, "layer": frontier, "error": str(e)[:120]})
    return {"works_scanned": len(work_ids), "advanced": advanced, "fully_done": done, "errors": errors}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-works", type=int, default=0, help="0=all registered works")
    ap.add_argument("--per-layer", type=int, default=3, help="passages per layer per work per pass")
    ap.add_argument("--layers", default=",".join(LAYER_ORDER))
    ap.add_argument("--works", default=None, help="comma-separated work ids (else all)")
    a = ap.parse_args()
    layers = [l.strip() for l in a.layers.split(",") if l.strip()]

    works = [w.strip() for w in a.works.split(",") if w.strip()] if a.works else _registered_works()
    if a.max_works:
        works = works[:a.max_works]
    print(f"scheduler pass: works={len(works)} layers={layers} per-layer={a.per_layer}", flush=True)
    r = scheduler_pass(works, layers, a.per_layer)
    print(f"pass done: advanced={r['advanced']} fully_done={r['fully_done']} errors={len(r['errors'])}",
          flush=True)
    for e in r["errors"]:
        print("  ERROR:", e, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
