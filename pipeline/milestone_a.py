#!/usr/bin/env python3
"""Milestone A — build one complete scholarly object for Kramasadbhāva 1.8,
driven by the hermes agent (the real model path)."""
import sys, os
sys.path.insert(0, "/root/projects/patala")
import pipeline.state_machine as sm

WORK = "kramasadbhava"
LOC = "1.8"
SANSKRIT = "ooṃ namaste devadeveśi mahākāli namo'stu te | namo'stu paramānande nirānande namo'stu te"
EDITION = "Dyczkowski ed."
SOURCE_ID = "pt:src:kramasadbhava:dyczkowski-ed"
FLOW = ("T1", "R1", "T2", "R2", "T3", "T3.1")

def main():
    import shutil
    path = sm.passage_path(WORK, LOC)
    if os.path.exists(path):
        os.remove(path)
    for i in range(14):
        res = sm.advance_passage(WORK, LOC, SANSKRIT, EDITION, SOURCE_ID, 1, 8,
                                 flow=FLOW, created_by="patala-agent")
        txn = res.get("next_transition") or {}
        print(f"step {i}: ran={res.get('stage')} ok={res['ok']} action={txn.get('action')} reason={res.get('reason','')[:60]}", flush=True)
        if res.get("stage") is None:
            break
        if res.get("stage") == "T1" and res["ok"]:
            print("  T1:", res["record"]["stages"]["T1"].get("close_translation","")[:120], flush=True)

if __name__ == "__main__":
    main()
