# ARG-NAT seed — naturally occurring evidence objects (Phase 7 byproduct)

*2026-08-12. Per the EVAL-CONTRACT, NAT candidates are frozen naturally-occurring outputs, then
independently adjudicated — NEVER constructed for the benchmark.*

## What this mission produced that is NAT-relevant

During normal scholarly-evidence production, Agent 1 produced **natural scholarly-evidence objects**: 13
`SourceAssertion`s (curated from actual source text, SPAN_VERIFIED), spanning **4 attributed authors**
(Isabelle Ratié, Alexis Sanderson, Goodall et al., Śivānanda) and **10 canonical propositions**. These are
natural evidence objects, not benchmark mutations.

These are recorded in `source-evidence/production/store/corpus.json` with adjudicator provenance:

```json
{
  "provenance": {
    "extraction_origin": "CURATED_HUMAN_READ",
    "adjudicator": {"type": "MACHINE", "agent": "agent1", "model": null, "prompt_hash": null},
    "review_status": "NOT_HUMAN_REVIEWED"
  }
}
```

**Machine-adjudicated, review_status = NOT_HUMAN_REVIEWED.** This is NOT expert gold.

## Honest status

The EVAL-CONTRACT NAT harnesses (`inspect_arglaundry_nat.py`, `inspect_l200_nat.py`) remain **empty** — they
are waiting for genuinely natural **argument/audit** outputs (the ARG-NAT SUT is the essay-audit detector, which
operates on prose/audit objects, not SourceAssertions). This mission produced *evidence* objects, not *audit*
objects, so it did not manufacture argument-level NAT samples (correctly — the review forbids constructing
outputs for the benchmark).

## What will seed ARG-NAT properly

- Genuine future Agent 1 essay/audit outputs (natural, frozen before adjudication).
- L200-CHECKER-NAT: Agent 2's frozen live L200 candidates via the export contract (read-only).
- Each frozen, then independently adjudicated (machine → human → expert upgrade separately).

Until those exist, NAT metrics are NaN/NA. No quota is manufactured.
