#!/usr/bin/env python3
"""pipeline/c1_worker.py — the C1 layer handler (passage commentary).

Per C1-SPEC (translations/_stack/ipvv/c1/C1-SPEC.md): C1 is the first hermeneutic layer above the
critical translation — "what is this passage saying/doing?" It is passage-local, concise (250-600
words), and reasons primarily through L200's MT/IA/OPEN split (never reverse-engineering those
distinctions from prose). No modern comparison, no essays-as-evidence, no unsupported strengthening.

Consumes committed L2 + L200 (and L0/L1 for terms where needed). The model produces the commentary
prose as a STRUCTURED object per the C1-SPEC default structure (SUMMARY / FUNCTION / KEY TERMS /
EXPLANATION / BOUNDARY / RELATED PASSAGES). MACHINE_PROPOSED, never self-validated: a deterministic
C1 validator gates the commit (passage-local, no modern-comparison lexicon, no essays-as-evidence,
boundaries explicit, structured fields present).
"""
from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import object_registry as R
from model import chat

# modern-comparison / essay-only lexicon (C1-SPEC §8, §9): presence of these in the C1 core
# signals the model drifted out of the passage-local layer.
_ESSAY_LEXICON = re.compile(
    r"\b(predictive processing|self-model|phenomenolog|active inference|illusionism|contemporary "
    r"idealism|neuroscien|ñāṇavīra|nāgārjuna|advaita|higher-order theor|sophisticated structure|"
    r"our essay|we have argued|we argue|this anticipates|modern theori)\b", re.I)
# the required C1-SPEC §5 structure
C1_SECTIONS = ["summary", "function", "key_terms", "explanation", "boundary", "related_passages"]


def _committed_l2_l200(object_id: str, input_hash: str) -> dict:
    """Resolve committed L2 and L200 objects (the C1 inputs)."""
    l2 = R.current("L2", object_id) or R.current("L1L2", object_id)
    l200 = R.current("L200", object_id)
    return {"l2": l2 if (l2 and l2.get("input_hash") == input_hash) else None,
            "l200": l200 if (l200 and l200.get("input_hash") == input_hash) else None}


def _build_prompt(object_id: str, ctx: dict) -> str:
    l2 = ctx.get("l2") or {}
    l200 = ctx.get("l200") or {}
    l2_payload = l2.get("payload", {})
    l2_text = (l2_payload.get("l2") or {}).get("text") or (l2_payload.get("text") or "")
    l1_text = (l2_payload.get("l1") or {}).get("text") or ""
    l200_payload = l200.get("payload", {}) or {}
    audit = l200_payload.get("l200", {}) or {}
    mt = json.dumps(audit.get("3_material_translation_decisions", []), ensure_ascii=False)[:1500]
    ia = json.dumps(audit.get("4_interpretive_assertions", []), ensure_ascii=False)[:1500]
    opn = json.dumps(audit.get("7_open_items", []), ensure_ascii=False)[:1000]
    return (
        "You are the Pāṭala C1 scholar. Produce a passage-local scholarly commentary (250-600 words) "
        "that explains what this passage is saying and doing. RULES (C1-SPEC):\n"
        "- Stay local to the passage. No modern comparison, no essays-as-evidence, no grand synthesis.\n"
        "- Reason through the L200 audit: use its Material Translation Decisions (MT) and Interpretive "
        "  Assertions (IA) and Open Items rather than reverse-engineering them from prose.\n"
        "- Distinguish what the passage EXPLICITLY says from what is LOCALLY implied from what "
        "  REQUIRES wider synthesis (never present the latter as established locally).\n"
        "- Keep technical terms contextually precise (contextual meanings, not dictionary entries).\n"
        "- Keep genuine uncertainties visible in BOUNDARY/OPEN.\n"
        "Return JSON ONLY with these fields (all strings/arrays):\n"
        "{\"summary\":\"...\",\"function\":\"...\",\"key_terms\":[{\"term\":\"...\",\"meaning\":\"...\"}],"
        "\"explanation\":\"...\",\"boundary\":\"...\",\"related_passages\":[\"...\"],"
        "\"uncertain\":[\"...\"]}\n\n"
        f"# L1 (grounded):\n{l1_text[:1200]}\n\n# L2 (published):\n{l2_text[:1200]}\n\n"
        f"# L200 MT:\n{mt}\n# L200 IA:\n{ia}\n# L200 OPEN:\n{opn}"
    )


