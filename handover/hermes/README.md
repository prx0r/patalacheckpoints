# HERMES AREA — Pāṭala's execution kernel + the peer-review / scholar surface

*2026-08-12. The dedicated home for everything Hermes-related: the canonical integration, the dev plan,
the setup, and (new) the **peer-review / scholar-surface** work. This is the execution-kernel lane's docs
home — read `CANONICAL.md` first for the corrected thesis.*

---

## THE THESIS (one line)

> **Hermes is Pāṭala's replaceable execution kernel; Pāṭala is the durable epistemic protocol + scholarly
> state. The moat is that a scholar's correction becomes an executable graph mutation with provenance.**

## THE IMMEDIATE ENGINEERING OBJECTIVE (the northstar)

> **Given raw Sanskrit and a registered source, autonomously produce a lossless, word/phrase-level literal
> analysis (RAW-L0) with every decision auditable, every uncertainty exposed, and no unsupported analysis
> silently promoted.** See `AUTOTRANSLATE-NORTHSTAR.md`.

The one giant hole blocking the autonomous translator: **RAW SANSKRIT → L0 (MODE_B) does not exist.**
MODE_A (AND_GLOSS) ✅ exists; MODE_B (RAW_SANSKRIT) ❌ not built — so raw works (Kramasadbhāva etc.) are
blocked from Agent 3. **Build RAW-L0, prove it blind on IPVV (Sanskrit-only replay), then unleash it on
Kramasadbhāva.** Then autonomous batch translation becomes a queue-processing problem.

## The docs

| Doc | What |
|---|---|
| **`CANONICAL.md`** | THE integration reference: corrected thesis, the 4 corrections, verified feature map, realized architecture, 16 advanced recipes, the scholar & API surface (Workbench, BYOA/MCP, A2A, peer review, executable-corrections moat, minimal architecture). |
| **`AUTOTRANSLATE-NORTHSTAR.md`** | **The immediate engineering objective** — RAW-L0 (MODE_B): the one gap blocking the autonomous translator. Target, terminology correction, the record shape, the agentic reasoning loop, the Sanskrit-only replay experiment, the build sequence (raw_l0.py → audit → replay → human review → Kramasadbhāva → batch). |
| **`HERMES-AGENT3-FACTORY-COORDINATOR.md`** | **Agent 3 = Factory Coordinator / control plane** — the design for a narrow A3 that routes/monitors factory work via Hermes Kanban + profiles, never editing scholarly objects. Profiles (producer/verifier/coordinator), dependency-aware Kanban, human blocking, scheduled tasks, worker lanes. The "make Agent 3 now" case + the exact guardrails. |
| **`TRANSLATION-APPROACH-AND-VALIDATION.md`** | **The production doctrine** — how to translate huge texts (the IPVV chunk + context-engineer + review method), the validation-first principle (a wrong translation is worse than none), Dyczkowski's Tantrāloka as the gold-standard reference, and the per-work term-context packet to stop Sanskrit terms being misread across traditions. |
| **`DEV-PLAN.md`** | The build sequence (Phase 1 execution kernel → Phase 2 A3 factory → Phase 3 ReviewEvent-as-graph-mutation → Phase 4 Scholar Workbench → Phase 5 BYOA + corrections dataset). |
| **`PATALA-SETUP.md`** | The fresh hermes profile/project + the Pāṭala "soul" plan (do NOT run the mutation commands until approved). |
| **`BACKEND-MODEL.md`** | The verified feature→vision map (superseded thesis — see CANONICAL). |
| **`PEER-REVIEW.md`** | **The peer-review system spec** — the scholar surface + the executable-corrections moat: ReviewEvent-as-graph-mutation, the honest state ladder, the Scholar Workbench + copilot, machine pre-review, the review API + tool boundary, and **the interoperability stack** (integration-heavy, invention-light — OpenReview/Hypothesis/DocMaps/COAR/ORCID/Crossref/OpenAlex/JATS as interop targets, NOT rebuilds). |
| `advanced-recipes-source.md`, `advanced3-correction-source.md`, `peer-review-interoperability-source.md` | The R2 source documents (preserved). |

## How this relates to the phases (DEV-PLAN.md)
- Phase 3 (ReviewEvent as graph mutation) + Phase 4 (Scholar Workbench) + Phase 5 (BYOA) all live here.
- The **peer-review spec** (`PEER-REVIEW.md`) is the concrete design for Phases 3–5.

## Carry-forward
**Pāṭala = epistemic state; Hermes = execution. The peer review is the product: a scholar's judgment
becomes a provenance-carrying graph mutation that recomputes downstream arguments, cruxes, and syntheses.**
Read `CANONICAL.md` + `DEV-PLAN.md` + `PEER-REVIEW.md` in that order.
