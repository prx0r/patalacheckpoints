# PRE-SYNTHESIS CONFIRMATION — everything done right before devpath8

*2026-08-13. Readiness gate. The user's requirement: **before building synthesis (devpath8), confirm
everything else is done right.** This is the honest confirmation checklist + result, so we do not build
the convergence object on an unverified base.*

---

## The rule

> Synthesis (`ArgumentSynthesis`) is the convergence object that essays/education/review consume. It must
> NOT be built on an unverified base. So: confirm the epistemic core (devpaths 1–6) is real and solid,
> and confirm the convergence prerequisites (devpath7, Atlas boundary) are understood — then build.

---

## ◆ CONFIRMED DONE-RIGHT

### 1. All devpath test suites pass (7/7)

| Test | Result |
|---|---|
| devpath1: `verify_claim_semantic` (bounded gate) | PASS |
| devpath1: Nyāya gate wiring | PASS |
| devpath4: proposition layer | PASS |
| devpath5: crux engine | PASS |
| devpath1: ARGMAP NAT harness | PASS |
| devpath6: ReviewBundle + human-authority path | PASS |
| regression: review engine | 23/23 |

### 2. Epistemic-core chain is real and coherent (the input to synthesis)

```text
24 propositions  →  4 arguments  →  15 cruxes  →  4 Nyāya profiles
```

- Every crux has a non-empty decisive premise set (no empty cruxes). ✅
- Nyāya profiles are bounded (outcomes PASS/PASS_WITH_OPEN/FAIL), never truth-oracles. ✅
- Integration verified end-to-end (gold → proposition → crux → review). ✅

### 3. Inspect NAT harnesses run

- `ARGMAP-NAT`: shape_pass_rate 1.000
- `ARGMAP-NAT-IPVV`: coverage_recall 1.000

### 4. R2 (Atlas asset store) access is valid

- Cloudflare token: **active / valid**.
- `patala` bucket: 87 source objects already content-addressed (SHA-256) — Agent 2's Atlas is progressing.
- `sanskritree` bucket holds `globalgoal` (the convergence directive) — now saved to `docs/global/globalgoal.md`.

### 5. The convergence directive is saved to global

- `docs/global/globalgoal.md` (the full R2 source, 1041 lines)
- `docs/global/agent1atlas.md` (my structured reformat)
- `devpaths/agent1atlas-reaction.md` (my analysis)

---

## ⚠ HONEST GAPS / PENDING — do not ignore these before devpath8

### G1. The real-corpus ARGMAP NAT gate is PENDING
- Only **1** committed ARGMAP map (kramasadbhava:v1), and it is clean.
- **6** findings still OPEN.
- Consequence: devpath8 synthesis can be built over **GOLD** arguments (valid), but its acceptance must
  NOT claim real-corpus validity until devpath3 consumes a real ARGMAP batch. Build on gold; label honestly.

### G2. devpath7 (the canonical graph contract) is spec-only, not implemented
- The Pydantic discriminated-union DSO fix (`PropositionContent` etc.) exists **only** in
  `docs/vision/atlas/technical-architecture-v1.md` §27–31 — **not in code**.
- My devpath4 `proposition_layer.py` and the Atlas `PropositionContent` are **two different field shapes**
  and are NOT yet reconciled.
- Consequence: **devpath8's `ArgumentSynthesis` should not be built before devpath7**, OR it will
  duplicate the content contract (the exact duplication the directive warns against). **devpath7 is the
  hard prerequisite, not optional.**

### G3. devpath2 (G2 correction loop) still blocked on Agent 2
- The 6-finding bundle is frozen, but `factory_rebuild(cidgagana:v1)` has not run.
- This does not block synthesis-over-gold, but it must be tracked (it affects real-corpus propositions).

---

## ◆ THE DECISION

| Question | Answer |
|---|---|
| Is the epistemic core (devpaths 1–6) built right? | **YES** — all tests pass, chain is coherent, NAT harnesses run. |
| Is the base verified for REAL-corpus synthesis? | **NO** — ARGMAP NAT gate is pending (G1). Gold synthesis is valid. |
| Is the content contract ready for synthesis? | **NO** — devpath7 reconciliation not done (G2). |
| Should we build devpath8 now? | **NOT yet** — do **devpath7 first** (reconcile + implement the typed contract), then devpath8 over gold. |

---

## ◆ THE CONFIRMED NEXT MOVE

**devpath7 (CANONICAL GRAPH CONTRACT)** is the confirmed next step, not devpath8. It is the last
schema-unification task: implement the typed DSO (Pydantic discriminated union) + vector authority from
`technical-architecture-v1.md` §27–31, AND reconcile my devpath4 `proposition_layer.py` to the Atlas
`PropositionContent`. Only then does devpath8 (synthesis) build on a clean contract.

This matches the globalgoal's own ordering: *"devpath7 = canonical object convergence contract, then
devpath8 = ArgumentSynthesis."*

---

## References

- `docs/global/globalgoal.md` / `agent1atlas.md` — the convergence directive
- `docs/vision/atlas/technical-architecture-v1.md` §27–31 — the already-written contract spec
- `devpaths/agent1atlas-reaction.md` — my analysis (G2 = the real devpath7 scope)
- `devpaths/devpath7.md`, `devpath8.md` — the next routes
