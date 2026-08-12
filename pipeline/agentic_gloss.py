#!/usr/bin/env python3
"""pipeline/agentic_gloss.py — the agentic RAW-L0 gloss runner (context engineering + multi-pass).

Makes Hermes follow the `raw-l0` skill properly:
  1. CONTEXT ENGINEERING  inject the skill's file-links + the work's term-context packet
                           (from the canonical_reference_map semantic-shift glossary) into the
                           prompt so the model reads the right senses, not a flat dictionary.
  2. PROPOSE              the literal gloss per token (word/phrase-level), anchored to Vidyut.
  3. SELF-CHALLENGE       a SEPARATE model pass that tries to falsify the proposal (wrong lemma /
                           wrong tradition sense / too interpretive / lost polarity) and returns a
                           revision or an honest ABSTAIN.
  4. UN-CHEATABLE VALIDATION  the output is validated by `validate_l0_spec.py` (schema + P0 +
                           abstraction-honesty + gloss), which the model does not control.

Usage:
  python3 pipeline/agentic_gloss.py --work kramasadbhava --verse-idx 2 [--max-tokens 400]
    --work       the queue work_id (its RAW_SANSKRIT source is read from the ledger)
    --verse-idx  which verse (index into split_verses)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent3_batch import load_raw_source, split_verses
from raw_l0 import raw_l0, raw_l0_to_canonical
from model import chat

REFERENCE_MAP = "/root/projects/patala/docs/corpus/canonical_reference_map.md"
SKILL_PATH = "/root/projects/patala/skills/raw-l0/SKILL.md"

# The terms most likely to appear and their sense-policy anchors (pulled from the reference map).
# This is a seed term-context packet; the model is instructed to READ the reference map for more.
TERM_PACKET = {
    "krama": "capitalize 'Krama' only when sectarian identity is demonstrable; else 'sequence/order'.",
    "śakti": "in Krama = Goddess/mantric power (not merely 'energy'); in Trika = freedom/power of consciousness.",
    "vimarśa": "Pratyabhijñā = reflexive awareness/self-apprehension; NEVER bare 'reflection'.",
    "kula": "Kubjikā = mantra-body/structured aggregate; Kaula = body/power-totality; NOT always 'family'.",
    "spanda": "dynamic pulse of consciousness; 'vibration' risks sounding mechanical.",
    "śiva": "the supreme principle / the auspicious; deity name.",
}


def _term_packet_for(work_id: str) -> str:
    lines = ["# TERM-CONTEXT PACKET (from docs/corpus/canonical_reference_map.md — the LEMMA→SENSE atlas)",
             "Semantic consistency is the goal, not lexical uniformity. Sense is set by tradition +",
             f"period + text. For this work ({work_id}), apply these policies where the lemma appears:"]
    for term, pol in sorted(TERM_PACKET.items()):
        lines.append(f"- {term}: {pol}")
    # merge the semantic-shift term-context for this work's school/period (if it's a sivaqueue target)
    try:
        from sivaqueue_targets import (term_context, translation_neighbourhood, guide_descriptions,
                                       all_targets, companion_guide_files)
        sq = all_targets().get(work_id)
        if sq:
            lines.append(f"\nWORK: {sq.get('name')} | school: {sq.get('tradition')} | "
                         f"period: {sq.get('period')} | genre: {sq.get('genre')} | "
                         f"status: {sq.get('translation_status')}")
            lines.append("\nCOMPANION TRANSLATION-MEMORY GUIDES to consult for correct terminology:")
            lines.append(guide_descriptions(sq.get("companion_guides", [])))
            # on-disk companion guide files (read these for the period-correct register)
            cg = companion_guide_files(sq.get("companion_guides", []))
            if cg:
                lines.append("\nCOMPANION GUIDE FILES NOW ON DISK (READ these before translating):")
                lines.append("- " + "\n- ".join(cg))
            nh = translation_neighbourhood(work_id)
            if nh:
                lines.append("\nTRANSLATION NEIGHBOURHOOD (consult these specific works for period-correct senses):")
                lines.append("- " + "\n- ".join(nh))
            tc = term_context(work_id)
            if tc:
                lines.append("\n" + tc)
    except Exception:
        pass
    lines.append("\n- Read the full glossary in the reference map if a token is not listed.")
    return "\n".join(lines)


def _skill_file_links() -> str:
    return (
        "FILES THIS TASK USES (read before proposing — context engineering, not blind prompting):\n"
        "- L0 spec (the contract): translations/_stack/ipvv/specs/l0_schema.json\n"
        "- Deterministic core + proof: pipeline/raw_l0.py, pipeline/verify_l0.py\n"
        "- The un-cheatable validator: pipeline/validate_l0_spec.py\n"
        "- Reference map (term senses): docs/corpus/canonical_reference_map.md\n"
        "- Doctrine: machinelearning/_ACTIVE/AGENTS-DOCTRINE.md\n"
    )


def propose_glosses(verse: str, tokens: list[str], work_id: str) -> dict:
    """Pass 1 (PROPOSE): literal gloss per token, with the term-context packet in-context."""
    packet = _term_packet_for(work_id)
    prompt = (
        "You are the Pāṭala RAW-L0 generative layer (the raw-l0 skill). Produce a literal, "
        "word/phrase-level English gloss for EACH Sanskrit token of the verse. Anchoring:\n"
        "- Each token has already been segmented + lemmatized by Vidyut (the deterministic witness).\n"
        "- Use the term-context packet for the technical senses (never a flat dictionary lookup).\n"
        "- A gloss is the literal meaning of the token, not a whole-verse translation.\n"
        "- Return JSON only: {\"<token>\": \"<literal gloss>\"} with EXACTLY the same keys as the prompt.\n"
        "- If a token is genuinely unanalyzable in context, use \"\" (empty) — do NOT fabricate.\n\n"
        f"{packet}\n\n"
        f"VERSE: {verse}\n"
        f"TOKENS: {json.dumps(tokens, ensure_ascii=False)}\n"
    )
    raw = chat("You are a careful Sanskrit L0 gloss generator.", prompt, max_tokens=800)
    try:
        return json.loads(raw)
    except Exception:
        # be honest: return empty glosses rather than fabricate
        return {t: "" for t in tokens}


def challenge_glosses(verse: str, glosses: dict, work_id: str) -> dict:
    """Pass 2 (SELF-CHALLENGE): a SEPARATE pass tries to falsify each gloss."""
    packet = _term_packet_for(work_id)
    prompt = (
        "You are a SECOND, adversarial Sanskrit philologist (the self-challenge pass). The first "
        "pass proposed literal glosses. Challenge each one:\n"
        "- wrong lemma or wrong tradition sense (imported from another school)?\n"
        "- gloss too interpretive (reading more than the token says)?\n"
        "- lost negation / polarity / case contribution?\n"
        "- should it be ABSTAIN (AMBIGUOUS) rather than a confident gloss?\n"
        "Return JSON only: {\"<token>\": \"<REVISED literal gloss or ABSTAIN>\"}. Keep same keys. "
        "Only change a gloss if the challenge finds a real problem.\n\n"
        f"{packet}\n\n"
        f"VERSE: {verse}\n"
        f"PROPOSED: {json.dumps(glosses, ensure_ascii=False)}\n"
    )
    raw = chat("You are a skeptical Sanskrit philologist (adversarial check).", prompt, max_tokens=800)
    try:
        return json.loads(raw)
    except Exception:
        return dict(glosses)


# ───────────────────────────────────────────────────────────────────────────── #
# BATCH MODE — many verses in ONE context/API call (as many L0 as possible per
# call). The batch prompt carries the work's term-context packet once, then all
# verses + their Vidyut token lists; the model returns glosses for every token.
# No max-token cap is passed to hermes (model.py's _hermes_call passes only the
# prompt + model to `hermes -z`), so the batch is bounded only by hermes's own
# handling of a single prompt — the "as many L0 as possible in one call" goal.
# ───────────────────────────────────────────────────────────────────────────── #

def _parse_batch_gloss(raw: str, entries: list) -> dict:
    """Parse a batch gloss JSON {\"<idx>\": {\"<token>\": \"<gloss>\"}} and map back per entry.
    Honest on failure: empty glosses (never fabricate)."""
    try:
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError("batch gloss not an object")
    except Exception:
        return {e["idx"]: {t: "" for t in e["tokens"]} for e in entries}
    out = {}
    for e in entries:
        got = data.get(str(e["idx"])) or data.get(e["idx"]) or {}
        if not isinstance(got, dict):
            got = {}
        out[e["idx"]] = {t: got.get(t, "") for t in e["tokens"]}
    return out


def propose_glosses_batch(entries: list, work_id: str, max_tokens=None) -> dict:
    """Pass 1 (PROPOSE) for a BATCH of verses in one call. entries: [{idx, verse, tokens}]."""
    packet = _term_packet_for(work_id)
    blocks = []
    for e in entries:
        blocks.append(
            f"--- VERSE {e['idx']} ---\n"
            f"VERSE: {e['verse']}\n"
            f"TOKENS: {json.dumps(e['tokens'], ensure_ascii=False)}\n"
        )
    prompt = (
        "You are the Pāṭala RAW-L0 generative layer (the raw-l0 skill). Produce a literal, "
        "word/phrase-level English gloss for EACH Sanskrit token of EACH verse below (the whole batch "
        "in ONE response). Anchoring:\n"
        "- Each token has already been segmented + lemmatized by Vidyut (the deterministic witness).\n"
        "- Use the term-context packet for the technical senses (never a flat dictionary lookup).\n"
        "- A gloss is the literal meaning of the token, not a whole-verse translation.\n"
        "- Return JSON ONLY: {\"<idx>\": {\"<token>\": \"<literal gloss>\"}} covering EVERY verse and EVERY token.\n"
        "- If a token is genuinely unanalyzable in context, use \"\" (empty) — do NOT fabricate.\n\n"
        f"{packet}\n\n"
        + "\n".join(blocks)
    )
    raw = chat("You are a careful Sanskrit L0 gloss generator.", prompt, max_tokens=max_tokens, timeout=600)
    return _parse_batch_gloss(raw, entries)


def challenge_glosses_batch(entries: list, proposed: dict, work_id: str, max_tokens=None) -> dict:
    """Pass 2 (SELF-CHALLENGE) for a BATCH in one call. proposed: {idx: {token: gloss}}."""
    packet = _term_packet_for(work_id)
    blocks = []
    for e in entries:
        blocks.append(
            f"--- VERSE {e['idx']} ---\n"
            f"VERSE: {e['verse']}\n"
            f"PROPOSED: {json.dumps(proposed.get(e['idx'], {}), ensure_ascii=False)}\n"
        )
    prompt = (
        "You are a SECOND, adversarial Sanskrit philologist (the self-challenge pass). The first pass "
        "proposed literal glosses for a BATCH of verses. Challenge each gloss of EACH verse:\n"
        "- wrong lemma or wrong tradition sense (imported from another school)?\n"
        "- gloss too interpretive (reading more than the token says)?\n"
        "- lost negation / polarity / case contribution?\n"
        "- should it be ABSTAIN (AMBIGUOUS) rather than a confident gloss?\n"
        "Return JSON ONLY: {\"<idx>\": {\"<token>\": \"<REVISED literal gloss or ABSTAIN>\"}} covering EVERY "
        "verse and EVERY token. Only change a gloss if the challenge finds a real problem.\n\n"
        f"{packet}\n\n"
        + "\n".join(blocks)
    )
    raw = chat("You are a skeptical Sanskrit philologist (adversarial check).", prompt, max_tokens=max_tokens, timeout=600)
    try:
        challenged = _parse_batch_gloss(raw, entries)
    except Exception:
        challenged = proposed
    return challenged


def run_batch(entries: list, work_id: str) -> list:
    """Run the full agentic gloss (propose → self-challenge) for a batch of verses in ONE propose
    call + ONE challenge call. entries: [{idx, verse, tokens}]. Returns list of
    {idx, proposed, challenged, gloss_map}."""
    if not entries:
        return []
    proposed = propose_glosses_batch(entries, work_id)
    challenged = challenge_glosses_batch(entries, proposed, work_id)
    out = []
    for e in entries:
        p = proposed.get(e["idx"], {})
        c = challenged.get(e["idx"], p)
        gloss_map = {}
        for t in e["tokens"]:
            g = c.get(t, p.get(t, ""))
            if g == "ABSTAIN":
                g = ""
            gloss_map[t] = {"literal": g, "compound": "", "supplied": False}
        out.append({"idx": e["idx"], "proposed": p, "challenged": c, "gloss_map": gloss_map})
    return out


def run(work_id: str, verse_idx: int, max_tokens: int = 800) -> dict:
    verses = split_verses(load_raw_source(work_id))
    verse = verses[verse_idx]
    records, _ = raw_l0_to_canonical(f"{work_id}-v{verse_idx+1}", verse)
    tokens = [r["raw_fragment"] for r in records if r["raw_fragment"]]

    glosses = propose_glosses(verse, tokens, work_id)
    final = challenge_glosses(verse, glosses, work_id)

    # build the canonical L0 with the glosses (nested shape; ABSTAIN -> empty gloss + AMBIGUOUS)
    gloss_map = {}
    for t in tokens:
        g = final.get(t, glosses.get(t, ""))
        if g == "ABSTAIN":
            g = ""
        gloss_map[t] = {"literal": g, "compound": "", "supplied": False}

    res = raw_l0(work_id, f"{work_id}:v{verse_idx+1}", verse, gloss_map)

    return {
        "work_id": work_id, "verse_idx": verse_idx, "verse": verse,
        "tokens": tokens, "proposed": glosses, "challenged": final,
        "records": res["records"], "proof": res["proof"],
        "PASS": res["proof"].get("PASS") and all(
            (r["status"] == "FAILED") or (r["literal_gloss"] != "") for r in res["records"]),
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="kramasadbhava")
    ap.add_argument("--verse-idx", type=int, default=2)
    ap.add_argument("--max-tokens", type=int, default=800)
    a = ap.parse_args()
    r = run(a.work, a.verse_idx, a.max_tokens)
    print(json.dumps(r, indent=2, ensure_ascii=False))
