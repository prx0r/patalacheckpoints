#!/usr/bin/env python3
"""pipeline/factory_batch.py — GOOD-ENOUGH autonomous batch production for each canonical layer.

Agent 2's job: MAKE THE FACTORY RUN. This driver produces MACHINE_PROPOSED objects for the canonical
layers (T1 → L0 → L2 → L200 → C1) over a batch of committed SOURCE objects, committing them to the
registry. It is deliberately SIMPLE and batch-oriented (like auto_translate_raw.py) — good-enough
output per layer, production-gated, NOT over-engineered. Agent 1 sharpens semantic quality later.

Each layer: resolve committed upstream -> run the layer worker -> commit MACHINE_PROPOSED.
Reuses the existing workers (t1_worker, l0_worker, l1_l2_worker, l1_l2_translate, l200_worker,
c1_worker) + the controller's LAYER_HANDLERS. Fail-closed: a layer that can't be produced is skipped,
never fabricated.

Usage:
  python3 pipeline/factory_batch.py --work kramasadbhava [--count 3] [--layers T1,L0,L2,L200,C1]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import autonomy as A


def _source_objects(work_id: str, count: int) -> list[dict]:
    """Committed SOURCE objects for a work: [{object_id, input_hash, verse}].

    The registry SOURCE payload is empty (only input_hash = source_sha256), so the verse text is
    recovered from the live runner's per-work translations file by source_sha256 — the simple,
    good-enough source of raw Sanskrit verses.
    """
    sha_to_verse = {}
    tpath = Path(f"/root/projects/patala/data/corpus/downloads/translations/{work_id}.jsonl")
    if tpath.exists():
        for line in tpath.open(encoding="utf-8"):
            try:
                r = json.loads(line)
                sha_to_verse[r.get("source_sha256")] = r.get("sanskrit", "")
            except Exception:
                pass
    out = []
    for oid in sorted(R._load("SOURCE")["objects"]):
        cur = R.current("SOURCE", oid)
        if not cur or not oid.startswith(work_id):
            continue
        verse = sha_to_verse.get(cur.get("input_hash", ""), "")
        out.append({"object_id": oid, "input_hash": cur.get("input_hash", ""), "verse": verse})
        if len(out) >= count:
            break
    return out


def _register_source(work_id: str, count: int) -> list[dict]:
    """Register SOURCE objects from the live-runner verses if not already present.

    Deduplicates by verse content hash. Returns the registered [{object_id, input_hash, verse}]."""
    tpath = Path(f"/root/projects/patala/data/corpus/downloads/translations/{work_id}.jsonl")
    if not tpath.exists():
        return []
    verses = []
    for line in tpath.open(encoding="utf-8"):
        try:
            r = json.loads(line)
            v = (r.get("sanskrit") or "").strip()
            if v:
                verses.append(v)
        except Exception:
            pass
    out = []
    for i, v in enumerate(verses):
        if count and len(out) >= count:
            break
        oid = f"{work_id}:v{i+1}"
        if R.current("SOURCE", oid):
            cur = R.current("SOURCE", oid)
            out.append({"object_id": oid, "input_hash": cur["input_hash"], "verse": v})
            continue
        import hashlib
        h = hashlib.sha256(v.encode("utf-8")).hexdigest()
        R.commit("SOURCE", oid, h, created_by="factory-batch",
                 payload={"verse": v, "source_text": v})
        out.append({"object_id": oid, "input_hash": h, "verse": v})
    return out


def _commit_proposal(layer: str, p: dict) -> dict:
    """Commit a layer proposal via the controller's handler validator, MACHINE_PROPOSED."""
    handler = A.LAYER_HANDLERS.get(layer)
    if not handler:
        return {"object_id": p.get("object_id"), "layer": layer, "error": "no handler"}
    ok, why = handler["validator"](layer, p)
    if not ok:
        return {"object_id": p.get("object_id"), "layer": layer, "rejected": why}
    payload = {k: v for k, v in p.items() if k not in ("object_id", "input_hash")}
    rec = R.commit(layer, p["object_id"], p.get("input_hash", ""), created_by="factory-batch",
                   status=R.GENERATED, payload=payload)
    return {"object_id": p["object_id"], "layer": layer, "version": rec.get("version")}


