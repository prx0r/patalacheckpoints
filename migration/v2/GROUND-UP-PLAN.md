# PĀṬALA — THE GROUND-UP PLAN (thesis → scope → harvest → transform → products)

*2026-08-14 · status: THE PLAN · the literal, bottom-up build, as if starting from zero. Every step is
grounded in real machinery that already exists or a concrete gap to build. The mental model throughout:
**Pāṭala harvests raw Sanskrit material (from PANDiT, Muktabodha, manuscripts, scholarship) and
transforms it, layer by layer, into scholarly products** — the way a refinery turns crude oil into
gasoline, plastics, and feedstock.*

---

## THE REFINERY MENTAL MODEL

```text
CRUDE (external sources: PANDiT, Muktabodha, manuscripts, texts)
   │  harvest
   ▼
CANONICAL OBJECTS (the ledger / one truth)
   │  refine layer by layer
   ▼
Source → Translation → Proof → Commentary → Argument → Synthesis
   │  project
   ▼
PRODUCTS (reading, proof, research packet, essay, lesson, benchmark)
```

The crude is external and fragmented; the refinery (Pāṭala) is what gives it structure, provenance,
and value. The moat is not the crude — it's the **refinement** (provenance + review + derivation) and
the **products** that only the refined object can produce.

---

## PHASE 0 — THE THESIS (why we exist at all)

**Start with what Pāṭala IS, because it narrows everything downstream.**

- **Thesis:** Pāṭala is the authority, provenance, expert-validation and workflow layer that turns
  digitised tantric/Sanskrit material into usable scholarly knowledge for humans and machines.
  *[NORTHSTAR]*
- **Not:** an archive, library, digitisation project, translation publisher, or "search Sanskrit."
  *[positioningpartners]*
- **Cleanest frame:** "OpenAlex for Sanskrit" — resolve the Sanskrit intellectual record. *[globalpartnerships]*

**This is the filter.** Every decision downstream asks: *"does this serve the connective/reconciliation
layer, or is it competing with an incumbent?"* If the latter, don't build it.

---

## PHASE 1 — POSITIONING & ECONOMICS (what narrows scope)

The economics tells us WHAT to harvest first and WHY it's defensible. *[endgame4, vision-08, economics/]*

**The scarce assets (the real moat):**
```
unique source data      manuscript imaging + transcription + alignment
rights                  legitimate digitisation + AI-data access
provenance              claim → translation → Sanskrit → manuscript witness
expert judgment         the thing no one can clone
trusted relationships   the scholar + institutional network
human corrections       continuously generated supervisory data
```

**The scope-narrowing economics:**
1. **Start with the Śaiva vertical** (IPVV + Tantrāloka) — because that's where the gold exists and the
   partner custodiators (IFP, Muktabodha, NGMCP) are most relevant. One vertical, deep, before breadth.
2. **Scholar incentives:** paid adjudication + ORCID/CRediT/DOI + ownership — NOT free AI cleanup.
   *[vision-08]* This decides the products (audit, research packet, attestation are monetizable).
3. **The first-product doctrine:** Translation Audit + IPVV Benchmark + Autonomous Factory. *[FIRST_PRODUCT_DECISION]*
   Start narrow, create structured correction data.

**Resulting scope:** one vertical (Śaiva/Tantra) → harvested from a handful of custodiators → refined
into proof-carrying objects → productized as scholar-facing tools. NOT "all Sanskrit, everything."

---

## PHASE 2 — THE HARVEST (data from the ground up)

**Crude oil collection.** This is the literal start of the data: pulling raw material from external
custodiators, immutable on R2, license-respected.

