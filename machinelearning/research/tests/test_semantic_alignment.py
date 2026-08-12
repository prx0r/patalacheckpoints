#!/usr/bin/env python3
"""test_semantic_alignment.py — validation of the Stage-A align() harness (vocabulary + abstention)."""
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.semantic_alignment import align, occurrence, LABELS, SPACES

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)

print("== vocabulary + spaces ==")
check("6-label vocabulary preserved", set(LABELS) == {"SAME_SENSE","NEAR_SAME","PARTIAL_OVERLAP",
      "DIFFERENT_SENSE","AMBIGUOUS","NOT_ENOUGH_CONTEXT"})
check("3 representation spaces", set(SPACES) == {"sanskrit","l2","c1"})

print("\n== align() contract ==")
A = occurrence("vimarśa", sanskrit="pratibhā vimarśa sphurattā", l2="reflexive awareness",
               c1="The essence of light is the reflexive awareness, not the bare showing of objects. "
                  "The crystal supplies the contrast.", passage_id="pt:p1")
B = occurrence("vimarśa", sanskrit="vimarśa sphurattā prakāśa", l2="reflexive awareness",
               c1="The reflexive awareness is the light's own grasp of itself in the act of manifesting.",
               passage_id="pt:p2")
r = align(A, B)
check("returns relation_proposal", r["relation_proposal"] in LABELS)
check("returns evidence + model_scores + abstain_reason",
      all(k in r for k in ["relation_proposal","evidence","model_scores","abstain_reason","status"]))
check("status is MACHINE_PROPOSED", r["status"] == "MACHINE_PROPOSED")

print("\n== abstention: NOT_ENOUGH_CONTEXT on near-empty occurrences ==")
C = occurrence("x", sanskrit="", l2="", c1="hi", passage_id="pt:p3")
D = occurrence("x", sanskrit="", l2="", c1="yo", passage_id="pt:p4")
r2 = align(C, D)
check("abstains NOT_ENOUGH_CONTEXT on too-short text", r2["relation_proposal"] == "NOT_ENOUGH_CONTEXT",
      r2["relation_proposal"])

print("\n== empty l2 space handled (does not crash, returns a label) ==")
E = occurrence("y", sanskrit="akrama pratibhā", l2="", c1="The orderless support is not itself ordered.",
               passage_id="pt:p5")
F = occurrence("y", sanskrit="pratibhā akrama", l2="", c1="The support, being orderless, is the knower.",
               passage_id="pt:p6")
r3 = align(E, F)
check("empty l2 does not crash; returns a valid label", r3["relation_proposal"] in LABELS,
      r3["relation_proposal"])

print(f"\n=== RESULT: {len(failures)} fail ===")
sys.exit(1 if failures else 0)
