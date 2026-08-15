#!/usr/bin/env python3
"""pipeline/synthesis_worker.py — the SYNTHESIS layer handler (model-derived, gated).

Per BUILDSTATUS (POST-C1 lane) + the patala doctrine:
  - SYNTHESIS sits between ARGUMENT and ESSAY on the derivational spine. It is the
    converged scholarly statement that a set of ENGINEERING_VALIDATED arguments +
    their committed THEME jointly support — NOT a paraphrase of one argument and
    NOT an essay-level thesis (those live in ESSAY, where comparison / original
    argument / modern application are allowed and must be marked).
  - authority(SYNTHESIS) <= authority(ARGUMENT/THEME): the synthesis text is MODEL-
    DERIVED (the generation engine: lib/gateway_exec.py -> deepseek-v4-flash via
    opencode-go) strictly over the REAL committed ARGUMENT + THEME (+ the C1 the
    argument resolves to). Never hand-typed, never regex-built.
  - CONVERGED + INPUTS QUALIFIED: a synthesis is only derived for a pair
    (ENGINEERING_VALIDATED argument, committed theme) where the argument's C1 is a
    member of the theme (the convergence/qualification requirement). Disconnected
    pairs are skipped (honest abstention), never invented.
  - A deterministic SYNTHESIS validator gates the commit: structural completeness
    (text / crux / unresolved), status MACHINE_PROPOSED, derived by the model,
    input_refs resolve to a qualified ENGINEERING_VALIDATED argument + committed
    theme, convergence metadata (converges_on subset of theme members, >= 2),
    anti-inflation metadata (does_not_claim non-empty), and fidelity
    (key_terms / uncertain / boundary carried from the C1).
  - ENGINEERING_VALIDATED is the structural/engineering rung only; never
    SCHOLARLY_CORROBORATED / INDEPENDENT_REVIEWED (those need humans/scholarship).

Mirrors pipeline/argument_worker.py: generator + validator handlers so the autonomy
controller can wire make_synthesis_handlers() the same way.
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
METHOD = "MODEL_DERIVED_FROM_ARGUMENT_THEME_C1"

PROMPT_SYSTEM = (
    "You are a Sanskrit philologist producing a converged scholarly synthesis from a set of "
    "already-validated inputs: an ARGUMENT (premises -> inference -> conclusion -> counterargument "
    "-> crux), its THEME dossier (member claims + boundary), and the underlying CLAIM (C1). "
    "Produce a REAL synthesis: a single statement of what the inputs JOINTLY support, the crux "
    "(the load-bearing commitment + why), and what remains UNRESOLVED. Derive every sentence "
    "strictly from the provided texts. Do not add external claims. Do not exceed the stated "
    "boundary (no essay-level thesis, no cross-tradition comparison, no modern application, no "
    "'universal Self' inflation). Flag the uncertain terms. Output ONLY JSON, no reasoning, no "
    "markdown. "
    'Format exactly: {"text": str, "crux": {"what": str, "why": str}, "unresolved": str}'
)


# ── input qualification ───────────────────────────────────────────────────────
def current_engineered_arguments() -> list[dict]:
    """Current ARGUMENT records at the ENGINEERING_VALIDATED rung (the qualified floor)."""
    return [v for v in R._load("ARGUMENT")["objects"].values()
            for v in v if not v.get("superseded")
            and v.get("status") == R.ENGINEERING_VALIDATED]


def current_themes() -> list[dict]:
    """Current (non-superseded) committed THEME records."""
    return [v for v in R._load("THEME")["objects"].values()
            for v in v if not v.get("superseded")]


def theme_member_ids(theme_rec: dict) -> list[str]:
    return [m.get("c1_id", "") for m in
            (theme_rec.get("payload", {}).get("theme", {}) or {}).get("member_claims", []) if m.get("c1_id")]


def argument_c1(argument_rec: dict) -> str:
    """The C1 an ARGUMENT resolves to (its first input_ref)."""
    refs = argument_rec.get("input_refs") or []
    return refs[0] if refs else ""


def qualified_pairs() -> list[tuple[str, str]]:
    """(arg_oid, theme_oid) pairs where the pair is QUALIFIED for synthesis.

    Qualification: the argument is current + ENGINEERING_VALIDATED, the theme is
    current + committed, and the argument's C1 is a member of the theme (so the
    synthesis really converges over inputs that are connected).
    """
    pairs = []
    for arg in current_engineered_arguments():
        c1 = argument_c1(arg)
        if not c1:
            continue
        for theme in current_themes():
            if c1 in theme_member_ids(theme):
                pairs.append((arg["object_id"], theme["object_id"]))
    return sorted(set(pairs))


def canonical_input_hash(arg_oid: str, theme_oid: str) -> str:
    """The canonical SYNTHESIS input hash: sha256 of the REAL current ARGUMENT +
    THEME record payloads.

    Semantics: same committed argument + same committed theme -> same hash ->
    is_committed() idempotent. (The pre-kanban records hashed their own output, so
    idempotency broke — same bug the ARGUMENT v2 records had.)
    """
    arg = R.current("ARGUMENT", arg_oid)
    theme = R.current("THEME", theme_oid)
    if not arg:
        raise KeyError(f"no current ARGUMENT: {arg_oid}")
    if not theme:
        raise KeyError(f"no current THEME: {theme_oid}")
    return hashlib.sha256(
        json.dumps({"argument": arg["payload"], "theme": theme["payload"]},
                   sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


# ── model derivation (generation engine; honest abstention on junk) ───────────
_last_error: list[str] = [""]


def last_error() -> str:
    return _last_error[0]


def model_derive_synthesis(arg_oid: str, theme_oid: str, max_attempts: int = 5) -> dict | None:
    """Have the MODEL derive the converged synthesis from the real committed inputs.

    Returns the parsed model JSON (text / crux / unresolved) or None if the model
    is unavailable or returns junk after retries. The gateway occasionally returns
    transient empty content; retry with backoff before giving up (an honest
    abstention beats a fabricated synthesis).
    """
    if not _GATEWAY:
        return None
    arg = R.current("ARGUMENT", arg_oid)
    theme = R.current("THEME", theme_oid)
    if not arg or not theme:
        return None
    a = arg["payload"].get("argument", {}) or {}
    t = theme["payload"].get("theme", {}) or {}
    c1_oid = argument_c1(arg)
    c1 = (R.current("C1", c1_oid).get("payload", {}).get("c1", {}) or {}) if c1_oid else {}
    user = (
        f"ARGUMENT conclusion: {a.get('conclusion', {}).get('text', '')}\n"
        f"ARGUMENT premises: {json.dumps([p.get('text','') for p in a.get('premises', [])], ensure_ascii=False)}\n"
        f"ARGUMENT inference: {a.get('inference', '')}\n"
        f"ARGUMENT counterargument: {a.get('counterargument', '')}\n"
        f"ARGUMENT crux: {json.dumps(a.get('crux', {}), ensure_ascii=False)}\n"
        f"THEME id: {t.get('theme_id', '')}\n"
        f"THEME members: {json.dumps(t.get('member_claims', []), ensure_ascii=False)}\n"
        f"THEME boundary (not_claiming): {json.dumps(t.get('boundary', {}), ensure_ascii=False)}\n"
        f"CLAIM summary: {c1.get('summary', '')}\n"
        f"CLAIM function: {c1.get('function', '')}\n"
        f"CLAIM explanation: {c1.get('explanation', '')}\n"
        f"CLAIM boundary: {c1.get('boundary', '')}\n"
        f"CLAIM key_terms: {json.dumps(c1.get('key_terms'), ensure_ascii=False)}\n"
        f"CLAIM uncertain: {json.dumps(c1.get('uncertain'), ensure_ascii=False)}"
    )
    last = None
    for attempt in range(max_attempts):
        try:
            res = generate_json(PROMPT_SYSTEM, user, max_tokens=1500, timeout=120)
            if (str(res.get("text", "")).strip()
                    and isinstance(res.get("crux"), dict)
                    and str(res.get("crux", {}).get("what", "")).strip()
                    and str(res.get("crux", {}).get("why", "")).strip()
                    and str(res.get("unresolved", "")).strip()):
                return res
            last = f"structurally incomplete response: {str(res)[:200]}"
        except Exception as e:  # network / parse / timeout
            last = str(e)
        time.sleep(2 * (attempt + 1))
    if last:
        _last_error[0] = f"{arg_oid}__{theme_oid}: {last}"
    return None


# ── payload assembly (model content + deterministic convergence metadata) ─────
def assemble_synthesis_payload(arg_oid: str, theme_oid: str, model_res: dict) -> dict:
    """Build the registry payload from the model's JSON + deterministic metadata.

    The convergence fields (converges_on / does_not_claim / source_text / fidelity)
    are assembled DETERMINISTICALLY from the real committed inputs — only the
    text / crux / unresolved come from the model.
    """
    arg = R.current("ARGUMENT", arg_oid)
    theme = R.current("THEME", theme_oid)
    if not arg or not theme:
        raise KeyError(f"inputs unresolved: arg={arg_oid} theme={theme_oid}")
    a = arg["payload"].get("argument", {}) or {}
    t = theme["payload"].get("theme", {}) or {}
    c1_oid = argument_c1(arg)
    cur_c1 = R.current("C1", c1_oid) if c1_oid else None
    c = (cur_c1["payload"].get("c1", {}) or {}) if cur_c1 else {}
    members = theme_member_ids(theme)
    crux = {
        "what": str(model_res.get("crux", {}).get("what", "")).strip(),
        "why": str(model_res.get("crux", {}).get("why", "")).strip(),
    }
    synthesis = {
        "object_id": f"{arg_oid}__synth",
        "text": str(model_res.get("text", "")).strip(),
        "crux": crux,
        "unresolved": str(model_res.get("unresolved", "")).strip(),
        "method": METHOD,
        "source_text": {"argument_id": arg_oid, "theme_id": theme_oid, "c1_id": c1_oid},
        # deterministic convergence metadata (the anti-inflation guard)
        "converges_on": sorted(members),
        "does_not_claim": str((t.get("boundary", {}) or {}).get("not_claiming", "")).strip(),
        # fidelity: carried from the real C1 payload
        "key_terms": list(c.get("key_terms") or []),
        "uncertain": list(c.get("uncertain") or []),
        "boundary": str(c.get("boundary") or "").strip(),
    }
    return {
        "synthesis": synthesis,
        "synthesis_status": "MACHINE_PROPOSED",
        "derived_by": DERIVED_BY,
    }


# ── deterministic gate ────────────────────────────────────────────────────────
def synthesis_validator(layer: str, proposal: dict) -> tuple[bool, str]:
    """Deterministic SYNTHESIS gate.

    - synthesis_status MACHINE_PROPOSED (never claims a higher state by construction)
    - derived_by == "model (gateway_exec)" (anti-theatre: never hand-fed)
    - object_id == <arg>__synth, input_refs = [arg_oid, theme_oid]
    - model content complete: text / crux.what / crux.why / unresolved
    - INPUTS QUALIFIED: input_refs[0] resolves to a current ARGUMENT at
      ENGINEERING_VALIDATED; input_refs[1] resolves to a current committed THEME
    - CONVERGED: the argument's C1 is a member of the theme; converges_on is
      non-empty, has >= 2 distinct members, all of which are theme members
    - anti-inflation: does_not_claim non-empty
    - fidelity: key_terms / uncertain / boundary carried from the C1 payload
    - source_text consistent with input_refs + the argument's C1
    """
    if proposal.get("synthesis_status") != "MACHINE_PROPOSED":
        return False, f"synthesis_status:{proposal.get('synthesis_status', 'MISSING')}"
    if proposal.get("derived_by") != DERIVED_BY:
        return False, f"derived_by:{proposal.get('derived_by', 'MISSING')} (must be model (gateway_exec))"
    synth = proposal.get("synthesis", {})
    refs = proposal.get("input_refs") or []
    if len(refs) < 2:
        return False, "input_refs must be [arg_oid, theme_oid]"
    arg_oid, theme_oid = refs[0], refs[1]
    if synth.get("object_id") != f"{arg_oid}__synth":
        return False, f"object_id:{synth.get('object_id','MISSING')} != {arg_oid}__synth"
    # model content complete
    if not str(synth.get("text", "")).strip():
        return False, "synthesis.text empty"
    crux = synth.get("crux") or {}
    if not str(crux.get("what", "")).strip() or not str(crux.get("why", "")).strip():
        return False, "synthesis.crux incomplete (need what + why)"
    if not str(synth.get("unresolved", "")).strip():
        return False, "synthesis.unresolved empty (must name what is not established)"
    # INPUTS QUALIFIED: ENGINEERING_VALIDATED argument + committed theme
    arg = R.current("ARGUMENT", arg_oid)
    if not arg:
        return False, f"input ARGUMENT unresolved: {arg_oid}"
    if arg.get("status") != R.ENGINEERING_VALIDATED:
        return False, f"input ARGUMENT not qualified: {arg_oid} status={arg.get('status')} (need ENGINEERING_VALIDATED)"
    theme = R.current("THEME", theme_oid)
    if not theme:
        return False, f"input THEME unresolved: {theme_oid}"
    # CONVERGED: the argument's C1 is a member of the theme
    c1_oid = argument_c1(arg)
    members = theme_member_ids(theme)
    if c1_oid not in members:
        return False, f"disconnected pair: argument C1 {c1_oid} not a member of theme {theme_oid}"
    converges_on = synth.get("converges_on") or []
    if len(set(converges_on)) < 2:
        return False, f"converges_on must have >= 2 distinct members (got {len(set(converges_on))})"
    if not set(converges_on).issubset(set(members)):
        return False, "converges_on has ids outside the theme members (convergence metadata inconsistent)"
    if not str(synth.get("does_not_claim", "")).strip():
        return False, "does_not_claim empty (anti-inflation guard)"
    # fidelity: key_terms / uncertain / boundary carried from the C1 payload
    cur_c1 = R.current("C1", c1_oid) if c1_oid else None
    if not cur_c1:
        return False, f"argument C1 unresolved: {c1_oid}"
    c = cur_c1["payload"].get("c1", {}) or {}
    if list(synth.get("key_terms") or []) != list(c.get("key_terms") or []):
        return False, "key_terms not carried from C1 (fidelity)"
    if list(synth.get("uncertain") or []) != list(c.get("uncertain") or []):
        return False, "uncertain not carried from C1 (fidelity)"
    if str(synth.get("boundary") or "").strip() != str(c.get("boundary") or "").strip():
        return False, "boundary not carried from C1 (fidelity)"
    # source_text consistency
    st = synth.get("source_text") or {}
    if (st.get("argument_id") != arg_oid or st.get("theme_id") != theme_oid
            or st.get("c1_id") != c1_oid):
        return False, f"source_text inconsistent: {st}"
    return True, ""


# ── generator (autonomy-controller wiring) ────────────────────────────────────
def synthesis_generator(layer: str, batch: list[dict]) -> list[dict]:
    """Model-derive ONE SYNTHESIS proposal per qualified (argument, theme) pair.

    Batch entries name ARGUMENT object_ids; the generator resolves each argument,
    finds the committed themes it is qualified for (its C1 is a member), derives a
    synthesis for each pair, and returns MACHINE_PROPOSED proposals with
    object_id / input_hash / input_refs / synthesis / synthesis_status / derived_by.
    Unqualified pairs are skipped — never fabricated.
    """
    out = []
    seen = set()
    for b in batch:
        arg_oid = b.get("object_id", "")
        arg = R.current("ARGUMENT", arg_oid)
        if not arg or arg.get("status") != R.ENGINEERING_VALIDATED:
            continue
        c1_oid = argument_c1(arg)
        for theme in current_themes():
            if c1_oid not in theme_member_ids(theme):
                continue
            theme_oid = theme["object_id"]
            pair = (arg_oid, theme_oid)
            if pair in seen:
                continue
            seen.add(pair)
            res = model_derive_synthesis(arg_oid, theme_oid)
            if res is None:
                print(f"  ✗ {arg_oid} x {theme_oid}: model derivation FAILED — not fabricating ({last_error()})")
                continue
            payload = assemble_synthesis_payload(arg_oid, theme_oid, res)
            out.append({
                "object_id": f"{arg_oid}__synth",
                "input_hash": canonical_input_hash(arg_oid, theme_oid),
                "input_refs": [arg_oid, theme_oid],
                "synthesis": payload["synthesis"],
                "synthesis_status": payload["synthesis_status"],
                "derived_by": payload["derived_by"],
            })
    return out


def make_synthesis_handlers() -> dict:
    return {"generator": synthesis_generator, "validator": synthesis_validator}


if __name__ == "__main__":
    print("gateway available:", _GATEWAY)
    print("qualified pairs (arg, theme):", qualified_pairs())
