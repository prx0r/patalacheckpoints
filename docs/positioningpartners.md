# Positioning & Partners — the connective research layer

> **STATUS: DETAILED COMPETITIVE LANDSCAPE.** Superseded as the *global* partnerships doc by
> `docs/global/globalpartnerships.md` (the integration/identity-layer framing). This file remains the
> detailed landscape + pitch templates. Global strategy: `docs/global/globalpartnerships.md`.

*The most important strategic conclusion: Pāṭala should not become another archive, Sanskrit library, manuscript-digitisation project, or translation publisher. Several established groups already do those jobs well. The gap is the **connective research layer between them**.*

## The landscape

| Player                       | What they already do extremely well                                                                                                                                                                                                             | Where we should NOT compete                                          |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Muktabodha**               | World's largest searchable collection of tantric literature; 3,000+ preserved texts, 570+ searchable e-texts, 380+ manuscript-derived tantric e-texts; active IFP transcription collaborations. ([Muktabodha][1])                               | Acquiring/transcribing huge numbers of tantric manuscripts ourselves |
| **Gyan Bharatam**            | National-scale manuscript surveying, digitisation, repository infrastructure, AI-assisted transcription, provenance and APIs; target of 1+ crore manuscripts. ([Ministry of Culture][2])                                                        | Generic digitisation, national manuscript repository, generic OCR/AI |
| **OCHS Śākta Database**      | Very close to our domain: manuscript images, provenance, NAK/NGMPP identifiers, scripts, dates, transliterations, translations and searchable Śākta/Tantric manuscript metadata; currently hundreds of records. ([OCHS Manuscript Database][3]) | Building another standalone Śākta manuscript catalogue               |
| **Centre for Kaula Studies** | Specifically identifies, locates, secures permission for, transcribes and digitises rare Kaula manuscripts. ([Centre for Kaula Studies][4])                                                                                                     | Becoming "another Kaula manuscript acquisition centre"               |
| **GRETIL / SARIT / Ambuda**  | Machine-readable Sanskrit. SARIT has TEI scholarly editions with provenance/change history and CC licensing; Ambuda provides bulk TEI/plain-text + structured metadata. ([Sarit][5])                                                            | Generic Sanskrit digitisation / general Sanskrit corpus              |
| **BDRC/BUDA**                | The mature Buddhist analogue: tens of millions of pages, IIIF, linked open data, cross-collection identifiers and research interfaces. ([BDRC][6])                                                                                              | Building a massive general-purpose archival repository               |
| **84000**                    | Professional translation production, translation guidelines, cumulative glossary and translation-memory infrastructure. ([84000][7])                                                                                                            | Making "we translate texts" the core proposition                     |
| **SuttaCentral/Bilara**      | Immutable passage IDs, aligned root/translation/comment/variant data, translation versioning and publication workflows. ([GitHub][8])                                                                                                           | Reinventing generic collaborative translation mechanics              |

The most important competitors/adjacent partners for **Pāṭala specifically** are probably **Muktabodha, OCHS and Kaula Studies**.

And that's good news, because none of them makes your idea redundant.

---

# Where the gap actually is

Suppose I am researching **Tantrasadbhāva** today.

I might need:

```text
Muktabodha
→ Sanskrit transcription

NGMPP
→ manuscript witness

OCHS
→ potentially manuscript metadata/images

GRETIL/SARIT
→ machine-readable related Sanskrit

Hamburg
→ Bang's research

Academia / journals
→ Sanderson etc.

Dyczkowski
→ lectures/commentary

publisher catalogues
→ existing translations

YouTube
→ lectures

Sanskrit Heritage
→ morphology
```

Those are **resources**.

What doesn't exist cleanly is:

```text
                    TANTRASADBHĀVA

Identity
├── alternate titles
├── date
├── traditions
└── textual family

Sources
├── manuscripts
├── editions
└── e-texts

Research
├── translations
├── scholarship
├── lectures
└── commentaries

Textual intelligence
├── terms
├── parallel passages
├── quotations
├── borrowing relationships
└── related works

Tools
├── passage API
├── concordance
├── historical term search
├── translation context
└── MCP
```

**That integrated object is the gap.**

Pāṭala should not own every leaf on the tree.

It should know **how all the leaves connect**.

---

# The closest analogue is actually BDRC

BDRC is worth studying very carefully because they already discovered the architectural insight we're converging on.

They describe BUDA not merely as a scan repository but as **Linked Open Data** connecting resources at the data level, with a scholarly model for identifying texts across languages and collections. ([BDRC][9])

That's essentially:

> authority graph + archive.

But BDRC is focused on Buddhist textual heritage.

Pāṭala can be:

> **authority graph + research intelligence for tantric textual heritage.**

And crucially, we do **not** need to build BDRC-scale archival infrastructure ourselves.

