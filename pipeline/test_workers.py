#!/usr/bin/env python3
"""pipeline/test_workers.py — L0 + L200 layer-worker tests (deterministic paths; model stubbed).

Covers: L0 validator (fail-closed), L200 generator scaffold + Task-2 validator + controller commit.
Model-proposal layers are stubbed so the test is deterministic and fail-fast.
"""
from __future__ import annotations

import json
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
    import autonomy as A

    # ---- L0 validator: fail-closed on a fabricated lemma; PARSED lemma commits w/o gloss ----
    from l0_worker import l0_validator
    def _l0rec(status, lemma, gloss):
        return {"id": "x:L1:T1", "chunk_id": "x", "line_id": 1, "line_kind": "prose",
                "chunk_char_start": 0, "chunk_char_end": 5, "line_char_start": 0, "line_char_end": 5,
                "wraps_line": False, "raw_fragment": "śivaḥ", "source_text": "śivaḥ",
                "lemma_iast": lemma, "literal_gloss": gloss, "quoted": False, "status": status}
    ok &= t("L0 validator rejects a PARSED record with empty lemma (fabricated)",
            l0_validator("L0", {"object_id": "x", "input_hash": "h", "verse": "śivaḥ",
                                "records": [_l0rec("PARSED", "", "")]})[0] == False)
    ok &= t("L0 validator accepts a PARSED record with a deterministic lemma, no gloss (L0-A)",
            l0_validator("L0", {"object_id": "x", "input_hash": "h", "verse": "śivaḥ",
                                "records": [_l0rec("PARSED", "śiva", "")]})[0] == True)

    # ---- L200 worker (model MT/IA stubbed; COMPARATIVE L1+L2; constrained classifier) ----
    LW._classify_candidates = lambda oid, cands: (
        "COMPLETE",
        [{"label": "MT-001", "type": "SUPPLIED", "basis": "x"}],
        [{"label": "IA-001", "text": "y"}], [])

    l2 = {"text": "The blue shines as one with the manifestation.",
          "l1_text": "blue manifests as one with the light (grounded).",
          "l2_ref": "pt:l2:IPVV:V1A",
          "paragraphs": ["The blue shines as one with the manifestation."],
          "par_refs": [["pt:l1:1", "pt:l0:2", "src:3"]],
          "source_layer": [{"par": 0, "speaker": "Abhinava"}],
          "cross_references": [{"target": "IPVV:V2-C", "type": "SAME_ARGUMENT_CONTINUATION"}]}
    # L200 resolves committed L2 from the registry (constrained compiler) — commit it first.
    R.commit("L2", "IPVV:V1A", "h2", created_by="test",
             payload={"l2": {"text": l2["text"]}, "l1": {"text": l2["l1_text"]}})
    p = LW.l200_generator("L200", [{"object_id": "IPVV:V1A", "input_hash": "h2"}])[0]
    secs = sorted(p["l200"].keys())
    ok &= t("L200 generator produces all 8 sections",
            secs == sorted(["0_identification","1_published_reading","2_derivation_map",
                            "3_material_translation_decisions","4_interpretive_assertions",
                            "5_source_layer","6_cross_references","7_open_items","8_review_state"]))
    ok &= t("L200 proposal status COMPLETE on success", p["proposal_status"] == "COMPLETE")
    ok &= t("L200 l2_ref is a canonical id, l2_hash separate",
            p["l200"]["0_identification"].get("l2_ref") == "IPVV:V1A" and
            p["l200"]["0_identification"].get("l2_hash") == "h2")
    ok &= t("L200 derivation map present", bool(p["l200"].get("2_derivation_map")))
    ok &= t("L200 validator passes on a complete audit", LW.l200_validator("L200", p)[0])
    p["l200"]["3_material_translation_decisions"] = [{"type": "BOGUS"}]
    ok &= t("L200 validator rejects a bad MT type", LW.l200_validator("L200", p)[0] == False)
    p["l200"]["3_material_translation_decisions"] = []
    p["proposal_status"] = "GENERATION_FAILED"
    ok &= t("L200 validator blocks a GENERATION_FAILED proposal (fail-closed)",
            LW.l200_validator("L200", p)[0] == False)
    p["proposal_status"] = "COMPLETE"
    p["l200"]["2_derivation_map"] = []
    ok &= t("L200 validator requires a derivation map", LW.l200_validator("L200", p)[0] == False)
    p["l200"]["2_derivation_map"] = [{"l2_par": "The blue shines as one with the manifestation."}]
    ok &= t("L200 validator passes after derivation map restored", LW.l200_validator("L200", p)[0])

    # ---- controller commits L200 once L2 is committed ----
    rep = A.tick(layers=["L200"], max_batch=1, dry_run=False,
                 inputs={"L200": [{"object_id": "IPVV:V1A", "input_hash": "h2"}]})
    ok &= t("controller L200 tick commits", rep["committed"] == 1 and rep["failed"] == 0)
    cur = R.current("L200", "IPVV:V1A")
    ok &= t("L200 object persisted with derivation map", cur and cur["payload"].get("l200", {}).get("2_derivation_map"))
    ok &= t("L200 idempotent (second tick skips)", A.tick(layers=["L200"], max_batch=1, dry_run=False,
                                                          inputs={"L200": [{"object_id": "IPVV:V1A", "input_hash": "h2"}]})["committed"] == 0)

    # ---- CP8: C1 worker consumes committed L200; deterministic validator gates ----
    from c1_worker import c1_generator, c1_validator
    c1b = [{"object_id": "IPVV:V1A", "input_hash": "h2"}]
    # stub the model call for a deterministic test
    _orig_chat = LW.chat
    from c1_worker import chat as c1_chat
    def _fake_chat(system, prompt, **kw):
        return json.dumps({"summary": "The powers need a support.",
                           "function": "introduces the support of the powers.",
                           "key_terms": [{"term": "pratibhā", "meaning": "the flashing"}],
                           "explanation": "This passage establishes that the flashing is not the order "
                                          "itself but has an order-less support, the great Lord.",
                           "boundary": "It establishes the local support, not every Śaiva claim.",
                           "related_passages": ["V2-P"], "uncertain": ["akrama"]})
    import c1_worker
    c1_worker.chat = _fake_chat
    pc1 = c1_generator("C1", c1b)[0]
    ok &= t("C1 generator produces MACHINE_PROPOSED", pc1["c1_status"] == "MACHINE_PROPOSED")
    ok &= t("C1 validator passes on good commentary", c1_validator("C1", pc1)[0])
    pc1["c1"]["explanation"] = "short"
    ok &= t("C1 validator rejects paraphrase-length explanation", c1_validator("C1", pc1)[0] == False)
    pc1["c1"]["explanation"] = ("This passage establishes that the flashing is not the order itself "
                                "but has an order-less support and anticipates contemporary self-model "
                                "theory.")
    ok &= t("C1 validator rejects modern-comparison lexicon", c1_validator("C1", pc1)[0] == False)
    rep_c1 = A.tick(layers=["C1"], max_batch=1, dry_run=False,
                    inputs={"C1": [{"object_id": "IPVV:V1A", "input_hash": "h2"}]})
    ok &= t("controller C1 tick commits", rep_c1["committed"] == 1 and rep_c1["failed"] == 0)
    ok &= t("C1 object persisted", R.current("C1", "IPVV:V1A") is not None)
    c1_worker.chat = _orig_chat

    # ---- CP3: L1/L2 provenance continuity (deterministic, no model) ----
    from l1_l2_worker import make_l1_handlers, make_l2_handlers
    from l0_worker import l0_generator, l0_validator
    # commit a deterministic L0 object first (L0-A floor)
    l0batch = [{"object_id": "sp:k1", "input_hash": "h0",
                "verse": "śivo bhūtvā śivaṃ yajet"}]
    l0prop = l0_generator("L0", l0batch)[0]
    ok &= t("CP3 L0-A floor commits", l0_validator("L0", l0prop)[0])
    R.commit("L0", "sp:k1", "h0", created_by="test", payload={k: v for k, v in l0prop.items() if k not in ("object_id", "input_hash")})

    h1 = make_l1_handlers()
    p1 = h1["generator"]("L1", [{"object_id": "sp:k1", "input_hash": "h0"}])[0]
    ok &= t("CP3 L1 resolves committed L0 provenance", h1["validator"]("L1", p1)[0])
    R.commit("L1", "sp:k1", "h0", created_by="test", payload={k: v for k, v in p1.items() if k not in ("object_id", "input_hash")})

    h2 = make_l2_handlers()
    p2 = h2["generator"]("L2", [{"object_id": "sp:k1", "input_hash": "h0"}])[0]
    ok &= t("CP3 L2 resolves committed L1 provenance", h2["validator"]("L2", p2)[0])

    # CP3.5 stale propagation: new L0 hash -> old L1 must be superseded, new L1 resolves
    # (driven through the controller tick so detect_stale/supersede runs, as in production)
    from object_registry import supersede
    l0h1 = [{"object_id": "sp:k1", "input_hash": "h1", "verse": "śivo bhūtvā śivaṃ yajet (emended)"}]
    l0prop1 = l0_generator("L0", l0h1)[0]
    R.commit("L0", "sp:k1", "h1", created_by="test", payload={k: v for k, v in l0prop1.items() if k not in ("object_id", "input_hash")})
    # drive L1 with the new hash through the controller (detect_stale supersedes the old L1)
    rep = A.tick(layers=["L1"], max_batch=1, dry_run=False,
                 inputs={"L1": [{"object_id": "sp:k1", "input_hash": "h1"}]})
    vers = [v for v in R.versions("L1", "sp:k1")]
    old = [v for v in vers if v["input_hash"] != "h1"]
    ok &= t("CP3.5 old L1 superseded on source mutation",
            (not old) or all(v.get("superseded") for v in old))
    ok &= t("CP3.5 new L1 resolves new L0", R.current("L1", "sp:k1")["input_hash"] == "h1")

    print("\n" + ("ALL PASS" if ok else "SOME FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
