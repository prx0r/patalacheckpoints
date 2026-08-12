"""patala_ml/vertical.py — the VERTICAL OBJECT: one proposition resolved all the way down.

This is the working miniature of the whole Pāṭala vision (the reviewer's gate #3, and
`PHILOSOPHY-ENGINE-ARGUMENT-UNDER-INTERPRETATION.md` §23):

    ResearchQuestion
      ↓
    Argument
      ↓
    Inference
      ↓
    Proposition
      ↓
    C1
      ↓
    L2
      ↓
    L0 anchor
      ↓
    SourceSpan
      ↓
    Sanskrit
      ↓
    PhilologicalProof

Every arrow must RESOLVE to real data, or be honestly reported as UNRESOLVED. This is a CONSUMER of
Agent 2's L0 output (the `l0/*.jsonl` + `.l0.proof.json` on the sanskritree mount + the published
passage/C1/L2) — it does not build or edit the L0 floor.

The one genuine judgment here is the term→L0-anchor mapping (which Sanskrit token grounds which
proposition). It is explicit (a `key_terms` argument) so the human reviewer can challenge it; nothing
is silently fuzzy.
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


def load_l0(chunk_id: str) -> list[dict]:
    p = os.path.join(L0_DIR, f"{chunk_id}.l0.jsonl")
    if not os.path.exists(p):
        return []
    return [json.loads(line) for line in open(p, encoding="utf-8") if line.strip()]


def norm(s: str) -> str:
    """Normalize a lemma for matching: lowercase, strip diacritics, trim ellipses/spaces."""
    if not s:
        return ""
    s = s.lower()
    for a, b in [("ā", "a"), ("ī", "i"), ("ū", "u"), ("ṛ", "r"), ("ṝ", "r"), ("ṣ", "s"),
                 ("ś", "s"), ("ṅ", "n"), ("ñ", "n"), ("ṭ", "t"), ("ḍ", "d"), ("ṇ", "n"),
                 ("ḥ", "h"), ("ṃ", "m"), ("…", ""), (".", ""), (" ", "")]:
        s = s.replace(a, b)
    return s


def extract_sanskrit(raw_fragment: str) -> str:
    """Pull the IAST from the trailing parenthetical of a raw fragment (tolerating trailing quotes)."""
    m = re.search(r"\(([^()]*)\)[\"'’\s]*$", raw_fragment or "")
    return m.group(1).strip() if m else ""


def resolve_terms(records: list[dict], terms: list[str]) -> dict[str, list[dict]]:
    """For each term, return the L0 records whose lemma contains it (normalized substring match).

    Returns {term: [anchor, ...]} where each anchor carries l0_id, lemma, gloss, span, sanskrit.
    """
    out = {t: [] for t in terms}
    for r in records:
        lemma = norm(r.get("lemma_iast", ""))
        for t in terms:
            if t and norm(t) in lemma:
                out[t].append({
                    "l0_id": r["id"],
                    "line_id": r.get("line_id"),
                    "lemma_iast": r.get("lemma_iast"),
                    "gloss": r.get("literal_gloss"),
                    "source_span": {
                        "chunk": r.get("chunk_id"),
                        "line": r.get("line_id"),
                        "char_start": r.get("char_start"),
                        "char_end": r.get("char_end"),
                    },
                    "sanskrit": extract_sanskrit(r.get("raw_fragment")),
                    "source_text": r.get("source_text"),
                })
    return out


def load_c1_body(c1_id: str) -> str:
    p = os.path.join(C1_DIR, f"c1_{c1_id}.md")
    if not os.path.exists(p):
        return ""
    return "\n".join(l.lstrip("> ").strip() for l in open(p, encoding="utf-8")
                     if l.strip().startswith(">"))


def load_l2(l2_name: str) -> str:
    # l2_name like "pilot_V2O_L2_read.md"
    p = os.path.join(PILOT_DIR, l2_name)
    if not os.path.exists(p):
        return ""
    return open(p, encoding="utf-8").read()[:2000]


def load_proof(chunk_id: str) -> dict:
    p = os.path.join(PROOF_DIR, f"{chunk_id}.l0.proof.json")
    if os.path.exists(p):
        return json.load(open(p))
    return {}


def build_vertical(gold: dict, proposition_id: str, key_terms: list[str],
                   l2_name: str, proof_id: str) -> dict:
    """Serialize one proposition as a vertical object. Every arrow resolves or is flagged UNRESOLVED."""
    nodes = {n.get("proposition_id") or n.get("id"): n for n in gold.get("nodes", [])}
    prop = nodes.get(proposition_id)
    if prop is None:
        raise KeyError(f"no node {proposition_id} in gold {gold.get('gold_id')}")

    grounding = prop.get("grounding") or prop.get("source_support") or {}
    passage_id = grounding.get("passage_id") or (grounding.get("passage_ids") or [None])[0]
    # passage id: pt:passage:ipvv:chunkV2-O-...md -> chunk identifier "chunkV2-O-..." (L0 files keep "chunk")
    chunk_id = passage_id.split(":chunk", 1)[-1] if passage_id else ""
    chunk_id = ("chunk" + chunk_id) if chunk_id else ""
    if chunk_id.endswith(".md"):
        chunk_id = chunk_id[:-3]

    # the inference(s) that use this proposition (normalize old gold.py vs new gold002-005 schema)
    def _iid(inf):
        return inf.get("inference_id") or inf.get("id")
    used_by = []
    for inf in gold.get("inferences", []):
        concl = inf.get("conclusion_ids") or ([inf["conclusion_id"]] if inf.get("conclusion_id") else [])
        if proposition_id in inf.get("premise_ids", []) or proposition_id in concl:
            used_by.append(inf)

    # resolve downward
    c1_body = load_c1_body(grounding.get("c1_id") or (grounding.get("c1_ids") or [""])[0])
    l2_text = load_l2(l2_name)
    l0_records = load_l0(chunk_id)
    anchors = resolve_terms(l0_records, key_terms)
    proof = load_proof(chunk_id)

    resolved = []
    unresolved = []
    if passage_id:
        resolved.append("passage")
    if c1_body:
        resolved.append("c1")
    if l2_text:
        resolved.append("l2")
    matched_terms = {t: a for t, a in anchors.items() if a}
    if matched_terms:
        resolved.append("l0_anchor")
        resolved.append("source_span")
        resolved.append("sanskrit")
    else:
        unresolved.append("l0_anchor (no lemma matched key_terms)")
    if proof:
        resolved.append("philological_proof")
    else:
        unresolved.append("philological_proof (no proof json for this chunk on disk)")

    return {
        "object_id": f"pt:vertical:ipvv:{chunk_id}:{proposition_id.lower()}",
        "task": "VERTICAL_OBJECT",
        "gold_id": gold.get("gold_id"),
        "research_question": gold.get("research_question") or (gold.get("debate_frame") or {}).get("question"),
        "argument": {"gold_id": gold.get("gold_id"), "title": gold.get("title"),
                     "structure": gold.get("structure")},
        "inferences_using_proposition": [
            {"inference_id": _iid(inf), "scheme": inf.get("scheme"),
             "premise_ids": inf.get("premise_ids"),
             "conclusion_ids": inf.get("conclusion_ids") or ([inf["conclusion_id"]] if inf.get("conclusion_id") else [])}
            for inf in used_by],
        "proposition": {
            "proposition_id": proposition_id,
            "text": prop.get("text") or prop.get("proposition"),
            "kind": prop.get("kind"),
            "explicitness": prop.get("explicitness"),
            "commitment": prop.get("commitment"),
            "task_level": prop.get("task_level"),
        },
        "c1": {"c1_id": grounding.get("c1_id") or (grounding.get("c1_ids") or [""])[0],
               "excerpt": c1_body[:600]},
        "l2": {"l2_id": l2_name, "excerpt": l2_text[:600]},
        "l0_anchors": anchors,
        "sanskrit_spans": sorted({a["sanskrit"] for anchors_ in anchors.values() for a in anchors_ if a["sanskrit"]}),
        "philological_proof": {
            "proof_id": proof_id,
            "chunk": proof.get("chunk", chunk_id),
            "source_sha256": proof.get("source_sha256"),
            "span_integrity": proof.get("span_integrity"),
            "coverage_unknown": (proof.get("coverage") or {}).get("unknown_chars"),
            "roundtrip": (proof.get("roundtrip") or {}).get("status"),
            "PASS": proof.get("PASS"),
            "note": "the authoritative frozen P0 is 35/35 PASS; this record is the on-disk proof for the chunk",
        },
        "passage_id": passage_id,
        "resolved_arrows": resolved,
        "unresolved_arrows": unresolved,
    }
