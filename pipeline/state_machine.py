"""Pāṭala state-machine driver — the "advance the work" engine.

The per-work stacked artifact IS the state. Given a work, this driver:
  1. loads the work's current floors (T1→T3.1, optionally C1)
  2. computes the NEXT missing floor for each passage
  3. runs that floor via the model (with the right prompt + context)
  4. audits the result; if invalid, flags it
  5. writes the floor + updates the work's AUDIT.md

It is NOT a rigid 7-stage loop — it advances state. The `translate-work` skill
drives it (and the agent can call it per floor, inspect, and iterate). This is the
"reference implementation" the skill follows.

FLOW:  bibliography → source → T1 → R1(cruxes) → T2(rival) → R2(decisions)
        → T3 → T3.1 → [C1 separate workflow] → AUDIT → structured claims feed back
"""
from __future__ import annotations
import json
import os
import sys
from typing import Any, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from . import schema, prompts, model as model_mod
    from .audit import audit_record, audit_ok
    from .from_t1 import parse_t1_verse
except ImportError:
    import schema, prompts, model as model_mod
    from audit import audit_record, audit_ok
    from from_t1 import parse_t1_verse

# The default flow ends at T3.1 (C1 is a separate commentary workflow).
DEFAULT_FLOW = ("T1", "R1", "T2", "R2", "T3", "T3.1")
STACK_ROOT = os.path.join("/root/projects/sanskritree/translations", "_stack")


# ── state inspection ────────────────────────────────────────────────────────

def next_missing(stages: dict[str, Any], flow: tuple[str, ...] = DEFAULT_FLOW) -> Optional[str]:
    """The first stage in the flow that has no recorded version."""
    for s in flow:
        if s not in stages:
            return s
    return None  # all flow stages done


def work_floor_state(work_id: str) -> dict[str, str]:
    """Read the work's AUDIT.md (if present) and return {floor: status}."""
    audit_path = os.path.join(STACK_ROOT, work_id, "AUDIT.md")
    state: dict[str, str] = {}
    if os.path.exists(audit_path):
        for line in open(audit_path, encoding="utf-8").read().splitlines():
            if "- floors:" in line:
                # "- floors: 00_source=pending, 01_t1=present, ..."
                for part in line.split(": ", 1)[-1].split(","):
                    part = part.strip()
                    if "=" in part:
                        k, v = part.split("=", 1)
                        state[k.strip()] = v.strip()
    return state


# ── building a record for one verse ─────────────────────────────────────────

def verse_to_record(work_id: str, sanskrit: str, edition: str, locator: str,
                    chapter: int, verse: int, existing_floors: Optional[dict] = None) -> dict:
    """Create (or hydrate) a passage record for one verse from the source."""
    rec = schema.new_passage(work_id, chapter, verse, sanskrit, edition, locator)
    # re-hydrate any existing floor payloads so we don't lose them
    for stage, payload in (existing_floors or {}).items():
        schema.set_stage(rec, dict(payload), created_by="agent",
                         derived_from=rec["pipeline_stage"] if rec["stages"] else None)
    return rec


# ── running one floor ───────────────────────────────────────────────────────

def run_floor(record: dict, stage: str, model: str = model_mod.DEFAULT_MODEL,
              created_by: str = "patala-agent") -> dict:
    """Run ONE stage of a record. Returns the updated record (audited)."""
    system = prompts.STAGE_SYSTEM[stage]()
    user = prompts.user_prompt(stage, record)

    text = model_mod.chat(system, user, model=model, temperature=_TEMP(stage))
    payload = _make_payload(stage, text, record)
    schema.set_stage(record, payload, created_by=created_by,
                     derived_from=record["pipeline_stage"] if record["stages"] else None)

    findings = audit_record(record)
    record["audit"][stage] = findings
    if not audit_ok(findings):
        errs = [f for f in findings if f["level"] == "error"]
        record["_stage_error"] = {"stage": stage, "errors": errs}
    return record


