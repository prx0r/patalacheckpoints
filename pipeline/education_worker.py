#!/usr/bin/env python3
"""pipeline/education_worker.py — the EDUCATION layer handler (LearningClaims from essays).

Per BUILDSTATUS (POST-C1 lane) + the patala doctrine + DAG (EDUCATION requires [ESSAY]):
  - EDUCATION sits at the top of the derivational spine (… SYNTHESIS -> ESSAY -> EDUCATION).
    It teaches what the essays argue: for EVERY committed essay the MODEL derives a set of
    LEARNING CLAIMS — a mastery question + the wrong-answer→known-neighbor mapping — so a
    learner who answers wrong can be routed to the NEAREST TRUE neighbor statement and taught
    the difference (the "known neighbor" pedagogy: teach from what the learner already holds).
  - authority(EDUCATION) <= authority(ESSAY): the education text is MODEL-DERIVED (the
    generation engine: lib/gateway_exec.py -> deepseek-v4-flash via opencode-go) strictly over
    the REAL committed ESSAY (+ the SYNTHESIS/ARGUMENT/THEME/C1 it resolves to via source_text).
    It distills; it never adds new philosophy beyond the essay's license.
  - REACTIVE + INPUT QUALIFIED: education is only derived for a current ENGINEERING_VALIDATED
    ESSAY record (the qualified floor). Unqualified essays are skipped (honest abstention),
    never invented.
  - A deterministic EDUCATION validator gates the commit: education_status MACHINE_PROPOSED,
    derived_by == "model (gateway_exec)" (anti-theatre: never hand-fed), object_id ==
    <essay>__educ, input_refs == [essay_oid], INPUTS QUALIFIED (essay current +
    ENGINEERING_VALIDATED), LEARNING CLAIMS COMPLETE (>= 2 claims; every claim has claim_id /
    question / expected / wrong_answer / maps_to / depends_on; claim_id unique; wrong_answer
    differs from expected), PROOF PATHS REAL (every depends_on id resolves via R.current() in
    C1/ARGUMENT/SYNTHESIS/THEME/ESSAY AND lies inside the allowed set = the essay itself + its
    proof universe + its synthesis anchor), SPINE coverage (the union of depends_on contains the
    essay AND its synthesis — education must trace to the evidence chain), deterministic
    claim_count, anti-inflation + fidelity (does_not_claim / key_terms / uncertain / boundary
    carried from the ESSAY payload), source_text consistent, no overreach lexicon on the TRUE
    side (expected + maps_to) — the WRONG side is deliberately false, so it is never gated.
  - ENGINEERING_VALIDATED is the structural/engineering rung only; never
    SCHOLARLY_CORROBORATED / INDEPENDENT_REVIEWED (those need humans/scholarship).

Mirrors pipeline/essay_worker.py: generator + validator handlers so the autonomy controller can
wire make_education_handlers() the same way.
"""
from __future__ import annotations

import hashlib
import json
import re
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
METHOD = "MODEL_DERIVED_FROM_ESSAY_SYNTHESIS"

# overreach lexicon: words that assert beyond the essay's license. Applied ONLY to the TRUE side
# of a learning claim (expected + maps_to); wrong_answer is deliberately false by construction.
_OVERREACH = ["proves", "certainly", "definitively", "undeniably", "always",
              "it is certain", "scientifically proven", "the one Self is"]

PROMPT_SYSTEM = (
    "You are a Sanskrit philologist turned educator. You are given a committed scholarly ESSAY "
    "(already validated, proof-carrying: every paragraph rests on real object ids) plus the "
    "evidence it resolves to (SYNTHESIS / ARGUMENT / THEME / CLAIM). Derive a set of LEARNING "
    "CLAIMS that teach the essay's argument. "
    "Each learning claim has EXACTLY this shape:\n"
    "  claim_id: a short unique slug (e.g. lc-support-local).\n"
    "  question: a MASTERY QUESTION — one that tests whether the learner understands the essay's "
    "actual argument (not trivia).\n"
    "  expected: the answer the essay actually establishes, in the essay's own cautious voice "
    "(stay inside the boundary; no universal-Self inflation; respect the uncertain terms).\n"
    "  wrong_answer: a PLAUSIBLE misconception — the near-miss a careful reader might pick. It "
    "must be genuinely wrong relative to the essay (the essay's boundary / counterargument / "
    "crux usually points at it).\n"
    "  maps_to: the KNOWN-NEIGHBOR — the nearest TRUE statement that the wrong_answer actually "
    "corresponds to (a short label of the neighbor claim, e.g. 'the flashing as the order "
    "itself'). This is what a learner who picks the wrong_answer is actually thinking of, so the "
    "system can route them to that neighbor and teach the difference.\n"
    "  depends_on: the list of REAL object ids (from the ALLOWED ids given below) that this "
    "claim rests on. The ESSAY id — the document you are teaching from — MUST be first in "
    "every claim's depends_on list (the claim is about what the ESSAY establishes). Add at "
    "least one more allowed id from the evidence chain (SYNTHESIS / ARGUMENT / THEME / CLAIM) "
    "that the claim also rests on. NEVER use an id outside the ALLOWED list.\n"
    "Derive every sentence strictly from the provided texts. Do not add external claims. "
    "Produce 3-5 learning claims. Output ONLY JSON, no reasoning, no markdown. "
    'Format exactly: {"learning_claims": [{"claim_id": str, "question": str, "expected": str, '
    '"wrong_answer": str, "maps_to": str, "depends_on": [str, ...]}]}'
)