def _produce_layer(layer: str, inputs: list[dict], batch_size: int = 4) -> dict:
    """Run a layer's worker over the inputs (bounded), commit each valid proposal.

    A2-11 (Era B): durable failure/retry queues + per-batch isolation.
      - each batch is produced+committed independently (a hung/failed batch never blocks the next)
      - permanent rejections (validator rejection) are recorded as-is
      - transient failures (generator exception / model failure) are recorded in the work's
        RETRYABLE failure queue so the next pass can retry them (idempotency prevents dupes)
    """
    handler = A.LAYER_HANDLERS.get(layer)
    if not handler:
        return {"layer": layer, "error": "no handler"}
    committed, rejected, retryable = [], [], []
    for start in range(0, len(inputs), batch_size):
        batch = inputs[start:start + batch_size]
        try:
            proposals = handler["generator"](layer, batch)
        except Exception as e:
            # transient (e.g. model timeout) -> retryable, don't block neighbors
            for b in batch:
                retryable.append({"object_id": b["object_id"], "layer": layer,
                                  "reason": str(e)[:120]})
            continue
        for p in proposals:
            r = _commit_proposal(layer, p)
            if "version" in r:
                committed.append(r)
            elif "rejected" in r and r["rejected"].startswith("t1_status:GENERATION_FAILED"):
                retryable.append({"object_id": p.get("object_id"), "layer": layer,
                                  "reason": "generation_failed (retryable)"})
            elif "rejected" in r and r["rejected"].startswith("proposal_status:GENERATION_FAILED"):
                retryable.append({"object_id": p.get("object_id"), "layer": layer,
                                  "reason": "generation_failed (retryable)"})
            elif "rejected" in r and r["rejected"].startswith("c1_status:GENERATION_FAILED"):
                retryable.append({"object_id": p.get("object_id"), "layer": layer,
                                  "reason": "generation_failed (retryable)"})
            elif "rejected" in r and r["rejected"].startswith("argmap_status:GENERATION_FAILED"):
                retryable.append({"object_id": p.get("object_id"), "layer": layer,
                                  "reason": "generation_failed (retryable)"})
            else:
                rejected.append(r)
    _record_failures(layer, retryable)
    return {"layer": layer, "committed": committed, "rejected": rejected, "retryable": retryable}


FAILURE_QUEUE = Path("/root/projects/patala/data/corpus/downloads/factory-failure-queue.jsonl")


def _record_failures(layer: str, retryable: list[dict]) -> None:
    """Append retryable failures to the durable queue (the next pass retries them)."""
    if not retryable:
        return
    FAILURE_QUEUE.parent.mkdir(parents=True, exist_ok=True)
    with FAILURE_QUEUE.open("a", encoding="utf-8") as fh:
        for f in retryable:
            fh.write(json.dumps({**f, "ts": __import__("time").strftime('%Y-%m-%dT%H:%M:%S')},
                                ensure_ascii=False) + "\n")


