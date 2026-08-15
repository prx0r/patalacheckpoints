#!/usr/bin/env python3
"""pipeline/test_education_worker.py — deterministic tests for the EDUCATION layer worker.

Covers the model-derived LEARNING-CLAIM chain (the top of the canonical stack), with
model calls STUBBED so the test is deterministic + fail-fast:
  - qualified essays: only current ENGINEERING_VALIDATED ESSAY records are eligible;
    unqualified records are excluded
  - canonical_input_hash is idempotent per essay — is_committed semantics
  - allowed_depends_on = the essay itself + its proof universe + its synthesis anchor
  - model_derive_education retries on transient empty gateway output and abstains
    (returns None) on persistent junk — never fabricates
  - education_generator assembles a MACHINE_PROPOSED proposal from model JSON
  - education_validator PASSES on a well-formed model-derived learning-claim set
  - education_validator REJECTS: wrong status / hand-fed / < 2 claims / missing
    question / missing expected / missing wrong_answer / missing maps_to / wrong_answer
    equals expected / empty depends_on / duplicate claim_id / unqualified essay /
    unresolved essay / depends_on id not a real object / depends_on id outside the
    allowed set / missing spine id (essay or synthesis) / claim_count mismatch /
    does_not_claim empty / fidelity break / wrong object_id / source_text
    inconsistency / overreach on the TRUE side (expected or maps_to)
  - the overreach lexicon is NEVER applied to wrong_answer (deliberately false side)
  - commit + gate promotion shape: is_committed() idempotent, event chain intact

Run with:
  PYTHONPATH=/root/patalacheckpoints/pipeline:/root/patalacheckpoints/machinelearning/research:/root/fuck-off/lib \
  /root/venv/bin/python pipeline/test_education_worker.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/root/patalacheckpoints/pipeline")
sys.path.insert(0, "/root/patalacheckpoints/machinelearning/research")
sys.path.insert(0, "/root/fuck-off/lib")

import object_registry as R
import essay_worker as EW
import education_worker as ED


def t(name, cond, detail=""):
    print((("PASS" if bool(cond) else "FAIL")) + " - " + name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def _fake_c1(oid: str) -> dict:
    return {"object_id": oid, "input_hash": oid,
            "c1": {"summary": "The verse establishes the support of the powers.",
                   "function": "introduces the support; the following argument depends on it.",
                   "explanation": "The flashing is not the order itself but has an order-less support, the great Lord.",
                   "boundary": "It establishes the local support, not every claim about the universal Self.",
                   "key_terms": [{"term": "pratibhā", "meaning": "the flashing"}],
                   "related_passages": ["V2-P"], "uncertain": ["akrama"]},
            "c1_status": "MACHINE_PROPOSED"}


def _fake_argument(c1_oid: str) -> dict:
    return {
        "argument": {
            "argument_id": f"arg:{c1_oid}",
            "conclusion": {"text": f"The verse establishes the support of the powers ({c1_oid}).",
                           "source": c1_oid},
            "premises": [{"id": f"{c1_oid}__P1", "text": "The passage establishes that the flashing is not the order itself.",
                          "role": "supporting_premise"},
                         {"id": f"{c1_oid}__P2", "text": "The passage establishes that the flashing has an order-less support, the great Lord.",
                          "role": "supporting_premise"}],
            "inference": "Since the flashing is not the order itself and ordered experience requires a support, the support must be the order-less great Lord.",
            "counterargument": "One might object that 'akrama' (order-less) is uncertain.",
            "crux": {"load_bearing_premise": 2, "why": "Premise 2 identifies the support."},
            "key_terms": [{"term": "pratibhā", "meaning": "the flashing"}],
            "uncertain": ["akrama"],
            "boundary": "It establishes the local support, not every claim about the universal Self.",
        },
        "argument_status": "MACHINE_PROPOSED",
        "derived_by": "model (gateway_exec)",
    }


def _fake_theme(c1_ids: list[str]) -> dict:
    return {
        "theme": {
            "theme_id": "kramasadbhava__theme_1",
            "label": "candidate theme 1",
            "member_claims": [{"c1_id": c, "strength": 1.0, "role": "DEFINES"} for c in c1_ids],
            "development": [], "counterexamples": [],
            "edge_evidence": [], "status": "MACHINE_PROPOSED",
            "boundary": {"included_because": c1_ids,
                         "not_claiming": "essay-level thesis / cross-tradition / modern application"},
        },
        "theme_status": "MACHINE_PROPOSED",
    }


def _fake_synthesis(c1_oid: str, arg_oid: str, theme_oid: str, c1_ids: list[str]) -> dict:
    return {
        "synthesis": {
            "object_id": f"{arg_oid}__synth",
            "text": f"The member claims jointly establish that the flashing has an order-less support, the great Lord ({c1_oid}).",
            "crux": {"what": "The load-bearing commitment is that the flashing has an order-less support.",
                     "why": "If this identification is removed, the other inputs cannot establish the support of the powers."},
            "unresolved": "The precise sense of akrama remains uncertain.",
            "method": "MODEL_DERIVED_FROM_ARGUMENT_THEME_C1",
            "source_text": {"argument_id": arg_oid, "theme_id": theme_oid, "c1_id": c1_oid},
            "converges_on": sorted(c1_ids),
            "does_not_claim": "essay-level thesis / cross-tradition / modern application",
            "key_terms": [{"term": "pratibhā", "meaning": "the flashing"}],
            "uncertain": ["akrama"],
            "boundary": "It establishes the local support, not every claim about the universal Self.",
        },
        "synthesis_status": "MACHINE_PROPOSED",
        "derived_by": "model (gateway_exec)",
    }


def _essay_payload(synth_oid: str, arg_oid: str, c1_oid: str, theme_oid: str) -> dict:
    """A well-formed reactive essay payload (passes essay_validator), built like the essay worker's."""
    return {
        "object_id": f"{synth_oid}__essay",
        "title": "The Local Support of the Powers",
        "sections": [
            {"id": "sec1", "heading": "The Established Support",
             "paragraphs": [
                 {"text": "The synthesis establishes that the flashing has an order-less support, the great Lord.",
                  "depends_on": [synth_oid, arg_oid, c1_oid]},
                 {"text": "The support is local; broader claims about the universal Self are outside the boundary.",
                  "depends_on": [synth_oid, c1_oid]},
             ]},
            {"id": "sec2", "heading": "Open Questions",
             "paragraphs": [
                 {"text": "The precise sense of akrama remains uncertain, so the support's character is underdetermined.",
                  "depends_on": [synth_oid, arg_oid, theme_oid]},
             ]},
        ],
        "conclusion": "The verse establishes the local support of the powers, bounded and with akrama unresolved.",
        "dependency_count": 4,
        "method": "MODEL_DERIVED_FROM_SYNTHESIS_ARGUMENT_C1",
        "source_text": {"synthesis_id": synth_oid, "argument_id": arg_oid,
                        "theme_id": theme_oid, "c1_id": c1_oid},
        "does_not_claim": "essay-level thesis / cross-tradition / modern application",
        "key_terms": [{"term": "pratibhā", "meaning": "the flashing"}],
        "uncertain": ["akrama"],
        "boundary": "It establishes the local support, not every claim about the universal Self.",
    }


