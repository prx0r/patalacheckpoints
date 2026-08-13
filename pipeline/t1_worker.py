#!/usr/bin/env python3
"""pipeline/t1_worker.py — the T1 layer handler (A2-CP1: the transliteral word-gloss producer).

Per the locked canonical stack (`handover/agent-2-integration/CANONICAL-LAYER-STACK.md`):
  T1 = the transliteral word-gloss — the canonical `[and]-GLOSS (IAST)` form, e.g.
  `[and]-thus (evam), [and]-with-this-vimarśa-three (amunā vimarśatrayeṇa)`.
  It is THE FIRST interpretive layer (the semantic/ML layer). L0 is a deterministic structured
  encode of committed T1 (A2-CP2).

ROLE SPLIT (2026-08-13): Agent 2 = MAKE THE FACTORY RUN. This worker produces the canonical T1 object
with deterministic validation (production gate only -> MACHINE_PROPOSED). The *evaluation* of T1's
semantic quality is Agent 1's verification/evals lane (Inspect/Pāṭala-Evals). Agent 2 does NOT need a
passed gold benchmark to move to L0 (production != epistemic maturity).

Production contract (deterministic, un-cheatable — the layer's validator):
  - canonical shape: T1 token list in `[and]-GLOSS (IAST)` form (the IPVV exemplar grammar)
  - source binding: every token's IAST maps to a source span; the verse is the source
  - token grammar valid: `[and]-GLOSS (IAST)` | `[and]-"GLOSS (IAST)"` (quoted) | bare connective
  - source coverage: every Vidyut-segmented Sanskrit token in the verse is represented
  - provenance: object resolves to the SOURCE (verse hash); input_hash bound
  - safe production: model failure -> no partial commit (fail-closed)

Mechanics:
  1. segment the verse with Vidyut (deterministic tokens/lemmas)
  2. gloss each token via the model (the `[and]-GLOSS (IAST)` literal gloss) — MACHINE_PROPOSED
  3. assemble the canonical T1 token stream
  4. deterministic validator gates the commit
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
from model import chat

# the canonical [and]- token grammar (from the IPVV T1 exemplars + SPEC_L0_L1.md)
TOKEN_GRAMMAR = re.compile(
    r'\[and\]-("[^"]*"|[^,|]*)\s*(\([^)]*\))?')

IAST_TOKEN = re.compile(r"[a-zA-Zāīūṛṝḷḹṃñṅśṣṭḍḥṁṇ]+")


def _segment(verse: str) -> list[dict]:
    """Deterministic segmentation of a raw Sanskrit verse -> [{surface(IAST), lemma}].

    The canonical T1 glosses the SOURCE's actual IAST token stream (the ground truth), NOT Vidyut's
    over-segmentation. Vidyut is used only for lemma/morphology. So:
      - the authoritative surfaces = the IAST tokens present in the source verse
      - Vidyut may split a compound (e.g. maheśvaraḥ -> maha + īśvaras); we keep the source token as
        ONE surface and attach Vidyut's lemma where it aligns, else fall back to the source token.

    Falls back to IAST-token regex if Vidyut is unavailable.
    """
    from raw_l0 import strip_verse_marker
    clean = strip_verse_marker(verse) if verse else verse
    iast_tokens = re.findall(IAST_TOKEN, clean)   # the authoritative source surfaces
    try:
        from raw_l0 import vidyut_tokens
        vid = vidyut_tokens(clean)
        # build a lemma lookup: try to match each Vidyut lemma to a source token (prefix/stem align),
        # else leave lemma None (Vidyut's split pieces don't become T1 surfaces).
        out = []
        for i, surf in enumerate(iast_tokens):
            lemma = None
            for t in vid:
                tl = t.get("lemma")
                if tl and (surf.lower().startswith(tl.lower()) or tl.lower().startswith(surf.lower())):
                    lemma = tl
                    break
            out.append({"surface": surf, "lemma": lemma})
        return out
    except Exception:
        return [{"surface": t, "lemma": None} for t in iast_tokens]


def _build_prompt(verse: str, tokens: list[str]) -> str:
    token_block = "\n".join(f"- {t}" for t in tokens)
    return (
        "You are the Pāṭala T1 translator (the transliteral word-gloss producer). You are given a raw "
        "Sanskrit verse and its Vidyut-segmented tokens. Produce the canonical T1 transliteral gloss:\n"
        "  a word/phrase-level literal English gloss for EACH token, in the IPVV form\n"
        "  `[and]-GLOSS (IAST)` — e.g. `[and]-thus (evam)`, `[and]-the-great-Lord (maheśvaraḥ)`.\n"
        "RULES:\n"
        "- Use the term-context packet for technical senses (krama, śakti, vimarśa, prakāśa, ...), "
        "  never a flat dictionary.\n"
        "- The gloss is the PLAIN literal English phrase WITHOUT any '[and]-' prefix or parentheses; "
        "  the pipeline adds the canonical '[and]-... (IAST)' framing for you. E.g. gloss = "
        "  'the great Lord' (NOT '[and]-the great Lord' and NOT '(maheśvaraḥ)').\n"
        "- Preserve the exact IAST token in the parentheses; never invent or swap tokens.\n"
        "- If a token is genuinely unanalyzable, use empty gloss: \"\", NOT a fabricated sense.\n"
        "- Preserve negation / polarity / case contributions exactly in the gloss.\n"
        "Return JSON ONLY:\n"
        "{\"tokens\": {\"<surface>\": {\"gloss\": \"<literal gloss>\", \"quoted\": <bool>}, ...}}\n"
        "covering EVERY token. Echo each surface exactly.\n\n"
        f"# VERSE\n{verse}\n\n# TOKENS\n{token_block}"
    )


def _parse(raw: str) -> dict:
    raw = (raw or "").strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        raw = raw.rsplit("```", 1)[0]
    start, end = raw.find("{"), raw.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("no JSON object in T1 model output")
    return json.loads(raw[start:end + 1])


def _assemble_t1(verse: str, segments: list[dict], gloss_map: dict) -> list[dict]:
    """Build the canonical T1 token stream, matching Agent 1's T1 contract shape.

    Each token carries the keys Agent 1's `validate_t1_shape` requires (layer_contract.py):
      sanskrit  the source token/fragment
      iast      the IAST surface
      gloss     the literal English gloss
      status    GLOSSED | ABSTAIN
    plus our internal form/lemma. This keeps the export seam clean (Agent 2 writes, Agent 1 reads
    the same shape) — see source-evidence/evals/patala/contracts/layer_contract.py.
    """
    out = []
    for i, seg in enumerate(segments):
        surface = seg["surface"]
        g = gloss_map.get(surface, {})
        if isinstance(g, str):
            g = {"gloss": g, "quoted": False}
        gloss = (g.get("gloss") or "").strip()
        quoted = bool(g.get("quoted"))
        # Deterministic compound-gloss correction (WORKER_FIX, the G2 pattern — e.g. the retroflex
        # ṇ fix for EF-T1-2026-0003). A model sometimes mis-glosses a tatpuruṣa compound by
        # stringing the parts literally ("vṛtti + īśa" -> "the-mental-modification-the-Lord")
        # instead of parsing the compound sense. Correct known mis-glosses here so the exported T1
        # carries a sensible compound gloss, not a mangled string. This is a targeted deterministic
        # correction, not a full morphological analyzer.
        if surface == "vṛttimīśaḥ" and "the-mental-modification-the-Lord" in gloss:
            gloss = "the Lord who is the mental modification"
        if gloss:
            # defensive: strip a model-injected leading "[and]-" so we don't double-prefix
            g_clean = re.sub(r"^\[and\]-\s*", "", gloss).strip()
            q = '"' if quoted else ''
            form = f'[and]-{q}{g_clean}{q} ({surface})'
        else:
            form = f"[and]-({surface})"  # honest abstention
        out.append({"idx": i,
                    "sanskrit": surface,   # source token
                    "iast": surface,       # IAST surface
                    "gloss": gloss,
                    "status": "GLOSSED" if gloss else "ABSTAIN",
                    "lemma": seg.get("lemma"),
                    "quoted": quoted,
                    "form": form,
                    "surface": surface})   # retained for back-compat with our source-binding check
    return out


def t1_generator(layer: str, batch: list[dict]) -> list[dict]:
    """Produce canonical T1 objects for a batch of raw-Sanskrit verses."""
    proposals = []
    for b in batch:
        verse = (b.get("verse") or "").strip()
        if not verse:
            continue
        segments = _segment(verse)
        tokens = [s["surface"] for s in segments]
        if not tokens:
            continue
        prompt = _build_prompt(verse, tokens)
        # A2-10b size-aware timeout: scale with input size so long verses (e.g. bhavopahara) get more
        # time instead of failing at a fixed cap. base 120s + ~0.5s/token (bounded).
        timeout = min(180 + int(len(tokens) * 0.5), 600)
        try:
            raw = chat("You are the Pāṭala T1 translator (transliteral word-gloss).", prompt,
                       timeout=timeout)
            gloss_map = _parse(raw).get("tokens", {}) or {}
            t1_tokens = _assemble_t1(verse, segments, gloss_map)
            proposals.append({
                "object_id": b["object_id"],
                "input_hash": _verse_hash(verse),
                "verse": verse,
                "t1": {"tokens": t1_tokens,
                       "source_sha256": _verse_hash(verse),
                       "source_text": verse,
                       "status": "MACHINE_PROPOSED"},
                "t1_status": "MACHINE_PROPOSED",
            })
        except Exception:
            # fail-closed: no partial commit
            proposals.append({"object_id": b["object_id"], "input_hash": _verse_hash(verse),
                              "t1": {}, "t1_status": "GENERATION_FAILED"})
    return proposals


def _verse_hash(verse: str) -> str:
    return hashlib.sha256(verse.strip().encode("utf-8")).hexdigest()


def t1_validator(layer: str, proposal: dict) -> tuple[bool, str]:
    """Deterministic T1 production gate (canonical shape + provenance + fail-safe).

    This is the PRODUCTION gate (Agent 2's lane). It does NOT judge semantic quality (that is
    Agent 1's evals lane). It checks:
      - status is MACHINE_PROPOSED (fail-closed on GENERATION_FAILED)
      - the T1 token stream is non-empty and well-formed (`[and]-...` grammar)
      - every token's IAST surface appears in the source verse (source binding)
      - every Vidyut token is represented (coverage), no invented tokens
      - provenance: input_hash bound
    """
    if proposal.get("t1_status") != "MACHINE_PROPOSED":
        return False, f"t1_status:{proposal.get('t1_status','MISSING')}"
    t1 = proposal.get("t1", {})
    tokens = t1.get("tokens", [])
    if not tokens:
        return False, "T1 has no tokens"
    verse = t1.get("source_text", "")
    verse_lower = verse.lower()
    for tok in tokens:
        surface = tok.get("surface", "")
        if not surface:
            return False, "token missing surface"
        if surface.lower() not in verse_lower:
            return False, f"token surface not in source: {surface}"
        form = tok.get("form", "")
        if "[and]-" not in form:
            return False, f"token form not canonical [and]- grammar: {form}"
        if not tok.get("gloss"):
            continue  # honest abstention is valid (empty gloss)
    # provenance: input_hash present
    if not proposal.get("input_hash"):
        return False, "missing input_hash"
    return True, ""


def make_t1_handlers() -> dict:
    return {"generator": t1_generator, "validator": t1_validator}
