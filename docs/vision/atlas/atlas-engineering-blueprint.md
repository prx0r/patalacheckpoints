Yes. The clean answer is: **copy OpenAlex’s product architecture, not its scale architecture**.

OpenAlex is dealing with hundreds of millions of entities and uses Elasticsearch-backed API infrastructure plus bulk S3 snapshots. ([GitHub][1]) Pāṭala will be orders of magnitude smaller for years, so reproducing their ingestion/cluster stack would create operational work without adding scholarly value.

For Pāṭala I would build this:

```text
                        PĀṬALA ATLAS
                           API
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
          PostgreSQL     Search Index    R2 OBJECT STORE
        canonical graph   projection       files/blobs
              │                              │
              │                              ├ manuscripts
              │                              ├ scans
              │                              ├ PDFs
              │                              ├ TEI
              │                              ├ e-text
              │                              ├ OCR/HTR
              │                              └ factory outputs
              │
              ▼
        PĀṬALA FACTORY
              │
      T1/L0/ARGMAP/L2...
              │
              ▼
        EPISTEMIC CORE
              │
              ▼
        PUBLIC SNAPSHOTS
       JSONL + Parquet + RO-Crate
```

The important rule:

> **Postgres stores what things ARE and how they relate. R2 stores the bytes. Search engines store disposable indexes.**

Never let Elasticsearch, R2 filenames, or the filesystem become canonical truth.

---

# 1. Use PostgreSQL as the canonical Atlas database

For your scale, Postgres is almost perfect.

It can comfortably hold:

```text
works
people
editions
manuscripts
institutions
surrogates
transcriptions
etexts
translations
bibliographic records
identifiers
rights
relationships
authority assertions
factory state
```

while keeping typed relational constraints.

And when an imported authority source has messy extra metadata, `jsonb` handles that without forcing you to redesign the schema every time; PostgreSQL supports indexed JSONB querying using GIN indexes. ([PostgreSQL][2])

So don't make:

```text
data/corpus/bibliography/*.json
```

the long-term database.

Make it:

```text
Postgres
= canonical state

JSON/JSONL
= exports, fixtures, snapshots
```

### Core schema

I would start with:

```text
work
person
institution

edition
witness
surrogate
transcription
etext
source

scholarly_work

identifier
name_variant
relationship
rights
authority_evidence

asset
asset_version

source_assertion
```

And **do not create separate tables for every external database**.

Use:

```text
external_identifier

entity_ref
scheme
value
canonical_url
metadata
retrieved_at
```

Examples:

```text
NCC
NGMCP
NMM
GRETIL
SARIT
MUKTABODHA
OCLC
DOI
OPENALEX
ORCID
ROR
IIIF
CTS
ISBN
```

---

# 2. The distinction between entity and asset is critical

This will save you enormous pain.

Consider a manuscript.

```text
MANUSCRIPT
Bodleian MS Sansk. X
```

is an intellectual/physical entity.

Its:

```text
JPEG scans
TIFF masters
PDF
IIIF manifest
OCR
transcription
```

are **assets**.

Likewise:

```text
Tantrāloka
= Work

Kaul 1918
= Edition

GRETIL transcription of Kaul
= EText

tantraloka.txt
= Asset
```

Don't combine them.

Model:

```text
Entity
   │
   └── Asset
         │
         ├── AssetVersion 1
         └── AssetVersion 2
```

---

# 3. Put every file in Cloudflare R2

This is probably the best fit for you right now.

R2 is S3-compatible, strongly consistent, and designed for frequently accessed unstructured data such as datasets and ML artifacts. ([Cloudflare Docs][3])

More importantly for your budget, current R2 Standard pricing is **$0.015/GB-month with no Internet egress fee**, plus a free tier of 10 GB storage and operation allowances. ([Cloudflare Docs][4])

So 500 GB would be roughly:

```text
500 × $0.015
≈ $7.50/month
```

before operation charges.

That is extremely reasonable for this project.

Use:

```text
R2 = blob layer
```

for:

```text
PDFs
TEI XML
plain Sanskrit
JSONL
manuscript images you may legally host
OCR/HTR
translations
audio later
benchmark bundles
release snapshots
```

---

# 4. But don't necessarily mirror every manuscript

This distinction matters.

If Bodleian/OCHS/etc. already exposes a stable IIIF resource:

```text
Pāṭala Witness
      ↓
external IIIF Manifest
```

can be enough.

