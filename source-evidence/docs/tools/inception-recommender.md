# INCEpTION recommender — AI → scholar → gold annotation loop

**What Pāṭala borrows:** INCEpTION's external recommender API — AI suggests annotations to humans who
accept/modify/reject, which becomes gold. Maps directly onto Pāṭala's `AI candidate → scholar interface
→ review event → gold` loop.

**License:** Apache-2.0. Repos: `inception-project/inception`, `inception-project/inception-external-recommender`.

## The loop
```
IPVV sentence
  ↓
AI highlights: [claim] [premise] [opponent] [technical term] [quotation] [textual reference]
  ↓
Scholar corrects
  ↓
Pāṭala ingests adjudication → gold
```

## How Pāṭala consumes it
**PLANNED.** Internal gold construction (the gold lab), not the final consumer UX. Complement to
`inception.md` (the annotation workbench).

## Doctrine
Use for internal gold construction; Pāṭala's own review engine owns the adjudication semantics.
