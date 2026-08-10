#!/usr/bin/env python3
"""Run C1 on kramasadbhāva 1.8 via the real Hermes path.

C1 is the first external-evidence challenge to the machine adjudication. It receives
the full translation stack + a mini nirānanda dossier direction, researches, and may
emit a TranslationChallenge routing back to R2/T3 v2.

Per the Milestone A review: nirānande was classified CONSTRAINED but external evidence
(Mahānaya renders 'the Bliss of Stillness'; nirācārānanda; Krama technical use) suggests
PREFERRED or OPEN. C1 must adjudicate this with evidence.
"""
import sys, os, json
sys.path.insert(0, "/root/projects/patala")
import pipeline.state_machine as sm
import pipeline.schema as schema
from pipeline import prompts
import pipeline.model as model_mod

WORK = "kramasadbhava"
LOC = "1.8"
FLOW = ("T1", "R1", "T2", "R2", "T3", "T3.1", "C1")

# The nirānanda dossier direction (evidence the C1 agent should research).
NIRANANDA_DIRECTION = (
    "EVIDENCE TO RESEARCH FOR nirānande:\n"
    "1. Morphology: nir- + ānanda literally permits the privative 'without bliss'.\n"
    "2. SAME/SCHOOL: the online Mahānaya edition of Kramasadbhāva 1.8 renders nirānande "
    "as 'the Bliss of Stillness', not merely 'bliss-less'.\n"
    "3. RELATED: Dyczkowski-related Kubjikā material treats nirānanda as technical, "
    "connected with nirācārānanda 'bliss of stillness'.\n"
    "4. PARALLELS: other tantric sources use nirānanda for a transcendental/void-related "
    "state of bliss beyond the bliss/absence opposition.\n"
    "5. QUESTION: can the root text alone force the literal privative, or is the "
    "historical technical sense PREFERRED/OPEN? Is R2's CONSTRAINED classification too strong?"
)

def main():
    rec = sm.load_record(WORK, LOC)
    if rec is None:
        print("NO RECORD — run milestone_a first"); return

    # add the direction into the record so the C1 user prompt can reference it
    rec.setdefault("research_direction", NIRANANDA_DIRECTION)

    # Build the C1 user prompt manually (with the full stack + direction)
    sys_msg = prompts.sys_C1()
    user = prompts.user_prompt("C1", rec, evidence_packet=None)
    user = user + "\n\n" + NIRANANDA_DIRECTION + \
           "\n\nReturn STRICT JSON: {\"interpretation\":\"...\",\"evidence_state\":\"C1_EVIDENCE_PARTIAL\",\"cruxes\":[],\"evidence\":[],\"open_questions\":[],\"proposals\":[],\"challenges\":[]}"

    print("=== C1 user prompt length:", len(user), flush=True)
    raw = model_mod.chat(sys_msg, user, model="deepseek-v4-flash", temperature=0.4)
    print("=== C1 raw length:", len(raw), flush=True)

    # store it
    try:
        obj = model_mod.parse_json(raw)
        payload = schema.stage_C1(
            interpretation=obj.get("interpretation", raw),
            c1_id=obj.get("c1_id", f"c1:{WORK}:{LOC}:v1"),
            derived_from_t3=rec.get("pipeline_stage", "T3"),
            evidence_state=obj.get("evidence_state", "C1_EVIDENCE_PARTIAL"),
            evidence=obj.get("evidence", []),
            open_questions=obj.get("open_questions", []),
            proposals=obj.get("proposals", []),
            challenges=obj.get("challenges", []),
            cruxes=obj.get("cruxes", []),
        )
        schema.set_stage(rec, payload, created_by="patala-agent", derived_from="T3")
        sm.save_record(rec)
        print("C1 SAVED. challenges:", len(payload["challenges"]), flush=True)
        for c in payload["challenges"]:
            print("  CHALLENGE:", c, flush=True)
    except Exception as e:
        print("C1 parse/contract fail:", e, flush=True)
        print("RAW:", raw[:800], flush=True)

if __name__ == "__main__":
    main()
