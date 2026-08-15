# manuscript_routing — the manuscript-onboarding diagnostic (vision E3)

Labels + routes a manuscript record: given its metadata (script, photos, text, incipit), tell it what
it needs (OCR → clean → re-derive). This is the "what transformation does this manuscript need" step
from vision-14 §4. Adopts kraken+eScriptorium for OCR (never rebuilds it).

## Run
```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/manuscript_routing/test.py   # 7/7 proof
PYTHONPATH=pipeline python3 pipeline/products/manuscript_routing/engine.py demo
```

## Engine API
```python
from products.manuscript_routing.engine import route_manuscript
r = route_manuscript({"id":"pt:ms:...","script":"Devanagari","photos":True,"text":False})
# -> {label: DEVANAGARI_SCAN, route: OCR_THEN_FACTORY, ocr_tool: kraken+eScriptorium, ...}
```

## Routes
- `OCR_THEN_FACTORY` — photos, no text → kraken OCR → post-OCR check → SOURCE → T1
- `FACTORY_READY` — clean text (incl. OCR'd) → SOURCE → T1
- `NEEDS_TEXT` — has photos but no transcription
- `IDENTIFY_THEN_ROUTE` — incipit anchors identity → resolve work first
- `UNROUTEABLE` — no text/photos/anchor

## Honest limits
- It ROUTES; it does NOT OCR. The OCR engine is the adopted GPU boundary (kraken/eScriptorium).
- Never fabricates a work identity — resolve first.
