# L0 STANDARDIZATION — the verifiable substrate

*2026-08-12. Recommended next work (from `handover/LOG.md` + `handover/agent-2-integration/INDEX.md`).
Goal: make L0 a standardised,
fully-verifiable substrate that "no one can argue with." Everything above L0 — C1, themes, hub,
journey, verify, essays, ML retrieval — rests on these tokens. If L0 isn't provably correct and
complete, the stack is built on sand.*

---

## 1. WHY THIS IS THE NEXT WORK

- **L0 is the floor.** It is the token-level literal substrate: every record is one word/fragment
  of the immutable T1 text, with IAST lemma + literal gloss + char provenance.
- **Current state:** 35 L0 files exist (`translations/_stack/ipvv/l0/*.l0.jsonl`), extracted by
  `t1_extract.py`. But there is **no verification tool beyond the extractor**, no round-trip proof,
  no formal schema contract, no CI gate.
- **The user's requirement:** "a standardised system that no one can argue with." That requires
  *deterministic, automated, auditable* proofs that L0 is faithful, complete, and lossless.

---

## 2. THE L0 SCHEMA CONTRACT (`l0_schema.json`)

Every L0 record MUST have these fields:

| field | type | invariant |
|-------|------|-----------|
| `id` | string | `{chunkId}:L{line}:T{token}` — unique, immutable |
| `chunk_id` | string | must match an existing T1 chunk id |
| `line_id` | string | which line of the chunk this token is on |
| `line_kind` | string | e.g. `verse` / `prose` / `lemma` (see T1 line kinds) |
| `source_text` | string | the immutable text this came from |
| `raw_fragment` | string | the exact literal token (byte-accurate from T1) |
| `char_start` | int | start offset (≥ 0) — **absolute offset in the FULL joined chunk text** (see §3) |
| `char_end` | int | end offset (> char_start) — **absolute offset in the FULL joined chunk text** |
| `lemma_iast` | string | the IAST lemma for this token (may be empty only if status FAILED) |
| `literal_gloss` | string | literal meaning (may be empty only if status FAILED) |
| `quoted` | boolean | is this token inside a quote |
| `status` | enum | `PARSED` \| `AMBIGUOUS` \| `FAILED` |

### Contract invariants (the "cannot argue" rules)
1. **Completeness:** per chunk, PARSED + AMBIGUOUS + FAILED = total tokens in the T1 chunk.
2. **Losslessness (round-trip):** the `raw_fragment`s, in file order, reconstruct the FULL joined T1
   chunk text with no silent invention/skip/reorder (see §3 — spans are absolute, not per-line).
3. **No gaps / no overlap:** `char_start`/`char_end` spans tile the full chunk text with no gaps and
   no overlap (see §3 — this is checkable against the FULL joined chunk, not per-line `source_text`).
4. **Well-formed lemma:** `lemma_iast` uses only IAST characters (no Devanagari/script mixing).
5. **Consistency:** a FAILED token must have empty `lemma_iast` + empty `literal_gloss`; a PARSED
   token must have both non-empty.
6. **Immutability:** `id` and `chunk_id` never change; a fix creates a new L0 version, never edits
   in place.

---

## 3. THE ROUND-TRIP VERIFIER (`verify_l0.py`)

The "no one can argue" proof — L0 is a faithful, complete, lossless tokenization of T1.

**⚠ Correction (verified against `t1_extract.py` + the emitted L0 data):** do **NOT** implement this
as a naive byte-equal string comparison, and be aware of a **coordinate-system bug** in the current
data. Two facts, both confirmed empirically (chunk `chunkV2-C-vistanti-ajadapramatrsiddhi`):

1. **`char_start`/`char_end` are ABSOLUTE offsets into the FULL joined chunk text**, NOT per-line
   offsets. `t1_extract.py` runs `tokenize_line` over the whole chunk joined by `\n` (`full =
   "\n".join(lines)`), computes spans against that, and only later remaps `source_text` to the
   containing line (`lines[ln-1]`) via `line_of()`. Result: for **100% of records** (2187/2187),
   `char_end > len(source_text)`. So you **cannot** resolve a span against `source_text` as stored.

2. **`raw_fragment` and `literal_gloss`** ARE correct and recoverable — the slice
   `full[char_start:char_end]` equals `raw_fragment` (verified). The glossary/lemma content is sound;
   it is only the **span↔source_text coordinate mapping** that is broken.

