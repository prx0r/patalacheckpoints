#!/usr/bin/env python3
"""pipeline/factory_scheduler.py — A2-13a: DAG-based backlog scheduler (the corpus OS).

The Era B controller. NOT a T1-only frontier walker — it enumerates ALL eligible (object, layer) jobs
across the whole graph (dependency eligibility from the registry), ranks them, and executes within the
model budget. This is true DAG scheduling:

  find all eligible (object, layer) jobs
    rank
    execute within budget
    repeat

A job (object, layer) is ELIGIBLE when:
  - its upstream layer has a committed object for that passage (from object_registry.PREREQS)
  - it does NOT already have a committed current object for that input
  - it is not source-blocked

Deterministic layers (L0) drain FREE (no model budget). Model-bound layers (T1/ARGMAP/L2/L200/C1)
consume the per-pass budget. Ranking spreads across works and prefers jobs that unlock downstream.

Usage:
  python3 pipeline/factory_scheduler.py [--max-model-calls N] [--throttle S] [--works a,b]
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
import factory_batch as FB
import factory_status as FS
from translation_targets import priority as _target_priority, priority_label

# canonical layer order + the upstream each layer depends on — DERIVED from the canonical DAG
# manifest (contracts/CANONICAL-DAG.yaml) via object_registry.PREREQS. Do NOT hardcode an independent
# UPSTREAM map here (that was the A2-ARCH-HARDEN bug — three competing DAG definitions).
LAYER_ORDER = ["T1", "ARGMAP", "L0", "L2", "L200", "C1"]
MODEL_LAYERS = {"T1", "ARGMAP", "L2", "L200", "C1"}   # L0 is deterministic (free-draining)


def work_priority(work_id: str) -> int:
    """Queue priority of a work (lower = higher). Unknown works = 100 (last)."""
    return _target_priority(work_id)


def _rank_works(by_work: dict) -> list[str]:
    """Order works by target priority (lower value = higher priority, i.e. next-best target).

    Unknown works (not in the translation-target registry) sort to the end (priority 100). Within a
    priority band the round-robin spread below prevents one work from monopolizing the model budget.
    """
    return sorted(by_work.keys(), key=lambda w: (work_priority(w), w))


def _registered_works() -> list[str]:
    works = set()
    for oid in R._load("SOURCE")["objects"]:
        if ":" in oid:
            works.add(oid.split(":")[0])
    return sorted(works)


def _committed_passages(layer: str) -> set[str]:
    return {oid for oid, vs in R._load(layer)["objects"].items()
            if vs and not vs[-1].get("superseded")}


def _eligible_jobs(works: list[str], layers: list[str]) -> list[dict]:
    """Enumerate all eligible (object, layer) jobs across the graph (DAG scheduling).

    A job is eligible when ALL its canonical 'requires' (from the manifest) have a committed object
    for the passage, AND this layer does not yet have a committed current object for it. This is
    MULTI-PARENT eligibility (e.g. L2 requires BOTH L0 AND ARGMAP)."""
    jobs = []
    for layer in layers:
        requires = R.PREREQS.get(layer, [])
        if not requires:
            continue
        done = _committed_passages(layer)
        # the passages whose EVERY required layer is committed
        eligible_ids = None
        for req in requires:
            req_done = _committed_passages(req)
            if eligible_ids is None:
                eligible_ids = set(req_done)
            else:
                eligible_ids &= set(req_done)
        for wid in works:
            for oid in eligible_ids or set():
                if not oid.startswith(wid):
                    continue
                if oid in done:
                    continue
                jobs.append({"object_id": oid, "layer": layer,
                             "requires": requires,
                             "input_hash": ""})   # resolved in _job_input from any parent
    return jobs



def _verse_for(object_id: str) -> str:
    """Recover the SOURCE verse for a passage (T1 needs it)."""
    # from SOURCE registry payload, else live-runner file
    cur = R.current("SOURCE", object_id)
    if cur:
        v = (cur.get("payload", {}) or {}).get("verse") or (cur.get("payload", {}) or {}).get("source_text", "")
        if v:
            return v
    wid = object_id.split(":")[0]
    sha = (cur or {}).get("input_hash", "")
    tpath = Path(f"/root/projects/patala/data/corpus/downloads/translations/{wid}.jsonl")
    if tpath.exists():
        for line in tpath.open(encoding="utf-8"):
            try:
                r = json.loads(line)
                if r.get("source_sha256") == sha:
                    return r.get("sanskrit", "")
            except Exception:
                pass
    return ""


def _job_input(job: dict) -> dict:
    """Resolve the input_hash + verse for a job from its canonical parents (multi-parent DAG).

    The passage's stable input_hash comes from SOURCE (the root); T1 and L0 need the verse text."""
    src = R.current("SOURCE", job["object_id"])
    ih = (src or {}).get("input_hash", "") if src else job.get("input_hash", "")
    inp = {"object_id": job["object_id"], "input_hash": ih}
    if job["layer"] in ("T1", "L0"):
        inp["verse"] = _verse_for(job["object_id"])
    return inp


