# PĀṬALA PROCESS — THE END-TO-END REFERENCE (Ingestion → Atlas → Factory)

*This is the canonical "how it all links" guide. It is the fixed reference for the permanent
infrastructure — the thing to read BEFORE writing any code, so you don't rebuild what exists.
If a piece is listed here as REUSABLE, extend it; do not redefine it.*

**Read order:** this index → `docs/process/01-ingestion.md` → `docs/process/02-atlas.md` →
`docs/process/03-factory.md` → `docs/process/04-r2-storage.md` → `docs/process/05-app-api-sites.md`.
Each is self-contained and links to the others.

---

## THE ONE PICTURE

```
                    EXTERNAL SOURCES (the many, the cheap)
   PANDiT · GRETIL · SARIT · MUKTABODHA · OpenAlex · Crossref · Gyan Bharatam (future)
                                   │
                                   ▼   (ingestion/ — Bronze snapshots)
                    ┌─────────────────────────────┐
                    │        INGESTION BUS        │
                    │  adapter → ExternalRecords  │
                    │  SourceAsserter → reconcile │
                    └─────────────────────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                    ▼
        R2 (immutable       Postgres Atlas        bibliography
        Bronze/Silver)      (the canonical        (thin contract)
        content-addressed   22-table graph)       id/title/status
                                   │
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                    ▼
       object_registry       factory_scheduler     verify_editions
       versioned JSONL       DAG-driven workers    attestations →
       + event ledger        SOURCE→T1→L0→…→C1     translation_status
                                   │
                                   ▼
                          THEMES → ARGUMENT → SYNTHESIS
                                   ▼
                       ESSAY · EDUCATION · REVIEW (projections)
                                   ▼
                   SITES / APIs (both read the same canonical truth)
```

## THE ONE RULE (why this stops duplication)

> **There is one canonical graph. Everything else is a projection.**
> Postgres stores what things ARE. R2 stores the bytes. The event ledger stores history.
> External IDs are crosswalks (`external_identifier`), NEVER canonical identity.
> Imported facts are `authority_evidence`/assertions, NEVER canonical fields.
> The two sites + all APIs consume the SAME canonical truth — never two databases.

## THE REUSABLE INVENTORY (do not rebuild — extend)

| Concern | Reusable entry point | Type |
|---|---|---|
| Ingestion contract | `source-evidence/schema/external_record.py` — `ExternalRecord`, `ReconciliationAdapter` | library |
| Identity resolver | `source-evidence/evals/patala/tasks/entity_reconciliation.py` — `reconcile()` | library |
| Text fingerprints | `source-evidence/schema/text_fingerprint.py` | library |
| **Intake engine** | `ingestion/asserter.py` — `SourceAsserter` | library |
| **Postgres writer** | `ingestion/persistence.py` — `AtlasWriter` | library |
| **R2 snapshot store** | `ingestion/r2.py` — `SnapshotStore` | library |
| **Concrete adapters** | `ingestion/adapters/pandit.py`, `gretil.py` | library |
| Bibliography (thin) | `python/patala_core/atlas/adapter.py` — `AtlasAdapter`, `load_bibliography` | library |
| Atlas read API | `python/patala_core/atlas/api.py` — FastAPI service | service |
| Atlas resolver | `python/patala_core/atlas/resolver.py` — `resolve_work`, `persist_evidence` | library |
| Rich→Postgres | `pipeline/atlas_persist_rich.py` — `persist()` | library |
| Postgres schema | `migrations/versions/0001_authority_graph_schema.py` (22 tables) | migration |
| Versioned registry | `pipeline/object_registry.py` — `commit`, `commit_batch`, `append_event` | library |
| State machine | `pipeline/corpus_state.py` — `next_valid_action`, `discover_works` | library |
| Translation queue | `pipeline/translation_targets.py` | library |
| Factory scheduler | `pipeline/factory_scheduler.py` — `scheduler_pass` | library |
| Canonical DAG | `contracts/CANONICAL-DAG.yaml` → `object_registry.PREREQS` | config |
| Attestation engine | `pipeline/verify_editions.py` — `verify_work` | library (wire its output!) |
| R2 bytes | `infra/r2_assets.py` | library |

