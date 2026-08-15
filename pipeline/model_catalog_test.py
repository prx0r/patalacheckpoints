#!/usr/bin/env python3
"""pipeline/model_catalog_test.py — proof for the live model catalog (real tokens × live price).
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/model_catalog_test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "pipeline"))

import model_catalog as MC  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("MODEL-CATALOG — proof (live prices + real-token cost)\n")

    d = MC.load_prices()
    gate("catalog loaded", d.get("count", 0) > 0, f"{d.get('count')} models (provider={d.get('provider')})")

    # a known model has a price record with positive prices
    p = MC.price_for("qwen/qwen3.7-plus")
    gate("qwen3.7-plus priced", p is not None and p["prompt_per_token"] > 0,
         f"prompt={p['prompt_per_token']}/tok" if p else "no price")

    # fuzzy match: 'deepseek-v4-flash' resolves
    pf = MC.price_for("deepseek-v4-flash")
    gate("fuzzy model match", pf is not None and pf["prompt_per_token"] > 0,
         f"found {pf and pf.get('completion_per_token')}")

    # live cost from real tokens
    c = MC.live_cost("qwen/qwen3.7-plus", 32, 1194, 0)
    gate("live cost computed", c["found_price"] and c["cost_usd"] is not None and c["cost_usd"] > 0,
         f"${c['cost_usd']:.6f}")
    gate("cost scales with tokens", MC.live_cost("qwen/qwen3.7-plus", 64, 1194, 0)["cost_usd"]
         > MC.live_cost("qwen/qwen3.7-plus", 32, 1194, 0)["cost_usd"],
         "double prompt → higher cost")
    gate("cache-read reduces cost", MC.live_cost("qwen/qwen3.7-plus", 32, 1194, 32)["cost_usd"]
         <= MC.live_cost("qwen/qwen3.7-plus", 32, 1194, 0)["cost_usd"],
         "cached tokens cheaper than fresh")

    # unknown model → found_price False (honest, not a fake number)
    u = MC.live_cost("nonexistent-model", 100, 100, 0)
    gate("unknown model is honest", u["found_price"] is False and u["cost_usd"] is None)

    # the projector uses live prices for a catalog model
    try:
        import project_translation as PT
        p = PT.project("matrkabhedatantra", model="qwen/qwen3.7-plus")
        gate("projector uses live pricing", p["pricing_source"] == "live-openrouter", p["pricing_source"])
        gate("projector live cost present", p["total_cost_miss_usd"] > 0,
             f"${p['total_cost_miss_usd']} miss for {p['total_verses']} verses")
    except Exception as e:
        gate("projector uses live pricing", False, str(e)[:60])

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
