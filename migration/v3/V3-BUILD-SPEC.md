# PĀṬALA V3 — THE EXACT BUILD SPEC (mechanisms · external tools · stack · build-from-scratch)

*2026-08-14 · status: THE IMPLEMENTATION SPEC · the precise, buildable spec for v3 — every mechanism,
the EXACT external tool it uses, and the EXACT stack. Grounded in: the ip-graph lab's proven kernels
(51/51 experiments pass, `lib/` + `specs/SPEC-0x`), Pāṭala's v2 blueprint, the `.meta` production
organism, and the ecosystem research (EXTERNAL-REPOS). This is what a from-scratch build follows.*
*Governing spec: `SPEC-00-INFRA-BUILD.md` (ip-graph) — the repo becomes a **compiler/factory producing
immutable, addressable read artifacts**, not a request-time knowledge reconstructor.*

---

## THE MASTER ARCHITECTURE (the exact stack, one diagram)

```text
                           WRITE PLANE
      ┌───────────────────────┴────────────────────────┐
 ingestion                                        enrichment
 Python workers                                    LLM/rules
 OCR/parsing                                      entities
 normalization                                    relations/embeddings
      └──────────────────┬─────────────────────────────┘
                         ▼
                  CANONICAL STORE
              PostgreSQL + object store (R2)
                         │
                         ▼
                PROJECTION COMPILER
        Python / DuckDB / Rust hot kernels
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
      HTML             JSON            Parquet
    pages/bundles    API objects       bulk data
        └────────────────┼────────────────┘
                         ▼
                         R2
                  immutable objects
                         ▼
              CLOUDFLARE EDGE CACHE
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
      HUMAN           REST/API           MCP
      Astro           Worker        Streamable HTTP
```

**The exact stack by concern (frozen):**

| Concern | Exact choice |
|---|---|
| Canonical DB | **PostgreSQL** (Neon initially) |
| Blobs | **Cloudflare R2** (SHA-256 addressed) |
| Kernel | **Python** (`lib/` — the 17 proven kernels) |
| Analytical compile | **DuckDB + Polars + SQL** |
| Bulk export | **Parquet + Zstd** |
| Web | **Astro** |
| Interactive UI | **Preact islands** |
| Edge/API | **Cloudflare Workers + TypeScript** |
| DB bridge | **Hyperdrive** |
| MCP | **thin Streamable-HTTP adapter** |
| Search | **Postgres FTS + pg_trgm** (Tantivy only if profiled hot) |
| Agent runtime | **Hermes** (replaceable via RuntimeRouter) |
| Rust | only stabilized, measured deterministic kernels |

---

## THE EXACT MECHANISMS, LAYER BY LAYER

### MECHANISM 1 — THE KERNEL (the skeleton)

**The 17 proven kernels (`lib/` from ip-graph) — reuse, never rebuild.** Internal deps: stdlib +
`networkx` + `yaml`. Deliberately dependency-light.

| Kernel | Exact mechanism | External dep | Status |
|---|---|---|---|
| `epistemic.py` | envelope + 4-axis authority + invariant | — | PROVEN |
| `schema.py` | single-source schema compiler | **Stencila** (optional: TS/Python/Rust/JSON-LD + C2PA) | PROVEN |
| `review.py` | herdr reducer (promotion gate) | **Herdr** (pattern) | PROVEN |
| `scholar_review.py` | adversarial panel + cross-review + citecheck | — | PROVEN |
| `staleness.py` | RKA blast-radius + rebuild order | — | PROVEN |
| `query.py` | KG2Code executable graph queries | — | PROVEN |
| `retrieval.py` | PathRAG + HippoRAG | — | PROVEN |
| `translation.py` | TranslationProof (non-aggregate vector) | — | PROVEN |
| `certificate.py` | Certification Weight | — | PROVEN |
| `discovery.py` | Research Value Score | — | PROVEN |
| `education.py` | LearningClaim + interaction compiler | — | PROVEN-MECH |
| `organism.py` | UserKnowledgeState + MisconceptionGraph | — | PROVEN-MECH |
| `organism_loop.py` | consumer→research machine | — | PROVEN-MECH |
| `pedagogy.py` | live adaptive pedagogy | **pyBKT** (pattern) | PROVEN-MECH |
| `evolve.py` | MAP-Elites evolution loop | — | PROVEN-MECH |
| `agent_delivery.py` | task contract + context routing + budget + human gate | — | PROVEN-MECH |
| `essay_ingest.py` | 9-stage essay-as-derivation-input | — | PROVEN (real Ratié) |

---

### MECHANISM 2 — INGESTION (the food)

