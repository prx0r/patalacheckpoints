#!/usr/bin/env python3
"""pipeline/corpus_state.py — Agent 2's core object: the translation-state ledger + transition contract.

Agent 2 = the corpus compiler / integrity layer. It does NOT generate translations; it maintains the
canonical machine-readable state that Agent 3 (the translation factory) consumes.

This module computes, for every work, its source/translation/L0/proof/review/factory state from ACTUAL
disk truth (the flat corpus + the _stack + sources/) + the bibliography (data/atlas) + the acquisition
manifest. It exposes:

  NEXT_VALID_ACTION(work)   — the single next valid transition (the control plane for Agent 3)
  ledger()                  — the full per-work state ledger
  eligible_for_agent3(work) — is it safe for Agent 3 to act on now?

The output contract is invariant across input formats:
  source -> [adapter] -> canonical L0   (adapter depends on source format; contract does not)

Modes (per the design):
  MODE_A  AND_GLOSS       the legacy [and]-apparatus format (IPVV / V1 / legacy T1) -> current extractor
  MODE_B  RAW_SANSKRIT    a raw Sanskrit source (kramasadbhava etc.) -> source-Sanskrit L0 mode (NOT YET BUILT)
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

MOUNT = "/mnt/HC_Volume_106427611/sanskritree"

# --------------------------------------------------------------------------- #
# source-format detection
# --------------------------------------------------------------------------- #
def detect_source_format(text: str) -> str:
    """Classify a source text as AND_GLOSS or RAW_SANSKRIT.

    AND_GLOSS  has '[and]-GLOSS (IAST)' markers (extractable by the current extractor).
    RAW_SANSKRIT is raw Sanskrit verses — in IAST or Devanagari script — needing the
    source-Sanskrit L0 mode (the factory's translation workers pass it to the model directly).
    """
    if "[and]-" in text:
        return "AND_GLOSS"
    # raw Sanskrit: IAST diacritics OR Devanagari block, few English words
    iast = len(re.findall(r"[āīūṛṝḷḹṃñṅśṣṭḍḥṁ]", text))
    deva = len(re.findall(r"[\u0900-\u097F]", text))
    if iast > 20 or deva > 20:
        return "RAW_SANSKRIT"
    return "UNKNOWN"


# --------------------------------------------------------------------------- #
# per-work state (computed, not asserted)
# --------------------------------------------------------------------------- #
@dataclass
class WorkState:
    work_id: str
    bibliographic_id: str | None = None
    source_available: bool = False
    source_format: str = "UNKNOWN"
    source_ref: str | None = None
    edition_ref: str | None = None
    t1: str = "NOT_STARTED"       # NOT_STARTED | LEGACY_PRESENT | MODERN_PRESENT | PARTIAL
    l2: str = "NOT_STARTED"
    c1: str = "NOT_STARTED"
    l0_status: str = "NOT_STARTED"  # NOT_STARTED | ELIGIBLE | VERIFIED | BLOCKED
    l0_reason: str | None = None
    proof_status: str = "NONE"       # NONE | FROZEN | STALE | PARTIAL
    review_status: str = "UNREVIEWED"  # UNREVIEWED | MACHINE_PROPOSED | REVIEWED | ADJUDICATED
    provenance: str | None = None

    def to_dict(self) -> dict:
        return {
            "work_id": self.work_id,
            "bibliographic_id": self.bibliographic_id,
            "source": {
                "available": self.source_available,
                "format": self.source_format,
                "source_ref": self.source_ref,
                "edition_ref": self.edition_ref,
            },
            "translation": {"t1": self.t1, "l2": self.l2, "c1": self.c1},
            "l0": {"status": self.l0_status, "reason": self.l0_reason},
            "proof": {"status": self.proof_status},
            "review": {"status": self.review_status},
            "provenance": self.provenance,
        }


# --------------------------------------------------------------------------- #
# the transition contract (the state machine Agent 3 consumes)
# --------------------------------------------------------------------------- #
def next_valid_action(s: WorkState) -> dict:
    """The single next valid transition for a work. This is Agent 3's control plane.

    The state machine (from the Agent 2 design):
      MISSING_SOURCE          -> ACQUIRE_SOURCE
      RAW_SOURCE              -> BUILD_L0_SOURCE_MODE   (blocked until MODE_B is built)
      LEGACY_T1_PRESENT       -> MODERNIZE_L0
      L0_VALID                -> GENERATE_TRANSLATION
      TRANSLATION_PROPOSED    -> RUN_QA
      QA_PASS                 -> GENERATE_C1
      C1_PROPOSED             -> WAIT_FOR_REVIEW
    """
    if not s.source_available and s.l0_status != "VERIFIED":
        return {"action": "ACQUIRE_SOURCE", "eligible_for_agent3": False,
                "reason": "MISSING_SOURCE"}
    if s.source_format == "RAW_SANSKRIT" and s.l0_status != "VERIFIED":
        return {"action": "BUILD_L0_SOURCE_MODE", "eligible_for_agent3": False,
                "reason": "RAW_SANSKRIT_L0_MODE_REQUIRED", "blocked": True}
    # source is present (either marked available, or L0 already VERIFIED implies it exists)
    if s.l0_status == "VERIFIED":
        if s.t1 in ("NOT_STARTED", "LEGACY_PRESENT"):
            return {"action": "GENERATE_TRANSLATION", "eligible_for_agent3": True,
                    "reason": "L0_VALID -> GENERATE_TRANSLATION"}
        if s.c1 == "NOT_STARTED":
            return {"action": "GENERATE_C1", "eligible_for_agent3": True,
                    "reason": "TRANSLATION_PROPOSED -> GENERATE_C1"}
        return {"action": "WAIT_FOR_REVIEW", "eligible_for_agent3": False,
                "reason": "C1_PROPOSED -> WAIT_FOR_REVIEW"}
    if s.source_format == "AND_GLOSS":
        if s.l0_status != "VERIFIED":
            return {"action": "MODERNIZE_L0", "eligible_for_agent3": True,
                    "reason": "LEGACY_T1_PRESENT -> MODERNIZE_L0"}
        if s.t1 in ("NOT_STARTED", "LEGACY_PRESENT"):
            return {"action": "GENERATE_TRANSLATION", "eligible_for_agent3": True,
                    "reason": "L0_VALID -> GENERATE_TRANSLATION"}
        if s.c1 == "NOT_STARTED":
            return {"action": "GENERATE_C1", "eligible_for_agent3": True,
                    "reason": "TRANSLATION_PROPOSED -> GENERATE_C1"}
        return {"action": "WAIT_FOR_REVIEW", "eligible_for_agent3": False,
                "reason": "C1_PROPOSED -> WAIT_FOR_REVIEW"}
    return {"action": "CLASSIFY_SOURCE", "eligible_for_agent3": False,
            "reason": f"UNKNOWN_SOURCE_FORMAT {s.source_format}"}


# --------------------------------------------------------------------------- #
# disk-truth discovery
# --------------------------------------------------------------------------- #
def discover_works() -> list[WorkState]:
    """Compute work state from actual on-disk files + bibliography + manifest."""
    works = {}

    # 1. the _stack works
    stack = Path(MOUNT) / "translations" / "_stack"
    for w in sorted(os.listdir(stack)):
        if not (stack / w).is_dir():
            continue
        works.setdefault(w, WorkState(work_id=w))
        # L0 jsonl present?
        l0f = list((stack / w).glob("*.l0.jsonl")) + list((stack / w).glob("**/*.l0.jsonl"))
        if l0f:
            works[w].l0_status = "VERIFIED"
            works[w].proof_status = "FROZEN"

    # 2. the flat translation corpus (01_t1_working, 05_t3_final, 06_c1_interpretation)
    flat_t1 = Path(MOUNT) / "translations" / "01_t1_working"
    flat_t3 = Path(MOUNT) / "translations" / "05_t3_final"
    flat_c1 = Path(MOUNT) / "translations" / "06_c1_interpretation"
    # map file prefix -> work
    def work_of(fname: str) -> str:
        m = re.match(r"(?:t3_|c1_|p[0-9]_|r1_|r2_)?([a-z0-9]+)", fname.lower())
        return m.group(1) if m else ""

    for f in flat_t1.glob("*.md"):
        w = work_of(f.name)
        if w:
            works.setdefault(w, WorkState(work_id=w))
            if works[w].t1 in ("NOT_STARTED",):
                works[w].t1 = "LEGACY_PRESENT"
    for f in flat_t3.glob("*.md"):
        w = work_of(f.name)
        if w:
            works.setdefault(w, WorkState(work_id=w))
            works[w].l2 = "LEGACY_PRESENT" if works[w].l2 == "NOT_STARTED" else "PARTIAL"
    for f in flat_c1.glob("*.md"):
        w = work_of(f.name)
        if w:
            works.setdefault(w, WorkState(work_id=w))
            works[w].c1 = "LEGACY_PRESENT"

    # 3. source discovery: which works have Sanskrit on disk? (Muktabodha lib + round2/3 + gretil)
    src_lib = Path(MOUNT) / "sources"
    raw_sources = {
        "kramasadbhava": ["round3/kramasadbhava_IAST.txt"],
        "kubjikamata": ["gretil2/raw_kubjikamata.txt"],
        "kubjika": ["muktabodha-lib/kubjikAtantra-M00030-IAST.txt"],
        "malinivijayottara": ["muktabodha-lib/mAlinIvijayottaratantra-M00160-IAST.txt"],
        "kiranatantra": ["muktabodha-lib/kiraNatantra-M00073-IAST.txt"],
        "sivasutra": ["muktabodha-lib/ziwasUtra with bhAskara-M00066-IAST.txt"],
        "spandakarika": ["muktabodha-lib/spandakArikA-M00067-IAST.txt"],
        "tantraloka": ["gretil_tantraloka.txt"],
        "kulasara": ["muktabodha-lib/kulasAra-M00294-IAST.txt"],
        "cidgagana": ["muktabodha-lib/cidgaganacandrikA-M00014-IAST.txt"],
        "jnanakarika": ["muktabodha-lib/jJAnakArikA-M00021-IAST.txt"],
        "kjn": ["round2/bagchi_kjn_1934.txt"],
        "mahanayaprakasha": ["muktabodha-lib/mahAnayaprakAza-M00033-IAST.txt"],
        "netratantra": ["muktabodha-lib/netratantra-M00038-IAST.txt"],
        "svacchandatantra": ["muktabodha-lib/svacchandatantra-M00091-IAST.txt"],
        "brahmayamala": ["muktabodha-lib/brahmayAmala-M00319-IAST.txt"],
    }
    for w, rels in raw_sources.items():
        if w not in works:
            works[w] = WorkState(work_id=w)
        # find the first existing source
        for rel in rels:
            if (src_lib / rel).exists():
                works[w].source_available = True
                works[w].source_ref = str(src_lib / rel)
                # detect format from the actual file
                try:
                    txt = (src_lib / rel).read_text(encoding="utf-8", errors="ignore")[:8000]
                    works[w].source_format = detect_source_format(txt)
                except Exception:
                    works[w].source_format = "UNKNOWN"
                break
        if not works[w].source_available:
            works[w].source_format = "UNKNOWN"

    # 3b. on-disk sivaqueue/acquisition sources (data/corpus/sources/<wid>/<wid>.txt)
    # These are the canonical addressable raw-Sanskrit texts the factory consumes
    # (see acquire_sivaqueue_targets.py). Fall back to them when the mount map doesn't cover
    # the work, so every downloaded source enters the ledger / queue automatically.
    corpus_src = Path("/root/projects/patala/data/corpus/sources")
    if corpus_src.exists():
        for wid in sorted(os.listdir(corpus_src)):
            src_file = corpus_src / wid / f"{wid}.txt"
            if not src_file.is_file():
                continue
            if wid not in works:
                works[wid] = WorkState(work_id=wid)
            # keep an already-resolved mount source_ref (canonical); otherwise use the corpus file
            if not works[wid].source_available:
                works[wid].source_available = True
                works[wid].source_ref = str(src_file)
                try:
                    txt = src_file.read_text(encoding="utf-8", errors="ignore")[:8000]
                    works[wid].source_format = detect_source_format(txt)
                except Exception:
                    works[wid].source_format = "UNKNOWN"

    # 4. bibliography linkage (data/atlas)
    atlas_ids = set()
    for af in ("audited.ts", "bibliographySeed.ts", "sivaqueueSeed.ts", "sivaqueue34Seed.ts"):
        p = Path("/root/projects/patala/data/atlas") / af
        if p.exists():
            atlas_ids |= set(re.findall(r'"?id"?\s*:\s*"([a-z0-9-]+)"', p.read_text()))
    for w, s in works.items():
        # normalize: devipancasataka ~ kalikulapancasatika etc. handled by bibliography
        s.bibliographic_id = w if w in atlas_ids else None

    return sorted(works.values(), key=lambda s: s.work_id)


def ledger_json() -> dict:
    works = discover_works()
    return {
        "note": "Agent 2 translation-state ledger. The control plane for Agent 3. Next action per work = NEXT_VALID_ACTION.",
        "works": {w.work_id: {**w.to_dict(), "next_action": next_valid_action(w)} for w in works},
    }


if __name__ == "__main__":
    import sys
    out = "/root/projects/patala/data/corpus/downloads/translation-state-ledger.json"
    data = ledger_json()
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
    # print the compact status table
    print("=== CORPUS STATUS ===")
    for w in data["works"].values():
        na = w["next_action"]["action"]
        print(f"{w['work_id']:<20} src:{w['source']['format']:<12} "
              f"L0:{w['l0']['status']:<10} t1:{w['translation']['t1']:<14} "
              f"c1:{w['translation']['c1']:<13} -> {na}")
    print(f"\nwrote {out}")
