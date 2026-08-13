#!/usr/bin/env python3
"""inspect_l200.py — PĀṬALA-L200-SYN v0.1 (Inspect AI benchmark task).

The second Inspect evaluation, porting the L200 typed-reference semantic layer. This tests the
DETERMINISTIC typed-reference checker (certificate_l200.check_dim) — the semantic layer that catches
the exact failure the structural validator cannot (F6: IA→MT laundering produced 5 MTs on an
IA-not-MT fixture). See factory-certificates/L200-v1/live-canary.md.

Design mirrors the ARG-LAUNDRY fix: gold is INDEPENDENT of the SUT.
  - GOLD: hardcoded {fixture_id -> expected verdict}, specified from mutation SEMANTICS.
  - Every sample carries a FROZEN L200 proposal object + the typed fixture reference. The solver
    consumes ONLY that object; it never sees the mutation recipe.
  - Both must-FAIL (laundering / missing-required) and must-PASS (negative) controls, so the checker
    cannot win by overzealousness.

Claims: PĀṬALA-L200-SYN (synthetic sensitivity of the typed-reference checker to controlled
mutations). NOT L200-NAT (real live-model proposals independently typed) and NOT whole-pipeline.

Run (deterministic, no model calls):
  machinelearning/research/.venv/bin/python -m inspect_ai eval source-evidence/evals/inspect_l200.py
"""
from __future__ import annotations

import copy
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
from certificate_l200 import FIXTURES, MT_TYPES, check_dim  # noqa: E402

BENCH = "PĀṬALA-L200-SYN"
VERSION = "v0.1"
PINNED_INSPECT = "inspect-ai==0.3.258"


def sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()


def _sut_sha() -> str:
    """Fingerprint of the SUT IMPLEMENTATION ONLY (check_dim), not the fixture/gold data."""
    import inspect as _inspect
    return sha256(_inspect.getsource(check_dim))


def dataset_hash(samples) -> str:
    """SHA over the ACTUAL frozen evaluation corpus: id + input + independent gold."""
    corpus = [{"id": s.id, "input": s.input, "expected": s.metadata.get("expected")}
              for s in samples]
    return sha256(corpus)


def _clean_proposal(fx: dict) -> dict:
    """A correct-by-fixture L200 proposal object (no model call — built directly)."""
    return {
        "proposal_status": "COMPLETE",
        "l200": {
            "3_material_translation_decisions": [dict(m) for m in fx["expected_mt"]],
            "4_interpretive_assertions": [dict(a) for a in fx["expected_ia"]],
            "5_source_layer": [{"par": 0, "speaker": s} for s in fx["source_layers"]],
            "7_open_items": [{"text": oi.get("desc", ""), "status": "OPEN"}
                             for oi in fx["required_open_items"]],
        },
    }


def _pristine_proposal(fx: dict) -> dict:
    """The pristine (should-PASS) proposal for a fixture."""
    return _clean_proposal(fx)


# ── GOLD: independent of check_dim — declared as DATA in FIXTURE_SPEC below ────
# Verdicts come from mutation SEMANTICS, never from running check_dim.
# FIXTURE_SPEC: (fixture_id, fx_ref, mutator | None, expected) — the single source of truth.
FIXTURE_SPEC = [
    # id, fx_id, mutation-key (or None for control), expected
    # ── controls: must PASS (correct-by-fixture objects) ──
    ("F1_CLEAN", "F1", None, "PASS"),
    ("F2_CLEAN", "F2", None, "PASS"),
    ("F4_CLEAN", "F4", None, "PASS"),
    ("F5_CLEAN", "F5", None, "PASS"),
    ("F10_CLEAN", "F10", None, "PASS"),
    # ── laundering / violation mutations: must FAIL ──
    # F6 is THE IA→MT laundering case: a forbidden SUPPLIED MT present must FAIL
    ("F6_IA_AS_MT", "F6", "launder_ia_as_mt", "FAIL"),
    # MT precision: a forbidden MT type present must FAIL
    ("F1_FORBIDDEN_LEXICAL", "F1", "forbidden_mt_lexical", "FAIL"),
    # MT recall: a required MT missing must FAIL
    ("F1_MISSING_REQUIRED_MT", "F1", "missing_required_mt", "FAIL"),
    # IA recall: expected IA absent must FAIL
    ("F6_MISSING_IA", "F6", "missing_ia", "FAIL"),
    # source-layer attribution: a required speaker missing must FAIL
    ("F3_MISSING_SOURCE_LAYER", "F3", "missing_source_layer", "FAIL"),
    # open-item honesty: required open item dropped must FAIL
    ("F9_MISSING_OPEN_ITEM", "F9", "missing_open_item", "FAIL"),
]