def _valid_model_json(essay_oid: str, synth_oid: str, arg_oid: str, c1_oid: str) -> dict:
    """A well-formed learning-claim set: 3 claims with real proof paths + known-neighbors."""
    return {
        "learning_claims": [
            {"claim_id": "lc-support-local",
             "question": "What does the essay establish about the flashing?",
             "expected": "The flashing is not the order itself but has an order-less support, the great Lord.",
             "wrong_answer": "The flashing is the order itself and needs no support.",
             "maps_to": "the flashing as the order itself",
             "depends_on": [essay_oid, synth_oid]},
            {"claim_id": "lc-scope-boundary",
             "question": "What is the scope of the claim about the support?",
             "expected": "It establishes the local support, not every claim about the universal Self.",
             "wrong_answer": "It establishes every claim about the universal Self.",
             "maps_to": "the universal-Self inflation",
             "depends_on": [essay_oid, c1_oid]},
            {"claim_id": "lc-akrama-uncertain",
             "question": "Which term remains uncertain in the argument?",
             "expected": "The term akrama remains uncertain, so the support's character is underdetermined.",
             "wrong_answer": "The term akrama is fully determinate.",
             "maps_to": "akrama as determinate",
             "depends_on": [essay_oid, synth_oid, arg_oid]},
        ]
    }


