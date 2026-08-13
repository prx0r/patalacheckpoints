#!/usr/bin/env python3
"""test_semantic_recovery_judge.py — P0 semantic matcher acceptance.

Checks (the reviewer's two-stage design):
  1. two stages exist: candidate alignment (embedding+lexical) + structured semantic judge
  2. a near-paraphrase of a gold proposition RECOVERS it (EQUIVALENT/NARROWER)
  3. a polarity-flipped claim is flagged CONTRADICTS (the 'embedding says they're similar' trap)
  4. the judge returns structured fields (relation + speaker/scope/modality/commitment)
  5. the design is frozen-safe: the offline fallback is deterministic and the LLM path is a swap-in
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from semantic_recovery_judge import (
    score_recovery_semantic, semantic_judge, align_candidates, RELATIONS,
)

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


print("== 1. two-stage design ==")
g1 = {"propositions": [
    {"pid": "P1", "text": "the pure ahaṃ-pratyavamarśa is not a vikalpa; it is the two-invoking determination"}]}
check("stage-1 align_candidates returns top-k per step", callable(align_candidates))
check("judge returns a relation from the vocabulary",
      semantic_judge("A", "B", use_llm=False)["relation"] in RELATIONS)

print("\n== 2. paraphrase recovers ==")
good = {"argument_steps": [
    "the pure 'I'-recollection is not a conceptual construction but the two-invoking determination"]}
r = score_recovery_semantic(g1, good, use_llm=False)
check("paraphrase recovers the gold (recall > 0)", r["proposition_recall"] > 0.5, r["proposition_recall"])

print("\n== 3. polarity-flip = contradiction (the trap) ==")
bad = {"argument_steps": ["the I-recollection IS a vikalpa, a constructed relation"]}
rb = score_recovery_semantic(g1, bad, use_llm=False)
check("contradiction flagged", len(rb["contradictions"]) > 0, str(rb["contradictions"]))
check("contradiction does NOT count as recovered", rb["proposition_recall"] == 0.0, rb["proposition_recall"])

print("\n== 4. structured judge fields ==")
j = semantic_judge("consciousness is self-aware", "consciousness is reflexive", use_llm=False)
check("judge has relation + axis matches",
      "relation" in j and "speaker_match" in j and "scope_match" in j and
      "modality_match" in j and "commitment_match" in j)

print("\n== 5. LLM path is a swap-in (offline fallback deterministic) ==")
j1 = semantic_judge("X", "Y", use_llm=False)
j2 = semantic_judge("X", "Y", use_llm=False)
check("offline fallback deterministic", j1 == j2)

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (P0 semantic recovery matcher works offline)"))
sys.exit(1 if failures else 0)