### Step 2.1 — The harvest adapters (real, working today)
| Source | Adapter | What it yields |
|---|---|---|
| PANDiT | `ingestion/adapters/pandit.py` | 69,779 records / 9 content types / 163 cols (bulk CSV → R2) |
| GRETIL | `gretil.py` | machine-readable Sanskrit texts |
| SARIT | `sarit.py` | TEI scholarly editions |
| NGMCP | `ngmcp.py` | Nepalese manuscript records |
| IFP/EFEO | (planned) | palm-leaf codices (~8,500, Śaiva Āgamas) |
| Muktabodha | (planned) | 3,000+ texts, 570+ e-texts |
| IIIF/VIAF/Wikidata | `iiif.py`/`viaf.py`/`wikidata.py` | manuscript images + identity crosswalks |

**The PANDiT rule (the model for every harvest):** PANDiT is CC BY-NC-SA → license firewall
(discovery/index/provenance, never unrestricted commercial). PANDiT IDs are crosswalk identifiers, never
canonical identity. Raw preserved forever; reconciliation produces NEW objects. Lossless. *[pandit.py]*

### Step 2.2 — Snapshotted to R2 (immutable Bronze)
Every harvest → `ingestion/r2.py` SnapshotStore → R2 `source/ingestion/<SRC>/snapshots/<id>/` + manifest.
Immutable, content-addressed. Nothing is lost, ever.

### Step 2.3 — Committed as canonical SOURCE objects
`register_sources.py` commits harvested material as SOURCE objects in the ledger (the one truth).
Source = raw material, a publication, NOT an epistemic verdict.

**The harvest target system** (real, machine-readable): `docs/corpus/TARGETS-INDEX.md` +
`data/corpus/targets/*.json` — `targets.json` (21 actionable), `leads.json` (39), `sivaqueue.json`
(100 "Śiva before Abhinava" targets). Query via `agent3_queue.py`.

---

## PHASE 3 — THE REFINERY (transform crude → canonical objects, layer by layer)

This is the vertical transformation — each layer a refinement with a verifier and a proof path. The
gold standard throughout is IPVV (where every layer has real hand-authored gold).

```
SOURCE ──▶ DraftTranslation ──▶ Tokenization ──▶ Translation ──▶ TranslationProof ──▶ Commentary
   (raw)     (T1 draft)          (token floor)    (prose)          (the proof)         (interpretation)
                                                                          │
                                            Theme ◀── Commentary ──▶ Argument ──▶ Review ──▶ Synthesis
                                            (clusters)              (propositions)  (gate)   (convergence)
                                                                                              │
                                                       Essay ──▶ Lesson ──▶ Scholar Attestation
                                                       (proof-linked) (understanding checks)  (human gate)
```

**The honest state today (verified):**
- Source→Commentary: **real + tested** (Source=32039, T1=306, L0=791, ARGMAP=50)
- TranslationProof: machinery + 63 golds, but only 5 registered — **the moat gap**
- Commentary: 3 registered, 63 golds exist
- Synthesis→Essay→Lesson: **EMPTY** (0 objects — workers exist, nothing triggers them)

---

## PHASE 4 — THE TRANSFORMATIONS (the "plants" — how each product is made)

Think of each product as a different **plant** built on the same refined crude. Same object, different
projection. This is where the education/economics connection becomes concrete.

| Product (plant) | Built from | The transformation |
|---|---|---|
| **Reading / Translation** | Source→Translation | the prose a reader consumes |
| **TranslationProof** | Translation + audit dimensions | the non-aggregate proof vector (the moat) |
| **Passage Workbench** | Source + Tokenization + readings | the philology-facing primitive |
| **Claim** | Passages → proposition | "Abhinavagupta treats recognition as re-identification" |
| **Argument** | Claims → inference | premises/inference/conclusion/validity/soundness |
| **Crux** | Arguments → smallest unresolved proposition | "what would change our mind" |
| **Research Packet** | all of the above compiled | a question → sources/claims/cruxes/bibliography |
| **Synthesis** | reviewed claims + arguments + cruxes | established/probable/disputed/unknown |
| **Essay** | Synthesis → sentence-sourced prose | click "why does Pāṭala say this" |
| **Lesson** | Arguments → questions | distractors map to reasoning errors |
| **Comparison** | two objects → structured disagreement | AGREEMENT/DISAGREEMENT/REAL CRUX |
| **Audit** | someone else's artifact → Findings[] | the standalone business product |
| **Benchmark** | reviewed objects → eval cases | from real failures, not trivia |
| **Context Bundle** | object + neighbors → token-budgeted packet | the agent-facing product |

