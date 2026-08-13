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
                                                              STATUS: ✅ CLOSED (2026-08-13)
devpath9  ──► SYNTHESIS NAT (mutation suite)                  STATUS: ✅ CLOSED (2026-08-13)
devpath10 ──► ESSAY COMPILER (Synthesis -> EssayPlan -> EssayClaim)
                                                              STATUS: ✅ CLOSED (2026-08-13)
devpath11 ──► EDUCATION COMPILER (Synthesis -> LearningClaim -> ...)
                                                              STATUS: ✅ CLOSED (2026-08-13)
devpath12 ──► UNIVERSAL BUNDLE (materialize_context(target, profile); ReviewBundle=REVIEW)
                                                              STATUS: ✅ CLOSED (2026-08-13)
```

## The sequence (PHASE 3 — scholar external-tools layer: S0 / Atlas NAT)

```
S0-COMMIT  ──► source-evidence substrate canonicalized          STATUS: ✅ CLOSED (2026-08-13)
ATLAS-NAT-v0 ─► source-reconciliation eval harness + multiaxis authority
                                                              STATUS: ✅ CLOSED (2026-08-13)
S0.1-PILOT ──► ugly-real-source chain through the adapters      STATUS: ✅ CLOSED (2026-08-13)
```

**Key insight:** devpath7 is not "small" — it is the reconciliation of my devpath4 proposition layer
with the Atlas `PropositionContent` (tech-arch-v1 §27–31). The genuinely new object is `ArgumentSynthesis`
(devpath8), which exists nowhere yet.

**A1-NEXT order (from the directive):** S0-COMMIT → ATLAS-NAT-v0 → S0.1-PILOT → devpath8 → devpath9 →
devpath10 → devpath11 → devpath12. All the unblocked routes in this order are now closed. devpath2/3
(G2/ARGMAP on real Agent-2 output) remain the only blocked routes — the NAT harnesses are ready gates.

**Branch note (peer-review verifiability):** the peer review (`docs/global/peer-review-goat.md`) could
not independently verify the Agent-1 work because it inspects `origin/agent1-argument-layer-a1b`, which
is a stale fork (146 commits behind `agent2`). The live Agent-1 epistemic + Atlas-NAT + synthesis work
lives on **`origin/agent2`** (pushed). Reconcile the `a1b` fork onto the live line when Agent 0 does the
branch merge — do not force-push between the diverged branches.

**Peer-review actions (A1-Q1..Q6):**
- A1-Q1 authority-inflation fix — DONE (resolver + ladders + test; `a96daee`)
- A1-Q2 ATLAS-NAT-NATURAL-v1 (natural benchmark, false-promotion metric) — DONE (devpath13 P0)
- A1-Q3 SYNTHESIS-NAT-NATURAL-v1 (real debates) — pending
- A1-Q4 real G2 blind retest — blocked on Agent 2
- A1-Q5 real ARGMAP whole-chain benchmark — blocked on Agent 2
- A1-Q6 scholar challenge (one hard real object + a human scholar) — pending

---

## The sequence (PHASE 4 — empirical qualification: A1-CONTINUE-v2)

```
devpath13 ──► A1-CONTINUE-v2: QUALIFY THE SYSTEM, DO NOT EXPAND THE ONTOLOGY
              P0 ATLAS-NAT-NATURAL-v1 · P1 cross-lane Atlas audit · P2 real ARGMAP G3A
              · P3–P12 VERTICAL-1 IPVV end-to-end · P13–P20 discipline/benchmarks
                                                              STATUS: 🔄 IN PROGRESS (2026-08-13)
              full spec → `endgamebuild/devpath13-a1-continue-v2.md` (verbatim directive)

  P0 ATLAS-NAT-NATURAL-v1  STATUS: ✅ CLOSED (2026-08-13) — 51 frozen natural cases, non-circular
              evidence-derived evaluator; SYSTEM_FALSE_AUTHORITY_PROMOTION_RATE=0.216, detection
              recall/precision=1.000, false-rejection=0.000; regression tests for the
              MULTI_SOURCE_MATCHED inflation bug. Record: benchmarks/v0/runs/atlas-nat-natural-*.json

  P1 cross-lane Atlas audit  STATUS: ✅ CLOSED (2026-08-13) — audited Agent 2 resolver; found 3
              semantic-inflation findings (publication not rights-aware [SEVERE], factory keyed on
              work-identity not edition, single-ladder vocab across heterogeneous dims). Fixed _gate
              to be rights-aware + dimension-consistent; P1 regression tests pass. → devpath13-p1-atlas-audit.md

  P2 real ARGMAP G3A  STATUS: ✅ CLOSED (2026-08-13) — ARGMAP NAT verifier runs on the real committed
              factory map (kramasadbhava:v1, PASS) + 51 real IPVV exemplars (shape 1.0, mutation recall
              1.0). Added G3A hard rule: build_proposition_layer gated on argmap_nat_ok — load-bearing
              ARGMAP failure => proposition production NOT_ELIGIBLE. → devpath13-p2-argmap-g3a.md
```

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
- `devpaths/devpath7.md` — ✅ complete
- `devpaths/devpath8.md` — ✅ complete
- `devpaths/s0-substrate.md` — ✅ complete (S0 + Atlas NAT + pilot)
- `devpaths/agent1atlas-reaction.md` — my reaction notes on the Atlas convergence directive
