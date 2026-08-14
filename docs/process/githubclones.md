# GITHUB CLONES & REPOS TO RAID — the reusable-research registry

*Part of `docs/process/README.md`. This is the canonical registry of EXTERNAL GitHub repos we have
found, cloned, or plan to clone — and what we can REUSE from each. It complements
`external-tools.md` (mature infrastructure) by tracking the **researcher-built, one-off projects** that
solve 30% of a Pāṭala subsystem and are worth stripping for machinery, data, or patterns.

**Discipline:** every entry records (a) what it is, (b) what's actually reusable, (c) license/provenance
check status, (d) whether we've cloned it, (e) where the clone lives. Before writing any code, check
here + `external-tools.md` — if a solution exists, adopt it; don't rebuild it.*

---

## 1. The two-tier model (why we raid these)

```text
MATURE INFRASTRUCTURE (external-tools.md)   → adopt as dependency/contract
RESEARCHER ONE-OFFS (this file)             → strip for machinery/data/patterns, don't depend on them
```

We DON'T replace Pāṭala with these projects — Pāṭala has the stronger epistemic architecture
(L0, provenance, evidence-use, claim ceilings, argument reconstruction, review events, adjudication,
stable IDs, synthesis, education). We **strip-mine** them for solved subsystems.

---

## 2. The registry

> **Verified 2026-08-14:** darshana-graph (MIT, cloned), emptiness-graph (cloned), pramana-nlp (cloned)
> live at `/mnt/HC_Volume_106427611/patala-ingest/clones/`. The highest-value reusables are CONFIRMED:
> closed-vocabulary tagging (tag_corpus.py), the disagreement finder (embedding_disagreement_finder.py,
> needs no API key), and the relation taxonomies below.

### A. joyboseroy — the parallel evolutionary branch (highest value)

| Repo | What it is | Reusable | Status |
|---|---|---|---|
| **`joyboseroy/darshana-graph`** | text-grounded comparative Indian-philosophy graph (Vedānta/Nyāya/Vaiśeṣika/Sāṃkhya/Yoga/Jain + Buddhist) | **all source adapters/scrapers** (`scrape_*.py`, `convert_*.py` for Bilara/SuttaCentral/Gita/Sacred-texts/Wisdomlib/Müller/DJVU/Tattvārthasūtra/Nimbārka/Madhva); **closed-vocabulary candidate tagging** (`tag_corpus.py`: LLM tags from FIXED CONCEPT_CATEGORIES + RELATION_VOCAB + SCHOOL_VOCAB, rejects anything outside, with verbatim `evidence_quote` citation anchor — the exact candidate-generation discipline); **disagreement/tension finder** (`embedding_disagreement_finder.py`, sentence-transformers, no API key); `fix_duplicate_ids.py`; `inventory.py`; `audit_tagged.py`; tagged corpus (`corpus/tagged/*.jsonl`, HF-exported `hf_dataset/darshana_graph.jsonl`) | ✅ **CLONED** (MIT) + AUDITED |
| **`joyboseroy/darshana-temporal-analysis`** | temporal attribution, structural-homology, diachronic sense disambiguation, larger graph | diachronic sense machinery | ✅ **CLONED** (MIT, 28 MB) — audit for diachronic-sense pipeline |
| **`joyboseroy/vada-simulator`** | citation-grounded multi-agent debate simulator (schools as agents, **fabricated-citation rejection**) | **CONFIRMED** — `retriever.py` pulls edges by concept+school from the darshana-graph dataset with verbatim `evidence_quote`; `agents.py`, `contradiction_finder.py`. Citation-enforcement → education/argument layer | ✅ **CLONED** (MIT, 440 KB) + AUDITED |
| **`joyboseroy/emptiness-graph`** | hand-authored typed philosophical graph of emptiness (Theravāda/Prajñāpāramitā/Madhyamaka/Yogācāra) | **typed relation taxonomy — VERIFIED 16 edges:** `negates, refutes` (distinguished), `presupposes, implies→is_ground_of, is_identical_to, depends_on→enables, is_obstacle_to, is_antidote_to, extends, applies_method_of, deconstructs, tensions_with` (unresolved disagreement), `reframes_as, is_conventional_expression_of, is_ultimate_level_of, is_precursor_of`. Compare against our relation vocab; `tensions_with` = no forced reconciliation | ✅ **CLONED** + AUDITED (relation vocab) |

