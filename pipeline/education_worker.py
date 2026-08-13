#!/usr/bin/env python3
"""pipeline/education_worker.py — the EDUCATION layer handler (teach the essay clearly).

Per SPEC_EDUCATION.md + the patala-education skill:
  - EDUCATION is downstream of ESSAYS: it teaches what the essays argue, in clearer terms.
  - authority(EDUCATION(x)) ≤ authority(x). It distills; it never contradicts or overreaches the
    essay/theme evidence chain.
  - Reading level: a normal reader understands it without prior specialization.

Consumes the committed ESSAY object; the model distills it into a 3-minute explainer / concept
primer; a deterministic EDUCATION validator gates the commit (derived-from-essay, concise, no new
philosophy beyond the source, links up to the essay and down to the passage).
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
from model import chat

# education overreach lexicon: words that assert beyond the essay's license
_OVERREACH = ["proves", "certainly", "definitively", "undeniably", "always", "the one Self is",
              "it is certain", "scientifically proven"]


def _resolved_essays(object_ids: list[str]) -> list[dict]:
    return [R.current("ESSAY", o) for o in object_ids if R.current("ESSAY", o)]


def _essay_summary(essay: dict) -> str:
    e = essay.get("payload", {}).get("essay", {}) or {}
    title = e.get("title", "")
    sents = [s.get("text", "") for s in e.get("sentences", [])]
    claims = [c.get("text", "") for c in e.get("claims", [])]
    return f"{title}\n\n" + "\n".join(sents) + "\n\nCLAIMS:\n" + "\n".join(claims)


def _build_prompt(essay_summary: str, essay_id: str) -> str:
    return (
        "You are the Pāṭala EDUCATION writer. Distill the essay below into a clear, short "
        "3-minute explainer / concept primer. RULES (SPEC_EDUCATION):\n"
        "- Teach ONE thing clearly, in plain language a non-specialist understands.\n"
        "- DISTILL the essay; do NOT add new philosophy, comparison, or argument beyond it.\n"
        "- Do NOT overreach the evidence (no 'proves'/'the one Self is' if the essay is cautious).\n"
        "- Link upward to the essay and downward to the passage/C1 it teaches.\n"
        "Return JSON ONLY:\n"
        "{\"title\":\"...\",\"summary\":\"...\",\"key_points\":[\"...\"],"
        "\"essay_id\":\"<echo the essay_id>\",\"status\":\"MACHINE_PROPOSED\"}\n\n"
        f"# ESSAY (source)\n{essay_summary[:3000]}"
    )


def _parse_edu(raw: str) -> dict:
    raw = (raw or "").strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        raw = raw.rsplit("```", 1)[0]
    start, end = raw.find("{"), raw.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("no JSON object in EDUCATION model output")
    return json.loads(raw[start:end + 1])


def education_generator(layer: str, batch: list[dict]) -> list[dict]:
    essays = _resolved_essays([b["object_id"] for b in batch])
    if not essays:
        return []  # no essay -> dependency (never teach from nothing)
    # one EDU object per essay
    props = []
    for e in essays:
        essay_id = e.get("object_id", "")
        summary = _essay_summary(e)
        try:
            raw = chat("You are the Pāṭala EDUCATION writer (distill the essay).",
                       _build_prompt(summary, essay_id), timeout=180)
            edu = _parse_edu(raw)
            body = {"title": edu.get("title", ""), "summary": edu.get("summary", ""),
                    "key_points": edu.get("key_points") or [],
                    "essay_id": edu.get("essay_id") or essay_id,
                    "status": "MACHINE_PROPOSED"}
            props.append({"object_id": f"edu__{essay_id}", "input_hash": essay_id,
                          "education": body, "education_status": "MACHINE_PROPOSED",
                          "_source_essay": essay_id})
        except Exception:
            continue
    return props


def education_validator(layer: str, proposal: dict) -> tuple[bool, str]:
    """Deterministic EDUCATION gate (SPEC_EDUCATION §6 / the skill).

    - derived from a committed essay (source resolves)
    - teaches one thing concisely (not an essay-length re-run)
    - no overreach lexicon that asserts beyond the essay's license
    - links upward to the essay
    """
    if proposal.get("education_status") != "MACHINE_PROPOSED":
        return False, f"education_status:{proposal.get('education_status','MISSING')}"
    edu = proposal.get("education", {})
    src = proposal.get("_source_essay", "")
    if not R.current("ESSAY", src):
        return False, "education not derived from a committed essay"
    if not (edu.get("summary") or "").strip():
        return False, "education missing summary"
    # concise: the explainer must be materially shorter than an essay (distill, not re-run)
    total = len(str(edu.get("summary", ""))) + sum(len(str(k)) for k in edu.get("key_points", []))
    if total > 1500:
        return False, "education too long (re-running the essay, not distilling)"
    # no overreach
    text = (str(edu.get("summary", "")) + " " + " ".join(str(k) for k in edu.get("key_points", []))).lower()
    over = [w for w in _OVERREACH if w in text]
    if over:
        return False, f"education overreach beyond essay: {over}"
    return True, ""


def make_education_handlers() -> dict:
    return {"generator": education_generator, "validator": education_validator}
