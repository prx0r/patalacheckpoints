#!/usr/bin/env python3
"""pipeline/model_catalog.py — the live model catalog (prices from OpenRouter, real tokens → cost).

Makes the projector LEGIT: instead of hardcoded per-verse cost, we (a) pull LIVE per-model prices from
the OpenRouter aggregator (/models returns prompt/completion/cache-read prices per model), and (b) pair
them with REAL token usage captured from a completion (prompt_tokens, completion_tokens, cached_tokens).
cost = prompt_tok × prompt_price + completion_tok × completion_price + cached_tok × cache_price.

Compute-on-write: prices are pulled + cached to data/corpus/model-prices.json (ETag/immutable per the
perf doctrine); the projector reads the cache, never hits the network per request.

This is the honest path: we do NOT maintain prices ourselves — the aggregator does. We add the real
token counts from the adapter. Both together = a true live cost.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(str(Path(__file__).resolve().parents[1]))
CACHE = ROOT / "data" / "corpus" / "model-prices.json"
OPENROUTER_MODELS = "https://openrouter.ai/api/v1/models"
MODELS_DEV = "https://models.dev/models.json"


def _get_json(url: str, timeout: int = 30):
    req = urllib.request.Request(url, headers={"User-Agent": "patala-model-catalog/0.1 (mailto:dev@patala.local)",
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _price_field(pricing: dict, key: str) -> float:
    """OpenRouter prices are strings in $/token."""
    try:
        return float((pricing or {}).get(key, "0") or 0)
    except (TypeError, ValueError):
        return 0.0


def fetch_models_dev() -> dict:
    """The models.dev machine-readable price+capability DB (the reference's 'poll this first')."""
    d = _get_json(MODELS_DEV)
    out = {}
    for mid, rec in d.items():
        price = rec.get("pricing", {}) or {}
        in_ = float(price.get("input", price.get("input_cost_per_mtok")) or 0)
        out_c = float(price.get("output", price.get("output_cost_per_mtok")) or 0)
        cache = float(price.get("cache_read") or 0)
        lim = rec.get("limit")
        out[mid] = {
            # models.dev gives per-M tokens → convert to per-token (match OpenRouter's per-token)
            "prompt_per_token": in_ / 1e6,
            "completion_per_token": out_c / 1e6,
            "cache_read_per_token": cache / 1e6,
            "context_length": lim.get("context") if isinstance(lim, dict) else None,
            "reasoning": bool(rec.get("reasoning")),
            "tool_call": bool(rec.get("tool_call")),
            "open_weights": bool(rec.get("open_weights")),
            "source": "models.dev",
        }
    return out


def fetch_prices() -> dict:
    """Pull live per-model prices from OpenRouter. Returns {model_id: {prompt, completion, cache_read}}."""
    d = _get_json(OPENROUTER_MODELS)
    out = {}
    for m in d.get("data", []):
        p = m.get("pricing", {})
        out[m["id"]] = {
            "prompt_per_token": _price_field(p, "prompt"),
            "completion_per_token": _price_field(p, "completion"),
            "cache_read_per_token": _price_field(p, "input_cache_read"),
            "context_length": m.get("context_length"),
        }
    return out


def refresh_cache() -> dict:
    """Compute-on-write: fetch live prices (models.dev primary, OpenRouter fallback) + cache + provenance."""
    merged = {}
    # models.dev is the reference's recommended primary (capabilities + pricing across providers)
    try:
        merged.update(fetch_models_dev())
    except Exception as _e:
        pass
    # OpenRouter adds live per-token prices for models models.dev misses (and is our router's live source)
    try:
        merged.update(fetch_prices())
    except Exception as _e:
        pass
    cache = {
        "schema": "patala.model-catalog.v1",
        "provider": "models.dev+openrouter",
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "count": len(merged),
        "models": merged,
        "note": "live per-token prices from models.dev (primary) + OpenRouter (fallback); paired with real usage tokens for true cost",
    }
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache, indent=1), encoding="utf-8")
    return cache


def load_prices(force_refresh: bool = False) -> dict:
    """The cached price table (reads cache, never hits network per request)."""
    if force_refresh or not CACHE.exists():
        return refresh_cache()
    try:
        return json.loads(CACHE.read_text(encoding="utf-8"))
    except Exception:
        return refresh_cache()


def price_for(model_id: str) -> dict | None:
    """The price record for a model (by exact id, or fuzzy: id containing the model name)."""
    d = load_prices()
    models = d.get("models", {})
    if model_id in models:
        return models[model_id]
    # fuzzy: e.g. "deepseek-v4-flash" matches "deepseek/deepseek-v4-flash-latest"
    base = model_id.split("/")[-1].lower()
    for mid, rec in models.items():
        if base in mid.lower() or mid.lower().split("/")[-1] in base:
            return rec
    return None


def live_cost(model_id: str, prompt_tokens: int, completion_tokens: int,
              cached_tokens: int = 0) -> dict:
    """cost($) from REAL tokens × LIVE price. Returns the breakdown + whether price was found.

    Caching model: cached prompt tokens are charged at the cache-read price INSTEAD of the fresh
    prompt price (they're part of prompt_tokens). So prompt-cost = (prompt-cached)*prompt_price +
    cached*cache_read_price. This is the honest OpenRouter model.
    """
    p = price_for(model_id)
    if p is None:
        return {"model": model_id, "cost_usd": None, "found_price": False,
                "reason": "no price in catalog (model not on OpenRouter)"}
    cached = min(cached_tokens, prompt_tokens)  # can't cache more than the prompt
    fresh = prompt_tokens - cached
    prompt_cost = fresh * p["prompt_per_token"] + cached * p["cache_read_per_token"]
    completion_cost = completion_tokens * p["completion_per_token"]
    cost = prompt_cost + completion_cost
    return {"model": model_id, "cost_usd": round(cost, 8), "found_price": True,
            "prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens,
            "cached_tokens": cached,
            "breakdown": {"prompt_fresh": round(fresh * p["prompt_per_token"], 8),
                          "cache_read": round(cached * p["cache_read_per_token"], 8),
                          "completion": round(completion_cost, 8)}}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--refresh", action="store_true", help="force a live refresh of prices")
    ap.add_argument("--model", default=None, help="show price for one model")
    ap.add_argument("--cost", nargs=4, metavar=("MODEL", "PROMPT_TOK", "COMP_TOK", "CACHED_TOK"),
                    help="compute a live cost from real tokens")
    a = ap.parse_args()
    if a.refresh:
        c = refresh_cache()
        print(json.dumps({k: c[k] for k in ("provider", "fetched_at", "count")}, indent=1))
        return 0
    if a.cost:
        m, pt, ct, cat = a.cost
        print(json.dumps(live_cost(m, int(pt), int(ct), int(cat)), indent=1))
        return 0
    if a.model:
        print(json.dumps(price_for(a.model), indent=1))
        return 0
    d = load_prices()
    print(f"catalog: {d.get('count')} models (provider={d.get('provider')}, fetched={d.get('fetched_at')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
