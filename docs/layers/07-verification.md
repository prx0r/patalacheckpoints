# LAYER 07 — VERIFICATION PLANE

*Part of the `NAVIGATION.md` layer map (the master tree / spine). External methods test Pāṭala; they never define Pāṭala truth.*

## 1. What it is
The two-plane architecture: a PRODUCTION COMPILER + a VERIFICATION PLANE that tests every object from
OUTSIDE the graph. External ML methods are the judge, never the truth-definer.

## 2. Purpose
Make every claim falsifiable. Separate deterministic contract checks, cheap semantic witnesses, and
expensive LLM critics so that only genuine borderline cases escalate. Emit certificates for
engineering-validated state.

## 3. External tools used
**Inspect AI** (INTEGRATED — the benchmark runtime) · RefChecker/FActScore (atomic claim decomposition) ·
AlignScore (cheap entailment) · conformal prediction (calibrated abstention) · metamorphic testing
(mutation) · StructEval (methodology). See `external-tools.md`.

## 4. Data
- `source-evidence/evals/` — the benchmark plane (Inspect tasks, NAT tests, golds).
- `source-evidence/evals/patala/tasks/` — TantraFact, ArgumentBench, TranslationBench,
  CorroborationBench, PāṭalaQA.
- Golds: `data/evaluation/recovery-gold-v1.json`, MANUSCRIPT-RESOLUTION-GOLD, etc.

## 5. Processes
```
claim → deterministic checks → AlignScore/NLI cheap verifier
  → obvious PASS/FAIL → record
  → borderline → LLM critic
  → critic uncertain → OPEN / human
```
Core equation: `License(O) = supported_upstream_atomic_claims / substantive_atomic_claims` — shared by
L2/C1/Essay/Education-License.

## 6. Implementations
- `source-evidence/evals/` — the Inspect benchmark plane.
- `source-evidence/evals/patala/tasks/entity_reconciliation.py` — the resolver (EXACT/PROBABLE/...).
- `source-evidence/evals/patala/tasks/atlas_qa_audit.py` — the authority-inflation audit.
- Tests: the 10 eval self-tests PASS.

## 7. Docs
- `docs/process/08-verification-plane.md` — the detailed layer guide.
- `docs/global/globalplan.md` — the benchmark family.
- `docs/global/peer-review-goat.md` — the adversarial-eval discipline.
- `docs/global/patala-peer-review.md` — the review architecture.