We can point at their equivalent upstream repositories.

---

# The biggest direct overlap: OCHS

This one deserves serious attention because their stated mission is remarkably close:

> searchable primary research materials, manuscript metadata, transliterations and translations, with a current emphasis on Śākta/tantric traditions. ([OCHS Manuscript Database][10])

Their Śākta database already tracks things we want:

```text
canonical/alternate title
script
language
author
repository
NAK / NGMPP identifiers
provenance
date
folios
physical condition
tradition
transliteration
translation
incipit
colophon
bibliography
```

([OCHS Manuscript Database][3])

So **don't recreate that schema manually if interoperability is possible.**

Our differentiation should be above it:

```text
OCHS

"Here is manuscript NAK 1-285
of the Netratantra."

             ↓

Pāṭala

"This manuscript witnesses
pt:work:netratantra.

Here are all other witnesses,
published editions,
translation coverage,
passage identities,
related scriptures,
citations,
terminology,
lectures,
and AI research tools."
```

That makes OCHS a potential upstream **partner**, not enemy.

---

# Same with Muktabodha

Muktabodha explicitly calls its searchable library the world's largest collection of Tantric literature, and its team has decades of expertise transcribing manuscripts—including Newari materials—into searchable texts. ([Muktabodha][1])

Trying to say:

> "We'll build a bigger Muktabodha"

would be ridiculous.

Much better:

```text
MUKTABODHA
preserves/transcribes Sanskrit
        ↓
TANTRAKOŚA
makes that Sanskrit computationally
and intellectually navigable
        ↓
scholars + AI agents
```

We should send traffic **back** to Muktabodha.

Every corpus record can say:

> Source transcription: Muktabodha M00xxx →

That reinforces their contribution.

Then there is no zero-sum relationship.

---

# Same with Kaula Studies

They already have the hard, human, location-dependent process:

```text
identify
locate
secure permission
transcribe
digitise
```

([Centre for Kaula Studies][4])

Excellent.

We want them doing that.

Pāṭala can provide downstream:

```text
stable work identity
bibliographic linkage
passage segmentation
translation workspace
term concordance
parallel detection
API
MCP
scholar profile
publication
```

Potentially they could literally use Pāṭala infrastructure.

That's more interesting than competing.

---

# Gyan Bharatam is even clearer

They explicitly intend to provide:

* national manuscript repository;
* AI-assisted transcription;
* OCR;
* provenance;
* cloud infrastructure;
* APIs connecting national/international manuscript archives. ([Ministry of Culture][2])

Therefore:

## Do **not** build

```text
Pāṭala OCR
Pāṭala generic manuscript cloud
Pāṭala national manuscript database
```

unless needed as tiny internal components.

Their scale makes that pointless.

Instead:

```text
Gyan Bharatam API
       ↓
millions of records
       ↓
Pāṭala resolver
       ↓
"Which of these belong to
tantric textual traditions?"
       ↓
authority matching
       ↓
text families
       ↓
research graph
```

That's complementary.

---

# Sanskrit Heritage / Ambuda / SARIT solve another layer

Ambuda already lets users download its corpus as **TEI XML, plain text and structured metadata**, including authors and source information. ([Ambuda][11])

SARIT intentionally builds scholarly TEI editions with provenance, change histories, search and downloadable XML/PDF/EPUB. ([Sarit][5])

Sanskrit Heritage already offers dictionary/grammar/sandhi/corpus functions. ([Sanskrit][12])

Therefore don't spend three years trying to invent:

> universal Sanskrit parser/database.

Integrate existing Sanskrit infrastructure and specialize where Tantra creates unusual requirements.

---

# So what do we uniquely own?

This is the important question.

I'd define Pāṭala's **seven proprietary competencies** as:

### 1. Tantric authority graph

```text
work
↔ alternate title
↔ manuscript
↔ edition
↔ passage
↔ author
↔ tradition
↔ historical period
```

Nobody above seems to provide this comprehensively across the Śaiva-Śākta field.

### 2. Textual relationship graph

```text
quotes
borrowed from
comments on
rewrites
same textual family
parallel passage
```

with **evidence**.

This is much stronger than mere hyperlinks.

### 3. Historical terminology layer

Not:

> `kula = family`.

Instead:

> occurrences and senses of *kula* across specific traditions, periods and textual families.

This is a direct scholarly research tool.

### 4. Scholar validation graph

```text
this identity
verified by X

this manuscript assignment
corrected by Y

this parallel
accepted by Z
```

Expert judgments accumulate.

This may become the strongest moat.

### 5. Research workflow

```text
passage
→ context
→ terms
→ parallels
→ manuscript readings
→ translation
→ review
→ publication
```

Most existing projects expose **data**.

We expose **workflows over federated data**.

### 6. Machine interface

Open:

```text
API
MCP
structured citations
```

