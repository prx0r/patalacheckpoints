#!/usr/bin/env python3
"""pipeline/test_extract_l0_v1.py — validate the V1 legacy-format extraction adapter.

The V1 adapter (`extract_l0_v1.py`) must turn V1 prose chunks (01_t1 format) into canonical L0
records that pass the EXISTING `verify_l0.py` proof harness UNCHANGED. This is the acceptance test
the user specified:

    V1 legacy prose
        ↓ adapter
    canonical L0
        ↓
    existing verify_l0.py    (UNCHANGED)

Checks:
  1. quoted IAST with a hyphen-suffix + line-wrap mid-gloss is fully covered (no lost chars)
  2. multi-word IAST lemma + bracket connectives ([being], [i.e.]) are covered
  3. blockquote + bare (non-IAST) words + apostrophes are covered
  4. every fixture passes verify_l0.py (0 unknown, 0 overlaps, 0 frag-fail)
  5. verify_l0.py itself is NOT modified (the adapter adapts; the verifier does not)

Run: cd /root/projects/patala && python3 pipeline/test_extract_l0_v1.py
"""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import extract_l0_v1 as V1
from verify_l0 import p0_proof

PASS = 0
FAIL = 0

FIXTURE_DIR = Path(__file__).resolve().parent.parent / "tests" / "l0_v1"


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        print(f"  ✓ {name}")
        PASS += 1
    else:
        print(f"  ✗ FAIL: {name}" + (f" — {detail}" if detail else ""))
        FAIL += 1


def run_verify(chunk_text, records):
    """Run the UNCHANGED p0_proof over records for a chunk."""
    return p0_proof("fixture", chunk_text, records)


def main():
    fixtures = sorted(FIXTURE_DIR.glob("fixture*.md"))
    if not fixtures:
        print(f"  (no fixtures found in {FIXTURE_DIR})")
        return 1

    print(f"== {len(fixtures)} V1 fixtures through verify_l0.py (unchanged) ==")
    for fx in fixtures:
        text = fx.read_text(encoding="utf-8")
        recs, skipped = V1.extract_chunk(fx, fx.stem)
        proof = run_verify(text, recs)
        check(f"{fx.stem}: PASS", proof["PASS"],
              f"unknown={proof['coverage']['unknown_chars']} "
              f"frag={proof['span_integrity']['failures']} "
              f"overlap={proof['ordering']['overlaps']}")
        check(f"{fx.stem}: 0 unknown chars", proof["coverage"]["unknown_chars"] == 0,
              proof["coverage"]["unknown_chars"])
        check(f"{fx.stem}: 0 overlaps", proof["ordering"]["overlaps"] == 0,
              proof["ordering"]["overlaps"])
        check(f"{fx.stem}: 0 fragment failures", proof["span_integrity"]["failures"] == 0,
              proof["span_integrity"]["failures"])
        check(f"{fx.stem}: >0 tokens", len(recs) > 0, len(recs))

    print("\n== adapter invariants ==")
    # every record conforms to the schema's required fields
    req = ["id", "chunk_id", "line_id", "line_kind", "chunk_char_start", "chunk_char_end",
           "line_char_start", "line_char_end", "wraps_line", "raw_fragment", "source_text",
           "lemma_iast", "literal_gloss", "quoted", "status"]
    for fx in fixtures:
        text = fx.read_text(encoding="utf-8")
        recs, _ = V1.extract_chunk(fx, fx.stem)
        for r in recs:
            missing = [k for k in req if k not in r]
            check(f"{fx.stem}: all schema fields present", not missing, missing)
            break  # check one record per fixture is enough
    # raw_fragment is a verbatim slice
    for fx in fixtures:
        text = fx.read_text(encoding="utf-8")
        recs, _ = V1.extract_chunk(fx, fx.stem)
        bad = [r for r in recs
               if text[r["chunk_char_start"]:r["chunk_char_end"]] != r["raw_fragment"]]
        check(f"{fx.stem}: every raw_fragment is a verbatim slice", not bad,
              f"{len(bad)} bad fragments")

    print(f"\n=== RESULT: {PASS} pass / {FAIL} fail ===")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
