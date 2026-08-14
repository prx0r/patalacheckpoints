# PĀṬALA INGESTION / REFINERY SYSTEM

*Advisory (2026-08-14, imported from the `sanskritree` R2 bucket). Stop "populating Atlas" by hand and
build a general ingestion/refinery bus: ingest PANDiT today, GRETIL tomorrow, 500,000 Gyan Bharatam
records later, future Greek datasets — without changing the underlying pipeline. The full flow:
sources → connector layer → Bronze/R2 (exact bytes) → normalization (Silver/Parquet) → resolver →
(EXACT/POSSIBLE/CONFLICT/UNRESOLVED) → scholar queue → Pāṭala Gold graph → reviewed → projections.*

---

Yes. This is the point where I would stop thinking in terms of “populate Atlas” and build a **general ingestion/refinery system**.

The architecture should let you ingest PANDiT today, GRETIL tomorrow, 500,000 Gyan Bharatam records later, and eventually Greek datasets **without changing the underlying pipeline**.

The core idea is:

```text
SOURCE SYSTEMS
PANDiT · GRETIL · SARIT · NGMCP · Muktabodha
OpenAlex · Crossref · Gyan Bharatam · future Greek data
                         │
                         ▼
                PĀṬALA INGESTION BUS
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
      RAW             NORMALIZED       RESOLVED
   immutable          source records     entities
        │                │                │
        └────────────────┼────────────────┘
                         ▼
                SCHOLARLY GRAPH
                         │
                         ▼
         REVIEW / ARGUMENT / EDUCATION
```

And **R2 is important, but R2 should not be your database.**

---

# 1. Use R2 as the immutable data lake

R2 is where I would put everything that is fundamentally a **file, snapshot, export, corpus, scan, XML document or immutable run artifact**.

Something like:

```text
r2://patala-source-data/

pandit/
  snapshots/
    2026-08-14/
      works.csv
      persons.csv
      manuscripts.csv
      prints.csv
      institutions.csv
      manifest.json

gretil/
  snapshots/
    <git-commit-sha>/
      corpus/
      manifest.json

sarit/
  snapshots/
    <git-commit-sha>/
      *.xml
      manifest.json

openalex/
  subsets/
    2026-08-14/
      sanskrit-related.parquet

gyan-bharatam/
  snapshots/
    2027-??-??/
      batch-000001.parquet
      batch-000002.parquet
      ...

runs/
  reconciliation/
  extraction/
  benchmarks/
```

**Never mutate these.**

If PANDiT changes tomorrow:

```text
pandit/2026-08-14/
pandit/2026-09-01/
```

Both survive.

That gives you reproducibility.

---

# 2. Put a manifest beside every ingestion

Every source acquisition should generate:

```json
{
  "source": "PANDIT",
  "snapshot_id": "pandit-2026-08-14",
  "retrieved_at": "...",
  "upstream_version": "...",
  "license": "CC-BY-NC-SA-4.0",
  "adapter_version": "pandit-v1.2",
  "files": [
    {
      "path": "works.csv",
      "sha256": "...",
      "bytes": 3829182
    }
  ]
}
```

Then everything downstream can answer:

> Where did this record come from?

That's hugely important.

---

# 3. PANDiT: don't use an API unless they give us one

This was an important result from the search.

I found **no documented public REST API** that I would currently architect around.

But PANDiT explicitly says all its data is downloadable, its search UI exposes **Download CSV**, and the current general search contains roughly **69,580 entities**. Their own description says the database contains tens of thousands of entities and hundreds of thousands of relationships. ([Pandit Project][1])

PANDiT currently models:

* State
* Site
* Institution
* Work
* Person
* Collection
* Manuscript
* Extract
* Print
* Project

plus Discipline, Genre, Language and Social Identifier categories. ([Pandit Project][2])

That's a gift.

### First step

Get:

```text
PANDiT model
+
all downloadable CSV exports
```

into R2.

I'd also contact them and say:

