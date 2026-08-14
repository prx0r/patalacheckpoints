# PĀṬALA VISION — CANONICAL REVIEW INDEX

*2026-08-14. THE machine-parseable review of every vision doc. Each entry follows ONE schema so an
agent can resolve any doc to: proper name · what it is · core contribution · layer · build status ·
related docs. This is the canonical "what does each vision doc actually say, and is it built" reference.
Every field is stable and queryable.*

---

## THE SCHEMA (every entry)

```yaml
doc:            # original path
name:           # proper / canonical name
summary:        # one line — what it actually decides
contribution:   # the 1-3 ideas that matter most
layer:          # Layer 00-12 (see docs/layers/) + category (A-H, see CATEGORIES.md)
status:         # BUILT | PARTIAL | ASPIRATIONAL | INDEX (describes existing state vs design)
related:        # docs it links to
```

**Layer key:** 00 Governance · 01 Ingestion · 02 Atlas · 03 Factory · 04 Evidence · 05 Research ·
06 Commentarial · 07 Verification · 08 Human Authority · 09 Organism · 10 Surfaces · 11 Org/Economics ·
12 Live System. **Status key:** `BUILT` = describes working machinery · `PARTIAL` = substrate built, feature pending ·
`ASPIRATIONAL` = design/strategy, not built · `INDEX` = an index/lens artifact (no new claims).

---

# A. FOUNDATIONS (core + origin arc)

| doc | name | contribution | layer | status |
|---|---|---|---|---|
| `CORE-BIBLE.md` | The Vision Canon — one vision in 6 zoomable layers | the "one vision, many zoom levels" doctrine; honest checkpoint layer | all (0-1) | PARTIAL |
| `endgame1.md` | The Translation Laboratory | machine-assisted critical translation to auditable publication | 03 | PARTIAL |
| `endgame2.md` | The Tantra Hub | living bibliography + text-reader + workshop + commentary + media | 10 | PARTIAL |
| `endgame3.md` | One Scholarly Infrastructure, Several Interfaces | never separate projects; one core, many surfaces | all | PARTIAL |
| `endgame4.md` | The Economic Thesis | scarce assets = source data + rights + provenance + expert judgment | 11 | ASPIRATIONAL |
| `endgame5year.md` | The 2026-2031 Strategic Window | manuscript-digitisation money, IKS funding, DH, AI | 11 | ASPIRATIONAL |
| `NORTHSTAR.md` | The Deepest Strategy | scholarly-intelligence layer for tantric heritage (Gyan Bharatam context) | 00 | ASPIRATIONAL |
| `foundationalideas.md` | The Passage-Identity Idea | every artifact attaches to a stable passage/text identity | 02 | PARTIAL |
| `positioningpartners.md` | Positioning & Partners | the connective-research-layer positioning | 11 | ASPIRATIONAL |

# B. SCHOLARS (human layer) → Layer 08

| doc | name | contribution | layer | status |
|---|---|---|---|---|
| `vision-06-adversarial-review.md` | Pāṭala Review — the Adversarial Scholarly Review Service | the "research compiler" metaphor (ERROR/WARNING/INFO diagnostics); auditable criticism; dependency/impact analysis | 07, 08 | ASPIRATIONAL |
| `vision-07-new-scholar.md` | The New Scholar — from Document Production to Structured Inquiry | essay = a rendering of the graph, not the object; forkable scholarship; "AI proposes, scholar adjudicates" | 08 (+05) | ASPIRATIONAL |
| `scholars/README.md` | The Scholars Lens | scholars are the engine (corrections = data capital), not the audience | 08 | INDEX |

# C. ECONOMICS (incentives + market) → Layer 11

| doc | name | contribution | layer | status |
|---|---|---|---|---|
| `vision-08-scholar-economics.md` | Scholar Incentives & Economics | paid adjudication not unpaid review; credit via ORCID/CRediT/DOI; the Scholar Compact | 11 | ASPIRATIONAL |
| `vision-10-market-entry-and-partnerships.md` | Market Entry & Partnerships | BHU anchor; funding map; low-cost gold-annotation pilots; Gantt roadmap | 11 (+08,05) | ASPIRATIONAL |
| `economics/README.md` | The Economics Lens | scarce-assets moat stack; the flywheel; six+ capital pools | 11 | INDEX |

# D. MEDIA & ORGANISM (human-understanding graph) → Layer 09

