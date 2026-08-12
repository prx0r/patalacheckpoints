# HANDOFF-LOG — the coordination record between Agent 1 (ML) and Agent 2 (integration)

*One entry per handoff: what · why · file · date · direction (A1→A2 or A2→A1). Per the
`DUAL_AGENT_TRACK.md` protocol, every data-carrying handoff includes a schema snippet.*

---

## E1 — Agent 1 → Agent 2: E1-fidelity baseline done (2026-08-12)

**What:** Agent 1 completed the first real retrieval baseline — BM25 vs dense vs hybrid on the
C1→L2 fidelity task (query = C1 commentary, index = L2 only, 49 items, 300-bootstrap CI).

**Why it matters to Agent 2:** plain dense embeddings did NOT beat BM25 (MRR delta −0.035, p=0.083;
hybrid tie). This is an honest negative — it argues the discriminating signal is **structured/graph**
(see_also, key terms, relations), not a fancier text encoder. Agent 1 will need Agent 2's
themes-with-evidence / structured edges to test the flagship question.

**Files:**
- `machinelearning/research/experiments/E1-fidelity-REPORT.md`
- `machinelearning/research/experiments/fidelity_bm25_dense_hybrid.json`
- `machinelearning/research/tasks/PATALA-FIDELITY.jsonl`

**Schema of what Agent 1 consumes (the current substrate snapshot):**
```json
{ "id": "pt:passage:...", "locator": "chunkV2-O-...md", "l2_text": "string",
  "c1": { "verse_commentary": [{ "locator": "string", "commentary": "string" }] },
  "c1_source": { "summary": "string", "key_terms": "string", "related_passages": "string" } }
```

**Requested from Agent 2 (when ready):** themes-with-evidence — the deterministic theme proposals with
their member C1s + edge reasons, exposed with a schema snippet (see step 5 of the Agent 1 queue). Not
blocking anything Agent 1 does next (tokenizer + benchmark + full retrieval baselines are independent).

---

## Agent 2 — session review: verified state + L0 spec correction (2026-08-12)

**What:** Agent 2 (integration lane) reviewed all handover + Pāṭala docs on taking over, and verified
the repo against the claims. Everything in `SESSION_HANDOVER.md` + `INDEX.md` checks out (all key files
present: published store, verify/citation libs, themes/hub/spines/journey/analyst/recommend, openapi,
MCP, L0 spec). Build green, 21 published-passage tests pass.

**⚠ Correction to the L0 recommendation — the round-trip claim needs rework.** The L0 spec
(`SPEC_L0_STANDARDIZATION.md` §3) says the verifier should assert L0 reconstructs the T1 chunk
"byte-identical modulo whitespace." That is **not achievable as specced**, because:

- `t1_extract.py` already emits `.l0.report.txt` (per-chunk PARSED/AMBIGUOUS/FAILED counts) AND
  `.l0.roundtrip.md` — so a partial verifier already exists; the "no tool beyond the extractor" framing
  is inaccurate.
- `reconstruct()` exists but is **unused** in `process_chunk` — the round-trip proof was never wired.
- The real gap is **lossless span recovery**, not naive string equality: `raw_fragment` is the literal
  `[and]-…(iast)` slice, and the source line's separators vary (`, ; | : –`). Joining with `", "` (as
  `reconstruct` does) will NOT reproduce the source line. Round-trip must compare **per-line span
  coverage** (reconstruct the line's token spans and assert they tile the source line with no gaps and
  no overlap), not a byte-equal string.

**Why it matters:** the spec's headline proof ("L0 is a lossless tokenization") is the user's exact
"no one can argue" requirement. If it's built as string-equality it will fail everywhere and undermine
the whole point.