def _seed_registry() -> tuple[str, str, str, str]:
    """Seed 3 C1s + 3 ENGINEERING_VALIDATED arguments + 1 theme + 3 ENGINEERING_VALIDATED
    syntheses + 3 ENGINEERING_VALIDATED essays. Returns (essay_oid, synth_oid, arg_oid, c1_oid)
    for the first pair."""
    c1_ids = ["kramasadbhava:v1", "kramasadbhava:v3", "kramasadbhava:v4"]
    for oid in c1_ids:
        R.commit("C1", oid, oid, created_by="test", payload=_fake_c1(oid))
    arg_oids = []
    for oid in c1_ids:
        rec = R.commit("ARGUMENT", f"{oid}__arg", oid, created_by="test",
                       payload=_fake_argument(oid), input_refs=[oid])
        R.set_status("ARGUMENT", rec["object_id"], rec["version"], R.ENGINEERING_VALIDATED,
                     actor="test::gate")
        arg_oids.append(rec["object_id"])
    theme_oid = R.commit("THEME", "kramasadbhava__theme_1", "theme-hash",
                         created_by="test", payload=_fake_theme(c1_ids), input_refs=c1_ids)["object_id"]
    essay_oids = []
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
        ep = _essay_payload(rec["object_id"], arg_oid, c1_oid, theme_oid)
        # the seeded essay must itself pass the essay gate (honest chain, not a hollow floor)
        vok, why = EW.essay_validator("ESSAY", {
            "essay": ep, "essay_status": "MACHINE_PROPOSED",
            "derived_by": "model (gateway_exec)", "input_refs": [rec["object_id"]]})
        assert vok, f"seeded essay failed its own gate: {why}"
        erec = R.commit("ESSAY", ep["object_id"], "essay-hash", created_by="test",
                        payload={"essay": ep, "essay_status": "MACHINE_PROPOSED",
                                 "derived_by": "model (gateway_exec)"},
                        input_refs=[rec["object_id"]])
        R.set_status("ESSAY", erec["object_id"], erec["version"], R.ENGINEERING_VALIDATED,
                     actor="test::gate")
        essay_oids.append(erec["object_id"])
    return essay_oids[0], synth_oids[0], arg_oids[0], c1_ids[0]


