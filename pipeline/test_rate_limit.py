#!/usr/bin/env python3
"""pipeline/test_rate_limit.py — deterministic tests for resource/rate limiting (A2-10).

Verifies the scheduler's model-call budget:
  - a global max-model-calls budget stops advancing once exhausted
  - model_calls is tracked accurately
  - the budget is per-pass (a later pass continues)
Run: python3 pipeline/test_rate_limit.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import factory_batch as FB
import factory_scheduler as FS
import t1_worker as TW


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def main() -> int:
    ok = True
    R.REG_DIR = Path(tempfile.mkdtemp())
    FB.FAILURE_QUEUE = Path(tempfile.mkdtemp()) / "q.jsonl"
    TW.chat = lambda s, p, **kw: '{"tokens": {"śivo": {"gloss":"x"}}}'

    print("=== A2-10 resource/rate limiting ===")
    for w in ("a", "b", "c"):
        for i in (1, 2):
            R.commit("SOURCE", f"{w}:v{i}", f"{w}h{i}", created_by="test",
                     payload={"verse": "śivo", "source_text": "śivo"})

    # budget of 2 model calls -> only work 'a' (2 verses) advances; b/c skipped
    r = FS.scheduler_pass(["a", "b", "c"], ["T1"], per_layer=2, max_model_calls=2)
    ok &= t("budget limits advance to 1 work", r["advanced"] == 1, f"advanced={r['advanced']}")
    ok &= t("model_calls tracked = 2", r["model_calls"] == 2, f"{r['model_calls']}")
    a_t1 = [o for o, vs in R._load("T1")["objects"].items() if o.startswith("a")]
    b_t1 = [o for o, vs in R._load("T1")["objects"].items() if o.startswith("b")]
    ok &= t("work a advanced", len(a_t1) == 2, f"{a_t1}")
    ok &= t("work b did NOT advance (budget)", len(b_t1) == 0)

    # a later pass with a fresh budget continues (b now advances)
    r2 = FS.scheduler_pass(["a", "b", "c"], ["T1"], per_layer=2, max_model_calls=4)
    b_t1 = [o for o, vs in R._load("T1")["objects"].items() if o.startswith("b")]
    ok &= t("later pass continues (budget resets per pass)", len(b_t1) == 2, f"b={b_t1}")

    print("\n" + ("RATE-LIMIT ALL PASS" if ok else "RATE-LIMIT SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