The correct proof therefore operates on the **FULL joined chunk text**, reconstructed per line:

```
For each L0 file:
   1. load the immutable T1 chunk; build full = "\n".join(T1 lines)
   2. sort all records by char_start (absolute offsets into full)
   3. assert spans tile `full` with no gaps and no overlap:
        first.char_start == 0
        span[i+1].char_start == span[i].char_end   (allowing the separators , ; | : – " and the
                                                    [and]- marker as the ONLY inter-token material)
        last.char_end == len(full)
   4. assert full[char_start:char_end] == raw_fragment for every record (verbatim)
   5. assert status counts sum to total tokens (invariant 1)
   6. cross-check against the extractor's existing .l0.report.txt (PARSED/AMBIGUOUS/FAILED)
   7. (optional, once fixed) re-emit source_text with corrected per-line spans
   PASS  → print "OK  <chunk_id>  N tokens  lossless (full-chunk)"
   FAIL  → print the first mismatch (offset, expected vs actual) and exit non-zero
```

**Two known data issues to expect and report (not paper over):**
- **247/267 lines have gaps between consecutive token spans** in the current data (tokens the
  tokenizer did not emit, e.g. the very first `[and]-…` on a line), so the tiling check WILL fail on
  the data as-is. This is a *finding*, not a test bug: it means the current L0 is **not yet lossless**.
- **85/267 lines have `raw_fragment` not present verbatim in `source_text`** — a downstream effect of
  the span↔line coordinate mismatch, not a content error.

**Note:** `t1_extract.py` already emits `.l0.report.txt` (status counts) and `.l0.roundtrip.md` (a
best-effort visual diff) per chunk — the verifier should *assert over* these and extend them into the
automated full-chunk span-coverage proof, not reinvent the extraction. The immediate **build step is
to fix `t1_extract.py`'s coordinate system** (emit `char_start/char_end` as per-line offsets, or keep
absolute + add a `full_text` reference) so the proof can be byte-exact.

Exit code: 0 if all chunks pass, 1 if any fails. This is the auditable proof.

---

## 4. THE SCHEMA VALIDATOR (`validate_l0.py`)

- every record satisfies the schema (all required fields, correct types).
- invariant 4 (IAST-only lemmas) and invariant 5 (status ↔ field consistency).
- no duplicate `id`s; no orphaned `chunk_id` (must resolve to a T1 chunk).
- reports a summary: total records, by status, by chunk.

---

## 5. THE CROSS-LAYER CHECK (L0 → the rest)

Prove the provenance spine is provable top-to-bottom:
- every published passage / C1 `verse_commentary` source-span resolves to an L0 `line_id` range.
- `script` `pipeline/verify_provenance.py` (or extend `verify_l0.py`): walk every published
  passage, assert its `source` span maps onto L0 tokens, and that the quoted text matches the L0
  `raw_fragment`s.
- Result: no layer can assert anything that doesn't trace to a proven token.

---

## 6. THE CI GATE

- `tests/test_l0.py` runs `verify_l0.py` + `validate_l0.py` across all 35 (and any future) L0 files.
- A chunk that fails round-trip or validation **blocks the build**. This is the "standardised
  system": deterministic, automated, auditable — not a claim, a gate.

---

## 7. DELIVERABLES / DEFINITION OF DONE

1. `l0_schema.json` — the formal contract (this doc is the prose spec; the json is the machine form).
2. `verify_l0.py` — round-trip + span + status-count proofs.
3. `validate_l0.py` — schema + IAST + consistency validator.
4. `tests/test_l0.py` — CI gate wiring.
5. **Proof:** all 35 existing L0 files pass (or the failing ones are fixed/re-run).
6. `docs/INDEX.md` entry for this spec.

---

## 8. START HERE

1. Read `THE_COMPANION.md` + `VISION_AND_NAVIGATION.md` for the substrate model.
2. Read one existing L0 file + the `t1_extract.py` extractor to confirm the exact fields.
3. Write `l0_schema.json` from the contract in §2.
4. Write `verify_l0.py`, then `validate_l0.py`, then `tests/test_l0.py`.
5. Run them across the 35 files; fix the extractor or the data until everything passes.
6. Commit with a clear message (`feat: verifiable L0 substrate — schema, round-trip verifier,
   validator, CI gate`).
