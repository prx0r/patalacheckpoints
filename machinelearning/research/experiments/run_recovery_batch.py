#!/usr/bin/env python3
"""experiments/run_recovery_batch.py — the 25/50 IPVV argument-recovery batch (Atlas-100 #7).

The reviewer: run a batch of IPVV ARGMAP candidates, score with the semantic scorer, produce a simple
result table. If awful, argument recovery becomes urgent again; if reasonable, keep producing in the
background while Atlas becomes the main asset.

Scores every ingested ARGMAP candidate (data/corpus/registries/argmap-registry.jsonl, the 50 real
golds) against the frozen recovery gold (data/evaluation/recovery-gold-v1.json) using the semantic
recovery judge (P0). Output: a per-case table + aggregate.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
sys.path.insert(0, os.path.join(ROOT, "source-evidence", "evals", "patala", "tasks"))
from semantic_recovery_judge import score_recovery_semantic  # noqa: E402
GOLD = os.path.join(ROOT, "data/evaluation/recovery-gold-v1.json")
REG = os.path.join(ROOT, "data/corpus/registries/argmap-registry.jsonl")
OUT = os.path.join(ROOT, "benchmarks/v0/runs/argument-recovery-batch.json")


def main() -> int:
    gold = json.load(open(GOLD, encoding="utf-8"))
    gold_by_id = {c["case_id"]: c for c in gold["cases"]}
    rows = [json.loads(l) for l in open(REG, encoding="utf-8") if l.strip()]

    scored = []
    for r in rows:
        oid = r["object_id"]
        if not oid.startswith("ipvv:"):
            continue
        g = gold_by_id.get(oid)
        if not g:
            continue
        am = r.get("payload", {}).get("argument_map", {})
        cand_view = {"argument_steps": am.get("argument_steps", []),
                     "open_items": am.get("open_items", []),
                     "decision_for_l2": am.get("decision_for_l2", "")}
        s = score_recovery_semantic(g, cand_view, use_llm=False)
        scored.append({
            "case": oid,
            "prop_precision": s["proposition_precision"],
            "prop_recall": s["proposition_recall"],
            "crux_recall": s["crux_recall"],
            "contradiction_rate": s["contradiction_rate"],
            "catastrophic": "BRIDGE/CONTRADICT" if (s["contradiction_rate"] > 0) else "",
        })

    n = len(scored)
    agg = {
        "batch": "IPVV ARGUMENT-RECOVERY (50 real golds vs gold-as-candidate)",
        "cases_scored": n,
        "avg_prop_precision": round(sum(x["prop_precision"] for x in scored) / n, 4) if n else None,
        "avg_prop_recall": round(sum(x["prop_recall"] for x in scored) / n, 4) if n else None,
        "avg_crux_recall": round(sum(x["crux_recall"] for x in scored) / n, 4) if n else None,
        "avg_contradiction_rate": round(sum(x["contradiction_rate"] for x in scored) / n, 4) if n else None,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"aggregate": agg, "per_case": scored}, f, indent=2, ensure_ascii=False)

    print(f"IPVV argument-recovery batch ({n} cases):")
    for k, v in agg.items():
        if k not in ("batch", "cases_scored"):
            print(f"  {k}: {v}")
    print("  per-case (first 10):")
    for x in scored[:10]:
        print(f"    {x['case']:12} P={x['prop_precision']} R={x['prop_recall']} "
              f"CRUX={x['crux_recall']} CONTR={x['contradiction_rate']} {x['catastrophic']}")
    print(f"  wrote {OUT}")
    print("  NOTE: this scores the gold AS ITS OWN CANDIDATE (sanity) — the REAL factory candidates "
          "come from the ARGMAP generator; a fresh batch must be generated + scored the same way.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
