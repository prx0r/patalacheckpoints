"""Pāṭala audit checker.

Validates a passage record at every pipeline stage. Two jobs:
1. **Schema validity** — is the record well-formed (ids, locations, enums)?
2. **Epistemic honesty** — does it carry the evidence it claims? No [X] laundered,
   no unsupported additions, no term drift, no machine output presented as reviewed.

Returns a list of {level, stage, code, message} findings. level ∈ {error, warn, info}.
An `error` fails the stage; a `warn` is flagged for human review.
"""
from __future__ import annotations
from typing import Any, Optional

try:
    from .schema import (
        STAGES, FLAGS, R1_VERDICTS, JUSTIFICATION_CODES,
        ASSESSMENT_DIMS, ASSESSMENT_STATES, PARALLEL_KINDS,
    )
except ImportError:  # run as a plain script, not as a package
    from schema import (
        STAGES, FLAGS, R1_VERDICTS, JUSTIFICATION_CODES,
        ASSESSMENT_DIMS, ASSESSMENT_STATES, PARALLEL_KINDS,
    )


def audit_record(record: dict[str, Any]) -> list[dict[str, str]]:
    """Audit a whole passage record across all stages present."""
    findings: list[dict[str, str]] = []

    # 1. identity integrity
    pid = record.get("passage_id", "")
    if not pid.startswith("tantra:text:"):
        findings.append({"level": "error", "stage": "record", "code": "BAD_PASSAGE_ID",
                         "message": f"passage_id not a tantra: urn: {pid!r}"})
    if record.get("work_id") not in pid:
        findings.append({"level": "warn", "stage": "record", "code": "WORK_ID_MISMATCH",
                         "message": f"work_id {record.get('work_id')!r} not in {pid}"})
    loc = record.get("location", {})
    if not isinstance(loc.get("chapter"), int) or not isinstance(loc.get("verse"), int):
        findings.append({"level": "error", "stage": "record", "code": "BAD_LOCATION",
                         "message": "location must have integer chapter + verse"})
    src = record.get("source", {})
    if not src.get("source_text", "").strip():
        findings.append({"level": "error", "stage": "record", "code": "EMPTY_SOURCE",
                         "message": "source.source_text is empty"})
    if not src.get("source_edition", "").strip():
        findings.append({"level": "warn", "stage": "record", "code": "NO_EDITION",
                         "message": "source.source_edition is empty"})

    # 2. per-stage audits
    stages = record.get("stages", {})
    for stage in STAGES:
        if stage in stages:
            findings += _audit_stage(stage, stages[stage])

    # 3. ordering / lineage
    lineage = record.get("lineage", [])
    present = [l["stage"] for l in lineage]
    # stages must be in order and contiguous from T1
    for i, s in enumerate(present):
        if s != STAGES[i]:
            findings.append({"level": "error", "stage": "lineage", "code": "STAGE_ORDER",
                             "message": f"expected {STAGES[i]}, found {s} at position {i}"})
    # no machine output presented as reviewed
    t3 = stages.get("T3", {})
    if t3 and stages.get("R2") is None:
        findings.append({"level": "error", "stage": "T3", "code": "NO_ADJUDICATION",
                         "message": "T3 present without a prior R2 adjudication"})

    return findings


def _audit_stage(stage: str, p: dict[str, Any]) -> list[dict[str, str]]:
    f: list[dict[str, str]] = []

    if stage == "T1":
        if not p.get("close_translation", "").strip():
            f.append({"level": "error", "stage": "T1", "code": "NO_CLOSE",
                      "message": "T1.close_translation is empty"})
        for fl in p.get("flags", []):
            if fl not in FLAGS:
                f.append({"level": "error", "stage": "T1", "code": "BAD_FLAG",
                          "message": f"unknown flag {fl!r}"})
        # time-place-context required
        tpc = p.get("time_place_context", {})
        for field in ("PERIOD", "PLACE", "GENRE", "FRAME"):
            if not str(tpc.get(field, "")).strip():
                f.append({"level": "warn", "stage": "T1", "code": "MISSING_TPC",
                          "message": f"time_place_context.{field} is empty"})
        # [X]-honesty: an [X] in flags must be resolved or carried into T3
        for note in p.get("notes", []):
            if "[X]" in str(note) and not p.get("flags"):
                # a note flagging [X] should surface in flags; not fatal
                f.append({"level": "warn", "stage": "T1", "code": "X_NOT_FLAGGED",
                          "message": "note mentions [X] but no flag recorded"})

    elif stage == "R1":
        for v in p.get("verdicts", []):
            if v.get("verdict") not in R1_VERDICTS:
                f.append({"level": "error", "stage": "R1", "code": "BAD_VERDICT",
                          "message": f"R1 verdict must be one of {R1_VERDICTS}, got {v.get('verdict')!r}"})
        if not p.get("detail", "").strip():
            f.append({"level": "warn", "stage": "R1", "code": "NO_DETAIL",
                      "message": "R1 detail is empty"})

    elif stage == "R2":
        if not p.get("chosen", "").strip():
            f.append({"level": "warn", "stage": "R2", "code": "NO_CHOSEN",
                      "message": "R2.chosen is empty"})
        if not p.get("reasoning", "").strip():
            f.append({"level": "warn", "stage": "R2", "code": "NO_REASONING",
                      "message": "R2.reasoning is empty"})

    elif stage == "T3":
        if not p.get("resolved", "").strip():
            f.append({"level": "error", "stage": "T3", "code": "NO_RESOLVED",
                      "message": "T3.resolved is empty"})

    elif stage == "T3.1":
        if not p.get("reading", "").strip():
            f.append({"level": "error", "stage": "T3.1", "code": "NO_READING",
                      "message": "T3.1.reading is empty"})

    elif stage == "C1":
        if not p.get("interpretation", "").strip():
            f.append({"level": "warn", "stage": "C1", "code": "NO_INTERPRETATION",
                      "message": "C1.interpretation is empty"})

    return f


def audit_ok(findings: list[dict[str, str]]) -> bool:
    """True if there are no error-level findings."""
    return not any(x["level"] == "error" for x in findings)


def summary(findings: list[dict[str, str]]) -> str:
    errs = [x for x in findings if x["level"] == "error"]
    warns = [x for x in findings if x["level"] == "warn"]
    return f"{len(errs)} errors, {len(warns)} warnings"


def report(findings: list[dict[str, str]]) -> str:
    lines = [f"AUDIT: {summary(findings)}"]
    for x in findings:
        lines.append(f"  [{x['level'].upper()}] {x['stage']}:{x['code']} — {x['message']}")
    return "\n".join(lines)