*Product details in `strategy/PRODUCTS.md` (16 products, 4 families, checkpoint ladders).*

---

## PHASE 5 — THE PRIMA MATERIA (where the interesting content comes from)

The **pushing method** (`research-library/pushing/PUSHING_GUIDE.md`) is the extraction engine that turns
"a text" into claims, cruxes, and auditable truth-packets. This is how the refinery gets its *depth* —
not just structure, but real intellectual content.

```
Text (IPVV / Tantrāloka / any tradition)
   │  hound with "why" (Pushing)
   ▼
claims → cruxes → truth-packets → (feed) → Lesson questions, Research Packets, Comparisons
```

The **layered comparative questionnaire** (`DESIGN_LAYERED_COMPARATIVE_QUESTIONNAIRE.md`) makes any
tradition (Buddhist, Greek, Nyāya, Advaita) a deep set of comparable questions — so Pāṭala grows beyond
Tantra without losing Śaiva depth. This is the *content* engine behind the Education and Comparison
products.

---

## THE GROUND-UP BUILD ORDER (what actually gets built, in sequence)

```
STEP 0  Freeze the thesis + scope        (Phases 0-1)  ← already done in docs; lock it
STEP 1  Harvest a real corpus             (Phase 2)
        → run PANDiT/Muktabodha/GRETIL adapters → R2 Bronze → SOURCE objects
        → IPVV + Tantrāloka as the first vertical (the gold exists)

STEP 2  Refine to the proof               (Phase 3)
        → Source→DraftTranslation→Tokenization→Translation→TranslationProof→Commentary
        → register the 63 L200 + 63 C1 golds (the moat becomes real)
        → the honest upper layers now have real inputs

STEP 3  Converge one truth                (the plumbing)
        → promote patala_core to canonical (kill the 4 ReviewEvent/Authority defs)
        → ledger → Postgres projection (reducer)
        → site reads the graph, not the .ts seeds

STEP 4  Build the first products          (Phase 4)
        → TranslationProof + Reading (what readers see)
        → Audit + IPVV Benchmark (the first scholar-facing + business products)

STEP 5  Prime the content engine          (Phase 5)
        → pushing on IPVV/Tantrāloka → claims/cruxes → Lesson + Research Packet + Comparison

STEP 6  Unlock the upper stack            (Phase 4)
        → THEME→ESSAY→LESSON as compiled projections
        → Synthesis (established/probable/disputed/unknown)

STEP 7  The scholar products              (Phase 4)
        → Scholar Attestation (granular)
        → Research Packet / Comparison / Benchmark / Context Bundles
```

**The order principle:** build bottom-up so nothing is theatre — each step makes the previous step's
output real and observable. The crude (harvest) feeds the refinery (transform) which feeds the plants
(products). You cannot build a real product plant before the crude and the refinery exist.

---

## THE ONE-LINE PLAN

> **Harvest crude (PANDiT, Muktabodha, manuscripts → R2 → SOURCE) on the Śaiva vertical; refine it
> layer-by-layer into proof-carrying objects (IPVV as the gold standard); converge one truth (kernel +
> Postgres projection + site reads the graph); then run the plants — the 16 products — each a projection
> of the refined object, with the Pushing method supplying the intellectual depth and the scholar
> products supplying the economics.**

*This is the ground-up plan. The documentation (migration/v2/) describes it fully; this is the order of
operations. The first two steps are harvest + the gold ingest — because everything else is a projection
of material that has to exist first.*