def main() -> int:
    ok = True
    R.REG_DIR = Path(tempfile.mkdtemp())

    essay_oid, synth_oid, arg_oid, c1_oid = _seed_registry()

    # ── canonical input hash: idempotent per essay ───────────────────────────
    h1a = ED.canonical_input_hash(essay_oid)
    h1b = ED.canonical_input_hash(essay_oid)
    ok &= t("canonical input hash stable for same essay", h1a == h1b)
    ok &= t("canonical input hash is sha256 of the ESSAY payload (not of the education)",
            h1a == R.input_hash({"essay": R.current("ESSAY", essay_oid)["payload"]}))

    # ── qualified essays: only ENGINEERING_VALIDATED current records ─────────
    qe = ED.current_engineered_essays()
    ok &= t("qualified essays found (3)", len(qe) == 3, f"{len(qe)}")
    ok &= t("qualified essays are current ENGINEERING_VALIDATED",
            all(e.get("status") == R.ENGINEERING_VALIDATED and not e.get("superseded") for e in qe))

    # ── allowed depends_on: essay + its proof universe + synthesis anchor ────
    allowed = ED.allowed_depends_on(essay_oid)
    ok &= t("allowed set contains essay + synth + arg + c1 + theme",
            {essay_oid, synth_oid, arg_oid, c1_oid}.issubset(allowed), f"{sorted(allowed)}")

    # ── model_derive_education: retries on transient empty, abstains on junk ──
    calls = {"n": 0}
    def _flaky_first(system, user, **kw):
        calls["n"] += 1
        if calls["n"] == 1:
            return {"_raw": ""}   # transient empty gateway response
        return _valid_model_json(essay_oid, synth_oid, arg_oid, c1_oid)
    orig = ED.generate_json
    ED.generate_json = _flaky_first
    res = ED.model_derive_education(essay_oid, max_attempts=3)
    ok &= t("model_derive retries past transient empty output", res is not None and calls["n"] >= 2,
            f"{calls['n']} calls")
    ED.generate_json = lambda system, user, **kw: {"_raw": "not json at all"}
    res = ED.model_derive_education(essay_oid, max_attempts=2)
    ok &= t("model_derive abstains (None) on persistent junk — never fabricates", res is None)
    ED.generate_json = orig

    # ── education_generator: proposal from stubbed model JSON ────────────────
    ED.generate_json = lambda system, user, **kw: _valid_model_json(essay_oid, synth_oid, arg_oid, c1_oid)
    essay_ids = [e["object_id"] for e in ED.current_engineered_essays()]
    props = ED.education_generator("EDUCATION", [{"object_id": o} for o in essay_ids])
    ok &= t("education_generator produced a proposal per qualified essay", len(props) == 3, f"{len(props)}")
    if props:
        p = props[0]
        ok &= t("proposal is MACHINE_PROPOSED", p["education_status"] == "MACHINE_PROPOSED")
        ok &= t("proposal derived_by model (gateway_exec)", p["derived_by"] == "model (gateway_exec)")
        ok &= t("proposal object_id = <essay>__educ", p["object_id"] == f"{essay_oid}__educ")
        ok &= t("proposal input_refs = [essay_oid]", p["input_refs"] == [essay_oid])
        ok &= t("proposal carries fidelity fields (key_terms/uncertain/boundary)",
                p["education"]["key_terms"] == [{"term": "pratibhā", "meaning": "the flashing"}]
                and p["education"]["uncertain"] == ["akrama"]
                and "local support" in p["education"]["boundary"])
        lcs = p["education"]["learning_claims"]
        ok &= t("proposal has >= 2 learning claims with question/expected/wrong_answer/maps_to/depends_on",
                len(lcs) >= 2
                and all(lc.get("question") and lc.get("expected") and lc.get("wrong_answer")
                        and lc.get("maps_to") and lc.get("depends_on") for lc in lcs))
        ok &= t("proposal source_text consistent with the essay",
                p["education"]["source_text"]["essay_id"] == essay_oid
                and p["education"]["source_text"]["synthesis_id"] == synth_oid
                and p["education"]["source_text"]["c1_id"] == c1_oid)
        vok, why = ED.education_validator("EDUCATION", p)
        ok &= t("education_validator passes on model-derived proposal", vok, why)

    # ── education_validator fail-closed checks ───────────────────────────────
    base = props[0] if props else None
    if base:
        import copy as _copy
        def _mut(**kw):
            d = {"education": _copy.deepcopy(base["education"]),
                 "education_status": base["education_status"],
                 "derived_by": base["derived_by"],
                 "input_refs": list(base["input_refs"])}
            for k, v in kw.items():
                d["education"][k] = v
            return d
        def _mut_claim(idx, **kw):
            d = _mut()
            lc = _copy.deepcopy(d["education"]["learning_claims"][idx])
            for k, v in kw.items():
                lc[k] = v
            d["education"]["learning_claims"][idx] = lc
            d["education"]["claim_count"] = len(d["education"]["learning_claims"])
            return d

        ok &= t("validator rejects < 2 learning claims",
                ED.education_validator("EDUCATION", _mut(learning_claims=[base["education"]["learning_claims"][0]]))[0] is False)
        ok &= t("validator rejects missing question",
                ED.education_validator("EDUCATION", _mut_claim(0, question=""))[0] is False)
        ok &= t("validator rejects missing expected",
                ED.education_validator("EDUCATION", _mut_claim(0, expected=""))[0] is False)
        ok &= t("validator rejects missing wrong_answer",
                ED.education_validator("EDUCATION", _mut_claim(0, wrong_answer=""))[0] is False)
        ok &= t("validator rejects missing maps_to (known-neighbor)",
                ED.education_validator("EDUCATION", _mut_claim(0, maps_to=""))[0] is False)
        ok &= t("validator rejects wrong_answer that equals expected",
                ED.education_validator("EDUCATION", _mut_claim(0,
                    wrong_answer=base["education"]["learning_claims"][0]["expected"]))[0] is False)
        ok &= t("validator rejects claim without depends_on (proof path missing)",
                ED.education_validator("EDUCATION", _mut_claim(0, depends_on=[]))[0] is False)
        dup = _mut_claim(1, claim_id=base["education"]["learning_claims"][0]["claim_id"])
        ok &= t("validator rejects duplicate claim_id",
                ED.education_validator("EDUCATION", dup)[0] is False)
        # hand-fed (not model-derived)
        hand = {"education": {k: v for k, v in base["education"].items()},
                "education_status": base["education_status"],
                "derived_by": "build-education::model-gate",
                "input_refs": list(base["input_refs"])}
        ok &= t("validator rejects hand-fed (not model-derived)",
                ED.education_validator("EDUCATION", hand)[0] is False)
        # wrong status
        no_status = {k: v for k, v in base.items()}
        no_status["education_status"] = "ENGINEERING_VALIDATED"
        ok &= t("validator rejects non-MACHINE_PROPOSED status",
                ED.education_validator("EDUCATION", no_status)[0] is False)
        # unresolved essay input
        ghost = {"education": {k: v for k, v in base["education"].items()},
                 "education_status": base["education_status"],
                 "derived_by": base["derived_by"], "input_refs": ["kramasadbhava:v99__arg__synth__essay"]}
        ghost["education"]["object_id"] = "kramasadbhava:v99__arg__synth__essay__educ"
        ghost["education"]["source_text"] = {"essay_id": "kramasadbhava:v99__arg__synth__essay",
                                             "synthesis_id": "kramasadbhava:v99__arg__synth",
                                             "argument_id": "kramasadbhava:v99__arg",
                                             "theme_id": "kramasadbhava__theme_1",
                                             "c1_id": "kramasadbhava:v99"}
        ok &= t("validator rejects unresolved essay input",
                ED.education_validator("EDUCATION", ghost)[0] is False)
        # unqualified essay (downgraded to GENERATED) — a SEPARATE object so the seeded
        # essay stays ENGINEERING_VALIDATED for the end-to-end commit test
        R.commit("C1", "kramasadbhava:v77", "kramasadbhava:v77", created_by="test", payload=_fake_c1("kramasadbhava:v77"))
        R.commit("ARGUMENT", "kramasadbhava:v77__arg", "kramasadbhava:v77", created_by="test",
                 payload=_fake_argument("kramasadbhava:v77"), input_refs=["kramasadbhava:v77"])
        unq_synth = R.commit("SYNTHESIS", "kramasadbhava:v77__arg__synth", "unq-hash", created_by="test",
                             payload=_fake_synthesis("kramasadbhava:v77", "kramasadbhava:v77__arg",
                                                     "kramasadbhava__theme_1", ["kramasadbhava:v77"]),
                             input_refs=["kramasadbhava:v77__arg", "kramasadbhava__theme_1"])
        unq_ep = _essay_payload(unq_synth["object_id"], "kramasadbhava:v77__arg", "kramasadbhava:v77",
                                "kramasadbhava__theme_1")
        unq_erec = R.commit("ESSAY", unq_ep["object_id"], "unq-essay-hash", created_by="test",
                            payload={"essay": unq_ep, "essay_status": "MACHINE_PROPOSED",
                                     "derived_by": "model (gateway_exec)"},
                            input_refs=[unq_synth["object_id"]])  # GENERATED, not validated
        downgrade = {"education": {k: v for k, v in base["education"].items()},
                     "education_status": base["education_status"],
                     "derived_by": base["derived_by"], "input_refs": [unq_erec["object_id"]]}
        downgrade["education"]["object_id"] = f"{unq_erec['object_id']}__educ"
        downgrade["education"]["source_text"] = {"essay_id": unq_erec["object_id"],
                                                 "synthesis_id": unq_synth["object_id"],
                                                 "argument_id": "kramasadbhava:v77__arg",
                                                 "theme_id": "kramasadbhava__theme_1",
                                                 "c1_id": "kramasadbhava:v77"}
        ok &= t("validator rejects unqualified (GENERATED) essay input",
                ED.education_validator("EDUCATION", downgrade)[0] is False)
        # depends_on id NOT a real object (fabricated)
        fab = _mut_claim(0, depends_on=["kramasadbhava:v99__arg__synth__essay"])
        ok &= t("validator rejects fabricated depends_on id (not a real object)",
                ED.education_validator("EDUCATION", fab)[0] is False)
        # depends_on id OUTSIDE the allowed set (real but unrelated)
        R.commit("C1", "kramasadbhava:v99", "kramasadbhava:v99", created_by="test", payload=_fake_c1("kramasadbhava:v99"))
        outsider = _mut_claim(0, depends_on=["kramasadbhava:v99"])
        ok &= t("validator rejects depends_on id outside the allowed proof-path set",
                ED.education_validator("EDUCATION", outsider)[0] is False)
        # spine missing: drop the essay id from the union
        no_essay_spine = _mut()
        for lc in no_essay_spine["education"]["learning_claims"]:
            lc["depends_on"] = [d for d in lc["depends_on"] if d != essay_oid]
        ok &= t("validator rejects education whose depends_on union misses the essay (spine)",
                ED.education_validator("EDUCATION", no_essay_spine)[0] is False)
        # spine missing: drop the synthesis anchor from the union
        no_synth_spine = _mut()
        for lc in no_synth_spine["education"]["learning_claims"]:
            lc["depends_on"] = [d for d in lc["depends_on"] if d != synth_oid]
        ok &= t("validator rejects education whose depends_on union misses the synthesis (spine)",
                ED.education_validator("EDUCATION", no_synth_spine)[0] is False)
        # claim_count mismatch
        bad_count = _mut(claim_count=999)
        ok &= t("validator rejects claim_count mismatch",
                ED.education_validator("EDUCATION", bad_count)[0] is False)
        # does_not_claim empty (anti-inflation)
        ok &= t("validator rejects empty does_not_claim (anti-inflation)",
                ED.education_validator("EDUCATION", _mut(does_not_claim=""))[0] is False)
        # fidelity break: key_terms dropped
        broke = _mut()
        broke["education"]["key_terms"] = []
        ok &= t("validator rejects fidelity break (key_terms dropped)",
                ED.education_validator("EDUCATION", broke)[0] is False)
        # wrong object_id
        wrong_id = _mut()
        wrong_id["education"]["object_id"] = "kramasadbhava:v3__arg__synth__essay__educ"
        ok &= t("validator rejects object_id mismatch",
                ED.education_validator("EDUCATION", wrong_id)[0] is False)
        # source_text inconsistency
        bad_st = _mut()
        bad_st["education"]["source_text"] = {"essay_id": essay_oid, "synthesis_id": synth_oid,
                                              "argument_id": arg_oid, "theme_id": "kramasadbhava__theme_1",
                                              "c1_id": "kramasadbhava:v99"}
        ok &= t("validator rejects source_text inconsistency",
                ED.education_validator("EDUCATION", bad_st)[0] is False)
        # overreach on the TRUE side: expected must not overreach the essay's license
        ok &= t("validator rejects overreach in expected (true side)",
                ED.education_validator("EDUCATION", _mut_claim(0,
                    expected="This proves the one Self is everywhere."))[0] is False)
        # overreach on maps_to (true-side label)
        ok &= t("validator rejects overreach in maps_to (true-side label)",
                ED.education_validator("EDUCATION", _mut_claim(0,
                    maps_to="always the one Self"))[0] is False)
        # the overreach lexicon is NEVER applied to wrong_answer (deliberately false side)
        ok &= t("validator does NOT gate wrong_answer by the overreach lexicon",
                ED.education_validator("EDUCATION", _mut_claim(0,
                    wrong_answer="This proves the one Self is everywhere."))[0] is True)

    # ── end-to-end: commit + gate promotion shape ────────────────────────────
    if props:
        p = props[0]
        rec = R.commit("EDUCATION", p["object_id"], p["input_hash"], created_by="test",
                       payload={"education": p["education"], "education_status": p["education_status"],
                                "derived_by": p["derived_by"]}, input_refs=p["input_refs"])
        ok &= t("committed EDUCATION record is GENERATED first", rec["status"] == R.GENERATED)
        ok &= t("is_committed() true for the canonical input hash",
                R.is_committed("EDUCATION", p["object_id"], p["input_hash"]))
        ok &= t("event ledger chain intact after commit", R.verify_event_chain())
        vok, why = ED.education_validator("EDUCATION", {
            "education": rec["payload"]["education"],
            "education_status": rec["payload"]["education_status"],
            "derived_by": rec["payload"]["derived_by"],
            "input_refs": rec["input_refs"],
        })
        ok &= t("post-commit validator re-check passes", vok, why)

    print("\n" + ("EDUCATION WORKER TESTS ALL PASS" if ok else "SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