def _parse_c1(raw: str) -> dict:
    raw = (raw or "").strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        raw = raw.rsplit("```", 1)[0]
    start, end = raw.find("{"), raw.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("no JSON object in C1 model output")
    return json.loads(raw[start:end + 1])


def c1_generator(layer: str, batch: list[dict]) -> list[dict]:
    proposals = []
    for b in batch:
        ctx = _committed_l2_l200(b["object_id"], b.get("input_hash", ""))
        if not ctx["l200"]:
            # C1 requires L200 committed (dependency) — never fabricate commentary without the audit
            proposals.append({"object_id": b["object_id"], "input_hash": b.get("input_hash", ""),
                              "c1": {}, "c1_status": "DEPENDENCY_BLOCKED"})
            continue
        prompt = _build_prompt(b["object_id"], ctx)
        try:
            raw = chat("You are the Pāṭala C1 scholar (passage commentary).", prompt, timeout=180)
            c1 = _parse_c1(raw)
            # deterministic structural coercion: ensure every C1-SPEC section is present
            body = {k: (c1.get(k) or "") for k in ("summary", "function", "explanation", "boundary")}
            body["key_terms"] = c1.get("key_terms") or []
            body["related_passages"] = c1.get("related_passages") or []
            body["uncertain"] = c1.get("uncertain") or []
            proposals.append({"object_id": b["object_id"], "input_hash": b.get("input_hash", ""),
                              "c1": body, "c1_status": "MACHINE_PROPOSED",
                              "_l200_version": ctx["l200"].get("version", "")})
        except Exception:
            proposals.append({"object_id": b["object_id"], "input_hash": b.get("input_hash", ""),
                              "c1": {}, "c1_status": "GENERATION_FAILED"})
    return proposals


def c1_validator(layer: str, proposal: dict) -> tuple[bool, str]:
    """Deterministic C1 quality gate (C1-SPEC §17). The model never self-validates."""
    if proposal.get("c1_status") != "MACHINE_PROPOSED":
        return False, f"c1_status:{proposal.get('c1_status','MISSING')}"
    c1 = proposal.get("c1", {})
    # 1. all structured sections present + non-empty
    for s in ("summary", "function", "explanation", "boundary"):
        if not (c1.get(s) or "").strip():
            return False, f"missing_c1_section:{s}"
    # 2. explains rather than merely paraphrases (explanation length floor)
    expl = (c1.get("explanation") or "").strip()
    if len(expl) < 40:
        return False, "explanation too short (paraphrase, not commentary)"
    # 3. concise enough to be commentary (ceiling per C1-SPEC: 250-600 words, hard cases to ~900).
    #    ~4500 chars ≈ the upper bound of a faithful passage commentary. The essay-drift guard is the
    #    lexicon check below (modern-comparison / essays-as-evidence), not raw length.
    total = len(" ".join(str(c1.get(k) or "") for k in C1_SECTIONS))
    if total > 4500:
        return False, "c1 too long (escalating toward essay)"
    # 4. no modern-comparison / essays-as-evidence lexicon in the core prose
    core = " ".join(str(c1.get(k) or "") for k in ("summary", "function", "explanation", "boundary"))
    if _ESSAY_LEXICON.search(core):
        return False, "essay/modern-comparison lexicon present (out of C1 scope)"
    return True, ""


def make_c1_handlers() -> dict:
    return {"generator": c1_generator, "validator": c1_validator}
