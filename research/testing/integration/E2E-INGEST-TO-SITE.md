# E2E PIPELINE INTEGRATION TEST — ingest → harvest → assess → queue → openpatala → site

*2026-08-15 · the full trace of one real work (`kiranatantra`) through the entire pipeline, verified
live. Each stage's command + real result. Reproducible.*

---

## The work: `kiranatantra` (a real Śaiva Tantra, from GRETIL + Muktabodha)

| Stage | Command | Real result |
|---|---|---|
| **1. INGEST** | `run_r2_ingestion --source GRETIL/MUKTABODHA --commit` | 784 + 499 SOURCE objects (idempotent: re-run commits 0) |
| **2. HARVEST** | `harvest_to_factory.py --source MUKTABODHA --dry-run` | 402 works / 318,475 verses |
| **3. ASSESS** | `assess.py --work kiranatantra` | CLEAN_ETEXT/RAW_SANSKRIT/EXACT/HIGH → NORMALIZE→SOURCE→QUEUE→TRANSLATE |
| **4. QUEUE** | `agent3_queue.eligible_works()` | 81 works; kiranatantra @ pos 9 (Krama packet first) |
| **5. OPENPATALA** | `/works/kiranatantra/translations` | partial English (Goodall) + Italian (Vivanti); 192 untranslated |
| **6. SITE** | `astro build` | 215 pages; kiranatantra archived + in translation-availability.json |

---

## The full data flow (one command chain)

```bash
# 1. ingest
python3 -m ingestion.run_r2_ingestion --all --commit
# 2. harvest (verse extraction → <work>.jsonl)
python3 pipeline/harvest_to_factory.py --all
python3 pipeline/register_harvest_sources.py
# 3. assess (the decision engine)
PYTHONPATH=pipeline python3 pipeline/assess.py --all
# 4. queue (needs vidyut in the venv)
.venv-atlas/bin/python3 -c "import sys;sys.path.insert(0,'pipeline');import agent3_queue as AQ;print(AQ.eligible_works())"
# 5. compile the translation-availability index (compute-on-write)
PYTHONPATH=python python3 pipeline/build_translation_index.py
# 6. serve (atlas API + Astro)
uvicorn patala_core.atlas.api:app --port 8791
PATALA_WEB_ROOT=/root/patalacheckpoints/web npx astro build
```

---

## Verified results

- **SOURCE registry**: 47,141 objects (incl. gretil:784 + muktabodha:499)
- **Verses**: 318,475 extractable (Muktabodha), 1.7M across all sources (documented)
- **Assess**: 125 works → 38 translate-route, 58 acquire, 29 scholar-queue
- **Queue**: 81 eligible (Krama packet first: kramasadbhava, mahanayaprakasha, kubjikamata...)
- **openpatala**: 254 works; kiranatantra = partial EN/IT; 192 untranslated targets
- **Site**: 215 pages built, 0-JS, ETag→304 on API

---

## The 3 honest caveats (from actually running it)

1. **`agent3_queue` needs `vidyut`** (in the venv, not bare python3) — the L0/queue worker path.
2. **The actual translation generation (T1/L0/L2)** is Hermes-driven and is the OTHER agent's lane —
   the queue is populated (81) but the generation worker isn't run here.
3. **The compiled site was stale** (SOURCE 501k vs live 47k) until rebuilt from the live registry —
   always run `build_translation_index.py` + `astro build` after ingest.

---

*The pipeline is real and connected end-to-end. Every stage reads/feeds the same canonical data.*
