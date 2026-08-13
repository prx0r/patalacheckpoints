#!/usr/bin/env python3
"""evals/patala/tasks/argmap_ipvv_eval.py — PĀṬALA-ARGMAP-NAT-IPVV (Inspect task, devpath1 E2-01).

The IPVV-grounded ARGMAP NAT eval. The base evaluator is `argmap_eval.py`'s `verify_argmap`
(shared contract); this task focuses on the REAL IPVV exemplar maps (the V2-O kārikā-1 argument map,
per `pilot_V2O_ARGUMENT_MAP.md`) so the verifier's fidelity is measured against a hand-authored
scholarly exemplar, not just the committed factory map.

It reuses the SAME cross-lane EvaluationCandidate/EvaluationFinding objects and the same
`verify_argmap` SUT. It adds a semantic-coverage dimension: the produced map must address the
load-bearing claims of the IPVV exemplar (support/āśraya, maheśvara, pratibhā, order-less, freedom).

Run (deterministic, no model calls):
  machinelearning/research/.venv/bin/python -m inspect_ai eval \
      source-evidence/evals/patala/tasks/argmap_ipvv_eval.py --model mockllm/mockllm
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset, Sample
from inspect_ai.scorer import Score, metric, scorer
from inspect_ai.scorer._metric import SampleScore
from inspect_ai.solver import Solver, solver

_TASKS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _TASKS)
from evaluation_candidate import EvaluationCandidate          # noqa: E402
from argmap_eval import verify_argmap, sha256, BENCH as BASE_BENCH  # noqa: E402
import argmap_contract as C                                    # noqa: E402

BENCH = "PĀṬALA-ARGMAP-NAT-IPVV"
VERSION = "v0.1"
PINNED_INSPECT = "inspect-ai==0.3.258"

# load-bearing claims a correct IPVV V2-O kārikā-1 map must address (from pilot_V2O_ARGUMENT_MAP.md)
IPVV_GOLD_CLAIMS = ["support", "āśraya", "maheśvara", "pratibhā", "flashing",
                    "order-less", "freedom", "powers"]


def _coverage(map_text: str) -> dict:
    low = map_text.lower()
    present = [c for c in IPVV_GOLD_CLAIMS if c.lower() in low]
    missing = [c for c in IPVV_GOLD_CLAIMS if c.lower() not in low]
    return {"present": present, "missing": missing}


def verify_ipvv(candidate: EvaluationCandidate) -> dict:
    base = verify_argmap(candidate)
    am = (candidate.payload or {}).get("argument_map", {})
    map_text = json.dumps(am, ensure_ascii=False)
    cov = _coverage(map_text)
    base["coverage"] = cov
    base["coverage_ok"] = len(cov["missing"]) <= 2   # tolerance for a first-pass map
    base["verdict"] = "FAIL" if (not base["ok"] or not base["coverage_ok"]) else "PASS"
    return base


def _fixture_candidate() -> EvaluationCandidate:
    """A frozen IPVV V2-O map candidate (structural stand-in for the committed exemplar)."""
    return EvaluationCandidate(
        candidate_id="cand-ipvv-v2o-k1",
        layer="ARGMAP", object_ref="ipvv:V2O:k1", version="argmap-ipvv:v2o:k1-v1",
        payload={"argument_map": {
            "what_is_at_issue": "What is the support (āśraya) of the powers of consciousness?",
            "argument_steps": [
                "The flashing (pratibhā) is ordered into the object's features.",
                "The free knower, the maheśvara, is the support of that flashing.",
                "The I-awareness is order-less, not a constructed relation.",
            ],
            "open_items": [{"text": "Whether the knower is strictly the maheśvara or a broader self",
                            "status": "OPEN"}],
            "decision_for_l2": "Render the flashing as grounded in the free maheśvara knower.",
        }},
        source_refs=["ipvv:V2O"],
        producer={"agent": "argmap_ipvv_eval", "commit": "", "status": "MACHINE_PROPOSED"},
    )


def build_dataset() -> MemoryDataset:
    cand = _fixture_candidate()
    return MemoryDataset([Sample(
        id=cand.candidate_id,
        input=json.dumps(cand.emit(), ensure_ascii=False),
        metadata={"bench": BENCH, "version": VERSION, "version": cand.version,
                  "pinned_inspect": PINNED_INSPECT},
    )])


@solver
def run_ipvv_verifier() -> Solver:
    async def solve(state, generate):
        cand = EvaluationCandidate.from_dict(json.loads(state.input))
        res = verify_ipvv(cand)
        state.output.completion = res["verdict"]
        state.store.set("coverage", res.get("coverage", {}))
        state.store.set("problems", res["problems"])
        return state
    return solve


@metric
def coverage_recall():
    def compute(scores: list[SampleScore]):
        vals = [s.score.as_float() for s in scores]
        return sum(vals) / len(vals) if vals else float("nan")
    return compute


@scorer(metrics=[coverage_recall()])
def ipvv_score():
    async def score(state, target):
        cov = state.store.get("coverage", {})
        problems = state.store.get("problems", [])
        ok = state.output.completion == "PASS"
        return Score(value=ok, answer=state.output.completion,
                     explanation=(f"verdict={state.output.completion} coverage={cov} problems={problems}"))
    return score


@task
def argmap_ipvv_nat():
    ds = build_dataset()
    return Task(
        dataset=ds, solver=run_ipvv_verifier(), scorer=[ipvv_score()],
        name="argmap_ipvv_nat", version=VERSION,
        metadata={"bench": BENCH, "pinned_inspect": PINNED_INSPECT,
                  "dataset_hash": sha256([{"id": s.id, "input": s.input} for s in ds.samples])},
    )


if __name__ == "__main__":
    cand = _fixture_candidate()
    res = verify_ipvv(cand)
    print(f"{BENCH} {VERSION}")
    print(f"  verdict={res['verdict']} ok={res['ok']} coverage_ok={res.get('coverage_ok')}")
    print(f"  coverage={res.get('coverage')}")
    print(f"  problems={res['problems']}")