def _apply_mutation(prop: dict, fx: dict, key: str) -> dict:
    p = copy.deepcopy(prop)
    l2 = p["l200"]
    if key == "launder_ia_as_mt":
        # move the fixture's IA into the MT list as a SUPPLIED type (IA→MT laundering)
        l2["3_material_translation_decisions"] = [{"type": "SUPPLIED", "desc": "the mirror that knows"}]
        l2["4_interpretive_assertions"] = []
    elif key == "forbidden_mt_lexical":
        l2["3_material_translation_decisions"] = [{"type": "LEXICAL", "desc": "core lexical"}]
    elif key == "missing_required_mt":
        l2["3_material_translation_decisions"] = []
    elif key == "missing_ia":
        l2["4_interpretive_assertions"] = []
    elif key == "missing_source_layer":
        l2["5_source_layer"] = [{"par": 0, "speaker": "OTHER"}]
    elif key == "missing_open_item":
        l2["7_open_items"] = []
    else:
        raise ValueError(f"unknown mutation {key}")
    return p


def build_dataset() -> MemoryDataset:
    fx_by_id = {f["id"]: f for f in FIXTURES}
    sut_sha = _sut_sha()
    samples = []
    for fid, fx_id, mut, expected in FIXTURE_SPEC:
        fx = fx_by_id[fx_id]
        prop = _pristine_proposal(fx)
        if mut:
            prop = _apply_mutation(prop, fx, mut)
        payload = {"proposal": prop, "fixture": fx}
        samples.append(Sample(
            id=fid,
            input=json.dumps(payload, ensure_ascii=False),
            metadata={
                "bench": BENCH, "version": VERSION, "fixture_id": fid,
                "expected": expected, "sut_sha": sut_sha,
                "object_hash": sha256(prop), "fixture_ref": fx_id,
                "pinned_inspect": PINNED_INSPECT,
            },
        ))
    ds = MemoryDataset(samples)
    ds.sha = sha256
    return ds


@solver
def run_typed_checker() -> Solver:
    """SUT: the deterministic typed-reference checker over the frozen object."""
    async def solve(state, generate):
        payload = json.loads(state.input)
        violations = check_dim(payload["proposal"], payload["fixture"])
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
def mutation_sensitivity():
    def compute(scores: list[SampleScore]):
        mut = [s for s in scores if s.sample_metadata and s.sample_metadata.get("expected") == "FAIL"]
        if not mut:
            return float("nan")
        return sum(1 for s in mut if s.score.as_float() == 1.0) / len(mut)
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


@scorer(metrics=[clean_specificity(), mutation_sensitivity()])
def verdict_split():
    async def score(state, target):
        got = state.output.completion
        expected = state.metadata["expected"]
        return Score(value=(got == expected), answer=got, explanation=state.metadata["fixture_id"])
    return score


@task
def l200_syn():
    from inspect_ai import Task as _Task
    ds = build_dataset()
    return _Task(
        dataset=ds,
        solver=run_typed_checker(),
        scorer=[verdict(), verdict_split()],
        name="l200_syn",
        version=VERSION,
        metadata={"bench": BENCH, "pinned_inspect": PINNED_INSPECT,
                  "dataset_hash": dataset_hash(ds.samples),
                  "sut_sha": _sut_sha()},
    )


if __name__ == "__main__":
    ds = build_dataset()
    print(f"{BENCH} {VERSION} dataset: {len(ds.samples)} fixtures "
          f"({sum(1 for s in ds.samples if s.metadata['expected']=='PASS')} PASS, "
          f"{sum(1 for s in ds.samples if s.metadata['expected']=='FAIL')} FAIL)")
    for s in ds.samples:
        print(f"  {s.metadata['expected']:4} {s.metadata['fixture_id']:26} "
              f"fx={s.metadata['fixture_ref']} obj={s.metadata['object_hash'][:10]}")
