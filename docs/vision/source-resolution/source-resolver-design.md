Yes — this exposes a **missing layer below Agent 2** that is strategically huge.

Right now Pāṭala effectively starts from:

```text
"we have a Sanskrit file"
        ↓
SOURCE
        ↓
factory
```

But for serious philology you eventually need:

```text
WORK
  ↓
EDITION / RECENSION
  ↓
MANUSCRIPT WITNESSES
  ↓
DIGITAL SURROGATES / SCANS
  ↓
TRANSCRIPTION / E-TEXT
  ↓
PĀṬALA SOURCE
  ↓
T1 → L0 → ARGMAP → ...
```

And the critical distinction is:

> **“I found an e-text called Tantrāloka” is not the same claim as “this is a verified transcription of edition X, which was constituted from witnesses A/B/C.”**

Your current bibliography strategy is already correctly curated rather than bulk-dump oriented: 254 records, on-disk sources promoted selectively, and `source_ready` deciding where deeper work is worthwhile.  Agent 2's newest branch goes further and exposes that factory quality signal through the API for 136 works.

What is missing is a **Source Authority / Edition Resolution layer** between bibliography and factory.

# The surprising answer: there is no one Sanskrit API

For modern papers:

```text
DOI
→ Crossref
→ OpenAlex
```

works beautifully.

For Sanskrit, especially old editions and manuscripts, the evidence is distributed across **library catalogs, Sanskrit-specific catalogs, manuscript databases, e-text projects, and scans**.

So don't search for one magical authoritative API.

Build:

# `Pāṭala Source Resolver`

as a **federated reconciliation engine**.

And use existing infrastructure for almost everything.

---

# 1. OpenRefine's reconciliation model is almost exactly the architecture

OpenRefine has a standardized Reconciliation API specifically for turning ambiguous labels plus contextual properties into ranked candidate identities, while preserving human review when the match is uncertain. ([OpenRefine][1])

That is precisely your problem:

```text
"Tantraloka"
"Tantrāloka"
"Tantralokah"
"TĀ"
"Tantrāloka with Viveka"
```

should resolve to:

```text
WORK:
Abhinavagupta — Tantrāloka

EDITION:
Madhusudan Kaul ed.
KSTS volumes...
publication data...

DIGITAL COPY:
scan X

E-TEXT:
GRETIL X
Muktabodha Y

MANUSCRIPT:
NGMCP A...
```

Don't blindly merge those.

Use the **reconciliation pattern**:

```text
input record
   ↓
candidate generation
   ↓
authority sources
   ↓
match evidence
   ↓
confidence
   ↓
AUTO / HUMAN REVIEW / UNRESOLVED
```

You can even expose your own Sanskrit authority data later as an OpenRefine-compatible reconciliation service.

That's an excellent standards-compatible move.

---

# 2. The Sanskrit-specific authority stack

I'd search these **in parallel**.

## A. New Catalogus Catalogorum — work identity

This is extremely important.

The University of Madras' **New Catalogus Catalogorum (NCC)** is explicitly intended as an encyclopedic master catalogue of Sanskrit and allied works/authors compiled from manuscript catalogues. ([UNO Myanmar University][2])

This helps answer:

```text
Does this title actually exist?
What aliases does it have?
Who is it attributed to?
Where are manuscripts catalogued?
Are there homonymous works?
```

For Pāṭala this is closer to a **Sanskrit work authority file** than OpenAlex is.

I'd eventually ingest/reconcile the relevant NCC slices.

Not dump everything.

Your lazy strategy applies perfectly:

```text
work touched
↓
query NCC
↓
cache relevant authority evidence
```

---

# 3. National Mission for Manuscripts — India-wide witness discovery

India's National Mission for Manuscripts maintains **Pandulipi Patala / Bharatiya Kriti Sampada**, with searchable fields for title, author, language, script, manuscript ID, accession number, material, scribe, commentary, date, institution, digitization status, etc. ([Namami Gange][3])

