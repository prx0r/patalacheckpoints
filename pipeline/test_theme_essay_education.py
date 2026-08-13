#!/usr/bin/env python3
"""pipeline/test_theme_essay_education.py — deterministic tests for the higher-layer workers.

Covers the autonomous THEME → ESSAY → EDUCATION chain (the upper half of the canonical stack),
with model calls stubbed so the test is deterministic + fail-fast:
  THEME:      hybrid-graph clustering of committed C1s -> ThemeProposal (every member resolves,
              overlapping allowed, MACHINE_PROPOSED, boundary present)
  ESSAY:      drafts from a committed THEME -> SentenceEvidenceAudit gates (fail-closed on
              certainty-inflation / boundary-erasure / orphan sentences)
  EDUCATION:  distills the committed ESSAY -> concise, no overreach, derived-from-essay

Requires the ML venv (python-louvain + networkx): run with
  machinelearning/research/.venv/bin/python pipeline/test_theme_essay_education.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")
sys.path.insert(0, "/root/projects/patala/machinelearning/research")

import object_registry as R
import theme_worker as TW
import essay_worker as EW
import education_worker as ED


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def _fake_c1(oid: str, term: str, summary: str) -> dict:
    return {"object_id": oid, "input_hash": oid,
            "c1": {"summary": summary, "function": "establishes",
                   "explanation": summary, "boundary": "local only",
                   "key_terms": [{"term": term, "meaning": "x"}],
                   "related_passages": [], "uncertain": []},
            "c1_status": "MACHINE_PROPOSED"}


def main() -> int:
    ok = True
    R.REG_DIR = Path(tempfile.mkdtemp())

    # seed 3 committed C1s that share a term (pratibhā) -> one theme
    for i in (1, 3, 4):
        c1 = _fake_c1(f"kramasadbhava:v{i}", "pratibhā",
                      "The verse establishes the support of the powers.")
        R.commit("C1", f"kramasadbhava:v{i}", f"kramasadbhava:v{i}", created_by="test", payload=c1)

    print("=== THEME: hybrid clustering of committed C1s ===")
    props = TW.theme_generator("THEME", [{"object_id": o} for o in
                                         ("kramasadbhava:v1", "kramasadbhava:v3", "kramasadbhava:v4")])
    ok &= t("THEME generator produced ≥1 proposal", len(props) >= 1, f"{len(props)}")
    if props:
        p = props[0]
        ok &= t("THEME proposal is MACHINE_PROPOSED", p["theme_status"] == "MACHINE_PROPOSED")
        members = p["theme"]["member_claims"]
        ok &= t("THEME members all resolve to committed C1s",
                all(R.current("C1", m["c1_id"]) for m in members),
                f"{[m['c1_id'] for m in members]}")
        ok &= t("THEME members carry strength+role", all("strength" in m and "role" in m for m in members))
        ok &= t("THEME has boundary (synthesis-inflation guard)",
                bool(p["theme"].get("boundary", {}).get("included_because")))
        vok, why = TW.theme_validator("THEME", p)
        ok &= t("THEME validator passes", vok, why)
        # commit the theme for the essay test
        for p_ in props:
            R.commit("THEME", p_["object_id"], p_["input_hash"], created_by="test",
                     payload={"theme": p_["theme"], "theme_status": p_["theme_status"]})

    print()
    print("=== ESSAY: drafts from committed THEME + SentenceEvidenceAudit gate ===")
    EW.chat = lambda system, prompt, **kw: json.dumps({
        "title": "The Support of the Powers",
        "sentences": [
            {"text": "The powers knowledge memory removal are established.",
             "claim_ids": ["TH-1-M1"], "provenance_relation": "PARAPHRASE"},
            {"text": "A power needs a support, the maheśvara.",
             "claim_ids": ["TH-1-M2"], "provenance_relation": "PARAPHRASE"},
            {"text": "The pratibhā is the flashing with an order-less support.",
             "claim_ids": ["TH-1-M3"], "provenance_relation": "PARAPHRASE"},
        ]})
    themes = [oid for oid, vs in R._load("THEME")["objects"].items() if not vs[-1].get("superseded")]
    batch = [{"object_id": t} for t in themes] + \
            [{"object_id": o} for o in ("kramasadbhava:v1", "kramasadbhava:v3", "kramasadbhava:v4")]
    eprops = EW.essay_generator("ESSAY", batch)
    ok &= t("ESSAY generator produced a proposal", len(eprops) == 1, f"{len(eprops)}")
    if eprops:
        p = eprops[0]
        ok &= t("ESSAY status MACHINE_PROPOSED", p["essay_status"] == "MACHINE_PROPOSED")
        ok &= t("ESSAY has claims + sentences", bool(p["essay"]["claims"]) and bool(p["essay"]["sentences"]))
        ok &= t("SentenceEvidenceAudit passed", p.get("_audit_ok") is True)
        vok, why = EW.essay_validator("ESSAY", p)
        ok &= t("ESSAY validator passes", vok, why)
        # commit the essay for the education test
        R.commit("ESSAY", p["object_id"], p["input_hash"], created_by="test",
                 payload={"essay": p["essay"], "essay_status": p["essay_status"],
                          "_audit_ok": p["_audit_ok"]})

    # fail-closed: an essay that overclaims must be rejected by the audit
    from patala_ml.essay import Essay, plan_hash
    from patala_ml.essaysentence import EssaySentence
    from patala_ml.essayverify import verify_essay
    bad = Essay("e-bad", "p", "h", "t", "bad",
                claims=[{"id": "TH-1-M1", "role": "claim", "text": "x",
                         "boundary": "does not by itself establish the universal Self"}])
    bad.add_sentence(EssaySentence("s1", "This proves consciousness is the one universal Self.",
                                   claim_ids=["TH-1-M1"], provenance_relation="PARAPHRASE"))
    ok &= t("verify_essay rejects certainty-inflation + boundary-erasure", verify_essay(bad)["ok"] is False)

    print()
    print("=== EDUCATION: distills the committed ESSAY, no overreach ===")
    ED.chat = lambda system, prompt, **kw: json.dumps({
        "title": "The Support of the Powers", "summary": "The powers need a support, the Lord.",
        "key_points": ["Powers are established.", "They rest in the maheśvara."],
        "essay_id": "x", "status": "MACHINE_PROPOSED"})
    essays = [oid for oid, vs in R._load("ESSAY")["objects"].items() if not vs[-1].get("superseded")]
    dprops = ED.education_generator("EDUCATION", [{"object_id": e} for e in essays])
    ok &= t("EDUCATION generator produced a proposal", len(dprops) >= 1, f"{len(dprops)}")
    if dprops:
        p = dprops[0]
        ok &= t("EDUCATION derived from a committed essay", bool(R.current("ESSAY", p.get("_source_essay", ""))))
        ok &= t("EDUCATION validator passes", ED.education_validator("EDUCATION", p)[0])
    # fail-closed: overreach rejected
    bad_prop = {"education_status": "MACHINE_PROPOSED",
                "education": {"summary": "this proves the one Self is everywhere",
                              "key_points": []}, "_source_essay": essays[0] if essays else ""}
    ok &= t("EDUCATION validator rejects overreach",
            ED.education_validator("EDUCATION", bad_prop)[0] is False)

    print("\n" + ("THEME/ESSAY/EDUCATION ALL PASS" if ok else "SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
