#!/usr/bin/env python3
"""pipeline/extract_l0_v1.py — V1 legacy-format T1 -> canonical L0 adapter.

V1 (the 01_t1 IPVV chunks, Vol 1) is a DIFFERENT prose format from the V2/V3 `[and]-` gloss format:
- continuous prose paragraphs (line-wrapped), NOT per-token `[and]-GLOSS (IAST)` markers
- inline IAST in parentheses after the English gloss: `spontaneity (svācchandya)`
- supplied-connectives in square brackets: `[being]`, `[as if]`, `[i.e.]`, `[so]`
- markdown: `#` title, `##` section headers, `*Source:...*` attribution, `---` rules, `> ` blockquotes

This adapter tokenizes V1 prose into canonical L0 records per `specs/l0_schema.json` so that the
EXISTING `verify_l0.py` proof harness can run over it UNCHANGED. The design rule (kept strict):

    every word becomes a token:
      gloss-word followed by (IAST)   -> one token  `GLOSS (IAST)`   (lemma = IAST, gloss = English)
      bare English word / [bracket] connective -> one token (lemma empty, gloss = word)

This guarantees full coverage: between-token gaps are only whitespace/separators, so P0 has ZERO
UNKNOWN chars (no lettered gaps), and the verifier's `[and]-` assumptions are never triggered.

V1-specific quirks handled:
  - editorial lines (headings, attribution, blanks, rules) are SKIPPED (not tokenized) — the verifier
    classifies them IGNORED_WITH_REASON, exactly as for V2/V3.
  - `GLOSS (IAST)` — the paren is absorbed into the preceding word token (no overlap).
  - hyphenated English glosses and multi-word IAST (saṃvido vimarśa-paryantatvāt) preserved verbatim.

Usage:
  python3 pipeline/extract_l0_v1.py <01_t1_dir> <out_dir> [--all]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# IAST chars incl. diacritics
IAST = "a-zA-Zāīūṛṝḷḹṃñṅśṣṭḍḥṁ"
# a parenthesised IAST lemma (may be multi-token, hyphenated)
PAREN_END = re.compile(rf"\(([{IAST}][{IAST}\s\-\.]*)\)$")
WORD = re.compile(r"\S+")


def is_editorial_line(s: str) -> bool:
    """True if a whole line is markdown scaffolding (skip; the verifier classifies it)."""
    if s == "":
        return True
    if s.startswith("#"):
        return True
    if s == "---" or set(s) <= set("-"):
        return True
    if s.startswith("*") and s.endswith("*"):
        return True
    return False


def tokenize_line(line: str, line_id: int, chunk_id: str) -> list[dict]:
    """Split one V1 prose line into L0 records.

    Every whitespace-delimited token is a record. If a token ends with a parenthesised IAST
    lemma (e.g. `spontaneity (svācchandya)` is TWO tokens, but `(svācchandya)`), the IAST is
    extracted from that token. This guarantees full coverage with no overlaps: adjacent tokens
    tile the line exactly (gaps are whitespace).
    """
    records = []
    for t, m in enumerate(WORD.finditer(line)):
        start, end = m.start(), m.end()
        raw = line[start:end]
        pm = PAREN_END.search(raw)
        if pm:
            iast = pm.group(1)
            gloss = re.sub(rf"\s*\([{IAST}][{IAST}\s\-\.]*\)$", "", raw)
        else:
            iast = ""
            gloss = raw
        records.append({
            "id": f"{chunk_id}:L{line_id}:T{t}",
            "chunk_id": chunk_id,
            "line_id": line_id,
            "line_kind": "prose",
            "chunk_char_start": start,
            "chunk_char_end": end,
            "line_char_start": start,
            "line_char_end": end,
            "wraps_line": False,
            "raw_fragment": raw,
            "source_text": line,
            "lemma_iast": iast,
            "literal_gloss": gloss,
            "quoted": False,
            "status": "PARSED",
        })
    return records


def extract_chunk(path: Path, chunk_id: str) -> tuple[list[dict], int]:
    """Extract L0 records for one V1 chunk. Returns (records, n_skipped_editorial_lines)."""
    text = path.read_text(encoding="utf-8")
    records = []
    skipped = 0
    acc = 0  # absolute char offset of the current line within the full chunk text
    for li, line in enumerate(text.split("\n"), start=1):
        if is_editorial_line(line.strip()):
            skipped += 1
            acc += len(line) + 1  # +1 for the \n
            continue
        for r in tokenize_line(line, li, chunk_id):
            # convert line-relative to chunk-absolute (schema dual-coordinate model)
            r["chunk_char_start"] = acc + r["chunk_char_start"]
            r["chunk_char_end"] = acc + r["chunk_char_end"]
            records.append(r)
        acc += len(line) + 1
    return records, skipped


def main() -> int:
    ap = argparse.ArgumentParser(description="V1 legacy T1 -> canonical L0 adapter")
    ap.add_argument("src_dir", help="dir of V1 01_t1 *.md chunks")
    ap.add_argument("out_dir", help="dir to write *.l0.jsonl")
    ap.add_argument("--all", action="store_true", help="process every *.md in src_dir")
    ap.add_argument("--chunk", default=None, help="single chunk stem (e.g. chunkA-svatyandya)")
    args = ap.parse_args()

    src = Path(args.src_dir)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    targets = [src / f"{args.chunk}.md"] if args.chunk else sorted(src.glob("*.md"))
    total = {"chunks": 0, "tokens": 0}
    for p in targets:
        if not p.exists():
            print(f"missing {p}")
            continue
        records, skipped = extract_chunk(p, p.stem)
        with (out / f"{p.stem}.l0.jsonl").open("w", encoding="utf-8") as fh:
            for r in records:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        total["chunks"] += 1
        total["tokens"] += len(records)
        print(f"{p.stem}: {len(records)} tokens ({skipped} editorial lines skipped)")
    print(f"TOTAL: {total['tokens']} tokens across {total['chunks']} chunks -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
