# DEVPATH 4 — G3B: Proposition core

**Status: ⏳ READY (unblocked; do after devpath3 if ARGMAP is evaluated)**

---

## Objective

Populate the epistemic core with derivational `Proposition` objects from verified ARGMAP/C1. The
core is currently thin (ARGMAP=1, proposition=5, argument=0, crux=3). Workbench, Pāṭala Review, and
education all need propositions/arguments/cruxes from real passages.

## The route (per `endgamebuild/SPEC-EPISTEMIC-CORE.md`)

1. **Derivational Proposition layer** — emit `Proposition` objects from verified ARGMAP/C1, each a
   `DerivedScholarlyObject(layer=PROPOSITION)` with:
   - `derived_from` (Sanskrit / L2 / C1 / implicit)
   - `explicitness` (explicit vs implicit/derived)
   - honest `epistemic_ceiling` (MACHINE_PROPOSED → ENGINEERING_VALIDATED)
2. **Objects to model** (the 12-IR / argument-IR core): `Proposition`, `Commitment`,
   `GroundingLink`, `InferenceApplication`.
3. **Discipline:** propositions start only from **evaluated** ARGMAP; a load-bearing ARGMAP failure →
   the proposition is `NOT_ELIGIBLE`.

## Acceptance

- A passage's ARGMAP → propositions chain exists as `DerivedScholarlyObject`s.
- Each proposition carries honest `epistemic_ceiling` (MACHINE_PROPOSED → ENGINEERING_VALIDATED).
- The proposition layer is reachable by the ARGMAP NAT harness's downstream consumers.

## References

- `endgamebuild/SPEC-EPISTEMIC-CORE.md` (A3/G3B) · `machinelearning/_ACTIVE/ARGUMENT-IR-VISION.md`
  (the 12 IR objects) · `source-evidence/schema/derived_scholarly_object.py`.