IIIF Presentation exists specifically to model digitized compound objects such as manuscripts/books through manifests, canvases, and annotations. So use that external identity rather than unnecessarily duplicating institutional master images. ([Text Encoding Initiative][5])

Your storage policy should be:

```text
RIGHTS-CLEARED / OWNED
→ R2 full copy

OPEN INSTITUTIONAL IIIF
→ preserve URI + metadata + checksum where possible
→ optional permitted cache

COPYRIGHTED / RESTRICTED
→ metadata + external locator only

USER/SCHOLAR UPLOAD
→ R2 private until rights resolved
```

So **Atlas completeness does not require file ownership**.

That is important for institutional partnerships.

---

# 5. Make R2 objects content-addressed

Do not use:

```text
tantraloka-final-final2.txt
```

Use the hash of the bytes.

For example:

```text
objects/
  sha256/
    6b/
      6bc178.../
         blob
```

Then database:

```json
{
  "asset_id": "pt:asset:8127",
  "sha256": "6bc178...",
  "storage_key": "objects/sha256/6b/6bc178.../blob",
  "media_type": "text/plain",
  "bytes": 923814
}
```

The logical identity:

```text
pt:etext:tantraloka:gretil
```

can move from:

```text
asset hash A
```

to:

```text
asset hash B
```

via explicit versioning.

The old bytes remain addressable.

This gets you genuine immutable artifact history without requiring a blockchain.

---

# 6. Use sane R2 namespaces as projections, not identity

You can additionally expose human-friendly keys:

```text
atlas/
  works/
    tantraloka/
      editions/
      witnesses/
      etexts/

factory/
  t1/
  l0/
  argmap/
  l2/
  l200/
  c1/

scholarship/
  pdf/
  tei/
  extracted/

manuscripts/
  surrogate/
  htr/
  transcription/

releases/
  2026-08/
```

But these are aliases/presentation organization.

Canonical file identity remains:

```text
sha256
```

---

# 7. Use TEI where it gives you real value

Don't convert every tiny internal object into XML.

But for **textual sources and editions**, TEI is exactly the mature standard you should borrow.

TEI is specifically designed for representing primary-source textual material, and its current critical-apparatus model explicitly represents witnesses, readings, and variant relationships. ([Text Encoding Initiative][5])

So use:

```text
TEI XML

for:
critical edition
transcription
apparatus
manuscript description
text structure
```

Internally your factory can consume normalized JSON.

Architecture:

```text
TEI
 ↓ compile
CanonicalText JSON
 ↓
Pāṭala factory
```

The TEI header is also designed to describe a text's source, encoding and revision history, which fits your provenance requirements extremely well. ([Text Encoding Initiative][6])

---

# 8. Keep factory outputs JSON/JSONL

Do not TEI-encode:

```text
ARGMAP
MachineTranslationProof
Proposition
Argument
Crux
ReviewEvent
```

Those are Pāṭala-native computational objects.

Use:

```text
Pydantic
↓
canonical JSON
```

Store the large immutable payload in R2.

Keep query-critical metadata in Postgres.

For example:

```text
object_version

object_id
version
layer
payload_hash
payload_uri
schema_version
created_at
supersedes
authority...
```

Then:

```text
payload
→ R2

metadata/index
→ Postgres
```

This avoids enormous database rows as you scale.

---

# 9. Initially, Postgres can also do your Atlas search

You do **not** need Elasticsearch tomorrow.

PostgreSQL already provides full-text search and ranked matching primitives. ([PostgreSQL][7])

And `pg_trgm` provides indexed trigram similarity search, which is particularly useful for your reconciliation problem:

```text
Tantraloka
Tantrāloka
Tantralokah
Tantra Loka
```

([PostgreSQL][8])

This gives you a very cheap first implementation:

```text
Postgres

exact identifiers
+
aliases
+
trigram fuzzy title search
+
FTS
```

That's plenty for:

```text
254
1,000
10,000
probably 100,000
```

entities.

---

# 10. Add Elasticsearch/OpenSearch when corpus search becomes serious

OpenAlex's open-source architecture explicitly includes an Elasticsearch-backed API and dedicated Elasticsearch configuration. ([GitHub][1])

That's sensible at their scale.

For you, add a dedicated search system when queries become things like:

```text
find Sanskrit phrase across 50m tokens

vimarśa NEAR svātantrya

all passages where:
school = Krama
date < 1050
lemma = śakti

search title aliases + transliterations

semantic search scholarship
```

Elasticsearch supports explicit mappings, custom text analysis, filters, full-text search, aggregations and vector/semantic search. ([Elastic][9])

