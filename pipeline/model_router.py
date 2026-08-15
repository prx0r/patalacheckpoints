#!/usr/bin/env python3
"""pipeline/model_router.py — the intelligent model router (tiered providers, quota swap, quality floor).

Picks the CHEAPEST AVAILABLE provider for each translation, using ALL possible inference sources
before paid flash, and auto-swaps when a provider's quota/rate-limit is hit — WITHOUT sacrificing
quality.

The tier ladder (most of the user's vision):
  TIER 0  FREE      Cloudflare Workers AI (daily neurons, e.g. 10k/day)  — free, swap on daily limit
  TIER 1  DISCOUNTED opencode-go aggregator (26 models, cheaper than DeepSeek direct)
  TIER 2  MARKET    OpenRouter (live per-token prices, 413 models)

Selection is (a) cost-aware (cheapest available tier that meets the quality floor) and (b) quality-aware
(a hard/rare verse must go to a quality-floor model even if a cheaper one exists). Quota/429 → mark the
provider exhausted for this batch → move to the next tier. Every decision is logged (routing log).

Pure stdlib. Quality scores from data/model-quality.json (IndicParam). Prices from model_catalog.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(str(Path(__file__).resolve().parents[1]))
if str(ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(ROOT / "pipeline"))

QUALITY_FILE = ROOT / "data" / "model-quality.json"
ROUTING_LOG = ROOT / "data" / "corpus" / "routing-log.jsonl"

# ---- the provider tier ladder (the free-first policy) ----
PROVIDERS = {
    "cloudflare": {
        "tier": 0, "kind": "free",
        "base_url": "https://api.cloudflare.com/client/v4/accounts/{account}/ai/run/{model}",
        "env_key": "CLOUDFLARE_AI_API_KEY", "env_account": "CLOUDFLARE_AI_ACCOUNT_ID",
        "daily_quota": 10000,  # neurons/day (Workers AI free tier) — configurable
        "models": ["@cf/qwen/qwen1.5-14b-awq"],
        "note": "free daily neurons; needs an AI-scoped token (the R2 token is S3-only)."
    },
    "opencode-go": {
        "tier": 1, "kind": "discounted",
        "base_url": os.environ.get("OPENCODE_GO_BASE_URL", "https://opencode.ai/zen/go/v1"),
        "env_key": "OPENCODE_GO_API_KEY",
        "daily_quota": None,  # no hard quota; rate-limits only
        # cheap models first (cost-ordered); strong models (deepseek-v4-pro) available for the floor
        "models": ["qwen3.7-flash", "deepseek-v4-flash", "deepseek-v4-pro", "glm-5.2", "kimi-k3"],
        "note": "the current provider; cheaper than DeepSeek direct."
    },
    "openrouter": {
        "tier": 2, "kind": "market",
        "base_url": "https://openrouter.ai/api/v1",
        "env_key": "OPENROUTER_API_KEY",
        "daily_quota": None,
        # cheap first; strong models (gemini, gpt) for the quality floor
        "models": ["qwen/qwen3.7-flash", "deepseek/deepseek-v4-flash-0731",
                   "deepseek/deepseek-v4-pro-0813", "google/gemini-3.7-flash", "openai/gpt-5.6-luna-pro"],
        "note": "live per-token prices; the price source of record."
    },
}

# the opencode-go vs DeepSeek-direct discount note (user's observation, encoded)
# (per-verse market prices from model_catalog: qwen3.7-flash $0.0011 vs deepseek-v4-flash $0.0035)


def _load_quality() -> dict:
    try:
        return json.loads(QUALITY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"models": {}, "min_translation_quality": 40.0}


def quality_for(model_id: str) -> float:
    """The IndicParam-style Sanskrit quality score for a model (conservative default if unknown)."""
    q = _load_quality()
    models = q.get("models", {})
    base = model_id.split("/")[-1].lower().replace("latest", "").strip()
    # exact
    if base in models:
        return models[base].get("sanskrit", 25.0)
    # fuzzy: match by distinctive token
    for name, rec in models.items():
        if name in base or base.split("-")[0] in name:
            return rec.get("sanskrit", 25.0)
    return models.get("unknown_default", {}).get("sanskrit", 25.0)


class Router:
    """Manages the provider tiers + quota + per-request selection."""

    def __init__(self, providers: dict | None = None, quality_file: Path | None = None):
        self.providers = providers or PROVIDERS
        self.quality = _load_quality()
        self._exhausted: set[str] = set()          # providers out of quota this batch
        self._quota_left: dict[str, float] = {}    # provider -> remaining (for free tiers)
        self.calls = 0

    def _avail(self, provider: str) -> bool:
        if provider in self._exhausted:
            return False
        p = self.providers[provider]
        key = os.environ.get(p["env_key"], "")
        if not key:
            # unkeyed provider: only skip if it's NOT the aggregator we already use (opencode-go key
            # lives in the hermes profile env, not the shell — treat missing-shell-key as still tryable)
            if provider != "opencode-go":
                return False
        if p["kind"] == "free" and not key:
            return False  # free tier needs a token we don't have yet
        if p.get("daily_quota") is not None:
            left = self._quota_left.get(provider, p["daily_quota"])
            return left > 0
        return True

    def _mark_used(self, provider: str, units: float = 1.0):
        p = self.providers[provider]
        if p.get("daily_quota") is not None:
            left = self._quota_left.get(provider, p["daily_quota"])
            self._quota_left[provider] = max(0.0, left - units)

    def exhaust(self, provider: str, reason: str):
        """Call on 429 / QUOTA_EXCEEDED — mark the provider out for this batch."""
        self._exhausted.add(provider)
        self._log({"event": "exhausted", "provider": provider, "reason": reason, "ts": time.time()})

    def order(self, min_quality: float = 0.0, quality_required: float | None = None) -> list[str]:
        """Providers available, ordered cheap→expensive, filtered by the quality floor."""
        available = [pid for pid in self.providers if self._avail(pid)]
        # quality floor: a provider is usable for the given task only if its best model clears the floor
        # (or quality not required → use all)
        def usable(pid):
            if quality_required is None:
                return True
            best = max((quality_for(m) for m in self.providers[pid]["models"]), default=0.0)
            return best >= quality_required
        return sorted([pid for pid in available if usable(pid)],
                      key=lambda pid: self.providers[pid]["tier"])

    def pick(self, quality_required: float | None = None) -> tuple[str | None, str | None]:
        """Cheapest available provider (+ its best model) that meets the quality floor."""
        for pid in self.order(quality_required=quality_required):
            p = self.providers[pid]
            models = p["models"]
            # within a provider, prefer the cheapest model that clears the floor
            best_model = None
            for m in models:
                if quality_required is None or quality_for(m) >= quality_required:
                    best_model = m
                    break
            if best_model:
                return pid, best_model
        return None, None

    def log_call(self, provider: str, model: str, cost_usd: float | None,
                 tokens_in: int, tokens_out: int, quality: float):
        self._log({"event": "call", "provider": provider, "model": model,
                   "cost_usd": cost_usd, "tokens_in": tokens_in, "tokens_out": tokens_out,
                   "quality": quality, "ts": time.time()})

    def _log(self, rec: dict):
        ROUTING_LOG.parent.mkdir(parents=True, exist_ok=True)
        with ROUTING_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")

    def reset(self):
        self._exhausted.clear()
        self._quota_left.clear()
        self.calls = 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--quality-required", type=float, default=None,
                    help="the quality floor (IndicParam score, 0-100); providers below it are skipped")
    ap.add_argument("--batch", type=int, default=5, help="simulate a batch of N selections")
    ap.add_argument("--providers", action="store_true", help="print the provider tier ladder")
    a = ap.parse_args()

    if a.providers:
        for pid, p in PROVIDERS.items():
            print(f"  T{p['tier']} {pid:<12} kind={p['kind']:<10} models={len(p['models'])} "
                  f"quota={p.get('daily_quota')}")
        return 0

    r = Router()
    print(f"=== ROUTER: batch of {a.batch}, quality_required={a.quality_required} ===")
    for i in range(a.batch):
        pid, model = r.pick(a.quality_required)
        if pid is None:
            print(f"  {i}: NO AVAILABLE PROVIDER (all exhausted or below quality floor)")
            break
        q = quality_for(model)
        print(f"  {i}: → {pid}/{model}  (quality {q}%, cost-ordered)")
        # simulate: some requests hit the free quota → swap
        if pid == "cloudflare" and i == 2:
            r.exhaust(pid, "QUOTA_EXCEEDED (daily neurons)")
            print(f"  {i}: [cloudflare quota hit → will swap next]")
    print(f"\n  exhausted this batch: {r._exhausted}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
