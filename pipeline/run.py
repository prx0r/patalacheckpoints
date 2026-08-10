"""Pāṭala pipeline orchestrator.

Drives a text through the full flow (per corpus/targets/translation_flow_spec.md):

    T1 → R1 → T2 → R2 → T3 → T3.1 → C1

Design:
- T1 is the working translation.
- R1 is the intimate peer review of T1 (verdicts + commentary stubs).
- T2 is a complete ALTERNATIVE that actively opposes T1 (informed by R1).
- R2 is the synthesis: hard-core / divergence / adjudication / readability /
  school-context / expanded commentary / equal alternates / OPEN.
- T3 is the final resolved text; T3.1 the reading layer (same call as T3).
- C1 is the plain-English commentary (may overturn T3).
- Every stage is audited (audit.py). The whole thing builds the commentary.

The pipeline is standalone: it reads source Sanskrit from a file, calls the model,
and writes structured per-passage JSON records. No API dependency.
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from typing import Any, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from schema import (  # noqa: E402
    new_passage, set_stage, stage_T1, stage_R1, stage_T2, stage_R2,
    stage_T3, stage_T31, stage_C1,
)
from audit import audit_record, audit_ok, report  # noqa: E402
import prompts  # noqa: E402
import model as model_mod  # noqa: E402

# The review stages run as separate, independent calls (they are adversarial).
# Generation (T1, T3+T3.1) can be batched; here we keep it simple and auditable.
REVIEW_STAGES = ("R1", "R2", "C1")


def run_stage(record: dict[str, Any], stage: str, model: str,
              created_by: str) -> dict[str, Any]:
    """Run one stage by calling the model with the house prompt, then store+audit."""
    system = prompts.STAGE_SYSTEM[stage]()
    user = prompts.user_prompt(stage, record)

    if stage == "T1":
        text = model_mod.chat(system, user, model=model, temperature=0.3)
        payload = stage_T1(close=text)
    elif stage == "R1":
        text = model_mod.chat(system, user, model=model, temperature=0.2)
        payload = stage_R1(detail=text, source=record["source"]["source_edition"])
    elif stage == "T2":
        text = model_mod.chat(system, user, model=model, temperature=0.4)
        payload = stage_T2(close=text, strategy="oppose-T1-informed-by-R1")
    elif stage == "R2":
        text = model_mod.chat(system, user, model=model, temperature=0.2)
        payload = stage_R2(chosen=text, reasoning=text, commentary=text)
    elif stage == "T3":
        text = model_mod.chat(system, user, model=model, temperature=0.3)
        payload = stage_T3(resolved=text)
    elif stage == "T3.1":
        text = model_mod.chat(system, user, model=model, temperature=0.5)
        payload = stage_T31(reading=text)
    elif stage == "C1":
        text = model_mod.chat(system, user, model=model, temperature=0.5)
        payload = stage_C1(interpretation=text)
    else:
        raise ValueError(f"unknown stage {stage}")

    set_stage(record, payload, created_by=created_by,
              derived_from=record["pipeline_stage"] if record["stages"] else None)

    # audit the record after this stage
    findings = audit_record(record)
    record["audit"][stage] = findings
    if not audit_ok(findings):
        print(f"  !! AUDIT FAIL at {stage}:\n{report(findings)}")
    else:
        warns = [x for x in findings if x["level"] == "warn"]
        if warns:
            print(f"  (~) {stage}: {len(warns)} warnings")
    return record


def run_text(source_file: str, work_id: str, edition: str,
             chapter: int, verse: int,
             model: str = model_mod.DEFAULT_MODEL,
             stages: tuple[str, ...] = ("T1", "R1", "T2", "R2", "T3", "T3.1", "C1"),
             created_by: str = "patala-pipeline") -> dict[str, Any]:
    """Run the flow on a single verse read from source_file (line `verse`)."""
    lines = open(source_file, encoding="utf-8").read().splitlines()
    line = lines[verse - 1] if verse <= len(lines) else ""
    if not line.strip():
        raise ValueError(f"no text on line {verse} of {source_file}")

    record = new_passage(work_id, chapter, verse, line.strip(), edition, source_file)
    for stage in stages:
        print(f"  → {stage}")
        record = run_stage(record, stage, model, created_by)
    return record


def main() -> None:
    ap = argparse.ArgumentParser(description="Pāṭala translation pipeline")
    ap.add_argument("source", help="path to the Sanskrit source file")
    ap.add_argument("work_id")
    ap.add_argument("--edition", default="our T1")
    ap.add_argument("--chapter", type=int, default=1)
    ap.add_argument("--verse", type=int, required=True, help="line number (verse) to translate")
    ap.add_argument("--model", default=model_mod.DEFAULT_MODEL)
    ap.add_argument("--stages", default="T1,R1,T2,R2,T3,T3.1,C1",
                    help="comma-separated stages")
    ap.add_argument("--out", required=True, help="output json path")
    ap.add_argument("--created-by", default="patala-pipeline")
    args = ap.parse_args()

    stages = tuple(s.strip() for s in args.stages.split(","))
    record = run_text(args.source, args.work_id, args.edition,
                      args.chapter, args.verse, args.model, stages, args.created_by)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    final = audit_record(record)
    print(f"\nWROTE {args.out}")
    print(f"FINAL AUDIT: {len([x for x in final if x['level']=='error'])} errors, "
          f"{len([x for x in final if x['level']=='warn'])} warnings")


if __name__ == "__main__":
    main()
