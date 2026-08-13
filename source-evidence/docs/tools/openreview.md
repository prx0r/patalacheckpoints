# OpenReview — peer-review submission/review workflow (integrate, don't build)

**What Pāṭala borrows:** the *workflow* layer for peer review — submission, review assignment, reviewer
UI/workflow, notifications, publication lifecycle. Pāṭala does NOT build reviewer-management software; it
contributes the **epistemic content**: claim decomposition, source verification, argument reconstruction,
scope/attribution attacks, counterevidence, minimal cruxes, exported as structured ReviewEvents.

**License:** code MIT. Alternatives to evaluate alongside: **Kotahi**, **Janeway** (similar workflow platforms).

## API
- Base URL `https://api2.openreview.net`.
- Auth: API key or bearer token (`Authorization: Bearer <token>`).
- `GET /notes/search`, `GET /notes` — notes (submissions/reviews/comments).
- `GET /notes?id=<id>`, `GET /groups`, `GET /edges`, `GET /invitations` — the object model
  (notes, groups/profiles, edges/scores, invitations).
- `POST /notes` (write), `POST /notes/edit`, `POST /invitations` — submission/review lifecycle (needs auth + venue
  invitation).
- Use `content` fields for structured review fields (e.g. claim refs, verdict, evidence).
- `GET /invitations/<id>` — the review form/schema a venue requires.

## Rate limiting / etiquette
- OpenReview enforces rate limits per API key; respect `429` and `Retry-After`, batch writes, and use paging
  (`offset`/`limit`, `sort`) on reads. Public reads of a venue's notes are fine but cache them. Be polite — it's
  shared community infrastructure.

## How Pāṭala consumes it
```
Pāṭala ReviewEvent (claim refs, source verification, argument attacks, cruxes)
   → export to OpenReview note content → the venue's review workflow
   ← import OpenReview review notes → structured ReviewEvents into Pāṭala's review graph
```
This is the *peer-review adversary* product surface, built on OpenReview's workflow + Pāṭala's epistemic layer.
