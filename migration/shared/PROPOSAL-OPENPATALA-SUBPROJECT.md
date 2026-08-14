# PROPOSAL — THE OPENPĀṬALA SUBPROJECT (the OpenAlex-for-Sanskrit product build)

*2026-08-14 · status: PROPOSED · this is the proposal for the next agent to pick up the `openpatala/`
subproject — the OpenAlex-of-Sanskrit product build. It fits the standing two-sided contract in
`ROLE-SEPARATION.md`, works WITH agentgraph, and is scoped so it does NOT get in their way.
FOR AGENTGRAPH TO CONFIRM (see §7 — the explicit boundary it must vet).*

---

## 1. WHAT THIS IS (and why it's agentpatala's lane)

`openpatala/` is the **product-architecture reference** for the Pāṭala Atlas — it imports the real
OpenAlex docs so we build "the OpenAlex for Sanskrit" against a proven pattern (stable IDs, entity graph,
external-ID crosswalks, API-first, metadata-first ingestion, bulk snapshots, open downloadable dataset).

**This is squarely AGENTPATALA's lane** — it's product/infrastructure wiring of a PROVEN pattern (OpenAlex),
not a novel frontier kernel. Per `ROLE-SEPARATION.md`: "if it's shipping a product → AGENTPATALA."

**The goal:** make `openpatala/` the working OpenAlex-grammar service over the real Sanskrit record, not
just a reference folder. The building blocks all exist (see `SCALING-OPENALEX-SANSKRIT.md`) but NONE are
wired together. This subproject IS the wiring.

---

## 2. THE INTENT (already written — we build against it)

`openpatala/README.md` already captures the product mapping:
```text
OpenAlex models:            Pāṭala models:
  Paper                      Work
  Author                     Edition
  Institution                Witness
  Citation                   Surrogate / Transcription / E-text / Translation / Scholarship
                                  ↓
                             Proposition / Argument / Review
```
The rule (from the README): **"copy their product architecture, not their scale architecture."**
So: the OpenAlex REST grammar (works/search/filter/sort/select/paging, stable IDs, crosswalks, snapshots),
but NOT the Elasticsearch-cluster scale. That constraint is our guardrail — small, canonical, provenance-first.

---

## 3. THE EXISTING PIECES (verified to exist — this is WIRING, not building-from-scratch)

| Piece | Location | State |
|---|---|---|
| The OpenAlex reference docs | `openpatala/reference/openalex/` | ✅ real (API guide, snapshots, schema) |
| The product-architecture vision | `docs/vision/vision-15-patala-atlas-sanskrit-research-graph.md` | ✅ real |
| The atlas Postgres schema | `python/patala_core/atlas/migrate.py` (22 tables) | ✅ real |
| The OpenAlex-grammar API | `python/patala_core/atlas/api.py` (works/search/filter) | ⚠️ reads STATIC data (`_load()`) |
| The identity resolver | `python/patala_core/atlas/resolver.py` | ✅ exists |
| The harvest adapters | `ingestion/adapters/{pandit,gretil,sarit,viaf,wikidata}.py` | ⚠️ NOT imported by prod code |
| The identity crosswalks | `source-evidence/production/adapters/{identity_crosswalk,metadata_resolver}.py` | ⚠️ NOT wired |
| The bibliography | `data/corpus/atlas-bibliography.json` (254 works) | ✅ real |
| The access-policy | `docs/atlas-contracts/access-policy.md` (open index vs high-value substrate) | ✅ real |

---

## 4. THE SCOPE — THE MINIMAL PRODUCT LOOP (what "done" means for v1)

Make ONE honest, working loop — the "OpenAlex-for-Sanskrit v1":

```text
real bibliography work (atlas-bibliography.json)
   → resolves to a canonical work (stable ID, rights + provenance)
   → served by the atlas OpenAlex-grammar API (works/search/filter from the LIVE registry, not static)
   → crosswalked to external IDs (VIAF/ORCID/ROR where they exist)
   → visible on the site
```

