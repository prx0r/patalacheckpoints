# SPEC — EPISTEMIC EVIDENCE PROPAGATION

*2026-08-12. The contract for how evidence propagates to claims in Pāṭala. This is the precondition
for any full Bayesian/graphical implementation (Option A). Until this spec is satisfiable with real
data, the evidence LEDGER is canonical and any posterior is a *projection* over it.*

---

## 1. What a probability means (the discipline)

A number like `0.83` is ONLY meaningful if it answers:

> Given these explicit assumptions and the observed evidence, how strongly is THIS claim supported?

It does NOT mean *"the claim is true."* Three legitimate modes:
1. **EMPIRICAL CALIBRATION** — learned from adjudicated benchmark data (`P(correct | Vidyut agrees)`).
2. **EXPLICIT EXPERT PRIORS** — with sensitivity analysis (show not a prior artifact).
3. **ORDINAL EVIDENCE ONLY** — a ranked ledger, NOT called a probability.

**Until calibrated, we are in mode 3 (ordinal).** We do not call `weighted_lbf` sums "probabilities."

---

## 2. Evidence classes (Pāṭala-specific, NOT the TruthEngine's F1–F8)

| Evidence class | What it is | Example |
|---|---|---|
| **PHILOLOGICAL** | morphology/syntax/alignment licenses a parse | "Vidyut licenses our lemma" |
| **PARALLEL** | same-author or cross-tradition usage supports | "TĀ uses vimarśa the same way" |
| **CONTRADICTING** | a witness/parser/manuscript favors a rival | "manuscript B favors reading Y" |
| **INTERPRETIVE** | C1 reconstruction / editorial reading | "C1 reads this as the order-less support" |
| **HUMAN** | an editor/specialist adjudicated | "editor accepted the reading" |

Each is a DIFFERENT epistemic object. They do not share identical weights.

---

## 3. Where weights come from (the honesty rule)

| Weight source | Status |
|---|---|
| hand-picked ("feels reasonable") | ❌ DECORATIVE — do not call it calibrated |
| learned from adjudicated benchmark | ✅ legitimate (empirical calibration) |
| explicit expert prior + sensitivity analysis | ✅ legitimate |
| ordinal rank only (no numeric Bayes factor) | ✅ legitimate (mode 3) |

**If a weight has no justified interpretation as an evidence likelihood ratio, do not feed it to a
Bayesian update.**

---

## 4. Independence assumptions

Bayesian combination assumes (or should declare) independence of the evidence contributions. For
scholarship this is often FALSE:
- Vidyut + Heritage agreeing is NOT two independent pieces (both are Sanskrit parsers).
- Two passages from the same vimarśa are NOT independent.

The `w_dep` paradigm-crowding (from the TruthEngine) is one attempt to handle this — REUSE GENERICALLY.
But it must be stated per-class, not global.

---

## 5. Contradictory evidence (must not silently vanish)

A claim's ledger always carries BOTH supporting and contradicting evidence. The propagation must expose
tension, not smooth it. `- manuscript B favors Y` is data, not noise.

---

## 6. Branches (alternative readings)

Pāṭala has "alternative readings" as a real concept (e.g. two plausible translations). A branch is a
coherent alternative interpretation. Branches exist only where Pāṭala actually has them — do NOT port
the TruthEngine's B1–B6 metaphysics branches.

---

## 7. How review affects evidence

- `MACHINE_PROPOSED` evidence carries less weight than `EDITOR_ACCEPTED`.
- Review does not change the *ledger* (the evidence stays recorded); it changes the *weight/status*.
- `OPEN` evidence is visible, never hidden, never silently resolved.

---

## 8. How OPEN propagates (the non-collapse rule)

An OPEN crux at a lower layer propagates UP as OPEN at every dependent claim. It is never collapsed
into a number. The gold-chain certificate already does this per-dimension (SOURCE_INTEGRITY /
MORPHOLOGY / LEXICAL_SENSE / ...); the propagation spec extends it to claims.

---

## 9. Uncertainty must not silently disappear upward

Each transition adds its own uncertainty:
```
Sanskrit → L2 (philological) → C1 (interpretive) → Theme (synthesis) → Argument (inferential) → Essay
```
`P(source) = .99` does NOT imply `P(essay claim) = .99`. Every arrow needs its own uncertainty source.

---

## 10. The benchmark discipline

Before deploying any propagation engine, compare against simple baselines on the frozen benchmark:
```
BASELINE 1 count supporting vs contradicting
BASELINE 2 hand-weighted score
BASELINE 3 logistic regression
MODEL 4     Bayesian evidence propagation
MODEL 5     graphical model
```
Metrics: **Brier · log loss · calibration error · AUROC · reliability plots.**
If the engine loses to logistic regression, don't deploy it.

---

## 11. The naming

Call this the **Epistemic Evidence Engine** (not "truth engine"). It answers "how strongly supported is
this claim, given explicit assumptions and observed evidence?" — not "is this true?"

---

## 12. The gated path to a full engine (Option A)

Only build the full engine after:
1. `TRUTHENGINE_TO_PATALA_MAPPING.md` gives a rigorous Pāṭala semantics to each component (it does NOT
   for F1–F8/D1–D5/B1–B6 now).
2. This spec is satisfiable with real data (weight provenance + independence + OPEN).
3. The benchmark has enough adjudicated data to calibrate likelihoods.

Until then: **the evidence ledger is canonical; the Bayesian posterior is a projection over it.**
