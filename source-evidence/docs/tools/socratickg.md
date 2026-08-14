# SocraticKG — QA-mediated knowledge-graph construction

**What Pāṭala borrows:** document → self-contained QA → atomic facts → knowledge graph. The key finding:
the QA intermediate representation preserves document-level relationships that direct text-to-triple
extraction loses.

**License:** Apache-2.0. Repo: `LABA-SNU/SocraticKG`.

## How Pāṭala consumes it
**PLANNED.** Replace generic 5W1H with the **Pāṭala scholarly-interrogator** (see
`06-commentarial-graph.md`):
```text
What question is answered? What position is advanced? What primary passage is interpreted?
What does this reading depend on? What alternative is rejected? What evidence is given?
Who is being followed/corrected? Where is the author uncertain? What downstream proposition follows?
```

## Doctrine
QA is a structured intermediate representation, not the final object. Extraction → MACHINE_PROPOSED
until review.
