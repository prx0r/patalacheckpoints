# PĀṬALA — THE COMPLETE EXTERNAL REPOSITORY MAP (every repo → layer/product · what to pinch · status)

*2026-08-14 · status: THE AUTHORITATIVE EXTERNAL REPO REGISTRY · companion to `EXTERNAL-EVIDENCE.md`
(the layer-level grounding) + `docs/process/githubclones.md` + `docs/process/external-tools.md` + the
`source-evidence/docs/tools/docs-cache/` research. This consolidates EVERY external GitHub repo Pāṭala
has researched into ONE place mapped to the v2 layer/product it serves, with what to pinch vs own, and
the clone/ingest/study status.*
*The two-tier model: **mature infra** (external-tools.md) → adopt as dependency/contract; **researcher
one-offs** (githubclones.md) → strip for machinery/data/patterns, don't depend on them.*
*The governing rule: Pāṭala has the STRONGER epistemic architecture (provenance, evidence-use, review
events, argument reconstruction, stable IDs, synthesis, education). We STRIP-MINE external repos for
solved subsystems — never replace Pāṭala's kernel with them.*

---

## THE COMPLETE REPO LANDSCAPE (mapped to v2)

### TRANSLATION SUBSYSTEM (Layer 05 — the user's focus) — *[githubclones.md §K, patalatranslate.md]*

> The frontier: **a translation can't be proven equivalent to source, but it CAN be made proof-carrying.**
> Stronger than a COMET score.