**The pattern to steal first:** closed-vocabulary candidate tagging (candidate-generation beneath our
stronger epistemic gates) + `tensions_with` (unresolved disagreement without forced reconciliation).

### B. Tyler Neill — pramāṇa & PANDiT lineage

| Repo | What it is | Reusable | Status |
|---|---|---|---|
| **`tylergneill/panditya`** | PANDiT relationship graph | **the PANDiT bulk export CSV** (already downloaded + snapshotted to R2); ETL/relationship extraction | ✅ USED (data), code under audit |
| **`tylergneill/pramana-nlp`** | Sanskrit pramāṇa corpus (GRETIL/SARIT/private) for computational analysis — Nyāya/Buddhist pramāṇa/epistemology/logic | **heterogeneous cleaning pipeline** (`transform.py` XSL daisy-chain, `validate_text.py`); **segmented corpus**; metadata spreadsheets; topic-model inputs | ✅ **CLONED** (882 MB corpus) + AUDIT (corpus feeds Pratyabhijñā argument work) |
| `vatayana.info` (related) | intertextuality search interface built on pramana-nlp | intertextuality/parallel-passage algorithms | trace + audit |

### C. Corpus/linguistic infrastructure

| Repo | What it is | Reusable | Status |
|---|---|---|---|
| **`ambuda-org/dcs`** | sanitized DCS dataset (650k+ annotated sentences, ~250 texts) | corpus-grounded linguistic priors | PLANNED (add to external-tools) |
| **`SriramKrishnan8/dcs_sh_alignment`** | align DCS ↔ Sanskrit Heritage analyses | cross-parser disagreement dataset → consensus/uncertainty layer | ✅ **CLONED** (GPL-3.0, 48 MB) — data requires external Google Drive downloads (not self-contained); usable as a pattern/reference |
| **`SriramKrishnan8/svarupa_alignment`** | align VedaWeb/DCS/Heritage/Samsaadhanii | multi-analyzer agreement matrix | CLONE + AUDIT |
| **`OliverHellwig/sanskrit`** | personal data for quantitative study of (Vedic) Sanskrit | derived corpora not in public DCS UI | ✅ **CLONED** (342 MB) — audit derived corpora |

### D. Buddhist/Tibetan corpus engineering

| Repo | What it is | Reusable | Status |
|---|---|---|---|
| **`xr843/fojin`** | 10,500+ Buddhist texts / 613 sources, trilingual cross-canon, RAG, KG | **how one dev normalized 613 sources** — a full-stack app (backend/frontend/Elasticsearch); mine `ARCHITECTURE.md` + `DECISIONS.md` + ingestion/workers for the source-registry + cross-canon + language-mapping patterns, NOT pluggable code | ✅ **CLONED** (Apache-2.0, 40 MB) — mine architecture patterns |
| **`Esukhia/derge-tengyur`** | Digital Derge Tengyur | page/folio anchoring, line numbering, normalized-vs-diplomatic, correction suggestions, TEI export, witness-preservation patterns | CLONE + AUDIT (manuscript witness model) |
| **`sinryo/buddha-cli`** (daizo-mcp) | Rust CLI + MCP for Buddhist text search | Buddhist MCP server pattern | inspect |

### E. Product/experiment precedents

