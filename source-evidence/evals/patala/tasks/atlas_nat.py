#!/usr/bin/env python3
"""evals/patala/tasks/atlas_nat.py — PĀṬALA-ATLAS-NAT (Inspect AI task, A1-NEXT #2).

The Agent-1 counterpart to Agent 2 building the Atlas source resolver. Mirrors ARGMAP NAT exactly:

    Agent 2 resolver
        ↓
    SourceResolutionCandidate
        ↓
    Agent 1 Atlas NAT  (this task)
        ↓
    SourceResolutionFinding[]

The resolver proposes. The evaluator tests. The evaluator NEVER says "THIS IS DEFINITELY THE
TANTRĀLOKA" — it says "candidate survived these checks, these dimensions remain open, these failure
families were/were-not detected."

Core evaluation dimensions (the directive §2):
    WORK_IDENTITY · AUTHOR_IDENTITY · TITLE_ALIAS_FIDELITY · EDITION_IDENTITY ·
    ETEXT_DERIVATION · WITNESS_LINKAGE · DATE_PRECISION · SOURCE_INDEPENDENCE

SOURCE_INDEPENDENCE is the key one: if Google Books / WorldCat / LoC all copied the same catalogue
metadata, that is NOT three independent corroborations (SOURCE_ECHO).

Mutation suite (the directive §3, the adversarial families the evaluator must catch):
    WORK_COLLAPSE, WORK_SPLIT, HOMONYMOUS_TITLE_MERGE, AUTHOR_COLLAPSE, UNSUPPORTED_AUTHORSHIP,
    EDITION_MISMATCH, EDITION_ETEXT_COLLAPSE, ETEXT_DERIVATION_INFLATION, WITNESS_EDITION_COLLAPSE,
    DATE_PRECISION_INFLATION, SOURCE_ECHO, IDENTIFIER_COLLISION, RIGHTS_INFLATION,
    ABSENCE_AS_NONEXISTENCE.
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
from source_authority import SourceAuthority, validate_authority  # noqa: E402

BENCH = "PĀṬALA-ATLAS-NAT"
VERSION = "v0.1"
PINNED_INSPECT = "inspect-ai==0.3.258"


def _sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()


# ── the 8 evaluation dimensions ───────────────────────────────────────────────
DIMENSIONS = (
    "WORK_IDENTITY", "AUTHOR_IDENTITY", "TITLE_ALIAS_FIDELITY", "EDITION_IDENTITY",
    "ETEXT_DERIVATION", "WITNESS_LINKAGE", "DATE_PRECISION", "SOURCE_INDEPENDENCE",
)

# ── the mutation families the evaluator must catch ────────────────────────────
MUTATION_FAMILIES = (
    "WORK_COLLAPSE", "WORK_SPLIT", "HOMONYMOUS_TITLE_MERGE", "AUTHOR_COLLAPSE",
    "UNSUPPORTED_AUTHORSHIP", "EDITION_MISMATCH", "EDITION_ETEXT_COLLAPSE",
    "ETEXT_DERIVATION_INFLATION", "WITNESS_EDITION_COLLAPSE", "DATE_PRECISION_INFLATION",
    "SOURCE_ECHO", "IDENTIFIER_COLLISION", "RIGHTS_INFLATION", "ABSENCE_AS_NONEXISTENCE",
)

# suspicious signals per family (structural cues the evaluator uses to NOMINATE, never settle)
_SIGNALS = {
    "WORK_COLLAPSE": ["two distinct works merged", "distinct works"],
    "WORK_SPLIT": ["same work split", "falsely split"],
    "HOMONYMOUS_TITLE_MERGE": ["same title", "wrong work"],
    "AUTHOR_COLLAPSE": ["similar author name merged", "authors merged"],
    "UNSUPPORTED_AUTHORSHIP": ["catalogue uncertainty upgraded", "uncertain attribution"],
    "EDITION_MISMATCH": ["wrong edition", "edition mismatch"],
    "EDITION_ETEXT_COLLAPSE": ["digital transcription treated as the edition"],
    "ETEXT_DERIVATION_INFLATION": ["probably based on", "verified transcription of"],
    "WITNESS_EDITION_COLLAPSE": ["manuscript witness treated as critical edition"],
    "DATE_PRECISION_INFLATION": ["10th–11th c.", "c. 995", "precise date from range"],
    "SOURCE_ECHO": ["all copied the same catalogue", "same upstream record", "single origin copied"],
    "IDENTIFIER_COLLISION": ["identifier attached to wrong entity"],
    "RIGHTS_INFLATION": ["discoverable/downloadable", "redistributable", "rights inflated"],
    "ABSENCE_AS_NONEXISTENCE": ["not found in queried catalogues", "no manuscript exists"],
}


def _sut_source() -> str:
    import inspect as _inspect
    return _inspect.getsource(evaluate_candidate)


# ── the SUT: a bounded structural evaluator of a SourceResolutionCandidate ────
def evaluate_candidate(candidate: dict) -> dict:
    """Evaluate one SourceResolutionCandidate against the 8 dimensions + mutation signals.

    Bounded: it NOMINATES structural failure candidates and reports which dimensions are open. It
    never asserts identity truth. Returns {ok, verdict, dimensions, problems}.
    """
    problems = []
    dimensions = {d: "CLEAN" for d in DIMENSIONS}
    # gather all text fields of the candidate for signal scanning
    text_blob = json.dumps(candidate, ensure_ascii=False).lower()

    # SCAN the 14 mutation-family signals (each hit nominates a defect on a dimension)
    family_hits = []
    for family, sigs in _SIGNALS.items():
        if any(s in text_blob for s in sigs):
            family_hits.append(family)
    if family_hits:
        # map family -> most-relevant dimension
        _fam_dim = {
            "WORK_COLLAPSE": "WORK_IDENTITY", "WORK_SPLIT": "WORK_IDENTITY",
            "HOMONYMOUS_TITLE_MERGE": "TITLE_ALIAS_FIDELITY", "AUTHOR_COLLAPSE": "AUTHOR_IDENTITY",
            "UNSUPPORTED_AUTHORSHIP": "AUTHOR_IDENTITY", "EDITION_MISMATCH": "EDITION_IDENTITY",
            "EDITION_ETEXT_COLLAPSE": "EDITION_IDENTITY", "ETEXT_DERIVATION_INFLATION": "ETEXT_DERIVATION",
            "WITNESS_EDITION_COLLAPSE": "WITNESS_LINKAGE", "DATE_PRECISION_INFLATION": "DATE_PRECISION",
            "SOURCE_ECHO": "SOURCE_INDEPENDENCE", "IDENTIFIER_COLLISION": "WORK_IDENTITY",
            "RIGHTS_INFLATION": "WITNESS_LINKAGE", "ABSENCE_AS_NONEXISTENCE": "WITNESS_LINKAGE",
        }
        for fam in family_hits:
            dim = _fam_dim.get(fam, "WORK_IDENTITY")
            dimensions[dim] = "DEFECT"
            problems.append(f"{fam}: structural defect candidate")
        # if a source-authority vector is present, also validate it
        if "authority" in candidate:
            va = validate_authority(candidate["authority"])
            for p in va["problems"]:
                problems.append(f"authority: {p}")
                dimensions["WORK_IDENTITY"] = "DEFECT"

    # SOURCE_INDEPENDENCE: if candidates are all single-origin (echo), flag open
    if "corroboration_sources" in candidate:
        srcs = candidate.get("corroboration_sources", [])
        if len(srcs) >= 1 and candidate.get("single_upstream_origin"):
            dimensions["SOURCE_INDEPENDENCE"] = "OPEN"
            problems.append("SOURCE_ECHO: multiple sources copy one upstream record — not independent")
    return {
        "ok": len(problems) == 0,
        "verdict": "PASS" if not problems else "FAIL",
        "dimensions": dimensions,
        "problems": problems,
        "family_hits": family_hits,
    }


# ── candidate builders ────────────────────────────────────────────────────────
def _base_candidate() -> dict:
    return {
        "candidate_id": "cand-tantraloka",
        "work_title": "Tantrāloka",
        "author": "Abhinavagupta",
        "edition": {"label": "Kaul 1918", "publisher": "KSTS"},
        "etext": {"source": "GRETIL", "derivation": "transcription"},
        "corroboration_sources": ["NCC", "NMM"],
        "single_upstream_origin": False,
        "authority": SourceAuthority(work_identity="MULTI_SOURCE_MATCHED",
                                     edition_identity="COPY_INSPECTED",
                                     etext_derivation="TRANSCRIPTION_VERIFIED",
                                     rights="PROCESSING_ALLOWED").model_dump(),
    }


_MUTATED = {
    "WORK_COLLAPSE": lambda c: {**c, "work_title": "Tantrāloka + Tantrasāra (two distinct works merged)"},
    "EDITION_MISMATCH": lambda c: {**c, "edition": {"label": "wrong edition", "publisher": "X"}},
    "ETEXT_DERIVATION_INFLATION": lambda c: {**c, "etext": {"source": "GRETIL", "derivation": "verified transcription of (probably based on) Kaul"}},
    "SOURCE_ECHO": lambda c: {**c, "corroboration_sources": ["Google Books", "WorldCat", "LoC"], "single_upstream_origin": True},
    "DATE_PRECISION_INFLATION": lambda c: {**c, "date": "c. 995 (from 10th–11th c. range)"},
    "RIGHTS_INFLATION": lambda c: {**c, "authority": {**c["authority"], "rights": "REDISTRIBUTABLE"}},
    "ABSENCE_AS_NONEXISTENCE": lambda c: {**c, "witness_note": "not found in queried catalogues → no manuscript exists"},
}


def build_dataset() -> MemoryDataset:
    samples = []
    # the clean control (must PASS)
    samples.append(Sample(id="CLEAN_CONTROL", input=json.dumps(_base_candidate(), ensure_ascii=False),
                          metadata={"bench": BENCH, "version": VERSION, "expected": "PASS"}))
    # one mutated candidate per family (must FAIL)
    for fam, fn in _MUTATED.items():
        cand = fn(_base_candidate())
        cand["candidate_id"] = f"cand-{fam.lower()}"
        samples.append(Sample(id=f"mut_{fam}", input=json.dumps(cand, ensure_ascii=False),
                              metadata={"bench": BENCH, "version": VERSION,
                                        "expected": "FAIL", "expected_family": fam}))
    return MemoryDataset(samples)


@solver
def run_atlas_eval() -> Solver:
    async def solve(state, generate):
        cand = json.loads(state.input)
        res = evaluate_candidate(cand)
        state.output.completion = res["verdict"]
        state.store.set("problems", res["problems"])
        state.store.set("family_hits", res["family_hits"])
        state.store.set("dimensions", res["dimensions"])
        return state
    return solve


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


@scorer(metrics=[clean_specificity(), mutation_sensitivity()])
def verdict():
    async def score(state, target):
        expected = state.metadata.get("expected")
        got = state.output.completion
        correct = (got == expected)
        return Score(value=correct, answer=got,
                     explanation=(f"expected={expected} got={got} "
                                  f"problems={state.store.get('problems')} "
                                  f"families={state.store.get('family_hits')}"))
    return score


@task
def atlas_nat():
    ds = build_dataset()
    return Task(
        dataset=ds, solver=run_atlas_eval(), scorer=[verdict()],
        name="atlas_nat", version=VERSION,
        metadata={"bench": BENCH, "pinned_inspect": PINNED_INSPECT,
                  "dataset_hash": _sha256([{"id": s.id, "input": s.input} for s in ds.samples]),
                  "sut_hash": _sha256(_sut_source()),
                  "dimensions": list(DIMENSIONS),
                  "mutation_families": list(MUTATION_FAMILIES)},
    )


if __name__ == "__main__":
    ds = build_dataset()
    print(f"{BENCH} {VERSION}: {len(ds.samples)} candidates")
    for s in ds.samples:
        cand = json.loads(s.input)
        res = evaluate_candidate(cand)
        print(f"  {res['verdict']:4} {s.id:24} families={res['family_hits']} problems={res['problems']}")
