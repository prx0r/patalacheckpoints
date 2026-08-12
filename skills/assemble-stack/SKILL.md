---
name: assemble-stack
description: "Assemble and inspect the per-work stacked artifact: the translations/_stack/{work} directory with its 00_source→07_c1 floors and AUDIT.md. Use when asked to see a work's pipeline state, add a work to the stack, or check which floors are done."
version: 1.0.0
author: Pāṭala
metadata:
  hermes:
    tags: [stack, pipeline, patala, translation, artifact]
    related_skills: [translate-passage, validate-passage]
    checkpoint: CP1 (assembles the per-work provenance stack the L0 floor certifies)
---

# Assemble the Per-Work Stack

## When to use
- Asked "what's the state of work X?" or "which floors are done for X?"
- Asked to add a work to the stack.
- Asked to produce a work's audit record.

## The stack layout
```
translations/_stack/{work_id}/
  00_source/   01_t1.md  02_r1.md  03_t2.md
  04_r2.md  05_t3.md  06_t3_1.md  07_c1.md  AUDIT.md
```
Each floor is both **content** and **audit**. The stack wraps the flat corpus
(pointers, not moves — no file is overwritten).

## How
```bash
python3 -m pipeline.stack --list          # works with translation files
python3 -m pipeline.stack <work_id>       # assemble one work + write its AUDIT.md
python3 -m pipeline.stack --all           # assemble all detected works
```

## Reading a work's AUDIT.md
- `floors:` — which of 00_source/01_t1/02_r1/03_t2/04_r2/05_t3/06_t3_1/07_c1 are `present` vs `pending`.
- `passages: valid / needs_review / invalid` — the passage validity for that work.
- `Integrity` / `Epistemic` — the machine-verifiable checks.

## Notes
- A floor is "done" when its file exists and passes the audit.
- Missing floors = the pipeline hasn't produced them yet (pending), not an error.
- The fullest example: `sivasutra` (7 floors). Kramasadbhāva has 563 validated passages.
