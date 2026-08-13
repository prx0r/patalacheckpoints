# Pāṭala Authority Graph — database schema

*Reference for the Pāṭala Atlas Postgres schema (Alembic migration `0001`, the dedicated `patala-atlas`
Postgres 17). These are the 22 tables of the Authority Graph — the entity/relationship truth. Bytes live
in R2 (content-addressed); history lives in the event log.*

> **Storage truth model:**
> - Postgres = **entity/relationship truth** (what exists, how it relates, authority)
> - R2 = **byte/artifact truth** (content-addressed by SHA-256)
> - Event log = **history truth** (what changed, who, why)
> Everything else (Elasticsearch, catalog pages, snapshots) is a disposable projection.

## Connection (local dev)

```
postgresql+psycopg2://patala:patala_atlas_pw@localhost:5433/patala_atlas
```
Extensions: `pg_trgm` (fuzzy title reconciliation) · `unaccent` · `pgcrypto`. Migrations via Alembic:
`.venv-atlas/bin/alembic upgrade head`. In production: Neon Postgres 17 + Cloudflare Hyperdrive.

## The 22 tables

### Entities
| Table | Key fields | Notes |
|---|---|---|
| `work` | id, canonical_title, title_normalized, work_type, language[], tradition[], date_min/max, date_note | author/edition/source are **relations**, not columns |
| `person` | id, canonical_name, name_normalized | |
| `institution` | id, canonical_name, name_normalized | |
| `edition` | id, work_id→work, title, edition_type, publication_year, publisher, series, volume, authority_state | editors in `edition_contributor` (not comma names) |
| `witness` | id, work_id, institution_id, shelfmark, material, script, language[], date_min/max, folio_count, authority_state | a physical manuscript |
| `surrogate` | id, witness_id→witness, surrogate_type, iiif_manifest, external_url, rights_id, authority_state | digital representation of a witness |
| `etext` | id, work_id, edition_id, provider, provider_record, transcription_method, authority_state, current_asset_version | machine-readable textual representation |
| `source` | id, work_id, etext_id, version, payload_hash | the exact textual basis the factory chose |
| `scholarly_work` | id, work_id, title, authority_state, created_at | modern scholarship about a work |

### Rights & assets
| Table | Key fields | Notes |
|---|---|---|
| `rights` | id, rights_status, license, rights_holder, hosting/redistribution/machine_processing/derivative_allowed, evidence_ref | per-asset policy → `evaluate_rights(asset, action, actor)` |
| `asset` | id, entity_type, entity_id, role | logical asset |
| `asset_version` | id, asset_id→asset, sha256 UNIQUE, media_type, byte_size, r2_bucket, r2_key, external_url | **bytes**; content-addressed |

### Identifiers, names, relations, authority
| Table | Key fields | Notes |
|---|---|---|
| `external_identifier` | id, entity_type, entity_id, scheme, value, url, retrieved_at, raw_metadata JSONB, UNIQUE(scheme,value) | schemes: NCC/NMM/NGMCP/GRETIL/SARIT/MUKTABODHA/IIIF/OCLC/ISBN/DOI/OPENALEX/ORCID/ROR/CTS |
| `name_variant` | id, entity_type, entity_id, variant, normalized | aliases for reconciliation |
| `relationship` | id, source_type, source_id, relation, target_type, target_id, confidence, evidence | typed edges |
| `authority_evidence` | id, subject_type, subject_id, dimension, source_scheme, source_record, relation, evidence_payload JSONB, asserted_at, reviewer_ref | **per-dimension**, never one `verified=true` |

Dimensions: `WORK_IDENTITY · AUTHORSHIP · DATE · EDITION_IDENTITY · WITNESS_IDENTITY · TEXT_DERIVATION · RIGHTS`

### Passages & scholarly objects
| Table | Key fields | Notes |
|---|---|---|
| `passage` | id, work_id, parent_passage_id, ordinal, canonical_locator | stable segments |
| `passage_version` | id, passage_id, source_version_id, text_original, text_normalized, content_hash, schema_version | original + exact offsets are canonical; derived forms rebuildable |
| `scholarly_object` | object_id, object_type | Proposition / Argument / … |
| `scholarly_object_version` | version_id, object_id, schema_name, schema_version, payload_jsonb, payload_hash, created_at | every payload validated against its typed Pydantic schema |
| `object_dependency` | consumer_version_id, dependency_version_id, relation, load_bearing, epistemic_role, PK(all three) | **one of the most important tables** — drives `ImpactReport` / staleness |

## Authority state (source identity)

A domain-specific ladder for **source identity**, separate from epistemic review:

```
DISCOVERED → CATALOG_MATCHED → MULTI_SOURCE_MATCHED → COPY_INSPECTED
→ EDITION_VERIFIED → TEXT_DERIVATION_VERIFIED → SCHOLAR_CONFIRMED
```
Do NOT reuse this ladder for propositions — different object types need different state machines.

## Round-trip example

```sql
INSERT INTO work (id, canonical_title, title_normalized, work_type, tradition, created_at, updated_at)
VALUES (gen_random_uuid(), 'Tantrāloka', 'tantraloka', 'work', ARRAY['Trika'], now(), now());

INSERT INTO authority_evidence (id, subject_type, subject_id, dimension, source_scheme,
                                relation, evidence_payload, asserted_at)
VALUES (gen_random_uuid(), 'work',
        (SELECT id FROM work WHERE title_normalized='tantraloka'),
        'WORK_IDENTITY', 'GRETIL', 'CATALOG_MATCHED', '{"record":"gretilbk"}', now());
```