| Repo | What it is | Reusable | Status |
|---|---|---|---|
| **`prx0r/blogengine`** | the sibling repo (prx0r) — Research Object lifecycle: content/authors/commentaries/factory/publishing/research | **the Research Object model + coverage/gaps/issues + source→affected-sections + RO→essay factory queue + acquire→impact→PR→version workflow.** The research says it already has ~half the paper-compiler (10/10 reuse). | **CLONE + AUDIT (reuse the RO lifecycle)** |
| **`prx0r/geometricengine`** | the sibling repo — hyperedge + typed incidences, episodes/transitions, feedback/preference events | **hyperedge representation** (ScholarContribution event), **SectionEpisode→DiscourseMove** argumentative flow, **feedback/PreferencePair** → adjudication/training data (9-10/10 reuse). Discard its reward/therapy ontology. | **CLONE + AUDIT (hyperedge + episode patterns)** |
| **`prx0r/Ochema`** | the sibling repo — synthesis/comparison/source-manuals/essay-AV representation | **output projection** only: Pāṭala structured scholarship → Ochema comparative synthesis → EssayViz → film/visual renderers. Never move its synthesis into canonical truth. | CLONE + AUDIT (projection only) |
| **`bhaskatripathi/graphGita`** | Bhagavad Gītā → knowledge graph + interpretation comparison | Compare-product UX/query ideas (same passage → many interpretations → agreement/conflict → graph nav) | mine UI ideas only |
| **`LABA-SNU/SocraticKG`** | QA-driven knowledge-graph construction (document → 5W1H self-contained QA → atomic triples → entity/relation canonicalization) | replace generic 5W1H with **Pāṭala scholarly-interrogator questions** → the commentarial-graph extraction (see `06-commentarial-graph.md`) | CLONE + AUDIT |

### G. The agentic-orchestration stack (peer-reviewed for the live system, Layer 12)

| Repo | What it is | Reusable | Status |
|---|---|---|---|
| **`alamops/agetor`** | local-first kanban for parallel CLI coding agents in git worktrees | **Task ≠ Run** — durable task identity vs reproducible runs pinned to base commit; approvals | ✅ **CLONED** (13 MB) + AUDITED |
| **`Dicklesworthstone/beads_rust`** | small reimplementation: SQLite=operational state, JSONL=git-readable projection, append-only events=audit, refuses to execute git | the "non-invasive" design — each subsystem does one thing | ✅ **CLONED** (290 MB) + AUDITED |
| **`Dicklesworthstone/beads_viewer`** | graph algorithms (PageRank/betweenness/critical-path/k-core) over the task dependency graph, robot-mode JSON output | **graph-aware triage** → `patala_next_action()` as a deterministic engine, not an LLM guess | ✅ **CLONED** (316 MB) + AUDITED |
| **`Dicklesworthstone/mcp_agent_mail`** | async coordination: agent identities, inboxes, threads, **advisory file leases** over FastMCP + Git + SQLite | **resource leases** (task ownership ≠ resource ownership); `patala_reserve_object()` | ✅ **CLONED** (23 MB) + AUDITED |
| **`gastownhall/gastown` + `gascity`** | multi-agent workspace manager + orchestration-builder SDK | persistent task identity, worktree isolation, role permissions; declarative workflows (Bead/Formula/Rig) | reference only |
| **`usemozzie/mozzie`** | local-first desktop orchestrating AI agents in parallel | **Attempt history** fed back into next run (negative epistemic knowledge) | reference |
| **`fynnfluegge/agtx`** | blackboard for coding agents | **`get_allowed_actions`** — orchestrator asks the state machine what transitions are legal | borrow structurally |
| `codingagentsystem/cas`, `charannyk06/conductor-oss`, `gannonh/kata`, `wshobson/agents`, `repowise-dev/repowise`, `mraza007/echovault` | assorted orchestration/context/memory builds | confirm patterns (Markdown=operator interface not runtime state; generated-artifact CI discipline; provenance-aware staleness) | reference |

### H. Knowledge-graph generation tools (text → graph — for the commentarial/organism layers)

> These convert arbitrary text/URLs → (entity, relation, entity) triples. Useful for the **candidate** layer
> beneath Pāṭala's epistemic gates (Layer 06 commentarial + Layer 09 organism) — never for canonical truth.
> All cloned 2026-08-14 to `/mnt/HC_Volume_106427611/patala-ingest/clones/`.