| doc | name | contribution | layer | status |
|---|---|---|---|---|
| `vision-09-media-and-cross-tradition.md` | The Media Projection Layer & Cross-Tradition Engine | projection doctrine; tradition-agnostic engine; anti-theater gate | 09 (+03) | ASPIRATIONAL |
| `organism/patalaorganism.md` | The Organism Thesis — User Interaction as a Second Graph | consumer as measurement instrument; two first-class graphs; the Q moat variable | 09 | ASPIRATIONAL |
| `organism/patalaorganismvisions.md` | The Organism at Scale | trajectories; empirical pedagogy; domain packs over shared primitives | 09 (+10) | ASPIRATIONAL |
| `organism/consumerorganism.md` | Consumer-as-Probe — Questions as a Research Signal | the Gap Engine + canonical `Gap` object; falsification pressure | 09 (+05,08) | ASPIRATIONAL |
| `organism/consumerorganismtech.md` | The Organism Engineering Blueprint | immutable event ledger → discrete graph projections; tool-reuse map; 5-gate review | 09 (+07,08) | ASPIRATIONAL |
| `organism/organism_meh.md` | The Adaptive-Learning Architecture | Knowledge Space Theory + outer fringe; BKT → graph-KT → contextual bandit | 09 | ASPIRATIONAL |

# E. PLATFORM & PRODUCT (multi-surface) → Layer 10

| doc | name | contribution | layer | status |
|---|---|---|---|---|
| `vision-12-multi-surface-platform.md` | The Multi-Surface Platform — Five Permission-Scoped Surfaces | one core, five surfaces; surfaces differ by permission not truth | 10 | PARTIAL |
| `vision-13-product-portfolio-by-user-base.md` | The Product Catalog by User Base | benchmark = authority / Audit = product wedge; M = D×P×V×N×A×E | 10 | ASPIRATIONAL |
| `ENDGAME_SITE_SPEC.md` | The Tantra Reader Site Spec | five-level authority; compile-time-only site; supply chain → rendered elements | 10 (02) | ASPIRATIONAL |

# F. EXPANSION / CORPUS (Śiva-before-Abhinava) → Layer 03

| doc | name | contribution | layer | status |
|---|---|---|---|---|
| `expansion/vision-11-siva-before-abhinava.md` | Śiva Before Abhinava — the Genealogy of Śaiva Ideas | braided-history correction; six corpora + three graphs; Abhinava-as-compiler-transformer | 03 (+01,05) | ASPIRATIONAL |
| `expansion/vision-11-siva-before-abhinava-prehistory.md` | Śiva Before Abhinava — the Deep Source Tree | the evidence ladder; Ṛgveda+Avesta as deepest corpus; Indus-as-hypothesis boundary | 03 (+01) | ASPIRATIONAL |
| `expansion/vision-11-siva-before-abhinava-corpus-manifest.md` | Śiva Corpus Acquisition Manifest | open/legal-vs-piracy; Tier 0-3 build order; machine-readable download manifest | 01, 03 | PARTIAL |
| `expansion/README.md` | The Expansion Lens | the cross-corpus expansion index | 03 | INDEX |

# G. ATLAS / IDENTITY (research graph + manuscripts) → Layer 02

| doc | name | contribution | layer | status |
|---|---|---|---|---|
| `vision-14-manuscript-to-scholarly-asset.md` | Manuscript → Machine-Readable Scholarly Asset | the quality fingerprint; derived-vs-input honesty; manuscript auto-ingest | 02 (+01,10) | PARTIAL |
| `vision-15-patala-atlas-sanskrit-research-graph.md` | The Pāṭala Atlas — OpenAlex for Sanskrit | the textual-transmission spine; identity distinction; lazy reconciliation ingest | 02 | PARTIAL |
| `source-resolution/source-resolver-design.md` | Source Resolver — a Federated Reconciliation Engine | OpenRefine-style federated reconciliation; authority ladder; textual-criticism compiler | 02 (+01,04) | ASPIRATIONAL |
| `atlas/technical-architecture-v1.md` | Pāṭala Technical Architecture v1 | the Pāṭala Authority Graph; Postgres/R2/event-log; 3 P0 schema corrections | 02 (+00,10,12) | PARTIAL |
| `atlas/atlas-engineering-blueprint.md` | Atlas Engineering Blueprint | copy OpenAlex product not scale; entity-vs-asset; the boring substrate | 02 (+10) | ASPIRATIONAL |
| `atlas/atlas-cloudflare-edge-layer.md` | Atlas Cloudflare Edge Layer | Cloudflare = global front door, not canonical DB; agent-native API | 10 (+02,12) | ASPIRATIONAL |
| `atlas/atlas-performance.md` | Atlas Performance Doctrine — Pāṭala Lightning | compute-on-write; immutable-is-cacheable; 6 performance laws | 10 (+02) | ASPIRATIONAL |
| `atlas/agent-optimization.md` | Agent Optimization — the Agent Product Surface | one-question=one-call; two-tier MCP; agent usability as measurable product | 10 (+12,07) | ASPIRATIONAL |

