#!/usr/bin/env python3
"""experiments/vertical1_synthesis_natural.py — VERTICAL-1 SYNTHESIS-NAT-NATURAL (devpath13 P7).

The mutation suite (synthesis_nat.py) proves the evaluator catches designed corruptions. This is the
NATURAL counterpart (A1-CONTINUE-v2 P14): audit the REAL ArgumentSynthesis for the VERTICAL-1 debate
(SYN-IPVV-REFLEXION-CORE-001) against the frozen dossier's expected structure, measuring the P7
metrics directly on real material.

Catastrophic metrics (must be ~0):
    RIVAL_AS_CONSENSUS   the Buddhist rival is preserved as a position, never folded into consensus
    OPEN_AS_RESOLVED      open questions / cruxes stay open, never silently resolved

Other P7 metrics:
    POSITION_RECOVERY     does the synthesis recover the two positions (Śaiva, Buddhist)?
    ARGUMENT_COVERAGE     are the load-bearing arguments present?
    CRUX_RECALL           is the decisive crux (self-luminosity of establishing) present?
    SCOPE_FIDELITY        are the 'does not establish' boundaries honest (no universal overreach)?
    COUNTEREVIDENCE_RECALL  is the Buddhist objection (O3 fire-wood) preserved as counterevidence?

This is a STRUCTURAL audit (present/absent of load-bearing markers), MACHINE_PROPOSED / NOT_HUMAN_REVIEWED.
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
SYN = os.path.join(ROOT, "benchmarks/v0/review/SYN-IPVV-REFLEXION-CORE-001.json")


def load():
    with open(SYN, encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    syn = load()
    blob = json.dumps(syn, ensure_ascii=False).lower()

    # 1. CATASTROPHIC: RIVAL_AS_CONSENSUS / OPEN_AS_RESOLVED
    consensus_markers = ["buddhist agrees", "both accept", "no disagreement",
                         "consensus", "both sides agree", "settled", "conclusive"]
    consensus_hits = [m for m in consensus_markers if m in blob]
    open_resolved = ["resolved beyond", "definitively settles", "no longer open", "conclusively resolved"]
    open_hits = [m for m in open_resolved if m in blob]

    # 2. POSITION_RECOVERY: rival position present
    rival_present = any(k in blob for k in ["buddhist", "opponent", "determination",
                                            "adhyavasāya", "adhyavasaya", "external"])
    saiva_present = any(k in blob for k in ["reflexiv", "vimarśa", "vimarsa", "self-luminous",
                                            "prakāśa", "prakasa", "self-experience"])

    # 3. ARGUMENT_COVERAGE + CRUX_RECALL
    crux_present = any(k in blob for k in ["crux", "self-luminous", "inert", "establish"])
    argument_markers = ["argument", "inference", "premise", "warrant", "position"]
    argument_hits = [m for m in argument_markers if m in blob]

    # 4. SCOPE_FIDELITY: an honest 'does not establish' boundary (no universal overreach)
    boundary = syn.get("boundary", {})
    does_not = boundary.get("does_not_establish", [])
    scope_honest = len(does_not) >= 1 and not any("universal self" not in str(x).lower()
                                                  for x in does_not if "self" in str(x).lower())

    # 5. COUNTEREVIDENCE_RECALL: the Buddhist objection preserved as a defeater
    counter_present = any(k in blob for k in ["defeater", "objection", "fire", "wood", "counter"])

    print("== SYNTHESIS-NAT-NATURAL-v1 on the real VERTICAL-1 synthesis ==")
    print(f"  synthesis: {syn.get('synthesis_id')}  status={syn.get('status')}")
    print(f"  RIVAL_AS_CONSENSUS hits: {consensus_hits}  {'~0 ✓' if not consensus_hits else '✗ PRESENT'}")
    print(f"  OPEN_AS_RESOLVED hits:    {open_hits}  {'~0 ✓' if not open_hits else '✗ PRESENT'}")
    print(f"  POSITION_RECOVERY: rival={rival_present} saiva={saiva_present}")
    print(f"  ARGUMENT_COVERAGE markers: {argument_hits}")
    print(f"  CRUX_RECALL: crux/self-luminosity/inert present = {crux_present}")
    print(f"  SCOPE_FIDELITY: does_not_establish={does_not}  honest={scope_honest}")
    print(f"  COUNTEREVIDENCE_RECALL: defeater/objection present = {counter_present}")

    verdict = (not consensus_hits and not open_hits and rival_present and saiva_present
               and crux_present and scope_honest and counter_present)
    print(f"\n  VERDICT: {'PASS (natural synthesis preserves the debate)' if verdict else 'FAIL'}")

    out = os.path.join(ROOT, "benchmarks/v0/review/VERTICAL-1-SYNTHESIS-NAT-NATURAL.json")
    payload = {
        "object_kind": "SYNTHESIS_NAT_NATURAL",
        "bench": "PĀṬALA-SYNTHESIS-NAT-NATURAL-v1",
        "synthesis": syn.get("synthesis_id"),
        "metrics": {
            "RIVAL_AS_CONSENSUS": consensus_hits,
            "OPEN_AS_RESOLVED": open_hits,
            "POSITION_RECOVERY": {"rival": rival_present, "saiva": saiva_present},
            "ARGUMENT_COVERAGE": argument_hits,
            "CRUX_RECALL": crux_present,
            "SCOPE_FIDELITY": {"honest": scope_honest, "does_not_establish": does_not},
            "COUNTEREVIDENCE_RECALL": counter_present,
        },
        "verdict": "PASS" if verdict else "FAIL",
        "review_status": "NOT_HUMAN_REVIEWED",
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"  wrote {out}")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
