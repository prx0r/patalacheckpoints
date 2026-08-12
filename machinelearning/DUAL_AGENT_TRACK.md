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

> **Schema-version pin (recommended).** "Immutable" drifts — Agent 2 will evolve the store (PARALLELS,
> L200-as-annotations). Add `data/published/ipvv/version.json` (a monotone integer bumped on any shape
> change). Agent 1's `corpus.py` records the version it snapshotted, so a stale eval is detectable. If
> the shape changes, Agent 2 bumps the version and handoff-notifies; Agent 1 re-snapshots before trusting
> results.

---

## 3. The handoff protocol

- **Agent 2 → Agent 1:** "Exposed X" — when a structure becomes machine-queryable (e.g. "themes
  now have `/api/themes` + `get_themes` MCP; the substrate for theme-retrieval is live"). Agent 1
  then builds retrieval/eval over it.
- **Agent 1 → Agent 2:** "Needs X" — when a model needs data that isn't exposed (e.g. "vertical
  fidelity needs paired L2→C1→Guide examples; where are they?"). Agent 2 exposes/provides it.
- Both log to a `HANDOFF-LOG.md` (one entry per handoff: what, why, file, date).

> **Schema handshake (recommended).** A prose handoff ("themes-with-evidence") is ambiguous for Agent 1's
> code. Every handoff that carries data should include a **minimal JSON schema snippet** of the exposed
> shape (field names + types), so Agent 1 can write a loader/test against it without guessing. A 5-line
> schema beats a paragraph of prose.

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

---

## 8. AGENT 1 — the ML lane, in depth (the working method)

*The personal, field-tested guidance for the ML/research agent. This is *how* to do the work well —
the discipline that turns "try a model" into a defensible research program.*

### 8.1 The mental model

Your job is **not** to find the fanciest model. It is to maintain an honest, falsifiable ledger of
"does X beat Y on the fixed task, and is that difference real?" The frozen rule is your whole identity:
**no INFER model is adopted until it beats a baseline on a fixed held-out set.** Everything else is
housekeeping.

Every experiment answers three questions:
1. What task, exactly? (which suite: RETRIEVAL / EVIDENCE / FIDELITY / STRUCTURE)
2. What baseline must it beat? (BM25 first, always)
3. Is the difference real? (CI + paired test, not vibes)

### 8.2 The order of operations (never reorder)

```
1. BASELINE        BM25 over the honest task. Get a number with a CI. This is the floor.
2. FIXED SPLIT     decide the leakage policy (passage→chunk→vimarśa→work) BEFORE any training.
3. ONE ARM         the cheapest meaningful model vs the baseline. Publish the delta + p.
4. ERROR ANALYSIS  look at WHERE it fails. This drives the next arm — not fashion.
5. HUMAN REVIEW    an editor checks a sample. Record acceptance.
6. ADOPT / REJECT  only here does a model become "the thing."
```

**The single most common failure** (I hit it on E1): a *leaky task* that makes the baseline score 1.0.
Always sanity-check that the query isn't a substring of the document, and that a trivial method doesn't
score ~perfect. If BM25 gets 1.0, your task is broken, not your model.

### 8.3 Build the baseline before the benchmark is "done"

Don't wait for a perfect 100-fixture benchmark. The moment you have ~30 honest fixtures, run BM25 and
get a number. A baseline that exists is more useful than a benchmark that's being polished. The
benchmark grows; the baseline is the anchor.

### 8.4 The tokenizer is a trap — be honest about it

Sanskrit inflection/sandhi means a naive whitespace tokenizer under-segments (`vimarśa` vs
`vimarśo` vs `vimarśam`). Options, in order of honesty:
- (a) **substring surface match** — honest, but weak. This is what the app does now (`lemmatized:false`).
- (b) **a small Sanskrit stemmer / morphological pass** — better, but a research task itself.
- (c) **sentence-level embeddings** that tolerate inflection — what dense retrieval does, and why
  dense may beat BM25 on *retrieval* even though it lost on *fidelity*.

**Rule:** never claim "morphological search" until (b) exists. State exactly which of (a)/(b)/(c) your
tokenizer is. The `match_method` honesty in the app is the precedent — keep it.

### 8.5 Density vs structure — the actual research question

My first result (BM25 ≥ dense on fidelity) is a *hint*, not a law. The interesting question is:
does dense beat BM25 when the task is **retrieval** (query from a *different* wording than the doc),
and does **structure** (see_also, key terms, relations) add signal on top of BOTH? That's the four-arm
test. Do not conclude "dense is useless" from one task; do not conclude "dense is king" from one task
either.

### 8.6 Statistical discipline (non-negotiable)

- Always paired: same query/claim/seed across arms.
- Report mean + bootstrap CI + delta + paired p. Never just "model A scored higher."
- At 30–100 items, variance is huge. A p>0.05 delta is **"no evidence of a difference"**, not a win.
- Save everything to `experiments/<id>/`: config, split manifest, seed, metrics, predictions, errors.

### 8.7 Leakage is the silent killer

The same corpus produces every layer (source→L2→C1→theme). If C1s from the same argument-family
appear in both train and test, your "improvement" is an artifact. Prefer the **hard splits**
(vimarśa/argument-family, and ultimately work-held-out). The transfer result — train IPVV, test a
held-out work — is the result that actually matters and is worth designing toward from the start.

### 8.8 Human review is data, not ceremony

Record per adjudication: reviewer · decision · confidence · time · disagreement. Build inter-rater
agreement. "Expert gold" that is unmeasured is just another opaque label source — and if the benchmark
is ever published, unmeasured gold is a liability.

### 8.9 What "done" looks like (definition of done for an experiment)

```
[ ] baseline number + CI recorded
[ ] task files + split manifest committed (reproducible)
[ ] delta + paired p vs baseline recorded
[ ] error analysis written (where it fails, why)
[ ] human review of a sample logged
[ ] decision recorded: ADOPT / REJECT / MORE-EVIDENCE
[ ] ADR written (machinelearning/decisions/)
[ ] handoff-logged if it needs Agent 2 (data/schema) or informs Agent 2
```

### 8.10 Your guardrails (repeat of §5, plus)

- **Never** edit `data/corpus/`, `app/`, `lib/` — that is Agent 2's ontology. Read the store; don't
  write it.
- **Never** claim a production capability from one experiment.
- **Never** re-derive what Agent 2 owns (C1 wiring, themes-as-exposed).
- **Always** consume the substrate through the shared contract; if the shape is missing, handoff-request
  it from Agent 2 with an exact schema snippet.

### 8.11 The current concrete queue (Agent 1, in order)

1. Create `HANDOFF-LOG.md`; log the E1-fidelity result (BM25 ≥ dense; needs Agent 2's structured edges
   for the flagship test).
2. **Sanskrit-aware tokenizer** (honest — pick a/(b)/(c), label it).
3. **Formalize Benchmark v0** from `BENCHMARK_HANDOVER.md` (gold.ts + qa_v1_gold 34 + stall-log 60) into
   the schema'd task files + leakage-safe split policy.
4. **Full retrieval baselines** on PATALA-RETRIEVAL (not just fidelity): BM25 / dense / hybrid, with CIs.
5. **The THEMES four-arm experiment** — text vs structure vs hybrid vs learned — handoff-requesting
   Agent 2 for themes-with-evidence (exact schema) first.
6. **Late-interaction (ColBERT-style)** — only after the baselines are on the board.

Steps 2–4 are independent of Agent 2 and buildable now. Step 5 is the first real *interdependency*
and the point where the handoff protocol earns its keep.

---

## 9. AGENT 2 — the integrator lane, in depth (how it serves the ML work + Pāṭala)

*Written from Agent 1's perspective: what the ML/research lane needs the integrator to expose, in what
shape, and why — so the two lanes compound rather than overlap. Agent 2 is the scholarly spine; the
discipline below is what makes its output *machine-learnable*, not just presentable.*

### 9.1 The mental model

You own the ontology, the corpus, and the reader. Your job is **not** to build the model — it is to make
the scholarship **machine-learnable**: every scholarly judgment you encode becomes supervision data the
ML lane can learn over. "AI proposes ≠ Pāṭala asserts" is your rule; the ML lane depends on your
assertions being *structured and addressable*, not just written.

The test for everything you build: **"Could an ML system retrieve, cluster, or verify over this?"** If
not, it is prose for a human; if yes, it is supervision for the whole project.

### 9.2 What I (Agent 1) actually need from you, in priority order

These are the structures that unblock real ML results. Expose them **as addressable data**, with the
schema-handshake note (a JSON snippet per handoff).

1. **Themes-with-evidence.** `/api/themes` exists (deterministic, shared-lemma). For the flagship
   four-arm experiment I need each theme's **member C1 ids + the edge reason** (which shared lemma /
   see_also justified the membership). Without the edges, I can't separate "structure helped" from
   "themes are just topic clusters."
   ```json
   { "theme_id": "...", "label": "memory-recognition",
     "members": [{ "c1_id": "...", "strength": 0.9, "role": "ESTABLISHES" }],
     "edges": [{ "a": "...", "b": "...", "type": "see_also|shared_term|sequence" }] }
   ```

