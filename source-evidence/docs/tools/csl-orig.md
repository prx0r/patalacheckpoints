# CSL-orig — the lexical evidence ecosystem (S-tier)

**What Pāṭala borrows:** canonical git-tracked source bodies for **45 dictionary collections** —
Monier-Williams (MW), PWG, PWK, Grassmann, Apte, etc. This is the raw material for a **lexical evidence
graph**: a term's sense across multiple dictionaries + corpus occurrences.

**License:** varies (mostly public domain). Repo: `sanskrit-lexicon/csl-orig`.

## What it enables
```
TERM: śakti

MW          ...
PWG         ...
PWK         ...
AP90        ...
GRA         ...

Tantric corpus occurrences:
IPVV        ...
Tantrāloka  ...
MVT         ...

semantic trajectory:
Vedic → grammatical → philosophical → Śaiva technical sense
```

## How Pāṭala consumes it
**PLANNED.** Ingest as a lexical evidence layer → LexicalSense candidates. Dictionary definitions stay
**external evidence**; Pāṭala's contextual Sanskrit sense objects remain ours.

## Doctrine
A dictionary entry is evidence for a sense candidate, never the canonical sense. Combine multiple
dictionaries + corpus occurrences for the semantic trajectory.
