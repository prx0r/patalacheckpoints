# OPENPATALA — HOW IT WORKS + HOW IT'S VALIDATED (the run/verify reference)

*2026-08-14 · status: OPERATIONAL · the concrete how-it-works + how-to-validate reference for the
OpenPāṭala build. Complements `BUILD-OPENPATALA.md` (the plan + checkpoints). This file is the
"press the buttons and prove it" doc — every command a new agent runs to see the live surface and
confirm it's real (anti-theatre: each check is reproducible + measured, not "code exists").*

---

## 1. THE ARCHITECTURE (one screen)

```text
object_registry (the live truth: SOURCE/T1/L0/... 47,102 SOURCE)
   + bibliography (254 works) + the R2 source snapshots (GRETIL/SARIT/MUKTABODHA/PANDIT)
        │
        ▼
   THE PROJECTION COMPILER   scripts/build-static-site.py  (agentgraph's, extended)
   (compute on write: rebuild-on-commit.py — unchanged = no-op)
        ▼
   IMMUTABLE CONTENT-ADDRESSED ARTIFACTS   site/   +  R2 releases/
        │
   ┌────┼────────┬────────────┐
   ▼    ▼        ▼            ▼
API  the site   crosswalk   R2 release
(openpatala    (0-JS work   (/resolve →    (works.jsonl
 + /works)     pages)       OpenAlex/Crossref)  + .parquet)
```

**The three truths (per `openpatala/README.md`):** Postgres = entity truth (future) · R2 = artifact
truth (content-addressed SHA-256) · the object_registry/event log = the live factory truth. Everything
else (the site, the search index, the Parquet snapshots) is a **rebuildable projection**.

---

## 2. THE SOURCE INGESTION (how the 47,102 SOURCE objects got there)

**Full file ingestion from the R2 snapshots** (`ingestion/run_r2_ingestion.py`), not the network:

| Source | Files | Records | Adapter |
|---|---|---|---|
| GRETIL | 784 TEI XML | 784 | file-based TEI parse (title/author from `<teiHeader>`) |
| MUKTABODHA | 499 IAST .txt | 499 | `ingestion/adapters/muktabodha.py` (built this session) |
| SARIT | 85 TEI XML | 85 | file-based TEI parse |
| PANDIT | 18MB bulk CSV (69,779 rows) | 13,695 unique Works | `PanditBulkAdapter` (content_types=["Work"]) |

**Total: 15,063 unique SOURCE objects added** (SOURCE 32,039 → 47,102). Idempotent — re-running
commits 0 (dedup by external_id).

**The honest provenance discipline (per the atlas contracts):**
- `status: MACHINE_PROPOSED` — NEVER `verified=true` (no fake truth).
- `license` recorded on every object (CC-BY-NC-4.0 for Muktabodha, per-file for GRETIL/SARIT) — the
  license firewall (PANDiT is CC BY-NC-SA: discovery/index/provenance only).
- External id preserved as a **crosswalk** in `provenance.external_id`, not canonical identity.
- The SOURCE registry uses semantic keys (consistent with the factory's existing `ipvv:V2L:k22`,
  `brahmayamala:v59`) — the `PT*` typed-ID discipline belongs to the Atlas Postgres layer, not the
  factory object store.

---

## 3. HOW TO RUN IT (the buttons)

### 3.1 Ingest / re-ingest the R2 snapshots
```bash
cd /root/projects/patala
python3 -m ingestion.run_r2_ingestion --all --dry-run   # report only (no writes)
python3 -m ingestion.run_r2_ingestion --all --commit    # commit SOURCE objects (idempotent)
```

### 3.2 Rebuild the compiled site projections (compute-on-write)
```bash
cd /mnt/HC_Volume_106427611/ip-graph
python3 scripts/rebuild-on-commit.py    # 1st rebuilds; 2nd = "no inputs changed" (no-op)
```

### 3.3 Build the open-data release snapshot + upload to R2
```bash
cd /root/projects/patala
python3 pipeline/build_release_snapshot.py --dry-run   # build, no upload
python3 pipeline/build_release_snapshot.py            # build + upload to R2 releases/<date>/
# (needs R2_ACCESS_KEY_ID + R2_SECRET_ACCESS_KEY in env)
```

### 3.4 Run the OpenAlex-grammar API
```bash
cd /root/projects/patala/python
python3 -m uvicorn patala_core.atlas.api:app --port 8787
# GET /works            the bibliography (254 works, filter/search/select/cursor)
# GET /openpatala       the live registry summary (SOURCE 47,102, T1 314, ...)
# GET /openpatala/{layer}  one layer projection (compiled bytes)
# GET /resolve?title=&author=  the identity crosswalk (OpenAlex/Crossref, live)
```

---

## 4. HOW IT'S VALIDATED (the anti-theatre gate)

Every claim must be **reproducible + measured**, never "code exists." The full validation suite:

