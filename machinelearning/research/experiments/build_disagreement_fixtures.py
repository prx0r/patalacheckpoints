#!/usr/bin/env python3
"""build_disagreement_fixtures.py — turn real cross-gold viruddha findings into T3/T4 fixtures.

The graph-aware viruddha (nyayagate.check_viruddha_graph) surfaces genuine disagreement cases between
established gold propositions. These are MORE valuable than green corroboration boxes: they are the
benchmark fixtures where the correct answer may be "this passage has two defensible historically
grounded readings; a competent system must represent the disagreement and abstain from false certainty."

We convert each cross-gold finding into a PATALA-EVIDENCE claim_to_counterevidence fixture:
  input  {claim: <the gold proposition>, target_gold: <the opposing gold>}
  expected {counterevidence: [<the opposing proposition>], relation: "RIVAL_READING" | "CONTRADICTS"}

These are CANDIDATE (machine-discovered disagreements, NOT adjudicated). A human/scholar validates them.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from patala_ml.gold import build_gold_v0
from patala_ml.gold002 import build_gold_002
from patala_ml.gold003 import build_gold_003
from patala_ml.gold004 import build_gold_004
from patala_ml.gold005 import build_gold_005
from patala_ml.nyayagate import check_viruddha_graph

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))

GOLDS = {"ARG-GOLD-001": build_gold_v0, "ARG-GOLD-002": build_gold_002,
         "ARG-GOLD-003": build_gold_003, "ARG-GOLD-004": build_gold_004,
         "ARG-GOLD-005": build_gold_005}


def txt(n):
    return n.get("proposition") or n.get("text") or ""


def collect_established() -> dict:
    out = {}
    for gid, fn in GOLDS.items():
        for n in fn()["nodes"]:
            comm = str(n.get("commitment") or n.get("speaker") or "").upper()
            if comm in ("ASSERTS", "DERIVES", "SIDDHANTA", "RECONSTRUCTED"):
                out.setdefault(gid, []).append(n)
    return out


def main() -> int:
    established = collect_established()
    findings = []

    for gid, fn in GOLDS.items():
        g = fn()
        for n in g["nodes"]:
            if n.get("kind") != "CONCLUSION":
                continue
            claim = {"claim_id": f"{gid}:{n.get('proposition_id')}",
                     "claim_text": txt(n), "pramana": "anumana"}
            for other_gid, props in established.items():
                if other_gid == gid:
                    continue
                for prop in props:
                    hits = check_viruddha_graph(claim, [prop])
                    if hits:
                        findings.append({
                            "fixture_id": f"EVID-DISAGREE-{len(findings)+1:03d}",
                            "task_family": "PATALA-EVIDENCE",
                            "task": "claim_to_counterevidence",
                            "source_ids": [g.get("passage"), GOLDS[other_gid]().get("passage")],
                            "gold_version": "1",
                            "authoring_method": "MACHINE_PROPOSED",
                            "review_state": "CANDIDATE",
                            "allowed_training_use": False,
                            "split_class": "EVALUATION_ONLY",
                            "input": {
                                "claim": txt(n),
                                "claim_gold": gid,
                                "target_gold": other_gid,
                                "claim_passage": g.get("passage"),
                            },
                            "expected": {
                                "counterevidence": [txt(prop)],
                                "counterevidence_prop": prop.get("proposition_id"),
                                "relation": "RIVAL_READING",
                                "viruddha": True,
                                "note": "machine-discovered disagreement (graph viruddha); adjudicate whether it is a real rival reading or a false positive",
                            },
                        })
                        break  # one counterevidence per finding

    out = os.path.join(ROOT, "benchmarks/v0/evidence/disagreement-fixtures.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"fixtures": findings}, f, indent=2)

    print(f"DISAGREEMENT FIXTURES (machine-discovered, CANDIDATE): {len(findings)}")
    for fx in findings:
        print(f"  {fx['fixture_id']}: {fx['input']['claim_gold']} vs {fx['input']['target_gold']} "
              f"— '{fx['input']['claim'][:50]}...' RIVAL_READING")
    print(f"\nwritten: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