The Mission says its national database contains information on roughly four million manuscripts. ([Namami Gange][4])

That's not an "edition verification API."

It is something even more useful:

```text
WORK
↓
possible physical manuscript witnesses
```

However, their own disclaimer explicitly warns that some metadata may contain errors and advises researchers to contact repositories for authoritative details. ([Pandulipipatala][5])

That is perfect for Pāṭala's authority semantics:

```text
NMM_MATCH
≠
VERIFIED_WITNESS
```

Instead:

```text
discovered_by: NMM
catalogue_status: CATALOGUED
repository_verified: false
```

Then a repository/scholar can later raise it.

---

# 4. NGMCP is incredibly valuable for your Śaiva/Nepal material

The Nepalese-German Manuscript Cataloguing Project exists specifically to catalogue more than **180,000 manuscripts microfilmed in Nepal**, and now exposes Indic title search through its current MyCoRe catalogue. ([AAI Hamburg][6])

For tantra this is high-signal.

This becomes:

```text
Pāṭala Work
   ↓
NCC
NMM
NGMCP
   ↓
WitnessCandidate[]
```

The combination is much better than any one source.

---

# 5. SARIT is probably your best "verified-ish e-text" source

SARIT deserves a higher authority class than arbitrary downloaded Sanskrit.

It describes its texts as electronic editions that are **documented, dated, carry change history, are citable, and are downloadable as XML**, with all texts under Creative Commons licensing. ([Sarit][7])

So your source classification should distinguish:

```text
SARIT_TEI_EDITION
```

from:

```text
UNKNOWN_TXT
```

Massively different provenance.

SARIT is exactly the kind of upstream digital project Pāṭala should **link into rather than replace**.

---

# 6. GRETIL is useful, but it's not an authority oracle

GRETIL is a machine-readable text register and explicitly records contributors/input sources and normalized files. ([Gretl][8])

That's extremely useful, but you need to distinguish:

```text
GRETIL e-text identity
```

from:

```text
printed edition underlying that e-text
```

For example:

```text
digital witness:
  GRETIL file

derived_from:
  edition ???

edition_resolution:
  VERIFIED / PARTIAL / UNKNOWN
```

That missing `edition_resolution` is important.

---

# 7. Muktabodha is strategically exceptional for Pāṭala

Muktabodha says its digital library contains more than 3,000 preserved texts and over 570 searchable e-texts, with particularly strong Śaiva, Śākta, Śrīvidyā, Nātha, Pāñcarātra etc. coverage. It also says more than 380 of the e-texts were edited from manuscripts under Mark Dyczkowski's supervision. ([Muktabodha][9])

That means it shouldn't be treated as:

```text
random internet Sanskrit source
```

It is potentially:

```text
digital scholarly witness
```

But again, not all Muktabodha objects necessarily have identical editorial status.

Pāṭala's job is to **make that distinction explicit per object**.

---

# 8. For actual printed editions: use library reconciliation

This is where Sanskrit-specific databases stop being enough.

For a candidate printed edition, query:

```text
Google Books
HathiTrust
Library of Congress
WorldCat/OCLC if accessible
Open Library
```

Google Books exposes a public volumes API returning title, author, publisher, publication date and identifiers. ([Google for Developers][10])

HathiTrust has a bibliographic/volume API that can return records, including full MARC XML in its fuller responses. ([GitHub Wiki][11])

Library of Congress exposes public JSON/YAML APIs for its digitized holdings, while noting that its general API isn't equivalent to its entire library catalog. ([The Library of Congress][12])

WorldCat's metadata/search APIs are stronger bibliographically, but useful access is largely tied to institutional subscriptions; OCLC's Metadata API 2.0 supports searching bibliographic records and identifying best matches. ([OCLC][13])

So a resolver can do:

```text
Madhusudan Kaul
Tantraloka
1918
Kashmir Series of Texts and Studies
```

and accumulate:

```text
Google Books match
HathiTrust match
WorldCat match
LoC match
```

If 3 independent catalogs agree on:

