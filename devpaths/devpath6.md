# DEVPATH 6 — G4: Human authority path + first UI

**Status: ⏳ READY (after devpath5)**

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
