# DEVPATH 6 — G4: Human authority path + first UI

**Status: ✅ CLOSED (2026-08-13)**
**Commit:** ReviewBundle materializer (pipeline/review_bundle.py)

---

## Objective

Make the human-authority path real on one actual object: machine generation → machine evaluation →
scholar review → correction → downstream consequence, every transition a first-class object. Once
this works, Proof-of-Scholarship stops being a strategy document and becomes a system property.
Product = **PĀṬALA Review v0**.

## The three constitutional rules (from `endgamebuild/SPEC-G3-HUMAN-AUTHORITY-PATH.md`)

- **R1** — machine output may establish generation/evidence authority, but cannot establish human
  review/adjudication authority. Only an H witness raises the review axis.
- **R2** — a `ReviewEvent` must NEVER directly change its target. Correction chain:
  `ReviewEvent → ReviewProposal → Adjudication/accepted editor action → new exact object version
  (supersedes) → dependency invalidation / ImpactReport`. Preserves disagreement.
- **R3** — authority is a VECTOR; `epistemic_ceiling` is DERIVED
  (`derive(authority vector, dependency ceilings)`). Never let both be independently writable.

## The four human objects (already spec'd / built in source-evidence/schema/contracts_human_authority.py)

- `ReviewEvent` (scoped judgment; ACCEPT · ACCEPT_WITH_QUALIFICATION · DISPUTE · PROPOSE_ALTERNATIVE ·
  ABSTAIN · OUT_OF_SCOPE)
- `ReviewProposal` (proposed successor)
- `Adjudication` (formal resolution, records unresolved dissent)
- `PromotionEvent` (mechanical transition NOT_REVIEWED → INDEPENDENT_REVIEWED → ADJUDICATED)

## The first scholar-facing object: `ReviewBundle` (v1)

Materialized read-only view over one exact object — `bundle_id`, `target {ref, version, hash}`,
source/t1/l0/l2/l200, proof, scholarship, alternatives, dependency_impact, review_actions.

## First UI = one screen (TD-81)

Sanskrit · current reading · T1/L0 · why-this-reading · other readings · machine proof ·
WHAT DEPENDS ON THIS · YOUR JUDGMENT. Signature interaction: "show me exactly what my objection
changes" (dependency impact), not "leave a comment".

## Agent split

- **Agent 1** → ReviewEvent schema/review validity/machine pre-review/failure taxonomy/adjudication
  semantics/authority-promotion contracts.
- **Agent 2** → ReviewBundle materialization/exact versions/dependencies/ImpactReport/fork/regeneration.
- **Human scholar** → ReviewEvent + Adjudication (human-only authority boundary).

## Agent 1 directive queue (9 steps)

close G2 → harden `DerivedScholarlyObject<T>` → make authority canonical + ceiling derived → formalize
the 4 human objects → specify ReviewBundle-v1 → build one machine-generated ReviewBundle from an actual
IPVV disputed decision → run one human-review simulation → verify supersession/ImpactReport/proof
refresh → then start the Translation Audit UI.

## References

- `endgamebuild/SPEC-G3-HUMAN-AUTHORITY-PATH.md` (a1b) · `source-evidence/schema/contracts_human_authority.py`
  · `source-evidence/schema/derived_scholarly_object.py` · `docs/vision/vision-06-adversarial-review.md`
  · `vision-07-new-scholar.md` · `vision-12-multi-surface-platform.md`.

## Work completed

`pipeline/review_bundle.py`:
- `materialize_bundle(target, ...)` — the read-only `ReviewBundle-v1` for one exact object (target
  ref/version/hash + source/t1/l0/l2/l200 + proof + evidence + scholarship + dependency_impact +
  review_actions).
- `build_review_event()` — one scholar's scoped judgment on the exact target (R2: evidence, not
  mutation).
- `simulate_correction()` — zero-write impact for "show me exactly what my objection changes".
- `promotion_event()` — the mechanical authority transition, explicitly justified.
- `run_human_authority_path()` — the full loop (ReviewEvent → simulated ImpactReport → status) with
  R1/R2/R3 enforced: machine can never promote; a review never mutates its target; authority is a
  vector, ceiling derived.

`pipeline/test_review_bundle.py` — 18 checks (bundle materialization, R1/R2/R3, zero-write
simulation, DISPUTE flips dependency impact → downstream NEED_REVIEW). All pass.

## Acceptance / verification

| Check | Result |
|---|---|
| `test_review_bundle.py` | 18/18 PASS |
| review engine regression | 23/23 PASS |

## Honest boundary

- This is the Agent-1 review-validity/authority side of G4. Agent 2 supplies exact versions +
  ImpactReport + regeneration. The materializer is deterministic + read-only (never mutates the
  object). The first UI (one screen, TD-81) is built over this bundle — the materializer is the
  API contract that UI consumes.

## Files

- `pipeline/review_bundle.py` (new)
- `pipeline/test_review_bundle.py` (new)
