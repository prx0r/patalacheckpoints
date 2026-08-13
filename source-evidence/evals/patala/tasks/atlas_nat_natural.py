#!/usr/bin/env python3
"""evals/patala/tasks/atlas_nat_natural.py — PĀṬALA-ATLAS-NAT-NATURAL-v1 (A1-CONTINUE-v2 P0).

The peer review's correction, applied to a real benchmark: ATLAS-NAT getting 1.000 on its own designed
mutations is NOT evidence it distinguishes good/bad bibliography reconciliation in the wild.

This is the NATURAL benchmark: 26 frozen real-world source-resolution ambiguities
(`atlas_nat_natural_cases.py`), each with its HONEST expected authority state, scored across the 8
authority dimensions. The PRIMARY metric is FALSE AUTHORITY PROMOTION RATE.

Epistemic rule (from the review):
    UNKNOWN -> OPEN    is cheap (always allowed, never penalized).
    UNKNOWN -> VERIFIED is dangerous (a false promotion).

Never:
    weak catalogue hit  ->  publication authority
    internal crosswalk  ->  MULTI_SOURCE_MATCHED
    one archive.org hit ->  MULTI_SOURCE_MATCHED
    discoverable-only   ->  redistributable / open license

The evaluator never says "THIS IS DEFINITELY X"; it reports which dimensions a candidate inflated
(claimed a stronger relation than its evidence licenses) and whether any gate was wrongly opened.
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
sys.path.insert(0, os.path.join(_TASKS, "..", "data"))
from source_authority import validate_authority  # noqa: E402
from atlas_nat_natural_cases import DIMENSIONS, NATURAL_SET_HASH, get_cases  # noqa: E402

BENCH = "PĀṬALA-ATLAS-NAT-NATURAL-v1"
VERSION = "v0.1"
PINNED_INSPECT = "inspect-ai==0.3.258"

# the strong relations a dimension may NOT reach without real evidence (all those ABOVE the open max)
_DIM_LADDER = {
    "WORK_IDENTITY": ["UNKNOWN", "DISCOVERED", "INTERNAL_IDENTITY_BOUND", "EXTERNAL_CANDIDATE_FOUND",
                      "CATALOG_MATCHED", "MULTI_SOURCE_MATCHED"],
    "AUTHOR_IDENTITY": ["UNKNOWN", "SELF_ATTRIBUTED", "CATALOG_SUPPORTED", "MULTI_SOURCE_CONFIRMED"],
    "EDITION_IDENTITY": ["UNKNOWN", "DISCOVERED", "INTERNAL_IDENTITY_BOUND", "EXTERNAL_CANDIDATE_FOUND",
                         "CATALOG_MATCHED", "COPY_INSPECTED", "EDITION_VERIFIED"],
    "ETEXT_DERIVATION": ["UNKNOWN", "OPEN", "PROBABLE_BASIS", "TRANSCRIPTION_VERIFIED"],
    "WITNESS_LINKAGE": ["UNKNOWN", "UNRESOLVED", "SINGLE_WITNESS", "MULTI_WITNESS"],
    "DATE_PRECISION": ["UNKNOWN", "APPROXIMATE", "EXACT"],
    "RIGHTS": ["UNKNOWN", "DISCOVERABLE", "PROCESSING_ALLOWED", "REDISTRIBUTABLE", "OPEN_LICENSE"],
    "SOURCE_INDEPENDENCE": ["SINGLE_SOURCE", "MULTI_SOURCE"],
}

# gate-open predicates (which relations may open which gate) — authority-inflation-fix semantics
_GATE_RULES = {
    # factory: usable as a translation source (needs a usable edition + processing rights)
    "factory": lambda a: _rank("EDITION_IDENTITY", a) >= 3 and _rank("RIGHTS", a) >= 2,
    # publication: redistributable rights + inspected edition (never a single archive hit / crosswalk)
    "publication": lambda a: _rank("RIGHTS", a) >= 3 and _rank("EDITION_IDENTITY", a) >= 5,
    # scholar review: a positively identified work
    "scholar": lambda a: _rank("WORK_IDENTITY", a) >= 4,
}


def _rank(dim, authority):
    ladder = _DIM_LADDER.get(dim, [])
    val = authority.get(dim, "UNKNOWN")
    if isinstance(val, dict):
        val = val.get("relation", "UNKNOWN")
    return ladder.index(val) if val in ladder else 0


def _looks_exact(date_str: str) -> bool:
    """A claimed date is 'exact-looking' if it asserts a specific year without an approx/range marker."""
    low = date_str.lower()
    if not date_str or date_str == "UNKNOWN" or date_str == "OPEN":
        return False
    if "approx" in low or "c." in low or "ca." in low or "circa" in low:
        return False
    if "-" in date_str or "–" in date_str or "centur" in low or "th" in low and low.isascii():
        return False
    # a bare 4-digit year
    return len(date_str.strip()) == 4 and date_str.strip().isdigit()


def evidence_date_is_exact(date_str: str) -> bool:
    """True when the claimed DATE_PRECISION asserts a specific attested year (not approx/range)."""
    return _looks_exact(date_str)


# ── the honest-ceiling rules: given the EVIDENCE, what is the strongest relation each dimension may
#    honestly claim? This is the NON-CIRCULAR core: it reads only `evidence` facts, never my labels. ─
def honest_ceiling(evidence: dict) -> dict:
    """Derive, per dimension, the strongest relation the evidence factually licenses."""
    indep = evidence.get("independent_sources", 0)
    archive = evidence.get("archive_hit", False)
    crosswalk = evidence.get("crosswalk", False)
    catalog = evidence.get("catalog_match", False)
    inspected = evidence.get("edition_inspected", False)
    etext = evidence.get("etext_verified", False)
    witnesses = evidence.get("witnesses", 0)
    rights = evidence.get("rights_granted", "UNKNOWN")
    date_exact = evidence.get("date_exact", False)
    echo = evidence.get("echo", False)

    # WORK_IDENTITY: multi-source needs >=2 INDEPENDENT sources (echo collapses them)
    if indep >= 2 and not echo:
        work = "MULTI_SOURCE_MATCHED"
    elif catalog and indep >= 1 and not echo and not evidence.get("ambiguous_match", False):
        work = "CATALOG_MATCHED"
    elif archive or witnesses >= 1:
        work = "EXTERNAL_CANDIDATE_FOUND"
    elif crosswalk:
        work = "INTERNAL_IDENTITY_BOUND"
    else:
        work = "DISCOVERED"

    # AUTHOR_IDENTITY
    if indep >= 2 and not echo:
        author = "MULTI_SOURCE_CONFIRMED"
    elif catalog:
        author = "CATALOG_SUPPORTED"
    elif archive:
        author = "SELF_ATTRIBUTED"
    else:
        author = "UNKNOWN"

    # EDITION_IDENTITY
    if inspected and indep >= 2 and not echo:
        edition = "EDITION_VERIFIED"
    elif inspected:
        edition = "COPY_INSPECTED"
    elif catalog:
        edition = "CATALOG_MATCHED"
    elif archive:
        edition = "EXTERNAL_CANDIDATE_FOUND"
    else:
        edition = "DISCOVERED"

    # ETEXT_DERIVATION
    etext_rel = "TRANSCRIPTION_VERIFIED" if etext else ("PROBABLE_BASIS" if catalog or archive else "OPEN")

    # WITNESS_LINKAGE
    witness = "MULTI_WITNESS" if witnesses >= 2 else ("SINGLE_WITNESS" if witnesses >= 1 else "UNRESOLVED")

    # RIGHTS: never claim more than the source actually grants
    rights_rel = rights if rights in ("UNKNOWN", "DISCOVERABLE", "PROCESSING_ALLOWED",
                                      "REDISTRIBUTABLE", "OPEN_LICENSE") else "UNKNOWN"

    # DATE_PRECISION
    date = "EXACT" if date_exact else ("APPROXIMATE" if not date_exact and (catalog or archive) else "UNKNOWN")

    # SOURCE_INDEPENDENCE
    indep_rel = "MULTI_SOURCE" if (indep >= 2 and not echo) else "SINGLE_SOURCE"

    return {
        "WORK_IDENTITY": work, "AUTHOR_IDENTITY": author, "EDITION_IDENTITY": edition,
        "ETEXT_DERIVATION": etext_rel, "WITNESS_LINKAGE": witness, "DATE_PRECISION": date,
        "RIGHTS": rights_rel, "SOURCE_INDEPENDENCE": indep_rel,
    }


def evaluate_natural_case(case: dict) -> dict:
    """Score ONE frozen natural case. Returns {verdict, problems, false_promotions, dims}.

    Non-circular: the honest ceiling is derived ONLY from `evidence` facts. A false promotion is when
    the claimed `authority` relation EXCEEDS the evidence-derived ceiling. `expect_promotion` is not
    read here — it is ground-truth used only by the scoring metrics.
    """
    problems = []
    false_promotions = []
    authority = case.get("authority", {})
    evidence = case.get("evidence", {})

    # 1. normalize per-dimension claimed relations
    relations = {d: (authority.get(d, {}).get("relation", "UNKNOWN")
                     if isinstance(authority.get(d), dict) else authority.get(d, "UNKNOWN"))
                 for d in DIMENSIONS}

    # 2. validate claimed relations are known ladder rungs (or honest opens)
    for d in DIMENSIONS:
        val = relations.get(d, "UNKNOWN")
        if d == "DATE_PRECISION":
            continue  # free-form, checked below
        if val not in _DIM_LADDER.get(d, []) and val not in ("OPEN", "UNSUPPORTED", "APPROXIMATE"):
            problems.append(f"{d} value '{val}' not in ladder")

    # 3. FALSE PROMOTION: claimed authority vs evidence-derived ceiling (the non-circular core)
    ceiling = honest_ceiling(evidence)
    for d in DIMENSIONS:
        val = relations.get(d, "UNKNOWN")
        if val in ("OPEN", "UNSUPPORTED"):
            continue  # honest-open is never inflation
        if d == "DATE_PRECISION":
            # free-form: inflation if an exact year is claimed without an exact date attested
            if evidence.get("date_exact") is False and (_looks_exact(str(val)) or "exact" in str(val).lower()):
                false_promotions.append("DATE_PRECISION inflated (approximate range rendered exact)")
            continue
        if val not in _DIM_LADDER.get(d, []):
            continue
        claimed = _rank(d, authority)
        licit = _DIM_LADDER[d].index(ceiling[d]) if ceiling[d] in _DIM_LADDER[d] else 0
        if claimed > licit:
            false_promotions.append(f"{d} inflated: claimed {val}, evidence licenses ≤ {ceiling[d]}")

    # 4. SOURCE_ECHO: MULTI_SOURCE claimed but evidence is echoed single-origin
    if relations.get("SOURCE_INDEPENDENCE") == "MULTI_SOURCE" and (evidence.get("echo") or evidence.get("independent_sources", 0) < 2):
        false_promotions.append("SOURCE_INDEPENDENCE=MULTI_SOURCE on echoed / single-origin catalogue data (SOURCE_ECHO)")

    # 5. GATES: a gate may open ONLY if its evidence predicate is met (never on weak evidence)
    gates = case.get("gates", {})
    for g, allowed in gates.items():
        if allowed:
            rule = _GATE_RULES.get(g)
            if rule and not rule(relations):
                false_promotions.append(f"FALSE_PROMOTION: gate '{g}' opened without qualifying authority evidence")

    verdict = "PASS" if not false_promotions else "FAIL"
    return {"verdict": verdict, "problems": problems, "false_promotions": false_promotions,
            "relations": relations, "case_id": case.get("id"), "category": case.get("category"),
            "gates": gates}


def build_dataset() -> MemoryDataset:
    return MemoryDataset([
        Sample(id=c["id"], input=c["id"],
               metadata={"bench": BENCH, "version": VERSION, "case_id": c["id"],
                         "category": c["category"], "expected": "PASS"})
        for c in get_cases()
    ])


@solver
def run_natural() -> Solver:
    async def solve(state, generate):
        case = next(c for c in get_cases() if c["id"] == state.input)
        res = evaluate_natural_case(case)
        state.output.completion = res["verdict"]
        state.store.set("problems", res["problems"])
        state.store.set("false_promotions", res["false_promotions"])
        state.store.set("category", res["category"])
        state.store.set("relations", res["relations"])
        return state
    return solve


def _case_expects_promotion(sample_score):
    meta = getattr(sample_score, "sample_metadata", None) or (
        getattr(getattr(sample_score, "sample", None), "metadata", None))
    if not meta:
        return False
    case_id = meta.get("case_id")
    c = next((x for x in get_cases() if x["id"] == case_id), None)
    return bool(c and c.get("expect_promotion"))


def _score_meta(s):
    return getattr(getattr(s, "score", None), "metadata", None) or {}


def _sample_false_promotions(s):
    return _score_meta(s).get("false_promotions", [])


def _sample_relations(s):
    return _score_meta(s).get("relations", {})


@metric
def promotion_detection_recall():
    """Of cases whose resolver-output genuinely contains a false promotion, how many were caught."""
    def compute(scores: list[SampleScore]):
        positives = [s for s in scores if _case_expects_promotion(s)]
        if not positives:
            return float("nan")
        caught = [s for s in positives if _sample_false_promotions(s)]
        return len(caught) / len(positives)
    return compute


@metric
def promotion_detection_precision():
    """Of cases the evaluator flagged, how many genuinely contained a false promotion."""
    def compute(scores: list[SampleScore]):
        flagged = [s for s in scores if _sample_false_promotions(s)]
        if not flagged:
            return float("nan")
        correct = [s for s in flagged if _case_expects_promotion(s)]
        return len(correct) / len(flagged)
    return compute


@metric
def system_false_promotion_rate():
    """SYSTEM primary metric: fraction of natural resolver-outputs that genuinely inflated authority.

    This is the directive's FALSE_AUTHORITY_PROMOTION_RATE: how often the pipeline (in these frozen
    cases) claims more authority than its evidence licenses. It is computed from the frozen case labels
    (expect_promotion), NOT from the evaluator's flags, so it measures the resolver-side problem directly.
    """
    def compute(scores: list[SampleScore]):
        cases = get_cases()
        if not cases:
            return float("nan")
        promoted = [c for c in cases if c.get("expect_promotion")]
        return len(promoted) / len(cases)
    return compute


@metric
def false_rejection_rate():
    """PRIMARY companion: honest cases (no inflation) wrongly flagged as false promotions."""
    def compute(scores: list[SampleScore]):
        honest = [s for s in scores if not _case_expects_promotion(s)]
        if not honest:
            return float("nan")
        wrongly = [s for s in honest if _sample_false_promotions(s)]
        return len(wrongly) / len(honest)
    return compute


@metric
def authority_honesty():
    """Fraction of natural cases that were PASS (no false promotion)."""
    def compute(scores: list[SampleScore]):
        vals = [s.score.as_float() for s in scores]
        return sum(vals) / len(vals) if vals else float("nan")
    return compute


@metric
def open_state_preservation():
    """Fraction of cases where every dimension that MUST stay open remained within its evidence-licensed ceiling."""
    def compute(scores: list[SampleScore]):
        ok = 0
        total = 0
        for s in scores:
            meta = getattr(s, "sample_metadata", None) or (
                getattr(getattr(s, "sample", None), "metadata", None))
            if not meta:
                continue
            total += 1
            c = next((x for x in get_cases() if x["id"] == meta.get("case_id")), None)
            if not c:
                continue
            rel = _sample_relations(s)
            ceiling = honest_ceiling(c.get("evidence", {}))
            preserved = True
            for d in DIMENSIONS:
                v = rel.get(d)
                if not isinstance(v, str) or v in ("OPEN", "UNSUPPORTED", "UNKNOWN"):
                    continue
                if d == "DATE_PRECISION":
                    if evidence_date_is_exact(str(v)) and c.get("evidence", {}).get("date_exact") is False:
                        preserved = False
                    continue
                if v in _DIM_LADDER.get(d, []) and _rank(d, rel) > (_DIM_LADDER[d].index(ceiling[d])
                                                                    if ceiling[d] in _DIM_LADDER[d] else 0):
                    preserved = False
            if preserved:
                ok += 1
        return ok / total if total else float("nan")
    return compute


@scorer(metrics=[system_false_promotion_rate(), promotion_detection_recall(),
                 promotion_detection_precision(), false_rejection_rate(), authority_honesty(),
                 open_state_preservation()])
def natural_score():
    async def score(state, target):
        got = state.output.completion
        fps = state.store.get("false_promotions", [])
        rel = state.store.get("relations", {})
        return Score(value=(got == "PASS"), answer=got,
                     explanation=(f"case={state.metadata.get('case_id')} category={state.store.get('category')} "
                                  f"verdict={got} false_promotions={fps} "
                                  f"problems={state.store.get('problems')}"),
                     metadata={"case_id": state.metadata.get("case_id"),
                               "false_promotions": fps, "relations": rel})
    return score


@task
def atlas_nat_natural():
    ds = build_dataset()
    return Task(
        dataset=ds, solver=run_natural(), scorer=[natural_score()],
        name="atlas_nat_natural", version=VERSION,
        metadata={"bench": BENCH, "pinned_inspect": PINNED_INSPECT,
                  "dataset_hash": NATURAL_SET_HASH,
                  "cases": len(ds.samples),
                  "dimensions": list(DIMENSIONS)},
    )


if __name__ == "__main__":
    cases = get_cases()
    print(f"{BENCH} {VERSION}: {len(cases)} frozen natural cases (hash {NATURAL_SET_HASH[:8]})")
    fps_total = 0
    for c in cases:
        res = evaluate_natural_case(c)
        fps = res["false_promotions"]
        mark = "FP!" if fps else "ok "
        if fps:
            fps_total += 1
        print(f"  {mark} {res['case_id']:10} [{res['category']:22}] verdict={res['verdict']}")
        for fp in fps:
            print(f"       ✗ {fp}")
    print(f"\nfalse promotions: {fps_total}/{len(cases)}")