# ── input qualification ───────────────────────────────────────────────────────
def current_engineered_essays() -> list[dict]:
    """Current ESSAY records at the ENGINEERING_VALIDATED rung (the qualified floor)."""
    return [v for v in R._load("ESSAY")["objects"].values()
            for v in v if not v.get("superseded")
            and v.get("status") == R.ENGINEERING_VALIDATED]


def _essay_payload(essay_oid: str) -> dict:
    essay = R.current("ESSAY", essay_oid)
    if not essay:
        return {}
    return essay.get("payload", {}).get("essay", {}) or {}


def essay_proof_universe(essay_oid: str) -> set[str]:
    """The ids the essay itself rests on (union of every paragraph's depends_on)."""
    e = _essay_payload(essay_oid)
    out = set()
    for sec in e.get("sections") or []:
        for par in sec.get("paragraphs") or []:
            out.update(d for d in (par.get("depends_on") or []) if str(d).strip())
    return out


def allowed_depends_on(essay_oid: str) -> set[str]:
    """The ids a learning claim for this essay MAY depend on (the proof-path universe).

    = the essay itself + everything the essay rests on (its depends_on union) + the essay's
    synthesis anchor. Everything else is OUT OF SCOPE (a claim must not lean on an unrelated
    object the essay never invoked).
    """
    allowed = essay_proof_universe(essay_oid)
    allowed.add(essay_oid)
    st = _essay_payload(essay_oid).get("source_text") or {}
    if st.get("synthesis_id"):
        allowed.add(st["synthesis_id"])
    allowed.discard("")
    return allowed


def canonical_input_hash(essay_oid: str) -> str:
    """The canonical EDUCATION input hash: sha256 of the REAL current ESSAY record payload.

    Semantics: same committed essay -> same hash -> is_committed() idempotent (the pre-kanban
    education records hashed their own output, so idempotency broke).
    """
    essay = R.current("ESSAY", essay_oid)
    if not essay:
        raise KeyError(f"no current ESSAY: {essay_oid}")
    return hashlib.sha256(
        json.dumps({"essay": essay["payload"]}, sort_keys=True, ensure_ascii=False)
        .encode("utf-8")
    ).hexdigest()


# ── model derivation (generation engine; honest abstention on junk) ───────────
_last_error: list[str] = [""]


def last_error() -> str:
    return _last_error[0]


