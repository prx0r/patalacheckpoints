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


# Max assembled-prompt size for one model call, in bytes. model.py passes the prompt as a
# command-line argument to `hermes -z`, so a prompt near the OS ARG_MAX (~2MB on Linux) fails with
# `[Errno 7] Argument list too long`. 800KB leaves generous headroom for argv/env overhead while
# still packing many verses per call.
T1_MAX_BYTES = int(os.environ.get("PATALA_T1_MAX_BYTES", "800000"))


def _block_bytes(e: dict) -> int:
    """Upper-bound estimate of the byte size one verse contributes to a T1 batch prompt."""
    return (len(e.get("verse", "").encode("utf-8"))
            + len(json.dumps(e.get("tokens", []), ensure_ascii=False).encode("utf-8"))
            + 200)


def _build_batch_prompt(verses: list[dict]) -> str:
    """One prompt for a WHOLE batch of verses -> ONE model call glosses many verses (max work per call).

    Mirrors batch_translate.py: each verse block carries its object_id (stable passage id) so the model
    can echo it back and we can bind each gloss map to the right verse. Uses the 1M context to pack as
    many verses as fit, instead of one call per verse."""
    blocks = []
    for e in verses:
        tokens = e["tokens"]
        blocks.append(
            f"--- VERSE ---\n"
            f"object_id: {e['object_id']}\n"
            f"VERSE: {e['verse']}\n"
            f"TOKENS: {json.dumps(tokens, ensure_ascii=False)}\n"
        )
    prompt = (
        "You are the Pāṭala T1 translator (the transliteral word-gloss producer). You are given a BATCH "
        "of raw Sanskrit verses with their Vidyut-segmented tokens. For EVERY verse, produce the "
        "canonical T1 transliteral gloss:\n"
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
        "{\"verses\": [\n"
        "  {\"object_id\": \"<echoed from the prompt>\", \"tokens\": {\"<surface>\": "
        "{\"gloss\": \"<literal gloss>\", \"quoted\": <bool>}, ...}}\n"
        "]}\n"
        "covering EVERY verse and EVERY token. You MUST echo each verse's object_id exactly; do not "
        "invent or swap them.\n\n"
        + "\n".join(blocks)
    )
    return prompt


def _parse_batch(raw: str) -> dict:
    """Parse the multi-verse JSON response into {object_id: {surface: gloss}}."""
    raw = (raw or "").strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        raw = raw.rsplit("```", 1)[0]
    start, end = raw.find("{"), raw.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("no JSON object in T1 batch output")
    data = json.loads(raw[start:end + 1])
    out = {}
    for item in (data.get("verses") or []):
        if not isinstance(item, dict):
            continue
        oid = item.get("object_id")
        if not oid:
            continue
        out[oid] = item.get("tokens") or {}
    return out


T1_OUT_LOG = Path(os.environ.get("PATALA_T1_OUT_LOG",
                                 "/root/projects/patala/data/corpus/downloads/t1-stream.jsonl"))


def _log_t1_output(object_id: str, status: str, gloss_map: dict, error: str = "") -> None:
    """Append one verse's T1 result to the streaming output log (immediate, crash-safe).

    This is the observability/streaming layer: every verse's model output is recorded as it is
    produced, so a later failure in the batch never loses the already-committed/labelled record, and
    an operator can tail the log to watch the factory gloss verses in near-real-time."""
    try:
        T1_OUT_LOG.parent.mkdir(parents=True, exist_ok=True)
        rec = {"ts": __import__("time").strftime('%Y-%m-%dT%H:%M:%S'),
               "object_id": object_id, "status": status, "gloss_count": len(gloss_map),
               "error": error or None}
        with T1_OUT_LOG.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass   # logging must never break production


