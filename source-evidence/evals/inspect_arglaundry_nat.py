#!/usr/bin/env python3
"""inspect_arglaundry_nat.py — PĀṬALA-ARG-LAUNDRY-NAT v0.1 (Inspect AI NAT task).

NAT = naturally occurring essay/audit outputs, independently adjudicated. This is the epistemic
jump from "we catch mutations we invented" (SYN) to "we catch corruption the machine actually
produced when nobody designed the failure for the test."

DESIGN (EVAL-CONTRACT, items 2, 4, 5, 11, + NAT additions):
  - Gold = an independent adjudication object, NOT the detector's output:
        {"verdict": "FAIL"|"PASS", "violations": [{family, sentence_ref, reason,
                                                    expected_detector_rule}], "uncertain": []}
    Gold is "this output is epistemically defective for reason X", never "the detector ought
    to emit string Y".
  - Each sample carries the FROZEN historical audit object + its adjudication (gold) + provenance.
    The solver consumes only the frozen object; it never sees the gold.
  - Metrics: object verdict accuracy, violation-level precision/recall, per-family recall, and the
    FIRST UNSUPPORTED LAYER (SOURCE→SPAN→ATTRIBUTION→SCOPE→WARRANT→CONCLUSION→PROJECTION).

CORPUS HONESTY (anti-theatre):
  The available historical natural corpus is currently SMALL: exactly one prior essay audit object
  exists on disk, and it is the object used to BUILD the SYN suite — not ideal NAT provenance.
  This task therefore ships the HARNESS + adjudication schema, seeded with whatever genuinely
  natural objects are frozen. EXPANDING the natural corpus (15-30 objects from prior Agent 1 runs,
  sampled across clean/problematic/borderline, not cherry-picked) is the required collection work;
  do not fabricate "historical" outputs to inflate the set.
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
sys.path.insert(0, os.path.join(ROOT, "machinelearning", "research", "experiments"))
sys.path.insert(0, os.path.join(ROOT, "machinelearning", "research"))
from check_sentence_evidence_audit import check_audit  # noqa: E402

BENCH = "PĀṬALA-ARG-LAUNDRY-NAT"
VERSION = "v0.1"
PINNED_INSPECT = "inspect-ai==0.3.258"

# ── corpus discovery ──────────────────────────────────────────────────────────
# Adjudicated NAT objects live in source-evidence/evals/nat/arg-laundry/ as
# "<id>.audit.json" (the frozen historical output) + "<id>.adjudication.json" (independent gold).
NAT_DIR = os.path.join(os.path.dirname(__file__), "nat", "arg-laundry")


def sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()


def _sut_sha() -> str:
    import inspect as _inspect
    return sha256(_inspect.getsource(check_audit))


def load_nat_objects() -> list[dict]:
    """Load frozen (audit, authority, adjudication, provenance) NAT objects from the NAT dir.

    NAT provenance discipline (EVAL-CONTRACT item 11):
      - audit: the frozen historical output (never recomputed)
      - authority: the frozen synthesis/dependency AUTHORITY SNAPSHOT that existed when the
        audit was produced (never the current synthesis_authority(), so a future change in
        synthesis/dependencies cannot silently change the verdict on an unchanged object)
      - adjudication: the independent gold
    """
    objects = []
    if not os.path.isdir(NAT_DIR):
        return objects
    for ap in sorted(glob.glob(os.path.join(NAT_DIR, "*.audit.json"))):
        base = ap[:-len(".audit.json")]
        adj_path = base + ".adjudication.json"
        auth_path = base + ".authority.json"
        if not os.path.isfile(adj_path):
            continue  # an un-adjudicated audit is not yet NAT material
        if not os.path.isfile(auth_path):
            continue  # without the frozen authority snapshot we cannot safely evaluate it
        with open(ap, encoding="utf-8") as f:
            audit = json.load(f)
        with open(auth_path, encoding="utf-8") as f:
            authority = json.load(f)
        with open(adj_path, encoding="utf-8") as f:
            adjudication = json.load(f)
        objects.append({
            "id": os.path.basename(base),
            "audit": audit,
            "authority": authority,          # frozen at production time
            "adjudication": adjudication,
            "provenance": {"path": ap, "audit_sha": sha256(audit),
                           "authority_sha": sha256(authority),
                           "adjudication_sha": sha256(adjudication)},
        })
    return objects


def build_dataset() -> MemoryDataset:
    sut_sha = _sut_sha()
    samples = []
    for o in load_nat_objects():
        expected = o["adjudication"]["verdict"]
        # solver-visible input: the frozen audit + its frozen authority snapshot
        samples.append(Sample(
            id=o["id"],
            input=json.dumps({"audit": o["audit"], "authority": o["authority"]},
                             ensure_ascii=False),
            metadata={
                "bench": BENCH, "version": VERSION, "fixture_id": o["id"],
                "expected": expected, "sut_sha": sut_sha,
                "object_hash": o["provenance"]["audit_sha"],
                "authority_sha": o["provenance"]["authority_sha"],
                "adjudication_sha": o["provenance"]["adjudication_sha"],
                "adjudication": o["adjudication"],   # gold, hidden from solver
                "pinned_inspect": PINNED_INSPECT,
            },
        ))
    return MemoryDataset(samples)


@solver
def run_detector() -> Solver:
    """SUT: the Commit-C detector over the frozen audit object, using the FROZEN authority.

    Gold is NOT visible. The authority snapshot is supplied as solver input (frozen at
    production time) — NEVER recomputed via synthesis_authority().
    """
    async def solve(state, generate):
        payload = json.loads(state.input)
        result = check_audit(payload["audit"], payload["authority"])
        state.output.completion = "PASS" if result["ok"] else "FAIL"
        state.store.set("detector_problems", result["problems"])
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
                                 f"got={got} problems={state.store.get('detector_problems')}")
    return score


@scorer(metrics=[clean_specificity(), defect_sensitivity()])
def verdict_split():
    async def score(state, target):
        got = state.output.completion
        expected = state.metadata["expected"]
        return Score(value=(got == expected), answer=got, explanation=state.metadata["fixture_id"])
    return score


@task
def arglaundry_nat():
    ds = build_dataset()
    if not ds.samples:
        raise ValueError(
            "PĀṬALA-ARG-LAUNDRY-NAT: no adjudicated natural objects. This is NOT a result. "
            "Freeze + independently adjudicate prior Agent 1 outputs into "
            "source-evidence/evals/nat/arg-laundry/ (see nat/README.md), then re-run."
        )
    return Task(
        dataset=ds,
        solver=run_detector(),
        scorer=[verdict(), verdict_split()],
        name="arglaundry_nat",
        version=VERSION,
        metadata={"bench": BENCH, "pinned_inspect": PINNED_INSPECT,
                  "dataset_hash": sha256([{"id": s.id, "input": s.input,
                                           "expected": s.metadata["expected"]} for s in ds.samples]),
                  "sut_sha": _sut_sha()},
    )


if __name__ == "__main__":
    objs = load_nat_objects()
    print(f"{BENCH} {VERSION}: {len(objs)} adjudicated natural objects "
          f"({sum(1 for o in objs if o['adjudication']['verdict']=='PASS')} PASS, "
          f"{sum(1 for o in objs if o['adjudication']['verdict']=='FAIL')} FAIL)")
    print(f"  corpus dir: {NAT_DIR} ({'present' if os.path.isdir(NAT_DIR) else 'MISSING — expand the natural corpus'})")
    for o in objs:
        print(f"  {o['adjudication']['verdict']:4} {o['id']} violations={len(o['adjudication'].get('violations', []))}")