def _TEMP(stage: str) -> float:
    return {"T1": 0.3, "R1": 0.2, "T2": 0.4, "R2": 0.2,
            "T3": 0.3, "T3.1": 0.5, "C1": 0.5}.get(stage, 0.3)


def _make_payload(stage: str, text: str, record: dict) -> dict:
    """Build the stage payload from the model text (structured where the stage
    declares JSON, else the prose goes in the primary field)."""
    if stage == "T1":
        return schema.stage_T1(close=text)
    if stage == "R1":
        # prefer a crux list if the model returned JSON; else prose
        try:
            obj = model_mod.parse_json(text)
            return schema.stage_R1(detail=obj.get("detail", text),
                                   cruxes=obj.get("cruxes", []),
                                   verdicts=obj.get("verdicts", []))
        except Exception:
            return schema.stage_R1(detail=text)
    if stage == "T2":
        return schema.stage_T2(close=text, strategy="strongest-defensible-rival")
    if stage == "R2":
        try:
            obj = model_mod.parse_json(text)
            return schema.stage_R2(chosen=obj.get("chosen", text),
                                   reasoning=obj.get("reasoning", text),
                                   decisions=obj.get("decisions", []),
                                   commentary=obj.get("commentary", ""))
        except Exception:
            return schema.stage_R2(chosen=text, reasoning=text)
    if stage == "T3":
        return schema.stage_T3(resolved=text)
    if stage == "T3.1":
        return schema.stage_T31(reading=text)
    if stage == "C1":
        return schema.stage_C1(interpretation=text)
    raise ValueError(f"unknown stage {stage}")


# ── the primary entry point ────────────────────────────────────────────────

def advance_work(work_id: str, source_texts: list[dict], edition: str,
                 flow: tuple[str, ...] = DEFAULT_FLOW,
                 model: str = model_mod.DEFAULT_MODEL,
                 created_by: str = "patala-agent") -> dict:
    """Advance every verse of a work to the next missing floor. Returns a report.

    source_texts: [{locator, chapter, verse, sanskrit}] for the work.
    This is the batch driver the skill calls; for a single passage the agent can
    call run_floor directly instead.
    """
    report = {"work": work_id, "advanced": [], "errors": [], "skipped": []}
    for st in source_texts:
        rec = verse_to_record(work_id, st["sanskrit"], edition, st["locator"],
                              st["chapter"], st["verse"])
        stage = next_missing(rec["stages"], flow)
        if stage is None:
            report["skipped"].append(f"{st['locator']}: complete ({rec['pipeline_stage']})")
            continue
        rec = run_floor(rec, stage, model=model, created_by=created_by)
        if rec.get("_stage_error"):
            report["errors"].append({st["locator"]: rec["_stage_error"]})
        else:
            report["advanced"].append(st["locator"])
    report["summary"] = f"advanced {len(report['advanced'])}, skipped {len(report['skipped'])}, errors {len(report['errors'])}"
    return report


def _cli():
    import argparse
    ap = argparse.ArgumentParser(description="Pāṭala state-machine driver")
    ap.add_argument("work_id")
    ap.add_argument("--source", required=True, help="path to a T1 markdown file to derive verses from")
    ap.add_argument("--edition", default="our T1")
    ap.add_argument("--flow", default=",".join(DEFAULT_FLOW))
    ap.add_argument("--limit", type=int, default=1, help="max verses to advance this run")
    args = ap.parse_args()
    verses = parse_t1_verse(open(args.source, encoding="utf-8").read())
    source_texts = []
    for v in verses[: args.limit]:
        loc = v["id"].split(".")
        ch = int(loc[0]) if loc[0].isdigit() else 1
        vs = int(loc[1]) if len(loc) > 1 and loc[1].isdigit() else int(loc[0].lstrip("g"))
        source_texts.append({"locator": v["id"], "chapter": ch, "verse": vs, "sanskrit": v["sanskrit"]})
    rep = advance_work(args.work_id, source_texts, args.edition, tuple(args.flow.split(",")))
    print(json.dumps(rep, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    _cli()
