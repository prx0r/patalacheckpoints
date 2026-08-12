# COMPONENT CONTRACTS — the anti-theatre 9-field protocol, applied

*2026-08-12. Every component gets a 9-field contract. If any field is empty, the component is
`EXPERIMENTAL_INFRASTRUCTURE`, NOT a scholarly capability. Nothing is "real" because code exists.*

---

## The 9 fields
**NAME · INPUT · OUTPUT · AUTHORITY · GOLD · BASELINE · METRIC · FAILURE MODE · ADOPTION GATE**

---

## 1. argument.py
- **NAME:** `ArgumentProposal` container (Claim-v3 schema)
- **INPUT:** C1s / passages / a `gate` slot
- **OUTPUT:** a typed argument *container*
- **AUTHORITY:** machine (schema only)
- **GOLD:** ARG-GOLD-001..010 (only 001 exists)
- **BASELINE:** trivial (majority / no-extraction)
- **METRIC:** proposition recovery F1 · role macro-F1 · grounding precision · relation F1 · scope-fidelity error
- **FAILURE MODE:** cannot recover >60% of hand-gold propositions; false-grounding >5%
- **ADOPTION GATE:** 5–10 hand-gold arguments → extractor → blind eval → error analysis → independent review
- **STATUS:** `SCHEMA / CONTAINER` — represents an argument; does NOT reconstruct one

## 2. aifgraph.py
- **NAME:** AIF-informed argument graph (proposition/inference/conflict nodes)
- **INPUT:** propositions (currently none real)
- **OUTPUT:** a graph representation
- **AUTHORITY:** machine (serialization)
- **GOLD:** the argument-gold propositions (when they exist)
- **BASELINE:** — (representation; no capability claim yet)
- **METRIC:** node integrity + resolvability (structural)
- **FAILURE MODE:** holds invented propositions as if real
- **ADOPTION GATE:** real propositions enter it; then it's useful
- **STATUS:** `SERIALIZATION / REPRESENTATION` — legitimate infrastructure waiting for validated content

## 3. Essay machinery (essaygen/essayplan/essaysentence/essayverify/essay)
- **NAME:** essay representation + rendering infrastructure
- **INPUT:** accepted claims → argument graph → plan
- **OUTPUT:** provenance-carrying essay (JSON canonical)
- **AUTHORITY:** machine (prose), verifier (adversarial)
- **GOLD:** one gold essay (does not exist)
- **BASELINE:** — (endpoint, not the machine)
- **METRIC:** 100% claims represented · 0 unsupported · 0 boundary-erasure
- **FAILURE MODE:** prose invents claims; verifier is regex-only
- **ADOPTION GATE:** real accepted claims + verified argument graph + verified synthesis FIRST
- **STATUS:** `ESSAY REPRESENTATION / RENDERING INFRASTRUCTURE` — frozen, do not develop until real content

## 4. strength.py
- **NAME:** `BayesianEvidencePrimitive`
- **INPUT:** weighted log-Bayes factors
- **OUTPUT:** posterior-style strength UNDER STATED ASSUMPTIONS
- **AUTHORITY:** machine (math)
- **GOLD:** calibrated adjudicated outcomes (none)
- **BASELINE:** count-supporting-vs-contradicting · hand-weighted · logistic regression
- **METRIC:** Brier · log loss · calibration error · AUROC
- **FAILURE MODE:** a fancy number over an uncalibrated weight sum presented as truth
- **ADOPTION GATE:** calibration on adjudicated data; must beat simpler baselines
- **STATUS:** `UNVALIDATED EVIDENCE AGGREGATION HEURISTIC` — no epistemic role until calibrated

## 5. C1 metrics (c1metrics.py)
- **NAME:** C1 candidate diagnostics
- **INPUT:** C1 body + L2 + terms
- **OUTPUT:** scored metrics (novelty/boundary/hedge/...)
- **AUTHORITY:** machine (heuristic)
- **GOLD:** no human-graded C1 quality set
- **BASELINE:** — 
- **METRIC:** precision/recall of the heuristic vs human judgment
- **FAILURE MODE:** thresholds tuned to make C1s pass, not to measure a real signal
- **ADOPTION GATE:** benchmark the thresholds against human-graded C1s
- **STATUS:** `CANDIDATE DIAGNOSTICS` — thresholds unvalidated

## 6. The Nyāya gate (truth-engine's, to wire)
- **NAME:** `NYAYA_GATE_CANDIDATE_v1` (NOT verify-claim-semantic until promoted)
- **INPUT:** claim + peer-claims
- **OUTPUT:** pramāṇa + hetvābhāsa failures + falsifier status + can_update_posterior
- **AUTHORITY:** deterministic
- **GOLD:** **NONE — the critical gap.** Need positive/negative/borderline fixtures per fallacy.
- **BASELINE:** regex · LLM · hybrid (when benchmarked)
- **METRIC:** false-positive fallacy rate · detects each defect · no confusion of absence-of-evidence with asiddha
- **FAILURE MODE:** deterministic ≠ correct; hallucinates defects; false asiddha
- **ADOPTION GATE:** hand-adjudicated gold per fallacy → run blind → measure → only then `verify-claim-semantic`
- **STATUS:** `CANDIDATE` — deterministic is not enough; needs gold examples

---

## The promotion rule

A component promotes from `EXPERIMENTAL_INFRASTRUCTURE` to a named capability (`VALIDATED_v1`) only when:
```
independent gold → blind prediction → metric → error analysis → human adjudication
```
all exist. "The tests pass," "the schema validates," "the output looks good," "the model said so,"
"the code is sophisticated" — **none** of these promote it.

---

## The next 4 checkpoints (brutally concrete)

- **CP0 — benchmark genuinely real:** 50 retrieval + 30 evidence + 10 structure + 30 fidelity fixtures,
  all real-ID, review-status, provenance, no-leakage.
- **CP1 — philological floor:** source coverage proven; Vidyut characterized; independent parser sample;
  specialist review.
- **CP4 — argument extraction:** extractor evaluated blind against 10 gold; proposition F1, grounding
  precision, relation F1, abstention; simple baseline.
- **CP6 — semantic verification:** adversarial benchmark (negation/scope/attribution/counterevidence/
  fallacies/boundary); Nyāya gate vs regex vs LLM vs hybrid.

---

## The permanent checkpoint test

> **Show me the independent evidence that this component performs the semantic function named in its API.**

If the answer is "tests pass / schema validates / looks good / model said so / code is sophisticated" →
it stays experimental.
If the answer is "here is the frozen gold, here was the prediction made blind, here is the metric, here
are the failures, here is the human adjudication" → it is no longer theatre. It is research.
