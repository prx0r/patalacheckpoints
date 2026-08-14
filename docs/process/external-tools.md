# EXTERNAL TOOLS & BORROWED INFRASTRUCTURE — the canonical status board

*Part of `docs/process/README.md`. This is the permanent, organized registry of every external project
Pāṭala borrows — **what it is, whether we've wired it, where in code, and why.** The machine-readable
source of truth is `source-evidence/docs/tools/MANIFEST.json` (validated against
`MANIFEST.schema.json`). This doc is the human summary + the adapter-contract mapping.*

**The governing rule (reuse-first):** Pāṭala owns only the epistemic graph. Everything beneath it is
borrowed. If it's listed here as INTEGRATED/WIRED, use it; if PARTIAL, finish it; if DOCS_ONLY/PLANNED,
don't rebuild it — adopt it when the layer needs it.

---

## 1. The one-liner

> External world = **adapters around a very small Pāṭala kernel.** We should write dramatically less
> foundational infrastructure than it feels like. ~6 adapter contracts let ~40 projects pour data into
> the same epistemic machine.

## 2. Integration status (69 tools, 2026-08-14)

| Status | Count | Meaning |
|---|---|---|
| **INTEGRATED** | 2 | in production code path, tested |
| **WIRED** | 2 | a working adapter exists |
| **PARTIAL** | 2 | a stub / half-wired |
| **DOCS_ONLY** | 20 | documented, no live code |
| **PLANNED** | 38 | identified for adoption, not started |
| **WATCH** | 3 | audited as prior-art, not adopted |
| **NOT_USED** | 2 | documented but intentionally not used |

### INTEGRATED (proven in production)
- **Vidyut** — Sanskrit linguistic engine (segmentation, morphology, inflection, transliteration, sandhi, meter). Used in `pipeline/agentic_gloss.py`. The canonical `SanskritLinguisticAdapter`.
- **Inspect** — the benchmark runtime (datasets/agents/scorers/EvalLog). Used across `source-evidence/evals/`.

### WIRED (working adapter, may be thin)
- **Crossref** — `metadata_resolver.py::resolve_crossref`
- **OpenAlex** — `metadata_resolver.py::resolve_openalex`
- *(plus our ingestion adapters: PANDiT/GRETIL/SARIT/Wikidata/VIAF/C-SALT/NGMCP/IIIF — see §3)*

### PARTIAL (finish these)
- **GROBID** — `grobid_live.py` real; `scholar_document.GrobidAdapter.parse()` is a placeholder.
- **OpenCitations** — adapter exists; `_same_author()` hard-wired UNKNOWN.

### DOCS_ONLY (documented, adopt when the layer needs it)
docling, anystyle, zotero, unpaywall, raid, paperqa, scirrag, crag, inception (bridge only), recogito,
hypothesis, orkg, ro-crate, openreview, coar-notify, manubot, storm, valsci-sciatlas, citevqa, tei-publisher.

### PLANNED (high-value, next to adopt)
ambuda-dcs, dcs-sh-alignment, csl-orig, csl-standards, sanskrit-util, aksharamukha, buda-owl-schema,
buda-rdf-editor, inception-recommender, argdown, nanopub.

### WATCH (audited prior-art, not adopted)
vedaweb-tekst, sangrahaka, pramana-nlp.

### NOT_USED (deliberately skip)
tantivy (Postgres FTS first), s2orc (Sanskrit paper coverage ~0%).

---

## 3. The 6 adapter contracts (the real integration skeleton)

All borrowed projects map onto ~6 contracts. We already have the skeleton:

| Contract | Adapters (built) | Purpose | Status |
|---|---|---|---|
| **Text corpus** | `GretilAdapter`, `SaritAdapter`, Muktabodha | TEI/IAST → TextInstance → Work | ✅ built |
| **Metadata/entities** | `PanditBulkAdapter`, `NgmcpAdapter` | entities → Work/Person/Manuscript | ✅ built |
| **Identity crosswalk** | `WikidataAdapter`, `ViafAdapter` + ORCID/ROR | external IDs → canonical IDs | ✅ built |
| **Linguistic** | Vidyut (via `agentic_gloss.py`) | token/lemma/morphology on passages | ✅ integrated |
| **Lexical** | `CSaltAdapter` (C-SALT) | dictionary evidence → LexicalSense | ⚠️ built, CSL-orig pending |
| **Manuscript/IIIF** | `IiifAdapter` | witness images → Surrogate | ⚠️ built, no live manifests |

---

## 4. How to read the manifest

```bash
# validate the manifest against its schema
python3 -c "import json,jsonschema; \
  s=json.load(open('source-evidence/docs/tools/MANIFEST.schema.json')); \
  m=json.load(open('source-evidence/docs/tools/MANIFEST.json')); \
  jsonschema.validate(m,s); print('VALID', len(m['tools']), 'tools')"
```

Each tool entry:
```json
{
  "category": "...",       // parsing/bibliography/.../linguistic/lexical/ontology/identity/argument/publishing
  "borrow": "...",         // what Pāṭala takes from it
  "license": "...",        // license firewall
  "docs_url": "...",       // canonical docs
  "repo": "...",
  "local_doc": "...",      // source-evidence/docs/tools/<tool>.md
  "docs_cache": "...",     // offline docs
  "status": "INTEGRATED|WIRED|PARTIAL|DOCS_ONLY|PLANNED|WATCH|NOT_USED",
  "used_in": ["..."],      // concrete code paths (file:line / module)
  "notes": "..."           // how/why / caveats
}
```

---

## 5. The doctrine for every borrowed tool

1. **Adapter, never canonical schema.** Pāṭala-native objects (Argument, Claim, EvidenceUse,
   TranslationChoice, Crux, Adjudication) stay ours; external ontologies are crosswalks.
2. **External IDs are crosswalk identifiers, never canonical identity.**
3. **Borrow, don't rebuild.** If it's in the manifest, adopt it — don't reimplement it.
4. **Rich-native-first, standards-adapters-outward** (validated by csl-standards' own findings).
5. **License firewall** — record license on every imported object; never treat NC/restricted data as unrestricted commercial.

---

## 6. Highest-value next steps (from the research + audit)

1. **Ambuda DCS** → ingest 650k annotated sentences (corpus linguistic priors). [PLANNED]
2. **csl-orig** → the lexical evidence graph (45 dictionaries). [PLANNED]
3. **BDRC owl-schema** → Person/Work/Instance crosswalk reference (esp. PANDiT layer). [PLANNED]
4. Finish **GROBID** + **OpenCitations** PARTIAL stubs.
5. Adopt **nanopub** as the assertion-publication adapter once assertions are real.

> Don't build all 15 at once. Build the 6 contracts solid (done), then adopt per-layer need.
