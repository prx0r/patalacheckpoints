#!/usr/bin/env python3
"""pipeline/test_workers.py — L0 + L200 layer-worker tests (deterministic paths; model stubbed).

Covers: L0 validator (fail-closed), L200 generator scaffold + Task-2 validator + controller commit.
Model-proposal layers are stubbed so the test is deterministic and fail-fast.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import l200_worker as LW
import object_registry as R
import autonomy as A


def t(name, cond):
    print(("PASS" if bool(cond) else "FAIL"), "-", name)
    return bool(cond)


def main() -> int:
    ok = True
    R.REG_DIR = Path(tempfile.mkdtemp())

    # ---- L0 validator: fail-closed on empty glosses (PARSED w/o gloss) ----
    from l0_worker import l0_validator
    ok &= t("L0 validator rejects a PARSED record with empty gloss",
            l0_validator("L0", {"object_id": "x", "input_hash": "h", "verse": "śivaḥ",
                                "records": [{"status": "PARSED", "lemma_iast": "śiva", "literal_gloss": "",
                                             "raw_fragment": "śivaḥ", "chunk_char_start": 0, "chunk_char_end": 5}]})[0] == False)

    # ---- L200 worker (model MT/IA stubbed) ----
    LW._propose_mt_ia = lambda oid, txt: (
        [{"label": "MT-001", "type": "SUPPLIED", "basis": "x"}],
        [{"label": "IA-001", "text": "y"}], [])

    l2 = {"text": "The blue shines as one with the manifestation.",
          "paragraphs": ["The blue shines as one with the manifestation."],
          "par_refs": [["pt:l1:1", "pt:l0:2", "src:3"]],
          "source_layer": [{"par": 0, "speaker": "Abhinava"}],
          "cross_references": [{"target": "IPVV:V2-C", "type": "SAME_ARGUMENT_CONTINUATION"}]}
    p = LW.l200_generator("L200", [{"object_id": "IPVV:V1A", "input_hash": "h2", "_l2": l2}])[0]
    secs = sorted(p["l200"].keys())
    ok &= t("L200 generator produces all 8 sections",
            secs == sorted(["0_identification","1_published_reading","2_derivation_map",
                            "3_material_translation_decisions","4_interpretive_assertions",
                            "5_source_layer","6_cross_references","7_open_items","8_review_state"]))
    ok &= t("L200 validator passes on a complete audit", LW.l200_validator("L200", p)[0])
    p["l200"]["3_material_translation_decisions"] = [{"type": "BOGUS"}]
    ok &= t("L200 validator rejects a bad MT type", LW.l200_validator("L200", p)[0] == False)
    p["l200"]["3_material_translation_decisions"] = []
    p["l200"]["5_source_layer"] = []
    ok &= t("L200 validator requires source-layer", LW.l200_validator("L200", p)[0] == False)

    # ---- controller commits L200 once L2 is committed ----
    R.commit("L2", "IPVV:V1A", "h2", created_by="test")
    rep = A.tick(layers=["L200"], max_batch=1, dry_run=False,
                 inputs={"L200": [{"object_id": "IPVV:V1A", "input_hash": "h2", "_l2": l2}]})
    ok &= t("controller L200 tick commits", rep["committed"] == 1 and rep["failed"] == 0)
    cur = R.current("L200", "IPVV:V1A")
    ok &= t("L200 object persisted with derivation map", cur and cur["payload"].get("l200", {}).get("2_derivation_map"))
    ok &= t("L200 idempotent (second tick skips)", A.tick(layers=["L200"], max_batch=1, dry_run=False,
                                                          inputs={"L200": [{"object_id": "IPVV:V1A", "input_hash": "h2", "_l2": l2}]})["committed"] == 0)

    print("\n" + ("ALL PASS" if ok else "SOME FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
