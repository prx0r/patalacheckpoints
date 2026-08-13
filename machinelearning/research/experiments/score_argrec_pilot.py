#!/usr/bin/env python3
"""experiments/score_argrec_pilot.py — blind ARGUMENT-RECOVERY scoring for IPVV-ARGREC-PILOT-001.

Gate #5: run the blind recovery scorer on the pilot ARGMAP candidate vs the frozen V2L gold.

Fully OFFLINE — reads only:
    - the frozen gold (data/evaluation/recovery-gold-v1.json, case ipvv:V2L)
    - the pilot ARGMAP candidate (data/evaluation/argrec-pilot-001-argmap.json)
It never touches the factory registries.

Scores the directive's full metric set; catastrophic = UNSUPPORTED_BRIDGE_RATE + SPEAKER_COLLAPSE.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "source-evidence", "evals", "patala", "tasks"))
from argument_recovery_bench import score_recovery  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
GOLD = os.path.join(ROOT, "data/evaluation/recovery-gold-v1.json")
CAND = os.path.join(ROOT, "data/evaluation/argrec-pilot-001-argmap.json")
OUT = os.path.join(ROOT, "benchmarks/v0/runs/argrec-pilot-001-score.json")


def main() -> int:
    golds = json.load(open(GOLD, encoding="utf-8"))["cases"]
    gold = next((c for c in golds if c["case_id"] == "ipvv:V2L"), None)
    if not gold:
        print("ERROR: ipvv:V2L gold not found")
        return 1
    if not os.path.exists(CAND):
        print("STATUS: pilot ARGMAP candidate not generated yet — run pipeline/run_argrec_pilot_argmap.py")
        return 2

    cand = json.load(open(CAND, encoding="utf-8"))
    am = cand["argument_map"]
    cand_view = {"argument_steps": am.get("argument_steps", []),
                 "decision_for_l2": am.get("decision_for_l2", ""),
                 "open_items": am.get("open_items", [])}
    r = score_recovery(gold, cand_view)
    print(f"IPVV-ARGREC-PILOT-001 blind recovery score (vs frozen V2L gold):")
    print(f"  {r['case_id']}")
    for k, v in r.items():
        if k != "case_id":
            print(f"    {k}: {v}")
    cat = []
    if r["unsupported_bridge_rate"] > 0:
        cat.append("UNSUPPORTED_BRIDGE")
    if r["speaker_accuracy"] < 0.5:
        cat.append("SPEAKER_COLLAPSE")
    print(f"  catastrophic: {cat if cat else 'none'}")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"metrics": r, "catastrophic": cat, "candidate": cand}, f, indent=2, ensure_ascii=False)
    print(f"  wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