def _est_tokens(inp: dict) -> int:
    """Rough input-token estimate for a verse job (IAST ~1.5 tok/char + ~40 tok JSON/echo framing)."""
    verse = inp.get("verse") or ""
    return int(len(verse) * 1.5) + 40


def scheduler_pass(works: list[str], layers: list[str], per_layer: int = 2,
                   max_model_calls: int = 6, throttle_s: float = 0.0) -> dict:
    """One DAG pass: enumerate eligible jobs, drain deterministic free, then spend the model budget.

    A2-13a (DAG scheduling): spends model calls across the WHOLE graph, not the lowest incomplete
    layer. A2-13b (free-draining): deterministic L0 jobs run immediately, never consuming the budget."""
    jobs = _eligible_jobs(works, layers)
    if not jobs:
        return {"eligible": 0, "committed": 0, "deterministic": 0, "model_calls": 0,
                "retryable": 0, "rejected": 0, "works": len(works)}

    # rank: spread across works; deterministic layers first (free); prefer unlock-downstream
    # deterministic jobs are free (A2-13b)
    deterministic = [j for j in jobs if j["layer"] not in MODEL_LAYERS]
    model = [j for j in jobs if j["layer"] in MODEL_LAYERS]
    # model ranking: ONE WORK AT A TIME, in TARGET-PRIORITY order (lower priority first). Process the
    # highest-priority work's eligible model jobs first, then the next work. This finishes a work
    # instead of round-robining across 20 (better per-work context consistency + clear completion).
    from collections import defaultdict
    by_work = defaultdict(list)
    for j in model:
        by_work[j["object_id"].split(":")[0]].append(j)
    ranked_model = []
    for w in _rank_works(by_work):
        ranked_model.extend(by_work[w])

    committed, retryable, rejected = [], [], []
    model_calls = 0

    # 1. drain deterministic jobs (free, no budget)
    for j in deterministic[:per_layer]:
        try:
            r = FB._produce_layer(j["layer"], [_job_input(j)], batch_size=1)
            committed += r["committed"]
            rejected += r["rejected"]
            retryable += r.get("retryable", [])
        except Exception as e:
            rejected.append({"object_id": j["object_id"], "layer": j["layer"], "error": str(e)[:100]})

    # 2. spend the model budget across the ranked graph. We ACCUMULATE up to batch_max verses (fills
    #    the context, huge-call throughput), but then SPLIT into independent CHUNKS of chunk_size that
    #    are produced+committed separately. This gives huge per-API-call volume while isolating
    #    failure: a timeout in one chunk loses only that chunk (retryable), not the whole batch.
    # Env: PATALA_CONTEXT / PATALA_INPUT_FRAC (token budget), PATALA_FACTORY_BATCH_MAX (accumulate cap),
    #      PATALA_FACTORY_CHUNK (independent commit size, default 50).
    context = int(os.environ.get("PATALA_CONTEXT", "1000000"))
    input_frac = float(os.environ.get("PATALA_INPUT_FRAC", "0.5"))
    input_budget = int(context * input_frac)
    batch_max = int(os.environ.get("PATALA_FACTORY_BATCH_MAX", "1000"))
    chunk_size = int(os.environ.get("PATALA_FACTORY_CHUNK", "50"))
    consumed = set()   # object_ids already placed in a batch (skip on later iterations)
    for j in ranked_model:
        if model_calls >= max_model_calls:
            break
        if j["object_id"] in consumed:
            continue
        # accumulate same-layer jobs until the batch's estimated INPUT tokens approach the budget
        batch = [_job_input(j)]
        consumed.add(j["object_id"])
        est_input = 900   # fixed prompt overhead (instruction + token grammar)
        est_input += _est_tokens(batch[0])
        work_id = j["object_id"].split(":")[0]
        for k in ranked_model:
            if batch_max and len(batch) >= batch_max:
                break
            if k["object_id"] in consumed:
                continue
            if k["layer"] != j["layer"]:
                continue
            # SINGLE-WORK batching (FIX 2026-08-13): keep every verse in one model call within ONE
            # work. Mixing many works into a single T1 prompt made the model return non-JSON and the
            # whole batch failed closed (retryable) -> ~93% T1 failure rate. Per-work calls match the
            # proven live-runner pattern (auto_translate_raw.py) and kalikarahasya's success, while
            # still filling the context budget with as many of that work's verses as fit.
            if k["object_id"].split(":")[0] != work_id:
                continue
            if est_input + _est_tokens(k) > input_budget:
                break   # context nearly full -> flush
            batch.append(_job_input(k))
            consumed.add(k["object_id"])
            est_input += _est_tokens(k)
        # produce+commit the batch in INDEPENDENT chunks (one API call per chunk, isolated failure).
        # PARALLEL MODEL CALLS: the agentic hermes call is the slow part and only reliably handles a
        # few verses per call, so scale by running the generator (model call) for each chunk in
        # PARALLEL (ThreadPoolExecutor), then commit all proposals SERIALLY in the main thread. This
        # avoids both the single-call hang (small batches) and the registry write race (serial commits).
        # FACTORY_PARALLEL = max concurrent hermes calls.
        parallel = int(os.environ.get("FACTORY_PARALLEL", "4"))
        tasks = []   # (layer, chunk)
        for start in range(0, len(batch), chunk_size):
            if model_calls >= max_model_calls:
                break
            chunk = batch[start:start + chunk_size]
            tasks.append((j["layer"], chunk))
            if j["layer"] in MODEL_LAYERS:
                model_calls += 1   # one API call reserved for this chunk
        if not tasks:
            continue
        from concurrent.futures import ThreadPoolExecutor
        gen_results = {}
        with ThreadPoolExecutor(max_workers=max(1, parallel)) as ex:
            fut_map = {ex.submit(FB._run_generator, layer, chunk): (layer, chunk)
                       for layer, chunk in tasks}
            for fut, (layer, chunk) in fut_map.items():
                try:
                    gen_results[(layer, id(chunk))] = fut.result()
                except Exception as e:
                    rejected.append({"object_id": chunk[0]["object_id"], "layer": layer,
                                     "error": str(e)[:100]})
        # commit serially (safe: no concurrent registry writes)
        for layer, chunk in tasks:
            proposals = gen_results.get((layer, id(chunk)))
            if proposals is None:
                continue
            r = FB._commit_proposals(layer, chunk, proposals)
            committed += r["committed"]
            rejected += r["rejected"]
            retryable += r["retryable"]
            if throttle_s:
                time.sleep(throttle_s)

    return {"eligible": len(jobs), "committed": len(committed),
            "deterministic": len(deterministic),
            "model_calls": model_calls,
            "retryable": len(retryable), "rejected": len(rejected),
            "committed_detail": [c["object_id"] for c in committed][:20],
            "works": len(works)}


