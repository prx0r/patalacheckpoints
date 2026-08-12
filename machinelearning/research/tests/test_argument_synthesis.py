#!/usr/bin/env python3
"""test_argument_synthesis.py — the canonical ArgumentSynthesis value probe + provenance validation.

Proves:
1. Dependency state is RESOLVED from actual proposition objects (no hardcoded status map).
2. Structural audit is SEPARATE from epistemic: with no persisted audits, inputs/deps are NOT_AUDITED,
   outcome null, and audit_state=AUDITED is REJECTED (no invented refs).
3. The thesis has a stable proposition_id == conclusion of the bridge (graph-shaped).
4. The bridge separates ORIGIN (RECONSTRUCTED) from EVIDENTIAL support_state (UNRESOLVED).
5. Audits NEVER merged: epistemic ceiling = WEAKEST over LOAD-BEARING only; structural axis separate.
6. Themes are metadata only (never inference premises).
7. The validator resolves inputs against the AUTHORITATIVE gold registry (rejects wrong pairing /
   nonexistent propositions), and rejects a manufactured AUDITED + a ghost thesis + an overclaiming boundary.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "experiments"))
from build_argument_synthesis import build_synthesis, resolve_dependency
from check_argument_synthesis import check_synthesis_obj

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)

syn = build_synthesis()  # no persisted audits -> honest NOT_AUDITED
r = check_synthesis_obj(syn)
check("canonical synthesis validates", r["ok"], str(r["problems"]))

print("\n== 1. dependency state RESOLVED from actual objects (no hardcoded status map) ==")
deps = {d["ref"]: d for d in syn["dependency_state"]["dependencies"]}
check("G2-CONC resolved with provenance + object-derived status",
      "ARG-GOLD-002:G2-CONC" in deps and deps["ARG-GOLD-002:G2-CONC"]["epistemic_status"] == "SCHOLARLY_CORROBORATED_PRELIMINARY",
      deps.get("ARG-GOLD-002:G2-CONC", {}).get("epistemic_status"))
check("G4-CONC is MACHINE_PROPOSED (per-proposition, not averaged)",
      deps["ARG-GOLD-004:G4-CONC"]["epistemic_status"] == "MACHINE_PROPOSED")

print("\n== 2. structural audit is SEPARATE from epistemic; NOT_AUDITED with no invented outcome ==")
for inp in syn["inputs"]:
    check(f"{inp['argument_ref']} structural_audit.state=NOT_AUDITED, outcome null",
          inp["structural_audit"]["state"] == "NOT_AUDITED"
          and inp["structural_audit"]["outcome"] is None
          and inp["structural_audit"]["audit_refs"] == [],
          str(inp["structural_audit"]))
audit = syn["synthesis_audit"]
check("structural_audit_state == INCOMPLETE (separate axis from epistemic_ceiling)",
      audit["structural_audit_state"] == "INCOMPLETE", audit["structural_audit_state"])
check("internal_consistency == NOT_EVALUATED (not a hardcoded STRUCTURALLY_COHERENT)",
      audit["internal_consistency"] == "NOT_EVALUATED", audit["internal_consistency"])

print("\n== 3. thesis has a stable proposition_id == bridge conclusion (graph-shaped) ==")
check("thesis.proposition_id == SYN-CONC-001 == conclusion of SYN-INF-001",
      syn["thesis"]["proposition_id"] == syn["inferences"][0]["conclusion"] == "SYN-CONC-001")

print("\n== 4. bridge ORIGIN separated from EVIDENTIAL state ==")
b = syn["inferences"][0]
check("origin == RECONSTRUCTED", b["origin"] == "RECONSTRUCTED")
check("support_state == UNRESOLVED", b["support_state"] == "UNRESOLVED")
check("no hardcoded 'unsupported_bridges' — evidential state in assessment", "unsupported_bridges" not in audit)

print("\n== 5. audits NEVER merged: ceiling = weakest over LOAD-BEARING only ==")
check("epistemic_ceiling == UNRESOLVED", audit["epistemic_ceiling"] == "UNRESOLVED", audit["epistemic_ceiling"])
check("load-bearing basis listed", {d["ref"] for d in deps.values() if d["role"].startswith("LOAD_BEARING")}
      == {"ARG-GOLD-002:G2-CONC", "ARG-GOLD-004:G4-CONC", "SYN-INF-001"})

print("\n== 6. themes are metadata only ==")
premises = [p for i in syn["inferences"] for p in i["premises"]]
check("no theme (cand_*) is a premise", not any("cand_" in p for p in premises))
check("theme_refs present as metadata", len(syn.get("theme_refs", [])) >= 1)

print("\n== 7. boundary uses reconstruct vocabulary, not overclaiming 'establishes' ==")
check("boundary has currently_supports (not establishes)",
      "currently_supports" in syn["boundary"] and "establishes" not in syn["boundary"])
check("currently_supports carries UNRESOLVED_RECONSTRUCTION status",
      syn["boundary"]["currently_supports"][0]["status"] == "UNRESOLVED_RECONSTRUCTION")
check("does_not_establish keeps the universalization as a boundary, not a claim",
      any("universal Self" in s for s in syn["boundary"]["does_not_establish"]))

print("\n== NEGATIVE TESTS (validator resolves against the AUTHORITATIVE registry) ==")

def mutate(fn):
    return json.loads(json.dumps(fn()))

# wrong argument/proposition pairing: G2-CONC declared under ARG-GOLD-004
bad = mutate(build_synthesis)
bad["inputs"][1]["proposition_refs"] = ["G2-CONC"]
check("wrong argument/proposition pairing is REJECTED", not check_synthesis_obj(bad)["ok"])

# nonexistent input proposition
bad = mutate(build_synthesis)
bad["inputs"][0]["proposition_refs"] = ["G2-CONC", "NONEXISTENT_PROP"]
check("nonexistent input proposition is REJECTED", not check_synthesis_obj(bad)["ok"])

# manufactured AUDITED audit with no persisted registry
bad = mutate(build_synthesis)
bad["inputs"][0]["structural_audit"] = {"state": "AUDITED", "outcome": "accepted",
                                        "audit_refs": ["totally-made-up-audit-123"]}
check("fake AUDITED audit_ref is REJECTED", not check_synthesis_obj(bad)["ok"])

# structural outcome manufactured while structural_audit_state != COMPLETE
bad = mutate(build_synthesis)
bad["dependency_state"]["dependencies"][0]["structural_audit"]["outcome"] = "accepted"
check("manufactured structural outcome (state INCOMPLETE) is REJECTED", not check_synthesis_obj(bad)["ok"])

# premise that does not resolve
bad = mutate(build_synthesis)
bad["inferences"][0]["premises"] = ["G2-CONC", "NONEXISTENT_PROP"]
check("unresolvable premise is REJECTED", not check_synthesis_obj(bad)["ok"])

# thesis not produced by any inference
bad = mutate(build_synthesis)
bad["thesis"]["proposition_id"] = "SYN-GHOST"
check("thesis with no incoming inference is REJECTED", not check_synthesis_obj(bad)["ok"])

# overclaiming boundary + STRUCTURALLY_COHERENT
bad = mutate(build_synthesis)
bad["boundary"]["establishes"] = ["reflexivity is proven"]
bad["synthesis_audit"]["internal_consistency"] = "STRUCTURALLY_COHERENT"
check("overclaiming boundary + STRUCTURALLY_COHERENT is REJECTED", not check_synthesis_obj(bad)["ok"])

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (canonical ArgumentSynthesis + provenance validator verified)"))
sys.exit(1 if failures else 0)
