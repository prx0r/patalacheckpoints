#!/usr/bin/env python3
"""pipeline/essay_worker.py — the ESSAY layer handler (reactive, proof-carrying prose).

Per BUILDSTATUS (POST-C1 lane) + the patala doctrine + DAG (ESSAY requires [SYNTHESIS]):
  - ESSAY sits between SYNTHESIS and EDUCATION on the derivational spine. It is the
    REACTIVE scholarly essay derived from a set of ENGINEERING_VALIDATED syntheses:
    sections whose paragraphs carry `depends_on` PROOF PATHS to REAL committed
    C1/ARGUMENT/SYNTHESIS ids (never fabricated, never hand-typed).
  - authority(ESSAY) <= authority(SYNTHESIS): the essay text is MODEL-DERIVED (the
    generation engine: lib/gateway_exec.py -> deepseek-v4-flash via opencode-go)
    strictly over the REAL committed SYNTHESIS (+ the ARGUMENT + THEME + C1 it
    resolves to). Comparison / original argument / modern application are allowed
    HERE (unlike in C1/SYNTHESIS) but must stay inside the carried boundary.
  - REACTIVE + INPUT QUALIFIED: an essay is only derived for a current
    ENGINEERING_VALIDATED SYNTHESIS record (the qualified floor). Unqualified
    syntheses are skipped (honest abstention), never invented.
  - A deterministic ESSAY validator gates the commit: structural completeness
    (title / >= 2 sections / every section heading + >= 1 paragraph / every
    paragraph text + depends_on / conclusion), status MACHINE_PROPOSED, derived by
    the model, input_refs resolve to a qualified ENGINEERING_VALIDATED synthesis,
    PROOF PATHS REAL (every depends_on id resolves via R.current() in the
    C1/ARGUMENT/SYNTHESIS/THEME registries and lies inside the allowed set), SPINE
    coverage (the union of depends_on contains the synthesis, its argument and its
    C1 — the essay must actually trace to the evidence), anti-inflation
    (does_not_claim carried from the synthesis), fidelity (key_terms / uncertain /
    boundary carried from the SYNTHESIS payload), deterministic dependency_count.
  - ENGINEERING_VALIDATED is the structural/engineering rung only; never
    SCHOLARLY_CORROBORATED / INDEPENDENT_REVIEWED (those need humans/scholarship).

Mirrors pipeline/synthesis_worker.py: generator + validator handlers so the autonomy
controller can wire make_essay_handlers() the same way.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pipeline"))
sys.path.insert(0, str(REPO / "machinelearning/research"))
sys.path.insert(0, "/root/fuck-off/lib")  # the PROVEN generation engine (gateway_exec)

import object_registry as R  # noqa: E402

try:
    from gateway_exec import generate_json  # noqa: E402
    _GATEWAY = True
except Exception as _e:  # pragma: no cover
    _GATEWAY = False
    _GATEWAY_ERR = str(_e)

DERIVED_BY = "model (gateway_exec)"
METHOD = "MODEL_DERIVED_FROM_SYNTHESIS_ARGUMENT_C1"

PROMPT_SYSTEM = (
    "You are a Sanskrit philologist writing a REACTIVE scholarly essay from a set of "
    "already-validated inputs: a SYNTHESIS (converged statement + crux + unresolved), "
    "its ARGUMENT (premises -> inference -> conclusion -> counterargument -> crux), its "
    "THEME dossier (member claims + boundary), and the underlying CLAIM (C1). "
    "Produce a REAL essay in SECTIONS: each section has a heading and paragraphs; every "
    "paragraph carries depends_on — the list of real object ids (from the ALLOWED ids "
    "given below) that the paragraph's claims rest on. Derive every sentence strictly "
    "from the provided texts. Do not add external claims. Do not exceed the stated "
    "boundary (no universal-Self inflation; the essay may add its own framing/application "
    "only where it stays inside the boundary and is presented as the essay's own, not as "
    "what the primary text establishes). Flag the uncertain terms. Output ONLY JSON, no "
    "reasoning, no markdown. "
    'Format exactly: {"title": str, "sections": [{"id": str, "heading": str, '
    '"paragraphs": [{"text": str, "depends_on": [str, ...]}]}], "conclusion": str}'
)


# ── input qualification ───────────────────────────────────────────────────────
def current_engineered_syntheses() -> list[dict]:
    """Current SYNTHESIS records at the ENGINEERING_VALIDATED rung (the qualified floor)."""
    return [v for v in R._load("SYNTHESIS")["objects"].values()
            for v in v if not v.get("superseded")
            and v.get("status") == R.ENGINEERING_VALIDATED]


def synthesis_source_text(synth_oid: str) -> dict:
    """The synthesis's own source_text {argument_id, theme_id, c1_id}."""
    synth = R.current("SYNTHESIS", synth_oid)
    if not synth:
        return {}
    return (synth.get("payload", {}).get("synthesis", {}) or {}).get("source_text", {}) or {}


