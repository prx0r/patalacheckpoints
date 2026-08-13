#!/usr/bin/env python3
"""experiments/run_argument_recovery_bench.py — run ARGUMENT-RECOVERY-BENCH-v1 on real candidates.

Agent 1 P0 runner: score generated ARGMAP candidates against the frozen recovery-gold.

Usage:
    # score the ingested gold ARGMAPs as a sanity baseline (gold-vs-gold, validates wiring)
    python3 experiments/run_argument_recovery_bench.py --candidates=registry

    # score a single candidate JSON (an ARGMAP producer's blind output) against one gold
    python3 experiments/run_argument_recovery_bench.py --candidate=<cand.json> --case=ipvv:V2L

The output is the recovery report: proposition precision/recall, speaker accuracy, commitment
accuracy, inference recovery, warrant invention rate, UNSUPPORTED_BRIDGE_RATE, qualification
retention, crux recall, open-question preservation — plus the aggregate.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "source-evidence", "evals", "patala", "tasks"))
from argument_recovery_bench import score_recovery, aggregate  # noqa: E402

GOLD = os.path.join(ROOT, "data/evaluation/recovery-gold-v1.json")
REG = os.path.join(ROOT, "data/corpus/registries/argmap-registry.jsonl")


def load_gold():
    return json.load(open(GOLD, encoding="utf-8"))["cases"]


def load_candidates_from_registry():
    """Use the ingested gold ARGMAPs as candidate maps (gold-vs-gold sanity baseline)."""
    rows = [json.loads(l) for l in open(REG, encoding="utf-8") if l.strip()]
    return [{"case_id": r["object_id"], "argument_map": r["payload"].get("argument_map", {})}
            for r in rows if r["object_id"].startswith("ipvv:")]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", choices=["registry"], default=None)
    ap.add_argument("--candidate", help="path to a candidate ARGMAP JSON")
    ap.add_argument("--case", help="the gold case_id to score against (when --candidate given)")
    a = ap.parse_args()

    golds = load_gold()
    gold_by_id = {g["case_id"]: g for g in golds}

    if a.candidates == "registry":
        candidates = load_candidates_from_registry()
        scores = []
        for cand in candidates:
            g = gold_by_id.get(cand["case_id"])
            if not g:
                continue
            am = cand["argument_map"]
            cand_view = {"argument_steps": am.get("argument_steps", []),
                         "decision_for_l2": am.get("decision_for_l2", ""),
                         "open_items": am.get("open_items", [])}
            scores.append(score_recovery(g, cand_view))
        agg = aggregate(scores)
        print(f"ARGUMENT-RECOVERY-BENCH-v1 (gold-vs-gold sanity on {agg['cases']} ingested golds):")
        for k, v in agg.items():
            if k != "cases":
                print(f"  {k}: {v}")
        print("\n  note: this is the gold-as-its-own-candidate baseline (validates scorer wiring). "
              "The real signal comes when the factory produces a FRESH candidate for the same passage.")
        out = os.path.join(ROOT, "benchmarks/v0/runs/argument-recovery-sanity.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(agg, f, indent=2, ensure_ascii=False)
        print(f"  wrote {out}")
        return 0

    if a.candidate and a.case:
        g = gold_by_id.get(a.case)
        if not g:
            print(f"case {a.case} not in gold (have {len(golds)} cases)")
            return 1
        cand = json.load(open(a.candidate, encoding="utf-8"))
        am = cand.get("argument_map", cand)
        cand_view = {"argument_steps": am.get("argument_steps", []),
                     "decision_for_l2": am.get("decision_for_l2", ""),
                     "open_items": am.get("open_items", [])}
        r = score_recovery(g, cand_view)
        print(f"ARGUMENT-RECOVERY-BENCH-v1 candidate {a.case}:")
        for k, v in r.items():
            if k != "case_id":
                print(f"  {k}: {v}")
        return 0

    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
