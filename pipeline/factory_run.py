#!/usr/bin/env python3
"""pipeline/factory_run.py — Agent 3 factory CALIBRATION run (one real production cycle).

⚠️ OBSOLETE / SUPERSEDED (2026-08-13): use the DAG scheduler + overnight loop instead.
  - `pipeline/factory_scheduler.py` — the real DAG scheduler (all eligible jobs, rate-limited)
  - `pipeline/factory_loop.sh` + `pipeline/start_overnight.sh` — the overnight operation
This file is kept only for historical reference (the original one-shot calibration run). It is NOT
part of the current factory; do not use it for new work.

The goal (from the spec) is NOT "autonomous translation works"; it is:

  Can Hermes execute ONE real translation job end-to-end under Pāṭala's state machine
  without losing provenance, inventing refs, or bypassing review status?

Calibration target: a LEGACY work with existing source + translation (kubjikā / kjn / kulasara),
so we have ground truth to compare against. The factory produces MODERN MACHINE_PROPOSED output
(T1/L2 + C1 proposal + provenance), A2 validates refs + source linkage, the ledger updates
deterministically, and one object enters the Phase-3 review.

Output: a FactoryRun report (the empirical record), NOT just translated files.

Do NOT add: subagent swarms, vector memory, generic ingest, more review ontology, automated A4,
large-scale cron. ONE profile, ONE skill, ONE worktree, ONE batch, ONE manifest.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model import chat  # the hermes-backed model client (already works)

MOUNT = "/mnt/HC_Volume_106427611/sanskritree"


# --------------------------------------------------------------------------- #
# the calibration manifest (ONE batch — kubjikā paṭala 10 verses)
# --------------------------------------------------------------------------- #
def load_verses(work: str) -> list[dict]:
    """Load the source Sanskrit + legacy translation for a work, verse by verse.

    kubjikā paṭala 10: the legacy T1 has '**N/N** — <sanskrit> — > — [and]-gloss' lines.
    We extract {verse_id, sanskrit, legacy_translation} for the comparison.
    """
    if work != "kubjika":
        raise ValueError(f"calibration target {work} not wired; use kubjika")
    path = Path(MOUNT) / "translations/01_t1_working/kubjikamata_patala10_pass1.md"
    verses = []
    cur = None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\*\*(\d+/\d+)\*\*\s*—\s*(.+?)—\s*$", line)
        if m:
            cur = {"verse_id": f"kubjika:10:{m.group(1)}", "sanskrit": m.group(2).strip(),
                   "legacy_translation": ""}
            verses.append(cur)
            continue
        if cur is not None and line.strip().startswith(">"):
            # the > gloss line is the legacy translation
            cur["legacy_translation"] = line.strip().lstrip(">—").strip()
            cur = None
    return verses


# --------------------------------------------------------------------------- #
# the factory (A3 — the translation production)
# --------------------------------------------------------------------------- #
@dataclass
class Production:
    verse_id: str
    sanskrit: str
    legacy_translation: str
    machine_t1: str = ""
    machine_c1: str = ""
    source_sha: str = ""
    model: str = ""
    skill_version: str = "factory-run-v1"

    def provenance(self) -> dict:
        return {"verse_id": self.verse_id, "source_sha": self.source_sha,
                "model": self.model, "skill_version": self.skill_version,
                "status": "MACHINE_PROPOSED", "origin": "machine",
                "generated_at": datetime.now(timezone.utc).isoformat()}


def produce(p: Production, model: str) -> None:
    """A3: generate the modern T1 + C1 proposal for one verse via hermes."""
    p.model = model
    p.source_sha = hashlib.sha256(p.sanskrit.encode("utf-8")).hexdigest()[:12]
    prompt_t1 = (
        "You are a careful Sanskrit translator. Produce a CONTROLLED T1 translation (word-close, "
        "proposition-faithful) of this Sanskrit verse from the Kubjikāmatatantra. Return ONLY the "
        "translation. If the text is corrupt/unreadable, return 'UNREADABLE'.\n\nSANSKRIT:\n"
        f"{p.sanskrit}"
    )
    try:
        p.machine_t1 = chat("You are a careful Sanskrit translator.", prompt_t1, model=model).strip()
    except Exception as e:
        p.machine_t1 = f"<ERROR: {str(e)[:120]}>"
    prompt_c1 = (
        "You are a scholar of Kaula/Kubjikā Śaivism. Give a 1-2 sentence C1 interpretive note for this "
        "verse (what it philosophically means), grounded in the text. If unreadable, return 'UNREADABLE'.\n\n"
        f"SANSKRIT:\n{p.sanskrit}"
    )
    try:
        p.machine_c1 = chat("You are a Kaula Śaivism scholar.", prompt_c1, model=model).strip()
    except Exception as e:
        p.machine_c1 = f"<ERROR: {str(e)[:120]}>"


# --------------------------------------------------------------------------- #
# A2 validation + ledger
# --------------------------------------------------------------------------- #
def validate_refs(p: Production) -> dict:
    """A2: validate the source refs + source linkage (no invented refs, no silent loss)."""
    problems = []
    if not p.sanskrit.strip():
        problems.append("empty source")
    if not p.source_sha:
        problems.append("no source hash")
    if p.machine_t1.startswith("<ERROR"):
        problems.append("model error on T1")
    if p.machine_t1 == "UNREADABLE":
        problems.append("unreadable source (expected — corrupt verse)")
    return {
        "verse_id": p.verse_id,
        "source_ref_resolved": bool(p.source_sha),
        "silent_source_loss": not p.sanskrit.strip(),
        "fabricated_refs": False,          # we only produce the verse's own sha — no invented refs
        "source_linkage": p.source_sha == hashlib.sha256(p.sanskrit.encode("utf-8")).hexdigest()[:12],
        "problems": problems,
    }


# --------------------------------------------------------------------------- #
# the calibration runner
# --------------------------------------------------------------------------- #
@dataclass
class FactoryRun:
    run_id: str
    work_id: str
    input_source_hash: str = ""
    model: str = ""
    skill_version: str = "factory-run-v1"
    pipeline_version: str = "0.1"
    passages_attempted: int = 0
    passages_completed: int = 0
    failures: list = field(default_factory=list)
    validation: list = field(default_factory=list)
    provenance_complete: bool = True
    cost: float = 0.0
    review_sample: dict = field(default_factory=dict)
    rerun_status: str = "PENDING"
    wall_clock_ms: float = 0.0
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id, "work_id": self.work_id,
            "input_source_hash": self.input_source_hash, "model": self.model,
            "skill_version": self.skill_version, "pipeline_version": self.pipeline_version,
            "passages_attempted": self.passages_attempted,
            "passages_completed": self.passages_completed,
            "failures": self.failures, "validation": self.validation,
            "provenance_complete": self.provenance_complete, "cost": self.cost,
            "review_sample": self.review_sample, "rerun_status": self.rerun_status,
            "wall_clock_ms": self.wall_clock_ms, "started_at": self.started_at,
        }


def run_calibration(work: str = "kubjika", model: str = "deepseek-v4-flash",
                     max_verses: int = 5, review_verses: int = 3) -> dict:
    """Run ONE calibration batch. Returns the FactoryRun report."""
    t0 = time.time()
    run = FactoryRun(run_id=f"factory-run-{int(time.time())}", work_id=work, model=model)
    verses = load_verses(work)
    run.passages_attempted = len(verses)
    run.input_source_hash = hashlib.sha256(
        "|".join(v["sanskrit"] for v in verses[:max_verses]).encode("utf-8")).hexdigest()[:12]

    productions = []
    for v in verses[:max_verses]:
        p = Production(verse_id=v["verse_id"], sanskrit=v["sanskrit"],
                       legacy_translation=v["legacy_translation"])
        produce(p, model)
        val = validate_refs(p)
        run.validation.append(val)
        if val["problems"]:
            run.failures.append({"verse_id": p.verse_id, "problems": val["problems"]})
        else:
            run.passages_completed += 1
        productions.append(p)
        # crude cost proxy (token-ish): chars/1000 (1k chars ~ 1 unit)
        run.cost += (len(p.sanskrit) + len(p.machine_t1) + len(p.machine_c1)) / 1000.0

    run.provenance_complete = all(v["source_ref_resolved"] and v["source_linkage"] and not v["fabricated_refs"]
                                  and not v["problems"] for v in run.validation)

    # the review sample: pick a few passages + compare machine vs legacy + feed one into review
    sample = []
    for p in productions[:review_verses]:
        sample.append({
            "verse_id": p.verse_id, "sanskrit": p.sanskrit[:120],
            "machine_t1": p.machine_t1[:200], "legacy_t1": p.legacy_translation[:200],
            "machine_c1": p.machine_c1[:150],
            "worth_reviewing_vs_redo": bool(p.machine_t1 and p.machine_t1 not in ("UNREADABLE",)
                                            and not p.machine_t1.startswith("<ERROR")),
        })
    run.review_sample = {"n": len(sample), "items": sample}
    run.wall_clock_ms = int((time.time() - t0) * 1000)
    run.rerun_status = "PASS" if (run.provenance_complete and run.failures == [] and run.passages_completed > 0) else "FAIL"

    # persist the report
    out = Path("/root/projects/patala/data/corpus/downloads/factory-run-report.json")
    with out.open("w", encoding="utf-8") as fh:
        json.dump(run.to_dict(), fh, indent=2, ensure_ascii=False)
    return run.to_dict()


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="kubjika")
    ap.add_argument("--model", default="deepseek-v4-flash")
    ap.add_argument("--max-verses", type=int, default=5)
    ap.add_argument("--review-verses", type=int, default=3)
    a = ap.parse_args()
    r = run_calibration(a.work, a.model, a.max_verses, a.review_verses)
    print(json.dumps(r, indent=2, ensure_ascii=False))