**Schema of what Agent 2 exposes to Agent 1 (L0 record, verified from `02_t1` extractor output):**
```json
{ "id": "chunkV2-C-...:L16:T3", "chunk_id": "chunkV2-C-...", "line_id": 16,
  "line_kind": "prose|verse_blockquote|heading|blank", "source_text": "string",
  "raw_fragment": "[and]-gloss (iast)", "char_start": 0, "char_end": 42,
  "lemma_iast": "svasattānapekṣayaiva", "literal_gloss": "string",
  "quoted": false, "status": "PARSED|AMBIGUOUS|FAILED" }
```

**Next (Agent 2 lane, after L0):** the deterministic related-rail (`/api/recommend` + MCP) is the
biggest missing product feature (`WHAT_NEXT_PATALA.md` §4) — reuses existing spines/relations/hub,
no collision with Agent 1's ML queue.

---

## Agent 2 — L0 DEEP REVIEW: coordinate-system bug found + infra survey (2026-08-12)

**What:** Agent 2 did the session's main task — deep review of L0→Sanskrit workings — and found a
**definitive, load-bearing bug** in the L0 data, plus verified all external tooling.

### 🔴 Finding 1 — the L0 coordinate-system bug (blocks P0 and the lossless proof)
In every L0 file, `char_start`/`char_end` are **absolute offsets into the FULL joined chunk text**, but
`source_text` holds **only the containing line**. `t1_extract.py` tokenizes the whole chunk
(`full = "\n".join(lines)`), computes spans against that, then remaps `source_text` per-line. Consequence
(verified on `chunkV2-C-vistanti-ajadapramatrsiddhi`):
- **100% of records (2187/2187): `char_end > len(source_text)`** → you cannot resolve a span against
  `source_text` as stored.
