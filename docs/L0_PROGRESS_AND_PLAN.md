# WHERE WE ARE & THE PLAN — what we're building and why

*2026-08-12. A plain-language map so anyone (including us) can see what the L0 work is for and what's
next. The problem being solved, the proof ladder, current status, and the plan.*

---

## The problem (why the L0 work exists)

Pāṭala's whole claim is that its scholarship is **verifiable** — that a translation can be traced to its
Sanskrit source, with interpretation explicitly marked. That claim is only as strong as its weakest
foundation. If the bottom layers (did we capture the source? is the grammar right? does the word mean
what we say?) aren't proven, then every essay/theme/argument above them is built on sand.

So we build a **proof ladder** — each layer makes one kind of claim *provable* rather than *asserted*.

## The proof ladder (CP1, from dualagentvision.md)

| Layer | Question | Status |
|---|---|---|
| **P0 source coverage** | did we account for every source char? | ✅ **REAL** — complete IPVV **63/63** lossless (V2/V3 35/35 + V1 legacy 28/28), frozen |
| **P2 morphology** | is the grammar linguistically plausible? | ✅ **CALIBRATED** — ensemble done, blind review pending |
| **P3 lexical sense** | what does the word MEAN here? | ⚠️ gold + baselines done; ranker rejected (P-012) |
| **P4 alignment** | which Sanskrit ↔ which English? | ✅ **SUPPORTED_MACHINE_WITNESS** (P-013) — frozen: 0.93/0.89/1.0 + Vidyut 0.81 |
| **P5 syntax** | agent/patient/negation roles | ⬜ later |

## The anti-theatre discipline (why reviews keep happening)

Per `AGENTS.md`: **code existing ≠ capability existing.** Each layer must earn its status via
*gold → baseline → evaluation → honest label*, not "I wrote a script." External reviews keep catching us
overclaiming — and they're right. The review discipline is what makes the eventual product credible.

## Where the value is

- **Low-visible but foundational:** the proof ladder (what we're building now). Makes the substrate
  trustworthy — the ML lane and every scholar-facing feature depend on it.
- **High-visible:** the product features (Vision 06–08: Pāṭala Review APIs, scholar workbench). These
  are what scholars actually use — but they'd be hollow without the proof floor.

## Current status + the plan

**Done (the CP1 proof ladder):**
- **P0 — complete IPVV 63/63 lossless + FROZEN.** V2/V3 35/35 + **V1 legacy 28/28** (via
  `pipeline/extract_l0_v1.py`, `verify_l0.py` unchanged).
- **P2 calibrated + frozen as witness (P-011).** Vidyut×Heritage ensemble: 84–85% control, 72%
  conflict-resolve, ~9% true double-conflict. Blind 160-case review built, unfilled (non-blocking).
- **P3 gold v0 + baselines; ranker REJECTED (P-012).** ranker.py 0.76 < embedding 0.81, 0 abstention.
- **P4 alignment — SUPPORTED_MACHINE_WITNESS (P-013), FROZEN.** L0↔L2 term-anchor: 0.93 recall / 0.89
  precision / 1.0 abstain, + independent Vidyut witness 0.81 analyzed-only. Frozen per the adequacy
  doctrine — do not keep tuning.

**Next (in order):**
1. **P2 blind review** (160 cases) → VALIDATED_AGAINST_HUMAN_GOLD (P-011 promotion) — non-blocking.
2. **Deterministic related-rail** — `/api/recommend` + `recommend_related` MCP.
3. **Cross-work ingestion demo** (later) — ingest a second real work to demonstrate/confirm L0
   generalization; do NOT build a generic ingestion framework until then.

**Human gates (logged, non-blocking):**
- Fill the genuinely-blind P2 cases → freeze P2 as human-validated.
- Editor the P3 fixtures → promote to gold (P3 remains a candidate; embedding 0.81 is the floor).

**Bigger-picture next (after the floor is solid):** pivot the same proof machinery toward the
high-visibility product — Pāṭala Review (Vision 06) — because that's what makes the project valuable to
scholars, not just sound. And the critical path moves UPWARD: ARG-001..005 review, the vertical
Proposition→Sanskrit object, and the first external evaluator.
