# Pāṭala — ML Review (mlreview.md)

*2026-08-12. A review of Pāṭala's ML roadmap (`PATALAML.md`, `REVIEW_PATALAML_VS_CODEBASE.md`, `GAPS.md`)
from an ML-engineering perspective, updated against two of the strongest existing analogues — **FoJin**
(xr843/fojin) and **Bilara / SuttaCentral** (suttacentral/bilara-data) — and the current literature
(GraphRAG arXiv:2404.16130, ColBERTv2 arXiv:2112.01488, RAPTOR arXiv:2401.18059).*

> **READ THIS TOO:** `mlcurriculum.md` — the *verified* 26-paper reading curriculum (every arXiv ID
> fetched and confirmed) with the required deliverables: per-paper technical notes (`ml/papers/`),
> proof notes (`ml/proofs/`), and implementation decision records (`ml/decisions/`). Templates live in
> each directory. This review gives the *what and why*; the curriculum gives the *how to learn it
> rigorously*.

> **The one-line verdict:** Pāṭala already holds the ontology for most of the ML ideas; the real work is
> **exposing explicit scholarly structure** (cheap, deterministic) vs **inferring new scholarly
> structure** (expensive, model-based). Those are two different difficulty classes and must be planned
> separately. The correct sequence is **benchmark-first, then deterministic services, then retrieval
> baselines, then one narrowly-scoped learned model.**

---

## 0. The two difficulty classes (the organizing frame)

Everything in the ML roadmap falls into one of two classes. Do not blur them.

| Class | Meaning | Cost | Examples |
|---|---|---|---|
| **EXPOSE** | surface scholarly structure that already exists in the data | cheap, deterministic, verifiable | `/find-counterevidence` over tagged `contradicts` edges; `/verify-claim-structure`; `/trace-dependency-structure`; multi-resolution retrieval over the existing ladder |
| **INFER** | model a new relation the data does not already assert | expensive, uncertain, needs evaluation | `discover-counterevidence` (NLI/relation over candidates); claim entailment; graph/hypergraph embeddings; vertical-fidelity classifier; relation-motif discovery |

**The governance rule:** an EXPOSE service is trustworthy on day one (it returns explicit edges).
An INFER service is a hypothesis until it beats a baseline on a benchmark. Never let an INFER result
be presented as established structure without passing through human review — this is the exact
"AI proposes ≠ Pāṭala asserts" principle, and it is also the standard the two analogue systems enforce.

---

## 1. The strongest change: **build the benchmark before the fancy ML**

The previous review put the benchmark last. **Reverse it.**

Before ColBERT, GNNs, hyperbolic embeddings, or entailment models, build **Pāṭala Benchmark v0** —
not a giant suite, ~100–300 expert/editor-checked examples:

```
passage retrieval            term-sense retrieval
related-passage retrieval    claim → support
claim → counterevidence      C1 → source fidelity
theme relationship           translation-crux retrieval
```

**Why it must come first:** every future model needs something to beat. Without it, you can spend
days building a graph model that produces beautiful embeddings while being *worse* than:

```
BM25 + good metadata filters + dense embeddings
```

The evaluation substrate is the thing that keeps the ML empirical from day one and stops "frontier
ML" from becoming novelty-chasing. Pāṭala already has the *seed* (`data/corpus/gold.ts`, the v0/v1/v2
QA toolchain, the stall log) — formalize it, don't grow a new one from nothing.

---

## 2. `/find-counterevidence` has **two** very different meanings

Calling this "a thin service because `contradicts` exists" is true for only one reading:

**CURATED counterevidence** (EXPOSE — build now):
```
GET /find-counterevidence?claim=x
→ the explicitly-tagged contradicts / qualifies edges
```
Trivial, deterministic, returns existing structure.

