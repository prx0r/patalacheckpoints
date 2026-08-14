# RARR — retrieve → assess → revise unsupported output

**What Pāṭala borrows:** the research/agreement/revision loop: generated claim → formulate question →
retrieve evidence → assess agreement → revise.

**License:** Apache-2.0. Repo: `anthonywchen/RARR`.

## How Pāṭala consumes it
**PLANNED.** For every generated sentence:
```text
generated sentence → claim atomization → Pāṭala graph query → source/scholar evidence → agreement check → rewrite if unsupported
```
Key modification: the trusted evidence universe is Pāṭala's own corpus, NOT unrestricted web retrieval
(`08-verification-plane.md`).

## Doctrine
Rewrite unsupported output against the trusted graph; never let generation outrun the evidence.
