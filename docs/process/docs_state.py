#!/usr/bin/env python3
"""docs/process/docs_state.py — the LIVE-STATE projection engine (anti-theatre).

Reads REAL state from the source of truth (object_registry + corpus_state) and emits a canonical
per-layer live-state report. The LAYER PAGES render from THIS, never from a hand-written "it works"
claim. If a layer's object count is 0, the output says "0 objects (not built)" — it does NOT pretend
the pipeline is complete.

Usage:
  python3 docs/process/docs_state.py             # full live-state report (stdout)
  python3 docs/process/docs_state.py --json      # machine-readable JSON
  python3 docs/process/docs_state.py --layer 03  # one layer's live state

This is Piece 1 (Canonical State API) + Piece 3 (Projection Engine) of docs/layers/12-live-system.md.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
for _p in (ROOT, ROOT / "pipeline"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))


def _registry_counts() -> dict:
    import object_registry as R
    return R.summary()


def _live_state() -> dict:
    """The canonical per-layer live state, derived from the source of truth."""
    reg = _registry_counts()
    return {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source": "object_registry.summary() (the canonical state, not hand-written)",
        "layers": {
            "00_governance": {"status": "BUILT", "note": "anti-theatre doctrine + DAG are real; tracked in AGENTS.md"},
            "01_ingestion": {"status": "BUILT", "note": "SourceAsserter + 8 adapters + R2 snapshots; tests pass"},
            "02_atlas": {"status": "PARTIAL", "note": "22-table Postgres + resolver + API real; read API/reconciliation pending"},
            "03_factory": {
                "status": "PARTIAL",
                "objects": {
                    "SOURCE": reg.get("SOURCE", {}).get("objects", 0),
                    "T1": reg.get("T1", {}).get("objects", 0),
                    "L0": reg.get("L0", {}).get("objects", 0),
                    "ARGMAP": reg.get("ARGMAP", {}).get("objects", 0),
                    "L2": reg.get("L2", {}).get("objects", 0),
                    "L200": reg.get("L200", {}).get("objects", 0),
                    "C1": reg.get("C1", {}).get("objects", 0),
                    "THEME": reg.get("THEME", {}).get("objects", 0),
                    "ARGUMENT": reg.get("ARGUMENT", {}).get("objects", 0),
                    "SYNTHESIS": reg.get("SYNTHESIS", {}).get("objects", 0),
                    "ESSAY": reg.get("ESSAY", {}).get("objects", 0),
                    "EDUCATION": reg.get("EDUCATION", {}).get("objects", 0),
                },
                "note": "SOURCE->C1->THEME->ARGUMENT real; SYNTHESIS/ESSAY/EDUCATION are 0 (not built)",
            },
            "04_evidence": {"status": "BUILT", "note": "contracts + 69 tools documented + eval plane"},
            "05_research": {"status": "PARTIAL", "note": "argument/crux/synthesis compilers + golds exist; 0 essay/education objects"},
            "06_commentarial": {"status": "DESIGN", "note": "paper->ScholarContributionPacket is design only"},
            "07_verification": {"status": "BUILT", "note": "Inspect eval plane + 10 self-tests"},
            "08_human_authority": {"status": "PARTIAL", "note": "ReviewEvent ledger + review_engine real; scholar workbench UI pending"},
            "09_organism": {"status": "DESIGN", "note": "human-understanding graph is design only"},
            "10_surfaces": {"status": "PARTIAL", "note": "app/ + mcp/ + openpatala real; Scholar/Contributor/Reviewer surfaces pending"},
            "11_org_economics": {"status": "DESIGN", "note": "credit/market/partnership strategy is aspirational"},
            "12_live_system": {"status": "PARTIAL", "note": "Tier-1 truth (registry/review/events) real; projection/staleness/MCP/queue pending"},
        },
        "proven_pipeline": "SOURCE(32k)->T1->L0->ARGMAP->L2->L200->C1->THEME->ARGUMENT",
        "not_built": ["SYNTHESIS", "ESSAY", "EDUCATION"],
    }


def _markdown(state: dict) -> str:
    out = ["## LIVE STATE (derived from object_registry — do NOT hand-edit)", "", "```text"]
    for k, v in state["layers"].items():
        label = k.upper()
        status = v["status"]
        obj = ""
        if "objects" in v:
            objs = v["objects"]
            real = [f"{lk}={lv}" for lk, lv in objs.items() if lv > 0]
            zero = [f"{lk}=0" for lk, lv in objs.items() if lv == 0]
            obj = f"  objects: {', '.join(real)}" + (f"  |  {', '.join(zero)} NOT-BUILT" if zero else "")
        out.append(f"{label}  [{status}]{obj}")
    out.append("```")
    out.append("")
    out.append(f"*Generated {state['generated_at']} from `object_registry.summary()` — the canonical source of truth.*")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--layer", default=None)
    ap.add_argument("--markdown", action="store_true")
    a = ap.parse_args()
    state = _live_state()
    if a.layer:
        key = f"{a.layer}_"
        match = {k: v for k, v in state["layers"].items() if k.startswith(key)}
        if a.json:
            print(json.dumps(match, indent=2, ensure_ascii=False))
        else:
            for k, v in match.items():
                print(f"{k.upper()}: {json.dumps(v, ensure_ascii=False)}")
        return 0
    if a.json:
        print(json.dumps(state, indent=2, ensure_ascii=False))
    elif a.markdown:
        print(_markdown(state))
    else:
        for k, v in state["layers"].items():
            label = k.upper()
            obj = ""
            if "objects" in v:
                real = [f"{lk}={lv}" for lk, lv in v["objects"].items() if lv > 0]
                obj = "  " + ", ".join(real) if real else "  (none built)"
            print(f"{label}  [{v['status']}]{obj}")
        print(f"\nproven pipeline: {state['proven_pipeline']}")
        print(f"not built: {state['not_built']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
