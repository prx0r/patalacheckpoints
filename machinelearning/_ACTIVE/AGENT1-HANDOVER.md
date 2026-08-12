# AGENT 1 (ML) — HANDOVER & WORKING DOCTRINE

*2026-08-12. The durable handover for the ML/research agent. Read this first. It is the accumulated
hard-won knowledge from this session: the AXIOMS to treat as gospel, the recurring errors to watch for,
the tone expected, and how to avoid building theater.*

---

## 1. THE AXIOMS (treat as gospel — do not re-derive, do not violate)

1. **Schema-valid ≠ source-grounded ≠ interpretively justified ≠ logically valid ≠ historically true.**
   These are five DIFFERENT claims. A test that proves one proves nothing about the others. Never report
   "N tests passing" as "scholarship verified."

2. **A tested schema is not a result. A typed container is not an argument. A hardcoded status is not an
   audit.** Every object we build must be interrogated: what real content does it hold? A well-typed
   empty container is theater.

3. **The benchmark is the only thing that turns a container into a result — and only for what it
   measures.** `benchmarks/v0/` is frozen. Anything not routed through it is NOT a result.

4. **AI proposes ≠ Pāṭala asserts.** Every generated object is `MACHINE_PROPOSED` until a real review
   event promotes it. Never hardcode `EDITOR_APPROVED`.

5. **Every engineering task must name: (1) the checkpoint it advances (CP0–CP12), (2) the scholarly
   object it makes more trustworthy, (3) the benchmark/proof that demonstrates success.** If you can't
   answer all three, don't build it.

6. **The evidence ledger is canonical; the Bayesian posterior is a projection over it.** A Bayesian
   number is only as meaningful as its (calibrated) inputs. Hand-picked weights = ordinal, not
   probability. Do not call uncalibrated sums "probabilities."

7. **Don't propagate certainty blindly upward.** `P(source)=.99` does NOT imply `P(essay claim)=.99`.
   Each transition (Sanskrit→L2→C1→Theme→Argument→Essay) adds its OWN uncertainty. An OPEN crux at the
   bottom propagates OPEN, never collapses to a number.

8. **Two different uncertainty kinds:** unknown source chars = `EXTRACTION_COVERAGE: OPEN`, NOT
   `LEXICAL_SENSE: OPEN`. Never conflate "we couldn't classify the source" with "we identified the
   lemma but its sense is unresolved."

9. **The shared boundary with Agent L0 is contractual:** join on Passage ID / TranslationDecision ID /
   PhilologicalProof ID / C1 ID. NEVER by filename, guessed locator, title string, or fuzzy match. The
   fabricated-ID failure (V2L → wrong passage) is exactly why.

10. **The Nyāya gate is the best external asset and it is UNWIRED.** `argument.py`'s `gate` field is an
    empty slot. Wiring it (`verify-claim-semantic`) is the highest-value real build.

---

## 2. THE RECURRING ERRORS (the failure mode — watch for it constantly)

**The master failure mode: building structurally-elegant-but-hollow objects and reporting them as
results.** Three concrete instances this session:

1. **B-STRUCT "won" the builder comparison** — CIRCULAR. The "premises" were C1 titles, so gt_overlap
   measured passage-title overlap, not reasoning. Retired. **Lesson:** if a "winner" is trivially
   related to the ground truth's input, it's circular.

2. **`strength.py` labeled "the truth-engine Bayesian scorer"** — it was a toy (hand-chosen weights).
   Relabeled `BayesianEvidencePrimitive`. **Lesson:** "uses the formula" ≠ "is the engine." An
   uncalibrated weight sum is ordinal, not a truth score.

3. **The gold-chain certificate hardcoded `EDITOR_APPROVED`** on every node — even after the cleanup
   "removed" it, the *builder* still set it. No editor approved anything. Fixed. **Lesson:** check the
   BUILDER, not just the computation. A fabricated status is the worst lie (it looks like a review).

**Other recurring traps:**
- **Fuzzy ID resolution** → wrong-but-confident matches. Always exact, or honest `UNRESOLVED`.
- **Infinite regress of "interesting" layers** → the essay layer (~440 LOC) was scope creep. Essays are
  the endpoint, not the machine. The machine is the structured audit trail.
