# PĀṬALA — DOCS INDEX (the single source of truth)

*2026-08-12. The one place to find the CURRENT authoritative document for each concern. The repo
accumulated overlapping handovers and specs; this index names the canonical one per topic and flags
stale ones as `[ARCHIVED]` so a new agent is never confused. If it's not here, it's not canonical.*

---

## How to read this

- **CANONICAL** = the one to read/trust for that concern.
- **[ARCHIVED]** = superseded; kept for history only, do not follow.
- The project has two sibling knowledge homes, by design:
  - **This repo (`/root/projects/patala`)** — the site/app: data model, API, reader, MCP, ML strategy.
  - **Sanskritree** (`/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/specs/`) — the
    scholarly factory specs + `THE_COMPANION.md` (the full-system onboarding).

---

## The canonical index

| Concern | Canonical doc | Where |
|---|---|---|
| **Onboarding (START HERE — single on-ramp, all agents)** | `onboarding/README.md` | repo `onboarding/` |
| **Agent system (who + tracked progress)** | `handover/SYSTEM.md` (template `agent0` → live instances) + `handover/flow.py status` | repo `handover/` |
| **Vision + navigation (START HERE)** | `VISION_AND_NAVIGATION.md` | repo root |
| **THE CORE BIBLE (top-level vision map)** | `docs/vision/CORE-BIBLE.md` | repo `docs/vision/` |
| **Full-system onboarding** | `THE_COMPANION.md` | sanskritree `_stack/ipvv/specs/` |
| **Handover folder (both lanes — README first)** | `handover/README.md` | repo `handover/` |
| **Cross-lane coordination log** | `handover/LOG.md` | repo `handover/` |
| **THE GOVERNING RULE — read first** | `AGENTS.md` + `machinelearning/_ACTIVE/AGENTS-DOCTRINE.md` | repo root |
| **Dual-agent vision + checkpoint map** | `machinelearning/_ACTIVE/dualagentvision.md` + `dualagentvision-ADAPTED.md` | repo `machinelearning/` |
| **The project's self-audit ledger** | `machinelearning/_ACTIVE/CLAIMS.md` | repo `machinelearning/` |
| **Anti-theatre component contracts** | `machinelearning/_ACTIVE/COMPONENT-CONTRACTS.md` | repo `machinelearning/` |
| **Agent 1 — ML lane (current state)** | `handover/agent-1-ml/INDEX.md` | repo `handover/` |
| **External standards alignment (SEPIO/xAIF/nanopub/SPARE/SCL — deferred roadmap)** | `docs/integrations/ARGUMENT-EVIDENCE-STANDARDS-ALIGNMENT.md` | repo `docs/integrations/` |
| **Global state checkpoint (2026-08-13, ELAD handover — timestamped, stale by design)** | `docs/global/GLOBAL-STATE-2026-08-13.md` | repo `docs/global/` |
| **Pāṭala Global Architecture v0.1 (THE definitive architecture — the one answer to "what are we building?")** | `docs/global/PATALA-GLOBAL-ARCHITECTURE.md` | repo `docs/global/` |
| **Global architectural files home (both agents read at orientation)** | `docs/global/README.md` | repo `docs/global/` |
| **Pāṭala Review vertical (synthesis → EO → essay → SentenceEvidenceAudit — Agent 1, frozen)** | `machinelearning/_ACTIVE/CURRENT-STATE-ARGUMENT-LAYER.md` + `handover/agent-1-ml/NEXT-STEPS.md` (rev 6) | repo `machinelearning/` |
| **P-019 v2 deterministic structural clustering (k-core) + Louvain stability ablation** | `benchmarks/v0/structural/{kcore-ipvv-c1-v0,louvain-stability-ipvv-c1-v0}.json` | repo `benchmarks/v0/structural/` |
| **Agent 1 closeout checkpoint (red-team review of the vertical — 2026-08-13)** | `handover/agent-1-ml/AGENT1-CHECKPOINT-2026-08-13.md` | repo `handover/` |
| **Source-Evidence substrate (S0) — the scholar corpus as the corroboration oracle** | `source-evidence/` (`schema/source_evidence_profile.py`, `registry.py`, `ro_crate.py`, `pilot.py`) | repo `source-evidence/` |
| **Source-Evidence guiding docs (schema-stack + evaluation/IDs + reuse-first)** | `source-evidence/docs/{scholar-layer-schema-stack,scholar-layer-evaluation-and-ids,reuse-first-stack}.md` | repo `source-evidence/docs/` |
| **External-tool integration docs (GROBID/Zotero/OpenAlex/Crossref/OpenCitations/RO-Crate/ORKG/OpenReview)** | `source-evidence/docs/tools/` | repo `source-evidence/docs/tools/` |
| **Agent 2 — integration lane (current state)** | `handover/agent-2-integration/INDEX.md` | repo `handover/` |
| **L0 standardization (NEXT WORK — verifiable substrate)** | `machinelearning/_ARCHIVE/SPEC_L0_STANDARDIZATION.md` | repo `machinelearning/` |
| **ML strategy (frozen)** | `machinelearning/_ACTIVE/MLUSEINPATALA.md` | repo `machinelearning/` |
| **ML dev plan** | `machinelearning/_ACTIVE/DEVPLAN.md` | repo `machinelearning/` |
| **ML vision (big picture)** | `machinelearning/_ARCHIVE/MLVISION.md` | repo `machinelearning/` |
| **IPVV stack integration (verified)** | `machinelearning/_ARCHIVE/IPVV-STACK-INTEGRATION.md` | repo `machinelearning/` |
| **Source-centric hub (organizing model)** | `machinelearning/_ARCHIVE/COMPOUNDING_RESEARCH_SYSTEM.md` | repo `machinelearning/` |
| **PUSHING method (deep-dive formula)** | `machinelearning/_ARCHIVE/SPEC_PUSHING_METHOD.md` | repo `machinelearning/` |
| **Logical arguments (the gold)** | `machinelearning/_ARCHIVE/SPEC_LOGICAL_ARGUMENTS_GOLD.md` | repo `machinelearning/` |
| **Argument truth-packet (strength-graded)** | `machinelearning/SPEC_ARGUMENT_TRUTH_PACKET.md` | repo `machinelearning/` |
| **PUSHING guide (the formal method)** | `research-library/pushing/PUSHING_GUIDE.md` | research-library |
| **Logicvid source files** | `research-library/pushing/_source/` | research-library |
| **Corpus build (Phase 1)** | `docs/PHASE1_IPVV_CORPUS_PROCESS_NOTES.md` | repo `docs/` |
| **Corpus targets (master index)** | `docs/corpus/TARGETS-INDEX.md` | the consolidated translation-target/lead/source goldmine (DB + links) |
| **Autonomous factory — current state** | `handover/agent-2-integration/PROGRESS-AUTONOMOUS-2026-08-12.md` | VERIFIED / CLOSE-unverified / STILL-NEEDED + file map + agent-1 scholarly-oracle handover (the autonomous RAW-L0 → L200 → C1 build) |
| **Autonomy build record** | `handover/agent-2-integration/BUILD-RECORD-2026-08-12-AUTONOMY.md` | full inventory + results of the controller / registry / certificates / live benchmark |
| **Autonomy architecture (canonical)** | `handover/hermes/hermespatalalayers.md` + `hermespatala-architecture-review.md` | the frozen end-state (one controller + one scheduler + per-layer skills; Hermes manages work, Pāṭala manages knowledge) |
| **Sanskritree import manifest** | `docs/corpus/SANSKRITREE-IMPORT-MANIFEST.md` | the full sanskritree audit: what's directly useful + where it imports + what's excluded |
| **Scholarly graph / data model** | `data/corpus/graph.ts` + `docs/SCHOLARLY_GRAPH.md` | repo |
| **Translation protocol** | `docs/TRANSLATION_PROTOCOL.md` | repo `docs/` |
| **Northstar / vision spec** | `docs/NORTHSTAR.md` | repo `docs/` |
| **Vision index (full arc, Vision 01–13)** | `docs/vision/INDEX.md` | repo `docs/vision/` |
| **Vision 06 — Pāṭala Review (adversarial)** | `docs/vision/vision-06-adversarial-review.md` | repo `docs/vision/` |
| **Vision 07 — The New Scholar** | `docs/vision/vision-07-new-scholar.md` | repo `docs/vision/` |
| **Vision 08 — Scholar Economics** | `docs/vision/vision-08-scholar-economics.md` | repo `docs/vision/` |
| **Vision 09 — Media & Cross-Tradition Engine** | `docs/vision/vision-09-media-and-cross-tradition.md` | repo `docs/vision/` |
| **Vision 10 — Market Entry & Partnerships** | `docs/vision/vision-10-market-entry-and-partnerships.md` | repo `docs/vision/` |
| **Vision 11 — Śiva Before Abhinava (genealogy corpus)** | `docs/vision/expansion/vision-11-siva-before-abhinava.md` | repo `docs/vision/expansion/` |
| **Vision 12 — Multi-Surface Platform** | `docs/vision/vision-12-multi-surface-platform.md` | repo `docs/vision/` |
| **Vision 13 — Product Portfolio (by user base)** | `docs/vision/vision-13-product-portfolio-by-user-base.md` | repo `docs/vision/` |
| **Dual-agent track** | `machinelearning/DUAL_AGENT_TRACK.md` | repo `machinelearning/` |
| **Context engineering** | `machinelearning/CONTEXT_ENGINEERING.md` | repo `machinelearning/` |
| **Education layer (vision)** | `machinelearning/EDUCATION_VISION.md` | repo `machinelearning/` |
| **Geometric ideas (borrowed)** | `machinelearning/geometric.md` | repo `machinelearning/` |
| **System growth + Hermes infra** | `machinelearning/SYSTEM_GROWTH_AND_HERMES.md` | repo `machinelearning/` |
| **Pāṭala as the Library's engine** | `machinelearning/PATALA_AS_LIBRARY_ENGINE.md` | repo `machinelearning/` |
| **API reference (OpenAPI)** | `docs/openapi.yaml` | repo `docs/` |
| **API docs (guide + endpoint index)** | `docs/api/README.md` | repo `docs/api/` |
| **MCP tool mapping** | `docs/api/mcp.md` | repo `docs/api/` |
| **Product research & build pack (2026-08-12)** | `docs/vision/functionality/research/2026-08-12/README.md` (Factory · Benchmarks · Audit · Review · Workbench + reuse/build doctrine) | repo `docs/vision/functionality/research/` |
| **Sanskritree deep-dive audit (agent usefulness)** | `handover/SANSKRITREE-AUDIT.md` (what Agent 1 + Agent 2 should mine: scholar corroboration, QA engine reuse, concordance, Lean verdict) | repo `handover/` |
| **Sanskritree truth/ classification (216 files)** | `handover/SANSKRITREE-TRUTH-CLASSIFICATION.md` (Class 1 scholarship citable / Class 2 frontier MACHINE_PROPOSED / Class 3 noise; + paper candidates) | repo `handover/` |
| **Corpus goldmine docs (imported)** | `docs/corpus/{canonical_reference_map, markguidance, translation_atlas, tradition_anchors, translation_flow_spec, leapfrog_guide, leapfrog_map, atlasflaws}.md` — the master substrate + Recognition Enquiry + method docs (read-first; originals live on sanskritree, never edit) | repo `docs/corpus/` |
| **Source-material graph (the tradition → scholar → source → essay map)** | `/root/projects/.meta/` (`TRADITION-GRAPH.md`, `SCHOLARS.md`, `SOURCE-RESOURCES.md`, `SOURCE-MANUAL.md`, `content-graph.json`) — the master index linking every tradition to its source-library texts + basecamp research objects + workengestation essays + sites | external `/root/projects/.meta/` |
| **Source-library (the actual scholar/source material)** | `/root/projects/source-library/` (`tantra/` incl. abhinavagupta, utpaladeva(-ipk), ksemaraja, jayaratha, lakshmanjoo, dyczkowski, matter-of-wonder, hareesh; `consciousness/scholars/` 29 dirs incl. biernacki, utpaladeva, dharmakirti; `platonism/`, `sufism/`, `occult/`, `buddhism/`, `frontier/`) — the scholarly corpus + extracted passages feeding corroboration/essays | external `/root/projects/source-library/` |

