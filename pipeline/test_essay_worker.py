#!/usr/bin/env python3
"""pipeline/test_essay_worker.py — deterministic tests for the ESSAY layer worker.

Covers the model-derived REACTIVE ESSAY chain (the layer between SYNTHESIS and
EDUCATION), with model calls STUBBED so the test is deterministic + fail-fast:
  - qualified syntheses: only current ENGINEERING_VALIDATED SYNTHESIS records
    are eligible; unqualified records are excluded
  - canonical_input_hash is idempotent per synthesis — is_committed semantics
  - model_derive_essay retries on transient empty gateway output and
    abstains (returns None) on persistent junk — never fabricates
  - essay_generator assembles a MACHINE_PROPOSED proposal from model JSON
  - essay_validator PASSES on a well-formed model-derived reactive essay
  - essay_validator REJECTS: wrong status / hand-fed / missing title / < 2 sections /
    section without heading / section without paragraphs / empty paragraph text /
    paragraph without depends_on / missing conclusion / unqualified synthesis /
    unresolved synthesis / depends_on id not a real object / depends_on id outside
    the allowed set / missing spine id (synth/arg/c1) / dependency_count mismatch /
    does_not_claim empty / fidelity break / wrong object_id / source_text
    inconsistency
  - commit + gate promotion shape: is_committed() idempotent, event chain intact

Run with:
  PYTHONPATH=/root/patalacheckpoints/pipeline:/root/patalacheckpoints/machinelearning/research:/root/fuck-off/lib \
  /root/venv/bin/python pipeline/test_essay_worker.py
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


def t(name, cond, detail=""):
    print((("PASS" if bool(cond) else "FAIL")) + " - " + name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def _fake_c1(oid: str, term: str, summary: str) -> dict:
    return {"object_id": oid, "input_hash": oid,
            "c1": {"summary": summary, "function": "introduces the support; the following argument depends on it.",
                   "explanation": "This passage establishes that the flashing is not the order itself but has an order-less support, the great Lord, and that this is required by the structure of ordered experience.",
                   "boundary": "It establishes the local support, not every claim about the universal Self.",
                   "key_terms": [{"term": term, "meaning": "the flashing"}],
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


def _valid_model_json(synth_oid: str, arg_oid: str, c1_oid: str) -> dict:
    """A well-formed reactive essay: 2 sections, paragraphs with proof paths to real ids."""
    return {
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
                  "depends_on": [synth_oid, arg_oid]},
             ]},
        ],
        "conclusion": "The verse establishes the local support of the powers, bounded and with akrama unresolved.",
    }


def _seed_registry() -> tuple[list[str], list[str], str]:
    """Seed 3 C1s + 3 ENGINEERING_VALIDATED arguments + 1 theme + 3 ENGINEERING_VALIDATED syntheses."""
    c1_ids = ["kramasadbhava:v1", "kramasadbhava:v3", "kramasadbhava:v4"]
    for oid in c1_ids:
        R.commit("C1", oid, oid, created_by="test", payload=_fake_c1(oid, "pratibhā",
                                                                     "The verse establishes the support of the powers."))
    arg_oids = []
    for oid in c1_ids:
        rec = R.commit("ARGUMENT", f"{oid}__arg", oid, created_by="test",
                       payload=_fake_argument(oid), input_refs=[oid])
        R.set_status("ARGUMENT", rec["object_id"], rec["version"], R.ENGINEERING_VALIDATED,
                     actor="test::gate")
        arg_oids.append(rec["object_id"])
    theme_rec = R.commit("THEME", "kramasadbhava__theme_1", "theme-hash",
                         created_by="test", payload=_fake_theme(c1_ids), input_refs=c1_ids)
    synth_oids = []
    for c1_oid, arg_oid in zip(c1_ids, arg_oids):
        payload = _fake_synthesis(c1_oid, arg_oid, theme_rec["object_id"], c1_ids)
        rec = R.commit("SYNTHESIS", f"{arg_oid}__synth",
                       R.input_hash({"argument": R.current("ARGUMENT", arg_oid)["payload"],
                                     "theme": R.current("THEME", theme_rec["object_id"])["payload"]}),
                       created_by="test", payload=payload, input_refs=[arg_oid, theme_rec["object_id"]])
        R.set_status("SYNTHESIS", rec["object_id"], rec["version"], R.ENGINEERING_VALIDATED,
                     actor="test::gate")
        synth_oids.append(rec["object_id"])
    return c1_ids, arg_oids, theme_rec["object_id"]


def main() -> int:
    ok = True
    R.REG_DIR = Path(tempfile.mkdtemp())

    c1_ids, arg_oids, theme_oid = _seed_registry()
    synth_oid, arg_oid, c1_oid = f"{arg_oids[0]}__synth", arg_oids[0], c1_ids[0]

    # ── canonical input hash: idempotent per synthesis ───────────────────────
    h1a = EW.canonical_input_hash(synth_oid)
    h1b = EW.canonical_input_hash(synth_oid)
    ok &= t("canonical input hash stable for same synthesis", h1a == h1b)
    ok &= t("canonical input hash is sha256 of the SYNTHESIS payload (not of the essay)",
            h1a == R.input_hash({"synthesis": R.current("SYNTHESIS", synth_oid)["payload"]}))

    # ── qualified syntheses: only ENGINEERING_VALIDATED current records ──────
    qs = EW.current_engineered_syntheses()
    ok &= t("qualified syntheses found (3)", len(qs) == 3, f"{len(qs)}")
    ok &= t("qualified syntheses are current ENGINEERING_VALIDATED",
            all(s.get("status") == R.ENGINEERING_VALIDATED and not s.get("superseded") for s in qs))

    # ── allowed depends_on: the proof-path universe ─────────────────────────
    allowed = EW.allowed_depends_on(synth_oid)
    ok &= t("allowed set contains synth + arg + theme + c1 + converges_on members",
            {synth_oid, arg_oid, theme_oid, c1_oid}.issubset(allowed)
            and set(c1_ids).issubset(allowed), f"{sorted(allowed)}")

    # ── model_derive_essay: retries on transient empty, abstains on junk ─────
    calls = {"n": 0}
    def _flaky_first(system, user, **kw):
        calls["n"] += 1
        if calls["n"] == 1:
            return {"_raw": ""}   # transient empty gateway response
        return _valid_model_json(synth_oid, arg_oid, c1_oid)
    orig = EW.generate_json
    EW.generate_json = _flaky_first
    res = EW.model_derive_essay(synth_oid, max_attempts=3)
    ok &= t("model_derive retries past transient empty output", res is not None and calls["n"] >= 2,
            f"{calls['n']} calls")
    EW.generate_json = lambda system, user, **kw: {"_raw": "not json at all"}
    res = EW.model_derive_essay(synth_oid, max_attempts=2)
    ok &= t("model_derive abstains (None) on persistent junk — never fabricates", res is None)
    EW.generate_json = orig

    # ── essay_generator: proposal from stubbed model JSON ───────────────────
    EW.generate_json = lambda system, user, **kw: _valid_model_json(synth_oid, arg_oid, c1_oid)
    props = EW.essay_generator("ESSAY", [{"object_id": o} for o in
                                         (f"{a}__synth" for a in arg_oids)])
    ok &= t("essay_generator produced a proposal per qualified synthesis", len(props) == 3, f"{len(props)}")
    if props:
        p = props[0]
        ok &= t("proposal is MACHINE_PROPOSED", p["essay_status"] == "MACHINE_PROPOSED")
        ok &= t("proposal derived_by model (gateway_exec)", p["derived_by"] == "model (gateway_exec)")
        ok &= t("proposal object_id = <synth>__essay", p["object_id"] == f"{synth_oid}__essay")
        ok &= t("proposal input_refs = [synth_oid]", p["input_refs"] == [synth_oid])
        ok &= t("proposal carries fidelity fields (key_terms/uncertain/boundary)",
                p["essay"]["key_terms"] == [{"term": "pratibhā", "meaning": "the flashing"}]
                and p["essay"]["uncertain"] == ["akrama"]
                and "local support" in p["essay"]["boundary"])
        ok &= t("proposal has >= 2 sections with depends_on proof paths",
                len(p["essay"]["sections"]) >= 2
                and all(sec.get("heading") and sec.get("paragraphs") for sec in p["essay"]["sections"])
                and all(d for sec in p["essay"]["sections"] for par in sec["paragraphs"] for d in par.get("depends_on", [])))
        ok &= t("proposal source_text consistent with the synthesis",
                p["essay"]["source_text"]["synthesis_id"] == synth_oid
                and p["essay"]["source_text"]["argument_id"] == arg_oid
                and p["essay"]["source_text"]["c1_id"] == c1_oid)
        vok, why = EW.essay_validator("ESSAY", p)
        ok &= t("essay_validator passes on model-derived proposal", vok, why)

    # ── essay_validator fail-closed checks ──────────────────────────────────
    base = props[0] if props else None
    if base:
        import copy as _copy
        def _mut(**kw):
            d = {"essay": _copy.deepcopy(base["essay"]),
                 "essay_status": base["essay_status"], "derived_by": base["derived_by"],
                 "input_refs": list(base["input_refs"])}
            for k, v in kw.items():
                d["essay"][k] = v
            return d

        ok &= t("validator rejects missing title",
                EW.essay_validator("ESSAY", _mut(title=""))[0] is False)
        ok &= t("validator rejects < 2 sections",
                EW.essay_validator("ESSAY", _mut(sections=[base["essay"]["sections"][0]]))[0] is False)
        no_heading = _mut()
        no_heading["essay"]["sections"][1]["heading"] = ""
        ok &= t("validator rejects section without heading",
                EW.essay_validator("ESSAY", no_heading)[0] is False)
        no_paras = _mut()
        no_paras["essay"]["sections"][1]["paragraphs"] = []
        ok &= t("validator rejects section without paragraphs",
                EW.essay_validator("ESSAY", no_paras)[0] is False)
        empty_para = _mut()
        empty_para["essay"]["sections"][1]["paragraphs"][0]["text"] = ""
        ok &= t("validator rejects empty paragraph text",
                EW.essay_validator("ESSAY", empty_para)[0] is False)
        no_deps = _mut()
        no_deps["essay"]["sections"][1]["paragraphs"][0]["depends_on"] = []
        ok &= t("validator rejects paragraph without depends_on (proof path missing)",
                EW.essay_validator("ESSAY", no_deps)[0] is False)
        ok &= t("validator rejects missing conclusion",
                EW.essay_validator("ESSAY", _mut(conclusion=""))[0] is False)
        # hand-fed (not model-derived)
        hand = {"essay": {k: v for k, v in base["essay"].items()},
                "essay_status": base["essay_status"], "derived_by": "build-essay::model-gate",
                "input_refs": list(base["input_refs"])}
        ok &= t("validator rejects hand-fed (not model-derived)",
                EW.essay_validator("ESSAY", hand)[0] is False)
        # wrong status
        no_status = {k: v for k, v in base.items()}
        no_status["essay_status"] = "ENGINEERING_VALIDATED"
        ok &= t("validator rejects non-MACHINE_PROPOSED status",
                EW.essay_validator("ESSAY", no_status)[0] is False)
        # unresolved synthesis input
        ghost = {"essay": {k: v for k, v in base["essay"].items()},
                 "essay_status": base["essay_status"], "derived_by": base["derived_by"],
                 "input_refs": ["kramasadbhava:v99__arg__synth"]}
        ghost["essay"]["object_id"] = "kramasadbhava:v99__arg__synth__essay"
        ghost["essay"]["source_text"] = {"synthesis_id": "kramasadbhava:v99__arg__synth",
                                         "argument_id": "kramasadbhava:v99__arg",
                                         "theme_id": theme_oid, "c1_id": "kramasadbhava:v99"}
        ok &= t("validator rejects unresolved synthesis input",
                EW.essay_validator("ESSAY", ghost)[0] is False)
        # unqualified synthesis (downgraded to GENERATED) — a SEPARATE object so the
        # v1 synthesis stays ENGINEERING_VALIDATED for the end-to-end commit test
        R.commit("C1", "kramasadbhava:v77", "kramasadbhava:v77", created_by="test",
                 payload=_fake_c1("kramasadbhava:v77", "other", "unrelated claim"))
        R.commit("ARGUMENT", "kramasadbhava:v77__arg", "kramasadbhava:v77", created_by="test",
                 payload=_fake_argument("kramasadbhava:v77"), input_refs=["kramasadbhava:v77"])
        unq_rec = R.commit("SYNTHESIS", "kramasadbhava:v77__arg__synth", "unq-hash", created_by="test",
                           payload=_fake_synthesis("kramasadbhava:v77", "kramasadbhava:v77__arg",
                                                   theme_oid, c1_ids),
                           input_refs=["kramasadbhava:v77__arg", theme_oid])  # GENERATED, not validated
        downgrade = {"essay": {k: v for k, v in base["essay"].items()},
                     "essay_status": base["essay_status"], "derived_by": base["derived_by"],
                     "input_refs": [unq_rec["object_id"]]}
        downgrade["essay"]["object_id"] = f"{unq_rec['object_id']}__essay"
        downgrade["essay"]["source_text"] = {"synthesis_id": unq_rec["object_id"],
                                             "argument_id": "kramasadbhava:v77__arg",
                                             "theme_id": theme_oid, "c1_id": "kramasadbhava:v77"}
        ok &= t("validator rejects unqualified (GENERATED) synthesis input",
                EW.essay_validator("ESSAY", downgrade)[0] is False)
        # depends_on id NOT a real object (fabricated)
        fab = _mut()
        fab["essay"]["sections"][0]["paragraphs"][0]["depends_on"] = ["kramasadbhava:v99__arg__synth"]
        ok &= t("validator rejects fabricated depends_on id (not a real object)",
                EW.essay_validator("ESSAY", fab)[0] is False)
        # depends_on id OUTSIDE the allowed set (real but unrelated)
        outsider = _mut()
        outsider["essay"]["sections"][0]["paragraphs"][0]["depends_on"] = ["kramasadbhava:v99"]
        R.commit("C1", "kramasadbhava:v99", "kramasadbhava:v99", created_by="test",
                 payload=_fake_c1("kramasadbhava:v99", "other", "unrelated claim"))
        ok &= t("validator rejects depends_on id outside the allowed proof-path set",
                EW.essay_validator("ESSAY", outsider)[0] is False)
        # spine missing: drop the C1 from the union
        no_spine = _mut()
        for sec in no_spine["essay"]["sections"]:
            for par in sec["paragraphs"]:
                par["depends_on"] = [d for d in par["depends_on"] if d != c1_oid]
        ok &= t("validator rejects essay whose depends_on union misses the C1 (spine)",
                EW.essay_validator("ESSAY", no_spine)[0] is False)
        # dependency_count mismatch
        bad_count = _mut(dependency_count=999)
        ok &= t("validator rejects dependency_count mismatch",
                EW.essay_validator("ESSAY", bad_count)[0] is False)
        # does_not_claim empty (anti-inflation)
        ok &= t("validator rejects empty does_not_claim (anti-inflation)",
                EW.essay_validator("ESSAY", _mut(does_not_claim=""))[0] is False)
        # fidelity break: key_terms dropped
        broke = _mut()
        broke["essay"]["key_terms"] = []
        ok &= t("validator rejects fidelity break (key_terms dropped)",
                EW.essay_validator("ESSAY", broke)[0] is False)
        # wrong object_id
        wrong_id = _mut()
        wrong_id["essay"]["object_id"] = "kramasadbhava:v3__arg__synth__essay"
        ok &= t("validator rejects object_id mismatch",
                EW.essay_validator("ESSAY", wrong_id)[0] is False)
        # source_text inconsistency
        bad_st = _mut()
        bad_st["essay"]["source_text"] = {"synthesis_id": synth_oid, "argument_id": arg_oid,
                                          "theme_id": theme_oid, "c1_id": "kramasadbhava:v99"}
        ok &= t("validator rejects source_text inconsistency",
                EW.essay_validator("ESSAY", bad_st)[0] is False)

    # ── end-to-end: commit + gate promotion shape ───────────────────────────
    if props:
        p = props[0]
        rec = R.commit("ESSAY", p["object_id"], p["input_hash"], created_by="test",
                       payload={"essay": p["essay"], "essay_status": p["essay_status"],
                                "derived_by": p["derived_by"]}, input_refs=p["input_refs"])
        ok &= t("committed ESSAY record is GENERATED first", rec["status"] == R.GENERATED)
        ok &= t("is_committed() true for the canonical input hash",
                R.is_committed("ESSAY", p["object_id"], p["input_hash"]))
        ok &= t("event ledger chain intact after commit", R.verify_event_chain())
        vok, why = EW.essay_validator("ESSAY", {
            "essay": rec["payload"]["essay"],
            "essay_status": rec["payload"]["essay_status"],
            "derived_by": rec["payload"]["derived_by"],
            "input_refs": rec["input_refs"],
        })
        ok &= t("post-commit validator re-check passes", vok, why)

    print("\n" + ("ESSAY WORKER TESTS ALL PASS" if ok else "SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
