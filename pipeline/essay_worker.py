#!/usr/bin/env python3
"""pipeline/essay_worker.py — the ESSAY layer handler (proof-carrying prose from themes).

Per SPEC_ESSAY.md + the patala-essay skill:
  - An ESSAY is where comparison / original argument / modern application occur, derived from ≥1
    THEME dossier (never forced onto passages).
  - Every essay claim carries a SHOW-EVIDENCE link that resolves (passage → Sanskrit → decision →
    scholarship). authority(ESSAY) ≤ authority(SYNTHESIS/THEME).
  - Essays are INTERNAL_SYNTHESIS, never PRIMARY_EVIDENCE for upstream layers.

This handler REUSES Agent 1's frozen machinery (machinelearning/research/patala_ml/):
  - Essay / EssaySentence object model (essay.py, essaysentence.py) — the canonical auditable object
  - verify_essay (essayverify.py) — the INDEPENDENT SentenceEvidenceAudit gate (never the generator's).

Consumes committed THEME + C1 objects; the model drafts the essay; verify_essay gates the commit.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")
sys.path.insert(0, "/root/projects/patala/machinelearning/research")

import object_registry as R
from model import chat

# Reuse Agent 1's essay object model + independent verifier.
try:
    from patala_ml.essay import Essay, plan_hash
    from patala_ml.essaysentence import EssaySentence
    from patala_ml.essayverify import verify_essay
    _AGENT1 = True
except Exception as _e:  # pragma: no cover
    _AGENT1 = False
    _AGENT1_ERR = str(_e)

MIN_THEMES = 1


def _theme_inputs(object_ids: list[str]) -> tuple[list[dict], list[dict]]:
    """Resolve committed THEME + C1 objects (the essay's evidence spine)."""
    themes, c1s = [], []
    for oid in object_ids:
        t = R.current("THEME", oid)
        if t:
            themes.append(t)
        c = R.current("C1", oid)
        if c:
            c1s.append(c)
    return themes, c1s


def _claims_from_themes(themes: list[dict]) -> list[dict]:
    """Deterministic claims: each theme member_C1 becomes an auditable EssayClaim (id + text + boundary)."""
    claims = []
    for ti, t in enumerate(themes):
        theme = t.get("payload", {}).get("theme", {}) or {}
        for mi, m in enumerate(theme.get("member_claims", []) or []):
            c1_id = m.get("c1_id", "")
            c1 = R.current("C1", c1_id)
            text = (c1.get("payload", {}).get("c1", {}) or {}).get("summary", "") if c1 else ""
            claims.append({
                "id": f"TH-{ti+1}-M{mi+1}",
                "role": m.get("role", "claim"),
                "text": text or f"theme {theme.get('theme_id','')} member {c1_id}",
                "boundary": (theme.get("boundary", {}) or {}).get("not_claiming", ""),
            })
    return claims


def _build_prompt(theme_ids: list[str], claims: list[dict], c1_texts: list[str]) -> str:
    claims_block = "\n".join(
        f"- **{c['id']}** ({c['role']}) — {c['text']}" + (f"  [boundary: {c['boundary']}]" if c['boundary'] else "")
        for c in claims)
    c1_block = "\n".join(f"[{i+1}] {t[:400]}" for i, t in enumerate(c1_texts))
    return (
        "You are the Pāṭala ESSAY writer. Write a short, evidence-carrying essay derived from the "
        "THEME dossier below. RULES (SPEC_ESSAY):\n"
        "- Every substantive sentence must map to ≥1 claim (claim_ids) with a provenance_relation.\n"
        "- Do NOT exceed a claim's boundary (no 'proves consciousness'/universal Self if the claim "
        "  says 'does not by itself'). No certainty inflation (no 'proves'/'always' beyond the claim).\n"
        "- Original argument / comparison / modern application are allowed HERE (not in C1) but must "
        "  be marked as the essay's own, not what the primary text establishes.\n"
        "- Quote our translation by stable passage/C1 id so the reader can jump to the Sanskrit.\n"
        "Return JSON ONLY:\n"
        "{\"title\":\"...\",\"sentences\":[{\"text\":\"...\",\"claim_ids\":[\"TH-x-My\"],"
        "\"provenance_relation\":\"PARAPHRASE|QUOTATION|COMPRESSION|INFERENCE|QUALIFICATION|TRANSITION\"}]}\n\n"
        f"# THEME dossier (claims)\n{claims_block}\n\n# C1 evidence\n{c1_block}"
    )


def _parse_essay(raw: str) -> dict:
    raw = (raw or "").strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        raw = raw.rsplit("```", 1)[0]
    start, end = raw.find("{"), raw.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("no JSON object in ESSAY model output")
    return json.loads(raw[start:end + 1])


def essay_generator(layer: str, batch: list[dict]) -> list[dict]:
    """Draft an Essay from committed THEME+C1; the SentenceEvidenceAudit gates the commit."""
    if not _AGENT1:
        return []
    themes, c1s = _theme_inputs([b["object_id"] for b in batch])
    if not themes:
        return []  # no theme -> DEPENDENCY (never write an essay from nothing)
    claims = _claims_from_themes(themes)
    c1_texts = [(c.get("payload", {}).get("c1", {}) or {}).get("summary", "") for c in c1s]
    theme_ids = [t.get("payload", {}).get("theme", {}).get("theme_id", "") for t in themes]
    prompt = _build_prompt(theme_ids, claims, c1_texts)
    try:
        raw = chat("You are the Pāṭala ESSAY writer (proof-carrying prose).", prompt, timeout=180)
        data = _parse_essay(raw)
        # build the canonical Essay object
        essay_id = f"essay__{_batch_hash(batch)}"
        essay = Essay(essay_id=essay_id, plan_id="themes-plan-1",
                      plan_hash=plan_hash({"themes": theme_ids}), theme_id=theme_ids[0] if theme_ids else "",
                      title=data.get("title", "untitled"), claims=claims)
        for i, s in enumerate((data.get("sentences") or [])[:60]):
            essay.add_sentence(EssaySentence(
                id=f"{essay_id}-s{i+1}", text=(s.get("text") or "").strip(),
                claim_ids=s.get("claim_ids") or [], provenance_relation=s.get("provenance_relation", "PARAPHRASE")))
        verdict = verify_essay(essay)
        return [{"object_id": essay_id, "input_hash": _batch_hash(batch),
                 "essay": essay.to_dict(), "essay_status": "MACHINE_PROPOSED",
                 "_sentence_evidence_audit": verdict["summary"],
                 "_audit_ok": verdict["ok"]}]
    except Exception:
        return []


def essay_validator(layer: str, proposal: dict) -> tuple[bool, str]:
    """Deterministic ESSAY gate (SPEC_ESSAY §7 / the skill's SentenceEvidenceAudit).

    - every sentence's refs resolve; no sentence asserts more than its refs license
    - the SentenceEvidenceAudit must PASS (0 rejected sentences)
    - derived from ≥1 theme (not forced onto passages); status MACHINE_PROPOSED
    """
    if proposal.get("essay_status") != "MACHINE_PROPOSED":
        return False, f"essay_status:{proposal.get('essay_status','MISSING')}"
    essay = proposal.get("essay", {})
    if not essay.get("sentences"):
        return False, "essay has no sentences"
    if not essay.get("claims"):
        return False, "essay has no claims (nothing grounded)"
    # the independent SentenceEvidenceAudit must pass
    audit = proposal.get("_sentence_evidence_audit", {})
    if proposal.get("_audit_ok") is not True:
        return False, f"essay failed SentenceEvidenceAudit: {json.dumps(audit)[:200]}"
    return True, ""


def _batch_hash(batch: list[dict]) -> str:
    import hashlib
    ids = "|".join(sorted(b.get("object_id", "") for b in batch))
    return hashlib.sha256(ids.encode()).hexdigest()[:12]


def make_essay_handlers() -> dict:
    return {"generator": essay_generator, "validator": essay_validator}
