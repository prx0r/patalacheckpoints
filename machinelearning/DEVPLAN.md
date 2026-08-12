# PĀṬALA — COMPREHENSIVE DEV PLAN (execution)

*2026-08-12. Turns the frozen ML strategy (`MLUSEINPATALA.md`), the grounded vision
(`VISION-COMPUTABLE-TRADITION.md`), and the verified corpus state (`IPVV-STACK-INTEGRATION.md`) into a
granular, ordered execution plan with concrete steps and tests. **Every task names: what to build, the
exact files, the test that proves it, and how to run it.***

> **Ground truth (verified 2026-08-12, updated after Phase 0A/2A):** 49 published IPVV passages (lazy
> JSON store, `data/published/ipvv/`), 63 C1 read/ renderings **wired into the 49 objects as
> `c1.verse_commentary[]`** (V1 multi-C1), 63 `c1/source/` records (10 + 53 derived), reader Commentary
> toggle now RENDERS for IPVV passages, THEMES exposed (`/api/themes` + `get_themes` MCP), and the 4
> deterministic verify services shipped (`/api/verify/*`). L200 validator passes. Test tooling:
> `npx tsx tests/*.test.ts` (invariants) · `python3 tests/api_suite.py` (needs dev server) ·
> `npm run lint` · `npm run build`.

---

## 0. Workflow & test conventions (apply everywhere)

- **Test-first per step:** write/extend the invariant test (`tests/*.test.ts`) that the new behavior
  must satisfy, before or with the implementation.
- **Run:** `npx tsx tests/<file>.test.ts` for data/loader invariants; `python3 tests/api_suite.py` for
  HTTP routes (start `npm run dev` first); `npm run lint && npm run build` before any merge.
- **Never overwrite:** canonicals, originals (`l200_legacy/`, `c1/_essay-material-legacy/`,
  `_archive_generated/`), or prior experiment outputs (`experiments/<id>/`).
- **Version everything ML** (per frozen rules): dataset version · split manifest · model · seed · git
  commit · hyperparameters · metrics · predictions · errors.
- **Commit discipline:** each phase is one coherent commit (or a small sequence), with the test first.

---

## PHASE 0A — Corpus + C1 publication (no ML)

Goal: the 63 C1s are machine-queryable and render in the reader. **No THEMES yet.**

### 0A.1 — Chunk→C1 id mapping (deterministic)
- **What:** a mapping from each of the 49 published passage `chunk` names to the list of covering
  `c1/read/*.md` files. The 14 V1 chunks each map to several C1s (`upoddhata`/`purvapaksa`/`k1.x`).
- **Where:** `pipeline/c1_map.py` producing `data/published/ipvv/c1_index.json`
  `{ chunk: { locator, c1: [{ id, title, file }] } }`.
- **Rule:** derived from the file-id convention (V2-A ↔ V2A; V1H ↔ V1H-upoddhata-k6-k8…). Manual
  verification for the 14 V1 chunks; machine for V2/V3.
- **Test:** `tests/c1_map.test.ts` — asserts every published chunk resolves to ≥1 C1, and every C1
  file appears in exactly the chunks that cover it (no orphans, no double-count within a chunk unless
  real).
- **Run:** `npx tsx tests/c1_map.test.ts`.

### 0A.2 — Emit the C1 bodies into the lazy store
- **What:** extend `pipeline/emit_published_json.py` (or a new pass) to attach `c1` to each passage
  record, shaped like the 1.5.11 exemplar:
  ```ts
  c1: {
    body: "<first L2 sentence as one-line summary>",
    verse_commentary: [
      { locator: "<chunk · section>", commentary: "<c1/read/c1_<id>.md body>" },
      ... // one per covering C1
    ],
    claim_links: []   // optional, Phase 7
  }
  ```
- **Also attach** `l200` (the audit sections) and `decisions` (derived from MT decisions) so the AUDIT
  view + `/api/resolve` are richer.
- **Test:** `tests/ipvv_published.test.ts` — extend: every published passage with a covering C1 now
  has `pub.c1.verse_commentary.length ≥ 1`, and the first entry's locator matches the chunk.
- **Run:** `python3 pipeline/emit_published_json.py --in <phase1 jsonl> --out data/published/ipvv`
  then `npx tsx tests/ipvv_published.test.ts`.

### 0A.3 — Render C1 in the reader
- **What:** the reader already renders `pub.c1.verse_commentary` (line ~239). Verify it renders for the
  lazy IPVV passages (it should, once `shapeIpvv` passes `c1` through — extend `shapeIpvv` in
  `data/corpus/published.ts` if needed).
- **Test:** `tests/ipvv_published.test.ts` — assert `pub.c1` present for a V2 and a V1 passage; manual
  visual check via `npm run dev` on `/read/isvarapratyabhijnavivrtivimarsini/<chunk>`.
