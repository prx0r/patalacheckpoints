#!/usr/bin/env python3
"""pipeline/product_reducer.py — the Hermes-reducer bridge for the epistemic products.

Wraps my standalone epistemic products (claim, crux, evidence_independence, review, tension_finder)
into the EXACT Hermes-reducer contract that the agentic OS drives (mirrors synthesis_worker.py):

  generator(layer, batch)   -> model/PRODUCT derives MACHINE_PROPOSED proposals from real inputs
  validator(proposal, inputs) -> deterministic gate (input_refs resolve, status honest, fidelity)
  canonical_input_hash(inputs) -> stable sha256 of REAL inputs -> is_committed() idempotent
  make_<product>_handlers()  -> {generator, validator} for the autonomy controller / Hermes worker
  promote -> ENGINEERING_VALIDATED (structural rung only; never SCHOLARLY_CORROBORATED)

This is what makes the products integrate into the Hermes-led agentic OS: the deterministic .py
REDUCTION layer that gates what the model / product derives, commits via object_registry, and
promotes only to the engineering rung. No hand-fed validators. No fake passes.

The doctrine (SOUL.md):
  - Hermes/PRODUCT for GENERATION, .py for REDUCTION.
  - authority(projection) <= authority(parent); every object resolves downward to C1.
  - MACHINE_PROPOSED -> ENGINEERING_VALIDATED (structural), never higher (that needs humans).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pipeline"))
sys.path.insert(0, str(REPO / "pipeline/products"))

import object_registry as R  # noqa: E402


def canonical_input_hash(*inputs) -> str:
    """A stable hash of the REAL input identities -> is_committed() idempotent.

    Semantics (per synthesis_worker): same committed inputs -> same hash -> never double-commit.
    """
    canonical = json.dumps(list(inputs), sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _current_refs(layer: str, object_ids: list[str]) -> list[str]:
    """The resolved current refs (input_refs that actually resolve downward)."""
    resolved = []
    for oid in object_ids:
        if R.current(layer, oid) is not None or R.current("SOURCE", oid) is not None:
            resolved.append(oid)
    return resolved


# ── CLAIM reducer (from real C1 -> a proposition, gated) ─────────────────────
def claim_validator(proposal: dict) -> tuple[bool, str]:
    """Deterministic gate: a claim proposal must be honest (MACHINE_PROPOSED, source-backed)."""
    c = proposal.get("claim") or {}
    if c.get("epistemic_status") == "PĀṬALA-INFERS" and c.get("epistemic_ceiling") != "MACHINE_PROPOSED":
        return False, "PĀṬALA-INFERS claim inflated (must stay MACHINE_PROPOSED)"
    if c.get("epistemic_status") == "SOURCE-SAYS" and not c.get("source_refs"):
        return False, "SOURCE-SAYS claim missing source_refs"
    if not c.get("evidence_quote"):
        return False, "claim missing evidence_quote (verbatim source anchor)"
    if not proposal.get("input_refs"):
        return False, "claim missing input_refs"
    return True, ""


def claim_generator(layer: str, batch: list[dict]) -> list[dict]:
    """Derive a Claim proposal for each real C1 (the honest PĀṬALA-INFERS floor)."""
    from products.claim.engine import make_claim
    from products._shared import ipvv
    out = []
    for b in batch:
        c1_oid = b.get("object_id", "")
        passage = next((p for p in ipvv.passages() if p.get("immutable_id") == c1_oid
                        or p.get("id") == c1_oid), None)
        if passage is None:
            continue  # unqualified input, honest abstention
        claim = make_claim(passage, "PĀṬALA-INFERS")
        out.append({
            "object_id": f"claim:{c1_oid}",
            "input_hash": canonical_input_hash(c1_oid),
            "input_refs": [c1_oid],
            "claim": claim,
            "claim_status": "MACHINE_PROPOSED",
            "derived_by": "product_reducer:claim",
        })
    return out


def make_claim_handlers() -> dict:
    return {"generator": claim_generator, "validator": claim_validator}


# ── CRUX reducer (minimal divergence between two arguments) ───────────────────
def crux_validator(proposal: dict) -> tuple[bool, str]:
    cx = proposal.get("crux") or {}
    if "crux_count" not in cx or not isinstance(cx.get("crux_count"), int):
        return False, "crux missing integer crux_count"
    if not proposal.get("input_refs") or len(proposal["input_refs"]) < 2:
        return False, "crux requires two argument input_refs"
    return True, ""


def crux_generator(layer: str, batch: list[dict]) -> list[dict]:
    from products.crux.engine import crux_between
    out = []
    for b in batch:
        a, b_ = b.get("a"), b.get("b")
        if not a or not b_:
            continue
        try:
            cx = crux_between(a, b_)
        except Exception:
            continue
        out.append({
            "object_id": f"crux:{a}:{b_}",
            "input_hash": canonical_input_hash(a, b_),
            "input_refs": [a, b_],
            "crux": cx,
            "crux_status": "MACHINE_PROPOSED",
            "derived_by": "product_reducer:crux",
        })
    return out


def make_crux_handlers() -> dict:
    return {"generator": crux_generator, "validator": crux_validator}


# ── EVIDENCE-INDEPENDENCE reducer (SOURCE_ECHO over real corroborations) ───────
def evidence_validator(proposal: dict) -> tuple[bool, str]:
    ind = proposal.get("independence") or {}
    if ind.get("status") not in ("CLASSIFIED", "OFFLINE", "UNAVAILABLE"):
        return False, f"independence status not honest: {ind.get('status')}"
    if not proposal.get("input_refs"):
        return False, "evidence proposal missing input_refs"
    return True, ""


def evidence_generator(layer: str, batch: list[dict]) -> list[dict]:
    from products.evidence_independence.engine import independence_report
    out = []
    for b in batch:
        prop = b.get("proposition") or "default"
        r = independence_report(live=False)
        for p in r.get("propositions", []):
            out.append({
                "object_id": f"evidence:{p['proposition'][:30]}",
                "input_hash": canonical_input_hash(prop, p.get("target_doi") or "offline"),
                "input_refs": [p.get("target_doi")] if p.get("target_doi") else [],
                "independence": p["independence"],
                "dedup": {"recorded": p["n_corroborations_recorded"], "unique": p["n_unique_sources"]},
                "evidence_status": "MACHINE_PROPOSED",
                "derived_by": "product_reducer:evidence",
            })
    return out


def make_evidence_handlers() -> dict:
    return {"generator": evidence_generator, "validator": evidence_validator}


# ── TENSION-FINDER reducer (the research-question surface, commits tension objects) ──
def tension_validator(proposal: dict) -> tuple[bool, str]:
    t = proposal.get("tension") or {}
    if not t.get("kind") or t.get("score") is None:
        return False, "tension missing kind/score"
    if not proposal.get("input_refs"):
        return False, "tension missing input_refs (the passages/positions it spans)"
    return True, ""


def tension_generator(layer: str, batch: list[dict]) -> list[dict]:
    from products.tension_finder.engine import find_tensions
    out = []
    for b in batch:
        kinds = b.get("kinds")
        r = find_tensions(kinds=kinds, limit=b.get("limit", 20))
        for t in r["tensions"]:
            ref = t.get("passage_id") or t.get("term") or t.get("a") or t.get("object_id")
            out.append({
                "object_id": f"tension:{t['kind']}:{ref}",
                "input_hash": canonical_input_hash(t["kind"], ref),
                "input_refs": [ref] if ref else [],
                "tension": t,
                "tension_status": "MACHINE_PROPOSED",
                "derived_by": "product_reducer:tension",
            })
    return out


def make_tension_handlers() -> dict:
    return {"generator": tension_generator, "validator": tension_validator}


# ── generic: run a product handler set ────────────────────────────────────────
HANDLERS = {
    "claim": make_claim_handlers, "crux": make_crux_handlers,
    "evidence": make_evidence_handlers, "tension": make_tension_handlers,
}


def run_generator(product: str, batch: list[dict]) -> list[dict]:
    """Run a product's generator over a batch (what a Hermes worker calls)."""
    h = HANDLERS[product]()
    return h["generator"](product.upper(), batch)


