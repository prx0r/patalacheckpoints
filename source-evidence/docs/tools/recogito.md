# Recogito Text Annotator — the native Workbench/Review annotation UI

**What Pāṭala borrows:** a small BSD-licensed JS annotation library with React support — text ranges, selection
events, user attribution, create/update/delete callbacks, annotation styling, and a model close to **W3C Web
Annotation**. This is the primitive for the Scholar Workbench annotation UX (highlight → challenge/propose/flag/
attach evidence/review translation) without building text-selection anchoring ourselves.

**License:** BSD.

## API / usage
- `npm` package `@recogito/text-annotator` (or the legacy `@recogito/annotorious`). Initialize on an element,
  listen to selection events, and map the resulting annotation (with Web-Annotation-style selectors) to a Pāṭala
  `ReviewProposal`.
- `annotation.body → Pāṭala ReviewProposal` (validate identity/resolution before promoting to `ReviewEvent`).

## Etiquette
Local JS library — no rate limit. Etiquette = annotations are proposals; never auto-promote to canonical
ReviewEvents.

## How Pāṭala consumes it
```
scholar highlights a sentence → [Challenge claim][Propose reading][Flag scope][Attach evidence][Review translation]
   → ReviewProposal → Pāṭala ReviewEvent
```
Distinction from INCEpTION: **INCEpTION = controlled gold/adjudication lab; Recogito = the native Pāṭala Workbench
annotation UI.**

**Priority: Workbench/Review surface (after the gold machinery).**
