# Global Partnerships — Pāṭala as the Integration & Identity Layer over the Sanskrit Ecosystem

*2026-08-13. The canonical global partnerships + ecosystem-positioning document. Consolidates the imported
"OpenAlex-for-Sanskrit / integration-layer" vision with the existing `docs/positioningpartners.md` (the
connective-research-layer thesis) and `docs/vision/vision-10-market-entry-and-partnerships.md` (go-to-market).
This file is the GLOBAL source of truth for how Pāṭala positions against and partners with the fragmented
Sanskrit ecosystem.*

---

## The one strategic thesis

> **Pāṭala is not another archive, Sanskrit library, manuscript-digitisation project, or translation
> publisher. It is the integration/identity layer that connects the fragmented Sanskrit ecosystem.**

Every partner class below already does its own job well. Pāṭala's value is *between* them: **resolve,
connect, contextualize and operationalize tantric/Sanskrit textual knowledge for scholars, institutions,
readers and machines** — while preserving every external custodian as the authoritative source.

The right mental model is Pāṭala as **"OpenAlex for Sanskrit"**: not "search Sanskrit," but
**resolve the Sanskrit intellectual record.**

---

## The four partner classes

### 1. Manuscript custodians (they own the physical witnesses)

For the Śaiva/Tantra launch specifically:

| Partner | Why it matters |
|---|---|
| **IFP Pondicherry + EFEO** | ~8,500 palm-leaf codices (IFP), ~10,000 in the broader IFP/EFEO effort, predominantly Sanskrit/Grantha around the Śaiva Āgamas. Disproportionately valuable for our Śaiva vertical. |
| **Muktabodha** | 3,000+ preserved texts, 570+ searchable e-texts, IFP transcripts, hundreds of Śaiva/Śākta/Kaula e-texts. Almost tailor-made for the initial vertical. |
| **NGMCP / NGMPP** | Cataloguing 180,000+ manuscripts microfilmed by the Nepal-German project — enormous Nepalese witness base. |
| **BORI, Pune** | Major Sanskrit/Prakrit manuscript repository with ongoing digitisation. |
| **National Mission for Manuscripts / IGNCA** | The route into the distributed Indian institutional network (catalogues from collections across India). |
| **Bodleian** | ~8,700 Sanskrit manuscripts; exposes a proper Data API + IIIF — an early clean adapter target. |
| **Cambridge University Library** | 1,600+ works/manuscripts across Sanskrit and related languages. |
| Later: Sarasvati Mahal, Mysore/Tirupati ORI, Kerala collections, Asiatic Society, Adyar, BHU/Sampurnanand, etc. | Via the National Mission network. |

For the Śaiva launch: **IFP + EFEO + Muktabodha + NGMCP** are disproportionately valuable.

### 2. Existing digital Sanskrit projects (become sources/adapters, never replaced)

```text
GRETIL        → electronic text instances
SARIT         → TEI scholarly electronic editions
Muktabodha    → tantric e-texts + manuscript surrogates
DCS           → segmentation/morphology
PANDiT        → people/work/manuscript metadata
NGMCP         → manuscript descriptions
Dharmamitra / DharmaNexus → intertextuality
BuddhaNexus   → parallels
C-SALT        → Sanskrit dictionaries (REST + GraphQL APIs)
```

SARIT is architecturally clean (TEI on GitHub, provenance + revision history). C-SALT gives us
lexicographical links while the dictionary definitions stay **external evidence**, and our contextual
Sanskrit sense objects remain **ours**.

### 3. Global open infrastructure (integrate immediately)

| System | Pāṭala use |
|---|---|
| **OpenAlex** | papers, scholars, institutions, citations |
| **Crossref** | DOI metadata |
| **Wikidata** | universal entity crosswalk |
| **VIAF** | authority IDs for historical authors |
| **ROR** | research institution identities |
| **ORCID** | living scholar identities |
| **IIIF** | manuscript images (native support — a strategic decision) |
| **Internet Archive** | scanned editions/books |
| **GitHub** | open textual datasets/software |

**IIIF is a major architectural decision — support it natively from the start.** It lets an institution
retain its high-resolution manuscript while Pāṭala publishes a JSON-LD manifest referencing their canvases.
Pāṭala's viewer displays Bodleian/IFP images directly — no need to become a giant image host. **One IIIF
adapter potentially connects many libraries.**

### 4. Buddhist analogues worth studying (not competing)

- **BDRC/BUDA** — the mature Buddhist analogue: millions of pages, IIIF, linked open data, cross-collection
  identifiers, research interfaces.
- **84000 / Bilara / SuttaCentral** — professional translation workflow + immutable passage IDs + versioned
  publication. Models, not competitors.
- **Syriaca.org** — the closest precedent to our exact problem: ~20,000 manuscripts across disparate
  catalogues; they built an **authority file for works** linking works → manuscripts → editions →
  translations. Study their modeling seriously before freezing our Work/Manuscript/Edition ontology.

---

## Pāṭala owns the identity/crosswalk (foundational)