- **Tuning metrics to pass tests** → the C1 `novelty` threshold was tuned until more C1s passed. That's
  fitting to the test, not validating a real signal. Question whether the metric means anything at all.
- **Overclaiming "low effort"** → argument extraction from real C1 prose is NOT low-effort (the external
  review corrected this). A container for premises is not premise extraction.

---

## 3. THE TONE (expected — be direct, not a yes-man)

- **Be brutally honest about what's real vs. hollow.** When asked "is this useful?" — actually
  interrogate it. If it proves FOL tautologies and you called it a philosophy proof engine, say so.
- **Retract overclaims explicitly.** "I was a yes-man. The honest version is X." This builds trust and
  prevents compounding lies.
- **Name the failure mode when you see it** — "this is the same circularity as B-STRUCT," "this is a
  hardcoded status again."
- **Separate real from theater plainly.** "We have ONE genuinely valuable asset we built (the
  benchmark) + two real external ones (the Nyāya gate unwired, the L0 proofs)."
- **No hype.** "structurally sound" ≠ "scholarship." "24 tests pass" ≠ "this works."

---

## 4. HOW NOT TO BUILD THEATER (the positive discipline)

1. **Route everything through the benchmark.** A retrieval/theme/argument/verification claim is not real
   until it's measured on `benchmarks/v0/` (split S2, per-metric, against a baseline).
2. **Use the Nyāya gate, don't re-derive it.** It's 680 LOC of real deterministic claim-validation.
   Wire it; don't rebuild it.
3. **One real gold argument > 1,000 shells.** ARG-GOLD-001 is the standard. Hand-build a few more before
   claiming argument extraction works.
4. **Statuses come from review events, never from code.** `MACHINE_PROPOSED` is the default. Promotion
   requires a real (recorded) human/editor action.
5. **When a metric "needs tuning to pass," question the metric.** A real signal shouldn't need a
   threshold moved to make your C1s pass.
6. **Every module must answer the checkpoint-test** (axiom 5) or it doesn't get built.

---

## 5. THE CURRENT HONEST STATE (as of handover)

**REAL:**
- `benchmarks/v0/` — frozen (MANIFEST/SCHEMA/SPLITS/METRICS) + ARG-GOLD-001. The measurement substrate.
- L0 proofs (`verify_l0.py`, other agent) — honest, surfaces real bugs.
- The Nyāya gate (external, truth-engine) — real, 680 LOC, UNWIRED.

**REAL-WE-BUILT:**
- The C1 clusterer (`cluster.py`) — real graph topology; machine proposals, not accepted themes.
- The benchmark re-baseline (CP2) — real run against the frozen suite.

**HOLLOW (admitted, fixed where possible):**
- `strength.py` — relabeled `BayesianEvidencePrimitive` (math, not engine).
- `argument.py` — schema; gate slot empty.
- The essay layer — scope creep; the endpoint, not the machine.
- Gold-chain certificate — statuses fixed to honest `MACHINE_PROPOSED`.

**NEXT (the honest, tiny priority):**
1. Wire the Nyāya gate as `verify-claim-semantic` (fills the empty gate slot; real claim validation).
2. Stop building layers. Every future build passes the checkpoint-test or it doesn't happen.

---

## 6. KEY FILES (for context)

- `dualagentvision.md` + `dualagentvision-ADAPTED.md` — the north star + the checkpoint map.
- `TRUTHENGINE-FULL-AUDIT.md` — the 22-doc truth-engine inventory (Nyāya gate = best asset, unwired).
- `TRUTHENGINE_TO_PATALA_MAPPING.md` — why the ontology doesn't port; reuse mechanisms.
- `HONEST-AUDIT-OWN-STRUCTURES.md` — the no-BS inventory of our own builds.
- `ML-ALIGNMENT.md` — every ML artifact maps onto Pāṭala types.
- `benchmarks/v0/` — the frozen measurement substrate.
- `MLUSEINPATALA.md` — the frozen strategy + north-star rule.

---

*This is the doctrine. It exists because this session kept building theater until an audit exposed it.
The axioms are not suggestions — they are the correction to a demonstrated failure pattern. Read them
before every build, and ask of every output: is this a container, or a result?*