```text
editor
publisher
year
series
volume
```

that's strong bibliographic evidence.

---

# 9. Don't represent this as `verified: true`

This is the Pāṭala lesson again.

Use dimensions.

For an edition:

```json
{
  "edition_id": "pt:edition:tantraloka:kaul",

  "work_ref": "pt:work:tantraloka",

  "statement": {
    "editor": "Madhusudan Kaul",
    "series": "...",
    "publisher": "...",
    "date": "..."
  },

  "authority_evidence": [
    {
      "source": "WORLD_CAT",
      "record_id": "...",
      "relation": "BIBLIOGRAPHIC_MATCH"
    },
    {
      "source": "GOOGLE_BOOKS",
      "record_id": "...",
      "relation": "BIBLIOGRAPHIC_MATCH"
    }
  ],

  "identity_status": "MULTI_SOURCE_MATCHED",

  "source_text_relation": "UNVERIFIED"
}
```

And then separately:

```text
WORK_IDENTITY
EDITION_IDENTITY
DIGITAL_COPY_IDENTITY
TEXT_DERIVATION
MANUSCRIPT_BASIS
```

These absolutely cannot be one boolean.

---

# 10. I would add an authority ladder

Something like:

```text
DISCOVERED
    ↓
CATALOG_MATCHED
    ↓
MULTI_SOURCE_MATCHED
    ↓
COPY_INSPECTED
    ↓
EDITION_VERIFIED
    ↓
TEXT_DERIVATION_VERIFIED
    ↓
SCHOLAR_CONFIRMED
```

Example:

```text
GRETIL Tantrāloka file

WORK_IDENTITY             VERIFIED
EDITION_IDENTITY          LIKELY
DIGITAL_FILE_INTEGRITY    VERIFIED
DERIVATION_FROM_EDITION   UNKNOWN
SCHOLAR_REVIEW            NONE
```

That's intellectually honest.

And very useful to the factory.

---

# 11. Your `source_ready` should eventually depend on this

Currently Agent 2 has built a useful quality signal.

Eventually:

```text
source_ready =
    file_clean
    AND work_identity_resolved
    AND edition_identity_above_threshold
    AND rights_ok
    AND source_text_provenance_ok
```

Not merely:

```text
there is clean Sanskrit on disk
```

This is a major upgrade.

---

# 12. And yes — the manuscript pipeline you're imagining is extremely real

This is where it gets interesting.

Use **IIIF** as the canonical external image layer.

IIIF Presentation 3 represents digitized compound objects as:

```text
Manifest
→ Canvas
→ image/text annotations
```

and is specifically designed to support manuscripts/books, rich viewing, distributed annotation, and linked representations. ([IIIF][14])

So if Oxford gives you:

```text
IIIF manifest
```

Pāṭala doesn't need to download some giant mysterious ZIP and reinvent image identity.

You store:

```json
{
  "witness_id": "pt:ms:...",
  "repository": "Bodleian",
  "shelfmark": "...",
  "iiif_manifest": "...",
  "canvases": [...]
}
```

Then every folio is stable and addressable.

---

# 13. Oxford is actually *eerily* aligned with this

You specifically mentioned Oxford Hindu work, and yes.

The **Oxford Centre for Hindu Studies has an Indic Manuscript Database** whose stated goals include:

* manuscript images;
* transliterated and translated texts side-by-side;
* structured downloads;
* textual analysis/concordance;
* overlays of text on images;
* comments/corrections. ([ochs-database.netlify.app][15])

Even more importantly, Oxford currently has a project training AI handwriting/text recognition models for South Asian manuscripts, using **Transkribus** on Devanāgarī Sanskrit material, including Śākta and Vaiṣṇava palm-leaf manuscripts in that OCHS database. ([Theology at Oxford][16])

This is almost the perfect institutional adjacency.

They're working on:

```text
manuscript
→ transcription
```

You're working on:

```text
transcription
→ verified edition/source
→ translation
→ arguments
→ scholarship
→ education
```