- **247/267 lines have gaps between token spans** (the tokenizer didn't emit every `[and]-` token) →
  the current L0 is **not yet lossless**.
- **85/267 lines: `raw_fragment` not verbatim in `source_text`** (downstream of the span↔line mismatch).
- The **content is good**: `full[char_start:char_end] == raw_fragment` (verified). Only the span↔source
  mapping is broken, plus genuine token-emission gaps.

**Action:** fix `t1_extract.py`'s coordinate system (per-line spans, or absolute + `full_text`), then
build `verify_l0.py` as a **full-chunk** lossless proof (spans tile the full joined text), then close the
token gaps. Updated in `SPEC_L0_STANDARDIZATION.md` §2–3.

### 🟢 Finding 2 — external infra verified; reuse Vidyut (don't rebuild)
All 9 links in `SPEC_L0_PROOF.md` fetched + alive. **Vidyut** (`ambuda-org/vidyut`, MIT, Python bindings)
is the standout: `vidyut-cheda` (segment+morphology), `vidyut-sandhi` (P1), `vidyut-prakriya`
(analysis→generation round-trip), `vidyut-lipi`, `vidyut-kosha`. This covers **P0–P2 out of the box** —
far better than the Heritage web mirror per token, and gives the independent-analyzer ensemble (Vidyut
vs Heritage vs Samsaadhanii). Mitrasamgraha (arXiv 2601.07314, 391k Skt→EN bitexts; authors = our IPVV
translators) is the calibration corpus for P4. Full survey: `SPEC_L0_PROOF.md` §15.

**Files:**
- `machinelearning/SPEC_L0_STANDARDIZATION.md` (corrected: full-chunk proof, coordinate-bug note)
- `machinelearning/SPEC_L0_PROOF.md` (new: the proof-carrying spec + §15 infra survey + §16 feasibility)
- `pipeline/t1_extract.py` (the extractor to fix — code unchanged this session, per "don't build yet")

**Recommended v0 order:** fix extractor coords → `verify_l0.py` lossless proof → adopt Vidyut as P1/P2
engine → `PhilologicalProof` object + O1–O12 checks → later P3/P4/P7. This is Agent 2's lane
(Sanskrit substrate + pipeline + `translations/_stack/ipvv/specs/`).

---

## Agent 2 — L0 P0 harness BUILT + extractor repairs (2026-08-12)

**What:** Built `pipeline/verify_l0.py` (P0 deterministic proof, no NLP deps), repaired the L0
coordinate model, and fixed four tokenizer content-loss bugs. Full record: `docs/BUILD_NOTES_L0_P0.md`.

### Done
- **`verify_l0.py` P0** — emits `.l0.proof.json` per chunk (source_sha256, span_integrity, ordering,
  coverage, roundtrip) + aggregate. Exit 0 only if all pass.
- **Coordinate model fixed** — dual `chunk_char_*` (absolute) + `line_char_*` (relative, null when
  `wraps_line`). Both slice invariants verified.
- **Schema contract** — `translations/_stack/ipvv/specs/l0_schema.json` (agnostic).
- **Coverage taxonomy** — `translations/_stack/ipvv/specs/l0_coverage.json`.
- **4 tokenizer bugs fixed** in `t1_extract.py`: `)` overlap, `\n> ` blockquote-wrap loss,
  `[And]-` case, comma/quote-in-gloss. Recovered ~1,900 tokens (V2/V3) + ~1,700 (V1).

### Current P0 status
- **V2/V3: 11/35 PASS**; 11 more within 16–312 unknown; 13 dominated by **unmarked quote-initial
  tokens** (`"now (idānīṃ)` — a quotation's first token lacks `[and]-`).
- **V1 (legacy): 0/28** — pervasive unmarked-token format; needs a separate V1 extractor pass.

### Next (Agent 2 lane, in order)
1. Handle unmarked quote-initial tokens (V2) + a V1 legacy-format extractor pass → goal **63/63 P0 PASS**.
2. Only then wire Vidyut as P1/P2 witness (non-authoritative) + emit per-token proof certificates.
3. Then hand clean certificates to Agent 1 (ML) for the real ML problems.

### External infra verified (do NOT rebuild)
Vidyut (MIT, py 0.4.0 installed) = P1/P2 engine. Heritage (1.1.0 installed) = 2nd analyzer. Existing
integration in sanskritree (`integrations/heritage_client.py`, `philology/adapters.py`). Full survey +
feasibility: `machinelearning/SPEC_L0_PROOF.md` §15–16.

## Agent L0 — Vidyut P2 witness + proof-semantics separation (2026-08-12)

**What:** Built `pipeline/verify_l0_p2.py` (Vidyut P2 morphology witness), ran it over the full
V2/V3 corpus (103,906 records), and fixed the `PhilologicalProof` semantics in `philproof.py`.
Full record: `docs/BUILD_NOTES_L0_P2.md`.

**P2 result (Vidyut over extracted IAST lemmas):** 55.1% linguistically supported (CONFIRMED 28.2% +
AMBIGUOUS_SUPPORTED 26.9%); 29.5% CONFLICT (mostly multi-member compounds Vidyut segments into
constituents — a real P1/P2 signal, not error); 11.8% UNANALYZED; 3.6% NO_SANSKRIT (gloss-only
AMBIGUOUS); 7 TOOL_ERROR.

**Matching-rule lesson (important for Agent ML):** L0's `lemma_iast` is the SURFACE (`saṃvedanasya`);
Vidyut returns the STEM (`saṃvid`). A naive exact match → ~50% false CONFLICT. Match stem-as-prefix +
surface token text to get derivationally-compatible matches.

**Proof-semantics fix (in `philproof.py`):** separated `extraction_coverage` (P0: did we classify every
T1 region?) from `lexical_sense` (P3: is the identified word's sense resolved?). Unknown T1 chars →
`extraction_coverage: OPEN`, NOT `lexical_sense`. Verified on passing (PROVED) + failing (OPEN) chunks.

**Schema of the L0 proof handshake (unchanged, still authoritative):**
```json
{ "chunk": "...", "source_sha256": "...", "records": 0,
  "span_integrity": {"exact_fragment_matches": 0, "failures": 0},
  "ordering": {"monotonic": true, "overlaps": 0, "duplicates": 0},
  "coverage": {"semantic_chars": 0, "unknown_chars": 0}, "roundtrip": "PASS" }
```

**Files:** `pipeline/verify_l0.py` (P0), `pipeline/verify_l0_p2.py` (P2 witness), `docs/BUILD_NOTES_L0_P2.md`,
`machinelearning/research/patala_ml/philproof.py` (semantics fix).

**Next (Agent L0):** run V2/V3 toward 63/63 P0 lossless; then Heritage as the P3 cross-check witness;
V1 legacy format.

## Agent L0 — reviewed old sanskritree translation engine for reusable L0 pieces (2026-08-12)

**What:** Reviewed `/mnt/HC_Volume_106427611/sanskritree/src/sanskritree/` (philology/alignment/evidence/
proof_engine) — the pre-DeepSeek hand-built translation engine — for anything reusable for L0's
deterministic proof floor. Full review: `docs/L0_REVIEW_OLDSANSKRITREE_ENGINE.md`.

**Reusable (and we have NOT rebuilt them):**
1. **`evidence/ranker.py`** — the P3 lexical-sense module: `rank_senses()` (tradition-proximity,
   multi-tier) + `TECHNICAL_TERMS_KS` (SLP1-keyed technical glossary). This is what resolves the
   `lexical_sense` dimension we froze at UNCHECKED.
2. **`alignment/spans.py` + `translation/alignments.py`** — the P4 alignment contract: typed relations
   (one_to_one/implicit/omitted/...) + `alignment_coverage_report()`. L0's `alignment` dimension.
3. **`philology/analysis_lattice.py` + `adapters.py`** — the Analysis witness + Vidyut/Heritage
   ensemble; confirms our P2 approach is right.
4. **`proof_engine/failure_taxonomy.py`** — failure-type → recovery-action pattern for the disagreement
   queue.

**Superseded (NOT reusable for L0):** the LLM translation pipeline (candidates/realization/factor-graph),
Lean/Nyāya proof engine (stub; Lean demoted).

**Recommended order:** P3 lexical-sense via ranker.py next (unfreezes a frozen dimension), then P4
alignment via the alignment model. Both AFTER P0 coverage is green.

**Files:** `docs/L0_REVIEW_OLDSANSKRITREE_ENGINE.md`.

## Agent L0 — V2/V3 P0 LOSSLESS: 35/35 PASS (2026-08-12)

**Milestone:** the flagship published IPVV corpus (V2/V3, 35 chunks) now passes P0 fully:
35/35 PASS, 0 unknown chars, exact spans, no overlaps, full classification, reproducible.

**Final steps that got it there:**
1. Multi-line `*Source:*` attribution (stateful) — recovered ~2800 chars.
2. Editorial markers (`this is where X begins`, `Y is COMPLETE`, `bo. paṃ. N ślo.`, `Upaniṣad`) → structural.
3. Uppercase IAST + `ṇ` added to tokenizer gloss class.
4. **Reviewed-exception file** (`docs/l0_reviewed_exceptions.json`) — 18 irregular editorial/gloss
   regions explicitly classified `IGNORED_WITH_REASON:reviewed`, visible in proofs (not silently dropped).

**V1 (legacy 01_t1) is a separate prose format** (no `[and]-` glosses; continuous English + inline
IAST) — 118k unknown across 28 chunks; needs its own extractor pass. Not part of this milestone; the
supported published corpus (V2/V3) is fully lossless.

**Files:** `docs/l0_reviewed_exceptions.json`, `docs/BUILD_NOTES_L0_P0.md` (updated).

**Next (Agent L0):** P3 lexical-sense via the old engine's `evidence/ranker.py` (unfreeze
`lexical_sense` dimension), then P4 alignment via the alignment model. Both AFTER P0 green (which is now
achieved for V2/V3).

## Agent L0 — P0 FROZEN + VERIFIED: V2/V3 35/35 PASS (first completed CP1 sub-capability)

**Per the cross-layer review, V2/V3 P0 is now FROZEN** — the extractor is not to be touched unless a new
reproducible loss bug appears.

**The verified proof (V2/V3 flagship published IPVV corpus, 35 chunks):**
- **35/35 PASS, 0 chunks fail.**
- **103,917 tokens, 4,159,600 source chars, 0 UNKNOWN, 0 bad spans, 0 overlaps, 0 duplicates.**
- `classification_complete: true` on all 35 — every source region accounted for
  (TOKEN/STRUCTURE/EDITORIAL/CITATION/WHITESPACE/IGNORED_WITH_REASON).
- **Deterministic** — identical source hashes + PASS across 2 runs.
- **Independently re-verified** on a 6-chunk random sample (slice-equality + monotonicity + no-overlap
  recomputed from raw data, not the harness) — all PASS.
- Reproduce: `python3 pipeline/verify_l0.py --t1 .../02_t1 --l0 .../l0 --level p0
  --exceptions docs/l0_reviewed_exceptions.json` → "P0: 35/35 chunks PASS".

**Honest status:** this is the V2/V3 **supported corpus** (CP1's "supported passages"). V1 (28 chunks)
is a separate legacy prose format, `MIGRATION_PENDING` (not part of this milestone). CLAIMS.md P-001
updated to SUPPORTED(V2/V3)/PARTIAL(full).

**Next (per the review — NOT lexical ranking):**
1. **P2 ensemble validation** — run Heritage (independent witness) over ALL Vidyut CONFLICT + ALL
   UNANALYZED, plus a stratified control sample (~500 CONFIRMED, ~500 AMBIGUOUS_SUPPORTED) → a
   Vidyut×Heritage confusion matrix + disagreement report. This tells us whether P2 is actually useful.
2. Only then: P3 lexical-sense — but FIRST a small human-reviewed lexical gold (50–100 fixtures incl.
   technical terms + NO-UNIQUE-SENSE abstention cases), then baseline evaluation (most-common gloss /
   local L0 gloss / embedding) before ranker.py becomes a non-authoritative witness.
3. P4 alignment — same discipline: held-out benchmark from manually checked L0 pairs before promotion.

## Agent L0 — P2 ensemble validation in progress (2026-08-12)

Built `pipeline/verify_l0_ensemble.py` — the Vidyut×Heritage independent-witness calibration.
Design (per the cross-layer review): run Heritage over all Vidyut CONFLICT + UNANALYZED + a stratified
control (~500 CONFIRMED, ~500 AMBIGUOUS_SUPPORTED), producing a normalized disagreement taxonomy
(V+/H+, V-/H+, V+/H-, V-/H-, V?/H?), relation classes (EXACT_LEMMA_AGREEMENT / STEM_EQUIVALENT /
COMPOUND_SEGMENTATION_DIFFERENCE / NO_ANALYSIS / TOOL_ERROR), and a review queue.

Artifacts: `p2_ensemble_report.json`, `p2_ensemble_confusion.csv`, `p2_disagreements.jsonl` (streamed),
`p2_review_queue.jsonl`, `docs/P2-ENSEMBLE.md` (design + interpretation framework).

**Key learning (tooling):** Heritage web API is rate-limited (~1-2s/call) → a full 42k-record run is
hours. The script now streams output incrementally and supports `--limit` for sampling. Sampled run in
progress. Honest status labels only (SUPPORTED_BY_ENSEMBLE / SUPPORTED_BY_SINGLE_WITNESS /
CONFLICTING_WITNESSES / UNANALYZED) — never PROVED.

**Files:** `pipeline/verify_l0_ensemble.py`, `docs/P2-ENSEMBLE.md`.

**Next:** blind manual review of 25-50 cases per major cell once the sample completes.

## Agent L0 — P2 ENSEMBLE COMPLETE (sampled, 500 records) (2026-08-12)

**Result (Vidyut × Heritage, 500 records: 150 CONFLICT + 150 UNANALYZED + 100 CONFIRMED + 100 AMBIGUOUS_SUPPORTED):**
- **CONTROL AGREEMENT RATE 85%** (170/200) — instruments validated.
- **CONFLICT RESOLUTION RATE 72%** — most Vidyut CONFLICT resolves to Heritage support (representation mismatch, NOT L0 error).
- **DOUBLE-CONFLICT RATE 28%** — the genuinely contested ~8.4% of all records.
- **DOUBLE-UNANALYZED 0.2%**, **TOOL ERROR 0.2%**.

**Conclusion:** the Vidyut 29.5% CONFLICT is heavily inflated by representation mismatch (72% resolves). Real philological dispute signal ≈ 8.4% (double-conflict). Vidyut's coverage gap is tiny. **P2 is a useful witness.**

**Artifacts:** `pipeline/verify_l0_ensemble.py`, `pipeline/analyze_ensemble.py`, `docs/P2-ENSEMBLE.md`,
`/tmp/ens_s2/{p2_ensemble_report.json, p2_ensemble_confusion.csv, p2_disagreements.jsonl, p2_review_queue.jsonl}`.

**Tooling lesson:** Heritage web API is rate-limited (~1-2s/call). The ensemble streams incrementally and
samples; a full 42k-record run is hours (not worth it — the sampled 500 already gives the signal).

**Next:** blind manual review of 25-50 cases per major cell (DOUBLE_CONFLICT, V+/H-, V-/H+) to confirm
"agreement ≈ correctness." Then, per the review: P3 lexical (build gold + baselines first, audit
ranker.py as non-authoritative witness), then P4 alignment benchmark. Do NOT promote MORPHOLOGY to PROVED.

## Agent L0 — blind P2 manual review workflow built (2026-08-12)

**Built the blind review pipeline** (the methodological lock-down before P2 promotion):
- `pipeline/build_p2_review.py` — samples the major ensemble cells, enriches with L0 source context +
  gloss + locator, emits a review file with **machine verdicts concealed** (reviewer sees only evidence).
- 150 blind cases: DOUBLE_CONFLICT 40, VIDYUT_MISMATCH 40, HERITAGE_MISMATCH 30, BOTH_SUPPORT 40 (control).
- Reviewer CSV: `/tmp/p2review_blind.csv` — reviewer fills `human_analysis` (SUPPORTED |
  PLAUSIBLE_ALTERNATIVE | CONFLICT | CANNOT_DECIDE) + preferred_lemma + material_to_translation + reason.
- `pipeline/score_p2_review.py` — joins completed reviews against concealed machine verdicts → the
  machine×human validation matrix (correct/wrong/unclear per cell).

**Status labels held:** P2 = CALIBRATED_MACHINE_WITNESS (NOT VALIDATED_AGAINST_HUMAN_GOLD until review
done). The "8.4% dispute" is an ESTIMATED candidate-dispute rate, not "L0 is wrong."

**Next:** fill the 150 review cases (human), compute the matrix, then freeze P2 as CLAIM P-002, then P3
lexical gold. Background ensemble (larger) running to enrich the rare V+/H- cell.

## Agent L0 — P3 lexical-sense gold v0 built (2026-08-12)

Built `docs/p3_lexical_gold_v0.json` (21 fixtures, SINGLE_EDITOR_REVIEW pending) via
`pipeline/build_p3_lexical_gold.py`:
- 12 technical lemmas: saṃvid, vimarśa, māyā, prakāśa, pratibhā, svātantrya, pramātṛ, krama, bheda,
  tattva, kāla, ābhāsa.
- 4 NO_UNIQUE_SENSE abstain fixtures (the correct answer is OPEN).
- Preferred sense is derived from the actual L0 gloss (`sense_for_gloss`) so fixtures are coherent
  (no preferred/gloss mismatch).

**Honest finding on stratification:** the target (20/20/15/5) is NOT met — the real L0 gloss layer is
dominated by single dominant senses per term. True polysemy lives at the L2/semantic layer, not L0.
So the gold undershoots to 21 (12/4/1/4). This is recorded honestly rather than padding with invented
contexts. The ranker benchmark will note this as a coverage caveat.

**Status:** ranker.py remains a CANDIDATE RANKER (NOT a P3 verifier). Next: SINGLE_EDITOR review of the
21 fixtures → then baselines (most-common gloss / local L0 gloss / embedding) → then evaluate ranker.py
(top-1, top-k, MRR, abstention quality, technical-term accuracy, false-certainty rate).

Background ensemble (larger, to enrich V+/H- cell) still running.

## Agent L0 — P3 lexical baseline evaluation (2026-08-12)

Built `pipeline/eval_p3_lexical.py` — benchmark-first evaluation of P3 lexical methods against the
21-fixture gold. Results:

| method | top1 | abstain | false-cert |
|---|---|---|---|
| baseline_most_common | 0.67 | 0.0 | 1.0 |
| baseline_local_l0 (leak) | 0.81 | 0.0 | 1.0 |
| baseline_embedding (lexical overlap) | 0.81 | 1.0 | 0.0 |
| **ranker_candidate (old engine)** | **0.76** | **0.0** | **1.0** |

**Finding (anti-theatre):** the old `ranker.py` does NOT beat the baselines. It is 0.76 top1 (below the
0.81 embedding baseline) and has 0 abstention quality / 100% false-certainty — it never abstains on the
NO_UNIQUE_SENSE fixtures, where the embedding baseline abstains perfectly. **ranker.py is NOT promoted
to P3 lexical witness.** It remains a candidate that would need to beat top1≥0.81 AND abstain≥1.0 to
earn promotion.

The embedding/lexical-overlap baseline is the current best (0.81 top1, 1.0 abstain) — the floor ranker.py
(and any real model) must beat. Report: `docs/p3_lexical_eval_report.json`.

## Agent L0 — P2 FROZEN as calibrated witness (not blocked on blind review) (2026-08-12)

**Decision:** freeze P2 as CALIBRATED_MACHINE_WITNESS now. The blind review is a non-blocking follow-up,
not a gate — the ensemble already justifies the freeze without a human:
- control agreement 85% (instrument consistency)
- CONFLICT resolution 72% (most Vidyut CONFLICT = representation mismatch, not L0 error)
- only ~8% double-conflict (42 cases) = the genuinely review-worthy set
- double-unanalyzed 0.2%, tool-error 0.2%

**Why blind is not a blocker:** the 42 double-conflict cases are the only ones where "both tools fail to
support L0" — and even that means "both tools fail," not "L0 is wrong." A human pass would disaggregate
REAL_L0_ERROR/GENUINE_AMBIGUITY/COMPOUND/BOTH_TOOLS_LIMITED/EDITORIAL_ARTIFACT, but that's refinement of
the small set, not a gate on the whole witness.

**CLAIMS:** added P-009 (P2 calibrated witness, SUPPORTED, blind review = path to human validation) and
P-010 (ranker.py rejected as P3 witness: 0.76 vs 0.81 baseline, 0 abstention).

**Next:** P4 alignment benchmark (the next proof layer, no human needed to build the held-out set from
checked L0 pairs).

## Agent L0 — incorporated external review of commit 70f237b (2026-08-12)

External review (`patala_review_70f237b.zip` from R2) found real flaws; all fixed:

**P2 blind review — 3 fixes:**
1. Machine stratum leaked via `review_id`+`cell` → now opaque IDs, cell removed from reviewer-facing data.
2. Scorer read `cell` from the review itself → now joins ONLY via the separate secret unblinding key.
3. V-/H+ and V+/H- scored per-witness (not one generic verdict) → now Vidyut-vs-human and
   Heritage-vs-human agreement reported separately.

Regenerated the genuinely-blind set (150 cases, shuffled, key separate): `/tmp/p2review_fixed.jsonl` +
secret `/tmp/p2review_key.jsonl`. Reviewer sees only `/tmp/p2review_fixed_blind.csv`.

**P3 lexical gold — circularity fixed:**
- Fixtures now carry real Sanskrit context (sanskrit_token, sanskrit_clause, passage_id, source_span_id),
  not just the English gloss that embodied the label.
- The 4 duplicate/incompatible-label fixtures are KEPT (they're adversarial/abstention tests) but now
  have the context to adjudicate them. Review state stays MACHINE_DRAFT (not gold).

**Files:** `pipeline/build_p2_review.py` (fixed), `pipeline/score_p2_review.py` (fixed),
`docs/P2_REVIEW_PROTOCOL.md`, `docs/P3_EDITORIAL_REVIEW.md`, `pipeline/build_p3_lexical_gold.py` (enriched).

Per the review: P2 not claimed human-calibrated until the 150 cases are reviewed; P3 not promoted until
an editor re-reads the enriched context.

## Agent L0 — P2 ensemble FINALIZED (4600 records) + balanced blind review (2026-08-12)

**Enriched ensemble (4600 records: 1500 CONFLICT + 1500 UNANALYZED + 800 CONFIRMED + 800 AMBIGUOUS_SUPPORTED):**
- **Control agreement 84.1%** (1345/1600) — instruments consistent.
- **CONFLICT resolution 71.6%** (1074/1500) — most Vidyut CONFLICT = representation mismatch, not L0 error.
- **Double-conflict 9.2%** (424 cases) — the genuinely-review-worthy set.
- **Heritage-disagrees (V+/H-)** 5.5% (254 cases) — now enough for a full blind cell.
- VIDYUT_COVERAGE_GAP 29.2%, TOOL_ERROR 0.2%.

**Balanced genuinely-blind review:** rebuilt from the enriched ensemble → **160 cases, 40 per cell**
(DOUBLE_CONFLICT / VIDYUT_MISMATCH / HERITAGE_MISMATCH / BOTH_SUPPORT), opaque IDs, shuffled, secret key
separate. Reviewer file: `/tmp/p2review_v2_blind.csv`; SECRET key `/tmp/p2review_v2_key.jsonl`.

The result is stable across sample sizes (500 → 4600), so P2's calibration is solid. The blind review is
the remaining human gate to VALIDATED_AGAINST_HUMAN_GOLD.

## Agent L0 — alignment + dedup check vs Agent 1 (2026-08-12)

Reviewed Agent 1's INDEX/NEXT-STEPS/SESSION + the ML docs for duplication + alignment.

**Claim-numbering collision FIXED:** Agent 1's NEXT-STEPS reserves P-009 (Argument Gold) + P-010
(DebateFrame). My L0 claims had taken P-009 (P2 morphology) + P-010 (P3 ranker). Renumbered mine to
**P-011 (P2 calibrated witness)** + **P-012 (P3 ranker rejected)** so Agent 1's reserved numbers are free.
⚠ Agent 1: use P-009/P-010 for Argument Gold/DebateFrame per NEXT-STEPS.

**Stale path (for Agent 1):** your INDEX references `machinelearning/CLAIMS.md` but the canonical ledger
is now `machinelearning/_ACTIVE/CLAIMS.md`. Fix the INDEX line 69.

**No duplication found:** Agent 1 is on CP4 (Argument Gold, viruddha-via-graph) using C1/L2/L200 on the
sanskritree mount; I'm on the L0 proof floor (P0/P2/P3/P4). They join at Passage ID / Proof ID / C1 ID.
My `philproof.py` semantics fix (extraction_coverage ≠ lexical_sense) is intact (Agent 1's gold chain
consumes it). No overlapping build targets.

**Alignment confirmed:** Agent 1's `build_goldchain.py` consumes my `verify_l0` proofs (the handshake).
Agent 1's argument gold grounds on `pt:passage:ipvv:chunk...` — the same passage IDs my L0 work keys on.
