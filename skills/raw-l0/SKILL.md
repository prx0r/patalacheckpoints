---
name: raw-l0
description: "Convert a new RAW Sanskrit work/verse into audited, canonical Pāṭala L0 (the IPVV 15-field schema), validated by verify_l0.p0_proof, and register the progress in the corpus-state ledger. Use when asked to ingest a new raw Sanskrit text, produce RAW-L0 / L0-SOURCE-MODE, or test that a new raw verse yields a successful v0 L0. This is the autonomous Agent 3 factory's Build 1."
version: 1.0.0
author: Pāṭala
metadata:
  hermes:
    tags: [sanskrit, raw-l0, l0, pipeline, factory, agent3, patala, scholarly]
    related_skills: [translate-passage, validate-passage, assemble-stack, use-api]
    checkpoint: CP1 (the source floor) → the autonomous RAW-L0 factory (A3)
---

# RAW-L0 — raw Sanskrit → audited canonical L0

## When to use
- Asked to ingest a NEW raw Sanskrit work or verse (not the IPVV).
- Asked to produce RAW-L0 / L0-SOURCE-MODE / "MODE_B".
- Asked to test whether a raw verse yields a successful v0 L0.
- Asked to advance the autonomous Agent 3 factory on a `RAW_SANSKRIT` work.

## The one thing to get right
**Emit the SAME canonical L0 schema the IPVV uses**, so the existing machinery
(`verify_l0.py` P0 proof, the published store, the C1 chain) consumes it UNCHANGED.
The precedent is `extract_l0_v1.py` (non-standard → canonical L0 that passes `verify_l0`).

## The flow (per verse — the atomic unit)

```
RAW SANSKRIT
   ↓  [pipeline/raw_l0.py]
canonical L0 records (15-field schema)
   ↓  [verify_l0.p0_proof — the EXISTING harness]
P0 proof (source_span PROVED · unknown_chars 0 · PASS)
   ↓  [pipeline/agent3_batch.py]
ledger update (RAW_SANSKRIT/BLOCKED → ELIGIBLE) + batch manifest (progress)
```

## Step 1 — get the raw source
The corpus-state ledger knows each work's `source_ref` (e.g. the Dyczkowski Kramasadbhāva
edition). Load it, or take the verse directly.

## Step 2 — run the deterministic core (no model needed)
```bash
python3 pipeline/raw_l0.py --work <work> --passage <work>:<loc> --sanskrit "<verse>"
```
This uses Vidyut (segmentation + lemma + morphology) to build canonical L0 records, then
runs the EXISTING `verify_l0.p0_proof`. Output: `data/corpus/downloads/raw-l0-canonical.json`.

**Verse locators** (`||1/1`) are stripped as STRUCTURAL (the passage locator, not content) so
P0 sees only the semantic Sanskrit.

**Abstention is honest:** a token Vidyut can't analyze (lemma=null) → `status: AMBIGUOUS`,
never `PARSED`. A lacuna verse (`* * * *`) → FAIL (sent to the review path). Never fabricate.

## Step 3 — batch a whole work (the factory loop)
```bash
python3 pipeline/agent3_batch.py --work <work> --max-verses N
```
Splits the raw source into verses, runs RAW-L0 per verse, audits (canonical schema + P0 PASS),
updates the ledger, writes `data/corpus/downloads/agent3-batches/<work>-batch.json`.

## Step 4 — the gloss (the generative layer, optional)
`literal_gloss` is genuinely an LLM task. Provide it via `--gloss-file` (a JSON
`{token: {literal, compound, supplied}}`) or a model call. The deterministic core + validation
NEVER depend on it. `literal_gloss` is MACHINE_PROPOSED, never "proved".

## Step 5 — verify + register
- Confirm the records have all 15 canonical fields: `id, chunk_id, line_id, line_kind,
  chunk_char_start, chunk_char_end, line_char_start, line_char_end, wraps_line, raw_fragment,
  source_text, lemma_iast, literal_gloss, quoted, status`.
- Confirm `P0: PASS`, `unknown_chars: 0`.
- Confirm the ledger moved the work forward (`RAW_SANSKRIT → ELIGIBLE`).

## The validation (what makes a v0 L0 "successful")
- [ ] canonical 15-field schema (all records, no missing)
- [ ] `verify_l0.p0_proof` PASS (unknown_chars 0)
- [ ] lemma=null → AMBIGUOUS (abstain, not fabricated)
- [ ] lacuna/unanalyzable → FAIL → review path (not a fake pass)
- [ ] ledger updated + batch manifest written (progress tracked)

## Falsification test
> What would convince you this does NOT work? A verse that claims a PARSED lemma Vidyut never
> produced, or a P0 PASS with unknown_chars>0, or records missing a canonical field.

## Test-drive on a new raw translation
1. Take a fresh raw verse (e.g. another Kramasadbhāva verse, or a new work's verse).
2. Run `raw_l0.py` → confirm canonical records + P0 PASS.
3. Run `agent3_batch.py` → confirm the ledger + batch manifest update.
4. Inspect the completed record: all 15 fields, honest AMBIGUOUS where Vidyut can't analyze.
5. Supply a gloss (file or model) → the record is a complete MACHINE_PROPOSED L0.
