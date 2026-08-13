# PĀṬALA × EXTERNAL TOOL — INTEGRATION SPEC (mapped to the current implementation)

*2026-08-13. Every external tool from the reuse-first doctrine (`tool-integration.md` + `tool-integration2.md`),
mapped to the **current Pāṭala implementation** it connects to: the contract, the seam, what Pāṭala builds, and
status. The principle: **borrow the mature tool, build only the epistemic seam.** For review.*

---

## 1. The integration map (tool → current Pāṭala module → contract → status)

| Tool | Current Pāṭala module it connects to | Contract / seam | Status |
|---|---|---|---|
| **GROBID** | `source-evidence/` witness extraction (the RO-Crate pilot's `sha256` witness) | PDF → TEI extraction **witness** (`derivation_method: grobid@ver`, `text_sha256`); feeds `pt:Witness` + Web-Annotation `SourceSpan` | adapter (S0.1) |
| **Docling** | same witness seam | non-PDF docs (DOCX/EPUB/HTML/audio) → normalized witness | adapter later |
| **AnyStyle** | GROBID reference fallback | raw citation string → structured ref → Crossref/OpenAlex | cheap win (adapter) |
| **Zotero** | `data/atlas/bibliographyTypes.ts` `BibliographyRecord` (kept unchanged) | **additive `crosswalks` field** (pt:id ↔ zotero item ↔ DOI ↔ OpenAlex); CRUD/citation/sync | adapter (S0.1) |
| **Crossref / OpenAlex** | `BibliographyRecord.crosswalks` + CorroborationEvent independence | metadata **witness** (enrichment; canonical decision stays Pāṭala, deterministic) | adapter |
| **OpenCitations** | CorroborationEvent `independence`/lineage | citation graph → "3 independent vs 3 repeating-one-scholar" | adapter (after vertical) |
| **Unpaywall** (via PaperQA) | `BibliographyRecord` rights/full-text | OA full-text discovery | adapter (via PaperQA) |
| **Tantivy (BM25)** | `patala_ml/retrieval.py` (the lexical baseline) | local full-text index over SourceSpan corpus = the independent lexical retrieval baseline | HIGH (via PaperQA) |
| **PaperQA2** | the Scholar Assistant (future) + `retrieval.py` | candidate retrieval/evidence → Pāṭala SourceSpans → SourceAssertions; Pāṭala decides what it licenses | IMMEDIATE prototype |
| **INCEpTION** | `benchmarks/v0/structure/PAT-STRUCT-*.json` (Argument Gold) + CorroborationEvents | annotation/adjudication UI → canonical gold JSON → Inspect | VERY HIGH |
| **Hypothesis** | `SourceSpan` + `ReviewEvent` | inline annotation → `ReviewProposal` → validated `ReviewEvent` | pilot |
| **Inspect AI** | `benchmarks/v0/` + the mutation tests (`test_reflexion_essay`, `test_argument_synthesis`) | the **entire benchmark runtime** — TantraFact/ArgumentBench/etc. as Inspect tasks, custom scorers + scanners, `BenchmarkRun ↔ EvalLog` | **IMMEDIATE** |
| **CRAG mock-API** | the benchmark containers | frozen corpus snapshot (mock source/bibliography/span APIs) for reproducible evals | when TantraFact v0 |
| **RO-Crate** | `source-evidence/ro_crate.py` (already built) | corpus/benchmark packaging + export | **done** (pilot) |
| **ORKG** | (patterns only) | structured-claims model reference | borrow patterns |
| **OpenReview** | the peer-review adversary (future) + `ReviewEvent` | submission/review workflow; Pāṭala exports/imports structured ReviewEvents | integrate |
| **CTS/DTS** | `pt:passage:ipvv:*` (passage identity) + the API | CTS-compatible passage identity; DTS-compatible text API | compatibility now |
| **IIIF / TEI / JATS** | `pt:Asset` + witness/extraction | IIIF assets; TEI critical editions; JATS consume-when-available | compatibility/consume |
| **S2ORC / SciAtlas / Valsci / CiteVQA** | (future modern-science + baselines) | science-side substrate + benchmark baselines/metrics | later |

---

## 2. Per-integration contracts (the key ones)

### 2.1 GROBID / Docling → witness extraction
- **Current:** `source-evidence/` builds a `pt:Witness` (sha256, path, format) — the RO-Crate pilot.
- **Add:** a `pt:extraction` witness from GROBID TEI (sections, paragraphs, coordinates) recorded as
  `derivation_method: grobid@<ver>`, `text_sha256`, `derives_from: pt:witness:<id>:file`. Same file + same GROBID →
  same extraction hash (determinism). GROBID failure affects extraction only, never erases the registered witness.
- **Pāṭala builds:** the extraction witness object + the GROBID adapter with LIVE/RECORDED/UNAVAILABLE modes.

### 2.2 Zotero → bibliography reconciliation
- **Current:** `data/atlas/bibliographyTypes.ts` `BibliographyRecord` (canonical identity + epistemic gate — kept
  verbatim).
- **Add:** optional `crosswalks?: { zotero, doi, openalex, opencitations, witness[] }` field.
- **Contract:** Pāṭala owns identity + epistemic fields (`verified`, `state`, `tier`, `translations`, `rights` enum);
  Zotero owns CRUD + citations + `since=` sync. External metadata = witness, never authority; audited
  (`verified:true`) records are immutable against external metadata. Full spec:
  `source-evidence/docs/bibliography-reconciliation-spec.md`.

### 2.3 Inspect AI → the benchmark runtime
- **Current:** `benchmarks/v0/` (MANIFEST/SCHEMA/SPLITS/METRICS, ARG-GOLD/ARG-REFERENCE fixtures) + the mutation
  tests (6 laundering classes + the k-core/louvain baseline).
- **Add:** port TantraFact / ArgumentBench / CorroborationBench / CitationBench / PāṭalaQA as **Inspect tasks** with
  custom scorers (verdict/span/attribution/scope/warrant/**false-corroboration**) + **scanners**
  (citation_laundering, scope_strengthening, unsupported_addition, benchmark_leak, gold_phrase_copying). Map
  `BenchmarkRun ↔ Inspect EvalLog`.
- **Pāṭala builds:** only the task definitions + the epistemic scorers/scanners + the datasets. **This is the
  IMMEDIATE prototype.**

### 2.4 PaperQA2 → Scholar Assistant + retrieval
- **Current:** `patala_ml/retrieval.py` (BM25/dense/hybrid) is the things-to-beat; `retrieval.py` indexes
  `PassageDoc`.
- **Add:** PaperQA2 as the candidate-retrieval engine over the scholar corpus full text → returns candidate
  SourceSpans → Pāṭala binds SourceAssertions → epistemically constrained answer. PaperQA2 finds evidence; Pāṭala
  decides what it licenses. Its local Tantivy BM25 becomes the independent lexical baseline for
  CorroborationBench.

### 2.5 INCEpTION → gold/adjudication workbench
- **Current:** the 5 Argument Gold/Reference objects (`benchmarks/v0/structure/PAT-STRUCT-*.json`) + the
  corroboration events.
- **Add:** an INCEpTION project with annotation layers (speaker/commitment/proposition/premise/inference/scope +
  Corroboration relations) → export canonical gold JSON → Inspect. Machine pre-annotation → INCEpTION review →
  Pāṭala reference object → Inspect benchmark.

### 2.6 OpenCitations → corroboration independence
- **Current:** `CorroborationEvent.independence` (SAME_AUTHOR/DERIVED_CITATION/INDEPENDENT_AUTHOR).
- **Add:** OpenCitations citation graph to disambiguate "3 independent scholars vs 3 papers repeating one scholar"
  → feeds `independence`/`lineage`. After the basic source→assertion vertical (not before).

---

## 3. The Pāṭala seam (what Pāṭala alone builds)

```
SourceAssertion · CorroborationEvent · SemanticAlignment · Proposition · Commitment · Argument ·
ArgumentAudit · Crux · ArgumentSynthesis · ReviewEvent · epistemic dependency propagation
+ Pāṭala-specific benchmark datasets/scorers/scanners · scholar UX
```
Everything else in §1 is borrowed. **The seam's acceptance criterion: replacing any external tool later must not
invalidate Pāṭala IDs or epistemic objects.**

## 4. Sequencing (do not do all at once)

```
NOW    Inspect AI (port the existing argument + corruption tests into one Inspect task — the benchmark runtime)
THEN   PaperQA2 (prototype Scholar Assistant retrieval over ~20 Ratié/Sanderson docs; steal its metadata clients)
THEN   INCEpTION (load the Argument Gold + Corroboration examples; test it as the gold/adjudication workbench)
THEN   S0.1 external-tool pilot (GROBID + Zotero + Crossref/OpenAlex → pt:source/witness/span → assertion)
THEN   F1 (false-positive-tested corroboration) → CorroborationBench → TantraFact
```
If Inspect + PaperQA2 + INCEpTION work, three custom-infrastructure categories are eliminated and Pāṭala spends
almost everything on the genuinely novel part: **can a machine preserve warranted authority through
source → interpretation → claim → argument → synthesis → review → explanation, and can we measure exactly where
it fails?**

## 5. Bibliography reconciliation (the one spec you're reviewing now)
`source-evidence/docs/bibliography-reconciliation-spec.md` — your current `BibliographyRecord` layout stays
unchanged; reconciliation is the additive `crosswalks` field + Zotero as management/citation backend, with the
merge/disagreement/sync rules and acceptance criteria. Review that doc; this §4 order assumes it's approved before
the Zotero adapter.
