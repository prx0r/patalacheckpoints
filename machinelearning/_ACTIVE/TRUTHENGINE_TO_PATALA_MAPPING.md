# TRUTHENGINE → PĀṬALA MAPPING

*2026-08-12. The hard question: does the full TruthEngine's ontology fit Pāṭala? This forces every
component to justify itself before any port (Option A). **The rule: "full Bayesian implementation" does
not make the epistemology valid — it only makes the implementation complete.** If a component has no
rigorous Pāṭala semantics, do not port it merely for completeness.*

---

## 0. The current honest state

- `strength.py` = **BayesianEvidencePrimitive** (relabeled): the `weighted_lbf` formula + the
  `Certainty` mapping. It is a *projection* over evidence, NOT the TruthEngine and NOT a truth claim.
- The full TruthEngine (`truthengine-propagation.py`) has: FeatureState (F1–F8), ClaimRecord,
  PropagationDB (persistence), discriminators (D1–D5), branch derivation (B1–B6), PropagationEngine.run().
- **None of F1–F8/D1–D5/B1–B6 are ported.** They were designed for a *metaphysics-comparison* engine
  (which filling of `S` is best). Porting them wholesale into philological/argumentative scholarship
  would produce an elaborate score with no defensible interpretation.

---

## 1. The component-by-component verdict

| TruthEngine object | Original meaning | Pāṭala candidate meaning | Defensible? |
|---|---|---|---|
| **F1–F8 (features)** | metaphysical features of `S` (consciousness-fundamental, pattern-space-real, teleology, cross-life continuity...) | textual/grammatical/parallel support? | **NO** — these are metaphysics-contest axes, not philological evidence classes |
| **D1–D5 (discriminators)** | eliminative binary questions pruning B1–B6 | rival-reading discriminators? | **PARTIAL** — the *eliminative-question* idea maps to Pāṭala's questionnaire (CORE shapes), but the specific D1–D5 content does not |
| **B1–B6 (branches)** | candidate fillings of `S` | alternative interpretive branches? | **PARTIAL** — "alternative readings" is a real Pāṭala concept, but B1–B6's specific metaphysics content is wrong |
| **FeatureState** | log-odds state per feature | log-odds state per evidence class | **REUSE GENERICALLY** (the mechanism, not the features) |
| **ClaimRecord** | a claim with weighted_lbf + paradigm | a philological/argument claim | **REUSE GENERICALLY** |
| **PropagationDB** | persistence protocol | persistence | **REUSE AS-IS** (mechanism) |
| **paradigm-crowding (w_dep)** | down-weight same-paradigm claims | down-weight same-tradition/same-source claims | **REUSE GENERICALLY** (anti-double-counting is real) |
| **branch probability derivation** | product of feature probs per branch | — | **NO** (until branch semantics fit) |
| **PropagationEngine.run()** | full/incremental propagation | the update engine | **REUSE GENERICALLY** (the mechanism) |

**Verdict:** The TruthEngine's **mechanisms** (FeatureState log-odds, ClaimRecord, PropagationDB,
paradigm-crowding, the update loop) are generic and reusable. Its **ontology** (F1–F8, D1–D5, B1–B6)
is metaphysics-specific and does NOT fit Pāṭala's philological/argumentative scholarship. **Porting the
ontology would replace a small overclaim with a much larger one — do not.**

---

## 2. What Pāṭala actually needs: a domain-neutral Evidence Propagation Engine

Not "port TruthEngine." Build a generic engine with Pāṭala-specific *adapters*:

```
PropagationEngine
├── EvidenceLedger      (the canonical record — supporting + contradicting + dependencies)
├── ClaimGraph          (claims + their relations)
├── BranchGraph         (alternative readings — when Pāṭala actually has them)
├── calibration adapter (weights from adjudicated data, not hand-feel)
├── update engine       (the propagation mechanism)
└── sensitivity analysis
```

Pāṭala supplies domain-specific features through adapters:

**PHILOLOGICAL CLAIM** ("X is the correct parse"):
```
Evidence:
+ morphology licenses X
+ syntax licenses X
+ parallel usage supports X
- manuscript B favors Y
- Heritage parser favors Y
```

