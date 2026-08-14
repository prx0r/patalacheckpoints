# PĀṬALA V2 — THE EXTERNAL EVIDENCE BASE (every layer grounded in literature + GitHub repos)

*2026-08-14 · status: THE AUTHORITATIVE EXTERNAL REFERENCE · companion to `LAYERS.yaml` + `LAYER-MAPPING.md`
+ `MODULES.md`. For EVERY layer: the external GitHub repos + literature that support it, what to pinch vs
what Pāṭala must own, and the source research docs. This is what makes migration/v2 the FINAL version —
each layer's design is validated against what the ecosystem has already built.*
*Sources: the research caches in `source-evidence/docs/tools/docs-cache/` (the fetched research) +
`docs/process/githubclones.md` + `docs/process/external-tools.md` + `docs/layers/12-live-system.md`.*
*The governing thesis: **a stack of narrow systems around a small kernel, with Hermes as the execution
plane.** Build the kernel brutally well; make Hermes its nervous system; make the GitHub projects its
organs. Pāṭala decides what is true; the ecosystem supplies the machinery.*

---

## THE GOLDEN RULE (for every layer)

> **Pāṭala decides what is true and what matters. Hermes decides who does the work and how it executes.
> The GitHub projects are organs — harvest their implementations, never vendor them.**

---

## LAYER BY LAYER — THE EXTERNAL GROUNDING

### Layer 00 — Governance (anti-theatre doctrine)

| External | What it supports | Pinch / Own |
|---|---|---|
| — (Pāṭala-native doctrine) | the anti-theatre rule, 3 categories, banned words | **OWN** — no external equivalent |

**Why no external:** the doctrine is Pāṭala's core value. Nothing in the ecosystem enforces
"a tested schema ≠ a result." This is the one thing never borrowed.

---

### Layer 01 — Ingestion / Harvest (sources → R2 → SOURCE)

