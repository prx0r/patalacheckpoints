#!/usr/bin/env python3
"""test_essay_from_synthesis.py — the first essay that consumes an ArgumentSynthesis, respecting the render rule.

Verifies:
1. The essay consumes the synthesis and respects its UNRESOLVED ceiling.
2. The reconstructed bridge (SYN-INF-001) is rendered as a marked reconstruction, not settled.
3. Every load-bearing sentence maps to a claim (SentenceEvidenceAudit: no orphan substantive sentences).
4. The hard rule: an UNRESOLVED claim is never rendered with certainty-inflation language.
5. The essay carries the gold-standard honest boundary (reflexivity established, universalization not entailed).
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


path = os.path.join(ROOT, "benchmarks/v0/review/ESSAY-REFLEXION-CORE-001.json")
check("essay exists", os.path.exists(path))
essay = json.load(open(path))

print("== the essay consumes the ArgumentSynthesis ==")
check("essay consumes the synthesis", essay["consumes_synthesis"] == "SYN-IPVV-REFLEXION-CORE-001")
check("essay inherits the UNRESOLVED ceiling", essay["synthesis_ceiling"] == "UNRESOLVED")
check("essay records the unsupported bridge (not hidden)", essay["unsupported_bridges"] == ["SYN-INF-001"])

print("\n== the reconstructed bridge is marked, never settled ==")
plan = essay["plan"]
thesis_sentences = [s for s in plan["sentences"] if "essay:c3" in s["claim_ids"]]
check("the thesis bridge sentence is marked as reconstruction",
      thesis_sentences and all(s.get("marked_bridge") for s in thesis_sentences))
thesis_text = " ".join(s["text"] for s in thesis_sentences)
check("thesis sentence uses honest language (reconstructed, not proven)",
      "reconstruct" in thesis_text.lower())

print("\n== every load-bearing sentence maps to a claim (no orphan substantive) ==")
for s in plan["sentences"]:
    check(f"sentence {s['id']} has claim_ids", bool(s.get("claim_ids")))

print("\n== the hard render rule: UNRESOLVED is qualified, never settled ==")
# no sentence licensed by an UNRESOLVED claim may use certainty-inflation language
inflation = ["proves", "certainly", "definitively", "therefore it is settled", "undeniably"]
violations = [s["id"] for s in plan["sentences"]
              if any(t in s["text"].lower() for t in inflation)]
check("no certainty inflation in any sentence", not violations, str(violations))

print("\n== the essay carries the gold-standard honest boundary ==")
boundary_claim = [c for c in plan["claims"] if c["id"] == "essay:c4"][0]
check("the boundary claim (reflexivity established, universalization not entailed) is present",
      "contested" in boundary_claim["text"] and "not entailed" in boundary_claim["text"])
check("essay includes a qualification sentence (universal-Self left open)",
      any("Universal Self" in s["text"] or "universal Self" in s["text"] for s in plan["sentences"]))

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (essay consumes the synthesis; render rule respected)"))
sys.exit(1 if failures else 0)