| Repo | What it is | Reusable | Status |
|---|---|---|---|
| **`yoheinakajima/instagraph`** (3.6k ⭐) | converts text OR a URL directly into a knowledge graph; LLM extracts (entity, relation, entity) triples + visualizes. **Best fit for point-at-content-get-a-graph.** | the URL→graph path (our info-phil content is scraped websites); triple extraction + display | ✅ CLONED (520K) — likely the best quick win for the commentarial candidate layer |
| **`iwe-org/seventeen-centuries`** (10 ⭐) | a philosophy knowledge graph (Marcus Aurelius → Nietzsche) via a **5-stage pipeline**: XHTML → fragments → LLM entity extraction → flatten/merge → categories → summaries. **Most domain-aligned.** | the 5-stage pipeline as a recipe for our exact task; **polyhierarchy** (a concept in multiple categories) matches how philosophy ideas interconnect | ✅ CLONED (6 MB) — closest to our domain |
| **`rahulnyk/knowledge_graph`** (3.6k ⭐) | "convert any text to a graph" — Jupyter-based, LLM triples, networkx | a clean, well-tested baseline | ✅ CLONED (49 MB) — good baseline |
| **`stair-lab/kg-gen`** (1.3k ⭐, NeurIPS '25) | Knowledge Graph Generation from Any Text — the most academically rigorous | best extraction quality; heavier; has an MCP server | ✅ CLONED (6.4 MB) — research-grade quality |
| **`varunshenoy/GraphGPT`** (4.4k ⭐) | extrapolates KGs from unstructured text with a nice UI | visual explorer / UI patterns | ✅ CLONED (8.2 MB) |
| **`dakshjain-1616/kg-extract`** (quick CLI) | PDF/MD/txt → triples → HTML/Cypher/JSON-LD | simple if text is already extracted; **Cypher/JSON-LD export** useful | ✅ CLONED (236K) — quick CLI |

**Review verdict:** these are **candidate-generation tools**, not epistemic infrastructure. For Pāṭala:
- **Best immediate fit:** `instagraph` (URL→graph, matches our scraped info-phil content) and
  `seventeen-centuries` (the philosophy-domain 5-stage pipeline + polyhierarchy).
- **Best quality:** `kg-gen` (research-grade) — but only where extraction quality justifies the weight.
- **Rule:** their output is `MACHINE_PROPOSED` candidate triples → reconciled through the epistemic core →
  reviewed. Never adopt their ontology or treat their graph as canonical (the `external_record.py` +
  `entity_reconciliation` + `reconcile` path already handles this).
- **Cypher/JSON-LD export** (kg-extract) is useful for interchange, not storage (Postgres stays canonical).
| **`mmehner/sanskrit-editing-suite`** | tiny Sanskrit critical-editing micro-tool | micro-tool candidate; verify implementation before adopting | next code-audit pile |

### F. OCR/student projects (experiment indexes, NOT foundations)

| Repo | Reusable |
|---|---|
| `Suyashkb/VedOCR`, `ari2612sarkar/ManuVision`, `NoiceHax/DivyaLipi-AI`, `Suganthi-23/Digitizing-Sanskrit-Manuscripts-using-OCR-and-Image-Processing`, `Samuela31/Sanskrit-Manuscripts-Revival-Using-Deep-Learning-Techniques`, `Sharzzz001/Sanskrit-OCR` | datasets found, preprocessing recipes, deskew/threshold combos, page-segmentation assumptions, handwriting samples, scripts tested, failure cases — experiment indexes for Gyan Bharat-scale OCR |

---

## 3. The immediate steal-list (ranked)

1. **darshana-graph closed-vocabulary candidate tagging** (`tag_corpus.py`) → **CONFIRMED** — adapt its
   FIXED-vocab + verbatim-`evidence_quote` discipline into Pāṭala's candidate-generation layer (beneath
   our stronger epistemic gates). MIT license → safe to reuse.
2. **darshana-graph `embedding_disagreement_finder.py`** → **CONFIRMED** — no-API-key cross-school
   disagreement detection; independent corroboration of the LLM graph.
3. **emptiness-graph typed relation taxonomy** → **CONFIRMED** (16 verified edges) — diff against our
   relation vocabulary; adopt `tensions_with` for unresolved disagreement.
4. **darshana-graph source adapters/scrapers** → `ingestion/adapters/` (after provenance check).
5. **pramana-nlp cleaning pipeline + segmented corpus** → pramāṇa/argument sources (882 MB cloned).
6. **vada-simulator citation-enforcement** → education/argument layer.
7. **fojin 613-source normalization** → Buddhist counterargument corpus.
8. **dcs_sh_alignment / svarupa_alignment** → multi-analyzer agreement/uncertainty.
9. **darshana-temporal-analysis diachronic sense** → term semantic trajectory.
10. **derge-tengyur witness patterns** → manuscript witness model.

