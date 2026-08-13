#!/usr/bin/env python3
"""experiments/vertical1_essay_audit.py — VERTICAL-1 whole-essay natural audit (devpath13 P8).

The C.1 sentence audit (ESSAY-IPVV-REFLEXION-CORE-001.audit.json) already checks per-sentence
prose-faithfulness. This is the WHOLE-ESSAY audit (A1-CONTINUE-v2 P8) measuring:

    THESIS_WARRANTED       does the evidence warrant the thesis (vs conclusion-strength inflation)?
    ARGUMENT_BALANCE       were relevant rivals/positions represented (not omitted)?
    CRUX_FIDELITY          does the essay focus on the actual dispute/crux?
    CONCLUSION_STRENGTH    does the conclusion exceed what the synthesis supports?
    SOURCE_TRACEABILITY    can load-bearing claims trace back to passages/synthesis?

Honest: this is a STRUCTURAL audit over the frozen essay + its sentence audit + the dossier.
MACHINE_PROPOSED / NOT_HUMAN_REVIEWED.
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
ESSAY_MD = os.path.join(ROOT, "benchmarks/v0/review/ESSAY-IPVV-REFLEXION-CORE-001.md")
ESSAY_AUDIT = os.path.join(ROOT, "benchmarks/v0/review/ESSAY-IPVV-REFLEXION-CORE-001.audit.json")
SYN = os.path.join(ROOT, "benchmarks/v0/review/SYN-IPVV-REFLEXION-CORE-001.json")


def main() -> int:
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    audit = json.load(open(ESSAY_AUDIT, encoding="utf-8"))
    syn = json.load(open(SYN, encoding="utf-8"))
    low = text

    findings = []

    # 1. THESIS_WARRANTED: the conclusion must be qualified, never exceed the synthesis ceiling
    thesis_honest = ("per-act" in low or "does not establish" in low or "boundar" in low)
    # 2. ARGUMENT_BALANCE: a rival/opponent must appear
    rival_present = any(k in low for k in ["buddhist", "opponent", "rival"])
    # 3. CRUX_FIDELITY: the decisive crux (self-luminosity of the establishing act) must appear
    crux_present = any(k in low for k in ["self-luminous", "self-luminous awareness", "prakāśa",
                                          "establish", "inert"])
    # 4. CONCLUSION_STRENGTH: the thesis must not over-claim (no universal-Self conclusion as fact)
    overclaim = any(k in low for k in ["conclusively proves", "definitively establishes",
                                       "therefore the universal self exists"])
    # 5. SOURCE_TRACEABILITY: load-bearing sentences carry claim_refs + source_refs in the audit
    lb = [s for s in audit["sentences"] if s.get("role") == "LOAD_BEARING"]
    traceable = all(s.get("claim_refs") and s.get("source_refs") for s in lb)
    supported = all(s.get("audit", {}).get("claim_supported", False) for s in lb)

    print("== VERTICAL-1 whole-essay audit (devpath13 P8) ==")
    print(f"  essay: {audit.get('essay_id')}  epistemic_ceiling={audit.get('epistemic_ceiling')}")
    print(f"  THESIS_WARRANTED   (per-act/boundary qualification present): {thesis_honest}")
    print(f"  ARGUMENT_BALANCE   (rival/opponent present): {rival_present}")
    print(f"  CRUX_FIDELITY      (self-luminous/establish/inert present): {crux_present}")
    print(f"  CONCLUSION_STRENGTH (no overclaim): {not overclaim}  overclaim={overclaim}")
    print(f"  SOURCE_TRACEABILITY (LB sentences claim+source refs): {traceable}; supported={supported}")

    if not crux_present:
        findings.append("CRUX_FIDELITY_OPEN: the essay does not explicitly foreground the decisive "
                        "adhyavasāya crux (self-luminosity of the establishing act); it uses the "
                        "reflexion-core framing instead. Not a defect, but the crux could be surfaced "
                        "more directly.")

    verdict = (thesis_honest and rival_present and crux_present and not overclaim
               and traceable and supported)
    print(f"\n  VERDICT: {'PASS' if verdict else 'FAIL'}")
    for f in findings:
        print(f"  finding: {f}")

    out = os.path.join(ROOT, "benchmarks/v0/review/VERTICAL-1-ESSAY-AUDIT.json")
    payload = {
        "object_kind": "WHOLE_ESSAY_AUDIT",
        "essay": audit.get("essay_id"),
        "metrics": {
            "THESIS_WARRANTED": thesis_honest,
            "ARGUMENT_BALANCE": rival_present,
            "CRUX_FIDELITY": crux_present,
            "CONCLUSION_STRENGTH": not overclaim,
            "SOURCE_TRACEABILITY": traceable,
            "sentence_claim_supported": supported,
        },
        "findings": findings,
        "verdict": "PASS" if verdict else "FAIL",
        "review_status": "NOT_HUMAN_REVIEWED",
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"  wrote {out}")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
