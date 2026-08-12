# AGENT 0 (COORDINATOR) — INDEX (the "what is true RIGHT NOW" pointer)

*2026-08-12. Live pointer — update as you work. Agent 0 governs the agent system, not a scholarly lane.*

---

## What Agent 0 owns (the system)
- `handover/SYSTEM.md` — the agent-system meta-architecture (vision-once + registry + derived orientations + staleness checker)
- `handover/AGENTS.yaml` — the machine-readable agent registry (the contract)
- `handover/check_staleness.py` — the staleness checker (the enforcement)
- `handover/ORIENTATION-AGENT0.md` — this lane's orientation
- `handover/CHECKPOINTS.md` — the shared execution map (governs the CP0–CP4 gates)
- `VISION_AND_NAVIGATION.md` — the canonical vision (lives once, never duplicated)
- `handover/agent0-coordinator/AGENT-ARCHITECTURE-VISION.md` — **the mature multi-agent architecture** (A0–A8: the production loop; only A0–A3 now). The canonical strategic reference for how the agent system grows.
- **`handover/hermes/`** — **the dedicated Hermes area** (execution kernel + scholar/peer-review surface). Read `handover/hermes/README.md` first, then `CANONICAL.md` (the corrected thesis: Hermes = REPLACEABLE execution kernel, NOT epistemic backend), `DEV-PLAN.md` (the 5-phase build), `PEER-REVIEW.md` (the executable-corrections system: review = a graph mutation with provenance), `PATALA-SETUP.md` (fresh profile/project plan), `BACKEND-MODEL.md` (verified feature map). Peer review is the product — it turns the scholar's judgment into a provenance-carrying graph mutation that recomputes downstream arguments/cruxes/themes.

## The architecture (from AGENT-ARCHITECTURE-VISION.md)
```
A0 governance ──┬── A2 CORPUS COMPILER ──┬── A4 REVIEW ──┐
                ├── A3 TRANSLATION FACTORY              │
                └── A1 PHILOSOPHY ENGINE  ── A5 SYNTHESIS ── A6 PROJECTION
                                                                   │
                                                          A7 SCHOLAR NETWORK
(+ A8 ACQUISITION later)
```
**Instantiate order:** A0–A3 now (A3 planned); A4 review next; A5/A6/A7/A8 when the substrate demands.
**The loop:** A8 acquire → A2 normalize/prove → A3 produce drafts → A1 model scholarship → A4 review/adjudicate → A5 synthesize → A6 project → world; A7 injects humans; A0 governs.
**Key principle:** "AI proposes ≠ Pāṭala asserts" becomes operational at A4 (epistemic separation — A1 must not review its own work).

## Current system state (2026-08-12)
- **Registry:** agents defined: agent0 (coordinator) · agent1 (philosophy/ML) · agent2 (CORPUS COMPILER — reframed from "L0 agent", 2026-08-12) · **agent3 (translation factory) — planned, scaffold when the auto_run supervisor is built.**
- **Agent 2 (corpus compiler):** IPVV L0 63/63 FROZEN; P2 calibrated, P3 ranker rejected, P4 witness frozen; **translation-state ledger built** (`pipeline/corpus_state.py` + `/api/corpus/state`) — the control plane Agent 3 consumes.
- **Agent 1 (CP4):** ARG-001..005 + vertical object v0; independent review of the 5 golds is the central gate.
- **Worktrees:** per-agent worktree paths registered in AGENTS.yaml (`patala-agent1`, `patala-agent2`) — root-cause fix for INCIDENT-2026-08-12-01 (`handover/GIT-INCIDENTS.md`).

## The checkpoint ladder (real state)
```
CP0 DONE · CP1 PARTIAL(L0) · CP2 PARTIAL · CP3 PARTIAL · CP4 PARTIAL · CP5–CP6 PARTIAL · CP7+ NOT STARTED
```

## Current open items (for the coordinator)
- [ ] Run `check_staleness.py` to 0 failures (Agent 2 orientation + Agent 0 dir now exist — verify).
- [ ] Confirm no orientation embeds a verbatim vision copy.
- [ ] Keep the vision live in `VISION_AND_NAVIGATION.md` only.
- [ ] Gate Agent 1's CP4 (5 golds consistent) and Agent 2's CP1 (PhilologicalProof v1 honest).
