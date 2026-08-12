# HANDOVER — the coordination folder (both lanes)

*The one place both agents document work and hand off to each other. Read this README first: it names
which doc is authoritative for what, so a new agent is never lost and status never rots in a stale
snapshot.*

---

## The two lanes

| Lane | Folder | Owns |
|---|---|---|
| **Agent 1 — ML/research** | `handover/agent-1-ml/` | ML strategy, benchmark, retrieval, experiments, tokenizer, statistical rigor |
| **Agent 2 — corpus compiler + integrity** (formerly "integration/content", formerly "the L0 agent") | `handover/agent-2-integration/` | data/corpus, app, lib, pipeline (verify_l0, corpus_state, raw_l0, agent3_batch/queue, l0_registry, review_engine), Sanskrit substrate + source→L0 proof, scholarly specs, docs |

`VISION_AND_NAVIGATION.md` + `machinelearning/DUAL_AGENT_TRACK.md` define the split in full. This
folder is the **operational record** of that split.

---

## The rules (how to stop the staleness)

1. **Each lane keeps ONE living `INDEX.md`** — the "what is true RIGHT NOW" pointer (done / in-progress /
   next). Update it as you work; it is the current state, not a snapshot.
2. **Everything else is append-only** under the lane: session notes, specs, handoffs. Never overwrite
   a past record — add a new file (or append a dated entry). History is preserved in `handover/archive/`.
3. **Cross-lane coordination goes in the shared `LOG.md`** (one entry per handoff: what · why · file ·
   date · direction · schema snippet when data-carrying).
4. **When a doc becomes the authority for a topic**, add it to the relevant lane's `INDEX.md` — never
   leave two competing "current" docs.
5. **When a session ends**, drop a `SESSION-<date>.md` note into your lane (what you did, what's open),
   then archive any superseded top-level snapshot.

---

## What's authoritative for what (the single source of truth)

| Concern | Document |
|---|---|
| Vision + navigation (START HERE) | `VISION_AND_NAVIGATION.md` (repo root) |
| Doc index (flat canonical map) | `docs/INDEX.md` |
| Lane split + protocol | `machinelearning/DUAL_AGENT_TRACK.md` |
| **Agent 1 current state** | `handover/agent-1-ml/INDEX.md` |
| **Agent 2 current state** | `handover/agent-2-integration/INDEX.md` |
| **Cross-lane handoffs** | `handover/LOG.md` |
| Full-system onboarding | `THE_COMPANION.md` (sanskritree) |
| Changelog (API/data/scholarly) | `docs/CHANGELOG.md` |

> The old top-level snapshots (`HANDOVER_FINAL.md`, `SITE_STATUS.md`, `SESSION_HANDOVER.md`) and the
> old `machinelearning/HANDOFF-LOG.md` have been moved to `handover/archive/` so this folder is the
> one current place. History is preserved, not deleted.