**Exact external tools:**
- **OCR/HTR:** Kraken (`mittagessen/kraken`) + eScriptorium (UI) — the default OCR, don't rebuild
- **Text normalisation:** Docling (+MCP) — PDF/Office/HTML/EPUB → normalised
- **Metadata:** GROBID (academic PDFs) · Zotero Translation Server (DOI/ISBN/arXiv)
- **Sources:** the PANDiT/GRETIL/SARIT/NGMCP/Muktabodha adapters (Pāṭala-owned)
- **Passage identity:** CTS (citable URNs, crosswalk) · **Text-Fabric** (the L0 slot model)
- **TEI:** SARIT (the export target)

**The exact flow:** source → (Kraken/Docling/GROBID) → normalise → provenance (nanopub/PROV-K) →
commit as SOURCE objects → R2 Bronze (content-addressed) → register.

---

### MECHANISM 3 — THE SCHOLARLY SPINE (Source → Commentary)

**The exact transformation sequence (each → a proven kernel):**

| Layer | Exact mechanism | External tool | Status |
|---|---|---|---|
| **Source** | (corpus) | CTS/Text-Fabric/SARIT | PROVEN |
| **DraftTranslation** | `translation.py` draft | Vidyut (Sanskrit mechanics) | PROVEN |
| **Tokenization** | the L0 token floor | **Text-Fabric** (slot model) + **Vidyut** | **NEEDS-BUILD** |
| **ArgumentOutline** | `discovery.py` + `query.py` | — | PROVEN |
| **Translation** | `translation.py` prose | — | PROVEN |
| **TranslationProof** | `translation.py` non-aggregate vector | **the moat** | **PROVEN** |
| **Commentary** | passage-local | — | **NEEDS-BUILD** |

**The TranslationProof mechanism (the moat, exact):**
- **Proof generators:** ByT5-Sanskrit · Sanskrit Heritage · Vidyut · skrutable
- **Auditors (intentionally redundant):** xCOMET · GemSpanEval · OTTAWA (omission/addition) · entailment ·
  term-consistency · MQM error vocabulary
- **The gate:** `BLOCKED` unless all hard dimensions PASS; reason is dimension-specific
  (`PARALLEL_WITNESS_CONFLICT`), never a mushy score.
- **No single aggregate score.**

---

### MECHANISM 4 — ARGUMENT / CRUX (the reasoning engine)

**The exact mechanism (`lib/review.py` + `experiment-crux-compiler.py`):**
- **IR (owned):** propositions/commitments/cruxes — the historically-grounded philosophical IR
- **External argument engines (borrowed):** ASPIC+ (semantics) · AIF/xAIF (interchange) · IAM
  (argument-mining)
- **Crux compiler:** computes minimal divergence between positions (the "what would change our mind"
  primitive)

**Exact flow:** Claims → Argument (AIF Info/Inference/Conflict) → Crux (minimal divergence) → evidence.

---

### MECHANISM 5 — REVIEW / ADJUDICATION (the immune system)

**The exact mechanism (`lib/scholar_review.py` — the frontier move):**
- **Adversarial panel** — N independent reviewers debate; a judge delivers the verdict
- **Anti-groupthink** — dissent reported, never forced into consensus
- **CiteCheck** — every citation verified; phantom/hallucinated citations flagged
- **Findings lifecycle** — OPEN → RESOLVED/REJECTED/OPEN_CRUX
- **Reviewer-of-reviewer** required (peer review is gameable — audit it)

