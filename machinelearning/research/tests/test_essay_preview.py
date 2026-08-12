#!/usr/bin/env python3
"""test_essay_preview.py — the essay depends on the argument layer + gate.

Per the hermes PEER-REVIEW spec §7 (machine pre-review) + §8 (review dossier): an essay is not
disconnected prose. Each load-bearing claim must resolve to a real gold proposition and get a
deterministic gate verdict. This is the 'review dossier' that compresses expert attention.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from patala_ml.gold002 import build_gold_002
from patala_ml.gold004 import build_gold_004

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


print("== the reflexion-core essay's claims depend on the golds + gate ==")
d = json.load(open(os.path.join(ROOT, "benchmarks/v0/review/REFLEXION-CORE-ESSAY-PREVIEW.json")))
dossier = d["review_dossier"]

g2 = build_gold_002(); g4 = build_gold_004()
g2_ids = {n.get("proposition_id") for n in g2["nodes"]}
g4_ids = {n.get("proposition_id") for n in g4["nodes"]}

check("essay has load-bearing claims", len(dossier) >= 3, str(len(dossier)))
for item in dossier:
    g = item["grounded_in"]
    check(f"{item['claim_id']} resolves to a real gold proposition",
          g["proposition_id"] in g2_ids | g4_ids, g["proposition_id"])
    check(f"{item['claim_id']} has a valid gate outcome",
          item["gate_outcome"] in ("accepted", "accepted_with_penalty", "needs_review", "hollow"),
          item["gate_outcome"])
check("every claim resolves to ARG-002 or ARG-004",
      all(i["grounded_in"]["argument_id"] in ("ARG-GOLD-002", "ARG-GOLD-004") for i in dossier))
check("the dossier is machine pre-review, NOT scholarly validation",
      d["summary"]["note"].startswith("machine pre-review"))

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (essay depends on the golds + gate)"))
sys.exit(1 if failures else 0)