But treat Elasticsearch as:

```text
derived index
```

Always rebuildable from:

```text
Postgres + R2
```

Never canonical.

For Sanskrit I would eventually index several parallel representations:

```text
text_devanagari
text_iast
text_slp1
text_normalized
text_lemma
text_sandhi_split
english
```

That will make Pāṭala search unusually good.

---

# 11. This is the OpenAlex pattern you should copy

OpenAlex gives entities stable IDs and exposes singleton/list/filter/search/grouping APIs over them; it also publishes downloadable complete snapshots. ([GitHub][10])

Copy that almost directly.

### Pāṭala API

```text
/api/works
/api/works/{id}

/api/editions
/api/editions/{id}

/api/witnesses
/api/witnesses/{id}

/api/people
/api/institutions

/api/etexts
/api/translations
/api/scholarship

/api/search
```

And support:

```text
filter=
search=
sort=
cursor=
select=
group_by=
```

OpenAlex uses essentially this API grammar today. ([GitHub][10])

That's a very good API design to steal.

---

# 12. Typed IDs should be first class

OpenAlex IDs have a type prefix, e.g. `W` for work and `A` for author. ([GitHub][11])

Do something similar.

For example:

```text
PTW0000129  Work
PTE0000048  Edition
PTM0003127  Manuscript
PTS0009271  Surrogate
PTT0003218  Transcription
PTX0001209  EText
PTP0000872  Person
PTI0000341  Institution
PTR0008129  ReviewEvent
```

Or keep your existing semantic IDs internally:

```text
pt:work:tantraloka
```

Either is fine.

But expose permanent HTTP identifiers:

```text
https://patala.org/W/PTW0000129
```

That should redirect/render forever.

---

# 13. Separate stable identity from version identity

This is essential.

```text
PTW0000129
```

means:

> Tantrāloka.

Never changes.

But:

```text
pt:source:tantraloka:v17
sha256:abc...
```

means an exact frozen textual state.

So external users can cite either:

```text
WORK
"Tantrāloka generally"
```

or:

```text
VERSION
"the exact source Pāṭala used in analysis X"
```

This is one of the things that makes the whole system scholarly rather than merely convenient.

---

# 14. Build an explicit textual-transmission graph

This is where you go beyond OpenAlex.

Relations:

```text
WORK
 ├ HAS_EDITION → EDITION
 ├ HAS_WITNESS → WITNESS
 └ HAS_TRANSLATION → TRANSLATION

EDITION
 ├ BASED_ON → WITNESS
 ├ EDITED_BY → PERSON
 └ DIGITIZED_AS → ETEXT

WITNESS
 ├ HELD_BY → INSTITUTION
 └ REPRESENTED_BY → SURROGATE

SURROGATE
 └ TRANSCRIBED_AS → TRANSCRIPTION

TRANSCRIPTION
 └ SUPPORTS → EDITION / SOURCE

ETEXT
 ├ DERIVED_FROM → EDITION
 └ PROVIDED_BY → PROJECT
```

Then the epistemic graph hangs below.

That is the true **Sanskrit OpenAlex**.

---

# 15. Don't use a graph database yet

This is another place I'd avoid overengineering.

You have maybe:

```text
10k–1m nodes
```

for quite a while.

Postgres:

```text
entity
relationship
```

is enough.

And NetworkX can perform in-memory DAG/graph algorithms for Pāṭala's dependency work.

Do not introduce Neo4j merely because we use the word "graph."

Eventually maybe.

Not now.

---

# 16. Add a data lake from day one—but make it stupidly simple

Every release generate:

```text
snapshots/
  2026-08-14/
    works.parquet
    editions.parquet
    witnesses.parquet
    people.parquet
    relationships.parquet
    etexts.parquet
    translations.parquet
```

into R2.

That's extremely valuable.

Why?

Researchers can download Pāṭala without touching your API.

OpenAlex follows this same API + complete-snapshot model. ([GitHub][12])

Later:

```text
DuckDB
Polars
PyArrow
Spark
```

can query it easily.

---

# 17. R2 is getting particularly interesting for this

Cloudflare now has an R2 Data Catalog built on Apache Iceberg and exposes a standard Iceberg REST catalog; importantly, it is currently public beta. ([Cloudflare Docs][13])

R2 SQL can query data in R2 and currently charges by compressed bytes scanned. ([Cloudflare Docs][14])

So eventually:

