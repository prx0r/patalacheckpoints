#!/usr/bin/env python3
"""pipeline/project_translation.py — the translation PROJECTOR (ingestion-ROI estimator).

Per the benchmark+projector thesis (infra-deepdive/13): "load a stack → with this model, it costs X,
takes Y." This is the INGESTION-side use: given a work's verse count (streamed from the SOURCE registry /
harvested <work>.jsonl), project the real cost + time + model calls to translate it.

  per-verse (measured, per model) × verse_count(work) × scenario(batch, parallel) = cost + time + calls

The per-verse numbers are the thesis's MEASURED defaults (from the progress registry + e2e-trace + the
DeepSeek pricing reference), made configurable so a real measured run can override them. This feeds the
assess-flow T5 priority (ingestion ROI: is it worth ingesting/translating this work?).

Deterministic, stdlib-only, streams verse counts (low-RAM per AXIOMS).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(str(Path(__file__).resolve().parents[1]))

# ---- the per-verse model defaults (from infra-deepdive/13, the measured values) ----
# cost per verse = 5 model calls (T1, ARGMAP, L2, L200, C1) on ~15k-in/5k-out chars.
MODELS = {
    "deepseek-v4-flash": {
        "per_verse_time_s": 325.0,   # measured default
        "per_verse_cost_miss": 0.000875,   # $ cache-miss
        "per_verse_cost_hit": 0.000361,    # $ cache-hit
        "calls_per_verse": 5,
    },
    "deepseek-v4-pro": {
        "per_verse_time_s": 290.0,   # faster but pricier (thesis: pro ≈ 3× cost)
        "per_verse_cost_miss": 0.0026,
        "per_verse_cost_hit": 0.0011,
        "calls_per_verse": 5,
    },
}


def verse_counts(work_id: str | None = None) -> dict[str, int]:
    """Stream verse counts per work from the harvested <work>.jsonl files (low-RAM)."""
    d = ROOT / "data" / "corpus" / "downloads" / "translations"
    if not d.exists():
        return {}
    out = {}
    for f in d.glob("*.jsonl"):
        c = sum(1 for _ in open(f, encoding="utf-8", errors="ignore"))
        if c:
            out[f.stem] = c
    if work_id and work_id in out:
        return {work_id: out[work_id]}
    return out if not work_id else {}


def project(work_id: str | None = None, model: str = "deepseek-v4-flash",
            batch: int = 1, parallel: int = 1) -> dict:
    """Project cost/time/calls for one work or the whole corpus.

    Cost uses LIVE prices from the aggregator (model_catalog, compute-on-write) when available,
    falling back to the measured per-verse defaults. Time/calls stay from the measured per-verse model.
    """
    if model not in MODELS:
        # allow a live-catalog model even if not in our defaults (cost live, time default)
        try:
            from model_catalog import price_for
            if price_for(model) is None:
                raise ValueError(f"unknown model {model}")
        except Exception:
            raise ValueError(f"unknown model {model}; known: {list(MODELS)}")
    m = MODELS.get(model, MODELS["deepseek-v4-flash"])
    # live per-token prices (None-safe): cost per verse estimated on ~15k-in/5k-out chars
    live_pt = live_completion = live_cache = None
    try:
        from model_catalog import price_for
        p = price_for(model)
        if p:
            live_pt, live_completion, live_cache = p["prompt_per_token"], p["completion_per_token"], p["cache_read_per_token"]
    except Exception:
        pass
    counts = verse_counts(work_id)
    rows = []
    for wid, verses in sorted(counts.items(), key=lambda x: -x[1]):
        calls = verses * m["calls_per_verse"]
        eff_calls = calls / batch
        hours = (verses * m["per_verse_time_s"] / batch / parallel) / 3600
        # live cost if we have aggregator prices (assume ~15k prompt / 5k completion tokens per verse,
        # 0 cached for the miss estimate; cache-hit uses the cache-read price on the full prompt)
        if live_pt is not None:
            prompt_tok = verses * 15000
            comp_tok = verses * 5000
            # miss: all prompt fresh; hit: all prompt cached at the cache-read price
            cost_miss = prompt_tok * live_pt + comp_tok * live_completion
            cost_hit = prompt_tok * live_cache + comp_tok * live_completion
        else:
            cost_miss = verses * m["per_verse_cost_miss"]
            cost_hit = verses * m["per_verse_cost_hit"]
        rows.append({"work": wid, "verses": verses, "calls": int(round(eff_calls)),
                     "hours": round(hours, 1),
                     "cost_miss_usd": round(cost_miss, 4), "cost_hit_usd": round(cost_hit, 4)})
    total_verses = sum(r["verses"] for r in rows)
    live_pricing = live_pt is not None
    return {
        "model": model, "batch": batch, "parallel": parallel,
        "works": len(rows), "total_verses": total_verses,
        "total_calls": int(round(sum(r["calls"] for r in rows))),
        "total_hours": round(sum(r["hours"] for r in rows), 1),
        "total_cost_miss_usd": round(sum(r["cost_miss_usd"] for r in rows), 4),
        "total_cost_hit_usd": round(sum(r["cost_hit_usd"] for r in rows), 4),
        "rows": rows,
        "pricing_source": "live-openrouter" if live_pricing else "hardcoded-defaults",
        "note": "cost uses LIVE per-token prices from OpenRouter (compute-on-write) when available; "
                "time/calls from the measured per-verse model",
    }


def render(p: dict) -> str:
    lines = [f"=== PROJECTION: {p['works']} works | model={p['model']} "
             f"(batch={p['batch']}/call, parallel={p['parallel']}) ==="]
    lines.append(f"{'work':<30} {'verses':>6} {'calls':>6} {'hours':>7} {'$ (miss)':>9} {'$ (hit)':>9}")
    for r in p["rows"]:
        lines.append(f"{r['work']:<30} {r['verses']:>6} {r['calls']:>6} {r['hours']:>7} "
                     f"{r['cost_miss_usd']:>9.4f} {r['cost_hit_usd']:>9.4f}")
    lines.append(f"TOTAL: {p['total_verses']} verses | {p['total_calls']} calls | "
                 f"~{p['total_hours']} hrs | ${p['total_cost_miss_usd']:.2f} (miss) / "
                 f"${p['total_cost_hit_usd']:.2f} (hit)")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--work", default=None, help="project one work (else the whole corpus)")
    ap.add_argument("--model", default="deepseek-v4-flash",
                    help="model id (a known default or any live OpenRouter model id, e.g. qwen/qwen3.7-plus)")
    ap.add_argument("--batch", type=int, default=1, help="verses per model call")
    ap.add_argument("--parallel", type=int, default=1, help="parallel works")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    p = project(a.work, a.model, a.batch, a.parallel)
    if a.json:
        print(json.dumps(p, indent=2, ensure_ascii=False))
    else:
        print(render(p))
    return 0


if __name__ == "__main__":
    sys.exit(main())
