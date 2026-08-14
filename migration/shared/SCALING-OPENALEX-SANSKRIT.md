# SCALING TO "OPENALEX OF SANSKRIT" — the honest path + the wiring gap

*2026-08-14 · status: THE SCALING PLAN · how Pāṭala becomes the "OpenAlex of Sanskrit" (the integration/
identity layer over the fragmented Sanskrit ecosystem). The honest truth: **the building blocks all
exist but NONE are wired together.** This is the exact scaling path, grounded in the real files.*

---

## 1. THE HONEST STATE (what exists vs what's connected)

### ✅ The building blocks (all real, but DISCONNECTED)
| Piece | File(s) | Status |
|---|---|---|
| The positioning (the thesis) | `docs/global/globalpartnerships.md` | ✅ fully written ("integration/identity layer") |
| The harvest adapters | `ingestion/adapters/{pandit,gretil,sarit,viaf,wikidata,iiif,ngmcp,csalt}.py` | ✅ exist as files |
| The identity machinery | `python/patala_core/atlas/{api,resolver}.py` | ✅ the OpenAlex-grammar API (works/search/filter) |
| The identity crosswalks | `source-evidence/production/adapters/{identity_crosswalk,metadata_resolver}.py` | ✅ exist |
| The bibliography | `data/corpus/atlas-bibliography.json` (254 works) | ✅ real |
| The atlas Postgres schema | `python/patala_core/atlas/migrate.py` (22 tables) | ✅ real |

### ❌ THE WIRING GAP (verified)
- **The adapters are NOT imported by any production code** — PANDiT/GRETIL/SARIT are just files, nothing calls them.
- **The identity crosswalks are NOT wired** into the atlas API or the factory.
- **The atlas API (`api.py`) reads static data** (`_load()`), not a live OpenAlex-style index.
- **The 43 site API routes read static `@/data`, not the live registry** (see `BUILD-SITE-LIVE-DATA.md`).

**So: Pāṭala is the BLUEPRINT for OpenAlex-of-Sanskrit, not the working service.** The pieces are all
there, disconnected.

---

## 2. WHAT "OPENALEX FOR SANSKRIT" MEANS (the target)

OpenAlex works because it's a **live identity/reconciliation service**: ask "what is this work / who is
this author / what cites what" → it resolves against a continuously-updated index.

For Pāṭala, that means:
```text
the fragmented Sanskrit ecosystem (PANDiT, GRETIL, SARIT, IFP, Muktabodha, NGMCP, Gyan Bharatam)
   → harvest (the adapters) → SOURCE in the registry
   → resolve (the atlas identity) → the bibliography + people + institutions
   → serve (the OpenAlex-grammar API + the site)
```
The value is NOT the data (each custodian has it). The value is **resolving it onto one canonical
identity** — "this record in PANDiT IS this work IS this edition" — with provenance + rights.

---

## 3. THE SCALING PATH (the exact steps, with the real files)

### Step 1 — Wire the harvest (the input) — `BUILD-INGESTION-HARVEST.md`
- Call the REAL adapters (pandit/gretil/sarit) into the SOURCE intake.
- PANDiT: 69,779 records, CC BY-NC-SA license firewall (discovery/provenance, never unrestricted).
- GRETIL: the 494-work corpus, via `acquire_sivaqueue_targets.py`.
- Result: the registry fills with real external-source records.

### Step 2 — The identity link — `BUILD-BIBLIOGRAPHY-IDENTITY.md`
- The 254 bibliography works resolve to their SOURCE objects (`bibliographic_id`).
- The atlas API (`api.py`) serves the OpenAlex-grammar surface (works/search/filter) from the LIVE registry.

### Step 3 — The crosswalks (the "who" surface)
- `identity_crosswalk.py` (ORCID/ROR) + `metadata_resolver.py` (OpenAlex/Crossref) resolve authors +
  institutions.
- This is the OpenAlex "people/institutions" surface.

### Step 4 — The live index (the continuous update)
- The atlas Postgres fills from the harvest (not static `_load()`).
- New records → resolve → the API serves them → the site shows them (via `BUILD-SITE-LIVE-DATA.md`).

---

## 4. THE LAUNCH VERTICAL ("at first")

Per `globalpartnerships.md`, start with ONE ecosystem (the Śaiva/Tantra vertical):
- **IFP + EFEO** (8,500+ palm-leaf codices, Śaiva Āgamas)
- **Muktabodha** (3,000+ texts, 570+ e-texts)
- **NGMCP** (180,000+ microfilmed manuscripts)
- **GRETIL/SARIT** (machine-readable Sanskrit)

Harvest their records → resolve them into the atlas → serve the OpenAlex-grammar API. **That's the
OpenAlex-for-Sanskrit v1** — the connective layer over these custodians, resolving their records onto one
canonical identity.

---

## 5. THE TEST

```bash
# 1. the adapters exist but are NOT wired (the gap)
cd /root/projects/patala
grep -rln "from .*adapters import\|import .*adapters" pipeline/ ingestion/ | wc -l  # should be >0 after wiring

# 2. the atlas API serves the OpenAlex-grammar surface
cd python/patala_core/atlas && python3 api.py  # the /works + /search OpenAlex-grammar API

# 3. after the harvest wiring: a PANDiT record resolves to a canonical work
python3 -c "
import sys; sys.path.insert(0,'/root/projects/patala/pipeline')
import object_registry as R
print('SOURCE:', len(R._load('SOURCE')['objects']))
"
```

**Pass when:** a PANDiT/GRETIL/SARIT record is harvested → resolved to a canonical work (with rights +
provenance) → served by the OpenAlex-grammar API → visible on the site. That's OpenAlex-for-Sanskrit v1,
working — not just specced.
