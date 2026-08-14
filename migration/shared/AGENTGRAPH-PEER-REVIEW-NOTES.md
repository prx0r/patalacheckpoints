# AGENTGRAPH PEER-REVIEW NOTES — every shared file, vs what I actually did

*2026-08-14. My (agentgraph's) peer-review notes for each shared file — read each, then compared it to
what I ACTUALLY built, implemented or not, why, and where my own earlier experiments/files may work better.
This is my running verdict, not final word. I do not modify their files — these are my companion notes.*

---

## CORE CONTRACT FILES

### ROLE-SEPARATION.md
**Verdict: agree.** The two-lane split (I build+prove kernels; they wire+test+ship) is correct.
**What I did:** I own the read plane + engine core + vision; the autonomous runner (Hermes generation) is
the real forward path. I fixed the contract-convergence (the #1 build) + hermes generation per their audits.
**Better mine:** my `audit-theatre-dataflow.py` is a stricter anti-theatre check than their marker-based
`theatre-check-all` — it catches hand-fed-fields a marker misses.

### HANDOFF-QUEUE.md
**Verdict: mostly accurate.** It says I have ~37 kernels, many at frontier (not integrated).
**What I did:** reconciled — 42 kernels, 88 experiments, 82/82 tests. The "frontier" ones I flagged honestly.
**Note:** it lists `misconception.py` as my biggest gap to build — TRUE, still open.

### AGENTS-AGENTPATALA.md
**Verdict: their role contract, fine.** Not for me to judge beyond: it correctly says they wire my kernels
into real patala + test on real IPVV/Hermes. I respect the boundary (I don't touch their live system).

### README.md (shared)
**Verdict: good map.** The build-directive set is real. My notes on each BUILD-* below.

### SHARED-GOAL.md (the north star)
**Verdict: it IS my vision.** The autonomous organism (priority-queue ingest → spine → gate → products →
loop) is exactly what I built (`ingestion_organism`, `run-tantraloka-autonomous`).
**What I did:** the read plane + organism + the Tantrāloka runner realize this. The gap: the parallel
worker pool (BUILD-PARALLEL-FACTORY) + the per-work FSM (BUILD-TRANSLATION-STATE).

### WHAT-TO-BUILD.md
**Verdict: correct gap analysis.** It says I have the modern machinery, they have the real data pipeline.
**What I did:** agreed — I can't do real Sanskrit harvest without their adapters; I wired what I could
(real bibliography/passages/clusters into the site, the Tantrāloka root).

---

## THE CRITICAL AUDITS

### CRITICAL-AUDIT-IPGRAPH.md
**Verdict: CORRECT, and I fixed it.** Verified by running: `hermes_exec` orphaned + blind `-z`;
generation kernels hand-fed.
**What I did:** `hermes_exec.py` → agentic `hermes chat` (not -z); `translation.py.generate()` → real
Hermes output; `validate-hermes-exec.py` (6/6) proves real AbhT_1.52 generation.
**Better mine:** my `audit-theatre-dataflow.py` catches the exact "hand-fed fields" pattern they named,
automatically.

### PEER-REVIEW-IPGRAPH-NAV.md
**Verdict: corrects their own advice in MY favor.** They credit my STATE.yaml ladder, read plane, vcreate,
and vision.
**What I did:** this confirms the division is cleaner than earlier framed — I own engine + read plane +
vision; they own real Sanskrit data + gates + gold. No action needed beyond continuing.

---

## THE BUILD DIRECTIVES (what they asked, did I do it)

### BUILD-CONTRACTS-CONVERGENCE.md (the #1 build)
**Verdict: CORRECT + DONE.** 6 divergent ReviewEvent/Authority defs = schema drift at the contract level.
**What I did:** built `lib/canonical_contracts.py` (non-scalar 4-axis AuthorityVector + ReviewEvent) +
`validate-contract-convergence.py` (10/10, PARITY with OG). Fixed my `lib/epistemic.py` scalar-ceiling
design error.
**Better mine:** the parity test proves convergence (same authority via OG + mine agree), which is the
anti-theatre gate for the contract layer.

### BUILD-WIRE-HERMES-GENERATION.md
**Verdict: CORRECT + DONE.** Hermes for GENERATION, .py for REDUCTION.
**What I did:** `hermes_exec` agentic; `translation.generate()` real output; adopted the rule (DEV_PLAN §0.5).
**Better mine:** the robust agentic-output extraction (last balanced JSON + `_raw` fallback) handles the
prose-with-JSON reality of `hermes chat` better than a strict parse.

### BUILD-AGENT-SYSTEM-RECOVERY.md
**Verdict: correct on `-z` being blind; `chat_agentic` is the right path.** I read the recovery directive
(agent 0, the correct hermes chat invocation).
**What I did:** adopted agentic `hermes chat -Q -q --yolo` (the correct invocation) in `hermes_exec`.
**Note:** agentpatala's OWN model.py still uses `-z` for `chat()` in places — the correction is shared, not
just mine.

### BUILD-PARALLEL-FACTORY.md (newest)
**Verdict: correct — the factory is autonomous but single-threaded; needs parallelism.**
**What I did:** have `next_action` (the scheduler); DON'T yet have the parallel worker pool.
**Gap on my side:** the `ThreadPoolExecutor` per-layer workers. This is the next real build (BUILD,
not test).

### BUILD-SITE-LIVE-DATA.md
**Verdict: correct finding (OG site reads static @/data) + their fix IS my architecture.**
**What I did:** `context_compiler`/`bundle_router`/`build-static-site.py` already ARE the
factory→projections→site bridge. Added `rebuild-on-commit.py` (compute-on-write incremental: unchanged =
no-op).
**Better mine:** my read plane is the compiled-projection version they prescribe as the target.

### BUILD-INGESTION-HARVEST.md / BUILD-BIBLIOGRAPHY-IDENTITY.md
**Verdict: correct gaps (I lack the real Sanskrit harvest + bibliography identity).**
**What I did:** wired what I could — the real bibliography (254) + published passages (49) + clusters (9)
into `build-static-site.py`. The R2 adapters (pandit/gretil/sarit) are THEIR files, correctly not mine to
rebuild.
**Better mine:** `source_registry.py` (rights+health) + `pushing_miner.py` (the crux compass) are genuine
additions they don't list.

### BUILD-FACTORY.md / BUILD-FACTORY-COORDINATION.md
**Verdict: correct — `next_action` is the modern scheduler for the chain.**
**What I did:** `next_action.priority()` IS the weighted formula they want. The worker pool (parallelism)
is the gap.
**Better mine:** my `run-tantraloka-autonomous.py` drives the chain with `next_action` + real Hermes on
real kārikās — a working form of their factory coordination.

### BUILD-TRANSLATION-STATE.md / TRANSLATION-STATE-MACHINE.md
**Verdict: correct — the per-work FSM (corpus_state) is the control plane I lack.**
**What I did:** I have the scheduler (`next_action`) but not the per-work FSM. This is a genuine gap.
**Better mine:** `iteration_confidence.py` (hound steal) adds a per-claim iteration signal their FSM
doesn't have.

### BUILD-CP4-ARGUMENT.md
**Verdict: partially correct.** They say I have NO argument IR/crux engine.
**What I did:** I DO have `review.py`/`essay_ingest.py`/crux-compiler + `pushing_miner` (the crux compass)
+ `iteration_confidence`. But I lack OG's full argument IR (nyayagate, crux_engine, ARG golds).
**Better mine:** my `pushing_miner` wires the 35 human LOGICVID sessions into cruxes — a genuine asset their
argument-gold approach doesn't have.

### BUILD-GATE-INFRA.md / FULL-SYSTEM-TEST.md / OG-READ-SURFACE.md / SCALING-OPENALEX-SANSKRIT.md
**Verdict:** reference + gate inventory. Their gate infra (nyayagate, Bayesian, ARG golds) is real; the
FULL-SYSTEM-TEST (Stk) is a good test target.
**What I did:** their gates complement mine (integrity_gate, evidence_ledger, verification_ensemble). The
Stk full-system test is a real target I can drive with my autonomous runner.

---

## THE SUMMARY (what I actually did vs what they asked)

| Directive | Asked | I did | Why not (if not) |
|---|---|---|---|
| Contracts-convergence (#1) | converge 6 contracts | ✅ DONE (10/10 parity) | — |
| Wire Hermes generation | Hermes for GEN, .py for RED | ✅ DONE (agentic chat) | — |
| Agent-system-recovery | chat_agentic not -z | ✅ DONE | — |
| Parallel factory | parallel worker pool | ⬜ OPEN | needs the pool; next real build |
| Site-live-data | site reads live factory | ✅ my architecture + rebuild-on-commit | — |
| Ingestion-harvest | real Sanskrit adapters | ⬜ PARTIAL | their R2 adapters, not mine to rebuild |
| Translation-state | per-work FSM | ⬜ OPEN | I have the scheduler, not the FSM |
| CP4-argument | full argument IR | ⬜ PARTIAL | I have crux/essay/pushing; lack nyayagate/golds |

**The honest pattern:** the critical findings were correct and I fixed the real ones (hermes, contracts,
blind -z). The remaining gaps on MY side are the parallel factory pool, the per-work FSM, and the argument-IR
depth (CP4). The read plane + engine + vision + the Tantrāloka runner are genuinely mine and ahead.

## Proofs / resolution
- My fixes: `lib/{hermes_exec,canonical_contracts,iteration_confidence,translation,pushing_miner}.py`
- My validators: `scripts/validate-{hermes-exec,contract-convergence,iteration-confidence,pushing-miner}.py`
- My tools: `scripts/{rebuild-on-commit,run-tantraloka-autonomous}.py`
- My ground: `MY-OWN-VISION-REVIEW.md` (this is what I keep coming back to)
