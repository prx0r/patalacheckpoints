# DEVPATH 4 — G3B: Proposition core

**Status: ✅ CLOSED (2026-08-13)**
**Commit:** derivational Proposition layer (machinelearning/research/patala_ml/proposition_layer.py)

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

## Work completed

`machinelearning/research/patala_ml/proposition_layer.py`:
- `Proposition` — commitment (ASSERTS/DENIES/PRESUPPOSES/ASSUMES_FOR_ARGUMENT/ATTRIBUTES_TO_OPPONENT/
  QUOTES/RECONSTRUCTED/EDITORIAL_RATIONAL_RECONSTRUCTION) + explicitness (EXPLICIT/RECONSTRUCTED/
  IMPLICIT) + derived_from (SANSKRIT_EXPLICIT/SANSKRIT_SUPPORTED/INTERPRETIVE_RECONSTRUCTION/
  C1_INTERPRETIVE/IMPLICIT/EDITOR/L2/C1) + grounding + scholarly_corroboration.
- `Proposition.to_dso()` — projects as `DerivedScholarlyObject(layer=PROPOSITION)` with the authority
  envelope; ceiling is DERIVED (R3); review axis NOT_REVIEWED (only an H witness raises it).
- Lifters from real committed sources: gold argument nodes (ARG-002/003/004/005), ARGMAP
  `argument_map` (Agent 2's committed map), SourceAssertions (assertion-registry).
- `build_proposition_layer()` — assembles the corpus as DSO emissions.

`machinelearning/research/tests/test_proposition_layer.py` — acceptance (all pass).

## Acceptance / verification

| Check | Result |
|---|---|
| `test_proposition_layer.py` | PASS |
| layer counts | 34 propositions (24 gold + 5 argmap + 5 assertions) |
| honest ceiling | every proposition MACHINE_PROPOSED/ENGINEERING_VALIDATED, review NOT_REVIEWED |

## Honest boundary

- The propositions are MACHINE_PROPOSED/ENGINEERING_VALIDATED — NOT independently reviewed.
- Per the handover discipline: propositions start only from evaluated ARGMAP; a load-bearing ARGMAP
  failure → NOT_ELIGIBLE. The ARGMAP NAT (devpath1/3) is the gate for real-map propositions.

## Exit → next

**devpath5 (G3C)**: crux (perturbation) + arguments + Nyāya-profile wired. See `devpaths/devpath5.md`.

## Files

- `machinelearning/research/patala_ml/proposition_layer.py` (new)
- `machinelearning/research/tests/test_proposition_layer.py` (new)
