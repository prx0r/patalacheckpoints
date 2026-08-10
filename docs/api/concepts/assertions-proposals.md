# Concepts — Assertions and proposals

The moat. Pāṭala doesn't store important scholarly claims as naked fields; it stores them as **assertions** — structured, reviewable objects — and keeps **machine proposals** separate.

## Assertions

`GET /api/assertions` returns contested claims as first-class objects:

```json
{
  "subject": "pt:work:kubjikamata",
  "predicate": "belongs_to",
  "value": "Kubjikā",
  "status": "expert_reviewed",
  "certainty": "probable",
  "origin": "institution",
  "evidence": [...],
  "review_events": [...]
}
```

An assertion says: **subject → predicate → value**, plus *why* (evidence) and *who checked it* (review events). This is how disagreement is representable without corrupting the graph — you can hold two dated assertions with different evidence, and the editorial state says which Pāṭala currently prefers.

**When something is an assertion:** if a scholar could legitimately say "I disagree" (a date, a tradition tag, a term sense, a manuscript identification, a parallel), model it as an assertion. Filenames, slugs and page numbers are not assertions.

## Proposals

`GET /api/term-proposals` is the proposal layer. A machine or a human proposes a term sense; it lives here **forever separated** from the accepted ledger. Promotion is strictly:

```
proposed → reviewed → accepted
```

A proposal can never auto-promote. This prevents the feedback loop where an LLM's guess becomes "established usage" by being retrieved as precedent.

## Review events

A review is an **event**, not a boolean:

```json
{
  "scope": "term_sense",
  "decision": "accept",
  "reviewer": { "kind": "scholar", "id": "person:x" },
  "reason": "...",
  "created_at": "..."
}
```

Scopes are specific (`work_identity`, `date`, `translation`, `term_sense`, `parallel`, `manuscript_identification`, `tradition_classification`) — never a vague "reviewed the record." Reviews are append-only and reversible.

## The crosswalk

`GET /api/crosswalks` maps our objects to external records (`same_as`, `witness_of`, `version_of`...) while preserving both identifiers — the federation layer. Resolve, don't duplicate.
