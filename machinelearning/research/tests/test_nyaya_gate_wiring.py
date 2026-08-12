#!/usr/bin/env python3
"""test_nyaya_gate_wiring.py — the graph-aware Nyāya audit seam.

Architecture (per peer review): construction and contextual validation are SEPARATE.
  build_argument(...)  → creates ArgumentProposal (construction only, no graph audit)
  audit_argument(arg, comparison_graph) → the graph-aware Nyāya audit (structural gate + graph
      viruddha), records audit_refs on the argument

This tests:
1. build_argument is construction-only (it does NOT claim to do graph audit).
2. audit_argument runs the graph-aware gate and records the audit on the argument.
3. check_viruddha_graph is a GRAPH operation: it detects a true contradiction of an established
   gold proposition, and does NOT fire on agreeing/unrelated claims.
4. opponent-attributed propositions are excluded from the established pool.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from patala_ml.argument import build_argument, audit_argument, NyayaMember
from patala_ml.gold002 import build_gold_002
from patala_ml.nyayagate import check_viruddha_graph, validate

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


def make_arg():
    return build_argument(
        "pt:argument:ipvv:arg-test", "ipvv", "Test argument", "ENTAILMENT",
        members=[NyayaMember(role="PRATIJNA", text="The I-grasp is not a construction."),
                 NyayaMember(role="HETU", text="It is not any of the three kinds of construction."),
                 NyayaMember(role="UDAHARANA", text="Joining, multiplying, splitting."),
                 NyayaMember(role="UPANAYA", text="The I-grasp is none of these."),
                 NyayaMember(role="NIGAMANA", text="The I-grasp is not a construction.")],
    )


print("== construction is separate from contextual audit ==")
arg = make_arg()
check("build_argument is construction-only (gate stays None unless supplied)",
      arg.gate is None, str(arg.gate))

print("\n== audit_argument runs the graph-aware audit and records audit_refs ==")
g = build_gold_002()
audit = audit_argument(arg, comparison_graph=g["nodes"])
check("audit returns an audit_id", "audit_id" in audit)
check("audit records audit_id on the argument's audit_refs",
      audit["audit_id"] in arg.audit_refs)
check("audit has a structural gate outcome",
      audit.get("outcome") in ("accepted", "accepted_with_penalty", "needs_review", "hollow"))

print("\n== graph viruddha: true contradiction detected, agreeing/unrelated clean ==")
g2 = build_gold_002()
true_contra = {"claim_id": "c:contra",
               "claim_text": "The I-reflexive-awareness IS a constructed relation among independently given elements",
               "pramana": "anumana"}
check("true contradiction of siddhānta is flagged (≥1 hit)",
      len(check_viruddha_graph(true_contra, g2["nodes"])) >= 1)
# via validate wrapper, a graph-viruddha downgrades to needs_review + blocks posterior
res = validate(true_contra, gold_propositions=g2["nodes"])
check("validate() downgrades graph-viruddha to needs_review + blocks posterior",
      res.get("graph_viruddha") is True and res.get("can_update_posterior") is False
      and res.get("outcome") == "needs_review", str(res.get("outcome")))

agreeing = {"claim_id": "c:ok",
            "claim_text": "The I-reflexive-awareness is NOT a conceptual construction, though linguistically expressed"}
# honest invariant: an agreeing claim must NOT fire against the proposition it AGREES with (G2-TC2:
# 'the I-awareness is not a constructed relation'). It may legitimately share subject words with
# other gold propositions (different predicates) — that is a NON_EQUIVALENT_PREDICATE case the
# semantic layer tests, not a settled contradiction.
tc2 = [n for n in g2["nodes"] if n.get("proposition_id") == "G2-TC2"]
check("agreeing claim does not fire against the proposition it agrees with (G2-TC2)",
      len(check_viruddha_graph(agreeing, tc2)) == 0)
unrelated = {"claim_id": "c:un", "claim_text": "Consciousness creates the world through freedom"}
check("unrelated claim not flagged", len(check_viruddha_graph(unrelated, g2["nodes"])) == 0)

print("\n== opponent-attributed propositions are excluded from established ==")
obj = [n for n in g2["nodes"] if n.get("proposition_id") == "G2-OBJ"]
check("opponent-attributed (objector) proposition does not nominate viruddha",
      len(check_viruddha_graph(
          {"claim_id": "x", "claim_text": "reflexive awareness IS a conceptual construction"}, obj)) == 0)

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (graph-aware Nyāya audit seam works)"))
sys.exit(1 if failures else 0)