def allowed_depends_on(synth_oid: str) -> set[str]:
    """The ids an essay for this synthesis MAY depend on (the proof-path universe).

    = the synthesis itself + its argument + its theme + its C1 + every theme-member
    C1 it converges on. Everything else is OUT OF SCOPE (a paragraph must not lean on
    an unrelated object).
    """
    allowed = {synth_oid}
    st = synthesis_source_text(synth_oid)
    allowed.update(v for v in st.values() if v)
    synth = R.current("SYNTHESIS", synth_oid)
    if synth:
        s = synth.get("payload", {}).get("synthesis", {}) or {}
        allowed.update(s.get("converges_on") or [])
    allowed.discard("")
    return allowed


def canonical_input_hash(synth_oid: str) -> str:
    """The canonical ESSAY input hash: sha256 of the REAL current SYNTHESIS record payload.

    Semantics: same committed synthesis -> same hash -> is_committed() idempotent
    (the pre-kanban essay records hashed their own output, so idempotency broke).
    """
    synth = R.current("SYNTHESIS", synth_oid)
    if not synth:
        raise KeyError(f"no current SYNTHESIS: {synth_oid}")
    return hashlib.sha256(
        json.dumps({"synthesis": synth["payload"]}, sort_keys=True, ensure_ascii=False)
        .encode("utf-8")
    ).hexdigest()


# ── model derivation (generation engine; honest abstention on junk) ───────────
_last_error: list[str] = [""]


def last_error() -> str:
    return _last_error[0]