**ARGUMENT CLAIM** ("P1 supports C"):
```
Evidence:
+ explicit connective
+ C1 reconstruction
+ human adjudication
- scope mismatch
- implicit premise required
```

These are DIFFERENT epistemic objects. They should NOT use identical feature weights.

---

## 3. The likelihood-semantics problem (the deepest issue)

Calling something "Bayesian" because it sums weighted log-Bayes factors is only meaningful if
`+2.1`, `-0.8`, `+1.4` have a justified interpretation as evidence likelihood ratios.

**Where did the weights come from?** If "morphological agreement = +2, parallel = +1.5, editor = +3"
because it "felt reasonable," the Bayesian machinery is **decorative**.

Three legitimate options:
1. **EMPIRICAL CALIBRATION** — learn likelihoods from adjudicated benchmark data
   (e.g. `P(correct | Vidyut agrees)` from 500 reviewed decisions).
2. **EXPLICIT EXPERT PRIORS** — with sensitivity analysis (show the result isn't an artifact of the prior).
3. **ORDINAL EVIDENCE ONLY** — don't call them probabilistic Bayes factors; treat them as a ranked
   ledger, not calibrated probabilities.

Until one of these holds, the evidence ledger is canonical and the Bayesian posterior is a *projection*
over it — replaceable if the statistical model changes, without touching the scholarship.

---

## 4. Do not propagate certainty blindly upward

Each transition introduces its OWN uncertainty source:
```
Sanskrit      → T1 philological uncertainty
L2            → T2 interpretive uncertainty
C1            → T3 synthesis uncertainty
Theme         → T4 inferential uncertainty
Argument      → T5 rhetorical/synthesis uncertainty
Essay
```
`P(source reading) = .99` does NOT imply `P(interpretation) = .99`. The interpretation is a new
uncertain transformation. Every transition needs its own uncertainty source.

---

## 5. When the full Bayesian/graphical model becomes genuinely valuable

Once the benchmark has enough adjudicated examples:
```
P(correct reading | Vidyut agrees)
P(correct reading | Vidyut + Heritage agree)
P(correct reading | morphology disagrees)
P(correct reading | strong same-author parallel)
P(correct reading | external translators disagree)
```
Then actual data calibrates the evidence contributions — and the derivation graph (which already
exposes dependencies) is a natural probabilistic-graphical-model substrate:

```
            Morphology
           ╱          ╲
Source → Segmentation   Syntax
           ╲          ╱
             Reading
               ↓
             Claim
```

But this is only real with observed adjudication data. Before that, it's decoration.

---

## 6. The benchmark discipline (does the engine even help?)

Compare the Bayesian engine against simpler baselines on the frozen benchmark:
```
BASELINE 1  count supporting vs contradicting evidence
BASELINE 2  hand-weighted score
BASELINE 3  logistic regression
MODEL 4     Bayesian evidence propagation
MODEL 5     graphical model
```
Measure: **Brier score · log loss · calibration error · AUROC · reliability plots.**
If the giant propagation engine loses to logistic regression, don't deploy it. That's science.

---

## 7. The naming correction

Do not call any of this a "truth engine" inside Pāṭala. Call it the **Epistemic Evidence Engine** (or
**Evidence Propagation Engine**). It answers:

> Given these explicit assumptions and observed evidence, how strongly supported is this particular claim?

Not: *Is this claim true?*

---

## 8. Immediate action (B — done) + gated future (A)

**Now (B):** `strength.py` is relabeled `BayesianEvidencePrimitive`, with an honest scope declaration
(see its docstring). Its tests still validate the math (the formula is correct); they no longer imply
"scholarship correctness."

**Gated (A):** do NOT port the full TruthEngine ontology (F1–F8/D1–D5/B1–B6) until:
1. This mapping finds a rigorous Pāṭala semantics for each component (it does not for the ontology now).
2. A `SPEC_EPISTEMIC_PROPAGATION.md` defines what a probability means, where weights come from, the
   independence assumptions, and how OPEN propagates.
3. The benchmark has enough adjudicated data to calibrate likelihoods.

Until then, the **evidence ledger is canonical**; the Bayesian posterior is a projection over it.