# H. EDUCATION / RESEARCH-PROGRAM

| doc | name | contribution | layer | status |
|---|---|---|---|---|
| `essayguide.md` | The Essay & Research Program Guide | essay/review/education as first-class science; six hard problems; 4 benchmarks | 05 (PG) | ASPIRATIONAL |
| `education/PATALA-EDUCATION-SYNTHESIS.md` | Pāṭala Education — Canonical Cross-Lane Vision | education is a projection of the scholarly graph; wrong-answer→epistemic-neighbor; proof-before-platform | 05, 09 | ASPIRATIONAL |
| `education/LEARNING_STRATEGY.md` | Learning Content Strategy | research once, structure once, distill repeatedly; the knowledge packet | 05 | ASPIRATIONAL |
| `education/EDUCATION_VISION.md` | The Graph-Native Teaching Engine | the graph (not LLM) selects the move; mechanism-shapes; register dial | 05, 09 | ASPIRATIONAL |
| `education/sources/` (01-05) | Raw Education Design Docs | original education design dialogue (byte-preserved) | 05 | reference |
| `functionality/hermes-execution.md` | The Vision × Hermes Execution Map | Hermes = replaceable execution; the moat = Pāṭala-owned layer | 12 | PARTIAL |
| `functionality/README.md` | The Functionality Lens | projection taxonomy (machinery vs interfaces vs foundations); anti-weeds rule | 04 | INDEX |
| `functionality/research/2026-08-12/` | Product Research-and-Build Pack | 5 projects (Factory/Benchmarks/Audit/Review/Workbench) + reuse/build doctrine | 03-08 | PARTIAL |

---

# THE PER-LAYER VISION SYNTHESIS (which docs build each layer)

> This is the operational view: **for each Layer, which vision docs specify it, and its overall vision.**

## Layer 00 — Governance
**Vision:** one constitution: the anti-theatre rule, the authority ladder, the operating axioms.
**Docs:** `AGENTS.md`, `AGENTS-DOCTRINE.md`, `CORE-BIBLE.md` (checkpoint layer), `NORTHSTAR.md`.
**Built:** `theatre_check.py`, `CANONICAL-DAG.yaml`.

## Layer 01 — Ingestion
**Vision:** any source → canonical objects with provenance + license firewall.
**Docs:** `expansion/vision-11...corpus-manifest.md`, `atlas-engineering-blueprint.md` (ingest step).
**Built:** `ingestion/` (SourceAsserter, AtlasWriter, 8 adapters), R2 Bronze snapshots.

## Layer 02 — Atlas
**Vision:** the canonical research graph — textual transmission, identity distinction, reconciliation.
**Docs:** `vision-14`, `vision-15`, `source-resolver-design`, `atlas/technical-architecture-v1`,
`atlas-engineering-blueprint`, `atlas-cloudflare-edge-layer`, `atlas-performance`.
**Built:** Postgres 22-table schema, resolver, API, crosswalk, deterministic UUID. **PARTIAL** (read API/reconciliation pending).

## Layer 03 — Factory
**Vision:** the compiler SOURCE→C1→THEMES, plus corpus expansion (Śiva-before-Abhinava).
**Docs:** `endgame1`, `expansion/*` (corpus), `technical-architecture-v1` (factory plane).
**Built:** workers, `object_registry`, scheduler, DAG, event ledger. **PARTIAL** (ARGUMENT/SYNTHESIS/upper layers empty).

## Layer 04 — Evidence
**Vision:** the contracts + adapters + eval plane (reuse-first, Pāṭala owns the epistemic seam).
**Docs:** `functionality/README.md`, `source-evidence/docs/reuse-first-stack.md`, `external-tools.md`.
**Built:** contracts, 62 tools documented, eval plane. **BUILT.**

## Layer 05 — Research / Epistemic Core (MOAT)
**Vision:** propositions → arguments → cruxes → synthesis → essay/education; the ArgumentSynthesis convergence.
**Docs:** `globalgoal.md`, `agent1atlas.md`, `essayguide.md`, `education/*`.
**Built:** argument/crux/synthesis/essay/education compilers, golds. **PARTIAL** (ARGUMENT/SYNTHESIS 0 objects).

## Layer 06 — Commentarial Graph
**Vision:** papers → ScholarContributionPackets over the primary graph.
**Docs:** `06-commentarial-graph.md`, `commentarialgraph-research.md`, `externalpaper-research.md`.
**Built:** none (design only).