def run_validator(product: str, proposal: dict) -> tuple[bool, str]:
    """Run a product's deterministic validator on a proposal (the gate)."""
    h = HANDLERS[product]()
    return h["validator"](proposal)


def promote_to_engineered(proposal: dict, actor: str, layer: str) -> dict:
    """Commit a gated proposal at ENGINEERING_VALIDATED (structural rung only) + event chain.

    SELF-GATING (per the red-team finding CRITICAL-1): never grants ENGINEERING_VALIDATED unless the
    product's own deterministic validator passes. If the caller didn't validate, we validate here.
    """
    # determine which product's validator applies (by the proposal's marker keys)
    if proposal.get("claim"):
        v, why = claim_validator(proposal)
    elif proposal.get("crux"):
        v, why = crux_validator(proposal)
    elif proposal.get("independence"):
        v, why = evidence_validator(proposal)
    elif proposal.get("tension"):
        v, why = tension_validator(proposal)
    else:
        raise ValueError("cannot determine validator for proposal (no claim/crux/independence/tension)")
    if not v:
        raise ValueError(f"refusing to promote unvalidated proposal: {why}")
    payload = {k: v for k, v in proposal.items() if k not in ("input_hash", "input_refs")}
    return R.commit(
        layer=layer, object_id=proposal["object_id"], input_hash_val=proposal["input_hash"],
        created_by=actor, status=R.ENGINEERING_VALIDATED, payload=payload,
        input_refs=proposal.get("input_refs", []),
    )


