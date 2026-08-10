#!/usr/bin/env python3
"""Run the real Kramasadbhāva 1.8 through the full audited stack (T1→R1→T2→R2→T3→T3.1).
The vertical slice that proves the compounding unit: source → audited decisions → C1.
Writes the persisted record to the work stack. Needs OPENCODE_GO_API_KEY."""
from __future__ import annotations
import json, os, sys, time, datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pipeline.state_machine as sm
from pipeline import model as model_mod

WORK = "kramasadbhava"
LOC = "1.8"
SANSKRIT = "ooṃ namaste devadeveśi mahākāli namo'stu te | namo'stu paramānande nirānande namo'stu te"
EDITION = "Dyczkowski ed., Muktabodha (NGMPP A 209/23)"
SOURCE_ID = "pt:src:kramasadbhava:dyczkowski-ed"
FLOW = ("T1", "R1", "T2", "R2", "T3", "T3.1")
MODEL = "deepseek-v4-flash"

EXPERIMENT = {
    "experiment_id": "kramasadbhava-1.8-v1",
    "pipeline_version": "translation-pipeline-v1.0",
    "model": MODEL,
    "base_source": SOURCE_ID,
    "passage": f"tantra:text:{WORK}:{LOC}",
    "date": datetime.date.today().isoformat(),
}

def main():
    print("=== EXPERIMENT CONFIG ===", flush=True)
    for k, v in EXPERIMENT.items():
        print(f"  {k}: {v}", flush=True)
    print(flush=True)
    start = time.time()
    while True:
        res = sm.advance_passage(WORK, LOC, SANSKRIT, EDITION, SOURCE_ID, 1, 8,
                                 flow=FLOW, created_by="patala-agent", model=MODEL)
        txn = res.get("next_transition") or {}
        elapsed = time.time() - start
        print(f"[{elapsed:.0f}s] ran={res.get('stage')} ok={res['ok']} "
              f"action={txn.get('action')} reason={res.get('reason','')[:50]}", flush=True)
        if not res["ok"]:
            print("BLOCKED:", res.get("reason"), flush=True)
            break
        if res.get("stage") is None:
            break

    rec = sm.load_record(WORK, LOC)
    if rec:
        print("\n=== PERSISTED STACK ===", flush=True)
        print("stages:", list(rec["stages"].keys()), flush=True)
        print("pipeline_stage:", rec.get("pipeline_stage"), "| editorial:", rec.get("editorial_status"), flush=True)
        for s in FLOW:
            if s in rec["stages"]:
                payload = rec["stages"][s]
                print(f"\n--- {s} (v{payload.get('version')}) ---", flush=True)
                if s == "T1":
                    print("close:", payload.get("close_translation","")[:200], flush=True)
                    print("flags:", payload.get("flags"), flush=True)
                    print("tpc:", payload.get("time_place_context",{}), flush=True)
                elif s == "R1":
                    print("cruxes:", payload.get("cruxes"), flush=True)
                elif s == "T2":
                    print("close:", payload.get("close_translation","")[:200], flush=True)
                    print("rival_decisions:", payload.get("rival_decisions"), flush=True)
                elif s == "R2":
                    print("decisions:", payload.get("decisions"), flush=True)
                    print("hard_core:", payload.get("hard_core","")[:200], flush=True)
                elif s == "T3":
                    print("resolved:", payload.get("resolved","")[:200], flush=True)
                    print("open_flags:", payload.get("open_flags"), flush=True)
                elif s == "T3.1":
                    print("reading:", payload.get("reading","")[:200], flush=True)
    else:
        print("NO RECORD PERSISTED", flush=True)

if __name__ == "__main__":
    main()