| Repo / resource | What it gives | Pinch / use | Status |
|---|---|---|---|
| **Mitrasamgraha** (`arxiv 2601.07314`) | 391k Sanskrit-EN bitext + post-corrected gold → **Pāṭala Translation Benchmark** + **error families** (compound loss, scope loss, negation loss) → Pāṭala validators | INGEST benchmark + validators | INGEST now |
| **`dharmamitra/mitra-parallel`** (MITRA) | 1.74M Sanskrit↔Tibetan↔Chinese parallel pairs → **cross-source translation verification** (S↔T↔C as independent checks) | cross-source verification | INGEST |
| **`xr843/fojin`** | 10,500+ Buddhist texts / 613 sources, trilingual cross-canon, RAG, KG — the best personal translation-adjacent project | CLONE + STUDY: mine `ARCHITECTURE.md` + `DECISIONS.md` + ingestion/workers for source-registry + cross-canon + language-mapping patterns | ✅ CLONED (Apache-2.0, 40 MB) |
| **ByT5-Sanskrit** | a **proof generator** (segmentation/morphology/tagging + OCR post-corr) | proof generator | INGEST |
| **`ambuda-org/vidyut`** | the deterministic Sanskrit kernel (morphology/normalization/lexical) | ✅ already INTEGRATED | built |
| **`hrishikeshrt/heritage`** (Sanskrit Heritage) | old Sanskrit-parsing machinery | reference | reference |
| **`tylergneill/skrutable`** | tiny Sanskrit text tool | reference | study |
| **`OliverHellwig/sanskrit`** | quiet goldmine (derived Vedic corpora) | reference | ✅ CLONED (342 MB) |
| **`Unbabel/COMET`** (xCOMET) | the MT audit frontier — general eval | study | study |
| **`google-research/mt-metrics-eval`** (MetricX-25, GemSpanEval) | Google's 2025 frontier | study | study |
| **OTTAWA** | omission/addition problem | study | study |
| **`neulab/awesome-align`** | word/span alignment | study | study |
| **`bfsujason/bertalign`** | sentence alignment | study | study |
| **`google/wmt-mqm-human-evaluation`** | MQM error vocabulary → the **Pāṭala translation error taxonomy** | adopt vocabulary | study |
| **`langtech-bsc/mt-evaluation`** + `bsc-lt/mt-evaluation` (MT-Lens) | don't build the metric harness from scratch | reuse | study |
| **`amazon-science/span-mt-metaeval`** | span meta-evaluation toolkit | reuse | study |
| **`ayushbits/saamayik`** | Sanskrit poetry (don't confuse with classical) | reference | study |
| **`AI4Bharat/IndicTrans2`** + `IndicLLMSuite` | baseline (not scholarly) + a human-audit pipeline | baseline + audit pipeline | study |

**The translation architecture (don't go Sanskrit→English directly):** an **intermediate representation**
+ a **`TranslationProof` first-class object** (`source_identity · source_analysis · alignment ·
semantic_obligations [negation/modality/scope] · unverified · alternatives · checks`) with **no single
aggregate score**, redundant independent auditors, and **bi-directional entailment** as a Pāṭala test.

---

### CORPUS / LINGUISTIC INFRASTRUCTURE (Layer 01/02) — *[githubclones.md §C, §D]*

| Repo | What it gives | Status |
|---|---|---|
| **`ambuda-org/dcs`** | 650k+ annotated sentences, ~250 texts (sanitized DCS) | PLANNED |
| **`SriramKrishnan8/dcs_sh_alignment`** | align DCS ↔ Sanskrit Heritage → consensus/uncertainty layer | ✅ CLONED (GPL-3.0) |
| **`SriramKrishnan8/svarupa_alignment`** | multi-analyzer agreement matrix | CLONE + AUDIT |
| **`OliverHellwig/sanskrit`** | derived Vedic corpora | ✅ CLONED |
| **`xr843/fojin`** | 613-source normalization, cross-canon, language mapping | ✅ CLONED |
| **`Esukhia/derge-tengyur`** | witness model: folio/line anchoring, normalized-vs-diplomatic, TEI | CLONE (pending, large) |
| **`annotation/text-fabric`** | **GENIUS — the L0 substrate model** (stable text-position primitive + annotation layers) | CLONE + STUDY DEEP |
| **`ambuda-org/vidyut`** | the Sanskrit deterministic kernel | ✅ built |

### OCR / MANUSCRIPTS (Layer 02) — *[githubclones.md §F, §J]*

| Repo | What it gives | Status |
|---|---|---|
| **`mittagessen/kraken`** | historical-document OCR for non-Latin scripts; trainable layout — **default OCR** | CLONE + AUDIT |
| **`UB-Mannheim/escriptorium`** | research UI around Kraken | INTEGRATE |
| **`ayushbits/pe-ocr-sanskrit`** | Sanskrit post-OCR correction benchmark → `OCRProofBenchmark` | INGEST now |
| **Saktumiva** (`saktumiva.org`) | Sanskrit critical-edition collation — reverse-engineer its object model | STUDY + AUDIT |
| OCR student projects (VedOCR, ManuVision, etc.) | datasets/recipes/failure-cases only | MINE, don't adopt |

### SCHOLARLY DISCOVERY / BIBLIOGRAPHY (Layer 02) — *[ecosystem-15planes.md §5]*

| Repo | What it gives | Status |
|---|---|---|
| **`alisoroushmd/zotero-mcp`** | graph-analysis + integration over Zotero/OpenAlex/SemanticScholar | CLONE + AUDIT |
| **`diegodlh/zotero-cita`** | citation sync adapters + coauthorship networks | CLONE + AUDIT |
| **`gallantlab/literature-review-toolkit`** | agent-judgment vs mechanical-verification separation; citation verification | **very high priority CLONE** |
| **`bricee98/Valsci`** | claim → literature search → support/contradiction report | study |

### ARGUMENT / PHILOSOPHY ENGINE (Layer 06) — *[ecosystem-15planes.md §7-8, githubclones.md §J]*

| Repo | What it gives | Status |
|---|---|---|
| **`romain-girardi-eng/EleutherIA`** | ~69k passages / 19k KG nodes, CTS IDs, dual-layer graph — **nearest neighbouring vertical** | CLONE + STUDY |
| **ASPIC+ / py-aspic** | structured argumentation semantics | PINCH (via `aspic_adapter.py`) |
| **`aif-arg-datasets` / `oAMF`** | AIF/xAIF argument interchange | PINCH (adapters) |
| **`LiyingCheng95/IAM`** | argument-mining decomposition | PINCH |
| **`sensein/assertion-evidence-paper`** | provenance/assertion/evidence ontology survey | ingest |
| **canonical-debate-lab** / `maps.simoncullen.org` | argument-map claim identity + UX | MINE, don't adopt |
| **`mntlra/knowledgeProvenance`** | multi-source assertions + supports/refutes/trust — **very strong fit** for the evidence model | CLONE + AUDIT |

### VERIFICATION / CLAIM-CHECKING (Layer 07) — *[ecosystem-15planes.md §8]*

| Repo | What it gives | Status |
|---|---|---|
| **`anthonywchen/RARR`** | retrieve→check→revise | PINCH (in the ensemble) |
| **`amazon-science/RefChecker`** | atomic-claim checking | PINCH |
| **`Yingjian-Chen/GraphCheck`** | relationship-structure checking | PINCH |
| **`stanfordnlp/dspy`** | optimize against Pāṭala gold | PINCH |
| **`shmsw25/factscore`** · **`TIGER-AI-Lab/StructEval`** · **`zjunlp/SciAtlas`** · **`opendatalab/CiteVQA`** | claim/citation verification | study |

### REVIEW GATING / KNOWLEDGE (Layer 06/08) — *[ecosystem-15planes.md §3]*

| Repo | What it gives | Status |
|---|---|---|
| **`vouchdev/vouch`** | proposal→validation→review→accept; cited evidence; append-only audit — **closest to the doctrine** | CLONE + dissect |
| **`xoai/sage-wiki`** | compiler model, fact→source citation, human-readable projection | CLONE + AUDIT |
| **`alfadur7/llm-wiki-newsroom`** | the "reground" cycle | CLONE + AUDIT |

### THE AGENT-ORCHESTRATION STACK (Layer 12) — *[ecosystem-15planes.md §1-2, githubclones.md §G]*

| Repo | What it gives | Status |
|---|---|---|
| **`nousresearch/hermes-agent`** | the execution plane (kanban, profiles, skills, sessions) | ✅ USE |
| **`alamops/agetor`** | Task≠Run, pinned base commit | ✅ CLONED + AUDITED |
| **`Dicklesworthstone/beads_rust`** | "non-invasive" design (SQLite state / JSONL projection / append-only audit) | ✅ CLONED + AUDITED |
| **`Dicklesworthstone/beads_viewer`** | graph triage (PageRank/betweenness) → `patala_next_action()` | ✅ CLONED + AUDITED |
| **`Dicklesworthstone/mcp_agent_mail`** | resource leases (`patala_reserve_object()`) | ✅ CLONED + AUDITED |
| **`gastownhall/gastown` + `gascity`** | declarative workflows, worktree isolation, role permissions | reference |
| **`usemozzie/mozzie`** | attempt history → negative epistemic knowledge | reference |
| **`fynnfluegge/agtx`** | `get_allowed_actions` state-machine transitions | borrow |
| **`jayminwest/overstory`** | typed agent mail, merge queues, watchdog | CLONE + AUDIT |
| **`SoloJiang/weft`** | remote questions, sidecar observation | study |

### KNOWLEDGE-GRAPH GENERATION (Layer 06/09 candidate layer) — *[githubclones.md §H]*

| Repo | What it gives | Status |
|---|---|---|
| **`yoheinakajima/instagraph`** | URL→graph (matches scraped content) — **best quick win** | ✅ CLONED |
| **`iwe-org/seventeen-centuries`** | the philosophy 5-stage pipeline + **polyhierarchy** — **closest to domain** | ✅ CLONED |
| **`rahulnyk/knowledge_graph`** | clean baseline | ✅ CLONED |
| **`stair-lab/kg-gen`** | research-grade quality (NeurIPS '25) | ✅ CLONED |
| **`varunshenoy/GraphGPT`** | visual explorer UI | ✅ CLONED |
| **`dakshjain-1616/kg-extract`** | Cypher/JSON-LD export | ✅ CLONED |

**Rule:** their output = `MACHINE_PROPOSED` candidate triples → reconciled through the epistemic core →
reviewed. Never adopt their ontology as canonical.

### CONSUMER TEMPORAL GRAPH (Layer 09) — *[ecosystem-15planes.md §9]*

| Repo | What it gives | Status |
|---|---|---|
| **`getzep/graphiti`** | temporal facts + episode provenance (as a PROJECTION, not canonical) | PINCH |
| **`CoWork-OS/CoWork-OS`** | entity/relationship memory, temporal edges, as_of, confidence decay | CLONE + AUDIT |
| **`HKUDS/DeepTutor`** | L1/L2/L3 memory + KB version fingerprints | CLONE + AUDIT |

### LEARNER MODEL / EDUCATION (Layer 07) — *[ecosystem-15planes.md §10, githubclones.md §J]*

| Repo | What it gives | Status |
|---|---|---|
| **`nagisanzenin/engram`** | **frighteningly close to the education vision** (knowledge-dependency graph, predict→act→explain, blind grading, FSRS) | **red-circle + CLONE before building more** |
| **`MysterionRise/adaptive-knowledge-graph`** | **GOLD** — the interfaces (Neo4j prerequisites + learner state + BKT/IRT) | CLONE + tear apart |
| **`CAHLR/pyBKT`** | interpretable mastery state | PINCH |
| **`umass-ml4ed/dialogue-kt`** | tutor/student dialogue KT | PINCH |
| **`CAHLR/OATutor`** · **`zijinz456/OpenTutor`** | BKT adaptive tutor UX | PINCH/CLONE |
| **`ktaletsk/learn-codebase`** | Socratic questioning + active recall ("explanation is not proof") | CLONE + AUDIT |
| **`lfnovo/open-cognition`** | Socratic LLM + KG + Feynman + SRS | study |
| **`SYuan03/Skill-Anything`** | source → study package (the compiler mentality) | study |
| **`studyield/studyield`** | KG + teach-back + SRS | study |
| **`arturseo-geo/llm-knowledge-base`** | gap tracker (UNKNOWN as first-class) | study |
| **FSRS** | the learning scheduler | adopt (don't build) |

### MEDIA / DISTRIBUTION (Layer 10) — *[ecosystem-15planes.md §13-14]*

| Repo | What it gives | Status |
|---|---|---|
| **`calesthio/OpenMontage`** | **MAJOR** — agentic research→script→assets→editing | CLONE + AUDIT |
| **`DojoCodingLabs/remotion-superpowers`** | director/media-scout/post-production job defs | CLONE + AUDIT |
| **`frankxai/remotion-video`** | Hermes + Remotion short-form video | CLONE + AUDIT |
| **`gitroomhq/postiz-agent`** | the Hermes publishing lane | CLONE + AUDIT |

### PUBLICATION / INTEROP (Layer 04) — *[githubclones.md §J]*

| Repo | What it gives | Status |
|---|---|---|
| **`ResearchObject/ro-crate`** | portable scholarly-object packaging — **first-class export target** | export target |
| **`stencila/stencila`** | canonical YAML schema → compiled TS/Python/Rust/JSON-Schema + C2PA — **THE schema-drift answer** | CLONE + STUDY |
| **SARIT** (Indic TEI) | the TEI encoding target | TEI target |
| **CapiTainS / CTS** | citable passage IDs (CTS URN) | crosswalk |
| **nanopub.net** | provenance export (NOT canonical ontology) | standard |
| **Eigenius** (`arxiv 2608.04457`) | typed KG with structural epistemic status — pinch the distinction | study |
| **`simonw/datasette`** | immutable SQLite → website/API ("stupidly simple fast read-plane") | study |

---

## THE "DON'T BUILD" BOUNDARY (what Pāṭala must NOT build — external already solves it)

```
generic OCR            → Kraken
OCR UI                 → eScriptorium
Indic TEI              → SARIT
passage IDs            → CTS
Sanskrit mechanics     → Vidyut
critical-edition       → Saktumiva
research package       → RO-Crate
provenance export      → nanopub / PROV-K
document schema        → Stencila
learning scheduler     → FSRS
manuscript rendering   → Mirador 4
generic agent sched    → Hermes / Agetor
generic trace obs      → Phoenix / Langfuse
social upload          → Postiz
BKT itself             → pyBKT
annotation widgets     → Recogito / INCEpTION
generic citation scrape → Zotero / Crossref / OpenAlex
```

---

## WHAT PĀṬALA MUST ITSELF OWN (the moat — the typed epistemic kernel + compiler)

```text
source-grounded proposition identity      ← the core
translation-proof lineage                  ← the differentiator (L200)
argument reconstruction                    ← CP4
semantic-strength ceilings                 ← the epistemic gate
crux propagation                           ← the crux primitive
scholar adjudication                       ← the human gate
cross-object dependency                    ← the derivation graph
education-from-verified-structure          ← the lesson layer
```

---

*This is the complete external repository map. Every repo Pāṭala has researched is mapped to the v2
layer/product it serves, with what to pinch vs own and the status. The translation subsystem (fojin,
MITRA, Mitrasamgraha, ByT5, COMET, MT-metrics) is the deepest-researched — it directly grounds the
TranslationProof moat. The full fetched research lives in `source-evidence/docs/tools/docs-cache/`.*
