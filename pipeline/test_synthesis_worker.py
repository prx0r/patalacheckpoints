#!/usr/bin/env python3
"""pipeline/test_synthesis_worker.py — deterministic tests for the SYNTHESIS layer worker.

Covers the model-derived SYNTHESIS chain (the layer between ARGUMENT and ESSAY),
with model calls STUBBED so the test is deterministic + fail-fast:
  - qualified_pairs: only (ENGINEERING_VALIDATED argument x committed theme) pairs
    whose C1 is a theme member are eligible; disconnected pairs are excluded
  - canonical_input_hash is idempotent per (argument, theme) — is_committed semantics
  - model_derive_synthesis retries on transient empty gateway output and
    abstains (returns None) on persistent junk — never fabricates
  - synthesis_generator assembles a MACHINE_PROPOSED proposal from model JSON
  - synthesis_validator PASSES on a well-formed model-derived synthesis
  - synthesis_validator REJECTS: wrong status / hand-fed / missing text / missing
    crux / missing unresolved / unqualified argument (not ENGINEERING_VALIDATED) /
    unresolved theme / disconnected pair / converges_on < 2 / does_not_claim empty /
    fidelity breaks / wrong object_id / source_text inconsistency
  - commit + gate promotion shape: is_committed() idempotent, event chain intact

Run with:
  PYTHONPATH=/root/patalacheckpoints/pipeline:/root/patalacheckpoints/machinelearning/research:/root/fuck-off/lib \
  /root/venv/bin/python pipeline/test_synthesis_worker.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/root/patalacheckpoints/pipeline")
sys.path.insert(0, "/root/patalacheckpoints/machinelearning/research")
sys.path.insert(0, "/root/fuck-off/lib")

import object_registry as R
import synthesis_worker as SW


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
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
    """A well-formed ENGINEERING_VALIDATED argument record for c1_oid."""
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


def _valid_model_json() -> dict:
    return {
        "text": "The three member claims jointly establish that the flashing (pratibhā) is not the order itself but has an order-less support, the great Lord, and that this support is required by the structure of ordered experience. The synthesis is bounded to this local support.",
        "crux": {"what": "The load-bearing commitment is that the flashing has an order-less support, the great Lord.",
                 "why": "If this identification is removed, the other inputs only describe the flashing's relation to order and cannot establish the support of the powers."},
        "unresolved": "The precise sense of akrama remains uncertain, so the character of the order-less support is not fully determined.",
    }


def _seed_registry() -> tuple[list[str], str, str]:
    """Seed 3 committed C1s + 1 ENGINEERING_VALIDATED argument per C1 + 1 committed theme."""
    c1_ids = ["kramasadbhava:v1", "kramasadbhava:v3", "kramasadbhava:v4"]
    for oid in c1_ids:
        c1 = _fake_c1(oid, "pratibhā", "The verse establishes the support of the powers.")
        R.commit("C1", oid, oid, created_by="test", payload=c1)
    arg_oids = []
    for oid in c1_ids:
        payload = _fake_argument(oid)
        rec = R.commit("ARGUMENT", f"{oid}__arg", oid, created_by="test",
                       payload=payload, input_refs=[oid])
        R.set_status("ARGUMENT", rec["object_id"], rec["version"], R.ENGINEERING_VALIDATED,
                     actor="test::gate")
        arg_oids.append(rec["object_id"])
    theme_rec = R.commit("THEME", "kramasadbhava__theme_1", "theme-hash",
                         created_by="test", payload=_fake_theme(c1_ids),
                         input_refs=c1_ids)
    return c1_ids, arg_oids[0], theme_rec["object_id"]


def main() -> int:
    ok = True
    R.REG_DIR = Path(tempfile.mkdtemp())

    c1_ids, arg_oid, theme_oid = _seed_registry()

    # ── canonical input hash: idempotent per (argument, theme) ────────────────
    h1a = SW.canonical_input_hash(arg_oid, theme_oid)
    h1b = SW.canonical_input_hash(arg_oid, theme_oid)
    ok &= t("canonical input hash stable for same (arg, theme)", h1a == h1b)
    ok &= t("canonical input hash is sha256 of arg+theme payloads (not of the synthesis)",
            h1a == R.input_hash({"argument": R.current("ARGUMENT", arg_oid)["payload"],
                                 "theme": R.current("THEME", theme_oid)["payload"]}))

    # ── qualified_pairs: only connected, qualified pairs ─────────────────────
    pairs = SW.qualified_pairs()
    ok &= t("qualified_pairs finds the 3 connected pairs", len(pairs) == 3, f"{pairs}")
    ok &= t("qualified pairs are (arg, theme) with member C1",
            all(a.startswith("kramasadbhava:v") and t == theme_oid for a, t in pairs))

    # ── model_derive_synthesis: retries on transient empty, abstains on junk ──
    calls = {"n": 0}
    def _flaky_first(system, user, **kw):
        calls["n"] += 1
        if calls["n"] == 1:
            return {"_raw": ""}   # transient empty gateway response
        return _valid_model_json()
    orig = SW.generate_json
    SW.generate_json = _flaky_first
    res = SW.model_derive_synthesis(arg_oid, theme_oid, max_attempts=3)
    ok &= t("model_derive retries past transient empty output", res is not None and calls["n"] >= 2,
            f"{calls['n']} calls")
    SW.generate_json = lambda system, user, **kw: {"_raw": "not json at all"}
    res = SW.model_derive_synthesis(arg_oid, theme_oid, max_attempts=2)
    ok &= t("model_derive abstains (None) on persistent junk — never fabricates", res is None)
    SW.generate_json = orig

    # ── synthesis_generator: proposal from stubbed model JSON ────────────────
    SW.generate_json = lambda system, user, **kw: _valid_model_json()
    props = SW.synthesis_generator("SYNTHESIS", [{"object_id": o} for o in
                                                 (f"{c}__arg" for c in c1_ids)])
    ok &= t("synthesis_generator produced a proposal per pair", len(props) == 3, f"{len(props)}")
    if props:
        p = props[0]
        ok &= t("proposal is MACHINE_PROPOSED", p["synthesis_status"] == "MACHINE_PROPOSED")
        ok &= t("proposal derived_by model (gateway_exec)", p["derived_by"] == "model (gateway_exec)")
        ok &= t("proposal object_id = arg__synth", p["object_id"] == f"{arg_oid}__synth")
        ok &= t("proposal input_refs = [arg, theme]", p["input_refs"] == [arg_oid, theme_oid])
        ok &= t("proposal carries fidelity fields (key_terms/uncertain/boundary)",
                p["synthesis"]["key_terms"] == [{"term": "pratibhā", "meaning": "the flashing"}]
                and p["synthesis"]["uncertain"] == ["akrama"]
                and "local support" in p["synthesis"]["boundary"])
        ok &= t("proposal converges_on = theme members (>= 2)",
                len(p["synthesis"]["converges_on"]) >= 2
                and set(p["synthesis"]["converges_on"]) == set(c1_ids))
        ok &= t("proposal does_not_claim non-empty (anti-inflation)",
                bool(p["synthesis"]["does_not_claim"]))
        vok, why = SW.synthesis_validator("SYNTHESIS", p)
        ok &= t("synthesis_validator passes on model-derived proposal", vok, why)

    # ── synthesis_validator fail-closed checks ───────────────────────────────
    base = props[0] if props else None
    if base:
        def _mut(**kw):
            d = {k: (v.copy() if isinstance(v, list) else v) for k, v in base.items()}
            d["synthesis"] = {k: (v.copy() if isinstance(v, list) else v) for k, v in base["synthesis"].items()}
            for k, v in kw.items():
                d["synthesis"][k] = v
            return d
        ok &= t("validator rejects missing text",
                SW.synthesis_validator("SYNTHESIS", _mut(text=""))[0] is False)
        ok &= t("validator rejects missing crux.what",
                SW.synthesis_validator("SYNTHESIS", _mut(crux={"what": "", "why": "x"}))[0] is False)
        ok &= t("validator rejects missing crux.why",
                SW.synthesis_validator("SYNTHESIS", _mut(crux={"what": "x", "why": ""}))[0] is False)
        ok &= t("validator rejects missing unresolved",
                SW.synthesis_validator("SYNTHESIS", _mut(unresolved=""))[0] is False)
        hand = {k: v for k, v in base.items()}
        hand["synthesis"] = {k: v for k, v in base["synthesis"].items()}
        hand["derived_by"] = "build-synthesis::model-gate"
        ok &= t("validator rejects hand-fed (not model-derived)",
                SW.synthesis_validator("SYNTHESIS", hand)[0] is False)
        no_status = {k: v for k, v in base.items()}
        no_status["synthesis_status"] = "ENGINEERING_VALIDATED"
        ok &= t("validator rejects non-MACHINE_PROPOSED status",
                SW.synthesis_validator("SYNTHESIS", no_status)[0] is False)
        # unqualified argument (downgraded to GENERATED)
        ghost_arg = R.current("ARGUMENT", arg_oid)
        downgrade = {k: v for k, v in base.items()}
        downgrade["input_refs"] = ["kramasadbhava:v99__arg", theme_oid]
        downgrade["synthesis"] = {k: v for k, v in base["synthesis"].items()}
        downgrade["synthesis"]["object_id"] = "kramasadbhava:v99__arg__synth"
        downgrade["synthesis"]["source_text"] = {"argument_id": "kramasadbhava:v99__arg",
                                                 "theme_id": theme_oid, "c1_id": "kramasadbhava:v99"}
        ok &= t("validator rejects unresolved argument input",
                SW.synthesis_validator("SYNTHESIS", downgrade)[0] is False)
        # disconnected pair: arg C1 not a theme member
        outsider = R.commit("C1", "kramasadbhava:v99", "kramasadbhava:v99", created_by="test",
                            payload=_fake_c1("kramasadbhava:v99", "other", "unrelated claim"))
        rec99 = R.commit("ARGUMENT", "kramasadbhava:v99__arg", "kramasadbhava:v99",
                         created_by="test", payload=_fake_argument("kramasadbhava:v99"),
                         input_refs=["kramasadbhava:v99"])
        R.set_status("ARGUMENT", rec99["object_id"], rec99["version"], R.ENGINEERING_VALIDATED,
                     actor="test::gate")
        SW.generate_json = lambda system, user, **kw: _valid_model_json()
        ghost_props = SW.synthesis_generator("SYNTHESIS", [{"object_id": "kramasadbhava:v99__arg"}])
        ok &= t("generator abstains on disconnected pair (not a theme member)",
                len(ghost_props) == 0, f"{len(ghost_props)}")
        # converges_on < 2
        ok &= t("validator rejects converges_on < 2",
                SW.synthesis_validator("SYNTHESIS", _mut(converges_on=["kramasadbhava:v1"]))[0] is False)
        # does_not_claim empty
        ok &= t("validator rejects empty does_not_claim (anti-inflation)",
                SW.synthesis_validator("SYNTHESIS", _mut(does_not_claim=""))[0] is False)
        # fidelity break: key_terms dropped
        broke = _mut()
        broke["synthesis"]["key_terms"] = []
        ok &= t("validator rejects fidelity break (key_terms dropped)",
                SW.synthesis_validator("SYNTHESIS", broke)[0] is False)
        # wrong object_id
        wrong_id = _mut()
        wrong_id["synthesis"]["object_id"] = "kramasadbhava:v3__arg__synth"
        ok &= t("validator rejects object_id mismatch",
                SW.synthesis_validator("SYNTHESIS", wrong_id)[0] is False)
        # source_text inconsistency
        bad_st = _mut()
        bad_st["synthesis"]["source_text"] = {"argument_id": arg_oid, "theme_id": theme_oid,
                                              "c1_id": "kramasadbhava:v99"}
        ok &= t("validator rejects source_text inconsistency",
                SW.synthesis_validator("SYNTHESIS", bad_st)[0] is False)

    # ── end-to-end: commit + gate promotion shape ────────────────────────────
    if props:
        p = props[0]
        rec = R.commit("SYNTHESIS", p["object_id"], p["input_hash"], created_by="test",
                       payload={"synthesis": p["synthesis"], "synthesis_status": p["synthesis_status"],
                                "derived_by": p["derived_by"]}, input_refs=p["input_refs"])
        ok &= t("committed SYNTHESIS record is GENERATED first", rec["status"] == R.GENERATED)
        ok &= t("is_committed() true for the canonical input hash",
                R.is_committed("SYNTHESIS", p["object_id"], p["input_hash"]))
        ok &= t("event ledger chain intact after commit", R.verify_event_chain())
        vok, why = SW.synthesis_validator("SYNTHESIS", {
            "synthesis": rec["payload"]["synthesis"],
            "synthesis_status": rec["payload"]["synthesis_status"],
            "derived_by": rec["payload"]["derived_by"],
            "input_refs": rec["input_refs"],
        })
        ok &= t("post-commit validator re-check passes", vok, why)

    print("\n" + ("SYNTHESIS WORKER TESTS ALL PASS" if ok else "SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
