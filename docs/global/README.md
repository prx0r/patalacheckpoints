# GLOBAL — shared architectural files for ALL agents

*2026-08-13. The home for **global architectural files** that every agent reads (both Agent 1 and Agent 2, and
future agents) at orientation. These are the shared, canonical, cross-lane documents — not lane-specific
handovers. Read the timestamped checkpoint first, then the architecture.*

## Files

| Doc | What it is | Read |
|---|---|---|
| `PATALA-GLOBAL-ARCHITECTURE.md` | **Pāṭala Global Architecture v0.1** — the definitive architecture: seven planes, the constitutional rule, the native epistemic ontology, the three DAGs, the object namespace, the benchmark family, the skill contract, the four proof tracks, the "what not to build" list, the six hard research questions, and the architecture criterion for every future feature. | **read first** — the one answer to "what are we actually building?" |
| `GLOBAL-STATE-2026-08-13.md` | **Timestamped global checkpoint** (ELAD handover) — the big picture, permanent epistemic discipline, the architecture, falsifications to preserve, and the CURRENT DIRECTION. Stale by design — a snapshot. | read early as orientation |
| `GLOBAL-NEXT-2026-08-13.md` | **Coordinated next-step reference** — reconciles the stale global-state doc with the ACTUAL current state (Agent 2 factory running + hardened; Agent 1 S0 scholar-corpus). Lists the priority next moves + how to check the live systems + the canonical files map. | read to see "what's true right now" |
| `patala-peer-review.md` | **External peer-review of the whole vision/architecture** (imported from R2) — rates architecture/epistemic design/product coherence, gives verdicts on every claim (dependency graph = computational moat + institutional moat; anti-build doctrine; projections not systems; the exact Pāṭala irreducible kernel), and lists required revisions ("stop saying owns the truth", strict SCHOLARLY_CORROBORATED semantics, etc.). | read for the strategic audit + required corrections |
| `patala-full-audit-bundle/` | **Full vision/moat/product audit** (imported zip) — the coherent center ("scholarly intelligence infrastructure, epistemic dependency graph"), the irreducible kernel, the 4 moats, executable corrections, the 4 first products (factory/benchmark/audit/review), the flywheel, and 7 repo contradictions to fix. | read for the deep audit |
| `patala-live-arch-spec/` | **Live repo reconciliation + canonical kernel spec** (imported zip) — turns the multi-agent implementation into one canonical versioned scholarly state; the exact package ownership boundary, cross-agent contract, migration plan, status-axis migration, the semantic-duplication problems, and the implementation backlog. | read for the concrete "make it one kernel" plan |
> **The relationship:** `GLOBAL-STATE` is the timestamped *snapshot* of where things are; `PATALA-GLOBAL-ARCHITECTURE`
> is the *durable* architecture everything points down to. The 13 vision docs are product/strategy lenses — they
> point down to the architecture, never independently describe implementation. `GLOBAL-NEXT` reconciles the stale
> snapshot with the actual current state (Agent 2's autonomous factory, Agent 1's S0). The three imported audit/spec
> bundles (`patala-peer-review.md`, `patala-full-audit-bundle/`, `patala-live-arch-spec/`) are durable cross-lane
> references imported from R2 on 2026-08-13. **Education lives in `docs/vision/education/`, not here** (it is a
> vision/product lens, not a global architectural file).

## How to add a global architectural file
If a document is (a) architectural, (b) cross-lane (both agents), and (c) durable (not a dated snapshot), put it
here and register it in:
- `handover/CONTEXT-CHAIN.yaml` `shared:` (so both agents read it at orientation), and
- `docs/INDEX.md`.