**DISCOVER counterevidence** (INFER — the genuinely interesting ML):
```
POST /discover-counterevidence
→ retrieve candidate passages
→ NLI / relation model
→ graph context
→ ranked adversarial evidence
```
This answers *"search the corpus for the strongest passage that would weaken this claim"* — the
frontier version. It is potentially one of the coolest parts of Pāṭala and is a real research
problem. Do not collapse the two.

---

## 3. `/verify-claim` is also not necessarily thin

If claims are first-class assertions, then *"does CLAIM-123 have valid evidence IDs?"* is trivial.
But *"does the cited evidence actually support the natural-language claim?"* is **not**.

Split it, mirroring the whole Pāṭala philosophy (deterministic structural floor + semantic judgment):

```
/verify-claim-structure      DETERMINISTIC  — evidence resolves, source exists,
                             citation valid, review state valid     (EXPOSE, build now)

/verify-claim-semantic       MODEL-BASED    — entailment, scope, polarity,
                             attribution, inference strength          (INFER, later)
```

Do the same for `trace-dependency`: a structural trace (the DAG already exists) is cheap;
determining whether an essay claim *really depends semantically* on a theme assertion is hard.

---

## 4. Minimal evidence is not automatically a thin service

Placing `/minimal-evidence` beside cheap exposure APIs is wrong. If it means "drop obviously
duplicate evidence IDs," fine. But the interesting version asks:

> **What smallest subset of evidence is sufficient to support the claim?**

That needs a support function: for evidence set `{A B C D E}`, is `{A + C}` sufficient while neither
`A` nor `C` alone is? That is search/optimization over semantic entailment — an INFER problem. **Keep
it later**, after claim-support scoring is trustworthy.

---

## 5. The execution order (revised)

```text
 0. FULL IPVV LIVE            finish the corpus publication first (C1 wiring + themes)
 1. PĀṬALA BENCHMARK v0       the evaluation substrate — before any model
 2. DETERMINISTIC SERVICES    resolve · verify_quote · verify_claim_structure
                              · trace_dependency_structure · curated_counterevidence
 3. RETRIEVAL BASELINES       BM25 · dense · hybrid lexical+dense
 4. LATE INTERACTION          benchmark ColBERT-style retrieval vs the baselines
 5. THEMES EXPERIMENT         semantic-only / structured-only / hybrid graph
                              → compare against benchmark + human review
 6. GRAPH LEARNING            only if a learned representation beats the hand-weighted hybrid graph
 7. SEMANTIC VERIFICATION     claim entailment · counterevidence discovery · vertical fidelity
 8. ADVANCED GRAPH ML         argument motifs · hyperbolic space
                              · cross-tradition relation prediction · counterfactual dependency
 9. MINIMAL EVIDENCE          once claim-support scoring is trustworthy
```

---

## 6. The flagship ML project — make it narrow

Don't call the flagship "GNN over C1s." Make it the clean research question:

> **Can structured scholarly relations improve intellectual-theme discovery and retrieval beyond text
> embeddings alone?**

Experiment (four arms, one fixed evaluation):

```
TEXT      C1 embeddings
STRUCTURE terms + relations + sequence + argument roles
HYBRID    text + structure (weighted)
LEARNED   graph representation learning over the C1 graph
```

Tasks:
```
recover expert-known relationships     (recall vs benchmark gold)
discover human-approved novel relationships
retrieve supporting passages
retrieve contrasting passages
```

If the learned graph **loses** to the hand-weighted hybrid graph, that is a useful, publishable
negative result (the pilot already suggests hand-weighted hybrid is strong). If it wins, you have a
real result. Either way it is empirical — and it directly tests the pilot's central claim.

---

## 7. Pāṭala's unusually valuable supervision signal: **paired transformation datasets**

The layered ladder (source · decision · commentary · theme · claim · essay · pedagogy) is the ML
gold. Explicitly generate **paired transformation datasets** so each transformation can be studied
separately:

