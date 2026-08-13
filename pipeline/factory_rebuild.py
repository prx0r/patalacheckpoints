#!/usr/bin/env python3
"""pipeline/factory_rebuild.py — Era C: supersession propagation + targeted regeneration (A2-14/15/16).

The living rebuild engine: when one upstream scholarly object is corrected (e.g. T1:v4 supersedes
T1:v3), this determines exactly which downstream objects are affected and regenerates ONLY those.

Compiler semantics (docs/agent2nextdev.md §3):
  source change        -> rebuild all dependent
  T1 correction        -> rebuild L0 onward
  ARGMAP correction    -> rebuild L2 onward
  L2 correction        -> rebuild L200/C1
  scholar review only  -> change status, not regenerate

Mechanics:
  1. DEPENDENCY GRAPH — the canonical layer DAG (from object_registry.PREREQS):
       T1<-SOURCE  L0<-T1  ARGMAP<-T1  L2<-{L1,ARGMAP}  L200<-L2  C1<-L200
  2. INVALIDATE — when an object at layer L changes, every downstream layer's object for the same
     passage_id is marked STALE (supersede) + recorded for regeneration.
  3. REGENERATE — re-run the affected downstream layers through the scheduler's producer (bounded,
     idempotent).

Returns the affected-object map so a scholar/ImpactReport sees exactly what was invalidated+rebuilt.

Usage:
  python3 pipeline/factory_rebuild.py --object t1-kramasadbhava:v1-v3 --dry-run
"""
from __future__ import annotations

import argparse
import sys

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import factory_batch as FB
import factory_scheduler as FS

# DOWNSTREAM is DERIVED from the canonical DAG manifest (contracts/CANONICAL-DAG.yaml) via
# object_registry.PREREQS — do NOT hardcode an independent map (the A2-ARCH-HARDEN bug).


def _downstream_of() -> dict[str, list[str]]:
    """Compute, for each layer, the layers that transitively depend on it (from the manifest)."""
    prereqs = R.PREREQS
    # direct: layer -> layers that require it
    direct = {L: [] for L in prereqs}
    for layer, reqs in prereqs.items():
        for req in reqs:
            direct.setdefault(req, []).append(layer)
    # transitive closure
    downstream = {L: set() for L in direct}
    for start in direct:
        stack = list(direct[start])
        seen = set()
        while stack:
            d = stack.pop()
            if d in seen:
                continue
            seen.add(d)
            downstream[start].add(d)
            stack.extend(direct.get(d, []))
    return {k: sorted(v) for k, v in downstream.items()}


DOWNSTREAM: dict[str, list[str]] = _downstream_of()


def _passage_id(object_id: str) -> str:
    """Extract the passage id (drop the layer-version suffix like 'l0-...-v1')."""
    # object_id is e.g. 't1-kramasadbhava:v1-v3' OR 'kramasadbhava:v1'
    if object_id.startswith(("t1-", "l0-", "argmap-", "l1-", "l2-", "l200-", "c1-")):
        # 'l0-kramasadbhava:v1-v3' -> 'kramasadbhava:v1'
        rest = object_id.split("-", 1)[1]
        return rest.rsplit("-", 1)[0]
    return object_id


def _layer_of(object_id: str) -> str | None:
    for layer in ("T1", "ARGMAP", "L0", "L1", "L2", "L200", "C1"):
        if object_id.startswith(layer.lower() + "-"):
            return layer
    return None


def invalidate(object_id: str) -> dict:
    """Mark the object's downstream as stale (supersede) + return the affected map.

    Affected = {downstream_layer: [passage_ids]} for every layer downstream of the object's layer."""
    layer = _layer_of(object_id)
    passage = _passage_id(object_id)
    if not layer:
        return {"error": f"cannot determine layer of {object_id}"}
    affected = {}
    for down in DOWNSTREAM.get(layer, []):
        cur = R.current(down, passage)
        if cur:
            superseded = R.supersede(down, passage)
            affected[down] = {"passage": passage, "superseded": superseded}
    return {"object": object_id, "layer": layer, "passage": passage, "affected": affected}


def regenerate(object_id: str, per_layer: int = 3, dry_run: bool = False) -> dict:
    """Regenerate only the affected downstream layers for the passage (targeted, bounded)."""
    layer = _layer_of(object_id)
    passage = _passage_id(object_id)
    if not layer:
        return {"error": "cannot determine layer"}
    rebuilt = {}
    # for each downstream layer, if it now has no current (non-superseded) object AND all its
    # canonical 'requires' are committed, regenerate it (targeted, bounded).
    for down in DOWNSTREAM.get(layer, []):
        if R.current(down, passage):
            continue  # still has a current version -> nothing to rebuild
        # canonical multi-parent eligibility: all 'requires' committed for this passage
        requires = R.PREREQS.get(down, [])
        if requires and not all(R.current(req, passage) for req in requires):
            rebuilt[down] = "DEPENDENCY_BLOCKED (a required parent not current)"
            continue
        # build the single-passage input via the scheduler (verse + input_hash from SOURCE)
        inp = FS._job_input({"object_id": passage, "layer": down})
        if dry_run:
            rebuilt[down] = "WOULD_REBUILD"
            continue
        try:
            r = FB._produce_layer(down, [inp], batch_size=2)
            rebuilt[down] = f"{len(r['committed'])} committed, {len(r.get('retryable',[]))} retryable"
        except Exception as e:
            rebuilt[down] = f"ERROR: {str(e)[:80]}"
    return {"object": object_id, "rebuilt": rebuilt}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--object", required=True, help="the changed object id, e.g. t1-kramasadbhava:v1-v3")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    inv = invalidate(a.object)
    print("INVALIDATE:", inv, flush=True)
    if not a.dry_run:
        print("REGENERATE:", regenerate(a.object, dry_run=False), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
