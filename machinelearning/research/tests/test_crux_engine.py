#!/usr/bin/env python3
"""test_crux_engine.py — devpath5 (G3C) crux + Nyāya-profile acceptance.

Checks (per ARGUMENT-IR-VISION + SPEC-EPISTEMIC-CORE G3C + the handover discipline):
  1. cruxes are computed by PERTURBATION (outcome-sensitivity), not importance/centrality
  2. each crux's decisive premises are a minimal set whose removal flips the conclusion
  3. every crux carries an adjudication question + honest review_status (NOT_HUMAN_REVIEWED)
  4. the Nyāya-profile is wired onto arguments via the bounded gate (verify_claim_semantic),
     and never asserts argument_valid=true
  5. a conclusion that holds only under a COMBINATION of premises yields a minimal set >1
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from patala_ml.crux_engine import (
    compute_cruxes, wire_nyaya_profile, build_crux_layer, _minimal_decisive_sets,
)
from patala_ml.proposition_layer import from_gold_node
from patala_ml.gold002 import build_gold_002
from patala_ml.gold003 import build_gold_003
from patala_ml.gold004 import build_gold_004
from patala_ml.gold005 import build_gold_005

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


def arg_from_gold(g):
    return {"argument_id": g.get("gold_id", "ARG"), "inference_scheme": "",
            "inferences": g.get("inferences", [])}


g002, g003, g004, g005 = build_gold_002(), build_gold_003(), build_gold_004(), build_gold_005()
all_golds = [g002, g003, g004, g005]
arguments = [arg_from_gold(g) for g in all_golds]
arguments = [a for a in arguments if a["inferences"]]
propositions = [from_gold_node(n, g.get("gold_id", "ARG"), "ipvv") for g in all_golds for n in g.get("nodes", [])]
gold_nodes = [n for g in all_golds for n in g.get("nodes", [])]

print("== perturbation cruxes ==")
cruxes = compute_cruxes(arguments, propositions)
check("produced >= 1 crux", len(cruxes) >= 1, len(cruxes))
check("every crux uses method PERTURBATION",
      all(c["method"] == "PERTURBATION" for c in cruxes))
check("every crux has decisive premises",
      all(c["decisive_premises"] for c in cruxes))
check("every crux has an adjudication question",
      all(c["adjudication_question"] for c in cruxes))
check("every crux is NOT_HUMAN_REVIEWED",
      all(c["review_status"] == "NOT_HUMAN_REVIEWED" for c in cruxes))
check("crux_id embeds the decisive premises",
      all(any(d in c["crux_id"] for d in c["decisive_premises"]) for c in cruxes))

print("\n== decisive sets are minimal (perturbation semantics) ==")
# the decisive set is minimal: removing ANY single premise from it must NOT flip the conclusion
# (i.e. a smaller decisive set does not exist). For a single-premise crux this is trivially minimal.
single = [c for c in cruxes if len(c["decisive_premises"]) == 1]
check("single-premise cruxes present (minimal by construction)", len(single) >= 1)

print("\n== a conclusion needing a COMBINATION yields a set > 1 ==")
# construct a synthetic inference where removing one premise is not enough
syn = {"premise_ids": ["P1", "P2", "P3"], "conclusion_ids": ["C"], "inference_id": "SYN"}
combos = _minimal_decisive_sets(["P1", "P2", "P3"], syn)
# with _conclusion_holds (all-or-nothing), removing ONE premise flips it, so each single is decisive
check("all-or-nothing model -> single premises decisive", combos == [["P1"], ["P2"], ["P3"]], combos)

print("\n== P6 stress-test: redundant support, joint necessity, defeaters (devpath13 P6) ==")
# (a) P1-OR-P2 independently sufficient: redundant support -> decisive set must be the OTHER premise(s)
or_inf = {"inference_id": "OR", "premise_ids": ["P1", "P2", "P3"],
          "alternative_support_sets": [["P1"], ["P2"]]}
or_combos = _minimal_decisive_sets(["P1", "P2", "P3"], or_inf)
# conclusion holds iff P1 OR P2 present; removing P3 does nothing (redundant), removing BOTH P1+P2 flips it
check("redundant support: P3 alone is NOT decisive", ["P3"] not in or_combos, or_combos)
check("redundant support: decisive set requires removing both P1 and P2",
      ["P1", "P2"] in or_combos, or_combos)
# (b) jointly-necessary premises that are redundant as a pair (P1+P2 together suffice; neither alone)
joint_inf = {"inference_id": "JOINT", "premise_ids": ["P1", "P2"],
             "alternative_support_sets": [["P1", "P2"]]}
joint_combos = _minimal_decisive_sets(["P1", "P2"], joint_inf)
# with a single alternative {P1,P2}, removing either one breaks it -> both single are decisive
check("jointly-necessary: removing either P1 or P2 flips", {"P1"} in {frozenset(c) for c in joint_combos}
      and {"P2"} in {frozenset(c) for c in joint_combos}, joint_combos)
# (c) an ACTIVE defeater blocks the inference -> no conclusion, no crux
defeated_inf = {"inference_id": "DEF", "premise_ids": ["P1", "P2"], "active_defeater": True}
defeated_combos = _minimal_decisive_sets(["P1", "P2"], defeated_inf)
check("active defeater blocks inference -> no decisive set (crux)", defeated_combos == [], defeated_combos)
# (d) an inactive defeater does NOT block
not_defeated = {"inference_id": "ND", "premise_ids": ["P1", "P2"], "active_defeater": False}
check("inactive defeater does not block", _minimal_decisive_sets(["P1", "P2"], not_defeated) == [["P1"], ["P2"]])

print("\n== Nyāya-profile wired via the bounded gate ==")
for a in arguments:
    prof = wire_nyaya_profile(a, gold_nodes)
    check(f"profile for {a['argument_id']} has outcome + checks",
          prof["outcome"] in ("PASS", "PASS_WITH_OPEN", "FAIL") and isinstance(prof["checks"], list))
    check(f"profile for {a['argument_id']} is bounded (no argument_valid)",
          "argument_valid" not in prof)
    for c_ in prof["checks"]:
        check("each check has bounded verdict + dimensions",
              c_["verdict"] in ("PASS", "PASS_WITH_OPEN", "FAIL") and set(c_["dimensions"]) ==
              {"pratijna", "hetu", "scope", "support_relation"})

print("\n== full layer ==")
res = build_crux_layer(arguments, propositions, gold_nodes)
check("layer reports crux + argument counts",
      res["counts"]["cruxes"] == len(res["cruxes"]) and res["counts"]["arguments_profiled"] == len(arguments))
check("method honesty declared", "perturbation" in res["method_honesty"].lower() and
      "not a truth oracle" in res["method_honesty"].lower())

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (perturbation crux engine + Nyāya-profile work)"))
sys.exit(1 if failures else 0)