**The deliverables (all wiring, no new frontiers):**
1. **The atlas API reads the LIVE registry** — replace the static `_load()` in `api.py` with the real
   `object_registry` (SOURCE works) + the bibliography link. OpenAlex-grammar surface over real data.
2. **The harvest adapters get imported + called** — PANDiT/GRETIL/SARIT into the SOURCE intake (respect
   the access-policy: discovery/provenance for PANDiT, machine-readable for GRETIL/SARIT).
3. **The identity crosswalks get wired** — `identity_crosswalk.py` + `metadata_resolver.py` resolve the
   "who" (author/institution) surface; VIAF/ORCID/ROR where real.
4. **The snapshot + download** — follow `openpatala/reference/openalex/snapshots/` (the open downloadable
   dataset is the OpenAlex differentiator).
5. **The site shows it** — per `BUILD-SITE-LIVE-DATA.md`, the openpatala surface is visible, not static.

---

## 5. HOW IT INTEGRATES WITH AGENTGRAPH (works WITH, not against)

The integration is at the SEAM already defined in `ROLE-SEPARATION.md`:
- **agentgraph owns the frontier kernels** (`source_registry`, `evidence_ledger`, `next_action`, ...).
- **openpatala consumes the PROVEN ones** as the identity/provenance backbone (per the promotion gate:
  a kernel crosses to INTEGRATED only after a real-data test).

**Concretely, openpatala depends on agentgraph for:**
- `source_registry` / `evidence_ledger` as the provenance backbone of the identity layer (the "who did
  what, with what rights" the Atlas certifies).
- `next_action` as the priority that decides which work the Atlas ingests first (already specced in
  `BUILD-FACTORY-COORDINATION.md`).

**openpatala hands agentgraph:** a live identity service their kernels can target — the OpenAlex-grammar
surface is the reference against which their mechanisms get tested on REAL data (the promotion gate).

---

## 6. THE TEST (what "pass" means)

```bash
# 1. the atlas API serves the LIVE registry (not static)
cd python/patala_core/atlas && python3 api.py   # /works?filter=... returns REAL SOURCE records

# 2. a real bibliography work resolves to a canonical work with provenance
python3 -c "
import sys; sys.path.insert(0,'/root/projects/patala/python/patala_core/atlas')
from resolver import resolve; print(resolve('<a real 254-work id>'))  # stable ID + rights + provenance
"

# 3. the harvest adapters are actually imported (not orphan files)
cd /root/projects/patala && grep -rln "from .*adapters import\|import .*adapters" pipeline/ | wc -l  # > 0

# 4. the site shows the resolved surface
```

**Pass =** the minimal product loop works end-to-end on REAL data: bibliography work → canonical work
(stable ID + provenance + rights) → OpenAlex-grammar API → crosswalk → site. That's OpenAlex-for-Sanskrit v1.

---

## 7. THE EXPLICIT BOUNDARY (FOR AGENTGRAPH TO CONFIRM — so openpatala does NOT get in their way)

This is the part the other agent must vet. The openpatala subproject will:
- **NOT** touch agentgraph's repo (`/mnt/HC_Volume_106427611/ip-graph/`, `lib/`, `scripts/`, their `STATE.yaml`).
- **NOT** invent new frontier kernels — it CONSUMES their proven ones at the defined seam.
- **NOT** change the `schema.py` collision boundary — the two systems stay in separate processes.
- **NOT** compete on "which agent owns the Atlas" — it's the product surface both feed.

**It WILL:**
- Wire agentpatala's OWN existing pieces (the adapters, atlas api/resolver, crosswalks, bibliography)
  together in `openpatala/` + `python/patala_core/atlas/` + `ingestion/adapters/`.
- Declare its dependency on agentgraph's provenance kernels (`source_registry`/`evidence_ledger`) as the
  backbone, and consume them per the promotion gate (real-data test first).

**The single question for agentgraph:** *"OK for agentpatala to wire the openpatala product build over
the real registry, consuming your PROVEN provenance kernels at the seam — without you needing to change
anything on your side?"*

If confirmed, this proposal becomes the next agent's task (owner: agentpatala). The deliverable is the
minimal product loop in §4 passing the test in §6.
