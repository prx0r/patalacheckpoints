#!/usr/bin/env python3
"""evals/patala/tasks/synthesis_nat.py — PĀṬALA-SYNTHESIS-NAT (Inspect AI task, devpath9).

Attacks the ArgumentSynthesis. This is Agent 1's most important NAT after ARGMAP: it is the proof
that the synthesis has NOT destroyed the lower-level argument graph (positions, argument direction,
cruxes, counterevidence, scope, openness, speaker attribution, source strength).

The SUT is a bounded structural evaluator of an ArgumentSynthesis (the convergence object from
devpath8). It catches the mutation families that corrupt a synthesis:
    POSITION_COLLAPSE, RIVAL_AS_CONSENSUS, ARGUMENT_DIRECTION_REVERSAL, CRUX_OMISSION,
    COUNTEREVIDENCE_DROP, QUALIFICATION_DROP, SCOPE_INFLATION, OPEN_AS_RESOLVED,
    MINORITY_VIEW_ERASURE, SCHOLAR_ATTRIBUTION_COLLAPSE, SOURCE_STRENGTH_INFLATION.

Gold is derived from the mutation SEMANTICS (what a faithful synthesis must NOT contain), never from
the evaluator's own output (the anti-circularity rule). The evaluator NOMINATES defects; it never
asserts scholarly truth.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys

from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset, Sample
from inspect_ai.scorer import Score, metric, scorer
from inspect_ai.scorer._metric import SampleScore
from inspect_ai.solver import Solver, solver

_TASKS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _TASKS)

BENCH = "PĀṬALA-SYNTHESIS-NAT"
VERSION = "v0.1"
PINNED_INSPECT = "inspect-ai==0.3.258"

# the 11 mutation families the evaluator must catch
MUTATION_FAMILIES = (
    "POSITION_COLLAPSE", "RIVAL_AS_CONSENSUS", "ARGUMENT_DIRECTION_REVERSAL", "CRUX_OMISSION",
    "COUNTEREVIDENCE_DROP", "QUALIFICATION_DROP", "SCOPE_INFLATION", "OPEN_AS_RESOLVED",
    "MINORITY_VIEW_ERASURE", "SCHOLAR_ATTRIBUTION_COLLAPSE", "SOURCE_STRENGTH_INFLATION",
)

# structural signals per family (the evaluator NOMINATES, never settles truth)
_SIGNALS = {
    "POSITION_COLLAPSE": ["positions merged", "collapsed into"],
    "RIVAL_AS_CONSENSUS": ["rival agreed", "consensus", "opponent agreed"],
    "ARGUMENT_DIRECTION_REVERSAL": ["argument reversed", "direction reversed", "refutes the proponent"],
    "CRUX_OMISSION": ["no crux", "cruxes: none", "without crux"],
    "COUNTEREVIDENCE_DROP": ["no counterevidence", "counterevidence removed"],
    "QUALIFICATION_DROP": ["no qualification", "without qualification", "unqualified"],
    "SCOPE_INFLATION": ["all works", "universally", "every tradition", "in all cases"],
    "OPEN_AS_RESOLVED": ["resolved", "settled", "no longer open"],
    "MINORITY_VIEW_ERASURE": ["minority view erased", "only one view"],
    "SCHOLAR_ATTRIBUTION_COLLAPSE": ["attribution collapsed", "attributed to the wrong scholar"],
    "SOURCE_STRENGTH_INFLATION": ["verified", "conclusively", "certainly established"],
}


def _sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()


def _sut_source() -> str:
    import inspect as _inspect
    return _inspect.getsource(evaluate_synthesis)


# ── the SUT: a bounded structural evaluator of an ArgumentSynthesis ──────────
def evaluate_synthesis(synthesis: dict) -> dict:
    """Evaluate one ArgumentSynthesis against the 11 mutation families.

    Bounded: nominates structural defects; never asserts scholarly truth. A faithful synthesis must
    preserve positions, argument direction, cruxes, counterevidence, scope, openness, speaker
    attribution, and source strength — the mutation signals flag when a synthesis corrupted one.
    """
    problems = []
    text_blob = json.dumps(synthesis, ensure_ascii=False).lower()
    family_hits = []
    for family, sigs in _SIGNALS.items():
        if any(re.search(r"\b" + re.escape(sig.rstrip(".")) + r"\b", text_blob) for sig in sigs):
            family_hits.append(family)
            problems.append(f"{family}: structural defect candidate")
    # a faithful synthesis is NOT truth-asserting: empty supported_conclusions + unresolved present
    supported = synthesis.get("supported_conclusions", [])
    unresolved = synthesis.get("unresolved_disagreement", [])
    if supported and not unresolved:
        family_hits.append("RIVAL_AS_CONSENSUS")
        problems.append("RIVAL_AS_CONSENSUS: supported conclusion with no unresolved disagreement")
    return {
        "ok": len(problems) == 0,
        "verdict": "PASS" if not problems else "FAIL",
        "problems": problems,
        "family_hits": family_hits,
    }


# ── a faithful base synthesis ─────────────────────────────────────────────────
def _base_synthesis() -> dict:
    return {
        "synthesis_id": "SYNTH-1",
        "research_question": {"research_question_id": "RQ-1", "question": "Is recognition recollection?"},
        "debate_frame": {
            "debate_frame_id": "DF-1",
            "positions": [{"position_id": "POS-S", "label": "Siddhānta", "stance": "ŚAIVA"},
                          {"position_id": "POS-O", "label": "Opponent", "stance": "OPPONENT"}],
        },
        "arguments": ["ARG-1", "ARG-2"],
        "relations": [{"from_ref": "ARG-1", "to_ref": "ARG-2", "relation": "ATTACKS"}],
        "cruxes": ["CRUX-1"],
        "propositions": ["P1", "P2"],
        "supported_conclusions": [],
        "counterevidence": ["CE-1"],
        "open_questions": ["OQ-1"],
        "scope_boundaries": ["within IPK 1.8"],
        "unresolved_disagreement": ["opponent present"],
        "source_refs": ["pt:passage:ipvv"],
        "review_status": "NOT_REVIEWED",
    }


_MUTATED = {
    "POSITION_COLLAPSE": lambda s: {**s, "debate_frame": {"positions": [s["debate_frame"]["positions"][0]]}, "note": "positions merged"},
    "RIVAL_AS_CONSENSUS": lambda s: {**s, "supported_conclusions": ["the rival agreed"], "unresolved_disagreement": []},
    "ARGUMENT_DIRECTION_REVERSAL": lambda s: {**s, "relations": [{"from_ref": "ARG-2", "to_ref": "ARG-1", "relation": "SUPPORTS"}], "note": "argument reversed"},
    "CRUX_OMISSION": lambda s: {**s, "cruxes": [], "note": "no crux"},
    "COUNTEREVIDENCE_DROP": lambda s: {**s, "counterevidence": [], "note": "counterevidence removed"},
    "QUALIFICATION_DROP": lambda s: {**s, "note": "unqualified claim, no qualification"},
    "SCOPE_INFLATION": lambda s: {**s, "scope_boundaries": ["universally, all works, in all cases"]},
    "OPEN_AS_RESOLVED": lambda s: {**s, "open_questions": [], "note": "settled, no longer open"},
    "MINORITY_VIEW_ERASURE": lambda s: {**s, "debate_frame": {"positions": [s["debate_frame"]["positions"][0]]}, "note": "only one view, minority erased"},
    "SCHOLAR_ATTRIBUTION_COLLAPSE": lambda s: {**s, "note": "attribution collapsed, attributed to the wrong scholar"},
    "SOURCE_STRENGTH_INFLATION": lambda s: {**s, "note": "conclusively verified, certainly established"},
}


def build_dataset() -> MemoryDataset:
    samples = []
    samples.append(Sample(id="CLEAN_CONTROL", input=json.dumps(_base_synthesis(), ensure_ascii=False),
                          metadata={"bench": BENCH, "version": VERSION, "expected": "PASS"}))
    for fam, fn in _MUTATED.items():
        cand = fn(_base_synthesis())
        cand["synthesis_id"] = f"SYNTH-{fam.lower()}"
        samples.append(Sample(id=f"mut_{fam}", input=json.dumps(cand, ensure_ascii=False),
                              metadata={"bench": BENCH, "version": VERSION,
                                        "expected": "FAIL", "expected_family": fam}))
    return MemoryDataset(samples)


@solver
def run_synth_eval() -> Solver:
    async def solve(state, generate):
        synth = json.loads(state.input)
        res = evaluate_synthesis(synth)
        state.output.completion = res["verdict"]
        state.store.set("problems", res["problems"])
        state.store.set("family_hits", res["family_hits"])
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
        return Score(value=(got == expected), answer=got,
                     explanation=(f"expected={expected} got={got} "
                                  f"problems={state.store.get('problems')} "
                                  f"families={state.store.get('family_hits')}"))
    return score


@task
def synthesis_nat():
    ds = build_dataset()
    return Task(
        dataset=ds, solver=run_synth_eval(), scorer=[verdict()],
        name="synthesis_nat", version=VERSION,
        metadata={"bench": BENCH, "pinned_inspect": PINNED_INSPECT,
                  "dataset_hash": _sha256([{"id": s.id, "input": s.input} for s in ds.samples]),
                  "sut_hash": _sha256(_sut_source()),
                  "mutation_families": list(MUTATION_FAMILIES)},
    )


if __name__ == "__main__":
    ds = build_dataset()
    print(f"{BENCH} {VERSION}: {len(ds.samples)} candidates")
    for s in ds.samples:
        res = evaluate_synthesis(json.loads(s.input))
        print(f"  {res['verdict']:4} {s.id:28} families={res['family_hits']}")
