# Hypothesis — inline public scholarly annotation (pilot)

**What Pāṭala borrows:** an open-source browser annotation system — the `h` server (annotation API) + a BSD
browser client embeddable in webpages. For the Scholar Hub: scholars highlight a passage directly and attach a
comment (e.g. "this citation doesn't support this claim") without Pāṭala building a text-selection/commenting UI.

**License:** `h` API server AGPL (self-host); browser client BSD. Public service at hypothesis.is.

## API / usage
- `GET /api/search?uri=...`, `POST /api/annotations` (auth: Hypothesis account / developer token), `GET /api/`.
- Embed the client in a page; users create `Annotation { uri, target[{selector}], text, ... }`.
- Web Annotation selectors on `target` — compatible with Pāṭala `SourceSpan`.

## Rate limiting / etiquette
Public Hypothesis service has rate limits; self-host `h` to avoid them. Etiquette: treat annotations as
**proposals**, never auto-promote to canonical ReviewEvents.

## How Pāṭala consumes it
```
Hypothesis Annotation → ReviewProposal → (validate identity/resolution) → Pāṭala ReviewEvent
```
Use for lightweight public scholarly annotation (commenting, flagging unsupported citations); INCEpTION stays the
controlled benchmark/adjudication environment.

**Priority: PILOT, not core yet.**
