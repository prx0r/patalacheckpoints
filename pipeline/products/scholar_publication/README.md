# scholar_publication — the Astro-servable JSON-LD scholar records

The bridge from the interactive scholar layer to the PUBLIC site: compiles a scholar's contributions
into immutable, JSON-LD, citable records the Astro site serves (the "CV-legible output" from vision-08).

## Run
```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/scholar_publication/test.py   # 5/5 proof
PYTHONPATH=pipeline python3 pipeline/products/scholar_publication/engine.py all
PYTHONPATH=pipeline python3 pipeline/products/scholar_publication/engine.py publish
```

## Engine API
```python
from products.scholar_publication.engine import profile_record, publish_all
publish_all(out_dir)   # emits scholar-*.json + attestation-*.json (JSON-LD, Astro-servable)
```

## Why it matters
The scholar product's PUBLIC surface — what the Astro site serves as immutable bytes. A scholar's
reviews + attestations become citable records, not disconnected acts.
