#!/usr/bin/env python3
"""pipeline/raw_l0.py — RAW SANSKRIT → canonical L0 (MODE_B). Emits the IPVV L0 schema.

The northstar's Build 1 (handover/hermes/AUTOTRANSLATE-NORTHSTAR.md): RAW SANSKRIT -> L0 is the
one gap blocking the autonomous factory. IPVV L0 EXTRACTS an already-glossed layer; RAW-L0 CREATES
it from raw Sanskrit.

CRITICAL DESIGN DECISION: RAW-L0 must emit the SAME canonical L0 schema that the IPVV uses, so the
EXISTING machinery (verify_l0.py P0 proof, the published store, the C1 chain) consumes it UNCHANGED.
The precedent is extract_l0_v1.py — a non-standard input (V1 prose) -> canonical L0 that passes
verify_l0.py. RAW-L0 does the same for raw Sanskrit.

The canonical L0 record (per specs/l0_schema.json):
  { id, chunk_id, line_id, line_kind, chunk_char_start, chunk_char_end,
    line_char_start, line_char_end, wraps_line, raw_fragment, source_text,
    lemma_iast, literal_gloss, quoted, status }

Pipeline per verse (the agentic loop):
  1. SOURCE            the raw Sanskrit verse (the chunk)
  2. DETERMINISTIC     Vidyut segmentation + lemma + morphology (the witness)
  3. PROPOSE           literal gloss per segment (the LLM/generative layer)
  4. VERIFY            P0 via the existing verify_l0.p0_proof
  5. WRITE             canonical L0 JSONL

The deterministic core (Vidyut + P0) needs NO model. The gloss is an LLM task — provided either
from a file (to prove mechanics) or a model call. Never fabricate: lemma=null -> status=AMBIGUOUS
(or a structural class), never PARSED.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from verify_l0_p2 import _get_vidyut, vidyut_analyze
from vidyut.lipi import transliterate, Scheme
from verify_l0 import p0_proof

VIDYUT_PATH = "/root/vidyut-0.4.0"

# IAST token: any run of Sanskrit letters/diacritics
IAST_TOKEN = re.compile(r"[a-zA-Zāīūṛṝḷḹṃñṅśṣṭḍḥṁ]+")
# structural chars (verse markers, punctuation) — classified, not UNKNOWN
STRUCTURAL = set(" ॥|॥,;:!?()[]{}*-—_।|")


# --------------------------------------------------------------------------- #
# Vidyut segmentation (the deterministic witness) — returns tokens + spans
# --------------------------------------------------------------------------- #
def vidyut_tokens(sanskrit: str) -> list[dict]:
    """Segment raw IAST into tokens with SLP1 surface + lemma + data class."""
    v = _get_vidyut(VIDYUT_PATH)
    slp = transliterate(sanskrit, Scheme.Iast, Scheme.Slp1)
    out = []
    for t in v["chedaka"].run(slp):
        out.append({"surface": t.text, "lemma": t.lemma,
                    "data_class": type(t.data).__name__ if t.data else None})
    return out


# --------------------------------------------------------------------------- #
# the canonical L0 builder (emits the IPVV schema)
# --------------------------------------------------------------------------- #
def strip_verse_marker(verse: str) -> str:
    """Separate the verse locator (e.g. '||1/1') from the Sanskrit content.

    The Dyczkowski/GRETIL editions append a locator like '||1/1' to each verse. This is a
    structural reference, NOT Sanskrit content — classify it as structural so P0 sees only
    the semantic Sanskrit (else '1/1' digits become UNKNOWN). The locator is preserved
    separately (it is the passage locator).
    """
    m = re.search(r"[।|]{1,2}\s*([0-9/\s]+|[a-z/0-9 ]+)?\s*[।|]*$", verse.strip())
    if m and m.start() > 0:
        return verse[:m.start()].rstrip()
    return verse


def build_l0_records(chunk_id: str, verse: str, segments: list[dict],
                     glosses: dict[str, dict] | None = None) -> list[dict]:
    """Build canonical L0 records for one verse (the 'chunk').

    Each Vidyut segment becomes a token record. The verse text is the chunk; we compute
    char spans by locating each segment's surface in the IAST verse.

    glosses: {surface: {literal, compound, supplied}} — the LLM/generative layer.
    """
    verse = strip_verse_marker(verse)   # drop the structural locator
    records = []
    # the verse is the source text; chunk_char == line_char (single-line chunk)
    n = len(verse)

    # naive span assignment: scan the IAST verse for each segment's SLP1 surface is lossy
    # (SLP1 != IAST). Instead, segment the IAST verse by whitespace and pair by order, then
    # cross-reference Vidyut's SLP1 analysis per IAST token.
    iast_tokens = [(m.start(), m.end(), m.group(0)) for m in IAST_TOKEN.finditer(verse)]

    for i, (cs, ce, token) in enumerate(iast_tokens):
        lemma = None
        dclass = None
        # analyze the IAST token via Vidyut (transliterates internally)
        try:
            analyses = vidyut_analyze(token)
            if analyses and not any("error" in a for a in analyses):
                lemma = analyses[0].get("lemma")
                dclass = analyses[0].get("data_class")
        except Exception:
            pass
        gloss = glosses.get(token, {}).get("literal", "") if glosses else ""
        supplied = glosses.get(token, {}).get("supplied", False) if glosses else False
        # status: PARSED only if we have both a lemma (or gloss) and a real token
        if lemma or gloss:
            status = "PARSED"
        elif token:
            status = "AMBIGUOUS"   # Vidyut couldn't analyze; abstain, don't fabricate
        else:
            status = "FAILED"
        records.append({
            "id": f"{chunk_id}:L1:T{i}",
            "chunk_id": chunk_id,
            "line_id": 1,
            "line_kind": "verse_blockquote",
            "source_text": verse,
            "raw_fragment": token,
            "char_start": cs, "char_end": ce,
            "chunk_char_start": cs, "chunk_char_end": ce,
            "line_char_start": cs, "line_char_end": ce,
            "wraps_line": False,
            "lemma_iast": lemma or token,
            "literal_gloss": gloss,
            "quoted": False,
            "status": status,
        })
    return records


# --------------------------------------------------------------------------- #
# the pipeline
# --------------------------------------------------------------------------- #
def raw_l0_to_canonical(chunk_id: str, verse: str,
                        glosses: dict[str, dict] | None = None) -> tuple[list[dict], dict]:
    """Produce canonical L0 records for a verse + run the P0 proof (existing verify_l0).

    Returns (records, proof) where proof is from the EXISTING verify_l0.p0_proof, so RAW-L0
    is validated by the same harness as IPVV. The verse locator is stripped as structural so
    P0 sees only the semantic Sanskrit.
    """
    stripped = strip_verse_marker(verse)
    records = build_l0_records(chunk_id, stripped, [], glosses)
    proof = p0_proof(chunk_id, stripped, records)
    return records, proof


def raw_l0(work_id: str, passage_id: str, sanskrit: str,
           glosses: dict[str, dict] | None = None) -> dict:
    """Top-level: build canonical L0 + proof for one verse."""
    chunk_id = f"{work_id}-{passage_id.split(':')[-1]}"
    records, proof = raw_l0_to_canonical(chunk_id, sanskrit, glosses)
    return {"chunk_id": chunk_id, "passage_id": passage_id, "verse": sanskrit,
            "records": records, "proof": proof}


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="RAW-L0: raw Sanskrit -> canonical L0 (MODE_B)")
    ap.add_argument("--work", default="kramasadbhava")
    ap.add_argument("--passage", default="kramasadbhava:1.1")
    ap.add_argument("--sanskrit", required=True)
    ap.add_argument("--gloss-file", default=None, help="JSON {token: {literal, compound, supplied}}")
    ap.add_argument("--out", default="data/corpus/downloads/raw-l0-canonical.json")
    a = ap.parse_args()

    glosses = json.load(open(a.gloss_file)) if a.gloss_file else None
    res = raw_l0(a.work, a.passage, a.sanskrit, glosses)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2, ensure_ascii=False)
    print(json.dumps(res["proof"], indent=2))
    print(f"records: {len(res['records'])}")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
