# NAT corpora — Pāṭala evaluation

*2026-08-12. NAT = naturally occurring model outputs, independently adjudicated. The eval substrate is
mature (EVAL-CONTRACT + SYN benchmarks + NAT harnesses). The next problem is **corpus provenance and
lane-safe freezing**, not more Inspect engineering.*

## The key property (not "old")

The essential requirement is NOT that a sample is historically old. It is:

> the candidate was generated naturally, without knowledge of its eventual adjudication and without being
> constructed as a benchmark mutation.

So NAT samples may be collected **prospectively** too:

```text
normal production run
  → freeze output BEFORE adjudication
  → do not tune producer
  → independent adjudication
  → NAT corpus
```

Do NOT manufacture "historical" samples to hit a target number.

## Collection protocol (anti-theatre — do NOT violate)

1. **Freeze exact object + provenance.** Each sample = the frozen output + origin (path, SHA). Never edit
   a natural sample to "help" the test.
2. **Frozen authority snapshot (ARG-NAT).** Each sample must freeze the **authority context that existed
   when the output was produced** (`<id>.authority.json`). The solver uses that frozen snapshot — NEVER
   the current `synthesis_authority()` — so a future change in synthesis/dependencies cannot silently
   change the verdict on an unchanged historical object.
3. **Independent adjudication.** Gold is set by blind independent adjudication, never by the detector.
   Gold is *"this output is epistemically defective for reason X"*, not *"the detector ought to emit Y."*
4. **Sample across the distribution.** clean / known-problematic / borderline — do NOT cherry-pick only
   obvious failures.
5. **Record the adjudication object** with verdict, violation families (with ref + reason + expected
   detector rule), uncertainty, and both failure axes:
   - `first_unsupported_layer`: `SOURCE → SPAN → ATTRIBUTION → SCOPE → WARRANT → CONCLUSION → PROJECTION`
   - `derivation_stage` (translation tasks): `SOURCE → L0 → L1 → L2 → L200_MT → L200_IA → L200_OPEN →
     SOURCE_LAYER`
   Do NOT force an IA→MT classification error into `WARRANT`/`PROJECTION` to unify schemas.

## Corpus layout

| Corpus | Directory | Harness | Status |
|---|---|---|---|
| ARG-LAUNDRY-NAT | `nat/arg-laundry/` | `inspect_arglaundry_nat.py` | **empty** — needs `<id>.audit.json` + `<id>.authority.json` + `<id>.adjudication.json` |
| L200-CHECKER-NAT | `nat/l200/` | `inspect_l200_nat.py` | **empty** — needs `<id>.candidate.json` (Agent 2 bundle, read-only) + `<id>.adjudication.json` |
| L200-DETECTOR-NAT | `nat/l200-detector/` | `inspect_l200_detector_nat.py` | harness only — no semantic detector SUT exists yet |

## L200 lane boundary

Agent 2 writes the frozen candidate bundle **once** per `EVAL-CONTRACT-L200-EXPORT.md`. Agent 1 consumes it
**read-only** and separately creates `adjudication.json`. No Agent 1 modification to the proposer or the
candidate.

## Target

Let the NAT corpus **emerge from production**, not production from the benchmark. Do NOT manufacture a fixed
quota of samples: collect genuine natural/prospective outputs as they occur (Agent 2's normal L200 dev stream
exported automatically; Agent 1's normal argument/review work). Until the corpus is meaningful, NAT metrics
are NaN/NA — do not report an empty NAT run as a result.

Every `adjudication.json` must carry **adjudicator provenance** (who/what produced the gold + review status);
Agent 1 machine-assigned gold is NOT expert gold (see `EVAL-CONTRACT.md`).
