# BUILD: THE EXTERNAL-SOURCE HARVEST (R2 adapters → SOURCE) — the real Sanskrit input

*2026-08-14 · status: WHAT TO BUILD (for agentgraph) · the precise build spec for wiring the REAL external
harvest into ip-graph's `ingestion_organism`, referencing the ACTUAL OG patala files that already exist.*

---

## THE GAP

ip-graph's `ingestion_organism.py` is the loop design, but it has **no real Sanskrit input** — its
`corpus.jsonl` is the Doyle/science-paper corpus. OG patala has the REAL harvest machinery (PANDiT/GRETIL/
SARIT adapters + the R2 snapshot store) that ip-graph needs.

---

## THE REAL OG PATALA FILES (already built — reference these)

### 1. The harvest adapters (in `/root/projects/patala/ingestion/adapters/`)
| File | What it harvests | Rights |
|---|---|---|
| `pandit.py` | the PANDiT bulk export (69,779 records, 9 content types, 163 cols) | CC BY-NC-SA 4.0 (license firewall) |
| `gretil.py` | GRETIL machine-readable Sanskrit (the 494-work corpus, GRETIL_MATCHES) | CC BY-NC-SA |
| `sarit.py` | SARIT TEI scholarly editions | open |
| `csalt.py` | C-SALT | — |
| `iiif.py` | IIIF manuscript images | — |
| `ngmcp.py` | Nepalese manuscript records | — |
| `viaf.py` | VIAF identity | — |
| `wikidata.py` | Wikidata identity | — |

### 2. The R2 snapshot store (in `/root/projects/patala/ingestion/r2.py`)
`SnapshotStore` — the immutable Bronze layer:
- `put_snapshot(source, snapshot_id, files)` → R2 `source/ingestion/<SRC>/snapshots/<id>/` + manifest
- Content-addressed, idempotent (same bytes = same key)
- The doctrine: every harvest → R2 Bronze → immutable → then process

### 3. The R2 buckets (the actual external data, verified live)
`patala · sourcematerial · atlas-sources · sanskritree · factory-assets · research-datasets` (+ media buckets)

### 4. The acquisition/targets system (the priority queue data)
- `pipeline/translation_targets.py` — the priority-ordered registry (kramasadbhava p10 → Krama packet first)
- `pipeline/agent3_queue.py` — the autonomous driver (`process_next`, `--registry`, `--sivaqueue`)
- `pipeline/acquire_sivaqueue_targets.py` — GRETIL download with verified matches
- `data/corpus/targets/sivaqueue.json` — 100 untranslated targets with period/tradition

---

## WHAT TO BUILD (wire them into `ingestion_organism`)

### The build:
1. `ingestion_organism.ingest()` should call the REAL adapters (pandit/gretil/sarit), not a hand-fed doc:
   - `pipeline/agent3_queue.py` picks the priority work (the sivaqueue, 100 targets)
   - `pipeline/acquire_sivaqueue_targets.py` downloads the GRETIL source
   - `ingestion/r2.py` SnapshotStore → R2 Bronze (immutable, content-addressed)
   - `ingestion/adapters/pandit.py` handles the license firewall (CC BY-NC-SA → discovery/provenance, never unrestricted)
2. The harvested source → content-addressed SOURCE objects in `object_registry` (via `ingestion/asserter.py`).
3. `ingestion_organism` tracks the per-work harvest state (source_registry rights + health).

### The WHY:
The thesis is "OpenAlex for Sanskrit" — the connective layer over PANDiT/GRETIL/SARIT/Muktabodha. The real
harvest adapters ARE that connective layer. ip-graph's organism is the loop; these adapters are the real
input. Wiring them makes the organism ingest ACTUAL untranslated Sanskrit, not the Doyle corpus.

---

## THE TEST (how agentgraph verifies)

```bash
# dry-run the harvest of a real work from the priority queue
python3 /root/projects/patala/pipeline/agent3_queue.py --registry
python3 /root/projects/patala/pipeline/acquire_sivaqueue_targets.py --work sardhatrisatikalottara --dry-run
# then: ingestion_organism.ingest() on the harvested source
```

**Pass when:** a real untranslated Sanskrit work from the sivaqueue flows R2 → SOURCE in the registry, with
correct rights (PANDiT = CC BY-NC-SA firewall, never unrestricted).