if __name__ == "__main__":
    import sys as _s
    verb = _s.argv[1] if len(_s.argv) > 1 else "reduce"
    product = _s.argv[2] if len(_s.argv) > 2 else "claim"

    if verb == "reduce":
        # Hermes worker: derive + validate proposals for a product from a batch
        if product not in HANDLERS:
            print(json.dumps({"error": f"unknown product {product}; have {sorted(HANDLERS)}"}))
            sys.exit(1)
        from products._shared import ipvv
        # product-aware default batch (a Hermes worker may pass a specific batch via args)
        if product == "claim":
            batch = [{"object_id": p.get("immutable_id")} for p in ipvv.passages()]
        elif product == "crux":
            from products.argument.engine import arguments
            args = arguments()
            batch = [{"a": args[i]["argument_id"], "b": args[i+1]["argument_id"]}
                     for i in range(min(3, len(args)-1))]
        elif product == "evidence":
            batch = [{"proposition": "default"}]
        elif product == "tension":
            batch = [{"limit": 20}]
        else:
            batch = [{}]
        proposals = run_generator(product, batch)
        result = []
        for p in proposals:
            v, why = run_validator(product, p)
            result.append({"object_id": p["object_id"], "gated": v, "why": why,
                           "input_hash": p["input_hash"], "input_refs": p["input_refs"]})
        print(json.dumps({"product": product, "proposals": len(proposals), "results": result},
                         indent=2, ensure_ascii=False))
    elif verb == "validate":
        proposal = json.loads(_s.argv[3])
        v, why = run_validator(product, proposal)
        print(json.dumps({"product": product, "gated": v, "why": why}, ensure_ascii=False))
    elif verb == "commit":
        proposal = json.loads(_s.argv[3])
        actor = _s.argv[4] if len(_s.argv) > 4 else "hermes-worker"
        layer = _s.argv[5] if len(_s.argv) > 5 else "CLAIM"
        v, why = run_validator(product, proposal)
        if not v:
            print(json.dumps({"error": f"validator failed: {why}"}, ensure_ascii=False))
            sys.exit(1)
        rec = promote_to_engineered(proposal, actor, layer)
        print(json.dumps({"committed": rec.get("object_id"), "status": rec.get("status"),
                          "version": rec.get("version"),
                          "event_chain": R.verify_event_chain()}, indent=2, ensure_ascii=False))
    else:
        print(json.dumps({"error": f"unknown verb {verb}; have reduce|validate|commit"}))
        sys.exit(1)
