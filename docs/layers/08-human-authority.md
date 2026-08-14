# LAYER 08 — HUMAN AUTHORITY (review / adjudication)

> **STATUS: PARTIAL — ReviewEvent ledger + review_engine are REAL; the scholar workbench UI is pending** (derived live state — see `docs_state.py`)


*Part of the `globalglobal.md` spine. The human layer — review, adjudication, supersession.*

## 1. What it is
The human-authority layer: scholars review, adjudicate, and promote objects. The four human objects
(ReviewEvent, ReviewProposal, Adjudication, PromotionEvent) with immutable, exact-version semantics.

## 2. Purpose
Make "reviewed" mean something. A review is evidence attached to an EXACT version — never a mutation.
Unresolved disagreement is preserved. Promotion is a mechanical transition with justification.

## 3. External tools used
Pāṭala-native. (Future: INCEpTION for the annotation/gold lab — see `external-tools.md`.)

## 4. Data
- `ReviewEvent` — one scholar's scoped judgment on an exact version (EVIDENCE, never mutation).
- `ReviewProposal` → `Adjudication` → supersession (P:v1 → P:v2).
- `PromotionEvent` — the review_status transition.
- `ReviewBundle` — the compiled review context (downstream: essays, lessons, videos).

## 5. Processes
```
review attached to EXACT version → proposal → adjudication → new version (supersedes) →
downstream staleness via object_dependency → ImpactReport
```
A source change fires a hook → Pāṭala's dependency engine calculates what's stale/affected — the
dependency logic lives in Pāṭala, not Hermes.

## 6. Implementations
- `source-evidence/schema/contracts_human_authority.py` — the 4 human objects.
- `pipeline/review_engine.py` — the review engine (23/23 tests).
- `pipeline/review_bundle.py` — the ReviewBundle compiler.
- `pipeline/scholarly_oracle.py` — source-assertion/corroboration (13 tests).
- Tests: `test_review_engine`, `test_review_bundle`, `test_scholarly_oracle`.

## 7. Docs
- `docs/process/README.md` (Layer 8 section) + `globalglobal.md`.
- `docs/global/globalgoal.md` + `agent1atlas.md` — the human-authority layer (E).
- `docs/vision/vision-06-adversarial-review.md` — Pāṭala Review.
- `docs/vision/vision-07-new-scholar.md` — the scholar workbench.
- `docs/global/patala-peer-review.md` — the review architecture.