**Never let an external database become our primary key.** `PATA-W-xxx` survives even if PANDiT changes,
GRETIL disappears, a URL moves, or scholars later decide two works are one.

```text
Work            PATA-W-00000182  Tantrasadbhāva
  external_identifiers: pandit / wikidata / gretil / ngmcp
  names, assertions (date, tradition)

Witness         PATA-M-001928  work → PATA-W-…, repository, shelfmark, catalogue_records, IIIF surrogates
Edition         PATA-E-000083  based_on MSs, edited_by scholar
TextInstance    PATA-T-000491  derived_from Edition, available_at GRETIL URL, encoding
```

**The critical separation (never flattened):** a *work* ≠ *edition* ≠ *manuscript* ≠ *scan* ≠
*transcription* ≠ *translation*. Most Sanskrit systems flatten some of these because they weren't built
as global identity infrastructure.

---

## Every imported fact carries provenance (the catalogue-scholarship generalization)

NGMCP says MS A = Mālinīvijayottara; PANDiT says the same; Scholar X later corrects it. **Pāṭala never
overwrites a field** — it records versioned, citable **Assertions**:

```text
ASSERTION 92381   subject: MS A   predicate: witness_of   object: Mālinīvijayottaratantra
  source: NGMCP   confidence: …   status: superseded / disputed / accepted
```

The translation-review machinery we already built generalizes to **catalogue scholarship itself**.

---

## The partnership pitch (make it collaborative, never extractive)

> **"We will make your manuscripts discoverable in the global Sanskrit knowledge graph while preserving
> your institution as custodian and canonical source."**

Don't ask for their data to hoard it — make their page the destination:

```text
Mālinīvijayottara  ── WORK ──
  Witnesses 17 · Editions 4 · Translations 2 · Related 31 · Citations 86
  IFP 1234        [French Institute of Pondicherry]  [View manuscript]
  NGMCP A123/4    [National Archives Nepal]          [Catalogue]
  Oxford MS ...   [Bodleian Libraries]               [View manuscript]
```

**Every institution gets attribution and traffic.**

Pitch templates (from `docs/positioningpartners.md`):
- **Muktabodha:** "We want Muktabodha records and passages to become easier for scholars and AI to
  discover and cite, while preserving Muktabodha as the authoritative source."
- **OCHS:** "We want to resolve your manuscript records against a shared tantric work authority graph."
- **Gyan Bharatam:** "We specialize in domain enrichment and scholarly validation of the tantric subset."
- **Kaula Studies:** "We can provide infrastructure for the research lifecycle after your texts are transcribed."

---

## Canonical schema additions (first-class objects)

Make these canonical first-class objects (integrate into the Atlas identity layer):

```text
Work · Person · Institution · Collection
Manuscript · ManuscriptPart · Folio
Edition · Translation · TextInstance
Passage · Token · LexicalSense
Publication · ScholarlyClaim
Assertion · Evidence · Review · Identifier
```

Universal pattern:

```text
Pāṭala entity
  ├── native assertions
  ├── external assertions
  └── identifiers (Wikidata / VIAF / PANDiT / NGMCP / OpenAlex / DOI / repository IDs)
```

---

## The killer end state

> A scholar discovers an unidentified manuscript in Kerala. The repository registers it once. Pāṭala
> resolves possible works from textual similarity; identifies parallels in GRETIL/Muktabodha/SARIT;
> connects probable authors through PANDiT/Wikidata/VIAF; discovers relevant scholarship through
> OpenAlex/Crossref; exposes the scan through IIIF; scholars adjudicate the identity; and that
> adjudication becomes a versioned, citable assertion in the graph.

**That is "OpenAlex for Sanskrit."**

---

## Integration-first order

Build these adapters first (not fifty):

```text
1.  Wikidata     universal cross-ID
2.  OpenAlex     secondary scholarship graph
3.  Crossref     DOI truth
4.  VIAF         historical people identities
5.  ROR          institutions
6.  C-SALT       dictionaries
7.  GRETIL       texts
8.  SARIT        TEI texts
9.  PANDiT       Indic works/people/manuscripts
10. NGMCP        manuscript catalogue
11. IIIF         generic manuscript-image adapter (one adapter → many libraries)
```

---

## Relation to existing docs

- **`docs/positioningpartners.md`** — the connective-research-layer thesis (superseded as *positioning*,
  consolidated here as *partnerships/identity*). Keep as the detailed competitive landscape.
- **`docs/vision/vision-10-market-entry-and-partnerships.md`** — the concrete go-to-market (BHU, funding,
  pilots, legal/IP). Complements this doc.
- **`docs/vision/vision-14-manuscript-to-scholarly-asset.md`** — the manuscript→asset onboarding flow.
- **`docs/global/agent1atlas.md`** — the Atlas convergence directive (identity/persistence ownership).
- **`docs/endgame2.md`** (Tantra Hub), **`docs/endgame4.md`** (economics), **`docs/endgame5year.md`**
  (funding window) — the institutional/economic framing.
- **Schema/Atlas:** the source-evidence substrate + the Atlas authority graph are where these objects land.