> We're building a provenance-aware scholarly graph extending PANDiT-style entities down to passages, interpretations and arguments. Is there a preferred bulk export/database dump rather than repeatedly using CSV exports?

Their project already has experience doing exactly these migrations: they previously imported SKSEC and Karl Potter's huge *Bibliography of Indian Philosophies*, and later BORI Vedānta catalogue records. ([Pandit Project][3])

So they'll understand what you're asking.

---

# 4. But don't make PANDiT your canonical database

Do:

```text
RAW PANDIT

pandit:work:91821
       ↓
ExternalRecord
       ↓
CandidateMatch
       ↓
PATA-W-002918
```

not:

```text
PATA ID = PANDIT ID
```

Your object might look like:

```json
{
  "id": "PATA-W-002918",
  "type": "WORK",
  "external_ids": [
    {
      "scheme": "PANDIT",
      "value": "91821"
    }
  ]
}
```

Then if later:

```text
PANDiT Work 91821
and
Gyan Bharatam Work GB1234
```

refer to the same intellectual work:

```text
             PATA-W-002918
              /         \
             /           \
PANDIT:91821             GB:1234
```

That's Pāṭala's job.

---

# 5. Import PANDiT relationships as assertions

This matters enormously.

Suppose PANDiT says:

```text
Person 128
AUTHORED
Work 91821
```

Don't turn that into an unqualified canonical field.

Import:

```text
Assertion PA-82819

subject:
PATA-P-00128

predicate:
AUTHORED

object:
PATA-W-002918

source:
PANDIT

source_record:
pandit:91821

review_state:
IMPORTED

license:
CC-BY-NC-SA-4.0
```

Later:

```text
Scholar X
says attribution doubtful
```

No database corruption.

You simply gain another assertion.

This is where the architecture you've already built for arguments/general provenance pays off massively.

---

# 6. One VERY important PANDiT issue: licensing

PANDiT explicitly licenses its data **CC BY-NC-SA 4.0**. ([Pandit Project][4])

So don't casually merge the entire PANDiT dataset into a proprietary commercial database and assume everything is fine.

I would create a **license firewall** from day one:

```text
ExternalRecord
    source
    license
    attribution
    commercial_use
    redistribution
    share_alike
```

For example:

```text
PANDIT
CC-BY-NC-SA

GRETIL
per-file license

SARIT
per-file/collection CC license

CROSSREF
metadata

OPENALEX
open metadata

PARTNER DATA
contract-specific
```

Before monetizing PANDiT-derived datasets directly, get clarification/permission or proper legal advice.

Much cleaner strategically: **partner with PANDiT**.

---

# 7. GRETIL then becomes stupidly easy

Current stable mirror:

