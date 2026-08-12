"""patala_ml/vertical.py — the VERTICAL OBJECT (v0, hardened): one proposition's evidence chain.

This is the working miniature of the whole Pāṭala vision (gate #3, and
`PHILOSOPHY-ENGINE-ARGUMENT-UNDER-INTERPRETATION.md` §23). It serializes one proposition and the
downward evidence/provenance layers beneath it, with **every edge typed and every resolution level
labeled honestly** — NOT a blanket "every arrow resolved".

The two structures are kept SEPARATE (they are orthogonal graphs joined by this view):
    ARGUMENT CONTEXT     ResearchQuestion → Argument → Inference → Proposition
    EVIDENCE / PROVENANCE Proposition → C1 → L2 → L0 → SourceSpan → Source, and
                          L0/SourceSpan → PhilologicalProof

Design rules (from the external review):
  - GOLD grounding is EXACT: `grounding_refs` lists explicit L0 IDs. NO substring search for gold.
    Broad term search is a SEPARATE, lower-epistemic-level `candidate_context` (a discovery aid, not evidence).
  - Every edge is a typed `GroundingLink` {from, to, relation, resolution, review_state}. "Resolved"
    never silently means five different things.
  - Proof resolution is REAL: the proof artifact is looked up on disk by chunk; a caller-supplied
    `proof_id` alone does NOT count as resolved. Unavailable/stale → UNRESOLVED / STALE.
  - C1 / L2 resolution granularity is explicit: DOCUMENT_LEVEL vs SPAN_LEVEL (exact span only when provided).
  - Missing IR fields (research_question, commitment, task_level) are surfaced, NOT retrofitted.
  - The serializer CONSUMES the L0 floor; it never builds/edits it.

This is a resolution/integrity tool, NOT a scholarly validator. It proves IDs/links resolve and are
typed; it does NOT prove the proposition is entailed, the C1/L2 spans are the reconstruction source, or
the inference is scholarly defensible.
"""
from __future__ import annotations

import json
import os
import re

IPVV = "/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv"
L0_DIR = os.path.join(IPVV, "l0")
C1_DIR = os.path.join(IPVV, "c1", "read")
PILOT_DIR = os.path.join(IPVV, "pilot")
PROOF_DIR = "/tmp/l0proof"

# typed edge relations + resolution levels (the GroundingLink vocabulary)
RELATIONS = {"TEXTUALLY_GROUNDED_BY", "INTERPRETIVELY_DERIVED_FROM", "RENDERED_BY",
             "ALIGNED_TO", "VALIDATED_BY", "CONTEXTUALIZED_BY"}
RESOLUTIONS = {"EXACT", "DOCUMENT_LEVEL", "PROPOSED", "UNRESOLVED", "STALE"}


def load_l0(chunk_id: str) -> list[dict]:
    p = os.path.join(L0_DIR, f"{chunk_id}.l0.jsonl")
    if not os.path.exists(p):
        return []
    return [json.loads(line) for line in open(p, encoding="utf-8") if line.strip()]


def norm(s: str) -> str:
    if not s:
        return ""
    s = s.lower()
    for a, b in [("ā", "a"), ("ī", "i"), ("ū", "u"), ("ṛ", "r"), ("ṝ", "r"), ("ṣ", "s"),
                 ("ś", "s"), ("ṅ", "n"), ("ñ", "n"), ("ṭ", "t"), ("ḍ", "d"), ("ṇ", "n"),
                 ("ḥ", "h"), ("ṃ", "m"), ("…", ""), (".", ""), (" ", "")]:
        s = s.replace(a, b)
    return s


def extract_sanskrit(raw_fragment: str) -> str:
    m = re.search(r"\(([^()]*)\)[\"'’\s]*$", raw_fragment or "")
    return m.group(1).strip() if m else ""


def resolve_exact_refs(records: list[dict], refs: list[str]) -> tuple[list[dict], list[str]]:
    """Exact L0-ID resolution: return the matching records + any refs that did NOT resolve."""
    by_id = {r["id"]: r for r in records}
    found, missing = [], []
    for ref in refs:
        if ref in by_id:
            found.append(by_id[ref])
        else:
            missing.append(ref)
    return found, missing


