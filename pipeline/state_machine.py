"""Pāṭala state-machine driver — the "advance the work" engine.

The per-work stacked artifact IS the state. This driver implements the real
transaction the `translate-work` skill describes:

    LOAD → determine next admissible transition → construct evidence/context →
    execute ONE operation → validate → persist immutable version → reload.

It is NOT a rigid loop and NOT an in-memory demo. Every passage record is persisted
to `translations/_stack/{work}/passages/{locator}.json` and reloaded, so
`next_transition()` reflects what is actually on disk.

Transitions are gated on VALID PREREQUISITES, not mere stage presence:

    stage_state: ABSENT | PRESENT_INVALID | PRESENT_NEEDS_REVIEW | PRESENT_VALID

The three dimensions are scoped to VERSIONS/annotations:
    pipeline_stage  on the version being produced
    origin          on the version (machine/human)
    editorial_status on the version (proposed/reviewed/accepted — set only by a
                     scoped ReviewEvent on that target/version)
"""
from __future__ import annotations
import json
import os
import sys
from typing import Any, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from . import schema, prompts, model as model_mod
    from .audit import audit_record, audit_ok, audit_record_stage
    from .from_t1 import parse_t1_verse
    from .evidence import build_evidence_packet
except ImportError:
    import schema, prompts, model as model_mod
    from audit import audit_record, audit_ok, audit_record_stage
    from from_t1 import parse_t1_verse
    from evidence import build_evidence_packet

# The default flow ends at T3.1 (C1 is a separate commentary workflow).
DEFAULT_FLOW = ("T1", "R1", "T2", "R2", "T3", "T3.1")
STACK_ROOT = os.path.join("/root/projects/sanskritree/translations", "_stack")

# stage states
ABSENT = "absent"
INVALID = "present_invalid"
NEEDS_REVIEW = "present_needs_review"
VALID = "present_valid"

# stage prerequisites: {stage: (stages that must be VALID before it)}
PREREQS: dict[str, tuple[str, ...]] = {
    "T1": (),
    "R1": ("T1",),
    "T2": ("T1", "R1"),
    "R2": ("T1", "R1", "T2"),
    "T3": ("R2",),
    "T3.1": ("T3",),
    "C1": ("T3",),  # C1 is a separate workflow but depends on a resolved T3
}


# ── persistence ─────────────────────────────────────────────────────────────

def passage_dir(work_id: str) -> str:
    return os.path.join(STACK_ROOT, work_id, "passages")


def passage_path(work_id: str, locator: str) -> str:
    return os.path.join(passage_dir(work_id), f"{locator}.json")


def load_record(work_id: str, locator: str) -> Optional[dict]:
    p = passage_path(work_id, locator)
    if os.path.exists(p):
        try:
            return json.load(open(p, encoding="utf-8"))
        except Exception:
            return None
    return None


