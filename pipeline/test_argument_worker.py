#!/usr/bin/env python3
"""pipeline/test_argument_worker.py — deterministic tests for the ARGUMENT layer worker.

Covers the model-derived ARGUMENT chain (the layer between THEME and SYNTHESIS),
with model calls STUBBED so the test is deterministic + fail-fast:
  - argument_generator assembles a MACHINE_PROPOSED proposal from model JSON
  - argument_validator PASSES on a well-formed model-derived argument
  - argument_validator REJECTS: missing inference / missing counterargument /
    crux out of range / hand-fed (no model derivation) / unresolved C1 /
    wrong status / fidelity breaks
  - model_derive_argument retries on transient empty gateway output and
    abstains (returns None) on persistent junk — never fabricates
  - canonical_input_hash is idempotent per C1 (is_committed semantics)

Run with:
  PYTHONPATH=/root/patalacheckpoints/pipeline:/root/patalacheckpoints/machinelearning/research:/root/fuck-off/lib \
  /root/venv/bin/python pipeline/test_argument_worker.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/root/patalacheckpoints/pipeline")
sys.path.insert(0, "/root/patalacheckpoints/machinelearning/research")
sys.path.insert(0, "/root/fuck-off/lib")

import object_registry as R
import argument_worker as AW


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


def _valid_model_json() -> dict:
    return {
        "conclusion": "The verse establishes that the flashing is not the order itself but has an order-less support, the great Lord.",
        "premises": [
            {"text": "The verse establishes the support of the powers."},
            {"text": "The passage establishes that the flashing is not the order itself."},
            {"text": "The passage establishes that the flashing has an order-less support, the great Lord."},
        ],
        "inference": "Since the flashing is not the order itself and ordered experience requires a support, the support must be the order-less great Lord.",
        "counterargument": "One might object that 'akrama' (order-less) is uncertain, so the verse may only establish some support within the order.",
        "crux": {"load_bearing_premise": 3, "why": "Premise 3 supplies the identification of the support as order-less great Lord."},
    }


def main() -> int:
    ok = True
    R.REG_DIR = Path(tempfile.mkdtemp())

    # seed 3 committed C1s
    for i in (1, 3, 4):
        c1 = _fake_c1(f"kramasadbhava:v{i}", "pratibhā",
                      "The verse establishes the support of the powers.")
        R.commit("C1", f"kramasadbhava:v{i}", f"kramasadbhava:v{i}", created_by="test", payload=c1)

    # ── canonical input hash: idempotent per C1, stable across commits ──────
    h1a = AW.canonical_input_hash("kramasadbhava:v1")
    h1b = AW.canonical_input_hash("kramasadbhava:v1")
    h3 = AW.canonical_input_hash("kramasadbhava:v3")
    ok &= t("canonical input hash stable for same C1", h1a == h1b)
    ok &= t("canonical input hash differs across C1s", h1a != h3)
    ok &= t("canonical input hash is sha256 of the C1 payload (not of the argument)",
            h1a == R.input_hash(R.current("C1", "kramasadbhava:v1")["payload"]))

    # ── model_derive_argument: retries on transient empty output, abstains on junk ──
    calls = {"n": 0}
    def _flaky_first(system, user, **kw):
        calls["n"] += 1
        if calls["n"] == 1:
            return {"_raw": ""}   # transient empty gateway response
        return _valid_model_json()
    orig = AW.generate_json
    AW.generate_json = _flaky_first
    res = AW.model_derive_argument("kramasadbhava:v1", max_attempts=3)
    ok &= t("model_derive retries past transient empty output", res is not None and calls["n"] >= 2,
            f"{calls['n']} calls")
    AW.generate_json = lambda system, user, **kw: {"_raw": "not json at all"}
    res = AW.model_derive_argument("kramasadbhava:v1", max_attempts=2)
    ok &= t("model_derive abstains (None) on persistent junk — never fabricates",
            res is None)
    AW.generate_json = orig

    # ── argument_generator: proposal from stubbed model JSON, MACHINE_PROPOSED ──
    AW.generate_json = lambda system, user, **kw: _valid_model_json()
    props = AW.argument_generator("ARGUMENT", [{"object_id": "kramasadbhava:v1"}])
    ok &= t("argument_generator produced a proposal", len(props) == 1, f"{len(props)}")
    if props:
        p = props[0]
        ok &= t("proposal is MACHINE_PROPOSED", p["argument_status"] == "MACHINE_PROPOSED")
        ok &= t("proposal derived_by model (gateway_exec)", p["derived_by"] == "model (gateway_exec)")
        ok &= t("proposal resolves to the C1 input_ref", p["input_refs"] == ["kramasadbhava:v1"])
        ok &= t("proposal carries fidelity fields (key_terms/uncertain/boundary)",
                p["argument"]["key_terms"] == [{"term": "pratibhā", "meaning": "the flashing"}]
                and p["argument"]["uncertain"] == ["akrama"]
                and "local support" in p["argument"]["boundary"])
        vok, why = AW.argument_validator("ARGUMENT", p)
        ok &= t("argument_validator passes on model-derived proposal", vok, why)

    # ── argument_validator fail-closed checks ────────────────────────────────
    base = props[0] if props else None
    if base:
        def _mut(**kw):
            d = {k: (v.copy() if isinstance(v, list) else v) for k, v in base.items()}
            d["argument"] = {k: (v.copy() if isinstance(v, list) else v) for k, v in base["argument"].items()}
            for k, v in kw.items():
                d["argument"][k] = v
            return d
        ok &= t("validator rejects missing inference",
                AW.argument_validator("ARGUMENT", _mut(inference=""))[0] is False)
        ok &= t("validator rejects missing counterargument",
                AW.argument_validator("ARGUMENT", _mut(counterargument=""))[0] is False)
        ok &= t("validator rejects crux out of range",
                AW.argument_validator("ARGUMENT", _mut(crux={"load_bearing_premise": 9, "why": "x"}))[0] is False)
        ok &= t("validator rejects crux index 0",
                AW.argument_validator("ARGUMENT", _mut(crux={"load_bearing_premise": 0, "why": "x"}))[0] is False)
        hand = {k: v for k, v in base.items()}
        hand["argument"] = {k: v for k, v in base["argument"].items()}
        hand["derived_by"] = "argument-layer-build"
        ok &= t("validator rejects hand-fed (not model-derived)", AW.argument_validator("ARGUMENT", hand)[0] is False)
        no_status = {k: v for k, v in base.items()}
        no_status["argument_status"] = "ENGINEERING_VALIDATED"
        ok &= t("validator rejects non-MACHINE_PROPOSED status",
                AW.argument_validator("ARGUMENT", no_status)[0] is False)
        # fidelity break: key_terms not carried from the C1
        broke = _mut()
        broke["argument"]["key_terms"] = []
        ok &= t("validator rejects fidelity break (key_terms dropped)",
                AW.argument_validator("ARGUMENT", broke)[0] is False)
        # unresolved C1
        ghost = {k: v for k, v in base.items()}
        ghost["input_refs"] = ["kramasadbhava:v99"]
        ok &= t("validator rejects unresolved input_ref C1",
                AW.argument_validator("ARGUMENT", ghost)[0] is False)

    # ── end-to-end: commit + gate promotion shape ────────────────────────────
    if props:
        p = props[0]
        rec = R.commit("ARGUMENT", p["object_id"], p["input_hash"], created_by="test",
                       payload={"argument": p["argument"], "argument_status": p["argument_status"],
                                "derived_by": p["derived_by"]}, input_refs=p["input_refs"])
        ok &= t("committed ARGUMENT record is GENERATED first", rec["status"] == R.GENERATED)
        ok &= t("is_committed() true for the canonical input hash",
                R.is_committed("ARGUMENT", p["object_id"], p["input_hash"]))
        ok &= t("event ledger chain intact after commit", R.verify_event_chain())

    print("\n" + ("ARGUMENT WORKER TESTS ALL PASS" if ok else "SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
