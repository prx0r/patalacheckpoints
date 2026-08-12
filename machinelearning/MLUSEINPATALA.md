# ML USE IN PATALA — the canonical recommendation (FROZEN)

*2026-08-12. **Frozen.** This is the final word on how Pāṭala should use ML: **what to build, in what
order, and why**, grounded in (a) what the codebase already holds, (b) the verified 26-paper curriculum,
(c) the executed analogues FoJin and Bilara, and (d) expert review of an earlier draft (incorporated in
full). Companion docs in this folder supply the detail; this is the decision. **Before acting, read
`IPVV-STACK-INTEGRATION.md`** — the verified audit of the actual IPVV stack and the current Pāṭala wiring
(it confirms the exact C1-wiring gap that Phase 0A must close). **For the full vision this serves, see
`VISION-COMPUTABLE-TRADITION.md` + `PATALA_AS_LIBRARY_ENGINE.md`** — the latter scales the "one graph,
many register-projections" idea to the whole Library (Pāṭala as the engine every wing derives from).*

> **FROZEN. No new ML idea enters unless it answers:** *"Which benchmark task does it improve, and what
> existing baseline must it beat?"* — if there is no answer, it does not get built.

> **Retain the full vision while building the foundation:** the data foundation built now (the typed
> ArgumentProposal, the provenance 4-level contract, the register-aware C1/themes) is what makes the
> Library-engine vision possible. Build the spine (passage → claim → theme, resolvable + auditable)
> BEFORE the content projections, so every future wing derives from it.

---

## 0. The one sentence

> **Use ML to (1) expose Pāṭala's already-built scholarly structure as deterministic services, then
> (2) learn over that structure — but only after a fixed benchmark exists — and never let an ML output
> become established scholarship without human review.**

That is the entire strategy. Everything below is justification and sequencing.

---

## 0.1 PROGRESS (updated 2026-08-12) — the deterministic substrate is now built

The strategy is no longer theory for Phase 0 + Phase 2; it is shipped:

- **Phase 0A — C1 wired into the published objects.** `pipeline/attach_c1.py` attaches the 63 C1
  read/ renderings into the 49 published passage JSONs as `c1.verse_commentary[]` — the exact shape
  the reader's Commentary toggle renders. **V1 chunks bundle multiple sub-C1s** (17 passages have
  >1 C1; 72 total entries). `getPublishedTranslation()` serves /read + /api/resolve the same object.
- **Phase 0B — c1/source structured records completed.** `pipeline/gen_c1_source.py` mechanically
  derived the missing 53 (SUMMARY ≈ body, KEY TERMS, RELATED). Now 63 total (10 hand-authored + 53
  derived). Deterministic, no model call.
- **Phase 0C — deterministic THEMES exposed.** `data/corpus/themes.ts` + `/api/themes` +
  `get_themes` MCP tool — MACHINE_PROPOSED themes from shared technical lemmas across C1s.
- **Phase 2 — the deterministic verification floor (EXPOSE services) shipped.** `lib/verify.ts` +
  `/api/verify/{quote,claim-structure,trace-dependency,counterevidence}` + 4 MCP tools
  (`verify_quote`, `verify_claim_structure`, `trace_dependency`, `find_counterevidence`). All
  deterministic, over existing data, never silent-fallback.
- **Benchmark seed documented.** `machinelearning/BENCHMARK_HANDOVER.md` — the fixtures (gold.ts,
  qa_v1_gold 34, stall-log 60) the ML master builds Benchmark v0 from.

The IPVV is now a **machine-queryable corpus** (source + L2 + C1 + themes + verification floor),
so the INFER phases can operate over real data, not test fixtures.

---

## 1. The diagnosis (why this is the right posture)

Pāṭala's unusual asset is **not scale** — it is that the corpus has **multiple explicitly derived
epistemic layers over the same source**:

```
source → reading → decision → commentary → theme → claim → essay → pedagogy
```

This layered supervision is the ML gold, and — critically — **Pāṭala already holds most of it as
structured data** (`REVIEW_PATALAML_VS_CODEBASE.md`): n-ary `TranslationDecision` objects, first-class
assertions, a `contradicts` evidence role, `derived_from`/`version_of` provenance, term trajectories,
gold fixtures, and a resolve kernel.

**Consequence:** at least 10 of the 20 ideas in `PATALAML.md` are *not greenfield* — they are about
**exposing + learning over existing structure**, not building new foundations. The ML work splits into
two difficulty classes that must be planned separately:

| Class | Cost | Ship gating |
|---|---|---|
| **EXPOSE** — surface structure that already exists | cheap, deterministic, verifiable today | immediate |
| **INFER** — model a relation the data doesn't assert | expensive, uncertain | only after beating a baseline on a fixed benchmark |

