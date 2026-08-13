# INCEpTION — the annotation / gold / adjudication workbench

**What Pāṭala borrows:** a multi-user semantic annotation platform — configurable text annotations, intelligent
annotation recommendations, corpus management, knowledge bases/entity linking, programmatic workflows. **Do not
build the gold/adjudication UI.** This removes a whole engineering category.

**License:** Apache-2.0 (actively maintained).

## API / usage
- Web application (Java/Spring) — deploy locally; REST/API + UI for projects, documents, annotation layers,
  users, workflows.
- Configure **annotation layers** per project (speaker, commitment, proposition, premise/conclusion, inference,
  scope, uncertainty, source attribution).
- **Machine pre-annotation → INCEpTION review → export → Pāṭala reference object** is the intended workflow
  (export the annotation as canonical gold JSON).

## Rate limiting / etiquette
Self-hosted — no third-party rate limit. Etiquette = keep gold projects versioned/exportable; never lose the
machine-proposal origin in the exported gold (adjudication provenance).

## How Pāṭala consumes it
```
Argument Gold project:   layers = speaker/commitment/proposition/premise/conclusion/inference/scope/uncertainty
Corroboration project:   Pāṭala proposition + Ratié paragraph → annotator picks DIRECT_SUPPORT / PARTIAL_SUPPORT /
                         CONTRADICTION / BACKGROUND / NON_EQUIVALENT
   → export canonical gold JSON → Inspect benchmark
```
This is gold **creation**, not the final Scholar Hub UX (which can be prettier later).

**Priority: VERY HIGH for benchmark/gold authoring.**
