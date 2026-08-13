# Global Access, Rights & Ecosystem — Open-Reference, Controlled-Corpus

*2026-08-13. The canonical access/rights/ecosystem strategy for Pāṭala. Complements
`docs/global/globalpartnerships.md` (who we partner with and why) and the Atlas/identity layer.
This doc is the **access-control and rights model**: what is public, what is controlled, and how the
ecosystem position ("OpenAlex-for-Sanskrit") becomes **publicly discoverable, privately deep**.*

---

## The clean ecosystem position

> **Pāṭala is the trusted reconciliation, provenance, and scholarly verification layer for Sanskrit —
> not the free bulk-download layer.**

You can hold a strong ecosystem role **without exposing the whole corpus through a public API**. The
durable moat is not "nobody knows our facts"; it is "everybody depends on our resolution and provenance."

The public identity we state:

> **Pāṭala provides persistent identities, provenance, and scholarly resolution for Sanskrit texts,
> manuscripts, editions, interpretations, and arguments. We connect existing collections rather than
> replace them.**

That tells IFP, Muktabodha, GRETIL and PANDiT that Pāṭala is **complementary**, not extractive.

---

## The four value props to institutions

1. **Discovery** — connect their manuscripts, editions, and scholars to the wider Sanskrit graph so
   their holdings become easier to find and cite.
2. **Identity resolution** — reconcile duplicate titles, variant author names, manuscript shelfmarks,
   editions, and cross-database records.
3. **Provenance + correction history** — turn uncertain catalogue metadata into explicit, reviewable
   scholarly assertions instead of silent database fields.
4. **Scholar tooling** — better interfaces for comparison, transcription, translation review,
   manuscript linking, argument mapping, and publication.

**The institutional bargain** (for IFP, Muktabodha, PANDiT, NGMCP, BORI, etc.):

```text
THEY CONTRIBUTE                    PĀṬALA RETURNS
────────────────────               ─────────────────────────────
manuscript metadata                cross-database reconciliation
catalogue records                  canonical Pāṭala IDs
text instances                     linked bibliography
scholarly corrections              manuscript ↔ work ↔ edition mapping
stable source identifiers          citation/export records
                                   error reports
                                   scholar attribution
                                   better discovery pages
                                   review infrastructure
```

---

## Asymmetric openness

Make public:

```text
PATA-W-000128
  canonical title: Tantrasadbhāva
  aliases, authors, date range, tradition
  external IDs
  known manuscripts: 14
  known editions: 3
  known translations: 1
```

But not expose:

```text
full normalized corpus
full passage graph
all translations
all scholarly adjudications
all embeddings
bulk training dump
complete argument graph
download-everything endpoint
```

**Public surface = an index and citation infrastructure, not a model-training corpus.**

---

## The four access layers

```text
L0 — OPEN IDENTITY LAYER
  stable IDs · canonical names · basic relations
  external crosswalks · citation metadata

L1 — PUBLIC DISCOVERY
  web pages · search · timelines · institution pages
  manuscript discovery · limited snippets

L2 — PARTNER/SCHOLAR ACCESS
  full records · provenance · comparison tools
  manuscript linking · review queues · controlled API

L3 — PĀṬALA CORE
  full text · translations · argument graph · embeddings
  adjudication corpus · training/evaluation datasets · internal machine interfaces
```

This is better than "no API." A completely closed system can't become infrastructure; a public bulk
API makes the most valuable dataset trivial to copy. **Expose identifiers and interfaces, not the whole
asset.**

The OpenAlex analogy shifts: OpenAlex's value is radical openness; Pāṭala's value is **canonicality and
trust** — think ORCID + Crossref + JSTOR + Wikidata + scholarly-edition infrastructure combined.

People should ask **"What is the Pāṭala ID for this work?"** not **"How do I download Pāṭala's dataset?"**

---

## The identifier is the highest-value ecosystem product