## KNOWN GAPS / WIRING TO-DO (so nobody "discovers" them again)

*Source: `endgamebuild/PROJECT-AUDIT.md` (2026-08-13) + this session. Status of the audit's "FIXED"
items was re-verified against the live Postgres on 2026-08-14: edition=3, etext=8, scholarly_work=6,
relationship=9 (the rich scholarship graph IS persisted; the audit §4 "never written" line is stale).*

### Infra / ingestion (this stack)
1. **`verify_editions` output is dead** — `verification-registry.jsonl` written but not consumed. Wire it into the bibliography's `translation_status`/`verified`.
2. **`translation_status`/`verified` in the thin bibliography not consumed by the factory** — `corpus_state` uses a `.ts` regex, not the thin JSON.
3. **R2 is not a downstream input** — intake/queue read local disk only; `SnapshotStore` is ready to change that.
4. **`source_assertion`/`corroboration_event` tables have no write path** — scholarship is JSON-only.
5. **No ORM layer** over Postgres (raw psycopg2) — optional.
6. **PANDiT** needs a manual CSV export (Cloudflare-blocked, no API); once dropped on disk it flows through the same `SourceAsserter`.

### App / API / MCP (not in the layer guides — see audit §5)
7. **IPVV passage-ID mismatch (top priority)** — published store uses `pt:passage:ipvv:chunkA-…md`; jsonl corpus uses `tantra:text:…:V2-A:<slug>`. So `/resolve`, `/context/passages/:id`, `/passages/:id` **404** against the richest IPVV data.
8. **`translation_status` vs `translationStatus`** casing inconsistency across works/texts routes.
9. **1 dangling atlas relation** (`nitya_shodasikarnava → yoginīhṛdaya`) + `passages: null` dead key in recovery-gold.
10. **Factory intake state fragmented** across 4 sivaqueue manifests / 3 sources of truth for "on disk".

### ML / research (audit §2)
11. `test_evidence_aware_essay.py` + `test_vertical.py` FAIL (stale-test drift; `/tmp/l0proof` ephemeral).
12. Hard-coded paths: `c1corpus.py:52`, `vertical.py:34,38`, `extract.py`, `concordance/route.ts`, `reingest_grobid.py`.
13. `pushing.py` — real engine, no unit tests.

### Source-evidence / external-tools (audit §3)
14. `scholar_document.py:164` `GrobidAdapter.parse()` is a placeholder (two GROBID classes).
15. `opencitations.py` `_same_author()` hard-wired UNKNOWN.
16. **26 tools documented, only 6 integrated** (grobid, docling, crossref, openalex, opencitations, inspect); 20 docs-only.

### Factory (audit §1)
17. **ARGUMENT / SYNTHESIS have NO real worker** — DAG ends at C1; `autonomy.LAYER_HANDLERS` falls back to a stub.
18. **THEME/ESSAY/EDUCATION not reachable via live `factory_loop.sh`** (runs only T1..C1) — needs a deliberate production rewire.
19. **Live-registry integrity debt:** `factory_certificate` reports 789 bad hashes, 119 conflicts, 19 duplicates (live-data debt, not a cert-logic bug).
20. **L1/L1L2 duplication** — two competing providers, bare L1 not in DAG.

### Owner decisions (audit §Open)
- Repo history rewrite (in-copyright PDFs — destructive filter-repo, deferred).
- Modern-paper external adapters ~0% coverage for Sanskrit (don't invest further).

---

*This is the fixed reference. Read the layer guides next:*
- `01-ingestion.md` — intake / reconciliation / persistence
- `02-atlas.md` — the canonical graph + Postgres + read API
- `03-factory.md` — the DAG, registry, ledger, scheduler
- `04-r2-storage.md` — the immutable data lake + the Bronze snapshot flow
- `05-app-api-sites.md` — the read surfaces (app, APIs, MCP, both sites)

> **Note:** the ML/research lane (Agent 1: arguments, cruxes, synthesis, essay, education — the
> `machinelearning/research/patala_ml/` engines) is NOT covered in these process guides. It is the
> epistemic upper layer; see `docs/vision/essayguide.md`, `docs/process`-adjacent
> `endgamebuild/INFRA-INVENTORY.md` §3, and `handover/agent-1-ml/` for that lane.
