#!/usr/bin/env python3
"""inspect_l200_nat.py — PĀṬALA-L200-CHECKER-NAT v0.1 (Inspect AI NAT task).

NAT for the L200 typed-reference layer, split into two DISTINCT claims (per Agent 0 review):

  L200-CHECKER-NAT  (this file)
    input:   proposal + independently adjudicated reference
    SUT:     check_dim
    claim:   does the deterministic checker correctly APPLY the independently adjudicated
             reference to the proposal? (the checker is given a reference BY DEFINITION)

  L200-DETECTOR-NAT  (future, NOT this file)
    input:   L0/L1/L2 + proposal
    SUT:     a semantic detector/model
    claim:   can the system INDEPENDENTLY identify MT/IA/open-item defects without being handed
             the answer?

This file is the FIRST claim (checker-NAT). It does NOT claim independent semantic detection.

LANE BOUNDARY (EVAL-CONTRACT item 11): consumes Agent 2's frozen live L200 proposals READ-ONLY;
does not modify or tune Agent 2's proposer. The reference conditions are the product of INDEPENDENT
adjudication of what the model actually produced (not the SYN fixture's expected labels).

IMPORTANT (no gold leak): the independently adjudicated REFERENCE is a legitimate solver INPUT
(because check_dim requires one by definition), passed via the frozen candidate payload — it is
NOT smuggled through hidden gold metadata. The adjudicated VERDICT remains hidden gold.
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
import sys

from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset, Sample
from inspect_ai.scorer import Score, metric, scorer
from inspect_ai.scorer._metric import SampleScore
from inspect_ai.solver import solver

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from certificate_l200 import check_dim  # noqa: E402

BENCH = "PĀṬALA-L200-CHECKER-NAT"
VERSION = "v0.1"
PINNED_INSPECT = "inspect-ai==0.3.258"

NAT_DIR = os.path.join(os.path.dirname(__file__), "nat", "l200")


def sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()


def _sut_sha() -> str:
    import inspect as _inspect
    return sha256(_inspect.getsource(check_dim))


def load_nat_objects() -> list[dict]:
    """Load frozen (proposal + reference, adjudication, provenance) NAT objects.

    Each candidate = Agent 2's frozen live proposal + the INDEPENDENTLY ADJUDICATED reference
    conditions (the product of adjudication of what the model actually produced). The reference
    is a legitimate solver INPUT (check_dim requires one by definition) — carried in the frozen
    candidate payload, NOT in hidden gold. The adjudicated VERDICT is the hidden gold.
    """
    objects = []
    if not os.path.isdir(NAT_DIR):
        return objects
    for pp in sorted(glob.glob(os.path.join(NAT_DIR, "*.proposal.json"))):
        base = pp[:-len(".proposal.json")]
        adj_path = base + ".adjudication.json"
        if not os.path.isfile(adj_path):
            continue
        with open(pp, encoding="utf-8") as f:
            candidate = json.load(f)   # {"proposal": ..., "reference": {...}} frozen bundle
        with open(adj_path, encoding="utf-8") as f:
            adjudication = json.load(f)
        objects.append({
            "id": os.path.basename(base),
            "candidate": candidate,
            "adjudication": adjudication,
            "provenance": {"path": pp, "candidate_sha": sha256(candidate),
                           "adjudication_sha": sha256(adjudication),
                           "read_only": True},
        })
    return objects


def build_dataset() -> MemoryDataset:
    sut_sha = _sut_sha()
    samples = []
    for o in load_nat_objects():
        expected = o["adjudication"]["verdict"]
        # solver-visible input: the frozen proposal + its independently adjudicated reference
        samples.append(Sample(
            id=o["id"],
            input=json.dumps(o["candidate"], ensure_ascii=False),
            metadata={
                "bench": BENCH, "version": VERSION, "fixture_id": o["id"],
                "expected": expected, "sut_sha": sut_sha,
                "object_hash": o["provenance"]["candidate_sha"],
                "adjudication_sha": o["provenance"]["adjudication_sha"],
                "adjudication": o["adjudication"],   # gold (verdict only), hidden from solver
                "pinned_inspect": PINNED_INSPECT,
            },
        ))
    return MemoryDataset(samples)


@solver
def run_typed_checker() -> Solver:
    """SUT: check_dim applying the independently adjudicated reference to the proposal.

    The reference is a legitimate solver INPUT (frozen in the candidate payload), not hidden gold.
    The adjudicated VERDICT (hidden gold) is compared in the scorer.
    """
    async def solve(state, generate):
        candidate = json.loads(state.input)
        violations = check_dim(candidate["proposal"], candidate["reference"])
        state.output.completion = "FAIL" if violations else "PASS"
        state.store.set("violations", violations)
        return state
    return solve


@metric
def verdict_accuracy():
    def compute(scores: list[SampleScore]):
        vals = [s.score.as_float() for s in scores]
        return sum(vals) / len(vals) if vals else float("nan")
    return compute


@metric
def clean_specificity():
    def compute(scores: list[SampleScore]):
        clean = [s for s in scores if s.sample_metadata and s.sample_metadata.get("expected") == "PASS"]
        if not clean:
            return float("nan")
        return sum(1 for s in clean if s.score.as_float() == 1.0) / len(clean)
    return compute


@metric
def defect_sensitivity():
    def compute(scores: list[SampleScore]):
        bad = [s for s in scores if s.sample_metadata and s.sample_metadata.get("expected") == "FAIL"]
        if not bad:
            return float("nan")
        return sum(1 for s in bad if s.score.as_float() == 1.0) / len(bad)
    return compute


@scorer(metrics=[verdict_accuracy()])
def verdict():
    async def score(state, target):
        got = state.output.completion
        expected = state.metadata["expected"]
        return Score(value=(got == expected), answer=got,
                     explanation=f"fixture={state.metadata['fixture_id']} expected={expected} "
                                 f"got={got} violations={state.store.get('violations')}")
    return score


@scorer(metrics=[clean_specificity(), defect_sensitivity()])
def verdict_split():
    async def score(state, target):
        got = state.output.completion
        expected = state.metadata["expected"]
        return Score(value=(got == expected), answer=got, explanation=state.metadata["fixture_id"])
    return score


@task
def l200_nat():
    ds = build_dataset()
    if not ds.samples:
        raise ValueError(
            "PĀṬALA-L200-NAT: no adjudicated live proposals. This is NOT a result. "
            "Consume Agent 2's frozen live proposals (read-only) into "
            "source-evidence/evals/nat/l200/ (see nat/README.md), then re-run."
        )
    return Task(
        dataset=ds,
        solver=run_typed_checker(),
        scorer=[verdict(), verdict_split()],
        name="l200_checker_nat",
        version=VERSION,
        metadata={"bench": BENCH, "pinned_inspect": PINNED_INSPECT,
                  "dataset_hash": sha256([{"id": s.id, "input": s.input,
                                           "expected": s.metadata["expected"]} for s in ds.samples]),
                  "sut_sha": _sut_sha()},
    )


if __name__ == "__main__":
    objs = load_nat_objects()
    print(f"{BENCH} {VERSION}: {len(objs)} adjudicated live proposals "
          f"({sum(1 for o in objs if o['adjudication']['verdict']=='PASS')} PASS, "
          f"{sum(1 for o in objs if o['adjudication']['verdict']=='FAIL')} FAIL)")
    print(f"  corpus dir: {NAT_DIR} ({'present' if os.path.isdir(NAT_DIR) else 'MISSING — expand the natural corpus'})")
    for o in objs:
        print(f"  {o['adjudication']['verdict']:4} {o['id']} violations={len(o['adjudication'].get('violations', []))}")
