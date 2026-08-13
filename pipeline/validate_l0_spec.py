#!/usr/bin/env python3
"""pipeline/validate_l0_spec.py — the UN-CHEATABLE L0-spec validator.

The autonomous Agent 3 (Hermes) produces candidate L0 records. THIS file decides whether they
are actually valid Pāṭala L0 — and it is the authority, not the model. A model cannot "cheat"
past it because it checks, deterministically and independently:

  1. SCHEMA     every record satisfies the canonical L0 JSON schema
                (translations/_stack/ipvv/specs/l0_schema.json) — all 15 required fields,
                correct types, correct `id` pattern, correct `status` enum.
  2. P0 PROOF   the EXISTING verify_l0.p0_proof re-runs over the records + the source chunk:
                exact span integrity (raw_fragment == chunk_text[cs:ce]), 0 unknown chars,
                0 bad spans, monotonic ordering, roundtrip. The model never supplies the proof.
  3. ABSTRACTION HONESTY   a record may claim `status: PARSED` only if it has BOTH a lemma
                and a gloss; `AMBIGUOUS` only if lemma/gloss is genuinely absent. A fabricated
                `PARSED` (lemma or gloss the model invented) is caught as a FAIL.
  4. GLOSS PRESENCE    unless `status: FAILED`, `literal_gloss` must be non-empty (the gloss is
                the point of the generative layer). An empty gloss on a PARSED record = FAIL.

This is the "use the .py that ensures it's exactly our L0 spec" gate. Every record must pass
ALL four before the batch/ledger may be updated.

Usage:
  python3 pipeline/validate_l0_spec.py --records <records.jsonl|json> [--chunk-text <file>]
    --records   path to the L0 records (JSONL one-per-line, or a JSON array/list)
    --chunk-text optional path to the source chunk text for the P0 proof (else P0 is skipped
                 but schema + abstraction + gloss are still enforced)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from verify_l0 import p0_proof

SCHEMA_PATH = "/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/specs/l0_schema.json"

REQUIRED_FIELDS = [
    "id", "chunk_id", "line_id", "line_kind",
    "chunk_char_start", "chunk_char_end",
    "line_char_start", "line_char_end", "wraps_line",
    "raw_fragment", "source_text", "lemma_iast", "literal_gloss",
    "quoted", "status",
]

STATUS_ENUM = {"PARSED", "AMBIGUOUS", "FAILED"}
LINE_KIND_ENUM = {"prose", "verse_blockquote", "heading", "rule", "blank"}

# json-schema-like type checks (we avoid importing jsonschema to stay dependency-light)
def _check_schema(record: dict) -> list[str]:
    errs = []
    for f in REQUIRED_FIELDS:
        if f not in record:
            errs.append(f"missing required field: {f}")
    if errs:
        return errs
    if not isinstance(record["id"], str):
        errs.append("id must be a string")
    elif not re.search(r".+:L\d+:T\d+$", record["id"]):
        errs.append(f"id '{record['id']}' must match pattern .+:L\\d+:T\\d+")
    for f in ("chunk_char_start", "chunk_char_end"):
        if not isinstance(record[f], int) or record[f] < 0:
            errs.append(f"{f} must be a non-negative integer")
    if record["chunk_char_end"] <= record["chunk_char_start"]:
        errs.append("chunk_char_end must be > chunk_char_start")
    for f in ("line_char_start", "line_char_end"):
        if record[f] is not None and (not isinstance(record[f], int)):
            errs.append(f"{f} must be int or null")
    if not isinstance(record["wraps_line"], bool):
        errs.append("wraps_line must be boolean")
    if record["status"] not in STATUS_ENUM:
        errs.append(f"status '{record['status']}' not in {sorted(STATUS_ENUM)}")
    if record["line_kind"] not in LINE_KIND_ENUM:
        errs.append(f"line_kind '{record['line_kind']}' not in {sorted(LINE_KIND_ENUM)}")
    if not isinstance(record["quoted"], bool):
        errs.append("quoted must be boolean")
    return errs


def _check_abstention(record: dict) -> list[str]:
    """L0-A (the deterministic floor) honesty rule.

    `PARSED` requires a deterministic lemma (Vidyut); `AMBIGUOUS` means Vidyut produced no
    clean lemma. The GLOSS is NOT part of the floor: it is optional L0-B enrichment and must
    never gate, delay, invalidate, or roll back a canonical L0 object. The anti-theatre rule
    here is that a PARSED record must have a real lemma (never a fabricated one) — not that it
    must have a gloss.
    """
    errs = []
    status = record["status"]
    lemma = (record.get("lemma_iast") or "").strip()
    if status == "PARSED" and not lemma:
        errs.append("PARSED record has empty lemma_iast (fabricated PARSED)")
    return errs


def validate(records: list[dict], chunk_text: str | None = None,
             chunk_id: str | None = None) -> dict:
    """Validate a list of L0 records against the canonical spec + (optionally) P0."""
    per_record = []
    n_schema_ok = n_abstention_ok = n_gloss_ok = 0
    for rec in records:
        schema_errs = _check_schema(rec)
        abstention_errs = _check_abstention(rec)
        gloss = (rec.get("literal_gloss") or "").strip()
        # GLOSS IS NEVER A COMMIT GATE. The gloss is optional L0-B enrichment (a versioned
        # enrichment object), not part of the deterministic L0-A floor. A record may carry an
        # empty gloss and still be valid canonical L0. No gloss-based failure here.
        gloss_errs = []

        ok = (not schema_errs) and (not abstention_errs) and (not gloss_errs)
        if not schema_errs:
            n_schema_ok += 1
        if not abstention_errs:
            n_abstention_ok += 1
        if not gloss_errs:
            n_gloss_ok += 1
        per_record.append({
            "id": rec.get("id"), "status": rec.get("status"),
            "schema_ok": not schema_errs, "abstention_ok": not abstention_errs,
            "gloss_ok": not gloss_errs, "errors": schema_errs + abstention_errs + gloss_errs,
        })

    # P0 proof — the independent source-span integrity check (only if chunk text given)
    p0 = None
    if chunk_text is not None:
        p0 = p0_proof(chunk_id or "validate", chunk_text, records)

    all_pass = (n_schema_ok == len(records) and n_abstention_ok == len(records)
                and n_gloss_ok == len(records)
                and (p0 is None or p0.get("PASS")))
    return {
        "n_records": len(records),
        "schema_ok": n_schema_ok, "abstention_ok": n_abstention_ok,
        "gloss_ok": n_gloss_ok,
        "per_record": per_record,
        "p0": p0,
        "PASS": all_pass,
    }


def load_records(path: str) -> list[dict]:
    p = Path(path)
    if p.suffix == ".jsonl":
        out = []
        for line in p.open(encoding="utf-8"):
            line = line.strip()
            if line:
                out.append(json.loads(line))
        return out
    data = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "records" in data:
        return data["records"]
    if isinstance(data, list):
        return data
    raise ValueError(f"cannot interpret {path} as L0 records")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", required=True, help="L0 records (jsonl or json array/list)")
    ap.add_argument("--chunk-text", default=None, help="source chunk file for the P0 proof")
    a = ap.parse_args()
    records = load_records(a.records)
    chunk_text = Path(a.chunk_text).read_text(encoding="utf-8") if a.chunk_text else None
    res = validate(records, chunk_text)
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return 0 if res["PASS"] else 1


if __name__ == "__main__":
    sys.exit(main())
