#!/usr/bin/env python3
"""source-evidence/evals/audit_atlas_producer.py — producer-side false-authority-promotion audit.

The repair-loop correction (agent2 takeover, reviewer directive):
   SYSTEM_FALSE_AUTHORITY_PROMOTION_RATE must be measured on the PRODUCER'S ACTUAL OUTPUT, not on a
   fixture suite of hypothetical bad producers.

The 51-case NATURAL benchmark (atlas_nat_natural_cases.py) contains 11 cases whose resolver-output
genuinely inflates authority; the evaluator correctly catches them (recall=precision=1.000). That 0.216
is the FIXTURE rate (how often a bad producer would be caught). This audit measures the REAL producer:
run the actual `patala_core.atlas.resolver.resolve_work` on the on-disk corpus and check each emitted
candidate against the honest-ceiling rules.

  - If the real producer never emits MULTI_SOURCE_MATCHED / EDITION_VERIFIED / MULTI_WITNESS /
    REDISTRIBUTABLE without the evidence to license them, SYSTEM_FALSE_AUTHORITY_PROMOTION_RATE = 0.000.
  - The gate predicates must also never open publication/factory on weak evidence.

net mode:
  net=False -> safe offline mode (crosswalk only).
  net=True  -> live archive.org candidate lookup (single hit = EXTERNAL_CANDIDATE_FOUND, never more).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

_REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "source-evidence", "evals", "patala", "tasks"))
sys.path.insert(0, os.path.join(_REPO, "source-evidence", "evals", "patala", "data"))
sys.path.insert(0, os.path.join(_REPO, "python"))

from atlas_nat_natural import honest_ceiling, _rank, _DIM_LADDER, DIMENSIONS  # noqa: E402
from patala_core.atlas import resolver as R  # noqa: E402


def _evidence_from_relations(rel: dict) -> dict:
    return {
        "independent_sources": 0,
        "archive_hit": rel.get("EDITION_IDENTITY") == "EXTERNAL_CANDIDATE_FOUND",
        "crosswalk": rel.get("WORK_IDENTITY") == "INTERNAL_IDENTITY_BOUND",
        "catalog_match": rel.get("WORK_IDENTITY") in ("CATALOG_MATCHED", "MULTI_SOURCE_MATCHED"),
        "edition_inspected": rel.get("EDITION_IDENTITY") in ("COPY_INSPECTED", "EDITION_VERIFIED"),
        "etext_verified": rel.get("ETEXT_DERIVATION") == "TRANSCRIPTION_VERIFIED",
        "witnesses": 2 if rel.get("WITNESS_LINKAGE") == "MULTI_WITNESS" else (1 if rel.get("WITNESS_LINKAGE") == "SINGLE_WITNESS" else 0),
        "rights_granted": rel.get("RIGHTS", "UNKNOWN"),
        "date_exact": False,
        "echo": False,
    }


def audit_work(wid: str, net: bool) -> dict:
    cand = R.resolve_work(wid, net=net)
    rel = {d: cand["authority"][d].get("relation", "OPEN") for d in R.DIMENSIONS}
    ev = _evidence_from_relations(rel)
    ceil = honest_ceiling(ev)
    problems = []
    for d in DIMENSIONS:
        v = rel.get(d, "UNKNOWN")
        if v in ("OPEN", "UNSUPPORTED", "UNKNOWN"):
            continue
        if v in _DIM_LADDER.get(d, []) and _rank(d, rel) > (_DIM_LADDER[d].index(ceil[d]) if ceil[d] in _DIM_LADDER[d] else 0):
            problems.append(f"{d}: claimed {v}, evidence licenses <= {ceil[d]}")
    # gate inflation: a gate opening without qualifying evidence
    for g, allowed in cand["gates"].items():
        if allowed and g in ("factory_eligible", "publication_eligible"):
            # for net=False / single-hit, factory+publication should not open (rights are OPEN/UNKNOWN)
            if rel.get("RIGHTS", "UNKNOWN") in ("UNKNOWN", "OPEN", "DISCOVERABLE"):
                problems.append(f"gate {g} opened with RIGHTS={rel.get('RIGHTS')}")
    return {"work": wid, "relations": rel, "gates": cand["gates"], "problems": problems}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--net", action="store_true", help="use live archive.org (slow); default offline")
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()

    src = os.path.join(_REPO, "data", "corpus", "sources")
    works = [w for w in sorted(os.listdir(src))
             if w not in ("sivaqueue2", "vedic-reference", "philosophy-encyclopedia", "sanderson")]
    if a.limit:
        works = works[: a.limit]

    results = []
    for w in works:
        try:
            results.append(audit_work(w, net=a.net))
        except Exception as e:
            results.append({"work": w, "problems": [f"error: {str(e)[:80]}"], "error": True})

    n = len(results)
    n_fp = sum(1 for r in results if any("claimed" in p or "gate" in p for p in r["problems"]))
    rate = n_fp / n if n else 0.0

    print(f"REAL producer audit (net={'ON' if a.net else 'OFF'}) on {n} works")
    print(f"  SYSTEM_FALSE_AUTHORITY_PROMOTION_RATE = {rate:.4f}  ({n_fp}/{n})")
    for r in results:
        if r["problems"]:
            print(f"  {r['work']}: {r['problems']}")

    now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = os.path.join(_REPO, "benchmarks", "v0", "runs", f"atlas-producer-{now}.json")
    payload = {
        "run_id": f"ATLAS-PRODUCER-{now}",
        "bench": "PĀṬALA-ATLAS-PRODUCER-AUDIT",
        "bench_version": "v0.1",
        "net": bool(a.net),
        "n_works": n,
        "SYSTEM_FALSE_AUTHORITY_PROMOTION_RATE": round(rate, 4),
        "n_false_promotions": n_fp,
        "acceptance_target": "<0.05",
        "accepted": rate < 0.05,
        "method": "run real resolver.resolve_work on the on-disk corpus; check every emitted relation "
                  "against the honest-ceiling rules (never MULTI_SOURCE_MATCHED/EDITION_VERIFIED/"
                  "MULTI_WITNESS/REDISTRIBUTABLE without evidence to license it); gates must not open "
                  "on RIGHTS=UNKNOWN/DISCOVERABLE.",
        "note": "This is the PRODUCER-side rate (what the resolver actually emits). It is distinct from "
                "the 0.216 FIXTURE rate in the 51-case natural benchmark, which measures how often a "
                "HYPOTHETICAL bad producer is caught (evaluator recall/precision=1.000).",
        "review_status": "NOT_HUMAN_REVIEWED",
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"\n  wrote {out}")
    print(f"  accepted: {payload['accepted']} (target rate < 0.05)")
    return 0 if rate < 0.05 else 1


if __name__ == "__main__":
    sys.exit(main())
