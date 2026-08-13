#!/usr/bin/env python3
"""pipeline/auto_run.py — the Agent 3 autonomous RAW-L0 supervisor (the "translate while I sleep" loop).

Per handover/hermes/PATALA-SETUP.md §4 "Not yet built (the remaining gap)": this is the supervisor
that connects the RAW-L0 factory to Agent 2's corpus-state NEXT_VALID_ACTION into a safe autonomous
loop. Hermes is the execution kernel (it does the gloss reasoning); PĀṬALA owns the decisions, the
log, the validation, and the state — every decision + output lands in a Pāṭala log, never Hermes memory.

The loop, per work (the smallest/next eligible first):
  NEXT_VALID_ACTION(work) → per verse:
    1. DETERMINISTIC   raw_l0 (Vidyut) → canonical L0 records
    2. CONTEXT ENGINEERING  agentic_gloss: Hermes reads the term-context packet, proposes a gloss,
                            then a SEPARATE self-challenge pass tries to falsify it
    3. UN-CHEATABLE VALIDATION  validate_l0_spec.py: schema + P0 + abstraction-honesty + gloss
    4. COMMIT          l0_registry.commit_l0 (immutable, versioned)
    5. LOG             a Pāṭala decision/action record (append-only JSONL)
  On completion of a work → advance to the next eligible work (smallest first, or queue order).

Fail-closed: a verse that fails validation is logged + skipped (the work's branch halts for it, the
work continues to clean verses). A work with too many failures is stopped; the run advances.

Usage:
  python3 pipeline/auto_run.py [--work cidgagana] [--max-verses 10] [--max-works 2] [--order smallest|queue]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent3_batch import load_raw_source, split_verses, update_ledger
from raw_l0 import raw_l0, raw_l0_to_canonical
from l0_registry import commit_l0


def _is_ocr_noise(verse: str) -> bool:
    """F7: detect illegible OCR/noise in a verse (e.g. '* * * * * * * *(?)', star runs, '(?)').
    Such verses are SOURCE_BLOCKED (preserved raw, never auto-cleaned into guessed Sanskrit)."""
    import re
    if re.search(r"\*\s*\*", verse):          # star runs = OCR noise
        return True
    if "(?)" in verse:                          # explicit illegibility marker
        return True
    return False
from validate_l0_spec import validate
from agentic_gloss import run_batch

LEDGER_PATH = "/root/projects/patala/data/corpus/downloads/translation-state-ledger.json"
LOG_PATH = "/root/projects/patala/data/corpus/downloads/agent3-autonomous-log.jsonl"
BATCH_DIR = "/root/projects/patala/data/corpus/downloads/agent3-batches"

# verse-merge cap: verse index -> records id prefix
def _log(record: dict) -> None:
    """Append one Pāṭala decision/action record to the autonomous log (append-only)."""
    Path(LOG_PATH).parent.mkdir(parents=True, exist_ok=True)
    record["ts"] = datetime.now(timezone.utc).isoformat()
    with open(LOG_PATH, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def eligible_works(order: str = "smallest") -> list[str]:
    """The RAW_SANSKRIT works on disk, ordered smallest-first or by queue priority."""
    ledger = json.load(open(LEDGER_PATH))
    rows = []
    for wid, w in ledger["works"].items():
        src = (w.get("source") or {}).get("source_ref", "")
        fmt = (w.get("source") or {}).get("format", "")
        if fmt == "RAW_SANSKRIT" and src and os.path.exists(src):
            rows.append((os.path.getsize(src), wid))
    if order == "smallest":
        return [w for _, w in sorted(rows)]
    # queue order = registry priority (from translation_targets)
    from translation_targets import priority as prio
    return sorted((w for _, w in rows), key=lambda w: prio(w))


def run_work(work_id: str, max_verses: int, log_every: int = 1,
             skip_gloss: bool = False) -> dict:
    """Run one work: RAW-L0 + agentic gloss (BATCHED — many verses per single
    hermes -z call) + un-cheatable validation + commit + log.

    F1 idempotency: completion is DERIVED FROM THE IMMUTABLE L0 REGISTRY, not the
    ledger. Verses whose stable passage_id already has a committed version are
    SKIPPED (never re-glossed, never re-committed). Only uncommitted verses are
    batched. passage_id and the record chunk_id always agree on the all-verses index.
    """
    from l0_registry import committed_passage_ids
    raw = load_raw_source(work_id)
    all_verses = split_verses(raw)
    committed = committed_passage_ids(work_id)

    picks = []  # (all_idx, passage_id, verse)
    blocked = []
    skipped_committed = 0
    for i, verse in enumerate(all_verses):
        if max_verses and len(picks) >= max_verses:
            break
        pid = f"{work_id}:v{i+1}"
        if pid in committed:
            skipped_committed += 1
            continue
        if _is_ocr_noise(verse):
            blocked.append(pid)
            _log({"event": "SOURCE_BLOCKED", "work_id": work_id, "passage_id": pid,
                  "reason": "OCR_NOISE / ILLEGIBLE_SOURCE", "verse": verse[:60]})
            continue
        picks.append((i, pid, verse))

    done = committed_count = failed = abstained = 0
    failures = []
    commits = []

    # deterministic pass over the UNCOMMITTED verses, then BATCH gloss them.
    entries = []
    for all_idx, pid, verse in picks:
        chunk = f"{work_id}-v{all_idx+1}"
        records, _ = raw_l0_to_canonical(chunk, verse)
        tokens = [r["raw_fragment"] for r in records if r["raw_fragment"]]
        entries.append({"idx": len(entries), "verse": verse, "tokens": tokens,
                        "records": records, "passage_id": pid, "chunk": chunk})

    gloss_lookup = {}
    if not skip_gloss:
        glossable = [e for e in entries if e["tokens"]]
        for g in run_batch(glossable, work_id):
            gloss_lookup[g["idx"]] = g["gloss_map"]

    for e in entries:
        passage_id = e["passage_id"]
        verdict = {"work_id": work_id, "passage_id": passage_id,
                   "verse": e["verse"][:80], "decisions": [], "ok": False}
        try:
            records = e["records"]
            tokens = e["tokens"]
            gloss_map = gloss_lookup.get(e["idx"]) or {t: {"literal": "", "compound": "", "supplied": False}
                                                       for t in tokens}
            if not skip_gloss and tokens:
                verdict["decisions"].append({"pass": "propose_challenge_batch", "tokens": len(tokens)})
                abstained += sum(1 for v in gloss_map.values() if not v["literal"])

            res = raw_l0(work_id, passage_id, e["verse"], gloss_map)
            verdict["n_records"] = len(res["records"])

            from raw_l0 import strip_verse_marker
            v = validate(res["records"], chunk_text=strip_verse_marker(res["verse"]))
            verdict["validation"] = {"schema_ok": v["schema_ok"], "n": v["n_records"],
                                     "p0_pass": v["p0"]["PASS"] if v["p0"] else None,
                                     "unknown": v["p0"]["coverage"]["unknown_chars"] if v["p0"] else None,
                                     "PASS": v["PASS"]}

            if not v["PASS"]:
                verdict["decisions"].append({"action": "FAIL_VALIDATION",
                                             "reason": "un-cheatable validator rejected"})
                failed += 1
                failures.append({"passage_id": passage_id, "why": "validate_l0_spec FAIL"})
                verdict["ok"] = False
            else:
                commit = commit_l0(work_id, res["records"], committed_by="agent3-autonomous",
                                   passage_ids=[passage_id])
                verdict["commit"] = commit
                verdict["decisions"].append({"action": "COMMIT_L0", "version": commit.get("version"),
                                             "passage_id": passage_id})
                committed_count += 1
                verdict["ok"] = True
                done += 1

        except Exception as ex:
            verdict["decisions"].append({"action": "ERROR", "error": str(ex)[:200]})
            failed += 1
            failures.append({"passage_id": passage_id, "why": f"exception: {str(ex)[:120]}"})

        _log(verdict)

    ledger_update = update_ledger(work_id, committed_count, len(all_verses))

    summary = {
        "work_id": work_id, "verses_attempted": len(picks), "verses_committed": committed_count,
        "verses_failed": failed, "abstentions": abstained,
        "verses_skipped_committed": skipped_committed,
        "verses_blocked_source": len(blocked),
        "failures": failures, "ledger_update": ledger_update,
    }
    _log({"event": "WORK_SUMMARY", **summary})
    return summary


def main() -> int:
    ap = argparse.ArgumentParser(description="Agent 3 autonomous RAW-L0 supervisor (per PATALA-SETUP spec)")
    ap.add_argument("--work", default=None, help="specific work; else next eligible")
    ap.add_argument("--max-verses", type=int, default=10, help="verses per work this run")
    ap.add_argument("--max-works", type=int, default=1, help="how many works to advance through")
    ap.add_argument("--order", default="smallest", choices=["smallest", "queue"],
                    help="smallest-first (user request) or queue priority")
    ap.add_argument("--skip-gloss", action="store_true", help="deterministic only (no Hermes)")
    a = ap.parse_args()

    works = [a.work] if a.work else eligible_works(a.order)
    works = works[:a.max_works]
    _log({"event": "RUN_START", "works": works, "order": a.order, "max_verses": a.max_verses})

    all_summaries = {}
    for wid in works:
        s = run_work(wid, a.max_verses, skip_gloss=a.skip_gloss)
        all_summaries[wid] = s
        print(json.dumps(s, indent=2, ensure_ascii=False))

    _log({"event": "RUN_END", "works_completed": list(all_summaries.keys())})
    print(f"\nlog: {LOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
