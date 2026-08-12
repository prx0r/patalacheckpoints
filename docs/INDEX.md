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
| **Full-system onboarding** | `THE_COMPANION.md` | sanskritree `_stack/ipvv/specs/` |
| **Handover folder (both lanes — README first)** | `handover/README.md` | repo `handover/` |
| **Cross-lane coordination log** | `handover/LOG.md` | repo `handover/` |
| **THE GOVERNING RULE — read first** | `AGENTS.md` + `machinelearning/_ACTIVE/AGENTS-DOCTRINE.md` | repo root |
| **Dual-agent vision + checkpoint map** | `machinelearning/_ACTIVE/dualagentvision.md` + `dualagentvision-ADAPTED.md` | repo `machinelearning/` |
| **The project's self-audit ledger** | `machinelearning/_ACTIVE/CLAIMS.md` | repo `machinelearning/` |
| **Anti-theatre component contracts** | `machinelearning/_ACTIVE/COMPONENT-CONTRACTS.md` | repo `machinelearning/` |
| **Agent 1 — ML lane (current state)** | `handover/agent-1-ml/INDEX.md` | repo `handover/` |
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
| **Scholarly graph / data model** | `data/corpus/graph.ts` + `docs/SCHOLARLY_GRAPH.md` | repo |
| **Translation protocol** | `docs/TRANSLATION_PROTOCOL.md` | repo `docs/` |
| **Northstar / vision spec** | `docs/NORTHSTAR.md` | repo `docs/` |
| **Vision index (full arc, Vision 01–08)** | `docs/vision/INDEX.md` | repo `docs/vision/` |
| **Vision 06 — Pāṭala Review (adversarial)** | `docs/vision/vision-06-adversarial-review.md` | repo `docs/vision/` |
| **Vision 07 — The New Scholar** | `docs/vision/vision-07-new-scholar.md` | repo `docs/vision/` |
| **Vision 08 — Scholar Economics** | `docs/vision/vision-08-scholar-economics.md` | repo `docs/vision/` |
| **Dual-agent track** | `machinelearning/DUAL_AGENT_TRACK.md` | repo `machinelearning/` |
| **Context engineering** | `machinelearning/CONTEXT_ENGINEERING.md` | repo `machinelearning/` |
| **Education layer (vision)** | `machinelearning/EDUCATION_VISION.md` | repo `machinelearning/` |
| **Geometric ideas (borrowed)** | `machinelearning/geometric.md` | repo `machinelearning/` |
| **System growth + Hermes infra** | `machinelearning/SYSTEM_GROWTH_AND_HERMES.md` | repo `machinelearning/` |
| **Pāṭala as the Library's engine** | `machinelearning/PATALA_AS_LIBRARY_ENGINE.md` | repo `machinelearning/` |
| **API reference (OpenAPI)** | `docs/openapi.yaml` | repo `docs/` |
| **API docs (guide + endpoint index)** | `docs/api/README.md` | repo `docs/api/` |
| **MCP tool mapping** | `docs/api/mcp.md` | repo `docs/api/` |

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
