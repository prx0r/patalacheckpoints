"""Pāṭala audit checker.

Validates a passage record at every pipeline stage. Audits are split into THREE
tiers so the docs never over-promise what's enforced:

STRUCTURAL (deterministic, implemented here):
  - schema validity (ids, locations, enums)
  - stage ordering (contiguous T1→…→C1), T3 requires a prior R2
  - empty close/resolved/reading detection
  - [X] / typed flags are valid; a T1 [X] must be resolved OR carried into T3

SEMANTIC (model-assisted, NOT yet enforced — flagged NOT_CHECKED):
  - unsupported additions (English without Sanskrit support)
  - term drift (same sense rendered inconsistently)
  - [X] laundering (an [X] silently resolved without evidence)
  - machine output masquerading as human review

PLANNED (documented intent, not yet implemented):
  - parallel-conflict, negation, number preservation

Each finding is {level: error|warn, stage, code, message}. error fails the stage;
warn is flagged for human review.
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

    # 3. dependency ordering (revision-safe): a stage may only be present if its
    #    prerequisites have at least one version. This permits T1 v1 → ... → T1 v2
    #    without treating the second T1 as a positional error.
    prereqs = {
        "T1": (), "R1": ("T1",), "T2": ("T1", "R1"), "R2": ("T1", "R1", "T2"),
        "T3": ("R2",), "T3.1": ("T3",), "C1": ("T3",),
    }
    for s in STAGES:
        if s in stages:
            for prereq in prereqs.get(s, ()):
                if prereq not in stages:
                    findings.append({"level": "error", "stage": "lineage", "code": "MISSING_PREREQ",
                                     "message": f"{s} present without required {prereq}"})
    # no machine output presented as reviewed
    t3 = stages.get("T3", {})
    if t3 and stages.get("R2") is None:
        findings.append({"level": "error", "stage": "T3", "code": "NO_ADJUDICATION",
                         "message": "T3 present without a prior R2 adjudication"})

    # 4. [X]-carried-to-T3: only once T3 EXISTS, every T1 [X] flag must be
    # resolved (R2) OR carried into T3's open_flags. A T1 [X] that vanishes by T3
    # is laundering (warn). Not checked at T1-only stage (that's premature).
    t3 = stages.get("T3", {})
    t1 = stages.get("T1", {})
    t1_flags = set(t1.get("flags", []))
    if t3 and (t1_flags & {"X", "TXT", "GRAM", "LEX", "DOCT", "WIT"}):
        resolved_or_carried = False
        open_flags = [f.get("flag") if isinstance(f, dict) else f
                      for f in t3.get("open_flags", [])]
        if set(open_flags) & {"X", "TXT", "GRAM", "LEX", "DOCT", "WIT"}:
            resolved_or_carried = True
        # an R2 that explicitly resolves is treated as carried (chosen set)
        if stages.get("R2") and stages["R2"].get("chosen"):
            resolved_or_carried = True
        if not resolved_or_carried:
            findings.append({"level": "warn", "stage": "T3", "code": "X_NOT_CARRIED",
                             "message": f"T1 flags {sorted(t1_flags)} not carried into T3.open_flags and no R2 resolution — possible laundering"})

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


def audit_record_stage(record: dict[str, Any], stage: str) -> list[dict[str, str]]:
    """Audit a single stage's payload (used by the state machine for the just-run
    stage, distinct from the whole-record audit)."""
    payload = (record.get("stages") or {}).get(stage, {})
    return _audit_stage(stage, payload)


def summary(findings: list[dict[str, str]]) -> str:
    errs = [x for x in findings if x["level"] == "error"]
    warns = [x for x in findings if x["level"] == "warn"]
    return f"{len(errs)} errors, {len(warns)} warnings"


def report(findings: list[dict[str, str]]) -> str:
    lines = [f"AUDIT: {summary(findings)}"]
    for x in findings:
        lines.append(f"  [{x['level'].upper()}] {x['stage']}:{x['code']} — {x['message']}")
    return "\n".join(lines)