```
L2 → C1           local explanation        (philological rendering)
C1 × C1 → THEME   synthesis
THEME → GUIDE     simplification
L200 → L2         decision → readable rendering
CLAIM → EVIDENCE  support relation
```

The **`C1 → GUIDE`** pair is the most promising. It gives positive examples of correct simplification;
deliberately corrupted variants give negative examples labeled by error type:

```
scope strengthening · certainty inflation · lost negation
lost boundary · false attribution
```

That becomes the **Vertical Fidelity dataset** (the semantic-conservation test of
`PLATFORM_PROVENANCE_PRESERVING_GENERATION.md` §7). Done well, this could be a genuinely interesting
benchmark **outside Sanskrit studies** — a general test of "does simplification preserve meaning?"

---

## 8. What FoJin teaches us (the executed analogue)

FoJin is the nearest thing to Pāṭala's Northstar already running, and it validates the core bets:

- **Deterministic verification is the differentiator.** FoJin's three guards — citation whitelist,
  verbatim-quote downgrade, per-answer trust state — took its served-trustworthy rate from ~11% raw
  to ~98% served. This is precisely Pāṭala's "AI proposes ≠ Pāṭala asserts" and it is *measurable*.
  Pāṭala should adopt the same **`served_trustworthy_rate`** style metric as a regression gate.
- **LLM-verify + human-review promotion** (not auto-accept) is how FoJin builds trusted alignments:
  candidate mining → LLM `{is_parallel, confidence, reason}` → human review gates → ground truth,
  then a **flywheel** expands outward from verified pairs. This is exactly the right pattern for
  Pāṭala's PARALLELS layer and for theme acceptance (MACHINE_PROPOSED → EDITOR_REVIEWED → ACCEPTED).
- **Margin-based candidate routing** (auto-accept / LLM-verify / auto-reject bands) cuts LLM cost
  while preserving a precision guarantee. Pāṭala should adopt this for any LLM-in-the-loop discovery.
- **A stable URN + MCP server** makes the corpus callable. Pāṭala already has `pt:`/`tantra:text:`
  URNs + `resolve_ref` — the right direction; extend it.
- **An eval harness as a regression gate** for every pipeline (RAG, alignment) — Pāṭala should gate
  its THEMES and retrieval work the same way.

### FoJin-specific cautions (what NOT to copy)

- FoJin is a *reader + answer engine*; Pāṭala's moat is *verified scholarly structure*. Do not build
  a general AI Q&A before the scholarly core is credible (NORTHSTAR's own warning).
- FoJin's parallel-alignment corpus (cross-canon chunks) is analogous to Pāṭala's PARALLELS — but
  Pāṭala's are *evidence-typed* (supports/qualifies/contradicts), which is stronger. Keep the typing.

---

## 9. What Bilara-data teaches us (the data-integrity analogue)

Bilara is the cleanest pattern for Pāṭala's publication model, and Pāṭala already mirrors much of it:

- **Immutable segment IDs** as the primary key, with cognate files (`root/translation/en/comment/
  variant/html`) keyed by the same ID. Pāṭala's `PublishedTranslation` (source_spans / target_spans /
  alignments / decisions / evidence / c1) is the same idea — one passage, many cognate layers.
- **Branch-based publication** (`unpublished` = develop, `published` = stable) with a JSON publication
  record per project (`_publication.json`). Pāṭala's `published.ts` + review states map cleanly onto
  this; adopting the *unpublished/published* branch discipline would formalize the editorial loop.
- **Version-controlled, Git-based change history** for every translation — the audit trail IS the
  data model. Pāṭala's `version_id` + `review_events` already do this; the improvement is making the
  whole corpus a Git-tracked dataset like Bilara so diffs/PRs are the review workflow.
- **Integrity tests as a CI gate** on merge (`bilara-data-integrity` + `sutta-processor` run per-file
  on every PR). Pāṭala should make its `l200_validate.py` + the scholarly invariants a per-PR gate.

### Bilara-specific cautions

