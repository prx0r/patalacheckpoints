#!/usr/bin/env python3
"""test_argument_synthesis.py — the ArgumentSynthesis value probe.

Proves the ArgumentSynthesis is the missing intellectual layer and does NOT overclaim:

1. The synthesis EXPOSES the unsupported leap: P1 (I-grasp not a construction) + P2 (manifestation
   without vimarsa is inert) do NOT entail "self-experience is intrinsically fundamental". The
   bridge SYN-INF-001 is listed as an unsupported_bridge (MACHINE_RECONSTRUCTED), not settled.
2. Audits are NEVER merged into stronger support: input ceiling MACHINE_PROPOSED -> epistemic_ceiling
   UNRESOLVED (weakest governs), NOT "strongly supported".
3. Themes are metadata only (never used as inference premises).
4. The EO is a PROJECTION of the synthesis (projection_of == synthesis_id), not the canonical schema.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "experiments"))
from check_argument_synthesis import check_synthesis_obj

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


syn_path = os.path.join(ROOT, "benchmarks/v0/review/SYN-IPVV-REFLEXION-CORE-001.json")
check("ArgumentSynthesis exists", os.path.exists(syn_path))
syn = json.load(open(syn_path))

print("== the synthesis is a valid ArgumentSynthesis ==")
r = check_synthesis_obj(syn)
check("synthesis validates", r["ok"], str(r["problems"]))
check("has inputs (ARG-002 + ARG-004)", [i["ref"] for i in syn["inputs"]] == ["ARG-GOLD-002", "ARG-GOLD-004"])

print("\n== THE VALUE PROBE: the unsupported leap is EXPOSED, not hidden ==")
audit = syn["synthesis_audit"]
check("the bridge SYN-INF-001 is listed as unsupported (MACHINE_RECONSTRUCTED, not entailed)",
      "SYN-INF-001" in audit["unsupported_bridges"], str(audit["unsupported_bridges"]))
check("thesis status is MACHINE_RECONSTRUCTED (not asserted as fact)",
      syn["thesis"]["status"] == "MACHINE_RECONSTRUCTED")

print("\n== audits are NEVER merged into stronger support (weakest-governs) ==")
check("input_ceiling is MACHINE_PROPOSED", audit["input_ceiling"] == "MACHINE_PROPOSED")
check("epistemic_ceiling is UNRESOLVED (not 'strongly supported')",
      audit["epistemic_ceiling"] == "UNRESOLVED", audit["epistemic_ceiling"])
check("audit_merge_note explicitly forbids merging", "NOT" in audit.get("audit_merge_note", ""))

print("\n== themes are metadata only (never premises) ==")
premises = [p for i in syn["inferences"] for p in i["premises"]]
check("no theme (cand_*) is used as an inference premise", not any("cand_" in p for p in premises))
check("theme_refs present as metadata", "theme_refs" in syn and len(syn["theme_refs"]) >= 1)

print("\n== the EO is a PROJECTION of the synthesis, not its schema ==")
eo_path = os.path.join(ROOT, "benchmarks/v0/review/EO-IPVV-REFLEXION-CORE.json")
check("EO projection exists", os.path.exists(eo_path))
if os.path.exists(eo_path):
    eo = json.load(open(eo_path))
    check("EO.projection_of == synthesis_id",
          eo.get("projection_of") == syn["synthesis_id"], eo.get("projection_of"))
    check("EO nigamana.status inherits the UNRESOLVED ceiling (structurally_suggestive, not settled)",
          eo["syllogism"]["nigamana"]["status"] == "structurally_suggestive")

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (ArgumentSynthesis exposes the leap, never overclaims)"))
sys.exit(1 if failures else 0)
