# HERMES AREA — Pāṭala's execution kernel + the peer-review / scholar surface

*2026-08-12. The dedicated home for everything Hermes-related: the canonical integration, the dev plan,
the setup, and (new) the **peer-review / scholar-surface** work. This is the execution-kernel lane's docs
home — read `CANONICAL.md` first for the corrected thesis.*

---

## THE THESIS (one line)

> **Hermes is Pāṭala's replaceable execution kernel; Pāṭala is the durable epistemic protocol + scholarly
> state. The moat is that a scholar's correction becomes an executable graph mutation with provenance.**

## The docs

| Doc | What |
|---|---|
| **`CANONICAL.md`** | THE integration reference: corrected thesis, the 4 corrections, verified feature map, realized architecture, 16 advanced recipes, the scholar & API surface (Workbench, BYOA/MCP, A2A, peer review, executable-corrections moat, minimal architecture). |
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
