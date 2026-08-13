#!/usr/bin/env python3
"""pipeline/factory_status.py — A2-12: the corpus progress dashboard (operational truth).

Produces the single canonical operational view per work that the roadmap (docs/agent2nextdev.md §1.3)
demands — the REGISTRY is authoritative, this is a read-only projection:

  WORK: Kramasadbhāva
    SOURCE       97 / 100
    T1           38 / 42
    ARGMAP       31 / 38
    L0           38 / 38
    L2           29 / 31
    L200         22 / 29
    C1           20 / 22
    FAILED       3 · OPEN 8 · STALE 2 · RETRYABLE 4

Denominator per layer = the objects eligible (SOURCE objects for T1/ARGMAP/L0; upstream commits for
L2/L200/C1). Status classes: committed (current version), superseded (stale), retryable (in the failure
queue), source-blocked.

Usage:
  python3 pipeline/factory_status.py [--work work_id] [--all]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R

FAILURE_QUEUE = Path("/root/projects/patala/data/corpus/downloads/factory-failure-queue.jsonl")

# layer order (canonical) and the upstream it consumes for its denominator
LAYER_ORDER = ["SOURCE", "T1", "ARGMAP", "L0", "L2", "L200", "C1"]
# for counting a layer's denominator we use the number of current objects of its dependency chain
# (SOURCE objects = the work's passages; each downstream layer consumes the prior layer's objects)


def _retryable_ids() -> set:
    ids = set()
    if FAILURE_QUEUE.exists():
        for line in FAILURE_QUEUE.read_text(encoding="utf-8").splitlines():
            try:
                f = json.loads(line)
                ids.add(f.get("object_id", ""))
            except Exception:
                pass
    return ids


def work_status(work_id: str) -> dict:
    """Operational view for one work: per-layer counts + status classes."""
    retryable = _retryable_ids()
    counts = {}
    for L in LAYER_ORDER:
        objects = R._load(L)["objects"]
        cur = [oid for oid, vs in objects.items()
               if oid.startswith(work_id) and not vs[-1].get("superseded")]
        stale = sum(1 for oid, vs in objects.items() if oid.startswith(work_id)
                    for v in vs if v.get("superseded"))
        counts[L] = {"current": len(cur), "stale": stale,
                     "total_versions": sum(len(vs) for oid, vs in objects.items()
                                           if oid.startswith(work_id))}
    # denominator: for SOURCE use current SOURCE objects; downstream = min(prev_current, this layer)
    n_source = counts["SOURCE"]["current"]
    view = {"work": work_id, "layers": {}}
    prev = n_source
    for L in LAYER_ORDER:
        cur = counts[L]["current"]
        view["layers"][L] = {"done": cur, "of": max(prev, cur), "stale": counts[L]["stale"]}
        # for layers after SOURCE, the denominator is the upstream's committed count
        if L != "SOURCE":
            view["layers"][L]["of"] = max(prev, cur)
        prev = cur
    # status classes across all layers
    view["retryable"] = len([i for i in retryable if i.startswith(work_id)])
    view["source_blocked"] = 0  # not yet tracked per passage
    return view


def render(view: dict) -> str:
    lines = [f"WORK: {view['work']}"]
    for L in LAYER_ORDER:
        d = view["layers"][L]
        lines.append(f"  {L:<8} {d['done']:>4} / {d['of']:<4} "
                     f"{'  (stale ' + str(d['stale']) + ')' if d['stale'] else ''}")
    lines.append(f"  RETRYABLE {view['retryable']} · SOURCE_BLOCKED {view['source_blocked']}")
    return "\n".join(lines)


def all_works() -> list[str]:
    works = set()
    for oid in R._load("SOURCE")["objects"]:
        if ":" in oid:
            works.add(oid.split(":")[0])
    return sorted(works)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=None)
    ap.add_argument("--all", action="store_true", help="show all works")
    a = ap.parse_args()
    if a.all:
        for w in all_works():
            print(render(work_status(w)))
            print()
    elif a.work:
        print(render(work_status(a.work)))
    else:
        for w in all_works():
            print(render(work_status(w)))
            print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