def model_derive_essay(synth_oid: str, max_attempts: int = 5) -> dict | None:
    """Have the MODEL derive the reactive essay from the real committed inputs.

    Returns the parsed model JSON (title / sections / conclusion) or None if the model
    is unavailable or returns junk after retries. The gateway occasionally returns
    transient empty content; retry with backoff before giving up (an honest
    abstention beats a fabricated essay).
    """
    if not _GATEWAY:
        return None
    synth = R.current("SYNTHESIS", synth_oid)
    if not synth:
        return None
    s = synth["payload"].get("synthesis", {}) or {}
    st = s.get("source_text", {}) or {}
    arg_oid, theme_oid, c1_oid = st.get("argument_id", ""), st.get("theme_id", ""), st.get("c1_id", "")
    arg = (R.current("ARGUMENT", arg_oid).get("payload", {}).get("argument", {}) or {}) if arg_oid else {}
    theme = (R.current("THEME", theme_oid).get("payload", {}).get("theme", {}) or {}) if theme_oid else {}
    c1 = (R.current("C1", c1_oid).get("payload", {}).get("c1", {}) or {}) if c1_oid else {}
    allowed = sorted(allowed_depends_on(synth_oid))
    user = (
        f"SYNTHESIS id: {synth_oid}\n"
        f"SYNTHESIS text: {s.get('text', '')}\n"
        f"SYNTHESIS crux: {json.dumps(s.get('crux', {}), ensure_ascii=False)}\n"
        f"SYNTHESIS unresolved: {s.get('unresolved', '')}\n"
        f"SYNTHESIS does_not_claim: {s.get('does_not_claim', '')}\n"
        f"SYNTHESIS converges_on: {json.dumps(s.get('converges_on', []), ensure_ascii=False)}\n"
        f"ARGUMENT conclusion: {arg.get('conclusion', {}).get('text', '')}\n"
        f"ARGUMENT premises: {json.dumps([p.get('text','') for p in arg.get('premises', [])], ensure_ascii=False)}\n"
        f"ARGUMENT inference: {arg.get('inference', '')}\n"
        f"ARGUMENT crux: {json.dumps(arg.get('crux', {}), ensure_ascii=False)}\n"
        f"THEME members: {json.dumps(theme.get('member_claims', []), ensure_ascii=False)}\n"
        f"THEME boundary (not_claiming): {json.dumps(theme.get('boundary', {}), ensure_ascii=False)}\n"
        f"CLAIM summary: {c1.get('summary', '')}\n"
        f"CLAIM function: {c1.get('function', '')}\n"
        f"CLAIM explanation: {c1.get('explanation', '')}\n"
        f"CLAIM boundary: {c1.get('boundary', '')}\n"
        f"CLAIM key_terms: {json.dumps(c1.get('key_terms'), ensure_ascii=False)}\n"
        f"CLAIM uncertain: {json.dumps(c1.get('uncertain'), ensure_ascii=False)}\n"
        f"ALLOWED depends_on ids (use ONLY these): {json.dumps(allowed, ensure_ascii=False)}"
    )
    last = None
    for attempt in range(max_attempts):
        try:
            res = generate_json(PROMPT_SYSTEM, user, max_tokens=2500, timeout=180)
            if (str(res.get("title", "")).strip()
                    and isinstance(res.get("sections"), list) and len(res["sections"]) >= 2
                    and str(res.get("conclusion", "")).strip()):
                return res
            last = f"structurally incomplete response: {str(res)[:200]}"
        except Exception as e:  # network / parse / timeout
            last = str(e)
        time.sleep(2 * (attempt + 1))
    if last:
        _last_error[0] = f"{synth_oid}: {last}"
    return None


# ── payload assembly (model content + deterministic metadata) ─────────────────
def _paragraph_depends_on(section: dict) -> list[str]:
    return [d for p in section.get("paragraphs", []) for d in (p.get("depends_on") or [])]


def assemble_essay_payload(synth_oid: str, model_res: dict) -> dict:
    """Build the registry payload from the model's JSON + deterministic metadata.

    The proof-path metadata (source_text / dependency_count / does_not_claim /
    key_terms / uncertain / boundary) is assembled DETERMINISTICALLY from the real
    committed inputs — only title / sections / conclusion come from the model.
    """
    synth = R.current("SYNTHESIS", synth_oid)
    if not synth:
        raise KeyError(f"inputs unresolved: synth={synth_oid}")
    s = synth["payload"].get("synthesis", {}) or {}
    st = s.get("source_text", {}) or {}
    sections = []
    for sec in (model_res.get("sections") or [])[:8]:
        sections.append({
            "id": str(sec.get("id", "")).strip(),
            "heading": str(sec.get("heading", "")).strip(),
            "paragraphs": [{
                "text": str(p.get("text", "")).strip(),
                "depends_on": [d for d in (p.get("depends_on") or []) if str(d).strip()],
            } for p in (sec.get("paragraphs") or [])[:8]],
        })
    all_deps = [d for sec in sections for d in _paragraph_depends_on(sec)]
    essay = {
        "object_id": f"{synth_oid}__essay",
        "title": str(model_res.get("title", "")).strip(),
        "sections": sections,
        "conclusion": str(model_res.get("conclusion", "")).strip(),
        "dependency_count": len(set(all_deps)),
        "method": METHOD,
        "source_text": {"synthesis_id": synth_oid, **{k: v for k, v in st.items() if k in ("argument_id", "theme_id", "c1_id")}},
        # anti-inflation + fidelity: carried from the real SYNTHESIS payload
        "does_not_claim": str(s.get("does_not_claim", "")).strip(),
        "key_terms": list(s.get("key_terms") or []),
        "uncertain": list(s.get("uncertain") or []),
        "boundary": str(s.get("boundary") or "").strip(),
    }
    return {
        "essay": essay,
        "essay_status": "MACHINE_PROPOSED",
        "derived_by": DERIVED_BY,
    }


