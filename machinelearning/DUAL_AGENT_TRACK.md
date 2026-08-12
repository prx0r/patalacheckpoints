# DUAL-AGENT TRACK — two specialized agents, one shared project

*2026-08-12. Split expertise and context across two agents working the same Pāṭala + Sanskritree
codebase, so neither holds the other's deep context and neither blocks the other. Each owns a lane;
both write to the same evidence graph and the same canonical docs.*

---

## 1. The two lanes (clean split, no overlap)

| | **Agent 1 — the ML/RESEARCH engineer** | **Agent 2 — the Pāṭala/expert integrator** |
|---|---|---|
| Role | ML + eval + retrieval + the research story | integration + scholarly content + docs + Sanskrit |
| Domain | arxiv, embeddings, graph ML, retrieval, benchmarks | the pāṭala codebase, the IPVV stack, Dyczkowski/Ratié register, the scholarly ontology |
| Owns | `machinelearning/` (MLUSEINPATALA, DEVPLAN, PATALAML, benchmark, experiments/) | `data/`, `app/`, `lib/`, `pipeline/`, the reader/API/MCP, the factory, `translations/_stack/ipvv/specs/` + process notes |
| Special context | the 26-paper curriculum, statistical rigor, leakage rules | the exact file layout, the scholarly standard (L200/C1), the "AI proposes ≠ Pāṭala asserts" rule |
| Tests | benchmark eval, retrieval metrics | invariant tests, build green, API/MCP contract |

**The load-bearing rule:** Agent 1 never builds on structure Agent 2 hasn't exposed; Agent 2 never
invents a model Agent 1 must later re-derive. They meet at the **deterministic substrate** (the
published corpus + verify/themes/resolve services), which is the shared contract.

---

## 2. The shared contract (where they meet)

Both agents treat these as immutable ground truth:

```text
data/published/ipvv/        the 49-passage lazy store (source + L2 + C1 + c1_source + immutable ids)
lib/verify.ts               the deterministic verification floor (quote/claim-structure/trace/counterevidence)
data/corpus/themes.ts       deterministic theme proposals
lib/citation.ts             the resolve/immutable-id kernel
data/corpus/graph.ts        the scholarly graph (annotations + evidence roles)
```

**Agent 1 consumes these; Agent 2 maintains them.** Neither edits the other's half without a
handoff note in `machinelearning/` or `docs/`.

---

## 3. The handoff protocol

- **Agent 2 → Agent 1:** "Exposed X" — when a structure becomes machine-queryable (e.g. "themes
  now have `/api/themes` + `get_themes` MCP; the substrate for theme-retrieval is live"). Agent 1
  then builds retrieval/eval over it.
- **Agent 1 → Agent 2:** "Needs X" — when a model needs data that isn't exposed (e.g. "vertical
  fidelity needs paired L2→C1→Guide examples; where are they?"). Agent 2 exposes/provides it.
- Both log to a `HANDOFF-LOG.md` (one entry per handoff: what, why, file, date).

---

## 4. Example parallel track (the next sprint)

```
Agent 1 (ML)                          Agent 2 (integration)
─────────────────────────             ─────────────────────────
· Formalize Benchmark v0              · Wire PARALLELS (cross-text witnesses) into C1s
  (from BENCHMARK_HANDOVER.md)        · Ingest L200 decisions as graph annotations
· Build Sanskrit tokenizer +          · Add /api/parallels + related-rail
  embedding index + BM25/dense        · Concept occurrence map (5-kind)
  baselines on PATALA-RETRIEVAL       · Wire more works (IPK/Vṛtti/IPV) into the store
· Run the THEMES four-arm experiment  · Reader: COMPARE view (L1 ∥ L2)
· Late-interaction (ColBERT)          · Essays grounded in themes + comparisons
```

Both run concurrently; the contract holds them aligned. When Agent 1 needs
"themes-with-evidence," Agent 2's `/api/themes` + curated edges are already there. When Agent 2
needs "which theme is this passage in," Agent 1's benchmark/retrieval gives it back.

---

## 5. What each agent must NOT do (the guardrails)

- **Agent 1 must not** edit `data/corpus/`, `app/`, `lib/` scholarly code, or re-derive the
  ontology; must not treat an experiment as production without a benchmark win + human review;
  must not claim morphological search until the tokenizer exists (search stays honestly substring).
- **Agent 2 must not** hand-build ML models, invent evaluation, or claim a model result; must not
  over-engineer the reader while the data/API isn't complete; must keep docs as source-of-truth.

---

## 6. The shared docs (both maintain, single source of truth)

- `machinelearning/MLUSEINPATALA.md` — the frozen ML strategy (Agent 1 owns; Agent 2 reads).
- `machinelearning/IPVV-STACK-INTEGRATION.md` — the verified stack audit (both read; Agent 2 updates
  on integration changes).
- `docs/PHASE1_IPVV_CORPUS_PROCESS_NOTES.md` — the corpus build (Agent 2 owns; Agent 1 reads).
- `machinelearning/BENCHMARK_HANDOVER.md` — the benchmark seed (Agent 1 owns; Agent 2 contributed).
- `HANDOFF-LOG.md` — the coordination record.

---

## 7. Why this is better than one agent

- **Context isolation:** Agent 1 holds arxiv/ML depth; Agent 2 holds the pāṭala file layout and the
  Sanskrit/scholarly register. Neither re-reads the other's domain.
- **No blocking:** while Agent 2 wires PARALLELS/COMPARE, Agent 1 builds the tokenizer/benchmark —
  the deterministic substrate decouples them.
- **Parallel throughput:** two independent workstreams on the same corpus, joined only by the
  shared contract + handoffs.