```text
https://patala.org/work/PW0000182     ← the durable record for a Sanskrit work
```

cross-referencing PANDiT · GRETIL · SARIT · Muktabodha · NGMCP · Wikidata · VIAF · OpenAlex · DOIs ·
IIIF manifests. Institutions can place the Pāṭala ID in their own catalogues — network effect without
giving away the corpus.

**Free resolution service** (constrained responses, no underlying corpus leak):

```text
resolve(title="Tantrasadbhāva", author=?, shelfmark=?, opening_words=?)
  → PATA-W-000182
  match: probable
  confidence: 0.94
  candidate aliases: [...]
```

---

## The strongest partner offer: "we improve your catalogue"

If IFP gives 8,000 records, Pāṭala returns:

```text
1,430 title normalizations
812 probable duplicate identities
329 author-name reconciliations
126 work-identification conflicts
73 manuscript/edition mismatches
2,881 external bibliography links
1,024 newly linked digital texts
```

The partnership is **not extractive** — you give them cleaner metadata + new scholarship.

```text
PANDiT:    their graph + Pāṭala textual evidence + our reconciliation machinery = better records
Muktabodha: their corpus + Pāṭala work identities + edition/manuscript/bibliography links = richer discovery
NGMCP:     catalogue manuscript + Pāṭala text matching = candidate work identification
```

---

## Scholar attribution as a lever

Every correction generates a persistent, citable record:

```text
Assertion A92821
  proposed by: Scholar X · institution: EFEO · ORCID: 0000-....
  evidence: MS 137 fol. 24r · Article DOI: ...
  reviewed by: Scholar Y · status: ADJUDICATED
```

Pāṭala gives scholars a **persistent contribution record**:

```text
Dr X — Pāṭala profile
  37 manuscript identifications
  18 textual corrections
  12 adjudicated translations
  6 argument reconstructions
  183 reviewed assertions
```

Institutions get visible credit too. Far more compelling than "annotate our database for free."

---

## Protecting against AI extraction

Do **not** rely on "no API = safe." Public web content can still be crawled. Protect the scarce layer
with multiple boundaries:

```text
Public HTML:          metadata + limited passages
robots / crawler:     explicit restrictions (allow search bots, deny harvest)
authentication:       for deeper material
rate limits:          prevent bulk harvesting
partner API keys:     institution-specific scopes
signed URLs:          for protected assets
query limits:         no corpus enumeration
exports:              reviewed/requested datasets only
licensing:            explicit machine-learning terms
audit logs:           know who accessed what
```

**Critical: do not put your highest-value derived corpus into client-side JavaScript.** If the browser
downloads `all_arguments.json` / `all_translations.json` / `all_embeddings.json`, you have effectively
published it. Keep the core server-side.

---

## Don't overprotect basic metadata

The open-commons metadata must be freely copyable — this is adoption:

```text
Pāṭala ID · canonical title · aliases · author · approximate date
external identifiers · basic bibliography
```

Success means Wikidata, libraries, scholars, Wikipedia, datasets and AI systems **repeat your IDs**.

The moat is not "nobody knows our facts." The moat is "everybody depends on our resolution and provenance."

---

## The access model (publicly discoverable, privately deep)

```text
                    PUBLIC COMMONS
            identities + crosswalks + canonical citations
                    │  free
                    ▼
               PĀṬALA IDS
        ┌───────────┼───────────┐
        ↓           ↓           ↓
    libraries   scholars    public
        │           │
        └─────┬─────┘
              ↓
        contributed evidence
              ↓
     ┌───────────────────────────┐
     │       PĀṬALA CORE         │
     │  provenance · reconciliation
     │  passages · translations   │
     │  arguments · adjudications │
     │  embeddings                │
     └───────────┬───────────────┘
                 │ controlled interfaces
          ┌──────┼──────┐
          ↓      ↓      ↓
      partner scholar commercial AI
       API   workbench   licensed
```