---

## 3b. CLONE PLAN (which to clone next + why — 2026-08-14)

> Decision rule: clone if (a) it maps to a Pāṭala subsystem we'll need, (b) license permits reuse, (c)
> it's self-contained or the data is obtainable. Already cloned (see §2): darshana-graph,
> emptiness-graph, pramana-nlp, darshana-temporal-analysis, vada-simulator, dcs_sh_alignment, fojin,
> OliverHellwig/sanskrit. All live at `/mnt/HC_Volume_106427611/patala-ingest/clones/`.

| Repo | Clone? | Why | License | State |
|---|---|---|---|---|
| `xr843/fojin` | ✅ CLONE | 613-source Buddhist normalization — the counterargument corpus ingestion pattern | Apache-2.0 | ✅ CLONED (40 MB) |
| `Esukhia/derge-tengyur` | ✅ CLONE | witness model: folio/line anchoring, normalized-vs-diplomatic, correction, TEI export | check | ⚠️ PENDING (large; volume 7.1G free) |
| `OliverHellwig/sanskrit` | ✅ CLONE | derived Vedic corpora not in the public DCS UI | check | ✅ CLONED (342 MB) |
| `SriramKrishnan8/svarupa_alignment` | ⚠️ OPTIONAL | extends dcs_sh_alignment (VedaWeb/DCS/Heritage/Samsaadhanii) — GPL, data may be external | GPL-3.0 | not cloned |
| `bhaskatripathi/graphGita` | ⚠️ OPTIONAL | Compare-product UX/query ideas only | MIT | not cloned |
| `mmehner/sanskrit-editing-suite` | ⚠️ DEFER | tiny micro-tool; verify before adopt | Unlicense | not cloned |
| OCR projects (VedOCR, ManuVision, etc.) | ❌ DON'T CLONE | experiment indexes only — mine datasets/recipes, don't adopt | varies | n/a |
| `vatayana.info` | ❌ HOLD | intertextuality is downstream; trace similarity algorithms when we need it | n/a | n/a |

### I. The Layer-12 "organs" ecosystem (from the 15-plane review — see `docs/layers/12-live-system.md` §6c)

> The endgame: a stack of narrow systems around a small Pāṭala kernel. Pinch implementations, don't vendor.
> These are the organs Pāṭala's kernel composes.