# ── deterministic gate ────────────────────────────────────────────────────────
def _resolves(oid: str) -> bool:
    """True when oid resolves to a real current record in C1/ARGUMENT/SYNTHESIS/THEME."""
    for layer in ("C1", "ARGUMENT", "SYNTHESIS", "THEME"):
        if R.current(layer, oid):
            return True
    return False


def essay_validator(layer: str, proposal: dict) -> tuple[bool, str]:
    """Deterministic ESSAY gate.

    - essay_status MACHINE_PROPOSED (never claims a higher state by construction)
    - derived_by == "model (gateway_exec)" (anti-theatre: never hand-fed)
    - object_id == <synth>__essay, input_refs = [synth_oid]
    - model content complete: title, >= 2 sections, each section heading + >= 1
      paragraph, each paragraph text + depends_on, conclusion
    - INPUTS QUALIFIED: input_refs[0] resolves to a current SYNTHESIS at
      ENGINEERING_VALIDATED
    - PROOF PATHS REAL: every depends_on id resolves via R.current() in the
      C1/ARGUMENT/SYNTHESIS/THEME registries AND lies inside the allowed set
    - SPINE: the union of depends_on contains the synthesis, its argument and its C1
    - deterministic dependency_count == distinct depends_on ids
    - anti-inflation: does_not_claim carried from the synthesis payload
    - fidelity: key_terms / uncertain / boundary carried from the SYNTHESIS payload
    - source_text consistent with the synthesis's source_text
    """
    if proposal.get("essay_status") != "MACHINE_PROPOSED":
        return False, f"essay_status:{proposal.get('essay_status', 'MISSING')}"
    if proposal.get("derived_by") != DERIVED_BY:
        return False, f"derived_by:{proposal.get('derived_by', 'MISSING')} (must be model (gateway_exec))"
    essay = proposal.get("essay", {})
    refs = proposal.get("input_refs") or []
    if len(refs) < 1:
        return False, "input_refs must be [synth_oid]"
    synth_oid = refs[0]
    if essay.get("object_id") != f"{synth_oid}__essay":
        return False, f"object_id:{essay.get('object_id', 'MISSING')} != {synth_oid}__essay"
    # model content complete
    if not str(essay.get("title", "")).strip():
        return False, "essay.title empty"
    sections = essay.get("sections") or []
    if len(sections) < 2:
        return False, "essay needs >= 2 sections (reactive essay structure)"
    for sec in sections:
        if not str(sec.get("heading", "")).strip():
            return False, "section missing heading"
        paras = sec.get("paragraphs") or []
        if not paras:
            return False, "section has no paragraphs"
        for p in paras:
            if not str(p.get("text", "")).strip():
                return False, "paragraph text empty"
            deps = p.get("depends_on") or []
            if not deps:
                return False, "paragraph has no depends_on (proof path missing)"
    if not str(essay.get("conclusion", "")).strip():
        return False, "essay.conclusion empty"
    # INPUTS QUALIFIED: ENGINEERING_VALIDATED synthesis
    synth = R.current("SYNTHESIS", synth_oid)
    if not synth:
        return False, f"input SYNTHESIS unresolved: {synth_oid}"
    if synth.get("status") != R.ENGINEERING_VALIDATED:
        return False, f"input SYNTHESIS not qualified: {synth_oid} status={synth.get('status')} (need ENGINEERING_VALIDATED)"
    # PROOF PATHS REAL + in scope
    allowed = allowed_depends_on(synth_oid)
    all_deps = [d for sec in sections for d in _paragraph_depends_on(sec)]
    for d in all_deps:
        if not _resolves(d):
            return False, f"depends_on id not a real committed object: {d}"
        if d not in allowed:
            return False, f"depends_on id outside the allowed proof-path set: {d}"
    # SPINE: the essay must actually trace to synthesis -> argument -> C1
    union = set(all_deps)
    st = synthesis_source_text(synth_oid)
    for spine_id in (synth_oid, st.get("argument_id", ""), st.get("c1_id", "")):
        if spine_id and spine_id not in union:
            return False, f"spine id missing from depends_on union: {spine_id}"
    # deterministic dependency_count
    if essay.get("dependency_count") != len(union):
        return False, f"dependency_count:{essay.get('dependency_count')} != distinct depends_on ids ({len(union)})"
    # anti-inflation + fidelity carried from the synthesis payload
    s = synth["payload"].get("synthesis", {}) or {}
    if str(essay.get("does_not_claim", "")).strip() != str(s.get("does_not_claim", "")).strip():
        return False, "does_not_claim not carried from SYNTHESIS (anti-inflation)"
    if list(essay.get("key_terms") or []) != list(s.get("key_terms") or []):
        return False, "key_terms not carried from SYNTHESIS (fidelity)"
    if list(essay.get("uncertain") or []) != list(s.get("uncertain") or []):
        return False, "uncertain not carried from SYNTHESIS (fidelity)"
    if str(essay.get("boundary") or "").strip() != str(s.get("boundary") or "").strip():
        return False, "boundary not carried from SYNTHESIS (fidelity)"
    # source_text consistency
    est = essay.get("source_text") or {}
    if est.get("synthesis_id") != synth_oid:
        return False, f"source_text.synthesis_id inconsistent: {est.get('synthesis_id')}"
    if (est.get("argument_id") != st.get("argument_id")
            or est.get("theme_id") != st.get("theme_id")
            or est.get("c1_id") != st.get("c1_id")):
        return False, f"source_text inconsistent with synthesis: {est}"
    return True, ""