**Economics:** Public = free identity/discovery. Scholars = free or subsidized workbench. Institutions =
reciprocal partnerships. Commercial AI = paid licensing/access. If AI labs want "the adjudicated Sanskrit
corpus with passage provenance and expert-reviewed interpretations," they **license** a dataset /
evaluation suite / retrieval endpoint / controlled tool — not `/dump.json`.

---

## Three constituencies, three access modes

### Public / AI discovery (unusually good)
Every important entity gets a permanent, server-rendered page:

```text
patala.org/work/ipk            patalala.org/person/utpaladeva
patala.org/concept/pratyabhijna patala.org/manuscript/...
patala.org/tradition/krama     patala.org/institution/ifp
```

High-quality enough that ChatGPT/Perplexity/Google cite Pāṭala as an obvious source. A work page might
expose:

```text
canonical title · Sanskrit title · aliases · author/attribution · approximate date · tradition
short description · known editions · known manuscripts · major translations · major scholarship
basic relationships · external IDs · Pāṭala ID · citation · selected evidence/snippets
```

That is a lot of useful information — it just isn't the entire machine-readable research asset.

### Scholar / institutional layer (opposite philosophy)
Authenticated scholars and partners get essentially complete access — otherwise they won't adopt it as
their working environment. Verified scholar: full texts (where rights permit), complete translations,
variant readings, manuscript images (where partner permissions permit), full provenance + argument
graph, evidence, competing interpretations, review history, reconciliation tools, bulk scholarly exports,
research API, MCP/tools, annotation environment.

**Don't charge scholars for access to the knowledge they are helping create.** The exchange:

```text
Pāṭala gives scholar:  tools + corpus + visibility + attribution + infrastructure
Scholar gives Pāṭala:  judgment + corrections + connections + scholarship
```

### Commercial machine access (restrictive)
Distinguish the economic events:

```text
HUMAN SCHOLAR ACCESS         very permissive
INSTITUTIONAL INTEROPERABILITY  permissive + contractual
PUBLIC SEARCH               rich but bounded
AUTOMATED BULK ACCESS       controlled/licensed
COMMERCIAL ML / TRAINING    licensed
```

---

## What should ChatGPT actually see?

Plenty — the conclusions, not the database:

```text
Īśvarapratyabhijñākārikā · Pāṭala Work ID: PW000381
  Author: Utpaladeva · Date: c. 10th century CE · Tradition: Pratyabhijñā / nondual Śaivism
  Description, textual relationships, known editions/translations, manuscript witnesses: 18 indexed
  Research status: 3 identifications disputed, 12 relationships scholar-reviewed
  Key concepts: recognition · consciousness · memory · agency
```

But the HTML does **not** contain the transcriptions, complete translation, every extracted proposition,
private comments, alignment pairs, evidence graph, embeddings, or training JSONL.

**Architectural rule: give search engines the conclusions, not the database.**

```text
Public:  "Pāṭala currently records 18 known witnesses."
Protected: the underlying normalized witness dataset + matching data + scholarly reasoning.

Public:  "The relation of Krama to Trika is complex; Abhinavagupta incorporates important Krama materials…"
Protected: every source passage, evidence object, annotation, inference, disagreement.
```

---

## Public dossiers (a publication pipeline, not an API)

For every Work / Person / Concept / Tradition / Manuscript, produce a **canonical public dossier**
(`/work/tantraloka`, `/concept/vimarsa`, `/person/abhinavagupta`, `/tradition/krama`) written for
Google / ChatGPT Search / Perplexity / researchers / students / Wikipedia editors / readers — but
**generated from the deeper graph**:

```text
PRIVATE/CONTROLLED GRAPH → verified claims → PUBLIC DOSSIER → web → Google / ChatGPT / humans
```