This is exactly the FoJin lesson and the `PLATFORM_PROVENANCE_PRESERVING_GENERATION.md` principle:
**"AI proposes ≠ Pāṭala asserts."** The deterministic structural floor comes first; model judgment
operates only above it.

---

## 2. What to do, in order (the decision)

### Phase 0A — Finish corpus + C1 publication (no ML needed)

- Wire the 63 C1 read/ renderings into the reader's Commentary toggle (`c1.verse_commentary[]` — the
  content already exists in the IPVV stack; the reader is built).
- Complete the 53 missing `c1/source/` structured records (mechanical derivation from the read/ bodies).
- Ensure all passages + C1s are **machine-queryable** (the lazy store, `getPublishedTranslation`).

**Why:** the benchmark construction (Phase 1) needs the 63 C1s available. **You do NOT build the final
THEMES system here.**

### Phase 1 — Pāṭala Benchmark Suite v0 (the single most important ML decision)

**Start smaller but harder:** 50–100 high-quality, human-reviewed fixtures with **deliberately difficult
negatives** (e.g. positive `V2-A ↔ V2-O` shared continuity/recognition structure; hard negative: two
passages sharing *vimarśa* vocabulary but performing different doctrinal jobs). A smaller expert-checked
benchmark beats 300 weak labels. Grow it only after the first experiment.

**Separate evaluation sets by task** — a benchmark **suite**, not one giant benchmark, so a model cannot
improve aggregate score while getting worse at what you actually care about:

```
PATALA-RETRIEVAL     passage retrieval · term-sense retrieval · related-passage retrieval
PATALA-EVIDENCE      claim → support · claim → counterevidence · translation-crux retrieval
PATALA-FIDELITY      C1 → source · C1 → theme · theme → guide
PATALA-STRUCTURE     theme relationships · argument relations
```

**Leakage rules are fixed BEFORE any split** (critical — the same corpus generates all layers; if C1s
from the same argument sequence appear in both train and test, results look better than they are):

```
PASSAGE SPLIT            easy
CHUNK SPLIT              better
VIMARŚA/ARGUMENT-FAMILY  harder
WORK-LEVEL HELD OUT      best test of transfer
```

**Why first:** every future model needs something to beat. Without it you can build embeddings *worse*
than `BM25 + metadata + dense`. The seed exists (`gold.ts` + the QA toolchain) — formalize it.

### Phase 0B / 2 — Run the THEMES pilot against the benchmark

Only after the benchmark exists: run the THEMES mechanism (the piloted hybrid graph) **against the
human-reviewed relational fixtures**. The benchmark contains human-reviewed theme/relation fixtures that
exist **before the production theme algorithm sees them** — protecting the experimental design from
self-contamination (otherwise your own machine-generated themes become the thing that defines "correct"
theme relationships).

### Phase 2A — The deterministic EXPOSE services (thin, high-value, ship now)

```
/verify-quote              (primary-text / translation quote verifier)
/verify-claim-structure    (evidence resolves · source exists · citation valid · review state)
/trace-dependency-structure(the DAG already exists; walk it backward)
/find-counterevidence      (the explicit contradicts/qualifies edges — CURATED)
/resolve                  (already exists — extend)
```

**Why:** these implement the verification floor as machine access, over data that already exists. They
are cheap and immediately trustworthy because they return explicit edges, not model judgment.

### Phase 3 — Retrieval baselines (then late interaction)

- Real embedding index + a Sanskrit-aware tokenizer (the E0.5 prerequisite — Pāṭala's current
  `search_surface_occurrences` is substring-only, `lemmatized: false`).
- Benchmark `BM25` vs `dense` vs `hybrid` on `PATALA-RETRIEVAL`.
- Then ColBERT-style **late interaction** (multi-vector per token) — attractive for Sanskrit technical
  terms where the exact lexical distinction matters.

### Phase 4 — The flagship experiment (the only INFER project that matters first)

> **Can structured scholarly relations improve intellectual-theme discovery + retrieval beyond text
> embeddings alone?**

Four arms, one fixed evaluation on `PATALA-STRUCTURE` + `PATALA-RETRIEVAL`:
```
TEXT (C1 embeddings)  vs  STRUCTURE (terms+relations+sequence+roles)
vs  HYBRID  vs  LEARNED (graph representation learning)
```
Tasks: recover known relationships · discover human-approved novel ones · retrieve supporting passages ·
retrieve contrasting passages.

**EXPERIMENT vs PRODUCTION — the key distinction:** running the LEARNED arm is **always allowed** if the
research question is meaningful, even if you expect it to lose. But **production adoption** requires a
benchmark win + acceptable cost + interpretability. The experiment is legitimate either way; the adoption
is gated.

