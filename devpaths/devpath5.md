# DEVPATH 5 — G3C: Crux + arguments + Nyāya-profile wired

**Status: ⏳ READY (after devpath4)**

---

## Objective

Compute cruxes and assemble full arguments over the proposition core, with the Nyāya-profile wired in.

## The route (per `endgamebuild/SPEC-EPISTEMIC-CORE.md` + `ARGUMENT-IR-VISION`)

1. **Crux computation** — the minimal hitting set of decisive premises (outcome-sensitivity), per
   ARGUMENT-IR-VISION. **Cruxes come from perturbation, not importance/centrality** (the handover's
   discipline).
2. **Arguments** — assemble `Argument` objects from the propositions (a `DerivedScholarlyObject`
   `layer=ARGUMENT`).
3. **Nyāya-profile** — run the bounded gate (`verify_claim_semantic`, devpath1) over the assembled
   arguments so each carries an honest structural audit.
4. **Crux evaluation contract** — extend the metamorphic suite to proposition/crux reconstruction.

## Discipline

- Cruxes are a **perturbation** result (remove premise → does the conclusion flip?), never a
  centrality/importance heuristic.
- The Nyāya gate stays a **bounded evaluator** — it never asserts `argument_valid=true`.

## Acceptance

- ARGMAP → propositions → arguments → cruxes chain exists as `DerivedScholarlyObject`s.
- Crux candidates are computed by perturbation and carry their outcome-sensitivity evidence.
- Education skills (SPEAKER_ATTRIBUTION, WARRANT_RECONSTRUCTION, CRUX_IDENTIFICATION) are exercisable.

## References

- `endgamebuild/SPEC-EPISTEMIC-CORE.md` · `machinelearning/_ACTIVE/ARGUMENT-IR-VISION.md` ·
  `machinelearning/research/patala_ml/{argument,nyayagate}.py` (devpath1).