Because every public claim derives from the evidence system
(`public statement → Pāṭala assertion → evidence → edition → Sanskrit`), public pages are unusually
trustworthy — more citable than SEO sludge.

---

## Institution pages are first-class (Atlas V2)

Not merely `Institution { name }` — actual institutional hubs:

```text
/institution/ifp · /institution/efeo · /institution/muktabodha · /institution/bodleian
  collections · manuscripts · works represented · digital resources
  scholars · projects · publications · Pāṭala contributions · external catalogue
```

A manuscript page identifies the **custodian** prominently:

```text
Custodian: French Institute of Pondicherry
Source record: IFP catalogue
Digital surrogate: IFP / partner
Pāṭala enrichment: work resolution · related editions · bibliography · passage correspondences
```

Pāṭala becomes a **traffic and attribution multiplier**, not a data thief. Institutions want to say
"See our Pāṭala collection."

---

## Scholar pages

```text
patala.org/scholar/isabelle-ratie
  Research areas · Publications indexed
  Pāṭala contributions: 47 reviewed claims · 13 textual identifications · 6 adjudicated interpretations
```

Makes scholars' expertise **more visible in the AI information ecosystem** rather than silently absorbed.

---

## The long-term social contract

### Public knowledge
Canonical identifiers, discovery metadata and reviewed high-level scholarship freely accessible + linkable.

### Scholarly commons
Qualified researchers and partner institutions receive deep access for legitimate scholarship.

### Attribution
Every substantive contribution remains attributable to its source, institution and contributor.

### Custodianship
Pāṭala does not pretend to own manuscripts or editions held by partners.

### Machine exploitation
Bulk commercial reuse and model training require explicit permission/licensing.

---

## Crawlers / access paths (technical)

```text
/public/*    OAI-SearchBot → YES        /scholar/*   authenticated
/work/*      OAI-SearchBot → YES        /corpus/*    authenticated
/person/*    OAI-SearchBot → YES        /export/*    authenticated
/concept/*   OAI-SearchBot → YES        /training/*  NO
/api/internal/* → NO
```

Distinguish search discovery (allow **OAI-SearchBot**) from other automated crawling. OpenAI's current
guidance: allowing OAI-SearchBot makes pages eligible for ChatGPT Search summaries/snippets/citations;
if it cannot crawl, ChatGPT may still know the URL/title via third-party search but won't summarize.

---

## The governing rule

> **Open what increases network effects. Control what increases extractability.**

Better than "closed": Pāṭala is **open-reference, controlled-corpus**.

```text
             OPEN                       │ increasingly controlled
IDs · citations · entities              │ complete texts
basic metadata · public dossiers        │ complete translations
selected passages                       │ apparatus · private manuscripts
institution attribution                 │ full evidence · reviews
scholar attribution                     │ argument graphs · alignment data
external crosswalks                     │ embeddings · bulk exports
                                        ▼
                                   CONTROLLED
```

And a strategic consequence: **Atlas itself should largely be public** — it is the map by which the rest
of the world (including AI search) learns Pāṭala exists. The extremely deep objects hanging underneath
Atlas are where access control begins.

---

## Relation to existing docs

- **`docs/global/globalpartnerships.md`** — the integration/identity-layer strategy (who we partner with).
  This doc is the **access/rights model** (what's public vs controlled).
- **`docs/vision/atlas/technical-architecture-v1.md`** — the Atlas is largely public; deep objects
  beneath it are where access control begins.
- **`docs/global/agent1atlas.md`** — Atlas owns identity/persistence.
- **`docs/vision/vision-10-market-entry-and-partnerships.md`** — go-to-market / funding / legal/IP.
- **`docs/endgame2.md`** (Tantra Hub), **`docs/endgame3.md`** (multi-interface), **`docs/endgame4.md`**
  (economics) — the institutional/economic framing.
- **Access-control implementation:** the API/MCP layer (`app/api`, `mcp/index.mjs`) + crawler policy.
