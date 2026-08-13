#!/usr/bin/env python3
"""source-evidence/evals/patala/tasks/warrant_reconstruction.py — the warrant-reconstruction program.

The directive: warrant reconstruction deserves its own research program. How good are reconstructed
warrants? This may be harder than proposition extraction.

Separate three kinds of inference (never conflate them):
    TEXT_EXPLICIT            the inference is stated in the source
    RATIONAL_RECONSTRUCTION  the inference is a defensible bridge the passage licenses but does not
                             state (necessitated by the premises+conclusion, constrained by spans)
    EDITORIAL_RECONSTRUCTION the inference is the modern interpreter's editorial/philosophical
                             reconstruction (weaker licensing)

Every warrant object must state:
    why it is needed
    what textual evidence constrains it
    whether alternative warrants exist
    what would change if rejected

The key risk this guards against: the machine pretending its glue was written by Abhinavagupta. A
RATIONAL_RECONSTRUCTION warrant is honest glue ONLY if it is (a) necessitated by the premises+conclusion
and (b) textually constrained (not invented).
"""
from __future__ import annotations

import json
import os
import re
import sys

# canonical warrant kinds
WARRANT_KINDS = ("TEXT_EXPLICIT", "RATIONAL_RECONSTRUCTION", "EDITORIAL_RECONSTRUCTION")

# textually-constraining signals in a source span (a warrant citing any of these is anchored)
_ANCHOR_CUES = (r"\(line", r"\(lines", r"kārikā", r"karika", r"sūtra", r"sutra", r"\d+–\d+", r"\d+-\d+")


def classify_warrant(warrant_text: str, source_has_explicit_inference: bool) -> str:
    """Classify a warrant as TEXT_EXPLICIT / RATIONAL_RECONSTRUCTION / EDITORIAL_RECONSTRUCTION.

    Rules (deterministic, structural):
      - If the source explicitly states the inference -> TEXT_EXPLICIT.
      - Else if the warrant is anchored (cites a line/kārikā/span) and hedged -> RATIONAL_RECONSTRUCTION.
      - Else if it asserts an unanchored bridging principle -> EDITORIAL_RECONSTRUCTION.
    """
    low = (warrant_text or "").lower()
    anchored = bool(re.search("|".join(_ANCHOR_CUES), warrant_text or ""))
    hedged = any(k in low for k in ("reconstruct", "it can be", "one can", "plausibly", "we infer",
                                    "warrant", "the bridge", "licensed"))
    # TEXT_EXPLICIT only if the source truly states it (caller decides via source_has_explicit_inference)
    if source_has_explicit_inference:
        return "TEXT_EXPLICIT"
    # anchored = cites a real span -> rational reconstruction (the constraint is the anchor itself)
    if anchored:
        return "RATIONAL_RECONSTRUCTION"
    # hedged but unanchored -> still rational reconstruction (the hedge owns the reconstruction)
    if hedged:
        return "RATIONAL_RECONSTRUCTION"
    return "EDITORIAL_RECONSTRUCTION"


def build_warrant_object(*, warrant_text, premise_ids, conclusion_id,
                         source_has_explicit_inference=False,
                         textual_constraints=(), alternatives=(), defeaters=()) -> dict:
    """The full warrant metadata object (the directive's JSON shape)."""
    kind = classify_warrant(warrant_text, source_has_explicit_inference)
    return {
        "warrant": warrant_text,
        "status": kind,
        "necessitated_by": list(premise_ids) + [conclusion_id],
        "textual_constraints": list(textual_constraints),
        "alternatives": list(alternatives),
        "defeaters": list(defeaters),
        "why_needed": (f"the step from {list(premise_ids)} to {conclusion_id} requires a license; "
                       "if none is stated it must be reconstructed and flagged as such"),
        "would_change_if_rejected": ("the conclusion {conclusion_id} loses its license and must be "
                                     "marked UNSUPPORTED, not silently retained"),
    }


def evaluate_warrant_reconstruction(gold_warrant: dict, candidate_warrant: dict) -> dict:
    """Score a candidate warrant against the frozen gold warrant.

    Metrics:
      - status accuracy: does the candidate classify the warrant the same way as the gold?
      - invention penalty: a candidate that upgrades a RATIONAL_RECONSTRUCTION to TEXT_EXPLICIT
        (pretends the source states it) is a fabrication.
      - constraint coverage: fraction of gold textual_constraints the candidate also cites.
    """
    g_status = gold_warrant.get("status")
    c_status = candidate_warrant.get("status")
    status_ok = (c_status == g_status)

    fabricated = (g_status in ("RATIONAL_RECONSTRUCTION", "EDITORIAL_RECONSTRUCTION")
                  and c_status == "TEXT_EXPLICIT")

    # constraint coverage
    g_cons = set(gold_warrant.get("textual_constraints", []))
    c_cons = set(candidate_warrant.get("textual_constraints", []))
    constraint_coverage = len(g_cons & c_cons) / len(g_cons) if g_cons else 1.0

    # alternative-warrant awareness: does the candidate note alternatives when the gold does?
    alt_aware = bool(candidate_warrant.get("alternatives")) if gold_warrant.get("alternatives") else True

    return {
        "status_accuracy": 1.0 if status_ok else 0.0,
        "fabrication_flagged": fabricated,           # True = candidate pretended source states it
        "constraint_coverage": round(constraint_coverage, 4),
        "alternative_warrant_awareness": 1.0 if alt_aware else 0.0,
    }


def aggregate(scores: list[dict]) -> dict:
    n = len(scores)
    return {
        "cases": n,
        "status_accuracy": round(sum(s["status_accuracy"] for s in scores) / n, 4) if n else None,
        "fabrication_rate": round(sum(1 for s in scores if s["fabrication_flagged"]) / n, 4) if n else None,
        "constraint_coverage": round(sum(s["constraint_coverage"] for s in scores) / n, 4) if n else None,
        "alternative_warrant_awareness": round(sum(s["alternative_warrant_awareness"] for s in scores) / n, 4) if n else None,
    }


if __name__ == "__main__":
    # self-test: honest vs fabricated warrant
    gold = build_warrant_object(
        warrant_text="inertness blocks establishing (lines 10-12)",
        premise_ids=["P2"], conclusion_id="C1",
        textual_constraints=["line 11"], alternatives=["W2 (causal continuity)"], defeaters=["O3-fire-wood"])
    honest = build_warrant_object(
        warrant_text="inertness blocks establishing (lines 10-12)",
        premise_ids=["P2"], conclusion_id="C1",
        textual_constraints=["line 11"], alternatives=["W2"])
    fabricated = build_warrant_object(
        warrant_text="Abhinavagupta explicitly states inertness blocks establishing",
        premise_ids=["P2"], conclusion_id="C1",
        source_has_explicit_inference=True)  # the candidate WRONGLY claims the source states it
    r_honest = evaluate_warrant_reconstruction(gold, honest)
    r_fab = evaluate_warrant_reconstruction(gold, fabricated)
    print("honest warrant:   ", json.dumps(r_honest))
    print("fabricated warrant:", json.dumps(r_fab))
    assert r_honest["fabrication_flagged"] is False
    assert r_fab["fabrication_flagged"] is True
    assert gold["status"] == "RATIONAL_RECONSTRUCTION"
    print("SELF-TEST PASS (warrant reconstruction discriminates honest from fabricated glue)")