def model_derive_education(essay_oid: str, max_attempts: int = 5) -> dict | None:
    """Have the MODEL derive the learning claims from the real committed inputs.

    Returns the parsed model JSON ({learning_claims: [...]}) or None if the model is
    unavailable or returns junk after retries. The gateway occasionally returns transient
    empty content; retry with backoff before giving up (an honest abstention beats a
    fabricated education).
    """
    if not _GATEWAY:
        return None
    essay = R.current("ESSAY", essay_oid)
    if not essay:
        return None
    e = essay["payload"].get("essay", {}) or {}
    st = e.get("source_text", {}) or {}
    synth = (R.current("SYNTHESIS", st.get("synthesis_id", "")).get("payload", {}).get("synthesis", {}) or {}) if st.get("synthesis_id") else {}
    arg = (R.current("ARGUMENT", st.get("argument_id", "")).get("payload", {}).get("argument", {}) or {}) if st.get("argument_id") else {}
    c1 = (R.current("C1", st.get("c1_id", "")).get("payload", {}).get("c1", {}) or {}) if st.get("c1_id") else {}
    allowed = sorted(allowed_depends_on(essay_oid))
    section_text = []
    for sec in (e.get("sections") or [])[:8]:
        paras = []
        for p in (sec.get("paragraphs") or [])[:8]:
            paras.append(f"      [{p.get('text', '')}]  depends_on={json.dumps(p.get('depends_on') or [], ensure_ascii=False)}")
        section_text.append(f"  {sec.get('heading', '')}:\n" + "\n".join(paras))
    user = (
        f"ESSAY id: {essay_oid}\n"
        f"ESSAY title: {e.get('title', '')}\n"
        f"ESSAY conclusion: {e.get('conclusion', '')}\n"
        f"ESSAY sections:\n" + "\n".join(section_text) + "\n"
        f"ESSAY does_not_claim: {e.get('does_not_claim', '')}\n"
        f"ESSAY key_terms: {json.dumps(e.get('key_terms'), ensure_ascii=False)}\n"
        f"ESSAY uncertain: {json.dumps(e.get('uncertain'), ensure_ascii=False)}\n"
        f"ESSAY boundary: {e.get('boundary', '')}\n"
        f"ESSAY source_text: {json.dumps(st, ensure_ascii=False)}\n"
        f"REMINDER: the ESSAY id {essay_oid} is your PRIMARY source — every claim's "
        f"depends_on MUST include it first.\n"
        f"SYNTHESIS text: {synth.get('text', '')}\n"
        f"SYNTHESIS crux: {json.dumps(synth.get('crux', {}), ensure_ascii=False)}\n"
        f"ARGUMENT conclusion: {arg.get('conclusion', {}).get('text', '')}\n"
        f"ARGUMENT crux: {json.dumps(arg.get('crux', {}), ensure_ascii=False)}\n"
        f"CLAIM summary: {c1.get('summary', '')}\n"
        f"CLAIM boundary: {c1.get('boundary', '')}\n"
        f"ALLOWED depends_on ids (use ONLY these): {json.dumps(allowed, ensure_ascii=False)}"
    )
    last = None
    for attempt in range(max_attempts):
        try:
            res = generate_json(PROMPT_SYSTEM, user, max_tokens=2500, timeout=180)
            lcs = res.get("learning_claims") if isinstance(res, dict) else None
            if isinstance(lcs, list) and len(lcs) >= 1:
                return res
            last = f"structurally incomplete response: {str(res)[:200]}"
        except Exception as e:  # network / parse / timeout
            last = str(e)
        time.sleep(2 * (attempt + 1))
    if last:
        _last_error[0] = f"{essay_oid}: {last}"
    return None


# ── payload assembly (model content + deterministic metadata) ─────────────────
def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", str(s or "")).strip().lower()


def assemble_education_payload(essay_oid: str, model_res: dict) -> dict:
    """Build the registry payload from the model's JSON + deterministic metadata.

    The proof-path metadata (source_text / claim_count / does_not_claim / key_terms /
    uncertain / boundary) is assembled DETERMINISTICALLY from the real committed inputs —
    only claim_id / question / expected / wrong_answer / maps_to / depends_on come from
    the model.
    """
    essay = R.current("ESSAY", essay_oid)
    if not essay:
        raise KeyError(f"inputs unresolved: essay={essay_oid}")
    e = essay["payload"].get("essay", {}) or {}
    st = e.get("source_text", {}) or {}
    claims = []
    for lc in (model_res.get("learning_claims") or [])[:12]:
        claims.append({
            "claim_id": str(lc.get("claim_id", "")).strip(),
            "question": str(lc.get("question", "")).strip(),
            "expected": str(lc.get("expected", "")).strip(),
            "wrong_answer": str(lc.get("wrong_answer", "")).strip(),
            "maps_to": str(lc.get("maps_to", "")).strip(),
            "depends_on": [d for d in (lc.get("depends_on") or []) if str(d).strip()],
        })
    education = {
        "object_id": f"{essay_oid}__educ",
        "learning_claims": claims,
        "claim_count": len(claims),
        "method": METHOD,
        "source_text": {
            "essay_id": essay_oid,
            "synthesis_id": st.get("synthesis_id", ""),
            "argument_id": st.get("argument_id", ""),
            "theme_id": st.get("theme_id", ""),
            "c1_id": st.get("c1_id", ""),
        },
        # anti-inflation + fidelity: carried from the real ESSAY payload
        "does_not_claim": str(e.get("does_not_claim", "")).strip(),
        "key_terms": list(e.get("key_terms") or []),
        "uncertain": list(e.get("uncertain") or []),
        "boundary": str(e.get("boundary") or "").strip(),
    }
    return {
        "education": education,
        "education_status": "MACHINE_PROPOSED",
        "derived_by": DERIVED_BY,
    }