### 4.1 The validators (repo integrity)
```bash
cd /root/projects/patala
python3 check_directory_manifest.py          # every top-level folder → role/layer/class
python3 docs/vision/check_manifest.py        # every vision doc → one role/file
python3 docs/check_docs_audit.py             # every loose docs/ file → classified
python3 docs/process/docs_state.py           # the live per-layer state (from object_registry)
```
**Pass = all VALID.**

### 4.2 The unit/integration tests
```bash
cd /root/projects/patala
python3 ingestion/test_smoke.py              # adapter contract + run_ingestion  → SMOKE TEST PASS
python3 ingestion/test_asserter.py           # SourceAsserter (false-merge guard) → ASSERTER TEST PASS
python3 source-evidence/production/adapters/test_identity_crosswalk.py → PASS
(cd python && python3 patala_core/atlas/test_api.py)  → ALL PASS (the OpenAlex-grammar contract)
```

### 4.3 The end-to-end reality checks (the OpenPatala surface)
```bash
# 1. the registry has the harvested SOURCE objects
python3 -c "import sys;sys.path.insert(0,'pipeline');import object_registry as R;s=R.summary();print(s['SOURCE']['objects'])"
#    → 47,102 (SOURCE)

# 2. the compiled projections reflect the live registry (compute-on-write)
curl -s localhost:8787/openpatala | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['counts']['SOURCE'])"
#    → 47,102  (matches the registry — the site is NOT stale)

# 3. the site renders a real work (0-JS + JSON-LD + canonical)
grep -c 'application/ld+json' /mnt/HC_Volume_106427611/ip-graph/site/works/*.html | head -1  # ≥1

# 4. the crosswalk is live + honest (identity evidence, not correctness)
curl -s "localhost:8787/resolve?title=Tantraloka&author=Abhinavagupta" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['data']['status'], d['data'].get('openalex_id'))"
#    → RESOLVED https://openalex.org/W2974993000  (or honest NOT_FOUND/UNAVAILABLE)

# 5. the open-data release is on R2
#    patala://releases/<date>/works.jsonl + works.parquet + manifest.json
```

### 4.4 The honesty checks (what must NOT be violated)
- **No `verified=true`** on any harvested object — status is `MACHINE_PROPOSED`.
- **No false merge** — reconciliation against a rich canonical set produces POSSIBLE → scholar queue,
  never auto-merged (`FALSE_MERGE_RATE = 0`).
- **External ids are crosswalks** — canonical identity is `PT*` (atlas) / the semantic factory key.
- **The factory contract is intact** — `/works` still returns 254 works; the atlas API tests pass;
  the additive `/openpatala` + `/resolve` paths don't touch the existing contract.

---

## 5. THE KNOWN LIMITS (honest — do NOT overclaim)

1. **The first 2000 work pages are verse-based SOURCE objects** (kalikapurana:v116 etc.); the harvested
   works (muktabodha/GRETIL) come after in the registry. The API + registry serve all 47,102; the
   static page set is bounded at 2000 to stay fast (the rest is API-only).
2. **The reconciliation engine's gold threshold needs a rich canonical set** (title + author). The thin
   bibliography only has id/title; the rich set is ~6 entries. So the ingestion registers the e-texts
   as SOURCE (MACHINE_PROPOSED), and the gold-reconcile + human-adjudication pass is the LATER, separate
   step (data capital).
3. **The Atlas Postgres (`patala-atlas`) is specced, not fully wired** — the API currently serves the
   compiled projections + the legacy adapter. The `PT*` typed identity + `authority_evidence` rows in
   Postgres are the next layer (not this build).
4. **10 pre-existing T1 certificate issues** (missing upstream SOURCE refs) are NOT from this build —
   they were committed before; untouched.

---

## 6. THE FILES (what to touch)

| File | Role |
|---|---|
| `ingestion/run_r2_ingestion.py` | the R2 full-file ingestion runner (GRETIL/SARIT TEI + MUKTABODHA/PANDIT adapters) |
| `ingestion/adapters/muktabodha.py` | the Muktabodha adapter (new this build) |
| `pipeline/build_release_snapshot.py` | the open-data release exporter (JSONL + Parquet → R2) |
| `python/patala_core/atlas/api.py` | the OpenAlex-grammar API + additive `/openpatala` + `/resolve` |
| `/mnt/HC_Volume_106427611/ip-graph/scripts/build-static-site.py` | the projection compiler (registry → artifacts + work pages) |
| `/mnt/HC_Volume_106427611/ip-graph/scripts/rebuild-on-commit.py` | compute-on-write (registry is a tracked input) |

---

*This is the operational reference. Every claim above is reproducible with the given commands. If a
check fails, the surface is stale or broken — don't paper over it (the anti-theatre rule). The two
non-negotiables: never fake `verified=true`, and never let an external ID become canonical identity.*
