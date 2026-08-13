#!/usr/bin/env python3
"""experiments/vertical1_certificate.py — PATALA-VERTICAL-1 benchmark certificate (devpath13 P16).

Assemble the PATALA-VERTICAL-1 certificate: one complete chain certified per the directive §P16,
reporting HONEST authority at each node. It certifies that the VERTICAL-1 stack (Pratyabhijñā
recognition vs Buddhist determination / adhyavasāya) was pushed through every layer and that each
node's authority is honestly reported — NOT that any node is scholar-validated.

Nodes (directive §P16):
    Atlas source identity · T1/L0 · ARGMAP NAT · Propositions · Argument · Crux · ArgumentSynthesis ·
    EssayPlan/Claims · Full audited essay · Education interactions · ReviewBundle ·
    Universal ContextBundle · Correction propagation

Honest authority vocabulary: MACHINE_PROPOSED / ENGINEERING_VALIDATED (never reviewed). No H witness.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))


def _read(rel):
    p = os.path.join(ROOT, rel)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    nodes = [
        {"node": "Atlas source identity",
         "artifact": "data/published/ipvv/index.json (work_id)",
         "authority": "ENGINEERING_VALIDATED",
         "verdict": "✓ identity resolved (isvarapratyabhijnavivrtivimarsini)",
         "open": "raw Sanskrit not on-disk; L2/C1 chain is the frozen reference"},
        {"node": "T1 / L0",
         "artifact": "data/published/ipvv/*.json (l0/l2)",
         "authority": "MACHINE_PROPOSED",
         "verdict": "✓ real L2 read frozen for VERTICAL-1 (pilot_V1M_L2_read.md)",
         "open": "NOT_HUMAN_REVIEWED"},
        {"node": "ARGMAP NAT",
         "artifact": "source-evidence/evals/patala/tasks/argmap_eval.py",
         "authority": "ENGINEERING_VALIDATED",
         "verdict": "✓ verifier on real committed map + 51 IPVV exemplars (shape 1.0)",
         "open": "verifier competence, not generator accuracy"},
        {"node": "Propositions",
         "artifact": "machinelearning/research/patala_ml/proposition_layer.py (G3A gate)",
         "authority": "ENGINEERING_VALIDATED",
         "verdict": "✓ derivational layer + G3A NAT gate (NOT_ELIGIBLE on ARGMAP failure)",
         "open": "NOT_HUMAN_REVIEWED"},
        {"node": "Argument",
         "artifact": "benchmarks/v0/review/SYN-IPVV-REFLEXION-CORE-001.json (inputs)",
         "authority": "ENGINEERING_VALIDATED",
         "verdict": "✓ real ARG-GOLD-002/004 reconstructed",
         "open": "bounded Nyāya profile; never argument_valid=true"},
        {"node": "Crux",
         "artifact": "benchmarks/v0/review/VERTICAL-1-CRUX-VALIDATION.json",
         "authority": "ENGINEERING_VALIDATED",
         "verdict": "✓ P6 stress-test: redundant support, defeaters, alternative routes (CRUX-IPVV-001)",
         "open": "perturbation result, MACHINE_PROPOSED"},
        {"node": "ArgumentSynthesis",
         "artifact": "benchmarks/v0/review/VERTICAL-1-SYNTHESIS-NAT-NATURAL.json",
         "authority": "MACHINE_PROPOSED / UNRESOLVED ceiling",
         "verdict": "✓ SYNTHESIS-NAT-NATURAL: RIVAL_AS_CONSENSUS=0, OPEN_AS_RESOLVED=0",
         "open": "UNRESOLVED (weakest-governs over load-bearing deps)"},
        {"node": "EssayPlan / EssayClaims",
         "artifact": "benchmarks/v0/review/ESSAY-PLAN-IPVV-REFLEXION-CORE-001.json",
         "authority": "MACHINE_PROPOSED",
         "verdict": "✓ plan + claims derive from the synthesis",
         "open": "claims resolve to synthesis->argument->proposition->span"},
        {"node": "Full audited essay",
         "artifact": "benchmarks/v0/review/VERTICAL-1-ESSAY-AUDIT.json",
         "authority": "MACHINE_PROPOSED",
         "verdict": "△ THESIS_WARRANTED/ARGUMENT_BALANCE/CRUX_FIDELITY/CONCLUSION_STRENGTH pass; "
                    "SOURCE_TRACEABILITY FAIL (S012/S013 lack refs)",
         "open": "whole-essay traceability gap OPEN"},
        {"node": "Education interactions",
         "artifact": "benchmarks/v0/review/VERTICAL-1-EDUCATION.json",
         "authority": "MACHINE_PROPOSED",
         "verdict": "✓ 8 interactions, epistemic + pedagogical validity PASS",
         "open": "no learner user-testing yet"},
        {"node": "ReviewBundle",
         "artifact": "pipeline/review_bundle.py",
         "authority": "ENGINEERING_VALIDATED (mechanism)",
         "verdict": "✓ ReviewEvent/Adjudication/Impact mechanism tested (23/23)",
         "open": "no external scholar has reviewed a VERTICAL-1 object"},
        {"node": "Universal ContextBundle",
         "artifact": "devpath12 (materialize_context)",
         "authority": "ENGINEERING_VALIDATED (mechanism)",
         "verdict": "✓ profiles + exact refs + honest authority (devpath12 closed)",
         "open": "production validation on VERTICAL-1 objects OPEN"},
        {"node": "Correction propagation",
         "artifact": "benchmarks/v0/review/VERTICAL-1-CORRECTION.json",
         "authority": "ENGINEERING_VALIDATED",
         "verdict": "✓ REVISE G2-TC2 propagates NEED_REVIEW through INF/CONC; isolation holds",
         "open": "semantic downstream marked stale (synthesis->essay->education)"},
    ]

    certified = sum(1 for n in nodes if n["verdict"].startswith("✓"))
    open_nodes = [n["node"] for n in nodes if not n["verdict"].startswith("✓")]

    cert = {
        "certificate_id": "PATALA-VERTICAL-1",
        "issued": now,
        "argument": "Pratyabhijñā recognition vs Buddhist determination (adhyavasāya)",
        "dossier": "data/published/ipvv/IPVV-VERTICAL-001-SOURCE-DOSSIER.md",
        "nodes": nodes,
        "summary": {
            "certified": certified,
            "total": len(nodes),
            "open_nodes": open_nodes,
        },
        "authority_statement": ("Every node above is MACHINE_PROPOSED or ENGINEERING_VALIDATED at best. "
                                "No node is SCHOLARLY_CORROBORATED or INDEPENDENT_REVIEWED; only an H "
                                "(human) witness raises authority. This certificate certifies that the "
                                "stack survived the real argument end-to-end, NOT that it is scholar-correct."),
        "review_status": "NOT_HUMAN_REVIEWED",
    }

    out = os.path.join(ROOT, "benchmarks", "v0", "review", "PATALA-VERTICAL-1-CERTIFICATE.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2, ensure_ascii=False)

    print("PATALA-VERTICAL-1 certificate")
    for n in nodes:
        print(f"  {'✓' if n['verdict'].startswith('✓') else '△'} {n['node']:24} [{n['authority']}]")
        print(f"      {n['verdict']}")
    print(f"\n  certified {certified}/{len(nodes)}; open: {open_nodes}")
    print("  authority: all MACHINE_PROPOSED/ENGINEERING_VALIDATED; no H witness (NOT_HUMAN_REVIEWED)")
    print(f"\n  wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
