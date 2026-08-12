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
| **P0 source coverage** | did we account for every source char? | ✅ **REAL** — V2/V3 35/35 lossless, frozen |
| **P2 morphology** | is the grammar linguistically plausible? | ✅ **CALIBRATED** — ensemble done, blind review pending |
| **P3 lexical sense** | what does the word MEAN here? | ⏳ gold + baselines done; ranker rejected |
| **P4 alignment** | which Sanskrit ↔ which English? | ⬜ next |
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

**Done:** P0 real & frozen. P2 calibrated (ensemble: 85% control, 72% conflict-resolve). P3 gold v0 +
baseline eval (ranker rejected, embedding baseline 0.81 is the floor).

**In flight:** background ensemble enriching the V+/H- cell (should finish soon).

**Next (no human needed):**
1. Finalize P2 with the enriched ensemble.
2. **P4 alignment benchmark** — but scoped correctly: the L0 gloss↔iast pairs are aligned *by
   construction*, so the real P4 question is L0↔L2 (published prose) alignment. That's the meaningful one.

**Human gates (logged, non-blocking):**
- Fill the 150 genuinely-blind P2 cases → freeze P2 as human-validated.
- Editor the 21 enriched P3 fixtures → promote to gold.

**Bigger-picture next (after the floor is solid):** pivot the same proof machinery toward the
high-visibility product — Pāṭala Review (Vision 06) — because that's what makes the project valuable to
scholars, not just sound.