Those systems fit together rather than compete.

---

# 14. Bodleian is another direct integration target

Digital Bodleian supports IIIF, and Oxford says its Sanskrit collection contains around **8,700 manuscripts**, with a dedicated Sanskrit and South Asian manuscript digitization effort. ([IIIF][17])

So imagine:

```text
Digital Bodleian IIIF manifest
               ↓
          Pāṭala Witness
               ↓
       folio / Canvas refs
               ↓
             HTR
               ↓
          transcription
               ↓
           collation
               ↓
            edition
               ↓
         SOURCE VERIFIED
               ↓
       Agent 2 factory
```

That is a legitimate scholarly infrastructure pipeline.

---

# 15. For OCR/HTR: don't build recognition from scratch

Oxford/OCHS is currently using Transkribus specifically for the Sanskrit manuscript HTR project. ([Theology at Oxford][16])

For your own open/self-hosted infrastructure, **Kraken** is the obvious thing to test. Kraken is designed for historical and non-Latin script recognition, is trainable, and exposes both CLI and programmatic APIs. ([GitHub][18])

So:

```text
external institution / easy collaboration:
Transkribus

open/self-hosted research:
Kraken
```

Don't spend six months building a generic HTR engine.

Spend your time building:

```text
HTROutput
→ SourceCandidate
→ collation
→ review
→ provenance
```

That's your layer.

---

# 16. There is a whole missing **textual criticism compiler**

This is the truly exciting extension.

Right now:

```text
SOURCE → T1
```

Eventually becomes:

```text
MS A ─┐
MS B ─┼─► transcription
MS C ─┘
          ↓
       collation
          ↓
    VariantReading[]
          ↓
      EditionDecision
          ↓
     CriticalText
          ↓
        SOURCE
```

And then Pāṭala can ask:

> Which manuscript variants actually matter downstream?

Example:

```text
variant v38
changes Sanskrit morphology
↓
changes translation TD-81
↓
changes Proposition P17
↓
breaks Argument ARG-4
↓
changes Essay / Education
```

That is insane in the good sense.

It's **semantic textual criticism**.

---

# 17. You should distinguish `Work`, `Edition`, `Witness`, `Surrogate`

I think this is essential.

```text
WORK
Tantrāloka
abstract intellectual work

EDITION
Kaul's constituted edition
an editorial scholarly object

WITNESS
MS A, MS B, MS C
physical manuscripts

SURROGATE
Bodleian scan / NGMCP microfilm / uploaded photos
digital representation of witness

TRANSCRIPTION
human/HTR reading of surrogate

E-TEXT
GRETIL/SARIT/Muktabodha digital textual representation

SOURCE
the exact textual basis Pāṭala chose for this run
```

This gives you sane lineage:

```text
pt:source:...
 derived_from
    pt:etext:...
 derived_from
    pt:edition:...
 constituted_from
    pt:witness:A
    pt:witness:B
```

Or sometimes:

```text
SOURCE
derived directly from manuscript transcription
```

No pretending.

---

# 18. Upload becomes powerful

Someone at a monastery, archive, university, or private collection uploads 300 folio images.

Pāṭala should do:

```text
UPLOAD
  ↓
checksums
  ↓
image metadata
  ↓
IIIF Manifest
  ↓
script/language estimate
  ↓
title / colophon candidate extraction
  ↓
NCC / NMM / NGMCP reconciliation
  ↓
possible:
"This appears to be Kubjikāmata"
  ↓
human confirmation
  ↓
Witness created
  ↓
HTR / transcription
  ↓
compare against known e-text / editions
  ↓
variant detection
  ↓
SourceCandidate
  ↓
scholar approval
  ↓
SOURCE
  ↓
T1 → L0 → ARGMAP...
```

This connects **acquisition directly into the epistemic graph**.

---

# 19. And then the bibliography strategy gets even better

Your tiers become two-dimensional.

Currently:

```text
Tier 0 audited
Tier 1 on-disk
Tier 2 documented
Tier 3 lazy
```