def _retry_failures(work_id: str, layer: str) -> int:
    """Retry retryable failures for a work+layer from the durable queue. Returns # retried.

    Idempotency (registry input-hash) prevents duplicate commits on retry."""
    if not FAILURE_QUEUE.exists():
        return 0
    lines = FAILURE_QUEUE.read_text(encoding="utf-8").splitlines()
    keep, retry = [], []
    for line in lines:
        try:
            f = json.loads(line)
        except Exception:
            continue
        if f.get("layer") == layer and f.get("object_id", "").startswith(work_id):
            retry.append(f)
        else:
            keep.append(line)
    if not retry:
        return 0
    inputs = [{"object_id": f["object_id"],
               "input_hash": (R.current(layer, f["object_id"]) or {}).get("input_hash", "")}
              for f in retry]
    r = _produce_layer(layer, inputs)
    # remove retried (regardless of outcome — a permanent reject is recorded, not looped forever)
    FAILURE_QUEUE.write_text("\n".join(keep) + ("\n" if keep else ""), encoding="utf-8")
    return len(retry)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="kramasadbhava")
    ap.add_argument("--count", type=int, default=3)
    ap.add_argument("--layers", default="T1,ARGMAP,L0,L2,L200,C1")
    ap.add_argument("--retry", action="store_true",
                    help="retry durable retryable failures for this work before producing")
    a = ap.parse_args()
    layers = [l.strip() for l in a.layers.split(",") if l.strip()]

    # retry durable failures first (A2-11: durable failure/retry queue)
    if a.retry:
        for L in layers:
            n = _retry_failures(a.work, L)
            if n:
                print(f"retried {n} {L} failure(s) from the queue", flush=True)

    # register SOURCE if not present, then recover the verse-text inputs
    _register_source(a.work, a.count)
    srcs = _source_objects(a.work, a.count)
    print(f"work={a.work} count={len(srcs)} layers={layers}", flush=True)
    if not srcs:
        print("no committed SOURCE objects found", flush=True)
        return 1

    # T1: produce from SOURCE directly (verses)
    if "T1" in layers:
        r = _produce_layer("T1", srcs)
        print(f"T1: {len(r['committed'])} committed, {len(r['rejected'])} rejected, "
              f"{len(r.get('retryable',[]))} retryable", flush=True)
        for c in r["committed"][:3]:
            print("   ", c["object_id"], c["version"], flush=True)

    # ARGMAP: the lateral guide from committed T1 (reconstruct the argument before L2)
    if "ARGMAP" in layers:
        t1_ids = [oid for oid, vs in R._load("T1")["objects"].items()
                  if not vs[-1].get("superseded") and oid.startswith(a.work)][:a.count]
        r = _produce_layer("ARGMAP", [{"object_id": o, "input_hash": R.current("T1", o)["input_hash"]}
                                      for o in t1_ids])
        print(f"ARGMAP: {len(r['committed'])} committed, {len(r['rejected'])} rejected, "
              f"{len(r.get('retryable',[]))} retryable", flush=True)

    # L0: consume committed T1 (or fall back to source verses via the L0 handler)
    if "L0" in layers:
        t1_ids = [oid for oid, vs in R._load("T1")["objects"].items()
                  if not vs[-1].get("superseded") and oid.startswith(a.work)]
        l0_inputs = [{"object_id": o, "input_hash": R.current("T1", o)["input_hash"],
                      "verse": R.current("T1", o)["payload"]["t1"]["source_text"]}
                     for o in t1_ids[:a.count]]
        r = _produce_layer("L0", l0_inputs or srcs)
        print(f"L0: {len(r['committed'])} committed, {len(r['rejected'])} rejected", flush=True)

    # L2: consume committed L0 via the L1L2/L2 workers
    if "L2" in layers:
        l0_ids = [oid for oid, vs in R._load("L0")["objects"].items()
                  if not vs[-1].get("superseded") and oid.startswith(a.work)][:a.count]
        l2_inputs = [{"object_id": o, "input_hash": R.current("L0", o)["input_hash"]}
                     for o in l0_ids]
        r = _produce_layer("L2", l2_inputs or srcs)
        print(f"L2: {len(r['committed'])} committed, {len(r['rejected'])} rejected", flush=True)

    # L200: consume committed L2
    if "L200" in layers:
        l2_ids = [oid for oid, vs in R._load("L2")["objects"].items()
                  if not vs[-1].get("superseded") and oid.startswith(a.work)][:a.count]
        r = _produce_layer("L200", [{"object_id": o, "input_hash": R.current("L2", o)["input_hash"]}
                                    for o in l2_ids])
        print(f"L200: {len(r['committed'])} committed, {len(r['rejected'])} rejected", flush=True)

    # C1: consume committed L200
    if "C1" in layers:
        l200_ids = [oid for oid, vs in R._load("L200")["objects"].items()
                    if not vs[-1].get("superseded") and oid.startswith(a.work)][:a.count]
        r = _produce_layer("C1", [{"object_id": o, "input_hash": R.current("L200", o)["input_hash"]}
                                  for o in l200_ids])
        print(f"C1: {len(r['committed'])} committed, {len(r['rejected'])} rejected", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
