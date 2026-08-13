#!/usr/bin/env python3
"""test_synthesis_core.py — devpath8 (ArgumentSynthesis core) acceptance.

Checks (per the directive §8 + the globalplan Phase 8):
  1. ArgumentSynthesis is a typed object with ResearchQuestion / DebateFrame / Position / relations
  2. the relation vocabulary is frozen (SUPPORTS/ATTACKS/UNDERPINS/UNDERMINES/REPLIES_TO/RESTRICTS/COMPLEMENTS)
  3. it NEVER asserts a single true conclusion (not a truth object); preserves disagreement
  4. it preserves: speaker identity, argument direction, cruxes, source grounding, review status
  5. build_synthesis_from_gold produces one synthesis over a real gold with positions derived from
     commitments (opponent NOT collapsed into consensus)
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from patala_ml.synthesis_core import (
    ResearchQuestion, DebateFrame, Position, ArgumentRelation, ArgumentSynthesis,
    build_synthesis, build_synthesis_from_gold, RELATION_VOCABULARY,
)
from patala_ml.gold002 import build_gold_002

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


print("== typed synthesis objects + frozen relation vocabulary ==")
check("ArgumentSynthesis is defined", ArgumentSynthesis is not None)
check("relation vocabulary frozen (7)", set(RELATION_VOCABULARY) ==
      {"SUPPORTS", "ATTACKS", "UNDERPINS", "UNDERMINES", "REPLIES_TO", "RESTRICTS", "COMPLEMENTS"})

print("\n== not a truth object (never asserts a single true conclusion) ==")
q = ResearchQuestion(research_question_id="RQ-1", question="Is recognition recollection?")
pos = Position(position_id="POS-A", label="A", stance="ŚAIVA")
frame = DebateFrame(debate_frame_id="DF-1", research_question_ref="RQ-1", positions=[pos])
s = build_synthesis(synthesis_id="S-1", question=q, frame=frame, arguments=["ARG-1"],
                    relations=[], cruxes=["CRUX-1"], propositions=["P1"],
                    supported_conclusions=[], counterevidence=[],
                    open_questions=[], scope_boundaries=[], unresolved_disagreement=["opponent present"])
check("supported_conclusions empty (no truth asserted)", s.supported_conclusions == [])
check("is_truth_asserting is False", s.is_truth_asserting() is False)
check("review_status defaults NOT_REVIEWED", s.review_status == "NOT_REVIEWED")

print("\n== preserves disagreement + positions ==")
g = build_gold_002()
out = build_synthesis_from_gold(g, synthesis_id="SYNTH-IPVV",
                                research_question="Is recognition recollection?")
s2 = ArgumentSynthesis(**out)
labels = [p.label for p in s2.debate_frame.positions]
check("positions derived from commitments (incl. opponent)", any("Opponent" in l for l in labels), labels)
check("disagreement preserved (opponent not collapsed)",
      any("opponent" in u.lower() for u in s2.unresolved_disagreement))
check("arguments present", len(s2.arguments) >= 1, str(s2.arguments))
check("cruxes present", len(s2.cruxes) >= 1, str(s2.cruxes))
check("relations present", len(s2.relations) >= 1, str([(r.from_ref, r.relation) for r in s2.relations]))
check("source grounding present", len(s2.source_refs) >= 1, str(s2.source_refs[:2]))
check("supported_conclusions empty (honest)", s2.supported_conclusions == [])
check("no manufactured consensus", s2.is_truth_asserting() is False)

print("\n== relations use the frozen vocabulary ==")
check("all relations in vocabulary", all(r.relation in RELATION_VOCABULARY for r in s2.relations))

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (ArgumentSynthesis core works)"))
sys.exit(1 if failures else 0)
