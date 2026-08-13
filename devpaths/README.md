# DEVPATH ROADMAP — status index

*Local devpath tracking for the endgame build (Agent 1 lane, verification + epistemic core).
Each route is self-contained: objective, work, acceptance, status. Update the status line as routes
close. The sequence comes from `endgamebuild/HANDOVER-TO-NEW-AGENT.md` (the a1b branch) +
`docs/global/agent1atlas.md` (the Atlas convergence directive) — see `devpaths/agent1atlas-reaction.md`
for my analysis.*

---

## The sequence (PHASE 1 — epistemic core: G2→G4)

```
devpath1 ──► wire Nyāya gate + build ARGMAP NAT harness        STATUS: ✅ CLOSED (2026-08-13)
devpath2 ──► G2: close the T1/L0 correction loop              STATUS: ⛔ BLOCKED (needs Agent 2 factory_rebuild)
devpath3 ──► G3A: ARGMAP NAT on real Agent 2 output           STATUS: ⛔ BLOCKED (needs real ARGMAP batch)
devpath4 ──► G3B: Proposition core                             STATUS: ✅ CLOSED (2026-08-13)
devpath5 ──► G3C: Crux + arguments + Nyāya-profile             STATUS: ✅ CLOSED (2026-08-13)
devpath6 ──► G4: Human authority path + first UI               STATUS: ✅ CLOSED (2026-08-13)
```

## The sequence (PHASE 2 — synthesis + projection: G5, the Atlas convergence)

```
devpath7  ──► CANONICAL GRAPH CONTRACT (typed DSO + vector authority + reconcile my
              proposition layer -> Atlas PropositionContent)  STATUS: ✅ CLOSED (2026-08-13)
devpath8  ──► SYNTHESIS CORE (ResearchQuestion / DebateFrame / Position / ArgumentSynthesis)
                                                             STATUS: ⏳ READY (after devpath7)
devpath9  ──► SYNTHESIS NAT (mutation suite)                  STATUS: ⏳ READY (after devpath8)
devpath10 ──► ESSAY COMPILER (Synthesis -> EssayPlan -> EssayClaim)
                                                             STATUS: ⏳ READY (after devpath9)
devpath11 ──► EDUCATION COMPILER (Synthesis -> LearningClaim -> ...)
                                                             STATUS: ⏳ READY (after devpath10)
devpath12 ──► UNIVERSAL BUNDLE (materialize_context(target, profile); ReviewBundle=REVIEW)
                                                             STATUS: ⏳ READY (after devpath11)
```

**Key insight:** devpath7 is not "small" — it is the reconciliation of my devpath4 proposition layer
with the Atlas `PropositionContent` (tech-arch-v1 §27–31). The genuinely new object is `ArgumentSynthesis`
(devpath8), which exists nowhere yet.

---

## Status legend

| Mark | Meaning |
|---|---|
| ✅ CLOSED | fully built, tested, committed |
| ⛔ BLOCKED | gated on another lane's output (Agent 2) |
| ⏳ READY | can start (unblocked), not yet started |
| 🔄 IN PROGRESS | currently being worked |

---

## Cross-lane gates

- **devpath2 (G2)** needs Agent 2 to: consume the 6-finding bundle (`data/evaluation/findings/`)
  → fix the segmentation root class → `factory_rebuild(cidgagana:v1)` → emit an `EvaluationCandidate`
  (new exact version) + `ImpactReport` (trigger=`EF-T1-2026-0003`).
- **devpath3 (G3A)** needs Agent 2's factory to emit a real ARGMAP batch (the worker is done;
  corpus pending). The ARGMAP NAT harness from devpath1 is ready to consume it.
- **devpath7 (canonical contract)** is the joint Agent-1/Agent-2 convergence point — Atlas owns
  identity+persistence; Agent 1 owns epistemic contracts (per `docs/global/agent1atlas.md`).

---

## Per-route notes

- `devpaths/devpath1.md` — ✅ complete
- `devpaths/devpath2.md` — blocked (G2 correction loop)
- `devpaths/devpath3.md` — blocked (G3A ARGMAP NAT on real output)
- `devpaths/devpath4.md` — ✅ complete
- `devpaths/devpath5.md` — ✅ complete
- `devpaths/devpath6.md` — ✅ complete
- `devpaths/agent1atlas-reaction.md` — my reaction notes on the Atlas convergence directive