# ── deterministic gate ────────────────────────────────────────────────────────
def _resolves(oid: str) -> bool:
    """True when oid resolves to a real current record in C1/ARGUMENT/SYNTHESIS/THEME/ESSAY."""
    for layer in ("C1", "ARGUMENT", "SYNTHESIS", "THEME", "ESSAY"):
        if R.current(layer, oid):
            return True
    return False


def _essay_fidelity(essay_oid: str) -> dict:
    e = _essay_payload(essay_oid)
    return {
        "does_not_claim": str(e.get("does_not_claim", "")).strip(),
        "key_terms": list(e.get("key_terms") or []),
        "uncertain": list(e.get("uncertain") or []),
        "boundary": str(e.get("boundary") or "").strip(),
    }


def education_validator(layer: str, proposal: dict) -> tuple[bool, str]:
    """Deterministic EDUCATION gate.

    - education_status MACHINE_PROPOSED (never claims a higher state by construction)
    - derived_by == "model (gateway_exec)" (anti-theatre: never hand-fed)
    - object_id == <essay>__educ, input_refs == [essay_oid]
    - model content complete: >= 2 learning claims; every claim has claim_id / question /
      expected / wrong_answer / maps_to / depends_on; claim_id unique; wrong_answer differs
      from expected (a wrong answer that equals the expected is not a wrong answer)
    - INPUTS QUALIFIED: input_refs[0] resolves to a current ESSAY at ENGINEERING_VALIDATED
    - PROOF PATHS REAL: every depends_on id resolves via R.current() in the
      C1/ARGUMENT/SYNTHESIS/THEME/ESSAY registries AND lies inside the allowed set
    - SPINE: the union of depends_on contains the essay AND its synthesis anchor
    - deterministic claim_count == len(learning_claims)
    - anti-inflation: does_not_claim carried from the essay payload
    - fidelity: key_terms / uncertain / boundary carried from the ESSAY payload
    - source_text consistent with the essay's source_text
    - no overreach on the TRUE side (expected + maps_to); wrong_answer is deliberately
      false and is never gated by the lexicon
    """
    if proposal.get("education_status") != "MACHINE_PROPOSED":
        return False, f"education_status:{proposal.get('education_status', 'MISSING')}"
    if proposal.get("derived_by") != DERIVED_BY:
        return False, f"derived_by:{proposal.get('derived_by', 'MISSING')} (must be model (gateway_exec))"
    education = proposal.get("education", {})
    refs = proposal.get("input_refs") or []
    if len(refs) < 1:
        return False, "input_refs must be [essay_oid]"
    essay_oid = refs[0]
    if education.get("object_id") != f"{essay_oid}__educ":
        return False, f"object_id:{education.get('object_id', 'MISSING')} != {essay_oid}__educ"
    # INPUTS QUALIFIED: ENGINEERING_VALIDATED essay
    essay = R.current("ESSAY", essay_oid)
    if not essay:
        return False, f"input ESSAY unresolved: {essay_oid}"
    if essay.get("status") != R.ENGINEERING_VALIDATED:
        return False, f"input ESSAY not qualified: {essay_oid} status={essay.get('status')} (need ENGINEERING_VALIDATED)"
    # model content complete: >= 2 learning claims, every field present, claim_id unique
    claims = education.get("learning_claims") or []
    if len(claims) < 2:
        return False, "education needs >= 2 learning claims"
    seen_ids = set()
    for lc in claims:
        if not str(lc.get("claim_id", "")).strip():
            return False, "learning claim missing claim_id"
        cid = str(lc["claim_id"]).strip()
        if cid in seen_ids:
            return False, f"duplicate claim_id: {cid}"
        seen_ids.add(cid)
        if not str(lc.get("question", "")).strip():
            return False, f"learning claim {cid} missing question (mastery question)"
        if not str(lc.get("expected", "")).strip():
            return False, f"learning claim {cid} missing expected"
        if not str(lc.get("wrong_answer", "")).strip():
            return False, f"learning claim {cid} missing wrong_answer"
        if not str(lc.get("maps_to", "")).strip():
            return False, f"learning claim {cid} missing maps_to (known-neighbor)"
        if _norm(lc.get("wrong_answer")) == _norm(lc.get("expected")):
            return False, f"learning claim {cid}: wrong_answer equals expected (not a wrong answer)"
        deps = lc.get("depends_on") or []
        if not deps:
            return False, f"learning claim {cid} has no depends_on (proof path missing)"
    # PROOF PATHS REAL + in scope
    allowed = allowed_depends_on(essay_oid)
    all_deps = [d for lc in claims for d in (lc.get("depends_on") or [])]
    for d in all_deps:
        if not _resolves(d):
            return False, f"depends_on id not a real committed object: {d}"
        if d not in allowed:
            return False, f"depends_on id outside the allowed proof-path set: {d}"
    # SPINE: the education must actually trace to the essay -> synthesis chain
    union = set(all_deps)
    st = _essay_payload(essay_oid).get("source_text") or {}
    if essay_oid not in union:
        return False, f"spine id missing from depends_on union: the essay itself ({essay_oid})"
    if st.get("synthesis_id") and st["synthesis_id"] not in union:
        return False, f"spine id missing from depends_on union: synthesis {st['synthesis_id']}"
    # deterministic claim_count
    if education.get("claim_count") != len(claims):
        return False, f"claim_count:{education.get('claim_count')} != len(learning_claims) ({len(claims)})"
    # anti-inflation + fidelity carried from the essay payload
    fid = _essay_fidelity(essay_oid)
    if str(education.get("does_not_claim", "")).strip() != fid["does_not_claim"]:
        return False, "does_not_claim not carried from ESSAY (anti-inflation)"
    if list(education.get("key_terms") or []) != fid["key_terms"]:
        return False, "key_terms not carried from ESSAY (fidelity)"
    if list(education.get("uncertain") or []) != fid["uncertain"]:
        return False, "uncertain not carried from ESSAY (fidelity)"
    if str(education.get("boundary") or "").strip() != fid["boundary"]:
        return False, "boundary not carried from ESSAY (fidelity)"
    # source_text consistency
    est = education.get("source_text") or {}
    if est.get("essay_id") != essay_oid:
        return False, f"source_text.essay_id inconsistent: {est.get('essay_id')}"
    if (est.get("synthesis_id") != st.get("synthesis_id")
            or est.get("argument_id") != st.get("argument_id")
            or est.get("theme_id") != st.get("theme_id")
            or est.get("c1_id") != st.get("c1_id")):
        return False, f"source_text inconsistent with essay: {est}"
    # no overreach on the TRUE side (expected + maps_to); wrong_answer is exempt by design
    text = " ".join(
        str(lc.get("expected", "")) + " " + str(lc.get("maps_to", ""))
        for lc in claims
    ).lower()
    over = [w for w in _OVERREACH if w in text]
    if over:
        return False, f"education overreach beyond essay (expected/maps_to): {over}"
    return True, ""


