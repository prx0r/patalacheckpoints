#!/usr/bin/env python3
"""pipeline/finalize_argrec_pilot.py — turn hermes raw output into the pilot ARGMAP + score it blind.

After `hermes -z <prompt>` writes /tmp/opencode/argmap_out.json, this:
  1. parses the model's JSON into the canonical ARGMAP candidate
  2. saves it as data/evaluation/argrec-pilot-001-argmap.json
  3. runs the blind ARGUMENT-RECOVERY score vs the frozen V2L gold (offline, no factory)

Usage:
    python3 pipeline/finalize_argrec_pilot.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, "/root/projects/patala/pipeline")
sys.path.insert(0, "/root/projects/patala/source-evidence/evals/patala/tasks")

from argument_recovery_bench import score_recovery  # noqa: E402

RAW = "/tmp/opencode/argmap_out.json"
CAND_OUT = "/root/projects/patala/data/evaluation/argrec-pilot-001-argmap.json"
SCORE_OUT = "/root/projects/patala/benchmarks/v0/runs/argrec-pilot-001-score.json"
GOLD = "/root/projects/patala/data/evaluation/recovery-gold-v1.json"


def parse(raw: str) -> dict:
    raw = (raw or "").strip()
    # hermes may wrap in fences or add prose; extract the JSON object
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0]
    s, e = raw.find("{"), raw.rfind("}")
    if s < 0 or e <= s:
        raise ValueError("no JSON in hermes output")
    return json.loads(raw[s:e + 1])


def main() -> int:
    if not os.path.exists(RAW):
        print("STATUS: hermes output not ready yet")
        return 2
    raw = open(RAW, encoding="utf-8").read()
    if not raw.strip():
        print("STATUS: hermes output empty (still running or failed)")
        return 2
    body = parse(raw)
    cand = {
        "pilot_id": "IPVV-ARGREC-PILOT-001",
        "window": ["k1", "k2", "k3", "k4", "k5"],
        "argument_map": {
            "what_is_at_issue": (body.get("what_is_at_issue") or "").strip(),
            "argument_steps": [s for s in (body.get("argument_steps") or []) if isinstance(s, str) and s.strip()],
            "open_items": body.get("open_items") or [],
            "decision_for_l2": (body.get("decision_for_l2") or "").strip(),
        },
        "inputs": {"T1": "chunkV2-L...apohana.md", "L0": "chunkV2-L...l0.jsonl", "C1": "c1_V2L-nonconstructed-I.md"},
        "model": "deepseek-v4-flash",
        "no_gold_leakage": True,
        "status": "MACHINE_PROPOSED",
    }
    os.makedirs(os.path.dirname(CAND_OUT), exist_ok=True)
    with open(CAND_OUT, "w", encoding="utf-8") as f:
        json.dump(cand, f, indent=2, ensure_ascii=False)

    # blind score vs frozen gold
    golds = json.load(open(GOLD, encoding="utf-8"))["cases"]
    gold = next((c for c in golds if c["case_id"] == "ipvv:V2L"), None)
    if not gold:
        print("ERROR: V2L gold missing")
        return 1
    cand_view = {"argument_steps": cand["argument_map"]["argument_steps"],
                 "decision_for_l2": cand["argument_map"]["decision_for_l2"],
                 "open_items": cand["argument_map"]["open_items"]}
    r = score_recovery(gold, cand_view)
    cat = []
    if r["unsupported_bridge_rate"] > 0:
        cat.append("UNSUPPORTED_BRIDGE")
    if r["speaker_accuracy"] < 0.5:
        cat.append("SPEAKER_COLLAPSE")
    with open(SCORE_OUT, "w", encoding="utf-8") as f:
        json.dump({"metrics": r, "catastrophic": cat, "candidate": cand}, f, indent=2, ensure_ascii=False)

    print(f"IPVV-ARGREC-PILOT-001 (blind, vs frozen V2L gold):")
    for k, v in r.items():
        if k != "case_id":
            print(f"  {k}: {v}")
    print(f"  catastrophic: {cat if cat else 'none'}")
    print(f"  steps recovered: {len(cand['argument_map']['argument_steps'])}")
    for s in cand["argument_map"]["argument_steps"]:
        print(f"    - {s[:100]}")
    print(f"  wrote {CAND_OUT} + {SCORE_OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
