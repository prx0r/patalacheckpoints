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
| **Full-system onboarding** | `THE_COMPANION.md` | sanskritree `_stack/ipvv/specs/` |
| **Current site handover** | `HANDOVER_FINAL.md` | repo root |
| **ML strategy (frozen)** | `machinelearning/MLUSEINPATALA.md` | repo `machinelearning/` |
| **ML dev plan** | `machinelearning/DEVPLAN.md` | repo `machinelearning/` |
| **ML vision (big picture)** | `machinelearning/MLVISION.md` | repo `machinelearning/` |
| **IPVV stack integration (verified)** | `machinelearning/IPVV-STACK-INTEGRATION.md` | repo `machinelearning/` |
| **Corpus build (Phase 1)** | `docs/PHASE1_IPVV_CORPUS_PROCESS_NOTES.md` | repo `docs/` |
| **Scholarly graph / data model** | `data/corpus/graph.ts` + `docs/SCHOLARLY_GRAPH.md` | repo |
| **Translation protocol** | `docs/TRANSLATION_PROTOCOL.md` | repo `docs/` |
| **Northstar / vision spec** | `docs/NORTHSTAR.md` | repo `docs/` |
| **Dual-agent track** | `machinelearning/DUAL_AGENT_TRACK.md` | repo `machinelearning/` |

---

## Archived / superseded (do not follow)

These are kept for history but are **not** current. Read only for provenance.

| File | Superseded by | Move to |
|---|---|---|
| `HANDOVER.md` | `HANDOVER_FINAL.md` | `docs/_archive/` |
| `HANDOVER_NEXT.md` | `HANDOVER_FINAL.md` | `docs/_archive/` |
| `HANDOVER_SITE.md` | `HANDOVER_FINAL.md` + `docs/SITE_STATUS.md` | `docs/_archive/` |
| `HANDOVER_MCP_API.md` | `HANDOVER_FINAL.md` + the live `mcp/index.mjs` | `docs/_archive/` |
| `STATE_OF_PLAY.md` | `HANDOVER_FINAL.md` + `docs/CHANGELOG.md` | `docs/_archive/` |
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
