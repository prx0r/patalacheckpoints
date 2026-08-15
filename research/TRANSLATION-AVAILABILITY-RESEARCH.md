# PĀṬALA TRANSLATION-AVAILABILITY RESEARCH — the compiled corpus map

*2026-08-15. The consolidated research for building the **translation-availability index** — the
greenfield layer ("for text X, which translations exist (full/partial, who, edition-base, license),
where they live, and which are missing") nobody has built for Sanskrit. This compiles: the two
deep-research reports (REPORT-15, REPORT-16), the web-verified new-source survey, the external-API
polite-usage reference, and how it all maps to our openpatala pipeline.*

---

## 0. THE THESIS (why this is the product)

> **Nobody indexes Sanskrit translations.** The clean-text sources are solved (Muktabodha/GRETIL/SARIT/
> DCS). What's missing is the *translation-availability layer*: which translations exist, in which
> language, who, on what edition-base, under what license, where they live, and which are missing.
> SuttaCentral built this for the finite Buddhist canon; the Sanskrit "Hindu" corpus is open-ended +
> multi-recension + no canonical text-ID, so it must be built on top of **our text-identity layer**
> (the atlas). That's the product. We already shipped the core: `translation_availability.py` +
> `translation_locator.py` (multi-API live).

---

## 1. THE TWO REPORTS (what they cover)

### REPORT-15 — Sanskrit Text Repositories: Survey & Analysis
A 20-repo comparative survey (custodian/scope/size/languages/access/formats/metadata/reliability).
Key conclusions:
- **Bulk-download sources:** Internet Archive, DLI/OUDL mirrors, Muktabodha.
- **Authoritative/citable:** Muktabodha, IFP/EFEO, IGNCA/ASI, CSU, GRETIL, Sanskrit Library.
- **Translation gap:** *no repository tracks "which translations exist"* — all are text/scan stores.

### REPORT-16 — Repositories + Programmatic Adapters + Search Strategies
The actionable companion: prioritized crawl list, GitHub/archive target names, the "hidden translation
evidence" playbook, search strategies, and a Top-30 source comparison (translation-yield × harvest-ease)
+ a phased implementation roadmap.
Key highlights:
- **Hidden translation evidence** lives in: PhD theses (Shodhganga), scanned-book footnotes (DLI),
  commentary volumes, personal sites, journals, and Crossref/OpenAlex abstracts.
- **Search strategies:** transliteration variants (IAST vs Latin vs Devanāgarī), incipit matching,
  OCR fuzzy matching, citation-chasing, regex near "transl."/"English".
- **Top-30 yield×ease leaders:** Google Books, Internet Archive(DLI), HathiTrust, OpenAlex, Crossref.

---

## 2. THE SOURCE LANDSCAPE (verified, consolidated)

### 2.1 The clean-text sources we ALREADY ingest (the anchors)
| Source | Size | Machine-readable | License | Status |
|---|---|---|---|---|
| **Muktabodha** | 3,000 texts / 570 e-texts | ✅ TEI/HTML | CC BY-NC 4.0 | ✅ on R2 (499 files) |
| **GRETIL** | thousands (90GB) | ✅ Unicode | mixed | ✅ on R2 (784 TEI) |
| **SARIT** | ~85 TEI | ✅ XML/EPUB | open CC | ✅ on R2 |
| **PANDIT** | 13,695 works | ✅ CSV | CC BY-NC-SA | ✅ on R2 |
| **OliverHellwig DCS** | 650k sentences | ✅ CoNLL-U/JSON | CC | cloned |
| **Ambuda DCS** | 14 works cleaned | ✅ token+POS | CC-BY 4.0 | cloned |

### 2.2 NEW translation-source additions (from the web-verified survey — added to `resources.ts`)
| Source | URL | What it gives | Added |
|---|---|---|---|
| **Shivashakti Mandalam** | shivashakti.com | deep free tantric-translation archive (PDF) | ✅ |
| **Sacred-Texts.com** | sacred-texts.com | big PD English translation trove (SBE etc.) | ✅ |
| **IFP OpenEdition (+EFEO)** | books.openedition.org/ifp | authoritative critical editions w/ translations | ✅ |
| **archive.org Indological** | archive.org | bulk PD scholarly scans | ✅ |
| **Granth Sañjīvanī** | granthsanjeevani.com | 2000+ manuscripts, high metadata | ✅ |
| **IGNCA/ASI** | ignca.gov.in | 2000+ scanned Indology books | ✅ |
| **Brown Sanskrit Library** | sanskritlibrary.org | morphologically-tagged scholarly texts | ✅ |
| **DLI/OUDL mirrors** | dli.sanskritdictionary.com | bulk PDF scans | ✅ |
| **Central Sanskrit Univ** | sanskrit.nic.in | Purāṇas/grammar PDFs | ✅ |
| **e-BharatiSampat** | ebharatisampat.in | Sanskrit **with parallel translations** | ✅ |

### 2.3 High-value sources from REPORT-16 to still consider
| Source | Translation yield | Harvest ease | Notes |
|---|---|---|---|
| **Google Books API** | High | Moderate (key) | broad scans, OCR search |
| **HathiTrust** | High | Medium (partnership) | ~100k Sanskrit volumes |
| **Shodhganga** | High (theses) | Medium (OAI) | PhD theses translate passages |
| **NDLI** | Medium | Medium (API) | national aggregation |
| **CORE** | Low-Med (OA papers) | High (key) | Indology/translation papers |
| **GitHub GRETIL-mirror** | High (e-texts) | High (Zenodo DOI) | full GRETIL on GitHub |
| **archive.org in.ernet.dli.*** | High | High | DLI scans on archive |

---

## 3. THE "HIDDEN TRANSLATION EVIDENCE" PLAYBOOK (from REPORT-16)

Translations often hide in non-obvious places. The finder should look for:
1. **PhD theses** (Shodhganga) — translate sample verses + survey prior translations in footnotes.
2. **Scanned-book footnotes/introductions** (DLI, Granth Sañjīvanī) — colonial-era editions translate
   stanzas in English/Hindi; OCR-search "translation"/"meanings".
3. **Commentary/edition volumes** (Muktabodha/CSU) — critical editions include parallel translations.
4. **Personal scholar sites** (SanskritDocuments, Indology lists) — translation snippets.
5. **Journal articles** (BORI, JIP, Saṃskṛta Racanā) — translated passages.
6. **Crossref/OpenAlex abstracts** — English abstracts often quote translations.

---

## 4. THE EXTERNAL-API LAYER (polite consumption — see `research/api-docs/API-USAGE-REFERENCE.md`)

| API | Our use | Polite rule | Status |
|---|---|---|---|
| **OpenAlex** | resolve → `locations[]`/`oa_url`/`open_access` | `mailto` → polite pool, 0.3s sleep | ✅ WIRED |
| **Crossref** | resolve → DOI/venue | UA + 0.3s sleep | ✅ WIRED |
| **Unpaywall** | DOI → OA download URLs | `email` required | ✅ WIRED (new) |
| **archive.org** | search scans/editions | ≥1s sleep, UA | ✅ WIRED (verify_editions) |

**Our code contract:** every request carries `User-Agent: patala-scholar-resolver/0.1 (mailto:dev@patala.local)`,
sleep between providers, fail-closed (UNAVAILABLE/NOT_FOUND valid), record `fetched_at` provenance.

---

## 5. WHAT WE BUILT THIS SESSION (the working layer)

| Artifact | What it does | Verified |
|---|---|---|
| `pipeline/translation_availability.py` | per-work: which translations exist (full/partial/missing), languages, urls, copyright, factory state | 11/11 PASS (254 works, 60 EN, 192 untranslated) |
| `pipeline/translation_locator.py` | live multi-API: OpenAlex locations + Crossref DOI + Unpaywall OA downloads, merged into curated availability | 10/10 PASS |
| `metadata_resolver.py` (extended) | added `resolve_unpaywall` + OpenAlex `locations`/`oa_status`/`oa_url` | tested live |
| `data/atlas/resources.ts` | +8 new sources (31→38) from the survey | valid |
| `research/api-docs/` | polite-usage reference + raw docs | written |
| `research/REPORT-15/16` | the raw source reports | saved |

### Live test results (real data)
- **kiranatantra**: curated = partial English (Goodall) + complete Italian (Vivanti); live OpenAlex
  resolved → DOI `10.1080/02666030.2014.892371` + a location (architexturez.net); Unpaywall NOT_OA.
- **spandapradipika**: curated = **missing**; live resolved a *related scholarly record* (EBSCO +
  ci.nii) → correctly flags "check if a translation" (anti-theatre, no overclaim).

---

## 6. THE IMPLEMENTATION ROADMAP (from REPORT-16, aligned to our stack)

```
PHASE 1  Core adapters      — OpenAlex/Crossref/Unpaywall/archive.org   ✅ DONE (locator)
PHASE 2  Content harvest    — Muktabodha/GRETIL on R2 ✅; SanskritDocuments/eBooks, Shodhganga OAI
PHASE 3  Extended sources   — DLI/Hathi OCR text, NDLI, IndCat/WorldCat, journals, personal sites
PHASE 4  Search & QA        — fuzzy OCR + incipit search, transliteration variants, citation heuristics
PHASE 5  Integration        — unified translation-availability DB → served on the atlas API → site
```

---

## 7. THE FILE MAP

| File | What |
|---|---|
| `research/REPORT-15-REPOSITORIES.md` | the 20-repo survey (raw) |
| `research/REPORT-16-REPOSITORIES-ADAPTERS.md` | the adapter/crawl/search roadmap (raw) |
| `research/SANSKRIT-REPOSITORIES-SURVEY.md` | first copy of report 15 |
| `research/api-docs/API-USAGE-REFERENCE.md` | polite API consumption rules |
| `pipeline/translation_availability.py` | the curated availability index |
| `pipeline/translation_locator.py` | the live multi-API locator |
| `data/atlas/resources.ts` | the 38-source register |

---

*The translation-availability index is real: curated (254 works) + live (multi-API) + a 38-source map +
a polite-API contract. This compiles the research that grounds it. The next phase is wiring it into the
atlas `/works/{id}` response so the site displays "which translations exist + where + which are missing"
per work.*
