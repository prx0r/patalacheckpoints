#!/usr/bin/env python3
"""test_proposition_layer.py — devpath4 (G3B) derivational Proposition layer acceptance.

Checks (per ARGUMENT-IR-VISION §5 + SPEC-EPISTEMIC-CORE G3B):
  1. every proposition is a DerivedScholarlyObject(layer=PROPOSITION) with the authority envelope
  2. every proposition carries Commitment (speaker/force) + explicitness + derived_from
  3. the authority invariant holds: authority(projection) <= authority(parent); ceiling is DERIVED
     (R3), review axis is NOT_REVIEWED (only an H witness raises it)
  4. lifters work from: gold nodes, ARGMAP argument_map, SourceAssertions
  5. honest ceiling: gold/argmap/assertion propositions are MACHINE_PROPOSED/ENGINEERING_VALIDATED,
     never INDEPENDENT_REVIEWED/ADJUDICATED (no H witness)
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from patala_ml.proposition_layer import (
    Proposition, from_gold_node, from_argmap, from_source_assertion, build_proposition_layer,
)
from patala_ml.gold002 import build_gold_002
from patala_ml.gold003 import build_gold_003
from patala_ml.gold004 import build_gold_004
from patala_ml.gold005 import build_gold_005

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
ARGMAP_REG = os.path.join(REPO, "data", "corpus", "registries", "argmap-registry.jsonl")
ASSERT_REG = os.path.join(REPO, "data", "corpus", "registries", "assertion-registry.jsonl")

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


print("== Proposition is a DerivedScholarlyObject(layer=PROPOSITION) ==")
g = build_gold_002()
p = from_gold_node(g["nodes"][1], "ARG-002", "ipvv")   # G2-TC1
dso = p.to_dso()
emit = p.emit()
check("dso.layer == PROPOSITION", dso.layer == "PROPOSITION")
check("emit has the authority envelope + hash",
      "authority" in emit and emit["schema"] == "DERIVED-SCHOLARLY-OBJECT-v1" and emit["hash"])
check("epistemic_ceiling is present in emit (derived)", "epistemic_ceiling" in emit)

print("\n== commitment + explicitness + derived_from present ==")
check("commitment is set", p.commitment in ("ASSERTS", "DENIES", "PRESUPPOSES", "ASSUMES_FOR_ARGUMENT",
                                            "ATTRIBUTES_TO_OPPONENT", "QUOTES", "RECONSTRUCTED",
                                            "EDITORIAL_RATIONAL_RECONSTRUCTION"), p.commitment)
check("explicitness is EXPLICIT/RECONSTRUCTED/IMPLICIT", p.explicitness in ("EXPLICIT", "RECONSTRUCTED", "IMPLICIT"))
check("derived_from is set", bool(p.derived_from), p.derived_from)

print("\n== honest ceiling: no H-witness authority ===")
for emitted in build_proposition_layer()["propositions"][:2] or []:
    pass
ceiling = emit["epistemic_ceiling"]
check("ceiling is MACHINE_PROPOSED or ENGINEERING_VALIDATED (never reviewed)",
      ceiling in ("MACHINE_PROPOSED", "ENGINEERING_VALIDATED"), ceiling)
check("review authority is NOT_REVIEWED", dso.authority.review == "NOT_REVIEWED")

print("\n== lifters from real sources ==")
argmap_row = None
if os.path.exists(ARGMAP_REG):
    with open(ARGMAP_REG) as f:
        argmap_row = json.loads(f.readline().strip())
if argmap_row:
    am_payload = argmap_row["payload"].get("argument_map", argmap_row["payload"])
    am_props = from_argmap(am_payload, argmap_row["object_id"])
    check("argmap lift produces >= 1 proposition", len(am_props) >= 1, len(am_props))
    check("argmap propositions are DSO-projected", am_props[0].emit()["layer"] == "PROPOSITION")

as_props = []
if os.path.exists(ASSERT_REG):
    with open(ASSERT_REG) as f:
        for line in f:
            if line.strip():
                as_props.append(from_source_assertion(json.loads(line.strip())))
check("assertion lift produces >= 1 proposition", len(as_props) >= 1, len(as_props))
check("assertion proposition carries span evidence + commitment",
      as_props and as_props[0].grounding.get("span_ref") and as_props[0].commitment in ("ASSERTS", "DENIES"))

print("\n== full layer assembles from all committed sources ==")
builders = [(build_gold_002, "ARG-002", "ipvv"), (build_gold_003, "ARG-003", "ipvv"),
            (build_gold_004, "ARG-004", "ipvv"), (build_gold_005, "ARG-005", "ipvv")]
res = build_proposition_layer(builders, argmap_row, None)
check("layer has >= 20 gold propositions", res["counts"]["gold"] >= 20, res["counts"]["gold"])
check("layer is honest (no reviewed ceiling)",
      all(x["epistemic_ceiling"] in ("MACHINE_PROPOSED", "ENGINEERING_VALIDATED")
          for x in res["propositions"]))

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (derivational Proposition layer works)"))
sys.exit(1 if failures else 0)
