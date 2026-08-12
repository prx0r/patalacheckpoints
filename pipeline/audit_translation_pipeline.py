#!/usr/bin/env python3
"""pipeline/audit_translation_pipeline.py — inventory the EXISTING T1/R1/T2 pipeline files.

These are the EASY WINS: works already translated (T1/R1/T2/R2/T3/C1) on disk. They should be
TRACKED and transformed into Pāṭala's required data structures — NOT queued for RAW-L0 from scratch.

This audit lists every work with pipeline files + which stages it has reached, and writes it as a
tracked inventory (data/corpus/downloads/translation-pipeline-inventory.json) distinct from the RAW-L0
translation-target queue.
"""
from __future__ import annotations

import json
import os
import re
from collections import defaultdict

MOUNT = "/mnt/HC_Volume_106427611/sanskritree"
T = os.path.join(MOUNT, "translations")
STAGES = ["01_t1_working", "02_r1_review", "03_t2_alternate", "04_r2_adjudication",
          "05_t3_final", "06_c1_interpretation"]
STAGE_NAMES = {"01_t1_working": "T1", "02_r1_review": "R1", "03_t2_alternate": "T2",
               "04_r2_adjudication": "R2", "05_t3_final": "T3", "06_c1_interpretation": "C1"}
# leading stage prefixes to strip
PREFIX = re.compile(r"^(t3_1_|t3_|c1_|p2_|p3_|r1_|r2_|p_)")


def work_of(fname: str) -> str:
    name = PREFIX.sub("", fname.replace(".md", ""))
    m = re.match(r"^([a-z0-9]+)", name)
    return m.group(1) if m else name


def audit() -> dict:
    works = defaultdict(lambda: defaultdict(int))
    for stage in STAGES:
        d = os.path.join(T, stage)
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if not f.endswith(".md"):
                continue
            w = work_of(f)
            works[w][STAGE_NAMES[stage]] += 1
    # build the inventory
    inventory = {}
    for w, stages in sorted(works.items(), key=lambda x: -sum(x[1].values())):
        reached = [s for s in ["T1", "R1", "T2", "R2", "T3", "C1"] if stages.get(s)]
        deepest = reached[-1] if reached else None
        inventory[w] = {
            "work": w, "n_files": sum(stages.values()),
            "stages": dict(stages), "deepest_stage": deepest,
            "track": True,  # already translated — track, don't RAW-L0-from-scratch queue
        }
    return {"note": "existing T1/R1/T2/R2/T3/C1 pipeline files — EASY WINS, tracked not queued",
            "works": inventory, "n_works": len(inventory)}


if __name__ == "__main__":
    res = audit()
    out = "/root/projects/patala/data/corpus/downloads/translation-pipeline-inventory.json"
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2, ensure_ascii=False)
    print(f"works with pipeline files: {res['n_works']}")
    for w, meta in sorted(res["works"].items(), key=lambda x: -x[1]["n_files"])[:40]:
        print(f"  {w:<26} {meta['n_files']:>3} | deepest={meta['deepest_stage']} | {meta['stages']}")
    print(f"\nwrote {out}")