2. **The PARALLELS / relation edges, typed.** When you wire PARALLELS, make the relation **typed and
   directional** (`supports | qualifies | contradicts`), because:
   - `contradicts` is the *counterevidence* seed (the `/discover-counterevidence` task, and my
     PATALA-EVIDENCE fixtures).
   - `supports`/`qualifies` are the *retrieval* gold for related-passage retrieval.
   A flat "related to" list is nearly useless for the ML lane; a typed one is the backbone of two tasks.

3. **L200 decisions as graph annotations.** When you ingest L200 into the graph, keep the
   `MT vs IA` split (translation decision vs interpretive assertion). For me, IAs are *claim-support*
   supervision and MTs are *translation-crux* retrieval. If you collapse them, I lose two tasks.

4. **A stable schema-version pin** on the store (`data/published/ipvv/version.json`), bumped on any
   shape change. My `corpus.py` snapshots the version; when it drifts, I re-snapshot before trusting a
   result. This is the single cheapest thing you can do to protect my results' validity.

### 9.3 The most valuable single thing: make the C1s *pair-ready*

The frozen strategy's most novel artifact is the **Vertical Fidelity Benchmark** (L2→C1→Theme→Guide).
That needs **paired** examples, and only you can produce the pairs with scholarly fidelity. The single
highest-leverage thing you can expose for the ML lane is a **paired dataset**: for a set of passages,
the aligned `{L2 passage, C1, theme, guide/plain rendering}`. With 30–50 such pairs (plus the corruption
set), I can build the cross-domain benchmark that makes Pāṭala matter beyond Sanskrit. That is a bigger
ML win than any tokenizer I build.