def save_record(record: dict) -> str:
    p = passage_path(record["work_id"], record["location"].get("locator", f"{record['location']['chapter']}.{record['location']['verse']}"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    return p


# ── stage state / transitions ───────────────────────────────────────────────

def stage_state(stages: dict[str, Any], audit: dict[str, Any], stage: str) -> str:
    """Classify a stage: ABSENT / PRESENT_INVALID / PRESENT_NEEDS_REVIEW / PRESENT_VALID.
    Uses the STAGE-LOCAL audit (audit.stage[stage]) so a warning from another stage
    does not contaminate this stage's eligibility."""
    if stage not in stages:
        return ABSENT
    # stage-local audit takes precedence; fall back to a flat `audit[stage]` for
    # records written before the stage/record split.
    stage_audit = audit.get("stage", {}).get(stage) or audit.get(stage, [])
    errs = [x for x in stage_audit if x.get("level") == "error"]
    warns = [x for x in stage_audit if x.get("level") == "warn"]
    if errs:
        return INVALID
    if warns:
        return NEEDS_REVIEW
    return VALID


def next_transition(record: dict, flow: tuple[str, ...] = DEFAULT_FLOW) -> dict:
    """Return the next admissible transition for a passage record.

    Returns: {stage, action, allowed, reason, state, blocked_by}.
      action: RUN (next missing stage) | RETRY (present but invalid → new version) |
              BLOCKED | COMPLETE
    """
    stages = record["stages"]
    audit = record["audit"]

    # An INVALID present stage is RETRYABLE as a new version (never a deadlock).
    for s in flow:
        st = stage_state(stages, audit, s)
        if st == INVALID:
            return {"stage": s, "action": "RETRY", "allowed": True,
                    "reason": f"current {s} version is invalid — retry as a new version",
                    "state": INVALID, "blocked_by": [s]}
        if st == ABSENT:
            # find this stage's unmet prerequisites (VALID or NEEDS_REVIEW both count
            # as "good enough to proceed" — a warning is a flag, not a blocker)
            missing = [p for p in PREREQS.get(s, ())
                       if stage_state(stages, audit, p) not in (VALID, NEEDS_REVIEW)]
            if missing:
                return {"stage": s, "action": "BLOCKED", "allowed": False,
                        "reason": f"{s} requires valid prerequisite(s) {missing}",
                        "state": ABSENT, "blocked_by": missing}
            return {"stage": s, "action": "RUN", "allowed": True,
                    "reason": f"{s} is the next stage",
                    "state": ABSENT, "blocked_by": []}

    return {"stage": None, "action": "COMPLETE", "allowed": True, "reason": "flow complete",
            "state": VALID, "blocked_by": []}


# ── building / hydrating a record ───────────────────────────────────────────

def new_verse(work_id: str, sanskrit: str, edition: str, source_id: str,
              locator: str, chapter: int, verse: int) -> dict:
    """Create a fresh passage record with a stable source identity."""
    return schema.new_passage(
        work_id=work_id,
        chapter=chapter,
        verse=verse,
        sanskrit=sanskrit,
        edition=edition,
        source_file=source_id,      # the provenance path/pointer
        source_id=source_id,        # the STABLE addressable source identity
        locator=locator,
    )


def _ensure_locator(rec: dict) -> dict:
    loc = rec["location"]
    loc.setdefault("locator", f"{loc['chapter']}.{loc['verse']}")
    return rec


# ── the atomic advance transaction ──────────────────────────────────────────

def advance_passage(work_id: str, locator: str,
                    sanskrit: str, edition: str, source_id: str,
                    chapter: int, verse: int,
                    flow: tuple[str, ...] = DEFAULT_FLOW,
                    model: str = model_mod.DEFAULT_MODEL,
                    created_by: str = "patala-agent",
                    require_structured: bool = True) -> dict:
    """LOAD → transition → RUN → VALIDATE → PERSIST → RELOAD for one passage.

    Returns a TransitionResult with the reloaded record + the audit + the next
    transition after persistence. The final reload proves durability.
    """
    # LOAD (or create fresh)
    rec = load_record(work_id, locator)
    if rec is None:
        rec = new_verse(work_id, sanskrit, edition, source_id, locator, chapter, verse)
    rec = _ensure_locator(rec)

    # determine the transition
    txn = next_transition(rec, flow)
    if not txn["allowed"]:
        return {"ok": False, "locator": locator, "reason": txn["reason"],
                "blocked_by": txn["blocked_by"], "record": rec,
                "next_transition": txn}

    stage = txn["stage"]
    if stage is None:
        # flow already complete — nothing to run
        return {"ok": True, "locator": locator, "stage": None,
                "reason": "flow complete", "path": None, "persisted_version": None,
                "audit_ok": True, "next_transition": txn, "record": rec}
    # RUN the one stage
    try:
        rec = run_floor(rec, stage, model=model, created_by=created_by,
                        source_id=source_id, require_structured=require_structured,
                        work_id=work_id)
    except model_mod.StageOutputError as e:
        return {"ok": False, "locator": locator, "stage": stage,
                "reason": f"invalid stage output: {e}", "blocked_by": [stage], "record": rec}

    # VALIDATE — stage-local audit (for this stage only) + whole-record audit,
    # stored separately so transition eligibility uses stage-local state.
    stage_findings = audit_record_stage(rec, stage)
    record_findings = audit_record(rec)
    rec["audit"].setdefault("stage", {})[stage] = stage_findings
    rec["audit"]["record"] = record_findings
    if not audit_ok(stage_findings):
        rec["_stage_error"] = {"stage": stage,
                               "errors": [x for x in stage_findings if x["level"] == "error"]}

    # PERSIST
    path = save_record(rec)

    # RELOAD (prove durability)
    reloaded = load_record(work_id, locator)
    next_after = next_transition(reloaded, flow) if reloaded else None

    return {
        "ok": not rec.get("_stage_error"),
        "locator": locator,
        "stage": stage,
        "path": path,
        "persisted_version": len(rec["versions"].get(stage, [])),
        "audit_ok": audit_ok(stage_findings),
        "next_transition": next_after,
        "record": reloaded or rec,
    }


# ── the batch orchestrator ──────────────────────────────────────────────────

def advance_work(work_id: str, source_texts: list[dict], edition: str, source_id: str,
                 flow: tuple[str, ...] = DEFAULT_FLOW,
                 model: str = model_mod.DEFAULT_MODEL,
                 created_by: str = "patala-agent",
                 require_structured: bool = True) -> dict:
    """Advance each verse of a work by exactly one transition. Thin orchestration
    over advance_passage; each call is a durable transaction."""
    report = {"work": work_id, "advanced": [], "blocked": [], "errors": []}
    for st in source_texts:
        res = advance_passage(work_id, st["locator"], st["sanskrit"], edition, source_id,
                              st["chapter"], st["verse"], flow, model, created_by,
                              require_structured)
        if res["ok"]:
            report["advanced"].append(st["locator"])
        elif res.get("blocked_by"):
            report["blocked"].append({st["locator"]: res["reason"]})
        else:
            report["errors"].append({st["locator"]: res["reason"]})
    report["summary"] = (f"advanced {len(report['advanced'])}, "
                         f"blocked {len(report['blocked'])}, errors {len(report['errors'])}")
    return report


# ── running one floor (structured, no silent prose fallback for core fields) ─

def run_floor(record: dict, stage: str, model: str = model_mod.DEFAULT_MODEL,
              created_by: str = "patala-agent", source_id: str = "",
              require_structured: bool = True, work_id: str = "") -> dict:
    """Run ONE stage with the house prompt + an EVIDENCE PACKET. Core stages
    (T1/R1/T2/R2) REQUIRE structured output; a prose fallback is an error."""
    system = prompts.STAGE_SYSTEM[stage]()
    packet = build_evidence_packet(record, work_id=work_id)
    user = prompts.user_prompt(stage, record, evidence_packet=packet)

    text = model_mod.chat(system, user, model=model, temperature=_TEMP(stage))
    payload = _make_payload(stage, text, require_structured=require_structured, model=model)
    schema.set_stage(record, payload, created_by=created_by,
                     derived_from=record["pipeline_stage"] if record["stages"] else None)
    return record


def _TEMP(stage: str) -> float:
    return {"T1": 0.3, "R1": 0.2, "T2": 0.4, "R2": 0.2,
            "T3": 0.3, "T3.1": 0.5, "C1": 0.5}.get(stage, 0.3)


def _make_payload(stage: str, text: str, require_structured: bool = True,
                  model: str = model_mod.DEFAULT_MODEL) -> dict:
    """Build the stage payload. FORMAT vs CONTRACT are distinct failures:

      FORMAT   — not parseable JSON            → one repair, else StageOutputError
      CONTRACT — parseable JSON but missing    → StageOutputError (rerun stage)
                 required substantive fields
    """
    from .contracts import validate_stage_contract, normalize_lean
    def repair(raw):
        # bounded: ask the model to re-emit ONLY the JSON object (format-only repair)
        return model_mod.chat(
            "You produce ONLY a valid JSON object. Return the JSON with no prose, "
            "no markdown fences, no commentary.",
            f"Here is malformed output. Re-emit it as a single valid JSON object:\n{raw}",
            model=model, temperature=0.0)
    if stage in ("T1", "R1", "T2", "R2", "T3"):
        try:
            obj = model_mod.parse_json(text, repair_fn=repair if require_structured else None)
        except Exception as e:
            if require_structured:
                raise model_mod.StageOutputError(f"{stage} must emit JSON: {e}")
            obj = {"_prose": text}
        # CONTRACT check: empty/{} output is INVALID, not silently accepted.
        # Map lean model fields to canonical schema fields FIRST so the contract
        # validates against canonical names (close_translation etc.), then check.
        obj = normalize_lean(stage, obj)
        problems = validate_stage_contract(stage, obj)
        if problems and require_structured:
            raise model_mod.StageOutputError(f"{stage} contract not met: {'; '.join(problems)}")
        return _payload_from_json(stage, obj, text)
    if stage == "T3.1":
        return schema.stage_T31(reading=text)
    if stage == "C1":
        # C1 is STRICT: interpretation + evidence_state + evidence + proposals + challenges
        try:
            obj = model_mod.parse_json(text, repair_fn=repair)
            return schema.stage_C1(
                interpretation=obj.get("interpretation", text),
                c1_id=obj.get("c1_id", ""),
                derived_from_t3=obj.get("derived_from_t3", ""),
                evidence_state=obj.get("evidence_state", "C1_EVIDENCE_PARTIAL"),
                evidence=obj.get("evidence", []),
                open_questions=obj.get("open_questions", []),
                proposals=obj.get("proposals", []),
                challenges=obj.get("challenges", []),
                cruxes=obj.get("cruxes", []),
            )
        except Exception as e:
            raise model_mod.StageOutputError(f"C1 must emit JSON: {e}")
    raise ValueError(f"unknown stage {stage}")


def _payload_from_json(stage: str, obj: dict, prose: str) -> dict:
    if stage == "T1":
        return schema.stage_T1(
            close=obj.get("close_translation", obj.get("_prose", prose)),
            reader_draft=obj.get("reader_draft", ""),
            flags=obj.get("flags", []),
            notes=obj.get("notes", []),
            lexical_decisions=obj.get("lexical_decisions", []),
            grammatical_notes=obj.get("grammatical_notes", []),
            time_place_context=obj.get("time_place_context", {}),
        )
    if stage == "R1":
        return schema.stage_R1(detail=obj.get("detail", prose),
                               cruxes=obj.get("cruxes", []),
                               verdicts=obj.get("verdicts", []))
    if stage == "T2":
        return schema.stage_T2(close=obj.get("close_translation", prose),
                               strategy=obj.get("strategy", "strongest-defensible-rival"),
                               rival_decisions=obj.get("rival_decisions", []),
                               constrained=obj.get("constrained", []))
    if stage == "R2":
        return schema.stage_R2(chosen=obj.get("chosen", prose),
                               reasoning=obj.get("reasoning", prose),
                               decisions=obj.get("decisions", []),
                               commentary=obj.get("commentary", ""),
                               hard_core=obj.get("hard_core", ""),
                               equal_alternates=obj.get("equal_alternates", []))
    if stage == "T3":
        return schema.stage_T3(resolved=obj.get("resolved", prose),
                               open_flags=obj.get("open_flags", []),
                               editorial_notes=obj.get("editorial_notes", []))
    raise ValueError(stage)


def _cli():
    import argparse
    ap = argparse.ArgumentParser(description="Pāṭala state-machine driver")
    ap.add_argument("work_id")
    ap.add_argument("--source", required=True, help="T1 markdown file to derive verses from")
    ap.add_argument("--edition", default="our T1")
    ap.add_argument("--source-id", default="pt:src:placeholder")
    ap.add_argument("--flow", default=",".join(DEFAULT_FLOW))
    ap.add_argument("--limit", type=int, default=1)
    args = ap.parse_args()
    verses = parse_t1_verse(open(args.source, encoding="utf-8").read())
    src = []
    for v in verses[: args.limit]:
        loc = v["id"].split(".")
        ch = int(loc[0]) if loc[0].isdigit() else 1
        vs = int(loc[1]) if len(loc) > 1 and loc[1].isdigit() else int(loc[0].lstrip("g"))
        src.append({"locator": v["id"], "chapter": ch, "verse": vs, "sanskrit": v["sanskrit"]})
    rep = advance_work(args.work_id, src, args.edition, args.source_id, tuple(args.flow.split(",")))
    print(json.dumps(rep, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    _cli()
