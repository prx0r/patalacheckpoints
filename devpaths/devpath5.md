# DEVPATH 5 — G3C: Crux + arguments + Nyāya-profile wired

**Status: ✅ CLOSED (2026-08-13)**
**Commit:** perturbation-based crux engine (machinelearning/research/patala_ml/crux_engine.py)

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

## Work completed

`machinelearning/research/patala_ml/crux_engine.py`:
- `compute_cruxes(arguments, propositions)` — finds the **minimal decisive premise-sets** whose
  removal flips each inference's conclusion (perturbation / outcome-sensitivity), packaged as cruxes
  with an adjudication question + `review_status=NOT_HUMAN_REVIEWED`.
- `wire_nyaya_profile(argument, gold_propositions)` — runs the bounded gate
  (`verify_claim_semantic`, devpath1) over each argument's conclusion + premises, attaching a
  bounded structural audit (outcome PASS/PASS_WITH_OPEN/FAIL; never `argument_valid=true`).
- `build_crux_layer(...)` — assembles cruxes + profiles; `build_arguments_from_gold(gold)` wraps
  gold objects into argument graphs.

`machinelearning/research/tests/test_crux_engine.py` — acceptance (all pass).

## Acceptance / verification

| Check | Result |
|---|---|
| `test_crux_engine.py` | PASS |
| cruxes | 15 perturbation cruxes over the 4 gold arguments |
| Nyāya-profiles | 4 arguments profiled (bounded, deterministic) |

## Honest boundary

- Cruxes are computed by **perturbation** (outcome-sensitivity), NOT importance/centrality.
- The Nyāya-profile is a bounded structural audit, NOT a truth oracle.
- Cruxes are NOT_HUMAN_REVIEWED — the adjudication question is for a scholar/H witness.

## Exit → next

**devpath6 (G4)**: human authority path (Review→Adjudication→new version→Impact) + first UI.

## Files

- `machinelearning/research/patala_ml/crux_engine.py` (new)
- `machinelearning/research/tests/test_crux_engine.py` (new)
