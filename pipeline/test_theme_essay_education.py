#!/usr/bin/env python3
"""pipeline/test_theme_essay_education.py — deterministic tests for the higher-layer workers.

Covers the autonomous THEME → ESSAY → EDUCATION chain (the upper half of the canonical stack),
with model calls stubbed so the test is deterministic + fail-fast:
  THEME:      hybrid-graph clustering of committed C1s -> ThemeProposal (every member resolves,
              overlapping allowed, MACHINE_PROPOSED, boundary present)
  ESSAY:      reactive essay from a committed ENGINEERING_VALIDATED SYNTHESIS -> the
              deterministic essay_validator gates (fail-closed on fabricated depends_on ids,
              missing proof paths, boundary-erasure, unqualified inputs)
  EDUCATION:  distills the committed ESSAY -> concise, no overreach, derived-from-essay

Requires the ML venv (python-louvain + networkx): run with
  machinelearning/research/.venv/bin/python pipeline/test_theme_essay_education.py
(or /root/venv/bin/python with PYTHONPATH set — see the run note at the bottom).
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/root/patalacheckpoints/pipeline")
sys.path.insert(0, "/root/patalacheckpoints/machinelearning/research")
sys.path.insert(0, "/root/fuck-off/lib")

import object_registry as R
import theme_worker as TW
import essay_worker as EW
import education_worker as ED


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL") + " - " + name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def _fake_c1(oid: str, term: str, summary: str) -> dict:
    return {"object_id": oid, "input_hash": oid,
            "c1": {"summary": summary, "function": "establishes",
                   "explanation": summary, "boundary": "local only",
                   "key_terms": [{"term": term, "meaning": "x"}],
                   "related_passages": [], "uncertain": []},
            "c1_status": "MACHINE_PROPOSED"}


def _fake_argument(c1_oid: str) -> dict:
    return {
        "argument": {
            "argument_id": f"arg:{c1_oid}",
            "conclusion": {"text": f"The verse establishes the support of the powers ({c1_oid}).",
                           "source": c1_oid},
            "premises": [{"id": f"{c1_oid}__P1", "text": "The passage establishes the support.",
                          "role": "supporting_premise"}],
            "inference": "The support is established.",
            "counterargument": "One might object.",
            "crux": {"load_bearing_premise": 1, "why": "It supplies the support."},
            "key_terms": [{"term": "pratibhā", "meaning": "x"}],
            "uncertain": [], "boundary": "local only",
        },
        "argument_status": "MACHINE_PROPOSED",
        "derived_by": "model (gateway_exec)",
    }


def _fake_synthesis(c1_oid: str, arg_oid: str, theme_oid: str, c1_ids: list[str]) -> dict:
    return {
        "synthesis": {
            "object_id": f"{arg_oid}__synth",
            "text": "The members jointly establish the local support of the powers.",
            "crux": {"what": "The load-bearing commitment is the support.",
                     "why": "Removing it leaves the inputs without a determinate support."},
            "unresolved": "Nothing further is resolved here.",
            "method": "MODEL_DERIVED_FROM_ARGUMENT_THEME_C1",
            "source_text": {"argument_id": arg_oid, "theme_id": theme_oid, "c1_id": c1_oid},
            "converges_on": sorted(c1_ids),
            "does_not_claim": "essay-level thesis / cross-tradition / modern application",
            "key_terms": [{"term": "pratibhā", "meaning": "x"}],
            "uncertain": [], "boundary": "local only",
        },
        "synthesis_status": "MACHINE_PROPOSED",
        "derived_by": "model (gateway_exec)",
    }


def _valid_essay_json(synth_oid: str, arg_oid: str, c1_oid: str) -> dict:
    return {
        "title": "The Support of the Powers",
        "sections": [
            {"id": "sec1", "heading": "The Established Support",
             "paragraphs": [
                 {"text": "The synthesis establishes the local support of the powers.",
                  "depends_on": [synth_oid, arg_oid, c1_oid]},
             ]},
            {"id": "sec2", "heading": "Scope",
             "paragraphs": [
                 {"text": "The claim is bounded to the local support.",
                  "depends_on": [synth_oid, c1_oid]},
             ]},
        ],
        "conclusion": "The verse establishes the local support of the powers.",
    }


def main() -> int:
    ok = True
    R.REG_DIR = Path(tempfile.mkdtemp())
    c1_ids = ["kramasadbhava:v1", "kramasadbhava:v3", "kramasadbhava:v4"]

    # seed committed C1s + ENGINEERING_VALIDATED ARGUMENTs (the THEME/ESSAY floors)
    for oid in c1_ids:
        R.commit("C1", oid, oid, created_by="test",
                 payload=_fake_c1(oid, "pratibhā", "The verse establishes the support of the powers."))
    arg_oids = []
    for oid in c1_ids:
        rec = R.commit("ARGUMENT", f"{oid}__arg", oid, created_by="test",
                       payload=_fake_argument(oid), input_refs=[oid])
        R.set_status("ARGUMENT", rec["object_id"], rec["version"], R.ENGINEERING_VALIDATED,
                     actor="test::gate")
        arg_oids.append(rec["object_id"])

    print("=== THEME: hybrid clustering of committed C1s ===")
    props = TW.theme_generator("THEME", [{"object_id": o} for o in c1_ids])
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
        for p_ in props:
            R.commit("THEME", p_["object_id"], p_["input_hash"], created_by="test",
                     payload={"theme": p_["theme"], "theme_status": p_["theme_status"]})
    theme_oid = "kramasadbhava__theme_1"

    print()
    print("=== ESSAY: reactive essay from a committed ENGINEERING_VALIDATED SYNTHESIS ===")
    # commit an ENGINEERING_VALIDATED SYNTHESIS (DAG: ESSAY requires [SYNTHESIS])
    synth_oids = []
    for c1_oid, arg_oid in zip(c1_ids, arg_oids):
        payload = _fake_synthesis(c1_oid, arg_oid, theme_oid, c1_ids)
        rec = R.commit("SYNTHESIS", f"{arg_oid}__synth",
                       R.input_hash({"argument": R.current("ARGUMENT", arg_oid)["payload"],
                                     "theme": R.current("THEME", theme_oid)["payload"]}),
                       created_by="test", payload=payload, input_refs=[arg_oid, theme_oid])
        R.set_status("SYNTHESIS", rec["object_id"], rec["version"], R.ENGINEERING_VALIDATED,
                     actor="test::gate")
        synth_oids.append(rec["object_id"])
    EW.generate_json = lambda system, user, **kw: _valid_essay_json(synth_oids[0], arg_oids[0], c1_ids[0])
    eprops = EW.essay_generator("ESSAY", [{"object_id": o} for o in synth_oids])
    ok &= t("ESSAY generator produced a proposal per qualified synthesis", len(eprops) == len(synth_oids), f"{len(eprops)}")
    if eprops:
        p = eprops[0]
        ok &= t("ESSAY status MACHINE_PROPOSED", p["essay_status"] == "MACHINE_PROPOSED")
        ok &= t("ESSAY has sections + depends_on proof paths",
                len(p["essay"]["sections"]) >= 2
                and all(sec["paragraphs"] and all(par.get("depends_on") for par in sec["paragraphs"])
                        for sec in p["essay"]["sections"]))
        vok, why = EW.essay_validator("ESSAY", p)
        ok &= t("ESSAY validator passes", vok, why)
        # commit the essay for the education test
        rec = R.commit("ESSAY", p["object_id"], p["input_hash"], created_by="test",
                       payload={"essay": p["essay"], "essay_status": p["essay_status"],
                                "derived_by": p["derived_by"]}, input_refs=p["input_refs"])
        ok &= t("ESSAY committed (GENERATED first)", rec["status"] == R.GENERATED)

    # fail-closed: an essay with a fabricated depends_on id must be rejected
    import copy as _copy
    if eprops:
        fab = _copy.deepcopy(eprops[0])
        fab["essay"]["sections"][0]["paragraphs"][0]["depends_on"] = ["kramasadbhava:v99__arg__synth"]
        ok &= t("essay_validator rejects fabricated depends_on id",
                EW.essay_validator("ESSAY", fab)[0] is False)

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