## Layer 07 — Verification
**Vision:** external methods test Pāṭala; the benchmark family (TantraFact/ArgumentBench/...).
**Docs:** `vision-06`, `08-verification-plane.md`, `peer-review-goat.md`.
**Built:** eval plane (Inspect), the 10 self-tests. **BUILT.**

## Layer 08 — Human Authority
**Vision:** scholars review/adjudicate/promote; the scholar workbench + the review engine.
**Docs:** `vision-06`, `vision-07`, `scholars/README.md`, `contracts_human_authority.py`, `review_engine.py`.
**Built:** ReviewEvent ledger + impact_report (the Vouch equivalent, done better). **PARTIAL** (workbench UI pending).

## Layer 09 — Organism
**Vision:** the human-understanding graph — consumers as probes; adaptive learning; the Q moat variable.
**Docs:** `vision-09`, `organism/*` (5 docs).
**Built:** none (design only).

## Layer 10 — Surfaces
**Vision:** one core, five permission-scoped surfaces; the sites + APIs + MCP.
**Docs:** `vision-12`, `vision-13`, `atlas/agent-optimization`, `ENDGAME_SITE_SPEC.md`, `05-app-api-sites.md`.
**Built:** `app/`, `mcp/`, `openpatala/`, Astro. **PARTIAL** (Scholar/Contributor/Reviewer surfaces pending).

## Layer 11 — Org & Economics
**Vision:** scholar credit + market entry + the funding window.
**Docs:** `vision-08`, `vision-10`, `economics/README.md`, `endgame4`, `endgame5year`, `positioningpartners`.
**Built:** documented strategy only. **ASPIRATIONAL.**

## Layer 12 — Live System
**Vision:** Pāṭala decides what matters; Hermes decides how; docs project from truth.
**Docs:** `12-live-system.md`, `hermes-execution.md`, `handover/hermes/*`, `coordinate-peer-review.md`.
**Built:** Tier-1 truth (object_registry, review_engine, event ledger). **PARTIAL** (the 7 pieces pending).

---

## HOW AN AGENT USES THIS

1. **Resolve a doc** → its `layer`, `status`, `contribution`, `related` from the tables above.
2. **Resolve a layer** → the per-layer synthesis section lists which docs build it + its overall vision.
3. **Decide build vs borrow** → cross-check `docs/process/RECONCILIATION.md` (built vs borrowed vs agentic)
   and `docs/process/external-tools.md` (the 62 tools).
4. **The status column is the honesty check** — `ASPIRATIONAL` means design, not built.

---

## THE ANTI-REDUNDANCY VERDICT (strict consolidation)

> The machine-verifiable rule (enforced by `docs/vision/check_manifest.py`): **no two vision docs may
> share a distinct role.** Every doc has ONE role, ONE accurate name, ONE real file.

**Consolidation findings (what stays, what's distinct):**

| Cluster | Finding | Verdict |
|---|---|---|
| **organism** | `consumerorganismtech` + `organism_meh` both survey Graphiti/pyBKT/pyKT/OATutor/OpenTutor/GRKT/GKT | **KEEP both** — engineering-blueprint vs learner-theory are distinct roles. But the shared tool-survey is REDUNDANT with `docs/process/external-tools.md` (canonical); the organism docs should reference it, not re-list it. |
| **education** | `EDUCATION_VISION` + `LEARNING_STRATEGY` + `PATALA-EDUCATION-SYNTHESIS` all mention knowledge-packet/prerequisite | **KEEP all 3** — canonical / content-strategy / teaching-engine are distinct. `PATALA-EDUCATION-SYNTHESIS` is THE canonical; the other two reference it. |
| **indices** | `CATEGORIES` + `INDEX` + `REVIEWS` + `VISION-MANIFEST` all describe the vision collection | **KEEP all 4** — distinct: taxonomy / narrative / agent-review / machine-registry. |
| **vision-11** | flat `vision-11-siva-before-abhinava.md` was an EXACT duplicate of `expansion/vision-11...` | **REMOVED** (deduplicated; canonical = `expansion/`). |

**The strict rule going forward:** if a new vision doc claims a role already in the manifest, it must be
consolidated into the existing doc (or the existing doc split). Run `python3 docs/vision/check_manifest.py`
to verify no drift.

*This index is the canonical, agent-resolvable view of the vision. `CATEGORIES.md` is the category taxonomy;
`CORE-BIBLE.md` is the one-vision map; `INDEX.md` is the fuller narrative reference.*