```text
R2
├ blobs
└ lakehouse/
    └ Iceberg/Parquet
```

could support:

```sql
SELECT *
FROM patala.works
WHERE tradition = 'Krama';
```

without building a separate analytics warehouse.

But because the Data Catalog is currently beta, I **would not make Pāṭala depend on it**.

Produce standard Parquet now.

Add Iceberg later.

---

# 18. Host the factory beside the object store conceptually, not physically

Your translation agents need quick access.

Don't download a 300 MB manuscript repeatedly.

Give every job:

```json
{
  "source_ref": "...",
  "source_asset": {
    "sha256": "...",
    "uri": "r2://patala/objects/..."
  }
}
```

Worker:

```text
check local cache
   │
   ├ HIT → use local
   │
   └ MISS → fetch R2
```

Then:

```text
~/.cache/patala/sha256/...
```

You get both:

```text
central source of bytes
+
fast local execution
```

Use hashes so cache correctness is deterministic.

---

# 19. Don't route uploads through your Next.js server

For manuscripts especially.

R2 supports S3-compatible direct uploads; Cloudflare explicitly recommends direct uploads/presigned flows for media storage rather than piping the bytes through your application server. ([Cloudflare Docs][15])

Architecture:

```text
browser
  │
  ├── POST /uploads/request
  │
  ▼
Pāṭala API
  │
  └── returns presigned R2 upload
          │
          ▼
browser ─────────────► R2
                        │
                        ▼
                    upload event/job
                        │
                        ▼
                    ingestion pipeline
```

For large objects, R2 supports resumable multipart upload up to multi-terabyte object sizes. ([Cloudflare Docs][16])

That's perfect for manuscript batches.

---

# 20. The ingestion pipeline becomes a first-class system

When anything enters Pāṭala:

```text
UPLOAD / URL / IIIF / GRETIL / SARIT
            ↓
       IngestionJob
            ↓
       FETCH / RECEIVE
            ↓
          HASH
            ↓
      MIME + metadata
            ↓
         RIGHTS
            ↓
        IDENTIFY
            ↓
       RECONCILE
            ↓
   Work / Edition / Witness
            ↓
        EXTRACT
            ↓
 TEI / OCR / transcription / text
            ↓
      SourceCandidate
            ↓
     SOURCE AUTHORITY GATE
            ↓
       factory_ready
```

This should sit **before Agent 2**.

---

# 21. I'd create four R2 buckets

Keep permissions very clear.

### `patala-public`

```text
rights-cleared texts
public TEI
public snapshots
public review bundles
public released translations
```

### `patala-source`

```text
factory source files
e-texts
OCR
transcriptions
source PDFs
```

private by default.

### `patala-manuscripts`

```text
user uploads
scans
TIFF/JPEG
HTR inputs
```

very controlled.

### `patala-artifacts`

```text
T1
L0
ARGMAP
L2
L200
C1
proof
benchmark outputs
```

private until promoted.

That is enough.

Don't create 35 buckets.

---

# 22. Rights metadata belongs in Postgres, bytes belong in R2

Every asset should have something like:

```text
rights_status
license
rights_holder
hosting_allowed
redistribution_allowed
machine_processing_allowed
derivative_allowed
evidence_ref
```

Then the API can deterministically answer:

```text
can user download?
can factory process?
can public API return text?
can snapshot contain bytes?
```

This becomes particularly important if universities give you material under limited agreements.

---

# 23. OpenAlex's downloader has one idea worth copying directly

OpenAlex's official bulk download tooling is explicitly **metadata-first**, with optional PDF/TEI content, resumable checkpointing, async concurrency and S3 storage support. ([GitHub][17])

That's exactly how your acquisition adapters should behave:

```text
metadata first
↓
resolve identity
↓
decide rights/value
↓
THEN fetch expensive bytes
```

Not:

```text
download all of GRETIL + 40 TB of scans
↓
figure it out later
```

Your current tier strategy already points this way.

---

# 24. Your source of truth becomes three things, not one

I would update the earlier statement that "bibliography is the source of truth."

More precisely:

```text
POSTGRES ATLAS
= ENTITY TRUTH
what exists / relationships / authority

R2
= ARTIFACT TRUTH
the exact bytes

EVENT LOG
= HISTORY TRUTH
what changed / who changed it / why
```

Then:

```text
Elasticsearch
Marquez
catalog pages
Next.js caches
Parquet snapshots
```

are all disposable projections.

That separation is extremely important.

---

# 25. Backups

Also boring, also necessary.

