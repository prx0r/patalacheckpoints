"""Pāṭala passage-record schema.

The machine shape every pipeline stage writes into. Mirrors the house contract
(docs/TRANSLATION_SCHEMA.md) and maps 1:1 to the existing T1/T2/T3/C1 markdown.
Versioned 1.0.0.

Each stage (T1 → R1 → T2 → R2 → T3 → T3.1 → C1) appends its layer to this record.
The audit checker (audit.py) validates it at every level.
"""
from __future__ import annotations
from typing import Any, Optional

# The pipeline stages, in order. T3.1 is derived from T3 (in lock-step).
STAGES = ["T1", "R1", "T2", "R2", "T3", "T3.1", "C1"]

# The [G]/[P]/[A]/[R] justification codes (PASS_PROTOCOL.md §2)
JUSTIFICATION_CODES = ("G", "P", "A", "R")

# The R1 verdicts (R1_CONTENT_ENGINEERING.md)
R1_VERDICTS = ("RIGHT", "ERROR", "FORK", "OPEN")

# The typed ambiguity flags (TRANSLATION_SCHEMA.md) + the legacy house [X]
# (provisional / corrupt / unresolved — PASS_PROTOCOL.md status vocabulary).
FLAGS = ("TXT", "GRAM", "LEX", "DOCT", "WIT", "SUP", "X")

# The audit dimensions (per-dimension, not scalar confidence)
ASSESSMENT_DIMS = ("textual", "grammatical", "lexical", "interpretive")
ASSESSMENT_STATES = ("secure", "ambiguous", "uncertain", "moderate")

# Parallel kinds (TRANSLATION_SCHEMA.md)
PARALLEL_KINDS = (
    "exact_quote", "probable_quote", "adaptation", "formulaic_parallel",
    "lexical_parallel", "syntactic_parallel", "conceptual_parallel",
)


def new_passage(work_id: str, chapter: int, verse: int, sanskrit: str,
                edition: str, source_file: str) -> dict[str, Any]:
    """A blank, schema-valid passage record."""
    return {
        "passage_id": f"tantra:text:{work_id}:{chapter}.{verse}",
        "work_id": work_id,
        "location": {"chapter": chapter, "verse": verse},
        "source": {
            "source_edition": edition,
            "source_file": source_file,
            "source_text": sanskrit,
        },
        "stages": {},          # stage -> layer payload
        "audit": {},           # stage -> audit report
        "lineage": [],         # [{stage, created_by, derived_from, at}]
        "policy": {
            "translation_contract": "1.0.0",
            "style_guide": "1.0.0",
            "schema": "1.0.0",
        },
        "review_status": "T1",
    }


# ── the per-stage payload shapes ────────────────────────────────────────────

def stage_T1(close: str, reader_draft: str = "", flags: Optional[list] = None,
             notes: Optional[list] = None, lexical_decisions: Optional[list] = None,
             grammatical_notes: Optional[list] = None, parallels: Optional[list] = None,
             time_place_context: Optional[dict] = None) -> dict[str, Any]:
    """T1: one careful working translation + evidence + the required header."""
    return {
        "close_translation": close,
        "reader_draft": reader_draft,
        "flags": [f for f in (flags or []) if f in FLAGS],
        "notes": notes or [],
        "lexical_decisions": lexical_decisions or [],
        "grammatical_notes": grammatical_notes or [],
        "parallels": parallels or [],
        "time_place_context": time_place_context or {},
        "stage": "T1",
    }


def stage_R1(detail: str, anchor_quote: str = "",
             source: str = "", verdicts: Optional[list] = None) -> dict[str, Any]:
    """R1: the intimate peer review of T1 — a full assessment with per-crux
    verdicts (RIGHT/ERROR/FORK/OPEN) and commentary stubs. `verdicts` records
    the per-crux findings; the free-text `detail` carries the review."""
    verdicts = verdicts or []
    for v in verdicts:
        if v.get("verdict") not in R1_VERDICTS:
            raise ValueError(f"R1 verdict must be one of {R1_VERDICTS}, got {v.get('verdict')!r}")
    return {"detail": detail, "anchor_quote": anchor_quote,
            "source": source, "verdicts": verdicts, "stage": "R1"}


def stage_T2(close: str, strategy: str = "") -> dict[str, Any]:
    """T2: a fresh translation with a different strategy (blind of T1's sentences)."""
    return {"close_translation": close, "strategy": strategy, "stage": "T2"}


def stage_R2(chosen: str, reasoning: str, rejected: Optional[list] = None,
             commentary: str = "", hard_core: str = "",
             divergence: str = "", readability: str = "",
             school_context: str = "", equal_alternates: Optional[list] = None,
             is_open: bool = False) -> dict[str, Any]:
    """R2: the synthesis. Compares T1-vs-T2 line by line, adjudicates which is
    best, researches school/period context, expands the commentary, and notes
    equally-valid alternate translations. Marks genuinely-interpretable verses OPEN."""
    return {"chosen": chosen, "reasoning": reasoning,
            "rejected": rejected or [], "commentary": commentary,
            "hard_core": hard_core, "divergence": divergence,
            "readability": readability, "school_context": school_context,
            "equal_alternates": equal_alternates or [], "is_open": is_open,
            "stage": "R2"}


def stage_T3(resolved: str, open_flags: Optional[list] = None,
             editorial_notes: Optional[list] = None) -> dict[str, Any]:
    """T3: the final resolved text."""
    return {"resolved": resolved, "open_flags": open_flags or [],
            "editorial_notes": editorial_notes or [], "stage": "T3"}


def stage_T31(reading: str) -> dict[str, Any]:
    """T3.1: the natural-English reading layer, derived from T3 (in lock-step)."""
    return {"reading": reading, "stage": "T3.1"}


def stage_C1(interpretation: str, may_overturn: bool = False,
             overturns: str = "") -> dict[str, Any]:
    """C1: the plain-English commentary/interpretation."""
    return {"interpretation": interpretation, "may_overturn": may_overturn,
            "overturns": overturns, "stage": "C1"}


def set_stage(record: dict[str, Any], payload: dict[str, Any],
              created_by: str, derived_from: Optional[str] = None,
              supersedes: Optional[str] = None) -> dict[str, Any]:
    """Attach a stage payload and update the lineage."""
    stage = payload["stage"]
    record["stages"][stage] = payload
    record["lineage"].append({
        "stage": stage,
        "created_by": created_by,
        "derived_from": derived_from,
        "supersedes": supersedes,
    })
    record["review_status"] = stage
    return record


def get_stage(record: dict[str, Any], stage: str) -> Optional[dict[str, Any]]:
    return record["stages"].get(stage)