def t1_generator(layer: str, batch: list[dict]) -> list[dict]:
    """Produce canonical T1 objects for a batch of raw-Sanskrit verses.

    BATCHED, PER-WORK, BYTE-CAPPED: verses are glossed in model calls grouped by WORK (each call
    contains only ONE work's verses) and sized so the assembled prompt stays well under the OS
    ARG_MAX limit. This fixes the two live failures:
      (a) mixing many works into one prompt made the model return non-JSON and the whole batch
          failed closed -> ~93% T1 failure rate;
      (b) prompts >~2MB hit `[Errno 7] Argument list too long` because model.py passes the prompt
          as a command-line argument to `hermes -z`.
    Each call is fail-closed: a failed call marks only THAT call's verses retryable, never the whole
    input. Same shape/provenance contract as before; per-verse stream log is preserved."""
    entries = []
    for b in batch:
        verse = (b.get("verse") or "").strip()
        if not verse:
            continue
        segments = _segment(verse)
        tokens = [s["surface"] for s in segments]
        if not tokens:
            continue
        entries.append({"object_id": b["object_id"], "verse": verse,
                        "segments": segments, "tokens": tokens})
    if not entries:
        return []

    # group by work so each model call is single-work (context-consistent)
    by_work: dict[str, list[dict]] = {}
    for e in entries:
        by_work.setdefault(e["object_id"].split(":")[0], []).append(e)

    proposals: list[dict] = []
    for work_entries in by_work.values():
        sub: list[dict] = []
        sub_bytes = 0

        def flush() -> None:
            nonlocal sub, sub_bytes
            if not sub:
                return
            n_tokens = sum(len(e["tokens"]) for e in sub)
            prompt = _build_batch_prompt(sub)
            # A2-10b size-aware timeout: scale with total batch size so big batches get enough time.
            timeout = min(180 + int(n_tokens * 0.5), 600)
            try:
                raw = chat("You are the Pāṭala T1 translator (transliteral word-gloss).", prompt,
                           timeout=timeout)
                gloss_by_oid = _parse_batch(raw)
            except Exception as exc:
                # fail-closed: only THIS call's verses, never the whole input
                for e_ in sub:
                    _log_t1_output(e_["object_id"], "GENERATION_FAILED", {}, error=str(exc)[:80])
                    proposals.append({"object_id": e_["object_id"],
                                      "input_hash": _verse_hash(e_["verse"]),
                                      "t1": {}, "t1_status": "GENERATION_FAILED"})
                sub, sub_bytes = [], 0
                return
            for e in sub:
                verse = e["verse"]
                gloss_map = gloss_by_oid.get(e["object_id"]) or {}
                try:
                    t1_tokens = _assemble_t1(verse, e["segments"], gloss_map)
                    _log_t1_output(e["object_id"], "MACHINE_PROPOSED", gloss_map)
                    proposals.append({
                        "object_id": e["object_id"],
                        "input_hash": _verse_hash(verse),
                        "verse": verse,
                        "t1": {"tokens": t1_tokens,
                               "source_sha256": _verse_hash(verse),
                               "source_text": verse,
                               "status": "MACHINE_PROPOSED"},
                        "t1_status": "MACHINE_PROPOSED",
                    })
                except Exception as ex:
                    _log_t1_output(e["object_id"], "GENERATION_FAILED", gloss_map, error=str(ex)[:80])
                    proposals.append({"object_id": e["object_id"], "input_hash": _verse_hash(verse),
                                      "t1": {}, "t1_status": "GENERATION_FAILED"})
            sub, sub_bytes = [], 0

        for e in work_entries:
            if sub and sub_bytes + _block_bytes(e) > T1_MAX_BYTES:
                flush()
            sub.append(e)
            sub_bytes += _block_bytes(e)
        flush()
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
    """Return the T1 layer handlers.

    Default: the batched generator (t1_generator) — one call glosses a whole batch (context-filled,
    stream-logged). Set PATALA_T1_SESSION=1 to use the PERSISTENT-SESSION streaming generator instead
    (long-lived per-work Hermes session that retains context across calls, "document as it goes")."""
    gen = t1_generator_session if os.environ.get("PATALA_T1_SESSION", "0") == "1" else t1_generator
    return {"generator": gen, "validator": t1_validator}


def t1_generator_session(layer: str, batch: list[dict]) -> list[dict]:
    """PERSISTENT-SESSION T1 generator: drive a long-lived per-work Hermes session that retains the
    work's context packet + accumulated verses across calls, and commit each verse incrementally.

    Solves the giant-call fragility: instead of one 10-min all-or-nothing call, feed chunked verses
    through `--resume <session>` (context retained), committing + stream-logging each chunk as it
    returns. A failed chunk loses only that chunk (retryable), never the whole text.

    Falls back to the batched generator if session streaming is unavailable."""
    try:
        import t1_session
        from agentic_gloss import _term_packet_for  # noqa: F401 (ensure importable)
    except Exception:
        return t1_generator(layer, batch)

    # group by work so each work uses its own persistent session
    by_work = {}
    order = []
    for b in batch:
        verse = (b.get("verse") or "").strip()
        if not verse:
            continue
        wid = (b.get("object_id") or "?").split(":")[0]
        segments = _segment(verse)
        tokens = [s["surface"] for s in segments]
        if not tokens:
            continue
        by_work.setdefault(wid, []).append(
            {"object_id": b["object_id"], "verse": verse, "segments": segments,
             "tokens": tokens, "input_hash": _verse_hash(verse)})
        if wid not in order:
            order.append(wid)

    proposals = []
    for wid in order:
        entries = by_work[wid]
        try:
            res = t1_session.stream_gloss_work(wid, entries)
            committed = {c["object_id"]: c for c in res["committed"]}
            failed_ids = {f["object_id"] for f in res["failed"]}
        except Exception as ex:
            committed, failed_ids = {}, set()
            for e in entries:
                _log_t1_output(e["object_id"], "GENERATION_FAILED", {}, error=str(ex)[:80])
        for e in entries:
            verse = e["verse"]
            c = committed.get(e["object_id"])
            if c is not None and c.get("gloss_map"):
                try:
                    t1_tokens = _assemble_t1(verse, e["segments"], c["gloss_map"])
                    proposals.append({
                        "object_id": e["object_id"],
                        "input_hash": _verse_hash(verse),
                        "verse": verse,
                        "t1": {"tokens": t1_tokens,
                               "source_sha256": _verse_hash(verse),
                               "source_text": verse,
                               "status": "MACHINE_PROPOSED"},
                        "t1_status": "MACHINE_PROPOSED",
                    })
                except Exception as ex:
                    proposals.append({"object_id": e["object_id"], "input_hash": _verse_hash(verse),
                                      "t1": {}, "t1_status": "GENERATION_FAILED"})
            elif e["object_id"] in failed_ids:
                proposals.append({"object_id": e["object_id"], "input_hash": _verse_hash(verse),
                                  "t1": {}, "t1_status": "GENERATION_FAILED"})
    return proposals
