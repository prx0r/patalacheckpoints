#!/usr/bin/env python3
"""evals/record_atlas_nat_natural.py — record a BenchmarkRun for ATLAS-NAT-NATURAL-v1.

Run the frozen natural benchmark offline (no network) and write an immutable BenchmarkRun under
benchmarks/v0/runs/. This is the guardrail-1 artifact: every agent-1 benchmark must leave a run record.

   primary metric (from A1-CONTINUE-v2 P0): SYSTEM_FALSE_AUTHORITY_PROMOTION_RATE
   + evaluator detection recall / precision + false-rejection rate + open-state preservation.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

_REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "source-evidence", "evals", "patala", "tasks"))
sys.path.insert(0, os.path.join(_REPO, "source-evidence", "evals", "patala", "data"))

from atlas_nat_natural_cases import NATURAL_SET_HASH, get_cases  # noqa: E402
from atlas_nat_natural import evaluate_natural_case, DIMENSIONS, BENCH, VERSION  # noqa: E402


def _git(what):
    try:
        return subprocess.check_output(["git", *what.split()], cwd=_REPO,
                                       text=True).strip().splitlines()[-1]
    except Exception:
        return "unknown"


def main() -> int:
    cases = get_cases()
    results = [evaluate_natural_case(c) for c in cases]

    expected_fp = [c for c in cases if c["expect_promotion"]]
    flagged = [r for r in results if r["verdict"] == "FAIL"]
    flagged_ids = {r["case_id"] for r in flagged}
    expected_ids = {c["id"] for c in expected_fp}

    recall = len(flagged_ids & expected_ids) / len(expected_ids) if expected_ids else float("nan")
    precision = len(flagged_ids & expected_ids) / len(flagged_ids) if flagged_ids else float("nan")
    false_rej = len(flagged_ids - expected_ids) / (len(cases) - len(expected_ids)) if (len(cases) - len(expected_ids)) else 0.0
    sys_fp = len(expected_ids) / len(cases)

    # open-state preservation: honest ceiling derived from evidence, claimed <= ceiling
    from atlas_nat_natural import honest_ceiling, _DIM_LADDER, _rank  # noqa: E402
    preserved = 0
    for c, r in zip(cases, results):
        rel = r["relations"]
        ceil = honest_ceiling(c.get("evidence", {}))
        ok = True
        for d in DIMENSIONS:
            v = rel.get(d)
            if not isinstance(v, str) or v in ("OPEN", "UNSUPPORTED", "UNKNOWN"):
                continue
            if d == "DATE_PRECISION":
                continue
            if v in _DIM_LADDER.get(d, []) and _rank(d, rel) > (_DIM_LADDER[d].index(ceil[d]) if ceil[d] in _DIM_LADDER[d] else 0):
                ok = False
        if ok:
            preserved += 1
    open_pres = preserved / len(cases)

    now = datetime.now(timezone.utc)
    ts = now.strftime("%Y%m%dT%H%M%SZ")
    run = {
        "run_id": f"ATLAS-NAT-NATURAL-{ts}",
        "benchmark_version": "v0",
        "family": "PATALA-ATLAS-NAT-NATURAL",
        "bench": BENCH,
        "bench_version": VERSION,
        "framework": "inspect-ai==0.3.258",
        "task": "atlas_nat_natural",
        "execution_base_sha": _git("rev-parse HEAD"),
        "working_tree_dirty": subprocess.call(["git", "diff", "--quiet"], cwd=_REPO) != 0,
        "date": ts,
        "dataset": {"kind": "NATURAL", "objects": len(cases),
                    "frozen_set_hash": NATURAL_SET_HASH,
                    "categories": sorted({c["category"] for c in cases})},
        "sut": "ATLAS source resolver evidence rules (honest_ceiling derived from evidence, non-circular)",
        "metrics": {
            "SYSTEM_FALSE_AUTHORITY_PROMOTION_RATE": round(sys_fp, 4),  # PRIMARY
            "promotion_detection_recall": round(recall, 4),
            "promotion_detection_precision": round(precision, 4),
            "false_rejection_rate": round(false_rej, 4),
            "open_state_preservation": round(open_pres, 4),
            "n_expect_false_promotion": len(expected_ids),
            "n_flagged": len(flagged_ids),
        },
        "findings": [
            f"{len(expected_ids)}/{len(cases)} frozen natural resolver-outputs genuinely inflate authority "
            "(SYSTEM_FALSE_AUTHORITY_PROMOTION_RATE={:.3f}) — the resolver-side problem the evaluator must catch.".format(sys_fp),
            "Evaluator detection: recall={:.3f}, precision={:.3f}, false-rejection={:.3f} — non-circular "
            "(honest ceilings derived from evidence facts, not hand-written labels).".format(recall, precision, false_rej),
        ],
        "notes": "NATURAL benchmark, not a mutation suite: real source-resolution ambiguities frozen with honest "
                 "expected state. UNKNOWN->OPEN is never penalized; UNKNOWN->VERIFIED (false promotion) is the primary metric.",
        "review_status": "NOT_HUMAN_REVIEWED",
    }

    outdir = os.path.join(_REPO, "benchmarks", "v0", "runs")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"atlas-nat-natural-{ts}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(run, f, indent=2, ensure_ascii=False)
    print(f"wrote {path}")
    print(json.dumps(run["metrics"], indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