Keep that.

But add an orthogonal source-authority vector:

```text
DISCOVERY DEPTH
Tier 0 / 1 / 2 / 3

SOURCE AUTHORITY
U0 unknown
U1 catalogued
U2 reconciled
U3 edition verified
U4 witness-grounded
U5 scholar reviewed
```

So:

```text
Kubjikāmata

discovery_depth: TIER_0
source_authority: U4
```

versus:

```text
obscure GRETIL item

discovery_depth: TIER_1
source_authority: U1
```

Now your prioritizer gets substantially smarter.

---

# 20. A fantastic near-term piece to build

I would give Agent 2 a new component:

```text
pipeline/source_resolver.py
```

Input:

```json
{
  "title": "Tantrāloka",
  "author": "Abhinavagupta",
  "local_file": "..."
}
```

Adapters:

```text
SANSKRIT
NCC
NMM / Pandulipi Patala
NGMCP
SARIT
GRETIL
Muktabodha

GENERAL BOOK
Google Books
HathiTrust
LoC
WorldCat if credentials

DIGITAL MANUSCRIPT
IIIF
```

Output:

```json
{
  "work_candidates": [],
  "edition_candidates": [],
  "witness_candidates": [],
  "digital_surrogates": [],

  "resolution": {
    "work": "RESOLVED",
    "edition": "MULTI_SOURCE_MATCH",
    "text_derivation": "OPEN"
  },

  "evidence": []
}
```

Crucially:

```text
NO automatic authority promotion from fuzzy matching.
```

---

# 21. Build a human reconciliation queue, not more AI

If resolver confidence is:

```text
0.99 — exact ISBN / exact catalog record
```

automatically bind.

If:

```text
0.78 — title/editor/year match
```

queue:

```text
REVIEW MATCH
```

If:

```text
Tantrasara
multiple similarly named works
```

don't guess.

Send to a human/scholar.

That follows Pāṭala's whole philosophy.

---

# 22. Partnership architecture suddenly becomes really compelling

You don't pitch Oxford/OCHS:

> Give us your manuscripts so our AI can translate them.

You pitch:

> **Keep ownership and canonical manuscript identity. Pāṭala consumes your stable images/transcriptions, attaches edition/provenance lineage, translates and analyzes them downstream, and every derivative claim remains resolvable back to your manuscript and your scholars' corrections.**

Much stronger.

For Oxford:

```text
OCHS / Bodleian
owns:
images
cataloguing
HTR ground truth
manuscript expertise

PĀṬALA
adds:
source reconciliation
translation audit
argument/evidence graph
dependency analysis
scholar review
education/media projections
```

That's complementary.

And importantly, the new Indian **Gyan Bharatam Mission** currently states an ambition to catalog/digitize up to one crore manuscripts, build a national digital repository, use AI-assisted transcription/provenance systems, and provide APIs integrating national and international archives. ([Ministry of Culture][19])

That's a potential ecosystem Pāṭala could plug into rather than duplicate.

---

# The bigger architecture

This is what I think you're actually building now:

```text
                 CULTURAL KNOWLEDGE SUPPLY CHAIN

                        DISCOVERY
                           │
          NCC / NMM / NGMCP / libraries
                           │
                           ▼
                         WORK
                           │
                     ┌─────┴─────┐
                     ▼           ▼
                  EDITION     MANUSCRIPT
                     │           │
                     │         IIIF
                     │           │
                     │       scan/images
                     │           ↓
                     │          HTR
                     │           ↓
                     └─────► TRANSCRIPTION
                               │
                            COLLATION
                               │
                         EditionDecision
                               │
                               ▼
                            SOURCE
                               │
                         PĀṬALA FACTORY
                               │
              T1 → L0 → ARGMAP → L2 → L200 → C1
                               │
                         EPISTEMIC CORE
                               │
                   propositions / arguments
                               │
                       scholar evidence
                               │
                           ReviewEvent
                               │
                          adjudication
                               │
              ┌────────────────┼──────────────┐
              ▼                ▼              ▼
            ESSAY          EDUCATION         API
              │                │              │
              └──────────── MEDIA ────────────┘
```

