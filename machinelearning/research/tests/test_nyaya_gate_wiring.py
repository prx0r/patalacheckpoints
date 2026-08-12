#!/usr/bin/env python3
"""test_nyaya_gate_wiring.py — the Nyāya gate wired into the argument layer + graph-aware viruddha.

Per WIRE-NYAYA-GATE.md (now valid: real Inference objects exist after the CP4 IR gate crossed):

1. build_argument fills its empty gate slot by running the real gate on the conclusion.
2. check_viruddha_graph is a GRAPH operation: it detects when a candidate claim contradicts an
   established gold proposition (the text argues the opposite), replacing the keyword heuristic.
3. No false positives on agreeing / unrelated claims.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from patala_ml.argument import build_argument, NyayaMember
from patala_ml.gold002 import build_gold_002
from patala_ml.nyayagate import check_viruddha_graph, validate

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


print("== the gate fills the empty ArgumentProposal.gate slot ==")
arg = build_argument(
    "pt:argument:ipvv:arg-test", "ipvv", "Test argument", "ENTAILMENT",
    members=[NyayaMember(role="PRATIJNA", text="The I-grasp is not a construction."),
             NyayaMember(role="HETU", text="It is not any of the three kinds of construction."),
             NyayaMember(role="UDAHARANA", text="Joining, multiplying, splitting."),
             NyayaMember(role="UPANAYA", text="The I-grasp is none of these."),
             NyayaMember(role="NIGAMANA", text="The I-grasp is not a construction.")],
)
check("argument.gate is now populated (not the empty slot)",
      arg.gate is not None and arg.gate.get("outcome") in ("accepted", "accepted_with_penalty", "needs_review", "hollow"),
      str(arg.gate))

print("\n== graph-aware viruddha: a contradicting claim is flagged against a real gold ==")
g = build_gold_002()
contradicting = {"claim_id": "c:contra",
                 "claim_text": "The I-reflexive-awareness IS a conceptual construction because it is linguistically expressed",
                 "pramana": "anumana"}
fails = check_viruddha_graph(contradicting, g["nodes"])
check("contradicting claim flagged as viruddha (GRAPH operation)", len(fails) == 1,
      str([f.rationale for f in fails]))

# via the validate wrapper, outcome must downgrade to needs_review (no posterior update)
res = validate(contradicting, gold_propositions=g["nodes"])
check("validate() downgrades a graph-viruddha to needs_review + blocks posterior",
      res.get("graph_viruddha") is True and res.get("can_update_posterior") is False
      and res.get("outcome") == "needs_review", str(res.get("outcome")))

print("\n== no false positives on agreeing / unrelated claims ==")
agreeing = {"claim_id": "c:ok",
            "claim_text": "The I-reflexive-awareness is NOT a conceptual construction, though linguistically expressed"}
unrelated = {"claim_id": "c:un", "claim_text": "Consciousness creates the world through freedom"}
check("agreeing claim not flagged", len(check_viruddha_graph(agreeing, g["nodes"])) == 0)
check("unrelated claim not flagged", len(check_viruddha_graph(unrelated, g["nodes"])) == 0)

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (Nyāya gate wired + viruddha-as-graph works)"))
sys.exit(1 if failures else 0)
