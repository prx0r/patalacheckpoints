# CLAIMS.md — Pāṭala's self-audit (the project auditable by its own philosophy)

*2026-08-12. The project's own claims ledger. Every significant capability claim has a STATUS, EVIDENCE,
CAVEAT, and what would promote it. This makes the project auditable using its own philosophy — no claim
is "real" because code exists; it's real only when independent gold + blind prediction + metric + human
adjudication show it.*

**The rule:** *Nothing is "real" because code exists. It becomes real only when an independently defined
task, human-grounded gold, and a reproducible evaluation show that it does what its name claims.*

---

## CLAIM P-001 — "Pāṭala has lossless source anchoring (L0)."
- **STATUS:** SUPPORTED (V2/V3 flagship corpus) / PARTIAL (full corpus incl. V1 legacy)
- **EVIDENCE:** `verify_l0.py` P0 harness — **V2/V3 (the flagship published IPVV corpus, 35 chunks):
  35/35 PASS** — 0 unknown chars, 0 bad spans, 0 overlaps, 0 duplicates, monotonic ordering, full
  classification (`classification_complete: true`), deterministic (identical proofs across runs).
  Independently re-verified on a random sample (slice-equality + monotonicity + no-overlap all pass).
  The 18 remaining irregular editorial/gloss regions are explicitly classified via
  `docs/l0_reviewed_exceptions.json` as `IGNORED_WITH_REASON:reviewed` (visible, not silently dropped).
  Reproduce: `python3 pipeline/verify_l0.py --t1 .../02_t1 --l0 .../l0 --level p0
  --exceptions docs/l0_reviewed_exceptions.json`.
- **CAVEAT:** This is the V2/V3 **supported published corpus** (CP1's "supported passages"). **V1 (28
  chunks) is a separate legacy prose format** — 0/28, `MIGRATION_PENDING`, not part of this milestone.
  P2 (Vidyut morphology) is characterized (55% supported) but not yet the P2 ensemble-validated proof.
- **REQUIRED to promote (full):** V1 gets its own importer + the same output contract (→ 63/63); P2
  ensemble validated against an independent witness (Heritage) over CONFLICT/UNANALYZED + a stratified
  control sample; specialist review of a sample.
- **STATUS THIS SESSION (2026-08-12):** V2/V3 P0 **FROZEN** as the first completed CP1 sub-capability.
  Next (per the cross-layer review): Heritage as an independent P2 witness over all Vidyut CONFLICT +
  UNANALYZED records + a stratified control sample (~500 CONFIRMED, ~500 AMBIGUOUS_SUPPORTED) → an
  ensemble disagreement report. ranker.py is NOT promoted to P3; it is first audited + given a small
  human-reviewed lexical-sense gold + evaluated against baselines before being a non-authoritative
  lexical witness.

## CLAIM P-002 — "Pāṭala's benchmark is a real evaluation substrate."
- **STATUS:** SUPPORTED (as infrastructure) / PARTIAL (as evidence)
- **EVIDENCE:** `benchmarks/v0/` frozen (MANIFEST/SCHEMA/SPLITS/METRICS); 1 retrieval fixture file,
  1 structure gold (ARG-GOLD-001).
- **CAVEAT:** EVIDENCE and FIDELITY families have **0 fixtures**. ARG-GOLD-001 is a SEED, not proof.
  Fixtures are CANDIDATE, not independently DOUBLE_REVIEWED.
- **REQUIRED to promote:** targets (50 retrieval / 30 evidence / 10 structure / 30 fidelity); every
  fixture real-ID + review-status + provenance + no-leakage.

## CLAIM P-003 — "Pāṭala can automatically reconstruct IPVV arguments."
- **STATUS:** NOT_ESTABLISHED
- **EVIDENCE:** none — no automatic extractor has been evaluated against hand-gold.
- **REQUIRED:** ARG-GOLD-001..010 hand-adjudicated; extractor evaluated blind; proposition F1,
  grounding precision, relation F1, abstention performance; simple baseline included.

## CLAIM P-004 — "The Nyāya gate validates claims."
- **STATUS:** CANDIDATE (NYAYA_GATE_CANDIDATE_v1)
- **EVIDENCE:** 680-LOC gate exists (deterministic); NO gold examples test it.
- **CAVEAT:** deterministic ≠ correct. No positive/negative/borderline fixtures exist for
  asiddha/viruddha/savyabhicara/satpratipaksa/badhita.
