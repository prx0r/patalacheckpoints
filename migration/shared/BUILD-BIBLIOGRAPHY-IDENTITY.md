# BUILD: THE BIBLIOGRAPHY ↔ IDENTITY ↔ FACTORY LINK (with editions)

*2026-08-14 · status: WHAT TO BUILD (for agentgraph) · the precise build spec for wiring the REAL OG
patala bibliography (254 works + rich editions) into ip-graph's graph/identity, referencing the ACTUAL
files.*

---

## THE GAP

ip-graph's `works.jsonl` is the Doyle/science corpus. OG patala has the REAL Sanskrit bibliography: **254
works** (thin) + **rich edition data** (Trika-10 full depth) + the identity seeds. ip-graph needs this as
its identity layer.

---

## THE REAL OG PATALA BIBLIOGRAPHY FILES (reference these)

### 1. The thin compiled bibliography (the 254-work index)
**`/root/projects/patala/data/corpus/atlas-bibliography.json`**
- `backend: postgres`, 254 records
- Each record: `{id, title, translation_status, verified}` (4 fields — THIN, no editions)

### 2. The RICH bibliography sources (with editions) — the real depth ip-graph needs
| File | Works | Depth |
|---|---|---|
| `/root/projects/patala/data/atlas/audited.ts` | 11 (Trika-10) | **FULL** — textSources (edition/critical_edition/etext, tier A/B, editor, year), translations (language/translator/coverage), traditions |
| `/root/projects/patala/data/atlas/bibliographySeed.ts` | 59 | medium — traditions, translationStatus, statusLabel |
| `/root/projects/patala/data/atlas/sanskritreeImportSeed.ts` | (old-batch import) | the sanskritree T1/T3 works, verified:false |
| `/root/projects/patala/data/atlas/sivaqueueSeed.ts` / `sivaqueue34Seed.ts` / `sivaqueueGapSeed.ts` | the sivaqueue targets | the 100-work priority registry |
| `/root/projects/patala/data/atlas/bibliographyTypes.ts` | the `BibliographyRecord` schema | the type every seed conforms to |

### 3. The identity-support data (the OpenAlex-for-Sanskrit layer)
- `/root/projects/patala/data/atlas/people.ts` — the scholars (Ratié, Torella, Sanderson, ...)
- `/root/projects/patala/data/atlas/traditions.ts` — the traditions
- `/root/projects/patala/data/atlas/relations.ts` — the work relations
- `/root/projects/patala/data/atlas/resources.ts` — the external-resource register
- `/root/projects/patala/data/atlas/concepts.ts` — the concepts
- `/root/projects/patala/data/atlas/index.ts` — the atlas barrel

### 4. The atlas identity machinery
- `/root/projects/patala/python/patala_core/atlas/migrate.py` — the Postgres 22-table schema
- `/root/projects/patala/python/patala_core/atlas/resolver.py` — per-dimension authority + rights gates
- `/root/projects/patala/python/patala_core/atlas/api.py` — OpenAlex-grammar API
- `/root/projects/patala/python/patala_core/atlas/adapter.py` — the dual backend

---

## THE EDITION DATA (the depth ip-graph is missing)

The `audited.ts` records have FULL edition/translation depth, e.g.:
```typescript
textSources: [
  { type: "edition", coverage: "complete", provider: "Muktabodha M00160", tier: "B" },
  { type: "critical_edition", coverage: "chs. 1–4, 7, 12–17", editor: "Somadeva Vasudeva", year: 2004, tier: "A" },
],
translations: [{ language: "en", translator: "Somadeva Vasudeva", ... }],
```
**This is the scholarly edition data ip-graph's graph lacks.** The thin `atlas-bibliography.json` only
has 4 fields; the rich `audited.ts` + `bibliographySeed.ts` have the editions, translators, tiers, and
providers.

---

## WHAT TO BUILD (wire it into ip-graph's graph)

### The build:
1. **The identity link:** make the 254 works resolve to their SOURCE objects via `bibliographic_id`
   (already in the state ledger). `data/corpus/atlas-bibliography.json` (254) ↔ `object_registry` SOURCE.
2. **The edition enrichment:** compile the RICH edition data (`audited.ts` + `bibliographySeed.ts`) into
   ip-graph's `works.jsonl` — so each work carries its editions, translators, tiers, providers.
3. **The identity layer:** ip-graph's graph nodes resolve to the real bibliography IDs (the
   OpenAlex-for-Sanskrit identity). `atlas/api.py` is the resolver.

### The WHY:
The thesis is "OpenAlex for Sanskrit" — the identity/reconciliation layer. The 254-work bibliography (with
editions) IS the identity graph. ip-graph's graph must reference these real IDs, so a concept or argument
node resolves to the real work, its editions, and its translations. Right now ip-graph's works.jsonl has
none of this.

---

## THE TEST

```bash
# verify the rich edition data is parseable + count
python3 -c "
import re
txt=open('/root/projects/patala/data/atlas/audited.ts').read()
print('edition refs in audited.ts:', len(re.findall(r'critical_edition|edition', txt)))
"
# verify the 254 thin works resolve to SOURCE
python3 -c "
import sys; sys.path.insert(0,'/root/projects/patala/pipeline')
import object_registry as R
print('SOURCE objects:', len(R._load('SOURCE')['objects']))
"
```

**Pass when:** a concept/argument node in ip-graph's graph resolves to a real bibliography work, its
editions (tier A critical edition, translator, provider), and its factory state.