### Phase 5 — Semantic verification (after the layers + benchmark exist)

- `verify-claim-semantic` (entailment, scope, polarity, attribution) — modeled on RAGChecker / MedRAGChecker.
- `discover-counterevidence` (the frontier adversarial retrieval) — modeled on SUCEA.
- **Vertical Fidelity** — see §5; this is likely Pāṭala's most novel benchmark and should be pushed
  hardest. Built from paired transformation datasets with deliberately corrupted variants labeled by
  error type.

### Phase 6 — Advanced graph ML (frontier, later)

Argument motifs · hyperbolic representations · cross-tradition relation prediction · counterfactual
dependency analysis. Run as experiments; production adoption requires the benchmark-win + cost +
interpretability bar. Do not implement hyperbolic tomorrow.

---

## 3. The sequencing table (with justification)

| # | Build | Why | ML? |
|---|---|---|---|
| **0A** | Finish corpus + C1 publication (wire 63 C1s into reader, complete 53 `c1/source/`) | the substrate; benchmark needs the C1s available | No — **DONE (2026-08-12)** |
| **1** | Pāṭala Benchmark **Suite** v0 (50–100 hard fixtures; task-specific sets; leakage rules) | evaluation substrate before any model; protects the experimental design | Eval — seed documented (BENCHMARK_HANDOVER) |
| **0B** | Run the THEMES pilot **against the benchmark** (NOT before it) | prevents machine-generated themes from contaminating the gold | No |
| **2A** | EXPOSE services (verify-quote/claim-structure, trace-dependency-structure, curated counterevidence) | verification floor as machine access; cheap; over existing data | No — **DONE (2026-08-12)** |
| **3** | Embedding index + Sanskrit tokenizer; BM25/dense/hybrid baselines | real retrieval to beat | Yes (baselines) |
| **4** | Late interaction (ColBERT-style) | benchmark against baselines on PATALA-RETRIEVAL | Yes (INFER) |
| **5** | THEMES experiment (text/struct/hybrid/learned) | the flagship research question on PATALA-STRUCTURE | Yes (INFER) |
| **6** | Graph learning | experiment always allowed; **adoption** needs benchmark win + cost + interpretability | Yes (INFER) |
| **7** | Semantic verification (entailment, counterevidence discovery, Vertical Fidelity) | after layers + benchmark exist | Yes (INFER) |
| **8** | Advanced graph ML (motifs, hyperbolic, cross-tradition, counterfactual) | frontier | Yes (INFER) |
| **9** | Minimal evidence (sufficient-subset) | once claim-support scoring is trustworthy | Yes (INFER) |

**Every INFER stage runs the same discipline:**
```
BASELINE → FIXED HELD-OUT TEST → EXPERIMENT → ERROR ANALYSIS → HUMAN REVIEW → ADOPT / REJECT
```

---

## 4. Non-negotiable rules

1. **Benchmark before model.** No INFER model is adopted until it beats a baseline on the fixed
   held-out Pāṭala benchmark — never on visual examples.
2. **Fixed test set decided before development.** No adjusting gold after seeing results unless the
   change is versioned and the original result stays recorded.
3. **Expose before infer.** Ship the deterministic services before any learned model.
4. **Every INFER result is a hypothesis until human review.** "AI proposes ≠ Pāṭala asserts."
5. **Do not adopt a hypergraph/hypergraph-DB engine** merely because the ontology is n-ary JSON.
   "Ontology first, representations interchangeable." The data is the asset; Neo4j/PyG/etc. are
   execution details.