For Postgres:

```text
nightly pg_dump
→ R2 backup bucket

+
WAL/PITR later
```

For R2:

content-addressed objects already give you useful immutability semantics, but retain manifests of expected hashes and replicate important releases separately.

For releases:

```text
release manifest
+
hashes
+
schema versions
+
database snapshot
+
Parquet snapshot
```

Later sign that manifest with Sigstore/Rekor.

---

# 26. API: copy OpenAlex aggressively

This part I really would copy conceptually.

OpenAlex exposes:

```text
single entity
lists
filters
search
sorting
cursor pagination
field selection
grouping
```

([GitHub][10])

Do the same.

Example:

```text
GET /works?filter=tradition:krama,date:<1100
GET /witnesses?filter=institution:Bodleian
GET /editions?filter=work:PTW123
GET /works?search=tantraloka
GET /works/PTW123
```

And return dehydrated references rather than nesting the entire universe:

```json
{
  "id": "PTW123",
  "title": "Tantrāloka",
  "authors": [
    {"id":"PTP42","display_name":"Abhinavagupta"}
  ],
  "editions": {
    "count": 4,
    "api_url": "/editions?filter=work:PTW123"
  }
}
```

Very OpenAlex-like.

Very good.

---

# 27. Publish an OpenAPI spec from day one

OpenAlex now publishes a complete OpenAPI 3.1 specification for its API. ([GitHub][10])

Do that.

Then:

```text
OpenAPI
   ├ TypeScript SDK
   ├ Python SDK
   ├ MCP adapter
   └ docs
```

can all derive from the same interface.

This matters because Pāṭala ultimately wants AI agents to consume it heavily.

---

# 28. The "Sanskrit OpenAlex" should expose external IDs aggressively

A work page shouldn't say merely:

```text
Tantrāloka
```

It should aggregate:

```text
Pāṭala ID
NCC refs
NMM refs
NGMCP refs
GRETIL
Muktabodha
SARIT
WorldCat
Google Books
OpenAlex scholarly references
DOIs
IIIF manifests
```

That makes Pāṭala a **resolver**, not another data silo.

This is a huge legitimacy feature.

---

# 29. The eventual data object is incredible

Imagine:

```json
{
  "id": "PTW0001",
  "type": "WORK",
  "title": "Tantrāloka",

  "names": [...],

  "attributed_authors": [...],

  "date": {
    "earliest": 975,
    "latest": 1025,
    "evidence": [...]
  },

  "traditions": ["Trika"],

  "external_ids": {...},

  "editions": [...],

  "witnesses": [...],

  "etexts": [...],

  "translations": [...],

  "scholarship": [...],

  "relationships": [...],

  "source_authority": {...},

  "factory": {
    "source_ready": true,
    "coverage": {...}
  }
}
```

That is already valuable before a single essay is generated.

---

# 30. What I would implement **right now**

Not the full architecture.

### Infrastructure commit 1 — Atlas DB

```text
PostgreSQL
Pydantic schema

Work
Person
Institution
Edition
Witness
Surrogate
EText
ExternalIdentifier
Relationship
Asset
Rights
AuthorityEvidence
```

Migrate the existing 254 bibliography records into it.

Keep JSON export compatibility.

---

### Infrastructure commit 2 — R2 asset store

Create:

```text
patala-public
patala-source
patala-manuscripts
patala-artifacts
```

Build:

```text
put_asset()
get_asset()
verify_asset()
presign_upload()
```

Everything keyed by SHA-256.

---

### Infrastructure commit 3 — Source resolver

```text
resolve_work()
resolve_edition()
resolve_witness()
```

using your Sanskrit authority adapters.

Results become `AuthorityEvidence`, not automatic truth.

---

### Infrastructure commit 4 — API v1

```text
/works
/people
/editions
/witnesses
/etexts
/search
```

with:

```text
filter
search
select
sort
cursor
```

---

### Infrastructure commit 5 — ingestion

```text
external URL / upload / IIIF
→ asset
→ reconcile
→ source candidate
→ factory
```

That's when institutional integration becomes real.

---

### Infrastructure commit 6 — snapshot exporter

Nightly/weekly:

```text
JSONL
Parquet
```

to R2.

Now Pāṭala is an actual **open data infrastructure project**, rather than an API nobody can reproduce.

---

# So: should you copy OpenAlex?

**Copy these:**

```text
stable first-class IDs
heterogeneous entity graph
external-ID crosswalks
API-first product
simple REST grammar
search as a projection
metadata-first ingestion
bulk snapshots
open downloadable dataset
incremental update model
```

