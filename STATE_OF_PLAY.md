# Pāṭala — State of Play (2026-08-10, honest)

*The strategic reset. We spent too long on model-interface / translation-generation
optimization. The translation files are NOT the valuable artifact — you can produce
translations fine with your main model + anchored context. The valuable artifact is
the STRUCTURE: identity, evidence, review, provenance, the reusable scholarly graph.*

---

## Where we actually are

### Proven (keep)
- **Milestone A1 — the complete machine adjudication loop works.** Kramasadbhāva 1.8
  ran source → T1 → R1 (real cruxes) → T2 (rival) → R2 (decision taxonomy) → T3
  (resolved) via the real Hermes path. Real interpretive disagreement was found,
  adjudicated, and resolved (devadeveśi = "mistress of the god of gods"; nirānande crux
  surfaced). **This is the threshold that matters — not the English output.**
- **The durable state machine** (load/transition/run/audit/persist/reload), the
  **stage-contract layer** (empty strict output is INVALID), the **six primitives**
  (Identity/Assertion/Evidence/Provenance/Review/Rights), the API/MCP, the term
  trajectories, the derived readiness gate.

### De-emphasized (stop chasing)
- **Translation generation via Hermes.** The C1 generation run was slow (backend
  latency) and it's not where value lives. You can produce better translations with
  your main model + anchored context. **Do not optimize this further.**
- The model-interface rabbit hole (JSON mode, response_format, retries, repair). Closed.

---

## The real strategic direction (reaffirmed)

Pāṭala is **provenance + adjudication infrastructure**, not a translation factory.

The pipeline is a boring Hermes job that runs, retries, records failures, moves on.
Hermes owns the plumbing. We own the scholarly model.

What we should focus on (the six primitives + their objects):
```
Work · Witness · Edition/DigitalRepresentation · CanonicalPassage · SourceSpan ·
Person · Term · Sense · Resource
```
plus annotations/assertions over them, with evidence + review.

---

## The nirānanda lesson (the project in miniature)

The first real run exposed exactly why C1/evidence matters:
- R2 classified nirānande as CONSTRAINED = "O bliss-less one" (literal privative).
- External evidence (Mahānaya renders "the Bliss of Stillness"; nirācārānanda in
  Kubjikā material) suggests it may be a **technical** Krama/Kubjikā term → PREFERRED
  or OPEN, not CONSTRAINED.

The system caught the crux and carried it — but the adjudicator was overconfident
because it lacked the *historical lexical evidence*. That gap is Pāṭala's whole reason
to exist. The moat is not "our AI translates better"; it is:

> What does nirānanda mean HERE, with what evidence, reviewed by whom, and how has
> that judgment changed?

---

## The immediate roadmap (collapsed)

1. **Stop** C1-generation via Hermes. You produce the C1/commentary with your main
   model + anchored context, as a structured object (see the C1 schema).
2. **Write the scholarly-graph schema** — the canonical object/assertion model that
   must survive years. This is the highest-leverage next artifact.
3. **Milestone B** — a contiguous 25-verse *research unit* (passages + a section-level
   lexical network + cross-passage parallels), not 25 isolated translations.
4. **Milestone C** — one real scholar conversation on the strongest passages.

---

## Files

- Pipeline: `pipeline/` (state_machine, schema, contracts, audit, evidence, validate)
- Skills: `skills/` (translate-work, write-commentary, etc.)
- The 1.8 run result: `experiments/milestone-a-kramasadbhava-1.8.md`
- Strategy: `PROCESS_NOTES.md`, `HANDOVER.md`, `docs/`
- Corpus strategy: `sanskritree/corpus/targets/` (reference map, markguidance, leapfrog)

## Repo
**https://github.com/prx0r/patala** (branch `main`).