6. **Do not build a general AI Q&A or translation factory.** The moat is verified scholarly structure,
   not LLM plumbing (FoJin is a reader+answer engine; Pāṭala's moat is the verified graph).
7. **Adopt FoJin's discipline:** a `served_trustworthy_rate`-style metric + deterministic guards as a
   regression gate; LLM-verify + human-review promotion (never auto-accept); margin-based candidate
   routing to cut LLM cost.
8. **Adopt Bilara's discipline:** immutable segment IDs + cognate layers + unpublished/published branch
   model + integrity tests as a per-PR CI gate.
9. **Statistical rigor.** "Model A scored higher" is not enough. Every experiment records, per metric:
   `mean · bootstrap CI · delta vs baseline · significance (paired test) · error categories`.
   Especially at 50–300 examples, variance matters. Metrics: retrieval → Recall@5/MRR@10/nDCG@10;
   classification → precision/recall/F1/calibration; human-adjudicated theme discovery → acceptance
   rate/edit burden/novel-theme yield/false-affinity rate.
10. **Leakage-safe splits.** The same corpus generates all layers; enforce the split policy
    (passage → chunk → vimarśa/argument-family → work-held-out) **before** any training, and prefer the
    harder splits. The serious transfer result is *train on IPVV, test on a different work*.
11. **EXPERIMENT ≠ PRODUCTION.** A research experiment is legitimate if the question is meaningful even
    when it is expected to lose. Production adoption requires a benchmark win + acceptable cost +
    interpretability.
12. **Reproducibility.** Every experiment persists: dataset version · split manifest · model version ·
    embedding model · random seed · hyperparameters · git commit · hardware · runtime · metrics ·
    predictions · errors — in `experiments/<id>/` (config.yaml, predictions.jsonl, metrics.json,
    errors.md, decision.md).
13. **Human review is itself measured.** For theme/claim adjudication record reviewer · decision · time ·
    confidence · disagreement · outcome; accumulate **inter-rater agreement**. "Expert gold" must not be
    an opaque label source, especially if the benchmark becomes publishable.

---

## 5. What ML is genuinely new here (the research asset worth protecting)

The frontier target Pāṭala is uniquely positioned to support:

> **Structured Scholarly Supervision for Provenance-Preserving Reasoning over Premodern Texts**

with experiments showing:
```
text embeddings  <  structured scholarly graph  <  text+graph  <  higher-order provenance representation
```
on passage retrieval, thematic discovery, claim support, counterevidence, and cross-layer fidelity.

The novelty is **the supervision structure produced by critical scholarship itself** — the
source → reading → decision → commentary → theme → claim → pedagogy ladder. That is the dataset/modeling
opportunity worth protecting, not "we applied GraphRAG to Sanskrit."

### The most novel artifact: the Vertical Fidelity Benchmark

Pāṭala uniquely has the full transformation chain (`source → L2 → C1 → Theme → Guide`), giving **controlled
positive pairs**. Add adversarial corruptions labeled by error type:

```
NEGATION_LOSS         "does not establish X" → "establishes X"
SCOPE_STRENGTHENING   "some contexts"        → "always"
CERTAINTY_INFLATION   "may suggest"          → "proves"
ATTRIBUTION_ERROR     "our interpretation"   → "Abhinavagupta says"
BOUNDARY_ERASURE      "not established locally" → omitted
AGENT_SWAP            A acts on B            → B acts on A
```

> **Name:** *Vertical Fidelity Benchmark for Multi-Resolution Scholarly Explanation.*

This is the dataset most likely to be valuable **outside Sanskrit studies** — a general test of "does
simplification preserve meaning across explanation depths." Push it hardest.

### The coherent research program (not "which embedding is best?")

```
Can explicit scholarly structure improve retrieval?
Can models discover relationships experts accept without erasing disagreement?
Can we detect when interpretation outruns source support?
Can we preserve semantic content while moving from critical scholarship to beginner explanation?
Can provenance improve reasoning reliability?
```

Pāṭala is not trying to make AI "understand Sanskrit better" in the abstract. It is creating a corpus
where **scholarly reasoning itself becomes supervised data**.

---

## 6. The immediate three actions (this week)

1. **Phase 0A**: wire the 63 C1s into the reader (`c1.verse_commentary[]`) + complete the 53
   `c1/source/` records. — **DONE (2026-08-12)**: 49 passages carry `verse_commentary[]` (V1
   multi-C1), 63 `c1/source/` records complete.
2. **Phase 1**: stand up Pāṭala Benchmark Suite v0 (50–100 hard fixtures across
   PATALA-RETRIEVAL/EVIDENCE/FIDELITY/STRUCTURE, leakage-safe splits fixed first). — seed documented
   (`BENCHMARK_HANDOVER.md`); the ML master formalizes it.
3. **Phase 2A**: ship `/verify-quote`, `/verify-claim-structure`, `/trace-dependency-structure`,
   `/find-counterevidence` (curated). — **DONE (2026-08-12)**: all four live + MCP tools.

Then run the THEMES pilot against the benchmark (0B), then the retrieval baselines (3).

---

## 7. Bottom line

Pāṭala should **not** chase frontier ML first. It should finish exposing the scholarship it already has,
build the benchmark **suite** that makes every future claim empirical (before any production theme
algorithm sees it), ship the deterministic verification services that operationalize "AI proposes ≠
Pāṭala asserts," and only then run **narrow, well-posed experiments** gated on a benchmark and a fixed
held-out test — with statistical rigor, leakage-safe splits, reproducible results, and measurable human
review. The layered supervision is the asset; the benchmark, the verification floor, and the experimental
discipline are what protect it. The most novel thing Pāṭala could produce is the **Vertical Fidelity
Benchmark for Multi-Resolution Scholarly Explanation** — a contribution that would matter beyond Sanskrit
studies.
