# manuscript_ingest — manuscript → Pāṭala SOURCE adapter (honest quality ladder)

Turns a manuscript + (optionally) its OCR text into a labelled, quality-scored Pāṭala SOURCE object
ready to enter the factory queue. The OCR itself is an **adapter boundary** (kraken/eScriptorium on a
GPU box); this product turns OCR output into a provenance-bearing SOURCE with an honest quality score.

## The quality ladder (vision-14)
`raw_scan → ocr_done → clean_etext → factory_ready`
- **raw_scan** (photos, no text) → status `PENDING_OCR`, not translate-ready
- **ocr_done** (OCR text) → needs review, **not auto-ready** (honest)
- **clean_etext** (has transcription) → **factory-ready** → SOURCE queue → T1

## Run
```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/manuscript_ingest/test.py   # 8/8 proof
PYTHONPATH=pipeline python3 pipeline/products/manuscript_ingest/engine.py demo
```

## Engine API
```python
from products.manuscript_ingest.engine import to_source, ingest_batch
s = to_source({"id":"pt:ms:...","script":"Devanagari","photos":True,"text":True})
# -> {quality, status, payload.provenance, ready_for_translate, route}
```

## Why it matters
The honest "how do we go from a shitty manuscript to a clean, labelled, translate-queue entry" — the
deterministic brain (routing + quality + SOURCE adapter) that works on CPU; the OCR is the GPU boundary.

## Honest limits
- Does NOT OCR — the OCR engine is the adopted GPU boundary (kraken/eScriptorium).
- Quality is MACHINE_PROPOSED; a scholar/pe-ocr gate decides if OCR is good enough to enter the factory.
