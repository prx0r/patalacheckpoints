#!/usr/bin/env python3
"""pipeline/test_autonomous.py — tests for the autonomous factory red-team fixes.

F1 idempotency (registry-derived skip) · F4 cross-verse contamination guard ·
F6 avagraha lossless handling · F9 idempotency replay (TEST 1) · F8 crash/resume.

Run: python3 pipeline/test_autonomous.py   (exit 0 = pass)
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def t(name, cond):
    print(("PASS" if cond else "FAIL"), "-", name)
    return cond


def main() -> int:
    ok = True

    # ---- F4: verify_batch rejects cross-verse misbinding / unexpected / duplicates ----
    from batch_translate import _verify_batch
    req = {"k:v1": {"source_sha256": "AAA", "tokens": ["a", "b"]},
           "k:v2": {"source_sha256": "BBB", "tokens": ["c"]}}
    good = {"translations": [
        {"passage_id": "k:v1", "source_sha256": "AAA", "tokens": {"a": "A", "b": "B"}, "close": "c1", "uncertain": []},
        {"passage_id": "k:v2", "source_sha256": "BBB", "tokens": {"c": "C"}, "close": "c2", "uncertain": []},
    ]}
    r = _verify_batch(json.dumps(good), req)
    ok &= t("F4 accepts all correctly-bound items", set(r.keys()) == {"k:v1", "k:v2"})
    bad = {"translations": [
        {"passage_id": "k:v1", "source_sha256": "WRONG", "tokens": {"a": "A"}, "close": "x", "uncertain": []},
        {"passage_id": "k:EVIL", "source_sha256": "AAA", "tokens": {"z": "Z"}, "close": "y", "uncertain": []},
    ]}
    r2 = _verify_batch(json.dumps(bad), req)
    ok &= t("F4 rejects sha-mismatch (misbind)", r2.get("k:v1") == {"rejected": "source_sha256_mismatch"})
    ok &= t("F4 drops unexpected/extra passage", "k:EVIL" not in r2)
    ok &= t("F4 non-JSON → empty (fail-closed)", _verify_batch("garbage", req) == {})

    # ---- F6: avagraha classified as STRUCTURAL:avagraha, P0 lossless ----
    from verify_l0 import classify_char
    ok &= t("F6 classifies apostrophe as avagraha", classify_char("'", False) == "STRUCTURAL:avagraha")
    from raw_l0 import raw_l0_to_canonical
    recs, proof = raw_l0_to_canonical("t", "so'ham")
    ok &= t("F6 P0 lossless on so'ham (0 unknown)",
            (proof.get("coverage") or {}).get("unknown_chars") == 0)

    # ---- F1 / F9: idempotent skip (registry-derived completion) ----
    # Use an isolated work id so we don't touch real data.
    from l0_registry import commit_l0, committed_passage_ids, REGISTRY_PATH
    import shutil
    backup = None
    if os.path.exists(REGISTRY_PATH):
        backup = REGISTRY_PATH + ".bak"
        shutil.copy(REGISTRY_PATH, backup)
    wid = "test-ido-12345"
    try:
        commit_l0(wid, [{"id": f"{wid}-v1:L1:T1"}], committed_by="test", passage_ids=[f"{wid}:v1"])
        cp = committed_passage_ids(wid)
        ok &= t("F1 committed_passage_ids returns the committed passage",
                f"{wid}:v1" in cp)
    finally:
        if backup and os.path.exists(backup):
            os.replace(backup, REGISTRY_PATH)
        else:
            if os.path.exists(REGISTRY_PATH):
                reg = json.load(open(REGISTRY_PATH))
                reg["works"].pop(wid, None)
                json.dump(reg, open(REGISTRY_PATH, "w"), indent=2, ensure_ascii=False)

    # ---- F10: L0-A deterministic floor — gloss is NEVER a commit gate; PARSED needs a lemma ----
    from validate_l0_spec import validate
    def _rec(status, lemma, gloss):
        return {"id": "k:v1:L1:T1", "chunk_id": "k:v1", "line_id": 1, "line_kind": "prose",
                "chunk_char_start": 0, "chunk_char_end": 3, "line_char_start": 0, "line_char_end": 3,
                "wraps_line": False, "raw_fragment": "abc", "source_text": "abc",
                "lemma_iast": lemma, "literal_gloss": gloss, "quoted": False, "status": status}
    amb = validate([_rec("AMBIGUOUS", "", "")], chunk_text="abc")
    ok &= t("F10 AMBIGUOUS empty gloss passes (honest abstention)", amb["PASS"])
    # PARSED with a deterministic lemma commits even with NO gloss (L0-A floor; gloss is L0-B)
    parsed_nogloss = validate([_rec("PARSED", "aSarIra", "")], chunk_text="abc")
    ok &= t("F10 PARSED lemma, empty gloss PASSES (gloss is not a commit gate)", parsed_nogloss["PASS"])
    # PARSED with NO lemma still FAILS (fabricated PARSED — the anti-theatre rule)
    parsed_nolemma = validate([_rec("PARSED", "", "")], chunk_text="abc")
    ok &= t("F10 PARSED empty lemma still FAILS (no fabricated lemma)", not parsed_nolemma["PASS"])

    # ---- F11: l0_worker derives the real work_id for the gloss term packet ----
    from agent3_batch import split_verses
    from l0_worker import source_objects
    verses = split_verses("aśarīrāḥ śarīrasthāḥ kālyārādhanatatparāḥ ||1/1\nvyomarūpā anantākhyā ||1/2")
    objs = source_objects("kramasadbhava", "\n".join(verses))
    ok &= t("F11 work_id derived from passage object_id",
            len(objs) > 0 and objs[0]["object_id"].startswith("kramasadbhava:v"))

    print("\n" + ("ALL PASS" if ok else "SOME FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