- **REQUIRED to promote to `verify-claim-semantic`:** hand-adjudicated gold for each fallacy; run blind;
  measure false-positive fallacy rate; compare vs regex + LLM + hybrid baselines.

## CLAIM P-005 — "The Bayesian primitive (strength.py) scores claim support."
- **STATUS:** UNVALIDATED_HEURISTIC (BayesianEvidencePrimitive)
- **EVIDENCE:** math correct (24 tests); weights HAND-CHOSEN, not calibrated.
- **CAVEAT:** no epistemic role until calibrated against adjudicated outcomes.
- **REQUIRED:** calibration on reviewed decisions; Brier/log-loss/calibration vs simpler baselines.

## CLAIM P-006 — "The gold-chain certificate audits cross-layer derivation."
- **STATUS:** INFRASTRUCTURE (renderer) — honest statuses now
- **EVIDENCE:** L0 layer REAL (source_integrity PROVED, morphology SUPPORTED, OPEN cruxes propagate).
  INTERPRETATION/INFERENCE/ESSAY_CLAIM = MACHINE_PROPOSED (fixed; no fabricated EDITOR_APPROVED).
- **CAVEAT:** the L0 floor is real; everything above is machine-proposed until reviewed.
- **REQUIRED to promote:** accepted themes/arguments with real review events enter the chain.

## CLAIM P-007 — "Vidyut improves L0 morphological validation."
- **STATUS:** NOT_RUN (Vidyut P2 not wired)
- **EVIDENCE:** none yet.
- **REQUIRED:** Vidyut over the 3,656 AMBIGUOUS + 2 FAILED records; measure how many ambiguities it
  constrains; characterize CONFIRMED/AMBIGUOUS_SUPPORTED/CONFLICT/UNANALYZED/TOOL_ERROR.

## CLAIM P-008 — "The C1 corpus is a genuine scholarly resource."
- **STATUS:** SUPPORTED (as content)
- **EVIDENCE:** 49 passages, 63 C1s, real content, resolvable.
- **CAVEAT:** C1 quality metrics are unvalidated heuristics (thresholds tuned, not benchmarked).

---

## The epistemic labels (the anti-conflation vocabulary)

| Label | Means | Not the same as |
|---|---|---|
| **BUILT** | code exists | TESTED |
| **TESTED** | software behavior tested | BENCHMARKED |
| **BENCHMARKED** | evaluated against independent fixtures | VALIDATED |
| **VALIDATED** | predefined threshold met | EDITOR_REVIEWED |
| **EDITOR_REVIEWED** | actual human review occurred | PRODUCTION |
| **PRODUCTION** | validated + monitored | — |

**The banned words (until independently justified):** PROVED · TRUTH · VERIFIED SEMANTICALLY · CORRECT ·
EDITOR APPROVED · BEST · WINS.
**The allowed words:** SUPPORTED BY · PASSED CHECK X · BENCHMARKED ON · MACHINE-PROPOSED · REVIEWED BY ·
NO CONFLICT DETECTED.

---

## The three kinds of validity (a permanent principle)

| Validity | Handled by |
|---|---|
| **SOFTWARE** — does the implementation behave per its spec? | tests |
| **EMPIRICAL** — does it perform on independent examples? | benchmarks |
| **SCHOLARLY** — are the examples and judgments intellectually defensible? | experts |

**Tests ≠ benchmarks ≠ expert review. Never report them as interchangeable.**

---

## The abstention principle (Pāṭala should know when NOT to assert)

- Precision over coverage for scholarship: **40% coverage / 98% grounded > 95% coverage / 75% grounded.**
- A good system must be able to abstain: "NO UNIQUE ARGUMENT RECOVERABLE" is a valid, valuable output.
- A model that confidently invents premises where none are recoverable = **severe failure**.
- Metrics include: precision at accepted claims · coverage · **abstention accuracy** · **false-assertion rate**.

---

## The anti-theatre protocol (the 9-field contract)

Every component must fill: **NAME · INPUT · OUTPUT · AUTHORITY · GOLD · BASELINE · METRIC · FAILURE MODE ·
ADOPTION GATE.** If any field is empty, the component is `EXPERIMENTAL_INFRASTRUCTURE`, not a scholarly
capability. See `AGENT1-HANDOVER.md` §4 + the component contracts below.