def queue_preview(works: list[str], layers: list[str]) -> dict:
    """Show the prioritized next-best-target ordering (read-only; no production).

    Returns the eligible model jobs ordered as the scheduler will spend budget on them, grouped with
    their work's priority tier. Use to confirm the factory picks the right targets first."""
    jobs = _eligible_jobs(works, layers)
    model = [j for j in jobs if j["layer"] in MODEL_LAYERS]
    from collections import defaultdict
    by_work = defaultdict(list)
    for j in model:
        by_work[j["object_id"].split(":")[0]].append(j)
    order = _rank_works(by_work)
    grouped = []
    for w in order:
        grouped.append({
            "work": w,
            "priority": work_priority(w),
            "tier": priority_label(w),
            "jobs": sorted(by_work[w], key=lambda j: LAYER_ORDER.index(j["layer"])),
        })
    return {"model_jobs": len(model), "works_ordered": grouped}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-works", type=int, default=0, help="0=all registered works")
    ap.add_argument("--per-layer", type=int, default=2, help="jobs per layer per pass")
    ap.add_argument("--layers", default=",".join(LAYER_ORDER))
    ap.add_argument("--works", default=None, help="comma-separated work ids (else all)")
    ap.add_argument("--max-model-calls", type=int, default=6)
    ap.add_argument("--throttle", type=float, default=0.0)
    ap.add_argument("--retry", action="store_true", help="retry durable failures first")
    ap.add_argument("--queue", action="store_true",
                    help="show the prioritized next-best-target ordering (read-only, no production)")
    a = ap.parse_args()
    layers = [l.strip() for l in a.layers.split(",") if l.strip()]

    if a.retry:
        for L in layers:
            n = FB._retry_failures("", L)
            if n:
                print(f"retried {n} {L} failure(s)", flush=True)

    works = [w.strip() for w in a.works.split(",") if w.strip()] if a.works else _registered_works()
    if a.max_works:
        works = works[:a.max_works]

    if a.queue:
        pv = queue_preview(works, layers)
        print(f"PRIORITIZED QUEUE: {pv['model_jobs']} eligible model jobs across "
              f"{len(pv['works_ordered'])} works", flush=True)
        for w in pv["works_ordered"]:
            layers_avail = ",".join(sorted({j["layer"] for j in w["jobs"]}))
            print(f"  p{w['priority']:>3} [{w['tier']:<28}] {w['work']:<40} -> {layers_avail}",
                  flush=True)
        return 0

    print(f"scheduler DAG pass: works={len(works)} layers={layers} "
          f"budget={a.max_model_calls} throttle={a.throttle}", flush=True)
    r = scheduler_pass(works, layers, per_layer=a.per_layer,
                       max_model_calls=a.max_model_calls, throttle_s=a.throttle)
    print(f"DAG pass done: {r}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