| External | What it supports | Pinch / Own |
|---|---|---|
| **Docling** + Docling MCP | general document normalization (PDF/Office/HTML/EPUB/images/OCR/tables) | **PINCH** — the ingest front-end (don't make DoclingDocument canonical) |
| **GROBID** | academic PDFs: metadata, references, citation contexts, TEI | **PINCH** |
| **S2ORC doc2json** | document normalization patterns | **PINCH** (study) |
| **Zotero Translation Server** | DOI/ISBN/PMID/arXiv resolution, webpage parse, BibTeX/RIS, metadata normalize | **PINCH** — "the boring piece that saves months" |
| PANDiT/GRETIL/SARIT/NGMCP/Muktabodha adapters | the actual sources | **OWN** (the adapters) |
| `ingestion/r2.py` (SnapshotStore) | immutable Bronze on R2 | **OWN** |

**Sources:** `ecosystem-15planes.md` §4 · `githubclones.md` · `external-tools.md`.

---

### Layer 02 — Atlas / Identity (the resolve backbone)

| External | What it supports | Pinch / Own |
|---|---|---|
| **Zotero MCP Plus** (`alisoroushmd/zotero-mcp`) | graph-analysis + integration for the bibliography graph | **PINCH** |
| **Cita** (`diegodlh/zotero-cita`) | sync/citation adapters (Wikidata/Crossref/SemanticScholar/OpenAlex), coauthorship networks | **PINCH** |
| OpenAlex / Crossref | identity + metadata resolution | **PINCH** (via `metadata_resolver.py`) |
| `source-resolution/source-resolver-design.md` | the federated resolver design | **OWN** |
| **Mirador 4** + Mirador TextOverlay | manuscript viewing + OCR overlay (IIIF) | **PINCH** (embed, don't build) |

**Sources:** `ecosystem-15planes.md` §5-6 · `vision-15` (OpenAlex for Sanskrit).

---

### Layer 03 — Factory / Compiler (the reactive compiler)

| External | What it supports | Pinch / Own |
|---|---|---|
| — (the transformation registry + projection DAG are Pāṭala's own) | the reactive compiler model | **OWN** |
| **DuckDB + Polars + SQL** | analytical compilation | **PINCH** |
| **Parquet + Zstd** | bulk publication format | **PINCH** |
| `SPEC-00` (from mixxii/other) | the write-side/read-side compilation model | **OWN** (adopt) |

**The projection DAG** (the single most important infra abstraction) is **Pāṭala-owned** — no external
tool does "the same graph as correctness + staleness + scheduler + retrieval."

---

### Layer 04 — Evidence / Adapters (the external-tool seam)

| External | What it supports | Pinch / Own |
|---|---|---|
| the 69-tool MANIFEST | the borrowed-tool registry | **OWN** (the registry) |
| **GROBID** · **Docling** · **OpenAlex** · **Crossref** · **OpenCitations** | the evidence adapters | **PINCH** |
| **AIF / xAIF** (`aif-arg-datasets`, `oAMF`) | argument interchange | **PINCH** (adapters only — native stays richer) |

**Honest state (verified):** only vidyut + the ingestion adapters are in production; the bibliography
adapters are built-not-wired. See `PRODUCTS-VISIONS.md` + the MANIFEST.

---

### Layer 05 — The Scholarly Spine (Source → Commentary)

| External | What it supports | Pinch / Own |
|---|---|---|
| **vidyut** (Sanskrit linguistics) | segmentation/morphology/inflection/transliteration/sandhi/meter | **PINCH** — the canonical SanskritLinguisticAdapter (INTEGRATED) |
| the IPVV gold (sibling repos) | hand-authored T1/L0/L200/C1 gold | **OWN** (the prima materia) |
| **MITRA** (`dharmamitra/mitra-parallel`) | 1.74M Sanskrit↔Tibetan↔Chinese parallel pairs → cross-source verification | **INGEST** (the proof's external grounding) |
| **MQM** (`google/wmt-mqm-human-evaluation`) | the translation error taxonomy for audit | **PINCH** (vocabulary) |

**Sources:** `githubclones.md` §K · `patalatranslate.md` · `external-paper-research.md`.

---

### Layer 05 — TranslationProof (L200) — **THE MOAT**

| External | What it supports | Pinch / Own |
|---|---|---|
| — (the non-aggregate proof vector is Pāṭala's own, NOVEL) | the proof model | **OWN** — the differentiator |
| **MITRA** | Sanskrit↔Tibetan↔Chinese as independent cross-source witnesses | **INGEST** |
| **MQM** | the error taxonomy for the proof's audit dimensions | **PINCH** |

**Why it's the moat:** *"A translation can't be proven equivalent to source, but it CAN be made
proof-carrying."* No external project does this. `docs/process/INDUSTRY-ALIGNMENT.md` marks
TranslationProof as NOVEL. The 63 gold audits (sibling `sanskritree/.../l200/`) are the evidence.

---

### Layer 06 — Argument / Crux (the philosophy engine, CP4)

| External | What it supports | Pinch / Own |
|---|---|---|
| **ASPIC+ / py-aspic** | structured argumentation semantics | **PINCH** (via `aspic_adapter.py`) |
| **AIF** (`aif-arg-datasets`, `oAMF`) | argument interchange | **PINCH** (adapters) |
| **RARR** (retrieve→check→revise) | claim checking | **PINCH** (in the ensemble) |
| **RefChecker** | atomic-claim checking | **PINCH** |
| **GraphCheck** | relationship-structure checking | **PINCH** |
| **DSPy** | optimize extraction against Pāṭala gold | **PINCH** |
| **IAM** | argument-mining decomposition | **PINCH** |
| **PHILOSOPHY-ENGINE-ARGUMENT-UNDER-INTERPRETATION.md** | the historical IR the engines can't provide | **OWN** (the moat) |

**The Pāṭala position:** *"Don't reinvent computational argumentation. Own the historically grounded
philosophical IR that existing engines cannot provide."* The engines (ASPIC/AIF/RARR/etc.) are the
verification; the IR is Pāṭala's. Sources: `PHILOSOPHY-ENGINE-*` + `ecosystem-15planes.md` §7-8.

---

### Layer 06 — Review / Adjudication (the reducer)

| External | What it supports | Pinch / Own |
|---|---|---|
| **Vouch** (`vouchdev/vouch`) | agents propose durable knowledge, require cited evidence, separate proposal from approval, append-only audit | **PINCH** — "closest to Pāṭala's central doctrine" |
| **Sage Wiki** (`xoai/sage-wiki`) | compiler model, fact→source citation | **PINCH** |
| **llm-wiki-newsroom** | the "reground" cycle (refresh published pages against source) | **PINCH** |

**Source:** `ecosystem-15planes.md` §3. Pāṭala's `review_engine.py` is the reducer; Vouch validates the
pattern (Pāṭala-native version already built).

---

### Layer 07 — Verification (the eval plane)

| External | What it supports | Pinch / Own |
|---|---|---|
| **Phoenix** (`Arize-ai/phoenix`) | OpenTelemetry agent/LLM tracing + eval | **PINCH** (external trace plane) |
| **Langfuse** | self-hosted trace instrumentation | **PINCH** |
| RARR / RefChecker / GraphCheck / DSPy | the verification ensemble | **PINCH** |
| the 5 golds + NAT evals | the independent eval plane | **OWN** |

**Rule:** external tracing stays EXTERNAL; Pāṭala's epistemic review stays INSIDE Pāṭala.
Source: `ecosystem-15planes.md` §8, §12.

---

### Layer 08 — Scholar Attestation (the human gate)

| External | What it supports | Pinch / Own |
|---|---|---|
| **Vouch** | proposal→validation→review→accept with cited evidence | **PINCH** |
| ORCID / CRediT / DOI | durable academic credit | **PINCH** (the identity/credit standard) |
| — (attestation to granular objects) | the granular attestation model | **OWN** |

**Source:** `vision-07` · `vision-08` · `ecosystem-15planes.md` §3.

---

### Layer 09 — Organism / Human-Understanding Graph

| External | What it supports | Pinch / Own |
|---|---|---|
| **Graphiti** (`getzep/graphiti`) | temporal facts + episode provenance | **PINCH** (as a PROJECTION, not canonical) |
| **CoWork OS** | entity/relationship memory, temporal edges, confidence decay | **PINCH** (study) |
| **DeepTutor** (`HKUDS/DeepTutor`) | L1/L2/L3 memory pipeline + KB version fingerprints | **PINCH** |
| **pyBKT** | interpretable mastery state | **PINCH** |
| **Dialogue-KT** | tutor/student dialogue KT | **PINCH** |
| **adaptive-knowledge-graph** (`MysterionRise/adaptive-knowledge-graph`) | **GOLD**: Neo4j concept/prerequisite + learner state + BKT/IRT | **PINCH** (tear apart for interfaces) |

**Sources:** `ecosystem-15planes.md` §9-10 · `organism/*` visions.

---

### Layer 10 — Surfaces / Products

| External | What it supports | Pinch / Own |
|---|---|---|
| **Mirador 4** | manuscript viewing | **PINCH** |
| **Recogito** | annotation/selection UX | **PINCH** |
| **INCEpTION** | multi-annotator adjudication | **PINCH** (study, not necessarily deploy) |
| — (the product projections) | the compiled read-plane products | **OWN** |

---

### Layer 11 — Org / Economics

| External | What it supports | Pinch / Own |
|---|---|---|
| **Postiz** (`gitroomhq/postiz-app`) | scheduling, analytics, multi-platform | **PINCH** (the publishing lane) |
| ORCID / CRediT / DOI | scholar credit | **PINCH** |

---

### Layer 12 — Live System (the orchestration glue)

| External | What it supports | Pinch / Own |
|---|---|---|
| **Hermes Agent** | primary orchestrator (kanban, profiles, worker lanes, skills, sessions) | **USE** — the execution plane |
| **Gas Town / Gas City** | declarative workflow formulas, worktrees, role hierarchy | **PINCH** |
| **Agetor** | Task≠Run, pinned base commit, run history | **PINCH** |
| **Overstory** (`jayminwest/overstory`) | typed agent mail, merge queues, watchdog | **PINCH** |
| **agtx** | state-machine transitions + allowed_actions | **PINCH** |
| **mcp_agent_mail** | identities, durable threads, file leases | **PINCH** |
| **Beads / Beads Viewer** | deterministic graph triage (PageRank/critical path) → `patala_next_action()` | **PINCH** |
| **Epicenter** (`epicenter-md/epicenter`) | DB-as-truth, Markdown-as-view | **PINCH** |
| **Postiz Agent** | the Hermes publishing lane | **PINCH** |

**Sources:** `ecosystem-15planes.md` §1-2, §11, §14 · `coordinate-peer-review.md` · `githubclones.md` §G.

---

## THE COMPLETE CLONE / PINCH LIST (all external repos, by layer)

*From `ecosystem-15planes.md` + `githubclones.md` + `layertools-research.md`:*

```
Hermes Agent · Gas Town · Gas City · Overstory · agtx · mcp_agent_mail · Agetor · Beads ·
Beads Viewer · Vouch · Sage Wiki · llm-wiki-newsroom · Docling (+MCP) · GROBID · Zotero Translation
Server · Zotero MCP Plus · Cita · Mirador 4 · Mirador TextOverlay · Recogito · INCEpTION · AIF
arg-datasets/oAMF · RARR · RefChecker · GraphCheck · DSPy · IAM · Graphiti · CoWork OS · DeepTutor ·
pyBKT · Dialogue-KT · OATutor · OpenTutor · adaptive-knowledge-graph · Epicenter · Phoenix · Langfuse ·
Remotion · OpenMontage · remotion-superpowers · frankxai/remotion-video · Postiz · Postiz Agent ·
MITRA · MQM
```

---

## WHAT PĀṬALA MUST ITSELF OWN (the moat — never borrowed)

```text
identity / provenance / permissions
passage / claim / argument / review / trajectory / event semantics
the epistemic review-gated promotion      ← the anti-theatre core
the capability API (domain verbs)
the learner/education semantics
the projection engine + staleness
patala_next_action() triage
the TranslationProof model               ← the differentiator
```

**Do NOT build:** PDF parsing, manuscript rendering, generic agent scheduling, generic trace
observability, social upload adapters, BKT itself, basic annotation widgets, generic citation scraping.
*[ecosystem-15planes.md]*

---

*This is the authoritative external grounding for every layer. Each layer's design is validated against
what the ecosystem built — Pāṭala owns the kernel + the doctrine + the proof; the GitHub projects supply
the organs. See the research caches in `docs-cache/` for the full fetched research.*
