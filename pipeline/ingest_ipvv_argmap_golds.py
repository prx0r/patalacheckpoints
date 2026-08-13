#!/usr/bin/env python3
"""pipeline/ingest_ipvv_argmap_golds.py — ingest the 51 real IPVV ARGMAP golds as production objects.

The real bottleneck: the factory has produced only 1 committed ARGMAP (kramasadbhava:v1), while there
are 51 hand-authored, scholar-grade IPVV argument-map golds (pilot_V*_ARGUMENT_MAP.md) that ARE the
gold standard. This ingests all 51 as committed canonical ARGMAP objects (MACHINE_PROPOSED, golden
provenance) so the essay/education layers have real, varied arguments to project.

Each gold is a structured markdown with the canonical 4 sections:
    ## 1. What is at issue   -> what_is_at_issue
    ## 2. The argument...    -> argument_steps (kārikā-by-kārikā)
    ## 3. Unresolved / uncertain -> open_items
    ## 4. Decision for L2    -> decision_for_l2

Registration uses the same immutable argmap-registry + ObjectEvent ledger as the factory, so these golds
become first-class objects with provenance (no fabricated provenance). They are flagged
status=GOLDEN_INGESTED / argmap_status=MACHINE_PROPOSED — review axis NOT_HUMAN_REVIEWED.

Usage:
    python3 pipeline/ingest_ipvv_argmap_golds.py [--dry-run]
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, "/root/projects/patala/pipeline")
import object_registry as R  # noqa: E402

GOLD_DIR = "/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/pilot"
OUT = "/root/projects/patala/data/corpus/registries/argmap-registry.jsonl"


def _sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _object_id_from_gold(path: str) -> str:
    """pilot_V2L_ARGUMENT_MAP.md -> ipvv:V2L  (canonical passage id)."""
    base = os.path.basename(path)                      # pilot_V2L_ARGUMENT_MAP.md
    m = re.match(r"pilot_(V\d+[A-Z]+(?:_[A-Za-z0-9]+)?)_ARGUMENT_MAP", base)
    if not m:
        m = re.match(r"pilot_([A-Za-z0-9_]+)_ARGUMENT_MAP", base)
    tag = m.group(1) if m else os.path.basename(path).replace("_ARGUMENT_MAP.md", "")
    # strip the suffix marker if present (e.g. V3B_K6 -> V3B) to keep the passage id canonical
    passage = re.match(r"(V\d+[A-Z]+)", tag)
    return f"ipvv:{passage.group(1) if passage else tag}"


def parse_gold(path: str) -> dict:
    """Parse one gold markdown into the canonical 4-section argument_map."""
    text = open(path, encoding="utf-8").read()
    lines = text.splitlines()

    def section(heading_re):
        out = []
        on = False
        for ln in lines:
            if re.match(heading_re, ln):
                on = True
                continue
            if on:
                if re.match(r"^#+ ", ln):   # a new section heading
                    break
                s = ln.strip()
                if s:
                    out.append(s)
        return "\n".join(out).strip()

    what = section(r"^##\s*1\.\s*What is at issue")
    arg = section(r"^##\s*2\.\s*The argument")
    opensec = section(r"^##\s*3\.\s*(Unresolved|Open|Uncertain)")
    decision = section(r"^##\s*4\.\s*Decision for L2")

    # argument_steps: split the argument section on kārikā markers (each becomes a step)
    steps = []
    for chunk in re.split(r"\n\s*\*{0,2}Kārikā\s*\d+", "\n"+arg):
        c = " ".join(chunk.split()).strip()
        if c:
            steps.append(c)
    if not steps and arg:
        steps = [arg[:400]]

    # open_items: parse the numbered/bulleted unresolved items
    open_items = []
    for ln in opensec.splitlines() if opensec else []:
        s = ln.strip().lstrip("0123456789.·- \t")
        if s and len(s) > 15:
            open_items.append({"text": s, "status": "OPEN"})
    if not open_items:
        open_items = [{"text": (opensec[:400] if opensec else ""), "status": "OPEN"}] if opensec else []

    return {
        "what_is_at_issue": what,
        "argument_steps": steps,
        "open_items": open_items,
        "decision_for_l2": decision,
        "_gold_file": os.path.basename(path),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()

    golds = sorted(glob.glob(os.path.join(GOLD_DIR, "*_ARGUMENT_MAP.md")))
    if a.limit:
        golds = golds[: a.limit]

    ingested = 0
    skipped = 0
    for path in golds:
        oid = _object_id_from_gold(path)
        parsed = parse_gold(path)
        if not parsed["what_is_at_issue"] or not parsed["argument_steps"]:
            print(f"  SKIP {oid}: missing sections")
            skipped += 1
            continue
        # if already committed, skip (idempotent)
        if R.current("ARGMAP", oid):
            skipped += 1
            continue
        payload = {
            "argument_map": {
                "what_is_at_issue": parsed["what_is_at_issue"],
                "argument_steps": parsed["argument_steps"],
                "open_items": parsed["open_items"],
                "decision_for_l2": parsed["decision_for_l2"],
            },
            "gold_provenance": {"source": "ipvv-pilot-gold", "file": parsed["_gold_file"]},
        }
        if a.dry_run:
            print(f"  [dry-run] would commit ARGMAP {oid} ({len(parsed['argument_steps'])} steps)")
            ingested += 1
            continue
        R.commit("ARGMAP", oid, _sha256(parsed), created_by="ipvv-gold-ingest",
                 status="GOLDEN_INGESTED", payload=payload,
                 input_refs=[f"pt:passage:ipvv:{oid.split(':')[1]}"])
        ingested += 1

    print(f"IPVV ARGMAP gold ingest: {ingested} committed, {skipped} skipped (already present/unparseable), "
          f"total golds={len(golds)}")
    if a.dry_run:
        print("(dry-run — no changes written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
