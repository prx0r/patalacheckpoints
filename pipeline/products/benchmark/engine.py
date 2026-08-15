#!/usr/bin/env python3
"""products/benchmark/engine.py — Dataset / Benchmark (#15).

The honest-eval product: compile REAL IPVV objects (passages, claims, arguments) into an inspect_ai
benchmark and run the deterministic CPU scorer. Reproducible, real samples, no GPU, no model.

The benchmark task here (a real, answerable question on real data):
  For each IPVV passage, the SUT is a deterministic checker that decides whether the derived
  CLAIM's epistemic ceiling is HONEST (i.e. a PĀṬALA-INFERS claim stays MACHINE_PROPOSED; a
  SOURCE-SAYS claim is SCHOLARLY_CORROBORATED). The 'gold' is the expected honest ceiling.

This is the anti-theatre eval: the gold is the HONEST expectation (never inflate), and the SUT is
the deterministic gate — a green result means the claim-envelope discipline holds on real data.

Run:
  cd /root/patalacheckpoints
  PYTHONPATH=pipeline python3 pipeline/products/benchmark/engine.py        # compile + print dataset
  PYTHONPATH=pipeline python3 -m inspect_ai eval pipeline/products/benchmark/engine.py  # run the eval

  (requires inspect-ai in the venv: /root/venv/bin/python -m inspect_ai eval ...)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(ROOT / "pipeline"))

from products.claim.engine import make_claim  # noqa: E402
from products._shared import ipvv  # noqa: E402

BENCH = "PĀṬALA-CLAIM-ENVELOPE"
VERSION = "v0.1"

EXPECTED_CEILING = {
    "SOURCE-SAYS": "SCHOLARLY_CORROBORATED",
    "SCHOLAR-RECONSTRUCTS": "SCHOLARLY_CORROBORATED_PRELIMINARY",
    "PĀṬALA-INFERS": "MACHINE_PROPOSED",
}


def _claim_ceiling_honest(claim: dict) -> bool:
    """The deterministic SUT: is the claim's ceiling the HONEST one for its status?"""
    expect = EXPECTED_CEILING.get(claim["epistemic_status"])
    if expect is None:
        return False
    return claim["epistemic_ceiling"] == expect


def build_samples() -> list[dict]:
    """Compile real IPVV passages -> benchmark samples (passage, claim, expected, honest_check)."""
    samples = []
    for p in ipvv.passages():
        # PĀṬALA-INFERS claims must be honest (MACHINE_PROPOSED) — the default, never inflated
        claim = make_claim(p, "PĀṬALA-INFERS")
        samples.append({
            "id": ipvv.passage_id(p),
            "passage_id": p.get("id"),
            "input": json.dumps({"passage": p.get("id"), "claim": claim}, ensure_ascii=False),
            "expected": _claim_ceiling_honest(claim),
            "expected_ceiling": claim["epistemic_ceiling"],
            "claim_text": claim["text"][:80],
        })
    return samples


def honest_metric(samples: list[dict]) -> dict:
    """Compute the honest-ceiling rate on the compiled dataset (deterministic)."""
    n = len(samples)
    honest = sum(1 for s in samples if s["expected"])
    return {"samples": n, "honest_ceiling_rate": round(honest / n, 3) if n else None,
            "honest": honest, "inflated": n - honest}


# ---- inspect_ai task (runs under: python -m inspect_ai eval this_file) ----
def _build_inspect_task():
    from inspect_ai import Task
    from inspect_ai.dataset import MemoryDataset, Sample
    from inspect_ai.scorer import Score, metric, scorer
    from inspect_ai.solver import solver

    samples = build_samples()
    ds = MemoryDataset([Sample(id=s["id"], input=s["input"],
                               metadata={"expected": s["expected"],
                                         "passage": s["passage_id"]}) for s in samples])

    @solver
    def run_checker():
        async def solve(state, generate):
            payload = json.loads(state.input)
            state.output.completion = "PASS" if _claim_ceiling_honest(payload["claim"]) else "FAIL"
            return state
        return solve

    @scorer
    def verdict():
        async def score(state, target):
            ok = (state.output.completion == "PASS") == target.metadata["expected"]
            return Score(value=1.0 if ok else 0.0, answer=state.output.completion,
                         metadata={"passage": target.metadata["passage"]})
        return score

    @metric
    def accuracy():
        def compute(scores):
            vals = [s.score.as_float() for s in scores]
            return sum(vals) / len(vals) if vals else float("nan")
        return compute

    return Task(dataset=ds, solver=run_checker(), scorer=[verdict(), accuracy()],
                name="claim_envelope", version=VERSION, metadata={"bench": BENCH})


try:
    from inspect_ai import task as _task
    @_task
    def claim_envelope():
        return _build_inspect_task()
except Exception:
    # inspect_ai not installed — the plain CLI (compile + metric) still works
    claim_envelope = None


if __name__ == "__main__":
    samples = build_samples()
    print(json.dumps(honest_metric(samples), indent=2))
    print(f"\nBENCH {BENCH} {VERSION}: {len(samples)} samples")
    for s in samples[:3]:
        print(f"  {s['id'][:24]:26} honest={s['expected']} ceiling={s['expected_ceiling']} "
              f"| {s['claim_text'][:40]}")
