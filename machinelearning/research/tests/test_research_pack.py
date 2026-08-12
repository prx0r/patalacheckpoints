#!/usr/bin/env python3
"""test_research_pack.py — the ResearchPack composition-layer contract.

A ResearchPack is a composition/projection layer, not a new epistemic layer. It must reference
existing objects (arguments/themes/propositions/evidence) and carry an honest review state. It must
NOT claim scholarly validity unless genuinely reviewed. It is the bridge between representation
(IR) and scholarly output (essays) — usable even when provisional.
"""
from __future__ import annotations

import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "experiments"))

from check_research_pack import check_pack

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
PACKS = os.path.join(ROOT, "benchmarks/v0/packs")

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


print("== every ResearchPack is well-formed (composition layer) ==")
pack_files = sorted(glob.glob(os.path.join(PACKS, "*.json")))
check("at least one ResearchPack exists", bool(pack_files))
for f in pack_files:
    r = check_pack(f)
    check(f"valid: {os.path.basename(f)}", r["ok"], str(r["problems"]))

print("\n== the Non-constructed-I pack references existing objects (not copied content) ==")
if pack_files:
    p = json.load(open(os.path.join(PACKS, "PACK-IPVV-NONCONSTRUCTED-I.json")))
    check("references ARG-GOLD-002 (the argument)", "ARG-GOLD-002" in p["argument_refs"])
    check("references themes (cand_vikalpa/construction/reflexive)", bool(p["theme_refs"]))
    check("references ARG-002 propositions", "G2-TC2" in p["proposition_refs"])
    check("has a dependency graph (for revision propagation)", len(p["dependency_graph"]) >= 4)
    check("honest review: composition complete, scholarly NONE",
          p["review_summary"]["composition"] == "COMPLETE"
          and p["review_summary"]["scholarly_review"] == "NONE"
          and p["review_summary"]["scholarly_validated"] is False)
    check("essay rendering points to the existing essay",
          "ESSAY-NONCONSTRUCTED-I.md" in p["renderings"]["essay"])

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (ResearchPack is a valid composition layer)"))
sys.exit(1 if failures else 0)
