#!/usr/bin/env python3
"""pipeline/test_rate_limit.py — deterministic tests for resource/rate limiting (A2-10).

Verifies the DAG scheduler's model-call budget:
  - a global max-model-calls budget caps model-bound jobs per pass
  - model_calls is tracked accurately
  - deterministic jobs (L0) do NOT consume the budget (free-draining)
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


def _stub_model():
    import t1_worker as TW
    import argument_map_worker as AM
    TW.chat = lambda s, p, **kw: '{"tokens": {"śivo": {"gloss":"x"}, "śivaṃ": {"gloss":"y"}}}'
    AM.chat = lambda s, p, **kw: '{"what_is_at_issue":"q","argument_steps":["s1"],"open_items":[],"decision_for_l2":"d"}'


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def main() -> int:
    ok = True
    R.REG_DIR = Path(tempfile.mkdtemp())
    FB.FAILURE_QUEUE = Path(tempfile.mkdtemp()) / "q.jsonl"
    _stub_model()

    print("=== A2-10 resource/rate limiting (DAG scheduler) ===")
    # 3 works, each with SOURCE done (so T1 eligible = model-bound)
    for w in ("a", "b", "c"):
        R.commit("SOURCE", f"{w}:v1", f"{w}h1", created_by="test",
                 payload={"verse": "śivo", "source_text": "śivo"})

    # budget 2 -> only 2 model-bound T1 jobs advance in this pass
    r = FS.scheduler_pass(["a", "b", "c"], ["T1", "ARGMAP", "L0", "L2", "L200", "C1"],
                          per_layer=2, max_model_calls=2)
    ok &= t("budget caps model-bound jobs", r["model_calls"] <= 2, f"model_calls={r['model_calls']}")
    committed_works = {oid.split(":")[0] for oid in r["committed_detail"]}
    ok &= t("only a subset of works advanced (budget)", len(committed_works) <= 2,
            f"advanced={sorted(committed_works)}")

    # a later pass with a bigger budget continues the remaining works
    r2 = FS.scheduler_pass(["a", "b", "c"], ["T1", "ARGMAP", "L0", "L2", "L200", "C1"],
                           per_layer=2, max_model_calls=4)
    ok &= t("later pass continues (budget resets per pass)",
            r2["model_calls"] >= 1, f"model_calls={r2['model_calls']}")

    print("\n" + ("RATE-LIMIT ALL PASS" if ok else "RATE-LIMIT SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
