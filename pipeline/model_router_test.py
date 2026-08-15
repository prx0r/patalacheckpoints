#!/usr/bin/env python3
"""pipeline/model_router_test.py — proof for the intelligent model router.
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/model_router_test.py
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "pipeline"))

import model_router as MR  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("MODEL-ROUTER — proof (tiered providers, quota swap, quality floor)\n")

    # quality scores load + rank correctly
    gate("quality_for known model", MR.quality_for("gemini-2.5") > 50, f"{MR.quality_for('gemini-2.5')}%")
    gate("quality_for unknown is conservative", MR.quality_for("weird-model-xyz") < 30,
         f"{MR.quality_for('weird-model-xyz')}%")

    # tier ladder is free-first
    tiers = {pid: p["tier"] for pid, p in MR.PROVIDERS.items()}
    gate("free tier is T0", tiers.get("cloudflare") == 0, "cloudflare first")
    gate("discounted is before market", tiers.get("opencode-go") < tiers.get("openrouter"))

    # with a CF key, the free tier is used first (no floor)
    os.environ["CLOUDFLARE_AI_API_KEY"] = "fake"
    r = MR.Router()
    pid, model = r.pick()
    gate("free tier used first (when keyed)", pid == "cloudflare", f"{pid}/{model}")

    # quality floor: hard verse routes to a strong model
    r2 = MR.Router()
    pid2, model2 = r2.pick(quality_required=50)
    gate("quality floor picks strong model", MR.quality_for(model2) >= 50 if model2 else False,
         f"{model2} ({MR.quality_for(model2)}%)" if model2 else "none")

    # quota swap: exhaust the free tier → moves to next
    r3 = MR.Router()
    first, _ = r3.pick()
    r3.exhaust("cloudflare", "QUOTA_EXCEEDED")
    second, _ = r3.pick()
    gate("quota swap moves off exhausted provider", second != "cloudflare" and first == "cloudflare",
         f"{first} -> {second}")
    gate("exhausted provider recorded", "cloudflare" in r3._exhausted)

    # exhausted-everything → honest 'no provider' (fail-closed)
    r4 = MR.Router()
    for pid in MR.PROVIDERS:
        r4.exhaust(pid, "all down")
    p5, _ = r4.pick()
    gate("all-exhausted returns None (fail-closed)", p5 is None)

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
