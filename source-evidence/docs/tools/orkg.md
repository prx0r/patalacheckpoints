# ORKG — structured-research-KG patterns (borrow, NOT backend)

**What Pāṭala borrows:** the *pattern* of converting scholarly literature into structured research knowledge —
papers/contributions/comparisons/research-problems/structured-claims + its data model + UI patterns. **Precedent
and an interoperability opportunity, NOT the backend** (Pāṭala's graph is more fine-grained and philosophical:
exact primary span → translation decision → interpretive assertion → proposition → argument → crux → review).

**License:** code MIT.

## API
- Base URL `https://incubating.orkg.org` (and `https://orkg.org`).
- `GET /api/papers`, `/api/papers/<id>` — papers/contributions.
- `GET /api/resource/<id>`, `/api/statements` — the knowledge-graph statements (subject-predicate-object triples
  over contributions).
- `GET /api/comparisons`, `/api/research-problems`, `/api/templates` — the structured-claims model.
- `POST /api/papers` (with API key) — contribute structured papers.

## Rate limiting / etiquette
- Public read endpoints are free; be polite (a few req/sec), cache responses, and use the provided paging/filters
  rather than dumping whole endpoints. Writes need an account/API key and are rate-limited. This is a small
  non-profit service — be gentle.

## How Pāṭala consumes it
- **Study** its paper → contribution → statement model as a reference for how to represent structured claims.
- **Interoperability** (optional): expose Pāṭala SourceAssertions / propositions in an ORKG-compatible shape so
  structured claims could be contributed/exchanged. Do NOT build Pāṭala on ORKG.