[https://github.com/INDOLOGY/GRETIL-mirror](https://github.com/INDOLOGY/GRETIL-mirror)

GRETIL now has stable GitHub/TextGrid snapshots, and most material in the mirror is Unicode with TEI versions available for nearly everything except some noted exceptions. ([GitHub][5])

Your connector does:

```text
git fetch
   ↓
record commit SHA
   ↓
copy snapshot/archive → R2
   ↓
parse TEI
```

For every GRETIL file extract:

```text
title
author
editor
source edition
data entry
contributor
date
language
license
bibliographic citation
file path
git commit
hash
```

GRETIL TEI headers already contain useful source information. Individual records can, for example, identify the edition from which the electronic text derives and the license attached to that electronic text. ([Gretl][6])

So:

```text
GRETIL XML
     │
     ├── metadata
     │
     └── Sanskrit content
             │
             ▼
         TextInstance
             │
          based_on?
             ▼
           Edition
             │
             ▼
            Work
```

---

# 8. Critical distinction: GRETIL file ≠ Work

Suppose:

```text
gretil/sa_tantraloka.xml
```

You create:

```text
TextInstance TI-8291
```

Then resolve it against:

```text
PATA-W-TANTRALOKA
```

The source edition might create:

```text
Edition ED-991
```

So:

```text
Tantrāloka
WORK

      ↓ realized in

Edition X

      ↓ digitized as

GRETIL TextInstance

      ↓ segmented into

Passages
```

That's much more correct than the current common corpus model.

---

# 9. SARIT plugs into exactly the same pipeline

Repository:

[https://github.com/sarit/SARIT-corpus](https://github.com/sarit/SARIT-corpus)

SARIT is even cleaner because the corpus is explicitly TEI P5 and its files encode scholarly information about authors, references, edition pages and other textual relationships. ([GitHub][7])

So the same generic ingestion contract:

```python
SourceAdapter:

    discover()
    snapshot()
    parse()
    emit_records()
    emit_relations()
    emit_assets()
```

can have:

```text
PanditAdapter
GretilAdapter
SaritAdapter
OpenAlexAdapter
CrossrefAdapter
GyanBharatamAdapter
```

That's the real infrastructure.

---

# 10. Then automatically populate bibliography

This is where it gets really good.

You don't manually type bibliography entries.

You create a **bibliographic resolution pipeline**.

Start from every:

```text
PANDiT Print
GRETIL source citation
SARIT bibliography
existing Pāṭala resource
```

Extract:

```text
title
author/editor
year
journal
volume
pages
publisher
ISBN
DOI if present
```

Then:

```text
citation
   ↓
DOI present?
   │
 YES ───────────────→ Crossref lookup
   │
 NO
   ↓
Crossref title search
   ↓
OpenAlex search
   ↓
candidate publications
   ↓
score candidate
```

Crossref's public API requires no signup and returns publisher-deposited bibliographic metadata, including identifiers such as ORCID and ROR when present. ([CrossRef][8])

OpenAlex gives:

```text
works
authors
sources
institutions
topics
citations
references
OA locations
```

with a free API key and $1/day free API usage; exact singleton lookups are currently free. ([OpenAlex][9])

---

# 11. The bibliography becomes another reconciliation graph

For example GRETIL header:

```text
Source:
Torella 1994 ...
```

Pāṭala does:

```text
raw citation
     ↓
candidate bibliography record
     ↓
Crossref
     ↓
OpenAlex
     ↓
PATA-PUB-892
```

Now:

```text
PATA-PUB-892

external IDs:
 DOI
 OpenAlex
 PANDiT Print

authors:
 PATA-PERSON-X

discusses:
 PATA-WORK-IPK
```

Beautiful.

---

# 12. How to find translations automatically

Create a separate **translation discovery worker**.

For every Work:

```text
canonical title:
Īśvarapratyabhijñā

aliases:
Īśvarapratyabhijñākārikā
Isvarapratyabhijnakarika
IPK
...
```

Generate searches such as:

```text
"title"
"title" translation
"title" English
"author" "title"
"title" edition translation
```

against:

```text
PANDiT Print records
OpenAlex
Crossref
existing bibliography
library/open repositories
```

Then classify candidates:

```text
EDITION
FULL_TRANSLATION
PARTIAL_TRANSLATION
STUDY
COMMENTARY
REVIEW
DISSERTATION
UNKNOWN
```

**Never let search results directly become canonical.**

They enter:

```text
CandidateResource
```

Then automatic verification:

```text
DOI match
ISBN match
author match
title similarity
year
bibliographic references
```

High confidence → accepted as bibliographic identity.

Whether it's actually a *complete translation* may still require inspection/review.

---

# 13. OpenAlex: don't download 330 GB yet

You technically can.

Their current free snapshot is roughly **330 GB compressed / ~1.6 TB decompressed** and updated quarterly. ([OpenAlex][10])

Don't do that right now.

Your problem is:

```text
~Sanskrit/Indic scholarship
```

not:

```text
every scientific publication on Earth
```

Use their REST API or official filtered CLI initially. OpenAlex itself recommends the API for normal applications and bulk downloads for large-scale/local-analysis use cases. ([OpenAlex][11])

Cache every resolved record in Pāṭala.

So:

```text
OpenAlex API
     ↓
source cache in R2
     ↓
normalized Publication
```

---

# 14. The real storage architecture

I would use **four storage layers**, not one.

### R2 — immutable objects

```text
raw CSV
XML
TEI
JSON snapshots
PDFs where allowed
scans where allowed
Parquet batches
benchmark runs
export files
```

### Relational DB — canonical graph

Initially your existing relational stack can handle:

```text
entities
external_ids
external_records
assertions
relations
works
people
manuscripts
editions
publications
reviews
matches
```

If you're eventually dealing with tens/hundreds of millions of relationships, I'd expect moving the heavy canonical/query layer to PostgreSQL-class infrastructure rather than trying to treat object storage as a database.

### Search index

For:

```text
titles
aliases
Sanskrit strings
incipits
full text
bibliography
```

### Vector/fingerprint index

For:

```text
candidate manuscript matching
parallel passages
similarity retrieval
```

Don't shove everything into one product because it's convenient today.

---

# 15. Store normalized bulk data as Parquet in R2

This becomes incredibly important once Gyan Bharatam-scale data arrives.

Raw:

```text
source CSV/XML/JSON
```

then transform to:

```text
Parquet
```

partitioned:

```text
normalized/
  source=gyan_bharatam/
    entity_type=manuscript/
      year=2027/
        batch-000001.parquet
```

Parquet gives you cheap columnar bulk processing.

Then tools like DuckDB/Spark/etc. can crunch millions of records **without loading your production database**.

---

# 16. Think Bronze → Silver → Gold → Reviewed

I would literally encode these states.

### BRONZE

Exact upstream bytes.

```text
PANDiT CSV
GRETIL XML
GB JSON
```

Never altered.

### SILVER

Normalized source objects.

```text
title_raw
title_normalized
author_raw
source_identifier
language
script
```

Still explicitly source-bound.

### GOLD

Canonical Pāṭala graph.

```text
PATA-W-001
PATA-P-991
PATA-MS-218
```

### REVIEWED

Scholar-reviewed assertions.

```text
authorship adjudicated
work identity reviewed
recension reviewed
argument reviewed
```

That gives you:

```text
RAW REALITY
   ↓
NORMALIZATION
   ↓
ENTITY RESOLUTION
   ↓
SCHOLARLY KNOWLEDGE
```

---

# 17. Every connector implements the same interface

This is the piece I'd actually build next.

```text
Connector

source_id

discover()
fetch()
snapshot()
parse()
normalize()
emit_entities()
emit_assertions()
emit_assets()
emit_bibliography()
checkpoint()
```

And every connector outputs generic envelopes:

```json
{
  "source": "GRETIL",
  "source_record_id": "...",
  "record_type": "TEXT_INSTANCE",
  "payload": {},
  "provenance": {},
  "rights": {}
}
```

Then Pāṭala doesn't care whether the source was:

```text
8,000 PANDiT manuscripts
500 GRETIL texts
60 SARIT editions
11,000,000 GB manuscript records
```

The ingestion engine sees:

```text
ExternalRecord[]
```

That's the abstraction that saves you later.

---

# 18. Gyan Bharatam then becomes another connector

Their published plan explicitly anticipates APIs for integration with national and international manuscript archives. ([Ministry of Culture][12])

When they finally publish:

```text
GET /manuscripts
```

we write:

```text
GyanBharatamConnector
```

which outputs exactly the same `ExternalRecord` envelopes.

Pipeline:

```text
GB
│
├── batch 1: 100k
├── batch 2: 100k
├── batch 3: 100k
│
▼
R2 RAW

        ↓

Parquet normalization

        ↓

Candidate generation

        ↓

Pāṭala resolver

        ↓

EXACT
PROBABLE
POSSIBLE
CONFLICT
UNRESOLVED

        ↓

canonical entities

        ↓

scholar queues
```

No architecture rewrite.

---

# 19. Make ingestion idempotent

Critical at millions of records.

Running:

```text
ingest pandit --snapshot 2026-08-14
```

twice should not create duplicate objects.

Every source record gets:

```text
source
external_id
version/hash
```

unique constraint.

Then:

```text
same hash
→ NOOP

new hash
→ new version

new external ID
→ new record
```

You already care about reproducibility elsewhere in Pāṭala. Apply it here too.

---

# 20. Entity matching should be its own service

Don't bury matching inside each importer.

All connectors feed:

```text
RESOLVER
```

which knows how to resolve:

```text
WORK
PERSON
MANUSCRIPT
PUBLICATION
INSTITUTION
PLACE
```

Different entity types use different evidence.

Work:

```text
title
aliases
author
incipit
explicit
language
genre
related works
```

Manuscript:

```text
repository
shelfmark
collection
dimensions
folio count
catalogue references
```

Publication:

```text
DOI
ISBN
title
author
year
pages
```

Person:

```text
name aliases
dates
teachers
students
works
places
```

This becomes a major piece of Pāṭala IP.

---

# 21. Never auto-merge ambiguous records

At scale, the dangerous error isn't:

> couldn't match this.

It's:

> incorrectly merged two distinct works.

So resolver:

```text
score > 0.995 + deterministic ID match
→ EXACT

strong evidence
→ PROBABLE

some evidence
→ POSSIBLE

contradictory evidence
→ CONFLICT

otherwise
→ UNRESOLVED
```

Only safe classes auto-resolve.

Everything else queues.

---

# 22. Scholars work the uncertainty frontier

Now your scholar UI becomes incredibly clean.

Not:

> Add stuff to Pāṭala.

Instead:

```text
REVIEW QUEUE

Potential duplicate works        18
Authorship conflicts              7
Possible new manuscript witnesses 4
Unknown texts                    11
Translation classification        9
```

Click one:

```text
PANDiT:
Tantrasadbhāva

GRETIL:
Tantrasadbhāvatantra

GB manuscript:
Śrītantrasadbhāvam

Machine:
PROBABLE SAME WORK — .94

Evidence:
title
incipit
author/tradition
parallel passages

[ SAME WORK ]
[ DISTINCT ]
[ UNSURE ]
```

A scholar resolves it.

That judgment becomes permanent data capital.

---

# 23. And return corrections upstream

This is essential for becoming part of the ecosystem rather than merely ingesting everyone.

For PANDiT:

```text
Pāṭala discovers probable duplicate
      ↓
scholar confirms
      ↓
export contribution/correction
      ↓
send back to PANDiT
```

For GRETIL:

```text
text mapped to correct edition
      ↓
link/correction contribution
```

For Gyan Bharatam:

```text
GB manuscript
      ↓
Pāṭala identifies Work
      ↓
reviewed enrichment
      ↓
return API/export
```

That's how partners start regarding Pāṭala as useful infrastructure.

---

# 24. One more major advantage: PANDiT already believes in this model

Their collaboration page literally argues that independent niche databases are less useful than connecting data into a broad framework, credits individual contributors, retains revisions, and says all data can be downloaded. ([Pandit Project][4])

That means culturally PANDiT is probably one of the most natural early collaborators imaginable.

The pitch isn't:

> I'm building a rival PANDiT.

It's:

> **I want Pāṭala to use PANDiT identity/model compatibility and contribute corrections/crosslinks back, while extending down into texts, passages, evidence and arguments.**

That's actually complementary.

---

# The full Pāṭala flow

This is what I would freeze conceptually:

```text
                    SOURCES

 PANDiT     GRETIL     SARIT      GB
    │          │          │        │
 OpenAlex   Crossref    NGMCP     etc
    │          │          │        │
    └──────────┴──────────┴────────┘
                       │
                       ▼
                CONNECTOR LAYER
                       │
                       ▼
                ┌─────────────┐
                │ BRONZE / R2 │
                │ exact bytes │
                └──────┬──────┘
                       │
                       ▼
              NORMALIZATION ENGINE
                       │
                       ▼
                ┌─────────────┐
                │ SILVER / R2 │
                │   Parquet   │
                └──────┬──────┘
                       │
                       ▼
                  RESOLVER
                       │
        ┌──────────────┼──────────────┐
        │              │              │
      EXACT         POSSIBLE       CONFLICT
        │              │              │
        │              └──────┬───────┘
        │                     ↓
        │                SCHOLAR QUEUE
        │                     │
        └────────────┬────────┘
                     ▼
                PĀṬALA GRAPH
                   GOLD
                     │
      ┌──────────────┼──────────────┐
      ↓              ↓              ↓
    WORKS       MANUSCRIPTS      PEOPLE
      │              │              │
   EDITIONS      WITNESSES      AUTHORS
      │                             │
   PASSAGES                    PUBLICATIONS
      │
   TRANSLATIONS
      │
    CLAIMS
      │
   ARGUMENTS
      │
    REVIEWS
      │
  ADJUDICATION
      │
      ▼
               REVIEWED PĀṬALA
                     │
      ┌──────────────┼─────────────┐
      ↓              ↓             ↓
  PUBLIC ATLAS   SCHOLAR LAB   PARTNER API
      │              │             │
      ↓              ↓             ↓
 Search/AI       full access   institutions
```

## If I were directing the next engineering sprint

I would **pause mass manual Atlas population** and build these six things first:

1. `ExternalRecord + ExternalIdentifier + SourceSnapshot + Rights` primitives.
2. Generic `Connector` interface.
3. R2 Bronze/Silver snapshot convention + manifests.
4. PANDiT connector and model crosswalk.
5. GRETIL connector extracting Work/TextInstance/Edition/bibliography candidates.
6. Generic entity resolver + reconciliation queue.

Then add:

```text
SARIT
Crossref
OpenAlex
```

Once those six work together, **Atlas can populate itself from existing scholarship rather than you manually constructing civilization one node at a time.**

And *that* is the infrastructure that makes the 11.9-million-manuscript possibility tractable: not because we can ingest eleven million JSON rows—that's easy—but because every row enters a reproducible system capable of turning **raw external records → candidate identities → resolved knowledge → expert judgment**.

[1]: https://panditproject.org/search?utm_source=chatgpt.com "Search | Pandit"
[2]: https://panditproject.org/info/types?utm_source=chatgpt.com "Entity types | Pandit"
[3]: https://panditproject.org/entity/131/info?utm_source=chatgpt.com "The project | Pandit"
[4]: https://panditproject.org/entity/132/info "Collaboration | Pandit"
[5]: https://github.com/INDOLOGY/GRETIL-mirror?utm_source=chatgpt.com "GitHub - INDOLOGY/GRETIL-mirror: Snapshots of the GRETIL repository of South Asian (Sanskrit, Pali, etc.) etexts · GitHub"
[6]: https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_dIpaMkarazrIjJAna-gurukriyAkrama.htm?utm_source=chatgpt.com "Dīpaṃkaraśrījñāna [= Atīśa]: Gurukriyākrama (GRETIL)"
[7]: https://github.com/sarit/SARIT-corpus?utm_source=chatgpt.com "GitHub - sarit/SARIT-corpus: The e-texts of the SARIT project · GitHub"
[8]: https://www.production.crossref.org/documentation/retrieve-metadata/rest-api/?utm_source=chatgpt.com "REST API - Crossref"
[9]: https://developers.openalex.org/api-reference/authentication?utm_source=chatgpt.com "Authentication & Pricing - OpenAlex Developers"
[10]: https://developers.openalex.org/download/download-to-machine?utm_source=chatgpt.com "Download to your machine - OpenAlex Developers"
[11]: https://developers.openalex.org/download/overview?utm_source=chatgpt.com "Overview - OpenAlex Developers"
[12]: https://culture.gov.in/gyan-bharatam-mission?utm_source=chatgpt.com "Gyan Bharatam Mission | Ministry of Culture"