# ── generator (autonomy-controller wiring) ────────────────────────────────────
def essay_generator(layer: str, batch: list[dict]) -> list[dict]:
    """Model-derive ONE reactive ESSAY proposal per qualified SYNTHESIS.

    Batch entries name SYNTHESIS object_ids; the generator resolves each synthesis,
    derives an essay, and returns MACHINE_PROPOSED proposals with object_id /
    input_hash / input_refs / essay / essay_status / derived_by. Unqualified
    syntheses are skipped — never fabricated.
    """
    out = []
    seen = set()
    for b in batch:
        synth_oid = b.get("object_id", "")
        synth = R.current("SYNTHESIS", synth_oid)
        if not synth or synth.get("status") != R.ENGINEERING_VALIDATED:
            continue
        if synth_oid in seen:
            continue
        seen.add(synth_oid)
        res = model_derive_essay(synth_oid)
        if res is None:
            print(f"  ✗ {synth_oid}: model derivation FAILED — not fabricating ({last_error()})")
            continue
        payload = assemble_essay_payload(synth_oid, res)
        out.append({
            "object_id": f"{synth_oid}__essay",
            "input_hash": canonical_input_hash(synth_oid),
            "input_refs": [synth_oid],
            "essay": payload["essay"],
            "essay_status": payload["essay_status"],
            "derived_by": payload["derived_by"],
        })
    return out


def make_essay_handlers() -> dict:
    return {"generator": essay_generator, "validator": essay_validator}


if __name__ == "__main__":
    print("gateway available:", _GATEWAY)
    print("qualified syntheses:", [s["object_id"] for s in current_engineered_syntheses()])
