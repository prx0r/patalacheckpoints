# Pramana-NLP — Sanskrit pramāṇa corpus + cleaning pipeline

**What Pāṭala borrows:** a Sanskrit pramāṇa corpus created for computational analysis (Nyāya, Buddhist
pramāṇa, epistemology, logic), assembled from GRETIL, SARIT, private collections in heterogeneous
formats (.htm, .xml, .doc). Plus the philological ETL micro-tools.

**License:** varies (no SPDX asserted). Repo: `tylergneill/pramana-nlp` (archived 2026-03).

## Reusable pieces
- `transform.py` — daisy-chains XSL transformations across heterogeneous scholarly files.
- `validate_text.py` — checks textual structure, bracket usage, suspicious character patterns.
- segmentation pipeline, metadata spreadsheets, cleaned texts, topic-model inputs, similarity analysis.

## How Pāṭala consumes it
**WATCH / CLONED.** The corpus + cleaning pipeline feed the pramāṇa/argument sources (Pratyabhijñā
argument work). The related `vatayana.info` (intertextuality search) is a downstream pattern for
passage-parallel discovery.

## Doctrine
Pre-cleaned computational material for the exact intellectual lineage (Nyāya/Buddhist pramāṇa/logic)
that feeds the Pratyabhijñā argument work.
