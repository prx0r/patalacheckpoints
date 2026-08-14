# THE DATA ASSETS INDEX — everything machine-readable that actually exists

*2026-08-14. The catalog of Pāṭala's **real data and real data-systems** — the machine-readable assets
that exist and can be queried, but were under-surfaced in the architecture docs. This is the "what data
do we actually have, and how do I query it?" reference. Complements `GOLD-EVIDENCE-INDEX.md` (verified
results) — this is the *data*, not the proofs.*

> **The principle:** the architecture docs describe machinery and vision. THIS is the actual data layer —
> the corpus, the targets, the registries, the site model. An agent should read this before querying or
> building data systems.

---

## 1. THE CORPUS TARGETS SYSTEM (the acquisition goldmine) — `docs/corpus/TARGETS-INDEX.md`

The master index consolidating every translation target, lead, source, and scholarly reference. Compiled
to machine-readable by `build_corpus_targets_db.py` → `data/corpus/targets/`:

| File | What | Count |
|---|---|---|
| `targets/sources.json` | downloaded source files | 64 |
| `targets/targets.json` | actionable RAW-L0 targets | 21 (Krama packet first) |
| `targets/leads.json` | acquisition leads (register I/II/III) | 39 |
| `targets/anchors.json` | translation anchors (which texts already have English) | 16 |
| `targets/sivaqueue.json` | **the second-corpus registry ("Śiva before Abhinava")** | **100 targets + 15 companion guides (G1-G14)** |
| `targets/index.json` | master doc index | 26 source docs |

**Query:** `python3 pipeline/agent3_queue.py --registry / --leads / --sivaqueue / --sivaqueue-work <id>`
**The master substrate:** `docs/corpus/canonical_reference_map.md` (1355 lines) — the Trika/Krama/Kubjikā/
Kaula/Spanda/Pratyabhijñā ecosystem + **the semantic-shift glossary** (lemma → sense per tradition/period/
evidence — do NOT build a single Tantric dictionary, build an evidence graph).

---

## 2. THE SIVAQUEUE MANIFESTS (the intake state) — `data/corpus/sivaqueue*.json`

The acquisition/translation state for the second corpus (100 "Śiva before Abhinava" targets):
| Manifest | Contents |
|---|---|
| `sivaqueue-targets.json` | the 100 targets + period/tradition/status |
| `sivaqueue-acquired.json` + `sivaqueue2-acquired.json` | what's been acquired |
| `sivaqueue-access-manifest.json` | access/rights per target |
| `sivaqueue-guides.json` | the G1-G14 companion guides |
| `source-ready.json` | **the factory intake state (236 entries)** — which works are ready to translate |

---

## 3. THE VERSIONED REGISTRIES (the factory's object state) — `data/corpus/registries/`

The live object store per layer (versioned, hash-chained via `object_registry`):
| Registry | Layer | (live counts via `docs_state.py`) |
|---|---|---|
| `source-registry.jsonl` | SOURCE | 32,039 |
| `l0-registry.jsonl` | L0 | 791 |
| `t1-registry.jsonl` | T1 | 306 |
| `argmap-registry.jsonl` | ARGMAP | 50 |
| `l2/l1l2/l200/c1/theme/argument/span/witness/assertion/corroboration` | the upper layers | see `docs_state.py` |
| `object-events.jsonl` | **the append-only event ledger** | 18.9 MB, hash-chained |
| `verification-registry.jsonl` | attestations (archive.org/GRETIL) | 22 entries |

**Query:** `python3 pipeline/object_registry.py` (summary) · `python3 docs/process/docs_state.py` (live layer state).

---

## 4. THE SITE DATA MODEL — `data/atlas/` + `data/corpus/*.ts`

The site's canonical data (consumed by the Next.js app):
| File | What |
|---|---|
| `data/atlas/texts.ts` · `traditions.ts` · `people.ts` · `concepts.ts` · `relations.ts` | the atlas graph |
| `data/atlas/audited.ts` + `bibliographySeed.ts` + `bibliographyTypes.ts` | the bibliography (254 works) |
| `data/atlas/historyTimeline.json` | the tradition timeline |
| `data/corpus/gold.ts` · `graph.ts` · `primitives.ts` · `terms.ts` · `themes.ts` · `hub.ts` | the corpus graph |
| `data/corpus/atlas-bibliography.json` | the thin compiled bibliography |
| `data/corpus/manuscripts.ts` · `sources/` · `passages/` | the manuscript + source + passage data |

---

## 5. THE PUBLISHED CORPUS — `data/published/`

| Asset | Count |
|---|---|
| `data/published/ipvv/` | **49+ IPVV passages** (`pt:passage:ipvv:chunk*-md.json`) + `index.json` |
| (IPVV vertical dossier) | `IPVV-VERTICAL-001-SOURCE-DOSSIER.md` |

---

## 6. THE QUERY SURFACE (how to actually use this data)

```text
Corpus targets    → python3 pipeline/agent3_queue.py --registry / --sivaqueue
Live factory state → python3 docs/process/docs_state.py
Object registry   → python3 pipeline/object_registry.py
Attestations      → data/corpus/registries/verification-registry.jsonl
Bibliography      → data/corpus/atlas-bibliography.json (+ the .ts sources)
Site data         → data/atlas/*.ts + data/corpus/*.ts (the Next.js app reads these)
```

---

## 7. HOW AN AGENT USES THIS

```text
"what data do we actually have?"  →  this index
  → the corpus targets (21 RAW-L0 + 100 sivaqueue + 39 leads)  →  the acquisition goldmine
  → the registries (32k SOURCE, 791 L0, ...) + event ledger      →  the live object state
  → the bibliography (254) + site data model                     →  what the site renders
  → the published IPVV (49)                                      →  the published corpus
```

---

*This is the data-assets index. It complements `GOLD-EVIDENCE-INDEX.md` (verified results) and
`IPVV-BUILD.md` (the IPVV specifically): this is the full map of the real machine-readable data and the
acquisition/site systems that own it.*
