# Argdown — human-readable argument notation

**What Pāṭala borrows:** a mature human-readable syntax for arguments that parses into visual argument
maps — premise-conclusion structures and relations between arguments.

**License:** MIT. Repo: `christianvoigt/argdown`. Also `debatelab/argdown-cotgen` (synthetic reasoning
traces for education — never epistemic truth).

## How Pāṭala consumes it
**PLANNED.** Argument import/export adapter:
```
Pāṭala Argument JSON
   → Argdown adapter
   → editable scholar notation
   → SVG / interactive argument map
```
`argdown-cotgen` → education: generate reconstruction steps a student must complete.

## Doctrine
Argdown is a notation/adapter, NOT Pāṭala's argument engine. Synthetic CoT traces are education
exercises, never epistemic truth.
