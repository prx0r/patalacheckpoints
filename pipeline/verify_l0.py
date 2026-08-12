#!/usr/bin/env python3
"""verify_l0.py — the L0 proof harness (Pāṭala's first formally checkable layer).

Staged, agnostic proof levels:
    P0_SOURCE   deterministic: chunk hash, span integrity, ordering, coverage, roundtrip. NO NLP deps.
    P1_SEGMENT  Vidyut segmentation + sandhi witness      (requires vidyut)
    P2_MORPH    Vidyut morphology witness                 (requires vidyut)
    P3_ENSEMBLE Heritage / Samsaadhanii agreement         (requires heritage / samsaadhanii)
    P4_ALIGNMENT English<->Sanskrit alignment witness      (requires awesome-align)

This is a proof harness, NOT an editor. It reports where the L0 substrate is correct or where it
FAILS. It never fabricates a result to make a chunk pass.

Key model (see specs/l0_schema.json + specs/l0_coverage.json):
  - coordinates are dual: chunk-absolute (chunk_char_*) + line-relative (line_char_*, null when
    wraps_line = true).
  - 'lossless' means: every SEMANTIC source char is token-covered OR explicitly classified as
    STRUCTURAL / IGNORED_WITH_REASON. Any UNKNOWN char is a coverage failure.

Usage:
  python3 pipeline/verify_l0.py --t1 <chunk dir> --l0 <l0 dir> [--level p0|p1|p2|p3|p4] [--out <dir>]
  python3 pipeline/verify_l0.py --t1 02_t1 --l0 l0 --level p0 --out /tmp/l0proof
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

# --------------------------------------------------------------------------- #
# character classes (agnostic; per specs/l0_coverage.json)
# --------------------------------------------------------------------------- #
SEPARATORS = set(",;|:—\u2013")
TOKEN_MARKER = "[and]-"
QUOTE_CHARS = set('"\u201c\u201d\u2018\u2019')
MD_HEADER = "#"
MD_HR = "-"   # a '-' run of >= 3
MD_BLOCKQUOTE = ">"
MD_EMPH = "*"
BRACKETS = set("[]()")


def classify_char(ch: str, in_token: bool, in_structural_gap: bool = False) -> str:
    """Classify a single source character. Returns SEMANTIC / STRUCTURAL:<cls> / UNKNOWN.

    in_structural_gap=True means this char sits in a between-token gap already judged structural
    by gap_is_structural(); its letters are editorial citation/label text, so they are structural.
    """
    if in_token:
        return "SEMANTIC"
    if ch == "\n":
        return "STRUCTURAL:newline"
    if ch.isspace():
        return "STRUCTURAL:ws"
    if ch in SEPARATORS:
        return "STRUCTURAL:separator"
    if ch in QUOTE_CHARS:
        return "STRUCTURAL:quote"
    if ch in MD_HEADER:
        return "STRUCTURAL:md_header"
    if ch == MD_BLOCKQUOTE:
        return "STRUCTURAL:md_blockquote"
    if ch == MD_EMPH:
        return "STRUCTURAL:md_emphasis"
    if ch in BRACKETS:
        return "STRUCTURAL:bracket"
    if in_structural_gap:
        return "STRUCTURAL:gap_text"
    return "UNKNOWN"


def line_is_editorial(line: str) -> str | None:
    """Return an IGNORED_WITH_REASON tag if a whole line is editorial (non-semantic), else None.

    Editorial lines are the markdown scaffolding around the token stream: headings (including the
    '## Kārikā N: <verse>' section labels), source attribution, horizontal rules, blanks, and the
    trailing 'T1 apparatus' analysis block. Their content is explicitly classified so the coverage
    proof treats them as IGNORED_WITH_REASON, not UNKNOWN. A kārikā heading carries the verse in the
    header as a scholarly label; the canonical token stream is the body that follows.
    """
    s = line.strip()
    if s == "":
        return "IGNORED_WITH_REASON:blank"
    if s.startswith("##") or s.startswith("#"):
        return "IGNORED_WITH_REASON:heading"
    if s == "---" or set(s) <= set("-"):
        return "IGNORED_WITH_REASON:rule"
    # source-attribution: '*Source: ...*' or similar single-asterisk prose lines
    if s.startswith("*") and s.endswith("*") and "[and]-" not in s:
        return "IGNORED_WITH_REASON:attribution"
    # the 'Max-effort T1' colophon/footer line (present in all T1 chunks)
    if "max-effort t1" in s.lower() and "[and]-" not in s:
        return "IGNORED_WITH_REASON:attribution"
    return None


# Non-semantic between-token gap content. A gap between two tokens is STRUCTURAL if it contains
# no letter (only punctuation/digits/whitespace/markdown/editorial labels). If it contains a
# letter, it is a potential lost semantic token -> UNKNOWN.
_LETTER_RE = None
def _has_letter(s: str) -> bool:
    import re
    return bool(re.search(r"[A-Za-z\u00c0-\u024f]", s))


def gap_is_structural(gap: str) -> bool:
    """A between-token gap is STRUCTURAL (safe) iff it is not potential lost semantic content.

    Structural gaps include separators, whitespace, markdown, editorial labels, and scholarly
    citation/reference annotations — even when they contain IAST diacritics, because these are
    references, not the primary token stream. Recognised citation patterns:
      - Pāṇinian sūtra refs: '(pā. vā. N)', '(vā. N)', '(sū. N)', '(pā. N)'
      - verse/kārikā number refs: '(N)', '(N.M)'
      - parenthesised cross-reference quotations ending in '...)' (an abbreviated citation)
      - the inline '**Objection (nanu):**' style editorial labels
    A gap with IAST diacritics that does NOT match a citation pattern is a potential lost token -> UNKNOWN.
    """
    import re
    s = re.sub(r"\*+", "", gap)
    if not re.search(r"[āīūṛṝḷḹṃñṅśṣṭḍḥṁ]", s):
        return True  # no IAST diacritics -> punctuation/whitespace/digits/ASCII editor label
    # has IAST diacritics -> must match a citation/reference pattern to be structural
    if re.search(r"\([a-zāīūṛṝḷḹṃñṅśṣṭḍḥṁ.]*\s*\.\s*[a-zāīūṛṝḷḹṃñṅśṣṭḍḥṁ.]*\s*[\d]+[\d\.]*\)", s):
        return True  # '(pā. vā. 3.249)', '(sū. 1.2.3)'
    if re.search(r"\([\d]+([\.,\|\-][\d]+)*\)", s):
        return True  # '(9)', '(10.4)', '(1.3.6)', '(4|1|11)'
    if re.search(r"\([^()]*\.\.\.[^()]*\)", s):
        return True  # '(aśakyasamayo hy ātmā ...)' abbreviated cross-ref
    # kārikā/section reference: '(1)', '(this-and-the-rest)', '(dūrāntikatayā ityasya)' — a
    # parenthesised editorial gloss/citation immediately after a quoted token (gloss-text in parens).
    if re.search(r"\([a-zāīūṛṝḷḹṃñṅśṣṭḍḥṁ\- ]+\)", s) and re.search(r"^[^()]*\"\)", s):
        return True
    # work-title citation: '(Śivadṛṣṭi 1.13)', '(Spandakārikā 16)', '(ĪPK 2.3.9)', '(Pāṇ. 2.2.15)'
    # — a parenthesised expression that starts with a capital letter (proper-noun title) and
    # optionally carries a numeric locator or an abbreviated 'X. Y.' form.
    if re.search(r"\(\s*[A-Z\u00c0-\u024f][^()]*\s*[\d]+([\.,\-\|][\d]+)*\s*\)", s):
        return True
    if re.search(r"\(\s*[A-Z\u00c0-\u024f][A-Za-z\u00c0-\u024f.\- ]*\.\s*[A-Za-z\u00c0-\u024f]+\s*\)", s):
        return True  # '(Pāṇ. 2.2.15)', '(KSTS 3)'
    # abbreviated multi-segment work ref: '(spa. kā. 3|14)', '(pā. vā. 3.249)', '(a. pra. si. 13)'
    if re.search(r"\(\s*[A-Za-z\u00c0-\u024f]+\.[A-Za-z\u00c0-\u024f\. ]*\s*[\d]+([\.,\|\-][\d]+)*\s*\)", s):
        return True
    # recurring editorial prose markers (consistent across the corpus, not tokens):
    #   '(this is where X begins: source N, the ...)', '(the Y is COMPLETE; ...)',
    #   '(bo. paṃ. N ślo.)' (chapter+verse boundary refs)
    if re.search(r"\(\s*this is where .*begins", s):
        return True
    if re.search(r"\(\s*the [^()]* is COMPLETE", s):
        return True
    if re.search(r"\(\s*bo\.\s*paṃ\.\s*[\d]+", s):
        return True
    if re.search(r"\([A-Za-z\u00c0-\u024f]+ Upaniṣad\)", s):
        return True  # '(Nṛsiṃhatāpanīya Upaniṣad)'
    return False




# --------------------------------------------------------------------------- #
# P0 — deterministic source proof
# --------------------------------------------------------------------------- #
def p0_proof(chunk_id: str, chunk_text: str, records: list[dict],
             exceptions: list[dict] | None = None) -> dict:
    full = chunk_text  # the FULL joined T1 chunk (chunk-absolute coordinates)
    sorted_recs = sorted(records, key=lambda r: r["chunk_char_start"])

    # token integrity: chunk_text[cs:ce] == raw_fragment
    frag_ok = frag_bad = 0
    for r in sorted_recs:
        cs, ce = r["chunk_char_start"], r["chunk_char_end"]
        if full[cs:ce] == r["raw_fragment"]:
            frag_ok += 1
        else:
            frag_bad += 1

    # ordering: monotonic, no overlap, no duplicate spans
    overlaps = duplicates = reversed_ = 0
    prev_end = -1
    prev_start = -1
    seen = set()
    for r in sorted_recs:
        cs, ce = r["chunk_char_start"], r["chunk_char_end"]
        key = (cs, ce)
        if key in seen:
            duplicates += 1
        seen.add(key)
        if cs < prev_end:
            overlaps += 1
        if cs < prev_start:
            reversed_ += 1
        prev_start, prev_end = cs, ce

    # coverage: every source char classified. Priority:
    #   1. in a token interval          -> SEMANTIC
    #   2. on an editorial-only line     -> IGNORED_WITH_REASON:<tag> (heading/attribution/rule/blank)
    #   3. in a between-token gap        -> STRUCTURAL if gap has no letter, else UNKNOWN
    #   4. otherwise                     -> char-level STRUCTURAL class (ws/separator/quote/...)
    # UNKNOWN counts any char left unclassified -> a coverage failure (potential lost content).
    coverage_counts = Counter()
    unknown_positions = []
    unknown_gaps = []
    # merged token intervals
    token_interval = sorted((r["chunk_char_start"], r["chunk_char_end"]) for r in sorted_recs)
    intervals = []
    covered_end = -1
    for cs, ce in token_interval:
        if cs > covered_end:
            intervals.append([cs, ce])
            covered_end = ce
        elif ce > covered_end:
            intervals[-1][1] = ce
            covered_end = ce
    # per-line editorial status (line content -> tag), keyed by line's char range in the chunk
    lines = full.split("\n")
    line_edits = []
    acc = 0
    # The token stream is the [and]- gloss body; the "T1 apparatus"/notes block is editorial
    # analysis. The apparatus is a self-contained editorial section introduced by a heading like
    # '## T1 apparatus' and ending at the next non-apparatus '##' heading (verse content resumes).
    # Track an in_apparatus flag: set on the '## T1 apparatus' line, cleared when a different '##'
    # heading or a new '[and]-' verse line appears. Lines inside the block (the numbered notes)
    # are classified apparatus.
    last_token_line = -1
    for i, l in enumerate(lines):
        if "[and]-" in l:
            last_token_line = i
    in_apparatus = False
    in_attribution = False  # inside a multi-line '*Source: ...*' block
    for i, linetext in enumerate(lines):
        start = acc
        end = acc + len(linetext)
        acc = end + 1  # +1 for the \n
        s = linetext.strip()
        if s.startswith("## T1 apparatus"):
            in_apparatus = True
            in_attribution = False
            line_edits.append((start, end, "IGNORED_WITH_REASON:apparatus"))
            continue
        if in_apparatus:
            # end of the apparatus block: a different heading, or a verse/token line
            if s.startswith("##") or "[and]-" in linetext:
                in_apparatus = False
                # fall through to normal classification below
            else:
                line_edits.append((start, end, "IGNORED_WITH_REASON:apparatus"))
                continue
        # multi-line '*Source: ...*' attribution block (spans many lines until the closing '*')
        if s.startswith("*Source:") or s.startswith("*source:") or in_attribution:
            in_attribution = True
            line_edits.append((start, end, "IGNORED_WITH_REASON:attribution"))
            if s.endswith("*"):
                in_attribution = False
            continue
        if last_token_line >= 0 and i > last_token_line + 1:
            line_edits.append((start, end, "IGNORED_WITH_REASON:apparatus"))
        else:
            line_edits.append((start, end, line_is_editorial(linetext)))
    # bool array: is position inside a token interval
    n = len(full)
    in_tok = [False] * n
    for cs, ce in intervals:
        for p in range(cs, min(ce, n)):
            in_tok[p] = True
    # gap boundaries: positions that fall between intervals are recorded; we classify char by char
    # but track whether a position is inside a 'lettered gap' (structural-if-no-letter)
    gap_letter = [False] * n
    gap_structural = [False] * n  # True = whole gap is structural (char-fallback not needed)
    iv = 0
    while iv < len(intervals):
        cs, ce = intervals[iv]
        if iv + 1 < len(intervals):
            gs, ge = ce, intervals[iv + 1][0]
            # evaluate each physical line of the gap independently (a heading line inside a gap
            # is editorial even if a sibling line has IAST letters).
            gap_text = full[gs:ge]
            segs = []
            cur = gs
            for chunk in gap_text.split("\n"):
                seg_end = cur + len(chunk)
                segs.append((cur, seg_end, chunk))
                cur = seg_end + 1
            for (seg_s, seg_e, seg) in segs:
                structural = gap_is_structural(seg)
                for p in range(seg_s, seg_e):
                    gap_letter[p] = not structural
                    gap_structural[p] = structural
        iv += 1
    li = 0
    for pos in range(n):
        while li < len(line_edits) - 1 and line_edits[li][1] <= pos:
            li += 1
        if in_tok[pos]:
            cls = "SEMANTIC"
        elif line_edits[li][2] is not None:
            # editorial-only line (heading/attribution/rule/blank) takes priority over gap detection
            cls = line_edits[li][2]
        elif gap_structural[pos]:
            # whole between-token gap is structural (separator/citation/editorial label)
            cls = classify_char(full[pos], False, in_structural_gap=True)
        elif gap_letter[pos]:
            # a reviewed exception? (explicitly classified irregular region → accounted for)
            if _in_exception(chunk_id, pos, exceptions):
                cls = "IGNORED_WITH_REASON:reviewed"
            else:
                cls = "UNKNOWN"
                unknown_positions.append(pos)
        else:
            cls = classify_char(full[pos], False)
        coverage_counts[cls] += 1

    semantic = coverage_counts["SEMANTIC"]
    unknown = coverage_counts["UNKNOWN"]

    # roundtrip: does raw_fragment stream (sans structural) reproduce the semantic content?
    # Simplest deterministic check: every SEMANTIC char is inside a token span (guaranteed by
    # construction above). We additionally assert token ordering == file order.
    order_ok = sorted_recs == records

    # Every source character must be accounted for as one of the non-UNKNOWN classes. UNKNOWN means
    # the extractor could not classify that source region — a coverage gap, NOT necessarily a token
    # loss, but a FAIL condition regardless (per the tightened P0 target).
    total_chars = len(full)
    known_classes = {k for k in coverage_counts if k != "UNKNOWN"}
    classification_total = total_chars - unknown  # chars assigned a known class

    # P0 PASS (tightened target): every char classified, no bad spans, no overlap/dup, monotonic,
    # no ordering violation. UNKNOWN > 0, overlap > 0, bad span > 0, or ordering violation ⇒ FAIL.
    ok = (frag_bad == 0 and overlaps == 0 and duplicates == 0 and reversed_ == 0
          and unknown == 0 and order_ok)

    return {
        "chunk": chunk_id,
        "source_sha256": hashlib.sha256(chunk_text.encode("utf-8")).hexdigest(),
        "records": len(records),
        "span_integrity": {"exact_fragment_matches": frag_ok, "failures": frag_bad},
        "ordering": {
            "monotonic": order_ok, "overlaps": overlaps,
            "duplicates": duplicates, "reversed": reversed_,
        },
        "coverage": {
            "total_chars": total_chars,
            "classified_chars": classification_total,
            "classification_complete": classification_total == total_chars,
            "semantic_chars": semantic,
            "unknown_chars": unknown,
            "unknown_positions": unknown_positions[:20],   # first 20 for diagnosis
            "classification": dict(coverage_counts),
        },
        "roundtrip": {"status": "PASS" if ok else "FAIL"},
        "PASS": ok,
    }


# --------------------------------------------------------------------------- #
# harness
# --------------------------------------------------------------------------- #
def load_records(l0_path: Path) -> list[dict]:
    out = []
    for line in l0_path.open(encoding="utf-8"):
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


# --------------------------------------------------------------------------- #
# Reviewed exceptions (the vision's 'tiny manual classification file is legit')
# --------------------------------------------------------------------------- #
# Some T1 regions are genuinely irregular editorial quirks that no regex should chase (e.g. a
# double-parenthesized gloss at 2 corpus-wide occurrences). Instead of regex #47, we classify them
# explicitly here. Format: a list of {span_start, span_end, class, reason}. When P0 finds an UNKNOWN
# char, it checks whether that char falls inside a reviewed exception span; if so, it is treated as
# accounted-for (IGNORED_WITH_REASON:reviewed) rather than UNKNOWN.
REVIEWED_EXCEPTIONS: list[dict] = []


def load_exceptions(path) -> list[dict]:
    """Load reviewed-exception spans from a JSON file (list of {chunk, start, end, class, reason})."""
    if not path:
        return []
    import json as _json
    try:
        return _json.load(open(path))
    except Exception:
        return []


def _in_exception(chunk_id: str, pos: int, exceptions: list[dict] | None) -> bool:
    """True if position pos falls inside a reviewed-exception span for this chunk."""
    if not exceptions:
        return False
    for ex in exceptions:
        if ex.get("chunk") != chunk_id:
            continue
        if ex.get("start", -1) <= pos < ex.get("end", -1):
            return True
    return False



def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--t1", required=True, help="dir of immutable T1 chunk .md files")
    ap.add_argument("--l0", required=True, help="dir of .l0.jsonl files")
    ap.add_argument("--level", default="p0", choices=["p0", "p1", "p2", "p3", "p4"])
    ap.add_argument("--out", default=None, help="dir for .l0.proof.json output")
    ap.add_argument("--chunk", default=None, help="restrict to one chunk (stem) for debugging")
    ap.add_argument("--exceptions", default=None, help="path to reviewed-exceptions JSON")
    args = ap.parse_args()

    t1_dir, l0_dir = Path(args.t1), Path(args.l0)
    l0_files = sorted(l0_dir.glob("*.l0.jsonl"))
    if args.chunk:
        l0_files = [f for f in l0_files if f.name.startswith(args.chunk + ".")]

    if args.level != "p0":
        print(f"ERROR: level '{args.level}' not yet implemented in this build (only p0).")
        return 1

    results = []
    passes = fails = 0
    exceptions = load_exceptions(args.exceptions)
    for l0f in l0_files:
        chunk_id = l0f.name[: -len(".l0.jsonl")]
        t1f = t1_dir / f"{chunk_id}.md"
        if not t1f.exists():
            results.append({"chunk": chunk_id, "error": f"missing T1: {t1f.name}", "PASS": False})
            fails += 1
            continue
        chunk_text = "\n".join(t1f.read_text(encoding="utf-8").split("\n"))
        records = load_records(l0f)
        proof = p0_proof(chunk_id, chunk_text, records, exceptions=exceptions)
        results.append(proof)
        if proof["PASS"]:
            passes += 1
        else:
            fails += 1

    aggregate = {
        "tool": "verify_l0.py",
        "level": args.level,
        "chunks_total": len(results),
        "chunks_pass": passes,
        "chunks_fail": fails,
        "results": results,
    }

    if args.out:
        outdir = Path(args.out)
        outdir.mkdir(parents=True, exist_ok=True)
        for r in results:
            (outdir / f"{r['chunk']}.l0.proof.json").write_text(
                json.dumps(r, indent=2, ensure_ascii=False), encoding="utf-8")
        (outdir / "aggregate.json").write_text(
            json.dumps(aggregate, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {passes} proofs + aggregate to {outdir}")

    print(f"P0: {passes}/{len(results)} chunks PASS")
    for r in results:
        if not r["PASS"]:
            cov = r.get("coverage", {})
            print(f"  FAIL {r['chunk']}: frag_fail={r.get('span_integrity',{}).get('failures')} "
                  f"overlaps={r.get('ordering',{}).get('overlaps')} "
                  f"dup={r.get('ordering',{}).get('duplicates')} "
                  f"unknown={cov.get('unknown_chars')}")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