### 9.4 The "expose, don't polish" principle

Prioritize **making what exists queryable** over **building new reader features**. A COMPARE view that
reads L1 ∥ L2 is nice; an `/api/parallels` that exposes typed edges is *load-bearing* for two ML tasks.
When you're deciding where to spend effort, ask: does this feed the graph, or just the page? Feed the
graph first — the page can always render it later.

### 9.5 The guardrails, restated for your lane

- **Don't** hand-build models or claim a result — that's mine, and an un-benchmarked claim poisons the
  project's credibility.
- **Don't** over-engineer the reader while the data/API isn't complete — the reader is a *renderer* of
  the graph; make the graph complete.
- **Do** keep the scholarly standard (L200/C1 discipline) — it is the *reason* the supervision data is
  trustworthy. A sloppy IA mislabeled as an MT corrupts the training signal.
- **Do** log every data exposure as a handoff with a schema snippet, and bump the version pin.
- **Do** preserve the originals (`l200_legacy/`, `c1/_essay-material-legacy/`) — provenance is the whole
  point.

### 9.6 What "done" looks like for a handoff to the ML lane

```
[ ] the structure is exposed as addressable data (API or store)
[ ] a JSON schema snippet is in the handoff log
[ ] the version pin is bumped if the shape changed
[ ] the provenance is preserved (nothing overwritten)
[ ] a test covers the exposed shape (so Agent 1's loader can trust it)
[ ] noted what ML task it unlocks (retrieval / evidence / fidelity / structure)
```

### 9.7 The concrete queue (Agent 2, in the order that most helps Pāṭala + the ML lane)

1. Add the **schema-version pin** to the store (cheap, protects all ML results).
2. Expose **themes-with-evidence** (members + edge reasons) — unblocks my flagship experiment.
3. Wire **typed PARALLELS** (`supports/qualifies/contradicts`) as addressable data — unblocks
   related-passage retrieval + counterevidence.
4. **Ingest L200 as graph annotations**, keeping the MT/IA split — unblocks claim-support + crux retrieval.
5. Produce the **paired L2→C1→Theme→Guide** set — the Vertical Fidelity substrate (the biggest ML win).
6. Wire more works (IPK/Vṛtti/IPV) into the store — the transfer-eval substrate.
7. Reader features (COMPARE view, concept maps) — **last**, once the graph is complete.

Items 1–2 are the immediate unblock; 5 is the highest long-term value; 7 is polish.

---

## 10. How the two lanes compound (the whole is the point)

Agent 1 and Agent 2 are not two agents doing separate things — they are **two ends of one loop**:

```
Agent 2 (scholarly spine)        Agent 1 (ML lane)
exposes structure                learns over it
  → themes, parallels, L200, C1     → retrieval, discovery, verification, fidelity
  ↑                                    ↓
  promoted structure                 benchmark + human-review gating
  (what ML "discovered" that         (proves a model beats a baseline
   the editor accepts becomes        before it is trusted)
   new explicit scholarship)
```

- Agent 2's *assertions* are the **supervision**; Agent 1's *benchmark* is the **check**.
- Agent 2 grows the graph; Agent 1 proves what in it is *learnable and reliable*.
- The shared contract (deterministic substrate) + schema handshakes + version pins keep them aligned
  without either holding the other's context.

The project only becomes "a computable scholarly tradition" (the vision) when BOTH loops run: the
scholarship is structured (Agent 2) AND the structure is verified to be learnable (Agent 1). Either
alone is just a corpus or just a model zoo.