def term_candidates(records: list[dict], terms: list[str]) -> dict[str, list[dict]]:
    """Discovery-only: broad normalized substring search. NOT gold evidence (see docstring)."""
    out = {t: [] for t in terms}
    for r in records:
        lemma = norm(r.get("lemma_iast", ""))
        for t in terms:
            if t and norm(t) in lemma:
                out[t].append({
                    "l0_id": r["id"], "lemma_iast": r.get("lemma_iast"),
                    "gloss": r.get("literal_gloss"),
                    "sanskrit": extract_sanskrit(r.get("raw_fragment")),
                    "line_id": r.get("line_id"),
                    "span": [r.get("char_start"), r.get("char_end")],
                })
    return out


def _anchor_dict(r: dict) -> dict:
    return {
        "l0_id": r["id"], "line_id": r.get("line_id"), "lemma_iast": r.get("lemma_iast"),
        "gloss": r.get("literal_gloss"), "sanskrit": extract_sanskrit(r.get("raw_fragment")),
        "source_span": {"chunk": r.get("chunk_id"), "line": r.get("line_id"),
                        "char_start": r.get("char_start"), "char_end": r.get("char_end")},
    }


def load_c1_body(c1_id: str) -> str:
    p = os.path.join(C1_DIR, f"c1_{c1_id}.md")
    if not os.path.exists(p):
        return ""
    return "\n".join(l.lstrip("> ").strip() for l in open(p, encoding="utf-8")
                     if l.strip().startswith(">"))


def load_l2(l2_name: str) -> str:
    p = os.path.join(PILOT_DIR, l2_name)
    if not os.path.exists(p):
        return ""
    return open(p, encoding="utf-8").read()


def load_proof(chunk_id: str) -> dict:
    p = os.path.join(PROOF_DIR, f"{chunk_id}.l0.proof.json")
    return json.load(open(p)) if os.path.exists(p) else {}


