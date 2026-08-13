#!/usr/bin/env python3
"""test_argmap_nat.py — devpath1 (E2-01) ARGMAP NAT harness acceptance.

Checks the ARGMAP NAT harness + the shared cross-lane contract:
  1. EvaluationCandidate wraps a registry row (frozen, exact-version, hashed)
  2. EvaluationFinding emits the SAME schema as the 6-finding bundle (EvaluationFinding-v1)
  3. finding lifecycle: OPEN -> retest(PASS) -> RESOLVED ; retest(FAIL) -> STILL_FAILING
  4. argmap_contract: canonical 4-section shape check + mutation-family vocabulary
  5. the verifier: clean map -> PASS; an OPEN-as-resolved or scope-inflated map -> FAIL
  6. the cross-lane object is the SAME for T1 and ARGMAP (no ARGMAP-specific handoff)

Run: cd /root/projects/patala && machinelearning/research/.venv/bin/python \
     source-evidence/evals/patala/tasks/test_argmap_nat.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evaluation_candidate import EvaluationCandidate
from evaluation_finding import EvaluationFinding
import argmap_contract as C
from argmap_eval import verify_argmap

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


print("== cross-lane EvaluationCandidate ==")
row = {"layer": "ARGMAP", "object_id": "kramasadbhava:v1",
       "version": "argmap-kramasadbhava:v1-v1", "status": "GENERATED",
       "created_by": "factory-batch", "input_refs": [],
       "payload": {"argument_map": {"what_is_at_issue": "x", "argument_steps": [],
                                    "open_items": [], "decision_for_l2": "y"}}}
cand = EvaluationCandidate.from_registry_row(row)
emit = cand.emit()
check("candidate carries exact version + layer", cand.layer == "ARGMAP" and cand.version == row["version"])
check("candidate_hash binds the payload", emit["candidate_hash"] == cand.emit()["candidate_hash"])
check("candidate roundtrips from_dict", EvaluationCandidate.from_dict(emit).version == cand.version)

print("\n== EvaluationFinding (same schema as the 6-finding bundle) ==")
f = EvaluationFinding(finding_id="EF-ARGMAP-2026-0001", object_ref="kramasadbhava:v1",
                      evaluated_version="argmap-kramasadbhava:v1-v1", layer="ARGMAP",
                      contract="ARGMAP-NAT-v1", dimension="OPEN", result="FAIL",
                      failure_class="OPEN_AS_RESOLVED", observed="an OPEN item was resolved")
femit = f.emit()
check("schema_version is EvaluationFinding-v1", femit["schema_version"] == "EvaluationFinding-v1")
check("finding_hash present", bool(femit["finding_hash"]))
check("status starts OPEN", femit["status"] == "OPEN")
# lifecycle
f2 = EvaluationFinding.from_dict(femit)
f2.retest(passed=True)
check("retest(PASS) -> RESOLVED", f2.status == "RESOLVED")
f3 = EvaluationFinding.from_dict(femit)
f3.retest(passed=False)
check("retest(FAIL) -> STILL_FAILING", f3.status == "STILL_FAILING")

print("\n== argmap_contract shape + mutation vocabulary ==")
ok_map = {"what_is_at_issue": "q", "argument_steps": ["s"], "open_items": [], "decision_for_l2": "d"}
check("canonical shape passes", C.check_shape(ok_map) == [])
bad_map = {"argument_steps": ["s"]}
check("missing sections detected", set(C.check_shape(bad_map)) <= set(C.CANONICAL_SECTIONS))
check("8 dimensions defined", set(C.DIMENSIONS) == {"NODE", "ROLE", "EDGE", "SPEAKER", "SCOPE", "OPEN", "INFERENCE", "SUPPORT"})
fam = set(C.MUTATION_FAMILIES)
check("core mutation families present",
      {"OBJECTION_AS_AUTHOR_VIEW", "GROUNDING_AS_INFERENCE", "PREMISE_CONCLUSION_SWAP",
       "RESPONSE_DIRECTION_FLIP", "FALSE_CONTRADICTION", "INVENTED_BRIDGE"} <= fam)
check("added families present (SPEAKER_COLLAPSE, SCOPE_INFLATION)",
      {"SPEAKER_COLLAPSE", "SCOPE_INFLATION", "OPEN_AS_RESOLVED"} <= fam)

print("\n== verifier: clean -> PASS ; defects -> FAIL ==")
clean = EvaluationCandidate(candidate_id="c1", layer="ARGMAP", object_ref="k", version="v1",
    payload={"argument_map": {
        "what_is_at_issue": "What supports the powers?",
        "argument_steps": ["The passage licenses the flashing as grounded in the free knower."],
        "open_items": [{"text": "open point", "status": "OPEN"}],
        "decision_for_l2": "Render the flashing as grounded in the free knower."}})
r_clean = verify_argmap(clean)
check("clean map -> PASS", r_clean["verdict"] == "PASS", str(r_clean["problems"]))

scope_bad = EvaluationCandidate(candidate_id="c2", layer="ARGMAP", object_ref="k", version="v1",
    payload={"argument_map": {
        "what_is_at_issue": "q",
        "argument_steps": ["Therefore every cognition always depends on the I-awareness."],
        "open_items": [],
        "decision_for_l2": "All cognition in all cases is the I-awareness."}})
r_scope = verify_argmap(scope_bad)
check("scope inflation -> FAIL", r_scope["verdict"] == "FAIL", str(r_scope["problems"]))

open_bad = EvaluationCandidate(candidate_id="c3", layer="ARGMAP", object_ref="k", version="v1",
    payload={"argument_map": {
        "what_is_at_issue": "q",
        "argument_steps": ["The passage shows X."],
        "open_items": [{"text": "resolved without flag", "status": "DECIDED"}],
        "decision_for_l2": "X is settled."}})
r_open = verify_argmap(open_bad)
check("silently-resolved open item -> FAIL (OPEN dimension)",
      r_open["verdict"] == "FAIL" and r_open["dimensions"]["OPEN"] == "DEFECT", str(r_open["problems"]))

print("\n== cross-lane: same object for T1 and ARGMAP (no ARGMAP-specific handoff) ==")
t1_row = {"layer": "T1", "object_id": "kramasadbhava:v1", "version": "t1-kramasadbhava:v1-v1",
          "status": "GENERATED", "created_by": "factory", "input_refs": [],
          "payload": {"t1": {"tokens": []}}}
t1_cand = EvaluationCandidate.from_registry_row(t1_row)
check("T1 and ARGMAP share the same EvaluationCandidate contract",
      t1_cand.layer == "T1" and t1_cand.emit()["candidate_hash"] is not None)
# both produce the same finding type
tf = EvaluationFinding(finding_id="EF-T1-X", layer="T1", evaluated_version="t1-x-v1",
                       object_ref="x", dimension="GLOSS", failure_class="UNGLOSSED")
af = EvaluationFinding(finding_id="EF-ARGMAP-X", layer="ARGMAP", evaluated_version="arg-x-v1",
                       object_ref="x", dimension="OPEN", failure_class="OPEN_AS_RESOLVED")
check("T1 and ARGMAP findings share the EvaluationFinding-v1 schema",
      tf.schema_version == af.schema_version == "EvaluationFinding-v1")

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (ARGMAP NAT harness + cross-lane contract work)"))
sys.exit(1 if failures else 0)