OpenAlex describes its own data as a heterogeneous directed graph and exposes API plus complete snapshots as two core access modes. ([GitHub][12])

**Don't copy these yet:**

```text
massive Elasticsearch deployment
their huge ETL architecture
hundreds-of-millions scale assumptions
their entity ontology
their compute infrastructure
```

Your differentiated graph is:

```text
OpenAlex:

Paper
Author
Institution
Citation


Pāṭala:

Work
Edition
Witness
Surrogate
Transcription
EText
Translation
Scholarship
        ↓
Proposition
Argument
Review
```

That's the magic.

And the **storage architecture can be extremely mundane**:

```text
             PostgreSQL
             canonical
                 │
       ┌─────────┼─────────┐
       │         │         │
       ▼         ▼         ▼
      R2       Search    API
     bytes      index    Next.js
       │
       ▼
     Factory
       │
       ▼
 Derived objects
       │
      R2
       │
 metadata → Postgres
```

I would lock that. It can comfortably carry you from the current few hundred records through tens of thousands of works, millions of passages, manuscript imagery, full translations, argument graphs and public API access without requiring a giant distributed-system rewrite.

And critically: **everything interesting Pāṭala owns remains above this boring substrate.**

[1]: https://github.com/ourresearch/OpenAlex?utm_source=chatgpt.com "GitHub - ourresearch/OpenAlex: Index of open source code for OpenAlex---an open, comprehensive catalog of scholarship, connecting papers, authors, institutions, and journals. · GitHub"
[2]: https://www.postgresql.org/docs/current/datatype-json.html?utm_source=chatgpt.com "PostgreSQL: Documentation: 18: 8.14. JSON Types"
[3]: https://developers.cloudflare.com/r2/how-r2-works/?utm_source=chatgpt.com "How R2 works · Cloudflare R2 docs"
[4]: https://developers.cloudflare.com/r2/pricing/?utm_source=chatgpt.com "Pricing · Cloudflare R2 docs"
[5]: https://tei-c.org/guidelines/?utm_source=chatgpt.com "Guidelines"
[6]: https://www.tei-c.org/release/doc/tei-p5-doc/en/html/HD.html?utm_source=chatgpt.com "2 The TEI Header - The TEI Guidelines"
[7]: https://www.postgresql.org/docs/current/datatype-textsearch.html?utm_source=chatgpt.com "PostgreSQL: Documentation: 18: 8.11. Text Search Types"
[8]: https://www.postgresql.org/docs/17/pgtrgm.html?utm_source=chatgpt.com "PostgreSQL: Documentation: 17: F.33. pg_trgm — support for similarity of text using trigram matching"
[9]: https://www.elastic.co/docs/manage-data/data-store/?utm_source=chatgpt.com "The Elasticsearch data store | Elastic Docs"
[10]: https://github.com/ourresearch/openalex-help/blob/main/content/api/introduction.md?utm_source=chatgpt.com "openalex-help/content/api/introduction.md at main · ourresearch/openalex-help · GitHub"
[11]: https://github.com/ourresearch/openalex-docs/blob/main/how-to-use-the-api/get-single-entities/README.md?utm_source=chatgpt.com "openalex-docs/how-to-use-the-api/get-single-entities/README.md at main · ourresearch/openalex-docs · GitHub"
[12]: https://github.com/ourresearch/openalex-docs?utm_source=chatgpt.com "GitHub - ourresearch/openalex-docs: DEAD (GitBook-era, retired). Live docs: github.com/ourresearch/docs -> developers.openalex.org · GitHub"
[13]: https://developers.cloudflare.com/r2/data-catalog/?utm_source=chatgpt.com "R2 Data Catalog · Cloudflare R2 docs"
[14]: https://developers.cloudflare.com/r2-sql/platform/pricing/?utm_source=chatgpt.com "R2 SQL - Pricing · R2 SQL docs"
[15]: https://developers.cloudflare.com/use-cases/media-streaming/store-media/?utm_source=chatgpt.com "Store media at scale · Cloudflare use cases"
[16]: https://developers.cloudflare.com/r2/objects/upload-objects/?utm_source=chatgpt.com "Upload objects · Cloudflare R2 docs"
[17]: https://github.com/ourresearch/openalex-official?utm_source=chatgpt.com "GitHub - ourresearch/openalex-official: Bulk download PDFs and TEI XML files from OpenAlex · GitHub"