def build_vertical(gold: dict, proposition_id: str, grounding_refs: list[str],
                   l2_name: str, proof_id: str, key_terms: list[str] | None = None,
                   c1_span: str | None = None, l2_span: str | None = None,
                   authoritative_proof_version: str | None = None) -> dict:
    """Serialize one proposition's vertical object.

    `grounding_refs`: EXACT L0 ids (gold grounding — verified to exist, no search).
    `key_terms`: optional — used ONLY for `candidate_context` (discovery, not evidence).
    `c1_span`/`l2_span`: optional exact sentence/span text, upgrading those edges to SPAN_LEVEL.
    `authoritative_proof_version`: e.g. "P0 35/35" — used to mark proof status honestly.
    """
    nodes = {n.get("proposition_id") or n.get("id"): n for n in gold.get("nodes", [])}
    prop = nodes.get(proposition_id)
    if prop is None:
        raise KeyError(f"no node {proposition_id} in gold {gold.get('gold_id')}")

    grounding = prop.get("grounding") or prop.get("source_support") or {}
    passage_id = grounding.get("passage_id") or (grounding.get("passage_ids") or [None])[0]
    chunk_id = passage_id.split(":chunk", 1)[-1] if passage_id else ""
    chunk_id = ("chunk" + chunk_id) if chunk_id else ""
    if chunk_id.endswith(".md"):
        chunk_id = chunk_id[:-3]

    def _iid(inf):
        return inf.get("inference_id") or inf.get("id")
    inferences = []
    for inf in gold.get("inferences", []):
        concl = inf.get("conclusion_ids") or ([inf["conclusion_id"]] if inf.get("conclusion_id") else [])
        if proposition_id in inf.get("premise_ids", []) or proposition_id in concl:
            role = "PREMISE" if proposition_id in inf.get("premise_ids", []) else "CONCLUSION"
            inferences.append({"inference_id": _iid(inf), "scheme": inf.get("scheme"),
                               "proposition_role": role, "premise_ids": inf.get("premise_ids"),
                               "conclusion_ids": concl})

    # ── evidence/provenance resolution ───────────────────────────────────────────
    c1_id = grounding.get("c1_id") or (grounding.get("c1_ids") or [""])[0]
    c1_body = load_c1_body(c1_id)
    l2_text = load_l2(l2_name)
    records = load_l0(chunk_id)
    direct_records, missing_refs = resolve_exact_refs(records, grounding_refs)
    candidates = term_candidates(records, key_terms or [])
    proof = load_proof(chunk_id)

    links = []
    # Proposition -> C1 (derivational). DOCUMENT_LEVEL unless an exact span is given.
    links.append({"from": proposition_id, "to": f"C1:{c1_id}", "relation": "INTERPRETIVELY_DERIVED_FROM",
                  "resolution": "SPAN_LEVEL" if c1_span else "DOCUMENT_LEVEL",
                  "review_state": "CANDIDATE"})
    # Proposition -> L2 (rendering). DOCUMENT_LEVEL unless an exact span is given.
    links.append({"from": proposition_id, "to": f"L2:{l2_name}", "relation": "RENDERED_BY",
                  "resolution": "SPAN_LEVEL" if l2_span else "DOCUMENT_LEVEL",
                  "review_state": "CANDIDATE"})
    # Proposition -> each exact L0 anchor (textual grounding). EXACT iff the ID resolved.
    for a in direct_records:
        links.append({"from": proposition_id, "to": a["id"], "relation": "TEXTUALLY_GROUNDED_BY",
                      "resolution": "EXACT", "review_state": "CANDIDATE"})
    # L0 token -> SourceSpan (exact alignment) + SourceSpan -> proof (validated by).
    for a in direct_records:
        links.append({"from": a["id"], "to": "SourceSpan", "relation": "ALIGNED_TO",
                      "resolution": "EXACT", "review_state": "CANDIDATE"})
    # PhilologicalProof resolution is REAL: load the artifact; caller-supplied ID alone is not resolved.
    if proof and authoritative_proof_version and proof.get("PASS"):
        proof_status = "REFERENCE_RESOLVED"
        proof_res = "EXACT"
    elif proof:
        proof_status = "STALE_LOCAL_ARTIFACT"
        proof_res = "STALE"
    else:
        proof_status = "PROOF_NOT_LOADED"
        proof_res = "UNRESOLVED"
    links.append({"from": "SourceSpan", "to": proof_id, "relation": "VALIDATED_BY",
                  "resolution": proof_res, "review_state": "CANDIDATE", "status": proof_status,
                  "note": "resolution=EXACT means the PROOF REFERENCE resolves exactly; it does NOT mean "
                          "the span semantically entails any proposition (that is semantic_support, "
                          "MACHINE_PROPOSED)."})

    resolved = sorted({l["resolution"] for l in links if l["resolution"] in ("EXACT", "SPAN_LEVEL", "DOCUMENT_LEVEL", "STALE")})
    unresolved = sorted({l["resolution"] for l in links if l["resolution"] in ("UNRESOLVED",)})

    return {
        "object_id": f"pt:vertical:ipvv:{chunk_id}:{proposition_id.lower()}",
        "task": "VERTICAL_OBJECT", "gold_id": gold.get("gold_id"),
        "version": "v0",
        # ARGUMENT CONTEXT (surfaced honestly — missing IR fields stay missing)
        "research_question": gold.get("research_question") or (gold.get("debate_frame") or {}).get("question"),
        "argument": {"gold_id": gold.get("gold_id"), "title": gold.get("title"),
                     "structure": gold.get("structure")},
        "inferences_using_proposition": inferences,
        "proposition": {
            "proposition_id": proposition_id,
            "text": prop.get("text") or prop.get("proposition"),
            "kind": prop.get("kind"), "explicitness": prop.get("explicitness"),
            "commitment": prop.get("commitment"), "task_level": prop.get("task_level"),
        },
        # EVIDENCE / PROVENANCE
        "c1": {"c1_id": c1_id, "resolution": "SPAN_LEVEL" if c1_span else "DOCUMENT_LEVEL",
               "exact_span": c1_span, "document_excerpt": (c1_body[:600] if not c1_span else "")},
        "l2": {"l2_id": l2_name, "resolution": "SPAN_LEVEL" if l2_span else "DOCUMENT_LEVEL",
               "exact_span": l2_span, "document_excerpt": (l2_text[:600] if not l2_span else "")},
        "direct_grounding": [_anchor_dict(a) for a in direct_records],
        "candidate_context": candidates,          # discovery only, NOT gold evidence
        "unresolved_grounding_refs": missing_refs,
        "philological_proof": {
            "proof_id": proof_id,
            "reference_resolution": proof_res,     # EXACT = the proof reference resolves exactly
            "status": proof_status,
            "semantic_support": "MACHINE_PROPOSED",  # NOT implied by reference_resolution=EXACT
            "review_status": "CANDIDATE",
            "authoritative_version": authoritative_proof_version,
            "on_disk_source_sha256": proof.get("source_sha256"),
            "on_disk_PASS": proof.get("PASS"),
            "on_disk_roundtrip": (proof.get("roundtrip") or {}).get("status"),
        },
        "passage_id": passage_id,
        "links": links,
        "resolved_resolutions": resolved,
        "unresolved_resolutions": unresolved,
    }
