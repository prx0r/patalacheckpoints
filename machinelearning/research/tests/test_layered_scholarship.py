#!/usr/bin/env python3
"""test_layered_scholarship.py — the layered scholarship object (devpath13 / user's framing).

Checks (the user's insight: hard data vs loose essay interpretation, multiple layers):
  1. five layers exist: SOURCE / LOGICAL / SYNTHESIS / ESSAY / EDUCATION
  2. INTERPRETATION != EVIDENCE is enforced
  3. an OPEN logical crux must stay OPEN upward (not silently resolved in synthesis/essay)
  4. the essay must carry labelled interpretation_claims (speculation not smuggled as evidence)
  5. layer relations are explicit (GROUNDS / BRIDGES / INTERPRETS / PROJECTS)
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from patala_ml.layered_scholarship import make_layered_object, audit_layer_honesty, LAYERS

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


def honest():
    return make_layered_object(
        object_id="V",
        source={"text": "..."},
        logical={"cruxes": [{"id": "C", "status": "OPEN"}]},
        synthesis={"cruxes": [{"id": "C", "status": "OPEN"}]},
        essay={"thesis": "x", "derived_claims": ["d"], "interpretation_claims": ["some read X as Y"]},
        education={"skills": ["IDENTIFY_CRUX"]})

def dishonest():
    return make_layered_object(
        object_id="B",
        source={"text": "..."},
        logical={"cruxes": [{"id": "C", "status": "OPEN"}]},
        essay={"thesis": "the text proves the universal Self", "derived_claims": ["proved"]})

print("== 1. five layers ==")
h = honest()
check("all 5 layers present", all(l in h["layers"] for l in LAYERS))

print("\n== 2. INTERPRETATION != EVIDENCE enforced ==")
check("honest object passes the law", audit_layer_honesty(honest())["ok"] is True)
check("dishonest object fails the law", audit_layer_honesty(dishonest())["ok"] is False)

print("\n== 3. open crux preserved upward ==")
findings = audit_layer_honesty(dishonest())["findings"]
check("open crux collapse detected", any("LOGICAL_OPEN_COLLAPSED" in f for f in findings))

print("\n== 4. essay interpretation layer required ==")
check("missing interpretation layer detected", any("ESSAY_NO_INTERPRETATION_LAYER" in f for f in findings))

print("\n== 5. explicit layer relations ==")
rels = honest()["layer_relations"]
check("relations map each layer to the one below", set(rels.values()) == {"GROUNDS", "BRIDGES", "INTERPRETS", "PROJECTS"},
      str(rels))

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (layered scholarship works)"))
sys.exit(1 if failures else 0)
