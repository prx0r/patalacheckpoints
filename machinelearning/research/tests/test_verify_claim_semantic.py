#!/usr/bin/env python3
"""test_verify_claim_semantic.py — devpath1 (E2-02) bounded evaluator acceptance.

The handover's target: `nyayagate.verify_claim_semantic` is a BOUNDED structural/evaluative gate,
NOT a truth oracle. It outputs PASS / PASS_WITH_OPEN / FAIL with the four dimensions
(pratijna/hetu/scope/support_relation) — and NEVER `argument_valid=true` / "proven".

Checks:
  1. returns a bounded verdict (PASS | PASS_WITH_OPEN | FAIL)
  2. reports all four dimensions (pratijna/hetu/scope/support_relation), each CLEAN|OPEN|DEFECT
  3. never claims truth (no `argument_valid=true`, no "proven" in the output)
  4. a clean, well-formed claim → PASS
  5. a graph viruddha (contradicts an established gold) → FAIL + can_update_posterior False
  6. overreach (universal claim without vyāpti) → scope DEFECT → PASS_WITH_OPEN/FAIL, not PASS
  7. additive: `validate` (the prior entry point) still works unchanged
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from patala_ml.nyayagate import verify_claim_semantic, validate
from patala_ml.gold002 import build_gold_002

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


clean = {"claim_id": "c:clean",
         "claim_text": "The I-awareness is not a conceptual construction of the elements it unifies",
         "falsifier": {"type": "structural"}}

print("== bounded verdict + dimensions ==")
r = verify_claim_semantic(clean)
check("returns a bounded verdict (PASS/PASS_WITH_OPEN/FAIL)", r["verdict"] in ("PASS", "PASS_WITH_OPEN", "FAIL"), r["verdict"])
check("reports the 4 dimensions", set(r["dimensions"]) == {"pratijna", "hetu", "scope", "support_relation"}, str(set(r["dimensions"])))
check("dimension values are CLEAN/OPEN/DEFECT",
      all(v in ("CLEAN", "OPEN", "DEFECT") for v in r["dimensions"].values()))
check("clean claim -> PASS", r["verdict"] == "PASS", r["verdict"])

print("\n== never a truth oracle ==")
check("no argument_valid=true field", "argument_valid" not in r)
check("no 'proven' truth claim in note",
      "proven" not in r["note"].lower() and "true" not in r["note"].lower())
check("can_update_posterior implies bounded PASS only",
      (r["can_update_posterior"] == (r["verdict"] == "PASS")))

print("\n== graph viruddha -> FAIL ==")
g = build_gold_002()
contra = {"claim_id": "c:contra", "claim_text": "The I-awareness IS a constructed relation among independently given elements",
          "falsifier": {"type": "structural"}}
rv = verify_claim_semantic(contra, gold_propositions=g["nodes"])
check("graph viruddha -> FAIL", rv["verdict"] == "FAIL", rv["verdict"])
check("graph viruddha blocks posterior", rv["can_update_posterior"] is False)
check("graph viruddha flagged", rv["graph_viruddha"] is True)

print("\n== overreach (universal w/o vyāpti) -> not PASS ==")
over = {"claim_id": "c:over", "claim_text": "Every cognition always depends on the I-awareness",
        "falsifier": {"type": "structural"}}
ro = verify_claim_semantic(over)
check("universal overreach -> scope DEFECT", ro["dimensions"]["scope"] == "DEFECT", ro["dimensions"]["scope"])
check("overreach verdict is not PASS", ro["verdict"] != "PASS", ro["verdict"])

print("\n== additive: validate() unchanged ==")
v = validate(clean)
check("validate() still returns dict with outcome", v["outcome"] in ("accepted", "accepted_with_penalty", "needs_review", "hollow", "refuted"))

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (bounded verify_claim_semantic works)"))
sys.exit(1 if failures else 0)