| Repo | Plane | Pinch | Status |
|---|---|---|---|
| **`vouchdev/vouch`** | 3 review gating | proposal→mechanical validation→review→accepted canonical object; cited evidence; append-only audit; MCP | **CLONE + dissect (closest to the doctrine)** |
| **`jayminwest/overstory`** | 1 control | typed agent mail, merge queues, watchdog hierarchy, permission enforcement | CLONE + AUDIT |
| **`xoai/sage-wiki`** | 3 review gating | compiler model, alias resolution, fact→source citation, MCP retrieval, human-readable projection | CLONE + AUDIT |
| **`alfadur7/llm-wiki-newsroom`** | 3 review gating | the "reground" cycle (refresh published pages vs source — don't assume docs stay correct) | CLONE + AUDIT |
| **`ddsyasas/llm-wiki`** | 3 review gating | simple source→crosslinked-wiki compiler (code to read, not adopt) | reference |
| **`zotero/translation-server`** | 4 ingestion | resolve DOI/ISBN/PMID/arXiv, parse webpages, BibTeX/RIS, normalize metadata — "saves months" | CLONE + AUDIT |
| **`alisoroushmd/zotero-mcp`** | 5 bibliography | graph-analysis + integration over Zotero/OpenAlex/SemanticScholar | CLONE + AUDIT |
| **`diegodlh/zotero-cita`** | 5 bibliography | citation sync adapters (Wikidata/Crossref/SemanticScholar/OpenAlex), coauthorship networks | CLONE + AUDIT |
| **`HKUDS/DeepTutor`** | 9 consumer | L1/L2/L3 memory pipeline + KB version fingerprints (drift detection) | CLONE + AUDIT |
| **`MysterionRise/adaptive-knowledge-graph`** | 10 learner | **GOLD** — the interfaces between components: Neo4j prerequisite graph + OpenSearch + Ollama + SQLite learner state + BKT/IRT | CLONE + tear apart |
| **`epicenter-md/epicenter`** | 11 KG→docs | Markdown + DB as ONE truth (DB canonical, Markdown a view) — directly relevant to `project_state()` | CLONE + AUDIT |
| **`calesthio/OpenMontage`** | 13 media | **MAJOR** — agentic research→script→assets→editing, footage from Archive.org/NASA/Wikimedia, Remotion/FFmpeg. Don't build the video stack from scratch | CLONE + AUDIT |
| **`DojoCodingLabs/remotion-superpowers`** | 13 media | director/media-scout/post-production agent job defs + MCP | CLONE + AUDIT |
| **`frankxai/remotion-video`** | 13 media | Hermes/Claude + Remotion short-form video factory (Hermes-oriented) | CLONE + AUDIT |
| **`gitroomhq/postiz-agent`** | 14 distribution | turns Postiz operations into agent-friendly CLI workflows — the Hermes publishing lane calls it | CLONE + AUDIT |
| `Arize-ai/phoenix` / `langfuse/langfuse` | 12 observability | OpenTelemetry agent/LLM tracing + eval (external trace plane; Pāṭala review stays internal) | reference |
| `gitroomhq/postiz-app` | 14 distribution | scheduling/analytics/multi-platform publishing + public API | reference |
| `ProjectMirador/mirador` + `dbmdz/mirador-textoverlay` | 6 manuscripts | IIIF viewer + OCR/transcription overlay — embed, don't build | reference (in external-tools) |
| `CoWork-OS/CoWork-OS` | 9 consumer | SQLite entity/relationship memory, temporal edges, as_of querying, confidence decay | CLONE + AUDIT |
| `sqliteai/sqlite-sync` + `sqlite-memory` | 11 KG→docs | CRDT-backed SQLite replicas for offline scholars (LATER, not now) | reference (later) |
| `SoloJiang/weft` | 1 control | remote agent questions, sidecar observation, skills mgmt | study |

### J. The "adapters around a kernel" full-stack map (from patalagithubs — see `docs-cache/patalagithubs.md`)

> The architectural conclusion: Pāṭala = a small typed epistemic kernel + compiler, surrounded by
> adapters around world-class existing infra. DON'T BUILD generic OCR/UI/TEI/ID/Sanskrit/provenance/
> schema/scheduler. These are the "never rebuild" substrate.

| Repo / project | Substrate it serves | Pinch / use | Status |
|---|---|---|---|
| **`mittagessen/kraken`** | OCR/HTR substrate | historical-document OCR for non-Latin scripts; ALTO/PageXML/hOCR; trainable layout. **Default OCR, don't rebuild.** | CLONE + AUDIT |
| **`UB-Mannheim/escriptorium`** | OCR/HTR UI | research UI around Kraken (transcription, annotation, model training). Don't build the transcription UI. | INTEGRATE |
| **`ayushbits/pe-ocr-sanskrit`** | OCR eval | Sanskrit post-OCR correction benchmark → `OCRProofBenchmark`. **Ingest now.** | INGEST benchmark |
| **Saktumiva** (`saktumiva.org`) | text criticism | Sanskrit critical-edition collation (witness→variant→editorial-decision). **Reverse-engineer its object model before building.** | STUDY + AUDIT |
| **SARIT** (`sarit.github.io`) | Indic TEI | the Indic TEI encoding conventions target (Pāṭala IR → TEI adapter → SARIT-compatible export). | TEI target |
| **`annotation/text-fabric`** | textual substrate | annotated-graph text corpora; stable text-position primitive + annotation layers. **GENIUS — the L0 substrate model.** | CLONE + STUDY DEEP |
| **CapiTainS / CTS** (`capitains.org`) | passage identity | citable text/passage IDs (CTS URN). Adopt the citation semantics, not the server stack. | crosswalk |
| **`ambuda-org/vidyut`** | Sanskrit mechanics | the deterministic Sanskrit kernel (morphology/normalization/lexical). Already INTEGRATED. | ✅ built |
| **`BetaMasaheft`** | comparative architecture | Ethiopian/Eritrean manuscript infra (TEI, witnesses, CollateX) — steal institutional lessons, not ontology. | study |
| **`CreativeCodingLab/TextAnnotationGraphs`** | annotation | semantic hypergraph annotations (relationships participate in relationships) — for argument annotation UI. | study |
| **`mntlra/knowledgeProvenance`** | provenance | multi-source assertions + supports/refutes/trust (extends nanopub) — **very strong fit** for evidence model | CLONE + AUDIT |
| **nanopub.net** | provenance | outward standard — Pāṭala ScholarlyObject → compile → nanopublication (NOT canonical ontology) | standard |
| **`sensein/assertion-evidence-paper`** | provenance vocab | survey comparing provenance/assertion/evidence ontologies — the ontology agent should ingest | ingest |
| **Eigenius** (`arxiv 2608.04457`) | epistemic substrate | typed KG DBMS with structural epistemic status (Declared/Observed/Derived/Verified) — pinch the distinction, not the DBMS | study |
| **`stencila/stencila`** | schema compilation | canonical YAML schema → compiled TS/Python/Rust/JSON-LD/JSON-Schema + C2PA signed provenance. **THE schema-drift answer.** | CLONE + STUDY |
| **`gallantlab/literature-review-toolkit`** | bibliography | agent-judgment vs mechanical-verification separation; citation verification. **Very high priority clone.** | CLONE + AUDIT |
| **`bricee98/Valsci`** | claim verification | claim → literature search → support/contradiction report pipeline | study |
| **`romain-girardi-eng/EleutherIA`** | argument layer | ~69k passages / 19k KG nodes, CTS IDs, dual-layer graph (primary-source vs modern-reception). Nearest neighbouring vertical. | CLONE + STUDY |
| **canonical-debate-lab** (debatemap.app) | argument map | decade-long argument-map obsession — claim identity, argument threading, UI. Mine, don't adopt. | study |
| **`maps.simoncullen.org`** (Because) | argument UI | argument visualization pedagogy — help users THINK with arguments, not just display | study |
| **`simonw/datasette`** | read plane | immutable SQLite → automatic website + JSON API. The "stupidly simple fast read-plane" principle. | study |
| **`simonw/research`** | agent method | agents investigating questions → executable research commits. A method, not a library. | study |
| **`ResearchObject/ro-crate`** | publication | portable scholarly-object packaging (JSON-LD). **First-class export target** (`Pāṭala Scholarly Release`). | export target |
| **`datalad/datalad-catalog`** | publication | dataset publication separate from ownership — reinforces the compiler architecture | study |
| **`nagisanzenin/engram`** | education | **frighteningly close to the education vision**: knowledge-dependency graph, predict→act→explain, blind grading, FSRS, receipts-not-enthusiasm. **Red-circle + clone before building more education infra.** | CLONE + AUDIT |
| **`ktaletsk/learn-codebase`** | education | Socratic questioning + active recall + mastery journal. "Explanation is not proof of understanding." | CLONE + AUDIT |
| **`lfnovo/open-cognition`** | education | Socratic LLM + KG + Feynman + spaced repetition + MCP — the MCP+learning-graph boundary | study |
| **`SYuan03/Skill-Anything`** | education | arbitrary source → study package (concept map/guide/quizzes/flashcards) — the **compiler mentality** | study |
| **`studyield/studyield`** | education | KG + teach-back eval + learning paths + SRS — mine teach-back UX + mastery dashboard | study |
| **`arturseo-geo/llm-knowledge-base`** | education | KG + learning layer + **gap tracker** — UNKNOWN should be a first-class object | study |

**The "don't build" boundary (from this review):** generic OCR (→Kraken) · OCR UI (→eScriptorium) ·
Indic TEI (→SARIT) · passage IDs (→CTS) · Sanskrit mechanics (→Vidyut) · critical-edition concepts (→Saktumiva) ·
research package (→RO-Crate) · provenance export (→nanopub/PROV-K) · document schema (→Stencila) · learning
scheduler (→FSRS). **Pāṭala's moat = the typed epistemic kernel + compiler**: source-grounded proposition
identity, translation-proof lineage, argument reconstruction, semantic-strength ceilings, crux propagation,
scholar adjudication, cross-object dependency, education-from-verified-structure.

### K. The translation subsystem (from patalatranslate — see `docs-cache/patalatranslate.md`)

> The frontier idea: **a translation can't be proven equivalent to source, but it CAN be made
> proof-carrying** — every translation ships a bundle showing what Sanskrit was read, how it was parsed,
> which target spans realize which source obligations, what couldn't be verified, what alternatives
> exist, and which independent checks/reviewers passed it. Stronger than a COMET score.

| Project | What it gives | Pinch / use | Status |
|---|---|---|---|
| **Mitrasamgraha** (`arxiv 2601.07314`) | 391k Sanskrit-EN bitext + post-corrected gold → **Pāṭala Translation Benchmark** (temporal/genre/philosophical/poetry slices) + **error families** (compound loss, scope loss, negation loss...) → Pāṭala validators | INGEST benchmark + error-family validators | INGEST now |
| **MITRA / `dharmamitra/mitra-parallel`** | 1.74M Sanskrit↔Tibetan↔Chinese parallel pairs + domain models → cross-source translation verification (S↔T↔C as independent checks) | cross-source verification | INGEST |
| **`xr843/fojin`** (Buddhist digital platform) | the best personal translation-adjacent project — cross-canon normalization | CLONE + STUDY (already tracked) | CLONE |
| **ByT5-Sanskrit** | one of the **proof generators** (segmentation/morphology/tagging + OCR post-corr) | proof generator | INGEST |
| **Sanskrit Heritage** (`hrishikeshrt/heritage`) | keep the old Sanskrit-parsing machinery | reference | reference |
| **`tylergneill/skrutable`** | tiny Sanskrit text tool | reference | study |
| **`OliverHellwig/sanskrit`** | quiet goldmine (derived Vedic corpora) | reference (already cloned) | CLONE |
| **xCOMET / `Unbabel/COMET`** | the MT audit frontier — general eval | study | study |
| **MetricX-25 + GemSpanEval** (`google-research/mt-metrics-eval`) | Google's 2025 frontier | study | study |
| **OTTAWA** | omission/addition problem | study | study |
| **`neulab/awesome-align`** | word/span alignment | study | study |
| **`bfsujason/bertalign`** | sentence alignment | study | study |
| **`google/wmt-mqm-human-evaluation`** | MQM error vocabulary → the Pāṭala translation error taxonomy | adopt vocabulary | study |
| **`langtech-bsc/mt-evaluation`** + `bsc-lt/mt-evaluation` (MT-Lens) | don't build the metric harness from scratch | reuse | study |
| **`amazon-science/span-mt-metaeval`** | span meta-evaluation toolkit | reuse | study |
| **`ayushbits/saamayik`** | Sanskrit poetry — useful, don't confuse with classical | reference | study |
| **`AI4Bharat/IndicTrans2`** + `IndicLLMSuite` | baseline (not scholarly translator) + a human-audit pipeline worth stealing | baseline + audit pipeline | study |
| **`dharmamitra/heritage`** / ByT5 / Vidyut | the Sanskrit deterministic proof-generator stack | compose | reference |

**The key architecture (don't go Sanskrit→English directly):** translation needs its own **intermediate
representation** + a **`TranslationProof` first-class object** (`source_identity · source_analysis ·
alignment · semantic_obligations [negation/modality/scope] · unverified · alternatives · checks`) — with
**no single aggregate score**, intentionally redundant independent auditors, and **bi-directional
entailment** as a Pāṭala test.

## 4. Next sweep (how to find more)

Traverse the **GitHub accounts, forks, citations and dependencies** of: Neill, Bose Roy, Hellwig,
Sriram Krishnan, and similar computational-Indology researchers. Don't search `"Sanskrit NLP"` — follow
the people.

---

*Keep this registry updated as repos are cloned, audited, and absorbed. Every entry needs a license +
provenance check before code is pulled into `ingestion/adapters/` or the epistemic core.*