The really important insight is that **the manuscript isn't merely another input file**.

It's the root of the entire dependency graph.

So eventually someone should be able to click a YouTube claim and descend:

```text
video statement
↓
essay claim
↓
argument
↓
proposition
↓
translation decision
↓
critical-text reading
↓
variant
↓
MS Bodl. Sanskrit xxx
↓
folio 41r
↓
IIIF pixels
```

That is what "legit" looks like.

Not because you used blockchain or a fancy AI.

Because the whole intellectual chain is **resolvable back to the physical historical evidence**.

[1]: https://openrefine.org/docs/technical-reference/reconciliation-api?utm_source=chatgpt.com "Reconciliation API | OpenRefine"
[2]: https://www.unom.ac.in/index.php?deptid=64&route=department%2Fdepartment%2Fabout&utm_source=chatgpt.com "Welcome to University of Madras"
[3]: https://namami.gov.in/database-menu-script?utm_source=chatgpt.com "Database of Manuscript | National Mission for Manuscripts |"
[4]: https://www.namami.gov.in/objectives?utm_source=chatgpt.com "Objectives | National Mission for Manuscripts |"
[5]: https://www.pandulipipatala.nic.in/article/disclaimer?utm_source=chatgpt.com "National Mission for Manuscripts"
[6]: https://www.aai.uni-hamburg.de/en/forschung/ngmcp.html?utm_source=chatgpt.com "The Nepalese-German Manuscript Cataloguing Project : Asia Africa Institute : University of Hamburg"
[7]: https://sarit.indology.info/apps/sarit-pm/docs/welcome.html?utm_source=chatgpt.com "SARIT: Search and Retrieval of Indic Texts (New)"
[8]: https://gretil.sub.uni-goettingen.de/gretilbk.htm?utm_source=chatgpt.com "GRETIL - Göttingen Register of Electronic Texts in Indian Languages"
[9]: https://muktabodha.org/digital-library/?utm_source=chatgpt.com "Digital Library | Muktabodha"
[10]: https://developers.google.com/books/docs/v1/reference/volumes/list?utm_source=chatgpt.com "Volume: list  |  Google Books APIs  |  Google for Developers"
[11]: https://github-wiki-see.page/m/hathitrust/catalog/wiki/Volume-API?utm_source=chatgpt.com "Volume API - hathitrust/catalog GitHub Wiki"
[12]: https://www.loc.gov/apis/json-and-yaml/?utm_source=chatgpt.com "JSON/YAML for LoC.gov | APIs at the Library of Congress | Library of Congress"
[13]: https://www.oclc.org/developer/news/2023/worldcat-metadata-api-2-release.en.html?utm_source=chatgpt.com "WorldCat Metadata API 2.0"
[14]: https://iiif.io/api/presentation/3.0/?utm_source=chatgpt.com "Presentation API 3.0 — IIIF | International Image Interoperability Framework"
[15]: https://ochs-database.netlify.app/?utm_source=chatgpt.com "Home | OCHS Manuscript Database Project"
[16]: https://www.theology.ox.ac.uk/node/4399991?utm_source=chatgpt.com "Digital Humanities & Hindu Studies: Creating AI Models for Handwriting and Text Recognition in South Asian Manuscripts | Faculty of Theology and Religion"
[17]: https://iiif.io/guides/guides/digital.bodleian.ox.ac.uk/?utm_source=chatgpt.com "University of Oxford (Digital Bodleian) — IIIF | International Image Interoperability Framework"
[18]: https://github.com/mittagessen/kraken/blob/main/docs/index.rst?utm_source=chatgpt.com "kraken/docs/index.rst at main · mittagessen/kraken · GitHub"
[19]: https://culture.gov.in/offering/mission/national-mission-manuscripts?utm_source=chatgpt.com "Gyan Bharatam Mission | Ministry of Culture"