**External pattern:** Vouch (proposal→validation→review→accept). **Pāṭala's `review_engine.py`/`lib/
review.py` is the native reducer — already built.**

---

### MECHANISM 6 — THE PRODUCTION ORGANISM (essay → render → publish) — `.meta`

**Exact flow (already built, reuse):**
- **Writer:** `.meta/workengestation/` (13 essays written) — the essay factory
- **Render:** `.meta/renderio/` (49 gold-packs proven) — the render engine
  - **Deterministic render:** Motion Canvas · Revideo · Remotion (adapters, not rewrite)
  - **Generative video (10-25% only):** LTX-2.x (hero) · Hunyuan 1.5 (workhorse) · Wan 2.2 (inserts) ·
    OmniWeaving (frontier)
- **Publish:** `.meta/reception/` + CONTROL + Postiz
- **Sites:** the 4 wing-sites (patala, tantrafiles, ochema, intelligentothers)

---

### MECHANISM 7 — EDUCATION / LESSON (the teaching layer)

**The exact mechanism (`lib/education.py` + `lib/pedagogy.py` + `lib/organism.py`):**
- **Learner model (borrowed):** pyBKT (mastery) · Dialogue-KT · adaptive-knowledge-graph (the GOLD
  interface map) · FSRS (scheduler)
- **The native object:** LearningClaim / Skill / Interaction / MasteryEvidence + MisconceptionGraph
- **The loop:** learner confusion → reveals source ambiguity → source-repair → re-teach (E2 organism)

---

### MECHANISM 8 — THE READ PLANE (the sensory system)

**The exact mechanism (from SPEC-00):**
- **Compile:** canonical store → immutable artifacts (HTML/JSON/Parquet) via the projection compiler
  (Python + DuckDB)
- **Serve:** R2 + Cloudflare CDN → static bytes; Worker only for dynamic (`/api`, MCP)
- **Agent bundles:** Context Bundles (micro 2k / standard 8k / deep 32k) — the "agent cache line"
- **MCP:** thin Streamable-HTTP adapter, ~8 verbs (resolve/search/get/context/trace/compare/query/submit)

---

## THE EXACT EXTERNAL TOOL MAP (by product — what to use, never rebuild)

| Product | Exact external tool |
|---|---|
| Translation | Vidyut · ByT5-Sanskrit · Sanskrit Heritage |
| TranslationProof | xCOMET · GemSpanEval · OTTAWA · MQM · entailment |
| Passage workbench | Mirador 4 + TextOverlay · Recogito · CTS · Text-Fabric |
| Claim | (the epistemic envelope — Pāṭala-native) |
| Argument | ASPIC+ · AIF/xAIF · IAM |
| Crux | (the crux-compiler — Pāṭala-native) |
| Review | Vouch (pattern) · Herdr (reducer pattern) |
| Scholar Attestation | ORCID/CRediT/DOI · C2PA (signed provenance) |
| Research Packet | PathRAG · HippoRAG · KG2Code · Zotero/Crossref/OpenAlex |
| Synthesis | (evolve.py MAP-Elites) |
| Essay | workengestation (.meta) |
| Education | pyBKT · Dialogue-KT · FSRS · adaptive-knowledge-graph |
| Comparison | (claim-standardisation — Pāṭala-native) |
| Audit | MQM · RARR · RefChecker · GraphCheck |
| Dataset/Benchmark | Mitrasamgraha · SciFact · wmt-mqm |
| Context Bundle | (the projection compiler — Pāṭala-native) |
| OCR/Manuscripts | Kraken · eScriptorium · Mirador |
| Video/Media | Remotion · Revideo · Motion Canvas · LTX-2 · Hunyuan · Wan |
| Distribution | Postiz · Postiz Agent |

---

## THE FROM-SCRATCH BUILD (the exact order)

```
STEP 0 — the substrate
  - PostgreSQL (Neon) + R2 bucket (patala) + Cloudflare account
  - the 17 kernels from lib/ (already written, dependency-light) + their validate-*.py

STEP 1 — the graduation test (make it real)
  - take ONE real IPVV claim → run through the whole stack on real evidence
  - build the 3 needs-build products: Essay, Commentary, Tokenization (via Text-Fabric + Vidyut)
  - this is the anti-theatre test that turns 51 passing experiments into "Pāṭala works"

STEP 2 — the harvest
  - wire the ingestion adapters (PANDiT/GRETIL/SARIT/Muktabodha) + Kraken/Docling/GROBID
  - source → R2 Bronze → register SOURCE objects

STEP 3 — the spine
  - Source → DraftTranslation → Tokenization → Translation → TranslationProof → Commentary
  - register the IPVV gold (63 L200 + 63 C1) with derivation edges

STEP 4 — the reasoning engine
  - Argument + Crux over the gold (the CP4 frontier)

STEP 5 — the review gate
  - the adversarial panel + CiteCheck + findings lifecycle (signed ReviewEvents)

STEP 6 — the production organism (reuse .meta)
  - verified Synthesis → workengestation (essay) → renderio (media) → reception (publish) → sites

STEP 7 — the read plane
  - the projection compiler → immutable R2 artifacts → CDN/Worker/MCP (8 verbs, Context Bundles)

STEP 8 — the sensory loop + expansions
  - education compiler + the organism (consumer-as-probe)
  - layer the 6 expansions (marketplace, what-if, question-growth, self-proving, etc.)
```

---

## THE THREE GOVERNING LAWS (unchanged — the organism's constitution)

```text
TRUTH     Nothing becomes true because an agent says so.   (the epistemic gate)
COMPILE   Nothing recomputes unless its dependencies changed. (the staleness DAG)
READ      Nothing computes at request time if bytes could already exist. (the read plane)
```

---

## THE BUILD TARGETS (the honest to-do)

1. **The graduation test** (one IPVV claim through the whole stack on real evidence) — makes it real
2. **3 needs-build products:** Essay · Commentary · Tokenization (via Text-Fabric + Vidyut)
3. **Signed human attestation** (gap E — C2PA/ORCID)
4. **The IPVV gold ingest** (63 L200 + 63 C1 with derivation edges)
5. **Then the 6 expansions** (each already proven as a mechanism)

---

*This is the exact v3 build spec — every mechanism, its exact external tool, and the exact stack,
grounded in the proven kernels. From-scratch build follows STEP 0-8; the graduation test is the gate
that makes the organism real. The machinery is already built and proven (17 kernels, 51/51 experiments);
v3 is the assembly, not the invention.*