so ChatGPT/Claude/research software can navigate the field programmatically.

84000, for comparison, says API access is currently made available to approved partners rather than operating an open API. ([84000][13])

That creates room for an explicitly machine-first scholarly layer.

### 7. Public bridge

Then:

```text
scholarship
↓
beautiful explanation
↓
lecture
↓
course
↓
event
↓
retreat
```

Muktabodha doesn't need to become that.

OCHS doesn't need to become that.

Gyan Bharatam definitely doesn't need to become that.

That's ours.

---

# I would describe the ecosystem like this

```text
              PHYSICAL COLLECTIONS
                     │
                     ▼
             GYAN BHARATAM
           OCHS · NGMPP · IFP
                     │
              manuscript data
                     │
                     ▼
               MUKTABODHA
           KAULA STUDIES · GRETIL
                     │
                usable texts
                     │
                     ▼
               TANTRAKOŚA
          ┌──────────┼──────────┐
          │          │          │
       identity   relations   context
          │          │          │
          └──────────┼──────────┘
                     ↓
              SCHOLAR WORKFLOW
                     ↓
         annotations / corrections
                     ↓
              API / MCP / AI
                     ↓
          PUBLIC LEARNING LAYER
```

That's extremely non-adversarial.

Everyone upstream gets cited and linked.

---

# The institutional pitch changes completely

Don't tell Muktabodha:

> "We're building a Tantra database."

Tell them:

> **"We want Muktabodha records and passages to become easier for scholars and AI systems to discover and cite, while preserving Muktabodha as the authoritative source."**

Don't tell OCHS:

> "We're building a manuscript database."

Say:

> **"We want to resolve your manuscript records against a shared tantric work authority graph and expose the scholarly relationships downstream."**

Don't tell Gyan Bharatam:

> "We digitize manuscripts."

Say:

> **"We specialize in domain enrichment and scholarly validation of the tantric subset of manuscript data."**

Don't tell Kaula Studies:

> "We'll acquire manuscripts."

Say:

> **"We can provide infrastructure for the research lifecycle after your texts are transcribed."**

Those pitches are collaborative by design.

---

# What I would explicitly put in Pāṭala's mission

Something like:

> **Pāṭala does not seek to replace manuscript archives, textual repositories, publishers, or scholarly projects. It connects them.**

Then:

> **Every externally sourced object retains its provenance and links to its authoritative custodian.**

That's both ethically good and strategically intelligent.

It makes institutions less afraid that you're trying to scrape their life's work into some AI site.

---

## The resulting niche is surprisingly clean

**Muktabodha:** preserve/transcribe tantric texts.
**OCHS:** document and expose manuscript collections.
**Kaula Studies:** locate/transcribe/study Kaula manuscripts.
**Gyan Bharatam:** national digitisation infrastructure.
**GRETIL/SARIT/Ambuda:** digital Sanskrit.
**Sanskrit Heritage:** language analysis.
**84000/Bilara:** models for translation workflow.

**Pāṭala:**

> **Resolve, connect, contextualize and operationalize tantric textual knowledge for scholars, institutions, readers and machines.**

That's the gap I would protect.

And it also means your most valuable early work isn't "get more PDFs." It's exactly what you're already beginning to build: **stable identities, clean metadata, passage IDs, relationships, provenance, scholar-validation workflows, and a genuinely useful API/MCP over the federation.**

[1]: https://muktabodha.org/digital-library/ "Digital Library | Muktabodha"
[2]: https://culture.gov.in/gyan-bharatam-mission "Gyan Bharatam Mission | Ministry of Culture"
[3]: https://ochs-database.netlify.app/sakta/ "Śākta | OCHS Manuscript Database Project"
[4]: https://www.kaulastudies.org/manuscriptdatabase "Manuscript Database | Discover Primary Texts—Explore Now — Centre for Kaula Studies"
[5]: https://sarit.indology.info/apps/sarit-pm/docs/welcome.html "SARIT: Search and Retrieval of Indic Texts (New)"
[6]: https://www.bdrc.io/ "Home - Buddhist Digital Resource Center"
[7]: https://84000.co/tools-for-translators "Tools for Translators | 84000"
[8]: https://github.com/suttacentral/bilara-data "GitHub - suttacentral/bilara-data: Content for Bilara translation webapp. · GitHub"
[9]: https://www.bdrc.io/programs/ "Programs - Buddhist Digital Resource Center"
[10]: https://ochs-database.netlify.app/ "Home | OCHS Manuscript Database Project"
[11]: https://ambuda.org/texts/downloads/ "Downloads | Ambuda"
[12]: https://sanskrit.inria.fr/cgi-bin/SKT/sktindex.cgi "Sanskrit Heritage Dictionary"
[13]: https://www.84000.co/documents/terms-of-use "Terms of Use (DRAFT)"