- Bilara is **translation production infrastructure**, not an evidence graph. Pāṭala's differentiator
  (evidence roles, review provenance, term trajectories, themes) is strictly more than Bilara. Do not
  flatten Pāṭala into a translation repo; use Bilara's *integrity discipline*, not its *scope*.
- Bilara keys are string-based and hand-maintained; Pāṭala's n-ary typed objects are richer. Keep the
  richness.

---

## 10. Concrete technical recommendations (from the literature + the analogues)

| Area | Recommendation | Source |
|---|---|---|
| **Retrieval** | Benchmark BM25 · dense · ColBERT-style late-interaction (multi-vector per token, residual compression) — do not assume any one wins on Sanskrit | ColBERTv2 arXiv:2112.01488 |
| **Themes** | Graph community structure is the substrate (pilot already favors Louvain/Leiden); learn representations only if they beat the hand-weighted hybrid | GraphRAG community-summaries pattern, arXiv:2404.16130 |
| **Multi-resolution** | The layered ladder already IS the RAPTOR tree; retrieve adaptively by question (passage / C1 / theme / cross-work) instead of top-k | RAPTOR arXiv:2401.18059 |
| **Verification** | Adopt a `served_trustworthy_rate`-style metric + deterministic guards as the regression gate | FoJin |
| **Human-in-the-loop** | Candidate → LLM-verify → human-review-gate → promote; margin-based routing to cut cost | FoJin alignment flywheel |
| **Publication** | Immutable segment IDs + cognate files + unpublished/published branches + integrity gate on merge | Bilara-data |

---

## 11. What to build now (the first three concrete things)

1. **Pāṭala Benchmark v0** — ~100–300 expert/editor-checked examples across the 8 tasks; the
   evaluation substrate everything else is judged against. (Highest priority — precedes all ML.)
2. **The deterministic EXPOSE services** — `/find-counterevidence` (curated), `/verify-claim-structure`,
   `/trace-dependency-structure`, `/verify-quote`, `/minimal-evidence` (dedupe-only). Thin, over data
   that already exists; they implement the verification floor as machine access.
3. **Wire the C1 + THEMES layers into the published objects** — the 63 C1 read/ renderings into the
   reader's Commentary toggle, and the accepted themes as `/api/themes` + an MCP tool. This makes the
   already-complete commentary layer visible and machine-queryable (GAPS.md priorities #1–#3).

Only after those three do the INFER projects (retrieval baselines → late-interaction → the themes
experiment → graph learning) become worth starting, each gated on the benchmark.

---

## 12. Bottom line

- **The previous diagnosis is fundamentally correct**: Pāṭala already has the ontology for ≥10 of the
  20 ML ideas; most work is exposing + learning over existing structure, not schema redesign.
- **The strongest correction**: benchmark before fancy ML. Make the sequence empirical from day one.
- **The two difficulty classes must govern planning**: EXPOSE (deterministic, cheap, ship now) vs
  INFER (model-based, expensive, benchmark-gated).
- **The flagship is narrow and well-posed**: *can structured scholarly relations beat text embeddings
  for theme discovery + retrieval?* — a clean four-arm experiment with a useful result either way.
- **The layered supervision is the genuine research asset**, especially as paired transformation
  datasets (C1 → GUIDE → vertical fidelity), a potential cross-domain benchmark.
- **FoJin validates the deterministic-guard thesis** (11% → 98% served-trustworthy); **Bilara shows
  the publication discipline**. Both confirm Pāṭala's direction and supply concrete patterns to adopt.

## PROGRESS (2026-08-12)

The review's "Expose before infer" prescription has been executed for the deterministic half:
C1s wired into the 49 published objects, 63 `c1/source/` records complete, THEMES exposed, and the 4
verify services live. The layered-supervision asset is now machine-queryable on real data — the
INFER experiments can begin against the benchmark seed (`BENCHMARK_HANDOVER.md`).