- **Run:** `npm run dev`, open a chunk, toggle Commentary.

### 0A.4 — Complete the 53 `c1/source/` structured records
- **What:** for each `c1/read/*.md` lacking a `c1/source/` record, generate the structured record
  (SUMMARY ≈ body; FUNCTION/LOCAL CONTEXT from the argument map; KEY TERMS from `Terms:`; BOUNDARY from
  the body's boundary sentence; RELATED from `See also`). Mechanical-but-verified derivation.
- **Where:** `c1/source/c1_<id>.md` in the IPVV stack.
- **Test:** a `validate_c1_source.py` (or extend `l200_validate.py` pattern) asserting all 63 have both
  representations and the required sections.
- **Run:** the C1-source validator; then re-run 0A.2 to include the structured SUMMARY/FUNCTION in the
  emitted `c1` (better machine features).

### 0A.5 — Done criterion
- All 63 C1s queryable; every published IPVV passage with a covering C1 renders commentary; `tests/`
  green; `npm run build` green. — **DONE (2026-08-12)**: `attach_c1.py` wired the C1s as
  `verse_commentary[]` (49 passages, 72 entries incl. V1 multi-C1); `gen_c1_source.py` completed the
  53 records; reader renders; tests + build green.

---

## PHASE 1 — Pāṭala Benchmark Suite v0

Goal: a small, hard, human-reviewed, leakage-safe eval substrate — BEFORE any production model.

### 1.1 — Define the four suites + schema
- **What:** fixture schema per suite:
  ```
  PATALA-RETRIEVAL  { query, work, relevant_passage_ids[], hard_negatives[] }
  PATALA-EVIDENCE   { claim, supporting[], counterevidence[], crux[] }
  PATALA-FIDELITY   { source, c1, theme, guide, correct:bool }
  PATALA-STRUCTURE  { pair_a, pair_b, relation_type, evidence[] }
  ```
- **Where:** `data/benchmark/` (JSONL per suite) + a `schema.json`.
- **Test:** `tests/benchmark_schema.test.ts` — every fixture validates against the schema; every
  referenced passage/C1 id resolves via `getPublishedTranslation`/the store.

### 1.2 — Seed 50–100 hard fixtures (human/editor-reviewed)
- **Start smaller-but-harder:** ~15 retrieval, ~15 evidence, ~10 fidelity, ~10 structure. Include hard
  negatives (e.g. two passages sharing *vimarśa* vocabulary but different doctrinal job).
- **Source the positives/negatives from:** the L200 cross-references (typed relations), the C1
  `See also` edges, the pilot's known clusters, the essays.
- **Record reviewer + decision + confidence per fixture** (feeds inter-rater later).
- **Test:** `tests/benchmark_gold.test.ts` — asserts the gold references resolve and the hard negatives
  are genuinely distinct (not trivially redundant).

### 1.3 — Fix leakage split policy BEFORE development
- **What:** implement a split utility that enforces the policy (passage → chunk → vimarśa/argument-family
  → work-held-out) and refuses a train/test split that leaks an argument-family.
- **Where:** `data/benchmark/split.py`.
- **Test:** `tests/benchmark_split.test.ts` — asserts no argument-family straddles train/test under the
  chosen policy.

### 1.4 — Reproducibility harness
- **What:** `experiments/<id>/` scaffold (config.yaml, split_manifest.json, metrics.json, predictions.jsonl,
  errors.md, decision.md) + a runner that records dataset version, split manifest, seed, commit.
- **Test:** `tests/experiment_harness.test.ts` — a dummy run produces all files + a complete decision.md.

### 1.5 — Done criterion
- 4 suites, 50–100 reviewed fixtures, leakage-safe split, reproducibility harness, all tests green.

---

## PHASE 2A — Deterministic EXPOSE services

Goal: the verification floor as machine access — thin services over existing data.

### 2A.1 — `/verify-quote`
- **What:** verify a quote is a verbatim (normalized) substring of a source span / translation span.
- **Where:** `app/api/verify-quote/route.ts` + `lib/verify.ts`.
- **Test:** `tests/api_suite.py` + `tests/verify.test.ts` — a real quote passes; a "cleaned" non-verbatim
  quote is flagged.

### 2A.2 — `/verify-claim-structure`
- **What:** given a claim id, check evidence resolves · source exists · citation valid · review state.
- **Where:** `app/api/verify-claim/route.ts` (structure mode) + `lib/verify.ts`.
- **Test:** a claim with valid evidence passes; a claim with dangling evidence fails.

### 2A.3 — `/trace-dependency-structure`
- **What:** walk the derivation DAG backward (guide ← theme ← C1 ← L2 ← source) and report where support
  breaks.
- **Where:** `app/api/trace-dependency/route.ts` + `lib/trace.ts`.
- **Test:** a full chain resolves; a deliberately-broken link reports the break point.

### 2A.4 — `/find-counterevidence` (curated)
- **What:** return the explicit `contradicts`/`qualifies` edges for a claim/passage (no inference).
- **Where:** `app/api/find-counterevidence/route.ts` + `lib/evidence.ts`.
- **Test:** returns the tagged edges only; returns empty (not error) when none.

### 2A.5 — MCP tools
- **What:** add `verify_quote`, `verify_claim_structure`, `trace_dependency`, `find_counterevidence`
  to `mcp/index.mjs`.
- **Test:** `tests/mcp.test.mjs` — each tool returns a well-formed, non-empty response for a known input.

### 2A.6 — Done criterion
- 4 services + 4 MCP tools, all returning explicit-structure (never invented), tests green, build green.
  — **DONE (2026-08-12)**: `lib/verify.ts` + `/api/verify/{quote,claim-structure,trace-dependency,
  counterevidence}` + 4 MCP tools; verified end-to-end; build green.

---

## PHASE 3 — Retrieval baselines

Goal: a real index + strong baselines to beat.

### 3.1 — Sanskrit-aware tokenizer
- **What:** a tokenizer that handles inflection/sandhi/compounds (or honestly delegates). The current
  `search_surface_occurrences` is substring-only (`lemmatized: false`) — this is the E0.5 fix.
- **Test:** `tests/tokenizer.test.ts` — known inflectional forms of a lemma map together; a compound
  splits expectedly.

### 3.2 — Embedding index
- **What:** index the C1s (+ L2 texts) with a dense embedder (sentence-transformers or an API).
- **Test:** `tests/embedding_index.test.ts` — retrieval returns doctrinally-relevant passages for a
  probe; hard negatives rank low.

### 3.3 — Baselines on `PATALA-RETRIEVAL`
- **What:** BM25 · dense · hybrid (BM25+dense) evaluated on the suite.
- **Metrics:** Recall@5, MRR@10, nDCG@10, with bootstrap CI + paired significance.
- **Where:** `experiments/E1-retrieval/`.
- **Test:** `tests/eval_runner.test.ts` — the runner reports the metrics dict + CI for each baseline.

### 3.4 — Done criterion
- Baselines measured, reproducible, with CIs; results recorded in `experiments/E1-retrieval/`.

---

## PHASE 4 — Late interaction (ColBERT-style)

- **What:** multi-vector token-level retrieval, benchmarked against the Phase 3 baselines.
- **Test:** `tests/eval_runner.test.ts` — same metrics; assert a reported delta vs each baseline with CI.
- **Adopt only if:** significant improvement on held-out `PATALA-RETRIEVAL` (frozen rule), not visual.
- **Where:** `experiments/E1-retrieval/colbert/`.

---

## PHASE 0B / 5 — THEMES pilot against the benchmark

Goal: run the THEMES mechanism against the human-reviewed fixtures (NOT before).

### 5.1 — Build THEMES over all 63 C1s
- **What:** the hybrid relation graph (semantic + curated `See also` + shared KEY TERMS + sequence +
  interlocutor + function) → community detection (Louvain/Leiden, overlapping) → ThemeProposal →
  `themes/proposals/`.
- **Where:** `pipeline/themes/` (extend `themes_pilot.py` to production).
- **Rule:** use curated `See also` + KEY TERMS, NOT shared body-words (pilot finding).

### 5.2 — ThemeProposal lifecycle
- **What:** MACHINE_PROPOSED → EDITOR_REVIEWED → ACCEPTED/REJECTED/SUPERSEDED; save proposals and
  accepted separately (`themes/proposals/` vs `themes/accepted/`); never overwrite.
- **Test:** `tests/themes.test.ts` — every proposal's members resolve; every accepted theme has edge
  evidence + a THEME BOUNDARY; status lifecycle is valid.

### 5.3 — Evaluate against `PATALA-STRUCTURE`
- **What:** measure acceptance rate · edit burden · novel-theme yield · false-affinity rate against the
  human-reviewed fixtures.
- **Where:** `experiments/E2-themes/`.
- **Test:** `tests/eval_runner.test.ts` — reports the four theme metrics + CI.

### 5.4 — Expose `/api/themes` + MCP tool
- **What:** query a theme → its C1s → passages; query a C1 → its themes.
- **Test:** `tests/api_suite.py` + `tests/mcp.test.mjs`.

### 5.5 — Done criterion
- THEMES built + evaluated on the benchmark + exposed; the flagship experiment (text/struct/hybrid/
  learned) can now run.

---

## PHASE 6 — The flagship experiment (text / structure / hybrid / learned)

- **What:** four arms on `PATALA-STRUCTURE` + `PATALA-RETRIEVAL`:
  TEXT (C1 embeddings) vs STRUCTURE (terms/relations/sequence/roles) vs HYBRID vs LEARNED (graph rep).
- **EXPERIMENT ≠ PRODUCTION:** run the LEARNED arm even if expected to lose; adopt into production only
  on a benchmark win + cost + interpretability.
- **Where:** `experiments/E2-themes/flagship/`.
- **Test:** `tests/eval_runner.test.ts` — all four arms report the same metrics with CIs + paired tests.

---

## PHASE 7 — Semantic verification

### 7.1 — Claim extraction (Claimify-style)
- **What:** decompose C1/essay prose into atomic, decontextualized claims; evaluate coverage +
  independence + decontextualization + semantic preservation.
- **Test:** `tests/claims.test.ts`.

### 7.2 — `/verify-claim-semantic`
- **What:** entailment / scope / polarity / attribution, modeled on RAGChecker/MedRAGChecker (NLI + KG
  consistency).
- **Test:** `tests/verify_semantic.test.ts`.

### 7.3 — `/discover-counterevidence`
- **What:** adversarial retrieval (SUCEA-style claim decomposition + iterative evidence + entailment).
- **Test:** `tests/discover_counterevidence.test.ts`.

### 7.4 — Vertical Fidelity Benchmark
- **What:** the depth ladder (`L2→C1→Theme→Guide` + GEN-Z) as controlled positives; the corruption set
  (NEGATION_LOSS, SCOPE_STRENGTHENING, CERTAINTY_INFLATION, ATTRIBUTION_ERROR, BOUNDARY_ERASURE,
  AGENT_SWAP) as negatives. **Name it:** *Vertical Fidelity Benchmark for Multi-Resolution Scholarly
  Explanation.*
- **Where:** `data/benchmark/PATALA-FIDELITY/` + `experiments/E5-vertical-fidelity/`.
- **Test:** `tests/fidelity.test.ts` — a detector catches each corruption type; a faithful
  simplification passes.

---

## PHASE 8 — Graph / argument ML (frontier)

- R-GCN / CompGCN / NBFNet / GraphGPS-style experiments on the scholarly graph (trace-dependency,
  relation paths, concept journeys as graph traversals).
- **Test:** `tests/eval_runner.test.ts`; **production adoption** gated per frozen rule.

---

## PHASE 9 — Advanced representations + transfer

- Hypergraph · hyperbolic · cross-work transfer (train IPVV, test held-out work) · counterfactual
  dependency.
- **The transfer result is the "bigger than the source" proof.**

---

## PHASE 10 — The vision surfaces (build on the phases above)

These render the `VISION-COMPUTABLE-TRADITION.md` products, each consuming the earlier phases:

| Vision product | Consumes | First cut |
|---|---|---|
| **Epistemic gearbox** (AI tutor retrieves by depth) | Phase 3/4 retrieval + the depth ladder | `app/ask/` a depth-aware QA route choosing GUIDE/C1/THEME/L200 by query |
| **Misconception maps** | term dossiers + trajectories + semantic-distance ladders | a `misconceptions.ts` + `/concepts/[slug]` render |
| **Semantic-distance ladder per concept** | the paired-transformation data (7.4) | a `depths.ts` + reader depth selector |
| **Audio narration** | the graph's structure (sequence/themes/definitions) | a script generator over a C1/theme |
| **Video-as-projection** | a theme + C1s + term packs + misconceptions | a storyboard generator |
| **Concept journeys** | theme graph + graph path traversal (Phase 8) | a journey builder endpoint |
| **Self-explaining corpus** | all EXPOSE services + the graph | the `/api/resolve` richer + an explain endpoint |

---

## The overall sequence (with tests)

```
0A  corpus+C1 publication      tests: c1_map, ipvv_published, c1_source validator
1   benchmark suite v0         tests: benchmark_schema/gold/split, experiment_harness
2A  EXPOSE services            tests: verify, trace, counterevidence, mcp
3   retrieval baselines        tests: tokenizer, embedding_index, eval_runner
4   late interaction           tests: eval_runner (delta + CI)
0B/5 THEMES vs benchmark       tests: themes, eval_runner
6   flagship experiment        tests: eval_runner (4 arms)
7   semantic verification      tests: claims, verify_semantic, discover_counterevidence, fidelity
8   graph/argument ML          tests: eval_runner
9   transfer + advanced        tests: eval_runner (transfer)
10  vision surfaces            tests: per-product
```

**Each phase gates the next.** Nothing past Phase 1 is built until the benchmark exists; nothing past
2A is a model until the EXPOSE floor exists; nothing is adopted into production without a benchmark win,
a fixed held-out test, statistical rigor, and human review — per the frozen `MLUSEINPATALA.md`.