---

## Archived / superseded (do not follow)

These are kept for history but are **not** current. Read only for provenance.

| File | Superseded by | Move to |
|---|---|---|
| `HANDOVER.md` | `handover/` (lane INDEXs) | `handover/archive/` |
| `HANDOVER_NEXT.md` | `handover/` (lane INDEXs) | `handover/archive/` |
| `HANDOVER_SITE.md` | `handover/` (lane INDEXs) | `handover/archive/` |
| `HANDOVER_MCP_API.md` | the live `mcp/index.mjs` | `handover/archive/` |
| `STATE_OF_PLAY.md` | `handover/` + `docs/CHANGELOG.md` | `handover/archive/` |
| `HANDOVER_FINAL.md` | `handover/README.md` + lane INDEXs | `handover/archive/` |
| `SITE_STATUS.md` | `docs/CHANGELOG.md` | `handover/archive/` |
| `SESSION_HANDOVER.md` | `handover/LOG.md` + lane INDEXs | `handover/archive/` |
| `PROCESS_NOTES.md` (root) | `docs/PROCESS_NOTES.md` | `docs/_archive/` |
| `docs/PROGRESS_2026-08-10.md` | `docs/CHANGELOG.md` | `docs/_archive/` |
| `docs/PIPELINE_PROGRESS_2026-08-10.md` | `docs/CHANGELOG.md` | `docs/_archive/` |

> **Do not delete** archived files — history matters. Moving them to `docs/_archive/` removes the
> ambiguity without losing provenance.

---

## The audit

- `docs/AUDIT_2026-08-12.md` — the full repo health audit + the organization plan (this is the
  current "where are we" record).

---

## Update protocol

When you add a doc that becomes the authority for a topic, **add it to this index and archive the
old one**. The index is the single gate for "what is current."
