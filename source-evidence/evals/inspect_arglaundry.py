#!/usr/bin/env python3
"""inspect_arglaundry.py — PĀṬALA-ARG-LAUNDRY-SYN v0.1 (Inspect AI benchmark task).

The Inspect AI prototype (Track C, Global Architecture v0.1), FIXED per Agent 0 review:

    >>> The single most important fix: GOLD IS INDEPENDENT OF THE SUT. <<<

v0 (99dec61) derived every target from check_audit() itself, so gold(x) == prediction(x)
by construction and the benchmark could NOT falsify the detector. This revision removes
that circularity.

Design:
  - Gold table (GOLD) is hardcoded: {fixture_id -> expected_verdict}, specified from the
    mutation SEMANTICS, never by running the detector. If the detector misses a laundering
    mutation, it is now a REAL benchmark failure.
  - Every sample carries a FROZEN candidate object: the (possibly mutated) audit JSON +
    the required authority context. The solver consumes ONLY that object. It does NOT
    receive the mutation-family recipe and does NOT need to know which mutation was
    injected. This is the abstraction any future solver (LLM, hybrid, external baseline)
    can share.
  - Suite covers Commit-C rules C01-C07, with both must-FAIL (laundering) and must-PASS
    (control) fixtures so the detector cannot win by being overzealous.

Claims: this is PĀṬALA-ARG-LAUNDRY-SYN (synthetic sensitivity — known-good + controlled
mutation -> does the checker detect known corruption). NOT RealWorldRecall (-NAT) and NOT
whole-pipeline (-GEN). See README.md.

Run (deterministic, no model calls):
  machinelearning/research/.venv/bin/python -m inspect_ai eval source-evidence/evals/inspect_arglaundry.py
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
from inspect_ai.solver import Solver, solver

# ── import the frozen detector (the system under test) ─────────────────────────
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "machinelearning", "research", "experiments"))
sys.path.insert(0, os.path.join(ROOT, "machinelearning", "research"))
from check_sentence_evidence_audit import check_audit, synthesis_authority  # noqa: E402

BENCH = "PĀṬALA-ARG-LAUNDRY-SYN"
VERSION = "v0.1"
AUDIT_PATH = os.path.join(ROOT, "benchmarks/v0/review/ESSAY-IPVV-REFLEXION-CORE-001.audit.json")
PINNED_INSPECT = "inspect-ai==0.3.258"


def sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()


def detector_sha() -> str:
    """SHA of the frozen detector source (the SUT version fingerprint)."""
    p = os.path.join(ROOT, "machinelearning/research/experiments/check_sentence_evidence_audit.py")
    with open(p, encoding="utf-8") as f:
        return sha256(f.read())


def dataset_hash(samples) -> str:
    """SHA over the ACTUAL frozen evaluation corpus: id + input + independent gold.

    Hashes the real contents the solver sees (and the expected verdict), not a description
    of them — so a change to any fixture body changes the hash even if ids/metadata stay put.
    """
    corpus = [{"id": s.id, "input": s.input, "expected": s.metadata.get("expected")}
              for s in samples]
    return sha256(corpus)


# ── GOLD: independent of the detector ──────────────────────────────────────────
# Verdicts come from the mutation SEMANTICS. PASS == must stay clean; FAIL == laundering.
# Each maps to a fixture_id; a fixture is built by applying the described edit to a COPY
# of the pristine audit (or passing it through unmodified for controls).
GOLD = {
    # ── controls: must PASS (negative controls — detect overzealousness) ──
    "CLEAN_CONTROL": "PASS",
    "C06_EXPLANATORY_NO_FULL_CHAIN": "PASS",   # non-load-bearing prose is exempt
    "C06_TRANSITION_NO_FULL_CHAIN": "PASS",    # transition is exempt
    "C07_EXPANSIVE_WITH_SUPPORT": "PASS",      # EXPANSIVE backed by extra refs is legal
    "C05_RIVAL_SOURCED_QUALIFIED": "PASS",     # a SOURCED rival may render QUALIFIED (not laundering)
    # ── laundering: must FAIL ──
    "C01_MISSING_CLAIM_REFS": "FAIL",          # load-bearing sentence lost claim_refs
    "C01_MISSING_SOURCE_REFS": "FAIL",         # load-bearing sentence lost source_refs
    "C01_MISSING_AUDIT_BLOCK": "FAIL",         # load-bearing sentence lost audit block
    "C02_BYPASS_WARRANT": "FAIL",              # cites sources directly, skips SYN-INF-001
    "C03_INFLATE_STRENGTH": "FAIL",            # PROVEN on a MACHINE_RECONSTRUCTED thesis
    "C03_AUTHORS_LAUNDER": "FAIL",             # attributes reconstruction to Abhinavagupta
    "C03_DIRECT_RENDER": "FAIL",               # DIRECT render of an UNRESOLVED thesis
    "C03_ATTRIBUTION_AUTHOR": "FAIL",          # attribution=AUTHOR on the reconstruction
    "C03B_DIRECT_UNDER_SUPPORTED": "FAIL",     # DIRECT but claims not fully supported
    "C03_BOUNDARY_QUALIFIED": "FAIL",          # retargeting a BOUNDARY sentence erases boundary content
    "C04_DROP_BOUNDARY": "FAIL",               # erases a does_not_establish item
    "C05_RIVAL_ASSERT": "FAIL",                # unsourced rival rendered as asserted
    "C07_INVALID_SEMANTIC_RELATION": "FAIL",   # semantic_relation_to_claim invalid
    "C07_EXPANSIVE_NO_SUPPORT": "FAIL",        # EXPANSIVE with no extra claim/inference refs
}


def _thesis_sentence(audit: dict) -> dict:
    for s in audit["sentences"]:
        if "SYN-CONC-001" in s.get("claim_refs", []):
            return s
    raise RuntimeError("no SYN-CONC-001 thesis sentence in audit")


def _pristine() -> dict:
    with open(AUDIT_PATH, encoding="utf-8") as f:
        return json.load(f)


# ── fixture builders: each returns the FROZEN candidate object for one fixture_id ──
# These are applied to deep COPIES. Originals are never modified. The solver only ever
# sees the returned object — it is deliberately blind to which builder produced it.
def _build_fixture(fixture_id: str) -> dict:
    a = copy.deepcopy(_pristine())
    if fixture_id == "CLEAN_CONTROL":
        pass
    # controls (must PASS) — no laundering edit, only benign role/exempt changes
    elif fixture_id == "C06_EXPLANATORY_NO_FULL_CHAIN":
        # a non-load-bearing (exempt) sentence MAY lack full refs/audit — must NOT fail
        for s in a["sentences"]:
            if s.get("role") == "EXPLANATORY":
                s["claim_refs"] = s.get("claim_refs") or []
                s["text"] = s["text"] + " (explanatory aside)"
                break
    elif fixture_id == "C06_TRANSITION_NO_FULL_CHAIN":
        # a transition (exempt) sentence MAY lack full refs/audit — must NOT fail
        for s in a["sentences"]:
            if s.get("role") == "TRANSITION":
                s["inference_refs"] = s.get("inference_refs") or []
                s["text"] = s["text"] + " (transition)"
                break
    elif fixture_id == "C07_EXPANSIVE_WITH_SUPPORT":
        # take an EXPANSIVE load-bearing sentence; guarantee extra claim+inference refs
        for s in a["sentences"]:
            if s.get("role") == "LOAD_BEARING":
                s["semantic_relation_to_claim"] = "EXPANSIVE"
                s["claim_refs"] = (s.get("claim_refs") or []) + ["SYN-CONC-001"]
                s["inference_refs"] = (s.get("inference_refs") or []) + ["SYN-INF-001"]
                break
    elif fixture_id == "C03_BOUNDARY_QUALIFIED":
        for s in a["sentences"]:
            if s.get("render_mode") == "BOUNDARY":
                s["render_mode"] = "QUALIFIED"
                s["assertion_strength"] = "MOTIVATES"
                break
    elif fixture_id == "C05_RIVAL_SOURCED_QUALIFIED":
        for s in a["sentences"]:
            if s.get("render_mode") == "RIVAL" and not s.get("source_refs"):
                s["source_refs"] = ["pt:passage:ipvv:chunkV2-H-pancamo-vimarsa-k11-13.md"]
                s["render_mode"] = "QUALIFIED"
                s["assertion_strength"] = "MOTIVATES"
                break
    # laundering (must FAIL)
    elif fixture_id == "C01_MISSING_CLAIM_REFS":
        for s in a["sentences"]:
            if s.get("role") == "LOAD_BEARING":
                s.pop("claim_refs", None); break
    elif fixture_id == "C01_MISSING_SOURCE_REFS":
        for s in a["sentences"]:
            if s.get("role") == "LOAD_BEARING":
                s.pop("source_refs", None); break
    elif fixture_id == "C01_MISSING_AUDIT_BLOCK":
        for s in a["sentences"]:
            if s.get("role") == "LOAD_BEARING":
                s.pop("audit", None); break
    elif fixture_id == "C02_BYPASS_WARRANT":
        _thesis_sentence(a)["inference_refs"] = []
    elif fixture_id == "C03_INFLATE_STRENGTH":
        _thesis_sentence(a)["assertion_strength"] = "PROVEN"
    elif fixture_id == "C03_AUTHORS_LAUNDER":
        _thesis_sentence(a)["speaker"] = "Abhinavagupta"
    elif fixture_id == "C03_DIRECT_RENDER":
        _thesis_sentence(a)["render_mode"] = "DIRECT"
    elif fixture_id == "C03_ATTRIBUTION_AUTHOR":
        _thesis_sentence(a)["attribution"] = "AUTHOR"
    elif fixture_id == "C03B_DIRECT_UNDER_SUPPORTED":
        # DIRECT render of a NON-thesis claim that is not fully supported (C03b)
        for s in a["sentences"]:
            if s.get("role") == "LOAD_BEARING" and "SYN-CONC-001" not in s.get("claim_refs", []):
                s["render_mode"] = "DIRECT"
                break
    elif fixture_id == "C04_DROP_BOUNDARY":
        for i, s in enumerate(a["sentences"]):
            if s.get("render_mode") == "BOUNDARY":
                del a["sentences"][i]; break
    elif fixture_id == "C05_RIVAL_ASSERT":
        for s in a["sentences"]:
            if s.get("render_mode") == "RIVAL" and not s.get("source_refs"):
                s["render_mode"] = "DIRECT"
                s["assertion_strength"] = "ESTABLISHES"
                break
    elif fixture_id == "C07_INVALID_SEMANTIC_RELATION":
        for s in a["sentences"]:
            if s.get("claim_refs"):
                s["semantic_relation_to_claim"] = "FABRICATED"; break
    elif fixture_id == "C07_EXPANSIVE_NO_SUPPORT":
        for s in a["sentences"]:
            if s.get("claim_refs"):
                s["semantic_relation_to_claim"] = "EXPANSIVE"
                s["claim_refs"] = [s["claim_refs"][0]]
                s["inference_refs"] = []
                break
    else:
        raise ValueError(f"unknown fixture {fixture_id}")
    return a


# ── build the dataset: frozen object + independent gold ───────────────────────
def build_dataset() -> MemoryDataset:
    authority = synthesis_authority()
    authority_hash = sha256(authority)
    samples = []
    for fixture_id, expected in GOLD.items():
        audit = _build_fixture(fixture_id)
        object_hash = sha256(audit)
        samples.append(Sample(
            id=fixture_id,
            # solver-visible input: the FROZEN candidate object, nothing else
            input=json.dumps({"audit": audit, "authority": authority}, ensure_ascii=False),
            # benchmark metadata: independent gold + provenance. NOT consumed by the solver.
            metadata={
                "bench": BENCH, "version": VERSION,
                "fixture_id": fixture_id,
                "expected": expected,             # independent gold
                "object_hash": object_hash,
                "authority_hash": authority_hash,
                "detector_sha": detector_sha(),
                "pinned_inspect": PINNED_INSPECT,
            },
        ))
    ds = MemoryDataset(samples)
    ds.sha = sha256  # dataset-level hash recorded below
    return ds


# ── solver: consumes ONLY the frozen object; never the mutation recipe ────────
@solver
def run_detector() -> Solver:
    async def solve(state, generate):
        payload = json.loads(state.input)
        result = check_audit(payload["audit"], payload["authority"])
        state.output.completion = "PASS" if result["ok"] else "FAIL"
        state.store.set("detector_problems", result["problems"])
        return state
    return solve


# ── metrics (aggregate statistics; NA-safe) ────────────────────────────────────
@metric
def verdict_accuracy():
    def compute(scores: list[SampleScore]):
        vals = [s.score.as_float() for s in scores]
        return sum(vals) / len(vals) if vals else float("nan")
    return compute


@metric
def clean_specificity():
    """Fraction of clean (must-PASS) fixtures correctly accepted: 1 - FPR."""
    def compute(scores: list[SampleScore]):
        clean = [s for s in scores if s.sample_metadata and s.sample_metadata.get("expected") == "PASS"]
        if not clean:
            return float("nan")
        return sum(1 for s in clean if s.score.as_float() == 1.0) / len(clean)
    return compute


@metric
def mutation_sensitivity():
    """Fraction of laundering (must-FAIL) fixtures correctly rejected: 1 - FNR."""
    def compute(scores: list[SampleScore]):
        mut = [s for s in scores if s.sample_metadata and s.sample_metadata.get("expected") == "FAIL"]
        if not mut:
            return float("nan")
        return sum(1 for s in mut if s.score.as_float() == 1.0) / len(mut)
    return compute


# ── scorer: verdict accuracy against INDEPENDENT gold ─────────────────────────
@scorer(metrics=[verdict_accuracy()])
def verdict():
    async def score(state, target):
        got = state.output.completion
        expected = state.metadata["expected"]
        correct = (got == expected)
        return Score(
            value=correct,
            answer=got,
            explanation=(
                f"fixture={state.metadata['fixture_id']} expected={expected} got={got} "
                f"problems={state.store.get('detector_problems')}"
            ),
        )
    return score


@scorer(metrics=[clean_specificity(), mutation_sensitivity()])
def verdict_split():
    """Same scoring but attached to split metrics (clean/mutation)."""
    async def score(state, target):
        got = state.output.completion
        expected = state.metadata["expected"]
        correct = (got == expected)
        return Score(value=correct, answer=got, explanation=state.metadata["fixture_id"])
    return score


@task
def arglaundry():
    ds = build_dataset()
    return Task(
        dataset=ds,
        solver=run_detector(),
        scorer=[verdict(), verdict_split()],
        name="arglaundry",
        version=VERSION,
        metadata={"bench": BENCH, "pinned_inspect": PINNED_INSPECT,
                  "dataset_hash": dataset_hash(ds.samples),
                  "detector_sha": detector_sha()},
    )


if __name__ == "__main__":
    ds = build_dataset()
    print(f"{BENCH} {VERSION} dataset: {len(ds.samples)} fixtures "
          f"({sum(1 for s in ds.samples if s.metadata['expected']=='PASS')} PASS, "
          f"{sum(1 for s in ds.samples if s.metadata['expected']=='FAIL')} FAIL)")
    for s in ds.samples:
        m = s.metadata
        print(f"  {m['expected']:4} {m['fixture_id']:36} object_hash={m['object_hash'][:10]}")