# ── generator (autonomy-controller wiring) ────────────────────────────────────
def education_generator(layer: str, batch: list[dict]) -> list[dict]:
    """Model-derive ONE EDUCATION proposal (learning claims) per qualified ESSAY.

    Batch entries name ESSAY object_ids; the generator resolves each essay, derives the
    learning claims, and returns MACHINE_PROPOSED proposals with object_id / input_hash /
    input_refs / education / education_status / derived_by. Unqualified essays are skipped —
    never fabricated.
    """
    out = []
    seen = set()
    for b in batch:
        essay_oid = b.get("object_id", "")
        essay = R.current("ESSAY", essay_oid)
        if not essay or essay.get("status") != R.ENGINEERING_VALIDATED:
            continue
        if essay_oid in seen:
            continue
        seen.add(essay_oid)
        res = model_derive_education(essay_oid)
        if res is None:
            print(f"  ✗ {essay_oid}: model derivation FAILED — not fabricating ({last_error()})")
            continue
        payload = assemble_education_payload(essay_oid, res)
        out.append({
            "object_id": f"{essay_oid}__educ",
            "input_hash": canonical_input_hash(essay_oid),
            "input_refs": [essay_oid],
            "education": payload["education"],
            "education_status": payload["education_status"],
            "derived_by": payload["derived_by"],
        })
    return out


def make_education_handlers() -> dict:
    return {"generator": education_generator, "validator": education_validator}


if __name__ == "__main__":
    print("gateway available:", _GATEWAY)
    print("qualified essays:", [e["object_id"] for e in current_engineered_essays()])
