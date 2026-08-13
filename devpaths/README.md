# DEVPATH ROADMAP — status index

*Local devpath tracking for the endgame build (Agent 1 lane, verification + epistemic core).
Each route is self-contained: objective, work, acceptance, status. Update the status line as routes
close. The sequence comes from `endgamebuild/HANDOVER-TO-NEW-AGENT.md` (the a1b branch) +
`docs/global/agent1atlas.md` (the Atlas convergence directive) — see `devpaths/agent1atlas-reaction.md`
for my analysis.*

**Global lens (2026-08-13):** Pāṭala = the integration & identity layer ("OpenAlex for Sanskrit") —
`docs/global/globalpartnerships.md`. The devpath work here (Atlas, synthesis, scholar substrate) IS the
identity/epistemic foundation that strategy sits on.*

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

  P0 ATLAS-NAT-NATURAL-v1  STATUS: ✅ QUALIFIED (2026-08-13) — 51 frozen natural cases, non-circular
              evidence-derived evaluator; SYSTEM_FALSE_AUTHORITY_PROMOTION_RATE=0.216 (FIXTURE rate),
              detection recall/precision=1.000, false-rejection=0.000.
              PRODUCER-SIDE audit (repair loop): real resolver on the corpus emits 0.000 false
              promotions (offline 0/69, online 0/10) — the 0.216 is the hypothetical-bad-producer
              catch-rate, NOT the real producer rate. Real producer <0.05 target: ACCEPTED.
              Record: benchmarks/v0/runs/atlas-producer-*.json + atlas-nat-natural-*.json

  P1 cross-lane Atlas audit  STATUS: ✅ CLOSED (2026-08-13) — audited Agent 2 resolver; found 3
              semantic-inflation findings (publication not rights-aware [SEVERE], factory keyed on
              work-identity not edition, single-ladder vocab across heterogeneous dims). Fixed _gate
              to be rights-aware + dimension-consistent; P1 regression tests pass. → devpath13-p1-atlas-audit.md

  P2 real ARGMAP G3A  STATUS: ✅ CLOSED (2026-08-13) — ARGMAP NAT verifier runs on the real committed
              factory map (kramasadbhava:v1, PASS) + 51 real IPVV exemplars (shape 1.0, mutation recall
              1.0). Added G3A hard rule: build_proposition_layer gated on argmap_nat_ok — load-bearing
              ARGMAP failure => proposition production NOT_ELIGIBLE. → devpath13-p2-argmap-g3a.md

  P3 VERTICAL-1 selection + dossier  STATUS: ✅ CLOSED (2026-08-13) — selected IPVV-VERTICAL-001 = the
              Pratyabhijñā recognition argument vs the Buddhist determination (adhyavasāya) account of
              external cognition. FROZEN the human-readable SOURCE-DOSSIER
              (data/published/ipvv/IPVV-VERTICAL-001-SOURCE-DOSSIER.md): source identity, L2 spans,
              reconstruction reference (thesis/premises/opponent/reply/qualification), and the load-bearing
              crux CRUX-IPVV-001 (self-luminosity of the establishing act). Exercises the existing
              reflexion-core stack (SYN-IPVV-REFLEXION-CORE-001).

  P4/P6 VERTICAL-1 proposition + crux stress-test  STATUS: ✅ CLOSED (2026-08-13) — extended the crux
              engine to model the directive's P6 hard structures: redundant support (P1-OR-P2
              independently sufficient), jointly-necessary premises, active non-monotonic DEFEATERS, and
              alternative-route bypass. Verified on the real VERTICAL-1 argument (adhyavasāya): decisive
              set {P1,P2}; O3 fire-burning-wood defeater blocks the inference (= CRUX-IPVV-001); warrant
              P4 is load-bearing. Tests in test_crux_engine.py + experiments/vertical1_crux_validation.py
              (all pass); output benchmarks/v0/review/VERTICAL-1-CRUX-VALIDATION.json.

  P7 SYNTHESIS-NAT-NATURAL-v1  STATUS: ✅ CLOSED (2026-08-13) — audited the real VERTICAL-1 synthesis
              (SYN-IPVV-REFLEXION-CORE-001) against the dossier on the P7 natural metrics: catastrophic
              RIVAL_AS_CONSENSUS=~0, OPEN_AS_RESOLVED=~0; POSITION_RECOVERY (rival+śaiva), ARGUMENT_
              COVERAGE, CRUX_RECALL, SCOPE_FIDELITY (honest does-not-establish boundary), and
              COUNTEREVIDENCE_RECALL (Buddhist defeater preserved) all PASS.
              → experiments/vertical1_synthesis_natural.py → benchmarks/v0/review/VERTICAL-1-SYNTHESIS-NAT-NATURAL.json

  P8 whole-essay audit  STATUS: ✅ CLOSED (2026-08-13) — the C.1 sentence audit (per-sentence fidelity)
              PASSES (all 12 load-bearing sentences claim_supported). The WHOLE-ESSAY audit found a genuine
              gap: S012 (the scope/boundary claim) and S013 (the Buddhist rival representation) are
              LOAD_BEARING but carry NO source/claim refs → SOURCE_TRACEABILITY=False. Promoted to
              EF-ESSAY-2026-0001 (OPEN).

  P9 education validation  STATUS: ✅ CLOSED (2026-08-13) — derived 8 LearningInteractions from the
              SAME VERTICAL-1 synthesis covering the directive §11 skills (speaker classify, proposition
              identify, premise attach, warrant reconstruct, opponent attack, crux identify, source
              ground, translation repair). Audited: EPISTEMIC_VALIDITY (no manufactured consensus;
              consensus-distractor never correct) and PEDAGOGICAL_VALIDITY (one task, declared skill,
              distractors encode the NAT failure taxonomy — OBJECTION_AS_AUTHOR_VIEW, QUALIFIER_DROP,
              SCOPE_INFLATION, etc.). All PASS.
              → experiments/vertical1_education.py → benchmarks/v0/review/VERTICAL-1-EDUCATION.json

  P11 whole-chain correction  STATUS: ✅ CLOSED (2026-08-13) — froze the expected consequences of a
              low-level correction (REVISE the load-bearing premise G2-TC2) BEFORE applying it, then
              verified the review_engine's deterministic impact: G2-INF1 + G2-CONC flip to NEED_REVIEW,
              isolation holds (ARG-004 stays CANDIDATE), and the semantic downstream (synthesis
              conclusion → essay claim → learning interactions) is marked stale. The correction
              propagates semantically, not merely 'rebuilds'.
              → experiments/vertical1_correction.py → benchmarks/v0/review/VERTICAL-1-CORRECTION.json

  P16 PATALA-VERTICAL-1 certificate  STATUS: ✅ CLOSED (2026-08-13) — assembled the certificate for the
              complete chain (Atlas identity → T1/L0 → ARGMAP NAT → propositions → argument → crux →
              ArgumentSynthesis → essay → education → ReviewBundle → ContextBundle → correction
              propagation). 12/13 nodes certified; the full-essay SOURCE_TRACEABILITY gap (S012/S013)
              is honestly marked OPEN. Authority at every node is MACHINE_PROPOSED/ENGINEERING_VALIDATED
              — no H witness, NOT_HUMAN_REVIEWED.
              → experiments/vertical1_certificate.py → benchmarks/v0/review/PATALA-VERTICAL-1-CERTIFICATE.json
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
