#!/usr/bin/env python3
"""audit_golds_vs_IR.py — check the 5 golds against the 14-object philosophical IR.

Per ARGUMENT-IR-VISION.md, the CP4 gate is: "can this gold argument be represented in the IR
without loss?" This audits each gold against the IR objects it should carry, and records exactly
where each falls short — so we know what to add (evidence-driven, not empty schema-building).

IR objects (activate first): ResearchQuestion · Proposition(derivational) · Commitment ·
DebateFrame · InferenceRule · InferenceApplication · Argument · Crux
Thin for now: Position · Attack · Preference · SemanticAlignment(3-level) · EpistemicRegime · ArgumentScheme
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from patala_ml.gold import build_gold_v0
from patala_ml.gold002 import build_gold_002
from patala_ml.gold003 import build_gold_003
from patala_ml.gold004 import build_gold_004
from patala_ml.gold005 import build_gold_005

BUILDERS = {"ARG-GOLD-001": build_gold_v0, "ARG-GOLD-002": build_gold_002,
            "ARG-GOLD-003": build_gold_003, "ARG-GOLD-004": build_gold_004,
            "ARG-GOLD-005": build_gold_005}

# IR objects -> how the gold should carry them (presence check)
IR_CHECK = {
    "ResearchQuestion": lambda g: "research_question" in g or (g.get("debate_frame") or {}).get("question"),
    "DebateFrame": lambda g: "debate_frame" in g,
    "Proposition": lambda g: len(g.get("nodes", [])) > 0,
    "Proposition.derivational": lambda g: any("derived_from" in n for n in g.get("nodes", [])),
    "Commitment": lambda g: any("commitment" in n or "speaker" in n or "dialectical_role" in n
                                for n in g.get("nodes", [])),
    "InferenceRule/Application": lambda g: len(g.get("inferences", [])) > 0,
    "SemanticAlignment": lambda g: bool((g.get("debate_frame") or {}).get("semantic_alignments")),
    "Boundary": lambda g: bool(g.get("boundary")),
}


def audit() -> dict:
    rows = {}
    for gid, fn in BUILDERS.items():
        g = fn()
        missing = [obj for obj, test in IR_CHECK.items() if not test(g)]
        rows[gid] = {
            "has_debate_frame": "debate_frame" in g,
            "has_research_question": "research_question" in g,
            "n_nodes": len(g.get("nodes", [])),
            "n_inferences": len(g.get("inferences", [])),
            "node_with_commitment": sum(1 for n in g.get("nodes", [])
                                        if n.get("commitment") or n.get("speaker") or n.get("dialectical_role")),
            "node_with_derived_from": sum(1 for n in g.get("nodes", []) if n.get("derived_from")),
            "missing_IR_objects": missing,
        }
    return rows


def main() -> int:
    rows = audit()
    print("GOLD vs 14-OBJECT IR AUDIT (CP4 gate: representable without loss)")
    print(f"{'Gold':12} {'df':5} {'deriv':7} {'comm':6} {'missing'}")
    for gid, r in rows.items():
        print(f"{gid:12} {'Y' if r['has_debate_frame'] else 'N':5} "
              f"{r['node_with_derived_from']:3}/{r['n_nodes']:1} "
              f"{r['node_with_commitment']:3}/{r['n_nodes']:1} "
              f"{','.join(r['missing_IR_objects'])}")
    print("\nWHERE EACH FALLS SHORT (the evidence-driven gap):")
    for gid, r in rows.items():
        if r["missing_IR_objects"]:
            print(f"  {gid}: missing {r['missing_IR_objects']}")

    # write a machine-readable audit (repo root = 4 levels up from experiments/)
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))), "benchmarks/v0/review/ARG-IR-AUDIT.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)
    print(f"\naudit written: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
