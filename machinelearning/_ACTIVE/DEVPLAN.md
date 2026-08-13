# PĀṬALA — DEV PLAN (revision 5: Agent 1 closed out; the scholar corpus is the oracle)

*2026-08-13. The single authoritative execution plan. **Revision 5 makes the strategic correction that closes
the "waiting for a human" dead end:** we do not need a live Sanskrit specialist on call — we already own
thousands of pages of published human Sanskrit scholarship (the Ratié cluster, Torella's IPK edition, the full
*Le Soi et l'Autre*, Dyczkowski, Bäumer, and the entire **Sanderson corpus** in `data/corpus/sources/sanderson/`
+ `source-material`). Corroborating our reconstructions against these scholars IS the human gate, and it needs
no live reviewer. Governed by `AGENTS.md` + `AGENTS-DOCTRINE.md` + `CLAIMS.md`.*

---

## 0. WHERE WE ARE (Agent 1's architecture is DONE and closed out)

The Pāṭala Review vertical is complete, validated, and peer-review-clean *relative to the current objects*,
pushed on `origin/agent1-argument-layer-a1b`:

```
source → propositions → local arguments → ContextualArgumentAudit (Nyāya ACTIVE)
  → ArgumentSynthesis → monotone EO → essay → SentenceEvidenceAudit
  + deterministic k-core / Louvain structural baseline (P-019 v2)
```

**The architecture is established. The content is not yet scholar-corroborated, and automatic argument
construction is not built.** Those are the real forward tasks, and neither needs a live human.

## THE STRATEGIC CORRECTION (revision 5)

The earlier docs repeatedly gated the argument layer on "human specialist review." **We do not need a live
reviewer on call for corroboration.** Published scholarship is **Pāṭala's scalable external scholarly evidence
oracle**: it can promote sufficiently matched claims/reconstructions to `SCHOLARLY_CORROBORATED` without a live
reviewer. **But corroboration is NOT review or adjudication of Pāṭala's exact object** — Sanderson supporting a
proposition in a paper does not mean he inspected our exact premise decomposition, commitment labels, inference
edges, scope, or reconstruction warrant. So:

> **Published scholarship is Pāṭala's scalable scholarly corroboration oracle. It can promote matched claims to
> `SCHOLARLY_CORROBORATED` without a live reviewer. It does NOT constitute review or adjudication of Pāṭala's
> exact object.**

### Two separate axes (never merge into one scalar)
```
EVIDENCE_STATUS (corroboration)      REVIEW_STATUS (review of this exact object)
  MACHINE_PROPOSED                       NOT_REVIEWED
  ENGINEERING_VALIDATED                  INDEPENDENT_REVIEWED   (a live human on our object — reachable
  SCHOLARLY_CORROBORATED                                             only for select cruxes, not all)
  SCHOLARLY_CORROBORATED_MULTI_SOURCE
  SCHOLARLY_CONTESTED
  UNDERDETERMINED
```
Coherent combos: `evidence_status=SCHOLARLY_CORROBORATED` + `review_status=NOT_REVIEWED`; or
`evidence_status=UNDERDETERMINED` + `review_status=INDEPENDENT_REVIEWED` (a reviewer may conclude the evidence is
underdetermined). Human scholars become scarce adjudicators for **novel claims, conflicts, high-impact cruxes,
source uncertainty, new translations, machine-vs-scholar disagreement** — not rubber-stamps on every object.

### Corroboration is a first-class event, proposition-by-proposition, with a hard protocol
Do NOT corroborate a whole argument because one scholar passage resembles its conclusion, and do NOT accept
"something vaguely similar in Sanderson → declared scholar-corroborated" (that would be the scholarly analogue of
the semantic-paraphrase problem). A `CorroborationEvent` is required per proposition:

```json
{
  "corroboration_id": "CORR-...",
  "target_ref": "ARG-GOLD-004:G4-CONC",
  "source_ref": "SCHOLAR:...",
  "source_locator": {"page": 123, "span": "..."},
  "relation": "DIRECT_SUPPORT",
  "scope": "PROPOSITION",
  "semantic_relation": "CONSERVATIVE_PARAPHRASE",
  "independence": "INDEPENDENT_AUTHOR",
  "method": "MACHINE_MATCHED_HUMAN_SOURCE",
  "review_state": "MACHINE_VERIFIED_MAPPING",
  "defeaters": []
}
```
- **`relation`** ∈ {DIRECT_SUPPORT, DIRECT_CONTRADICTION, PARTIAL_SUPPORT, BACKGROUND_CONTEXT, ALTERNATIVE_READING,
  SAME_TERM_DIFFERENT_CLAIM, IRRELEVANT} — only the first few affect epistemic status.
- **Weakest-governs per proposition then per argument:** `status(ARG) = min(status(load-bearing deps))`. Premises
  corroborated + warrant unresolved ⇒ argument stays UNRESOLVED, not SCHOLARLY_CORROBORATED.
- **Preserve disagreement:** Ratié+Torella support A, Sanderson suggests B ⇒ keep three events, target becomes
  `SCHOLARLY_CONTESTED` or `SCHOLARLY_CORROBORATED with active defeater` — never averaged.
- **Independence classes:** track `SAME_AUTHOR / DERIVED_CITATION / INDEPENDENT_AUTHOR / INDEPENDENT_TEXTUAL_ANALYSIS /
  PRIMARY_EDITION`; never count raw source count as support strength (Ratié paper A + Ratié book B + paper citing
  Ratié is not three independent witnesses). Model `EvidenceSource{author_id, publication_id, derives_from[]}`.

ARG-002's five propositions were already promoted to `SCHOLARLY_CORROBORATED_PRELIMINARY` this way.

### The scholar oracle (all on disk — the "what more do we need" answer: nothing)

| Scholar / corpus | Where | What it corroborates |
|---|---|---|
| **Sanderson corpus (the entire thing)** | `data/corpus/sources/sanderson/` (`sanderson_manifest.json` = 53 works; `Saivism_and_the_Tantric_Traditions_Festschrift_fulltext.txt`; `academia_bundles/consolidated/` = 213 PDFs; `saiva_exegesis_kashmir.txt`; `encyclopedia_of_religion_1987.txt` [Krama/Trika/Abhinavagupta]) | cross-work Śaiva doctrine, Krama/Trika, the argument layer, dating/tradition |
| **Ratié cluster (31 papers)** | `sanskritree/corpus/ipvv-anchor/scholarship/` + the full *Le Soi et l'Autre* (`research-library/recognition/books/`) | the recognition/reflexivity argument — the "I", vimarśa, reason/scripture, proof-of-God |
| **Torella IPK edition + Ajaḍapramātṛsiddhi** | `sanskritree/.../primary/torella_ipk.txt` + `muktabodha-lib/` | the primary text, the vikalpa/self-luminous analysis |
| **Dyczkowski / Bäumer** | `source-library/tantra/` + `ochema2/sleepyshorts/baumer-*` | Tantrāloka doctrine, accessible scholarship |

The mapping of which scholar/page corroborates which gold proposition is already in
`benchmarks/v0/corroboration/SCHOLAR-SOURCE-MAP.md`.

---

## 1. THE FORWARD PLAN (in order)

**Revised order (the coordinator's directive):** F1 is deceptively huge without a stable scholarship substrate.
Before "corroborate ARG-001/004/005," we need **Phase S0 — the Scholar Corpus Foundation**: a generic, agnostic
`source-evidence/` substrate that turns "hundreds of PDFs + folders + filenames + maybe page numbers" into a
**provenance-addressable evidence corpus** (stable, citable, deduplicated, resolvable). Otherwise F1 would
recreate the exact provenance problem Pāṭala is built to solve.

```
Agent 2 factory reliability
   ↓
S0  scholar-corpus vertical (source-evidence substrate)
   ↓
stable scholarly source IDs / spans / assertions
   ↓
F1  corroboration experiment
   ↓
scale scholar ingestion
   ↓
scale argument packs
   ↓
extractor
```

---

## 1a. S0 — SCHOLAR CORPUS FOUNDATION (`source-evidence/`) — the substrate BEFORE F1

### Do NOT build a new ontology — compose a Pāṭala Source Evidence Profile v0 (schema stack)
Most of the generic substrate already exists, distributed across standards. The high-value move is an **application
profile** that composes them and adds only the epistemic objects none provide:

| Pāṭala requirement | Reuse |
|---|---|
| bibliographic conceptual identity | **FaBiO** (`pt:BibliographicWork` profile of fabio Work/Expression; `pt:Witness` = fabio Manifestation/Item) |
| library interoperability | **BIBFRAME** adapter (Work→Instance→Item) |
| DOI/ISBN metadata + enrichment | **DataCite / Crossref / OpenAlex** (metadata *witness*, never canonical identity — canonical = stable `pt:*` id) |
| local/remote file packaging | **RO-Crate** (export/interchange, NOT the DB) |
| provenance / derivation | **PROV-O** (Entity/Activity/Agent; wasDerivedFrom/used/wasGeneratedBy/wasAttributedTo) |
| exact source spans | **W3C Web Annotation** (SpecificResource + multiple selectors: TextQuote/TextPosition/HumanPage + Pāṭala hash selectors) |
| publication citation semantics | **CiTO** (for publication→publication citations; Pāṭala epistemic relations stay native) |
| images / pages / manuscripts / assets | **IIIF Presentation** (Manifest→Canvas→Annotations; make the object model IIIF-compatible from the start) |
| critical editions / textual variants | **TEI** (a specialized projection, not the registry backend) |
| atomic assertion publishing | **Nanopublication** adapter (SourceAssertion/CorroborationEvent export) |
| **evidence + argument epistemology** | **Pāṭala native** (SourceAssertion, CorroborationEvent, review/authority state, dependency propagation) |

The architecture boundary:

```
FaBiO/DataCite/OpenAlex → Bibliographic Identity → Manifestation + Agent(PROV) → Witness
        → Web Annotation (Span) + IIIF (Asset)
═══════ PĀṬALA BOUNDARY ═══════
SourceAssertion → CorroborationEvent → Proposition → Argument → Synthesis → Essay/Education/API
```

### The object model (the profile's internal shape — mapped to the standards, not invented)
```
Publication → Witness → Span → SourceAssertion → CorroborationEvent → claim/argument status
```
Key objects: `Agent/Person · Publication · Edition · Witness · Span · SourceAssertion · Asset ·
CitationRelation · DerivationRelation` — each aligned to FaBiO/PROV/WebAnnotation/CiTO/IIIF, with a **small Pāṭala
epistemic extension** (SourceAssertion, CorroborationEvent, authority/review state, dependency propagation) that
no bibliographic standard provides.

- **Bibliography is the identity spine.** `Publication` (`pt:publication:...`) is canonical; everything points to
  it. **Bibliographic identity ≠ local file ≠ text extraction.**
  ```json
  {"publication_id":"pt:publication:sanderson:2007:saiva-exegesis","type":"ARTICLE","authors":["pt:person:alexis-sanderson"],"year":2007,"venue":"...","identifiers":{"doi":"..."}}
  ```
- **DocumentWitness** — one Publication may have many files (Academia PDF, publisher PDF, OCR txt, chapter
  reprint). Record `witness_id, publication_ref, format, sha256, source_uri, rights, derives_from, extraction_status`.
- **SourceSpan** — universal stable locator: `page / folio / section / paragraph / line / timestamp / char range /
  token range / TEI anchor`, with a `text_sha256`. Dual addressing: human "Ratié 2011, p.123" ↔ machine
  `pt:span:ratie-2011:v1:p123:para4`.
- **SourceAssertion** (deliberately NOT `ScholarAssertion` — future-proof for commentators, primary authors,
  institutions, datasets, interviews):
  ```json
  {"assertion_id":"pt:assertion:source:...","source_span_ref":"pt:span:...","attributed_to":"pt:person:isabelle-ratie","claim":"...","assertion_type":"INTERPRETIVE","commitment":"ASSERTS","extraction_origin":"MACHINE_PROPOSED","verification":"SPAN_VERIFIED"}
  ```
  **`SPAN_VERIFIED` means "the source really says this, adequately represented" — NOT "the assertion is
  philosophically true."** Same Pāṭala discipline.
- **Asset** (figure/table/manuscript image/map/audio) as a sibling — `asset_id, witness_ref, publication_ref, type,
  locator, rights, sha256`.
- **Rights first-class now:** each publication/witness/asset carries `rights_status, license, copyright_holder,
  allowed_uses, attribution_requirement, source_url`. (citation ≠ permission to redistribute ≠ permission to
  reproduce a figure.)

### Dedup / derivation lineage (the anti-fake-multi-source guard)
Track `SAME_PUBLICATION · REPRINT_OF · PREPRINT_OF · OCR_OF · EXCERPT_FROM · TRANSLATION_OF · EDITION ·
DERIVED_FROM · CITES · QUOTES · DISCUSSES · ASSERTS · ATTRIBUTES_TO · SUPPORTS · CONTRADICTS · CORROBORATES ·
USES_AS_EVIDENCE`. Without this, the same Sanderson argument in PDF A + Festschrift reprint + OCR txt looks like
4 independent sources when epistemically it is ONE judgment. **Never count raw source count as support.**

### Vertical-first (do NOT overbuild the 213 PDFs)
Build the substrate against a deliberately messy 5–10 sources for ONE existing argument (ARG-002, already partially
corroborated): 2–4 Ratié papers, 1 Torella source, 1 Sanderson source, *Le Soi et l'Autre*, a duplicate/reprint
case, an OCR-derived text, and one source with a useful figure. Prove one source travels end-to-end
`file → publication → witness → normalized text → stable span → source assertion → bibliography → site citation →
argument corroboration → education citation` **without custom glue**. The schema is forced by real problems (page
numbers missing in OCR, same paper in three collections, footnote corruption, scholar-quoting-vs-asserting,
summary-of-opponent misread as author's position, historical-vs-interpretive, book page numbering mismatch,
French/German, Sanskrit quotations inside scholar prose) — the gold-first discipline.

### The two-source-side architecture (what S0 enables)
```
PRIMARY-TEXT SIDE            SCHOLARSHIP SIDE
  SOURCE → L0/L1 → L2           Publication → Witness → Span
  → L200 → C1                    → SourceAssertion
         \                    /
          Proposition ↔ CorroborationEvent ↔ SourceAssertion
```
The generic source substrate sits **under/alongside** the Sanskrit L0/L200 stack — do NOT force modern English
scholarship through L0/L1/L2/L200.

### Source Registry (one service)
`resolve_publication / resolve_witness / resolve_span / search_publications / search_spans /
get_source_assertions / get_assets / register_publication / register_witness / register_span /
propose_source_assertion` — reads separated from writes. The site/education/media/API resolve IDs, not files:
`site → pt:publication:... → resolver → metadata + allowed witness + citations + assets`.

### Skills (reusable autonomous layers)
```
skills/scholar-ingest/SKILL.md       RAW PDF → bibliographic ID → witness → text/page map → source assertions → citation graph
skills/scholar-corroborate/SKILL.md  Proposition + SourceAssertions → DIRECT_SUPPORT / PARTIAL_SUPPORT / ALTERNATIVE_READING / CONTRADICTION / BACKGROUND_ONLY (model proposes; provenance checks bind)
```

### Four standards families (scholarlayer2) — do NOT implement 20 standards; triage them
```
1. IDENTIFY / PACKAGE SOURCES   FaBiO · BIBFRAME · DataCite/Crossref · ORCID · ROR · RO-Crate
2. ADDRESS / EXPOSE CONTENT     W3C Web Annotation · CTS (primary-text identity) · DTS (text API) · IIIF · JATS · TEI
3. REPRESENT EVIDENCE + REASONING  CiTO · nanopub · xAIF · SEPIO
4. TEST WHETHER THE SYSTEM WORKS  TantraFact · ArgumentBench · PāṭalaQA · CorroborationBench · CitationBench (SciFact/FEVER/FEVEROUS/MultiVerS/QASPER inspiration)
```
Triage: **build compatibility into the schema now** (FaBiO-ish identity, PROV semantics, Web Annotation selectors,
**CTS-compatible textual identity**, ORCID/ROR external IDs, rights) · **adopt as adapters later** (RO-Crate, DTS,
IIIF, TEI, JATS, CiTO, BIBFRAME, nanopub, xAIF, SEPIO) · **use as benchmark inspiration only** (SciFact/FEVER/
FEVEROUS/MultiVerS/QASPER — no ontology dependency).

### The evaluation plane is separate from the production graph (scholarlayer2)
TantraFact / ArgumentBench / PāṭalaQA / CorroborationBench / CitationBench **sit OUTSIDE the production graph** —
they TEST it, they are not more graph content. Crucially: **TantraFact must NOT be generated from the same
machine-produced graph it evaluates** (no circular evaluation). Its closest precedents are SciFact + FEVER, mapped
as `SUPPORTED / REFUTED / UNDERDETERMINED` + exact SourceSpans. Design `EvidenceTarget` polymorphically now
(TextSpan/TableCell/FigureRegion/GraphNode/DataRecord) even if v0 uses only text spans. The most Pāṭala-native
benchmark innovation: instead of "is claim C supported?", ask **"at what exact layer does support fail?"** —
SOURCE EXISTS → SPAN SUPPORTS → ATTRIBUTION → SCOPE → INFERENCE WARRANT → CONCLUSION (a process benchmark of
epistemic conservation, not final-label accuracy).

### Primary-text identity + API (scholarlayer2 additions)
- **CTS-compatible identifiers** for canonical primary-text passages (`TextGroup → Work → Edition/Translation →
  Passage`) — complementary to Web Annotation: CTS = *what canonical passage is this?*, Web Annotation = *where
  exactly is this span in this witness?*. Keep `pt:*` internal; be CTS-compatible.
- **DTS-compatible text API** for the future public text surface (internal `pt:*`/canonical graph, external DTS
  retrieval) rather than a proprietary endpoint design.
- **JATS** ingestion preference when publisher XML exists (JATS → structured HTML → born-digital PDF → OCR PDF);
  consume losslessly when available, don't convert everything ourselves.
- **ORCID/ROR** as external IDs on `pt:person:` / `pt:org:` (sameAs); internal IDs stay because not every
  historical author has an ORCID.

### REUSE-FIRST (the S0 execution doctrine — scholarlayer3): borrow open-source SYSTEMS, not just schemas
The strongest move is to **reuse actual mature open projects**, not merely align Pāṭala schemas to standards.
The criterion for every infra ticket:

> **Before building this, find out whether GROBID, Zotero, OpenAlex, OpenCitations, RO-Crate, ORKG, OpenReview,
> IIIF/TEI or another mature open project already solves it. If yes, integrate it. Spend Pāṭala engineering only
> where epistemic structure and philosophical reasoning begin.**

Borrow: **GROBID** (PDF→structured text, Apache-2.0) · **Zotero** (bibliography/library CRUD, `since=` sync, CSL
citations) · **OpenAlex/Crossref/DataCite** (metadata enrichment) · **OpenCitations** (citation graph) ·
**RO-Crate** (packaging) · **ORKG** (borrow patterns, NOT backend) · **OpenReview/Kotahi/Janeway** (peer-review
workflow) · **PROV-O / W3C Web Annotation / CiTO / CSL** (vocab) · **JATS/TEI** (consume) · **IIIF** (assets) ·
**SciFact/FEVER** (benchmark concepts).

The custom source subsystem shrinks to a thin Pāṭala resolver:
```
source/  ids.py · resolver.py · span.py (Web-Annotation SourceSpan + Pāṭala hashes) · assertion.py (SourceAssertion) · crosswalk.py
```
Everything else is borrowed. The ingest pipeline is very small:
`RAW PDF → GROBID → {TEI, refs, coordinates} → Zotero identity → OpenAlex/OpenCitations enrichment →
Pāṭala SourceSpan → Pāṭala SourceAssertion` — only the last two are ours. Full doctrine:
`source-evidence/docs/reuse-first-stack.md`.

### Directory layout (scaffold when starting S0)
```
source-evidence/  schema/ registry/ ingest/ normalize/ spans/ assertions/ assets/ rights/ citations/ validators/
```
Guiding docs: `source-evidence/docs/scholar-layer-schema-stack.md` (FaBiO/PROV/WebAnnotation/CiTO/RO-Crate/IIIF
profile) · `source-evidence/docs/scholar-layer-evaluation-and-ids.md` (four families, evaluation plane,
CTS/DTS/JATS/ORCID/ROR) · `source-evidence/docs/reuse-first-stack.md` (borrow open-source systems, thin resolver) ·
**`source-evidence/docs/tool-integration.md` (THE AUTHORITATIVE S0 EXECUTION GUIDE — use this for the build)**
+ **`source-evidence/docs/tool-integration2.md` (the EXPANDED reuse stack — Inspect/PaperQA2/INCEpTION/Docling/
AnyStyle/Hypothesis + baselines)**.

### S0.5 — The expanded reuse stack (tool-integration2) — the top-3 prototypes
The next three integrations to prototype (they eliminate three huge engineering categories — custom benchmark
framework, custom scholarly RAG engine, custom annotation/gold UI):
```
A. INSPECT AI (MIT) — the ENTIRE benchmark runtime. TantraFact / ArgumentBench / CorroborationBench / CitationBench
   / PāṭalaQA become Inspect tasks with CUSTOM SCORERS (verdict/span/attribution/scope/warrant/false-corroboration)
   + SCANNERS (citation_laundering, scope_strengthening, unsupported_addition, benchmark_leak, gold_phrase_copying)
   + EvalLog/View. Map Pāṭala BenchmarkRun ↔ Inspect EvalLog.  [IMMEDIATE]
B. PAPERQA2 (Apache-2.0) — the Scholar Assistant retrieval engine. It finds likely-useful evidence; Pāṭala decides
   what it licenses. Prototype on top of it; reuse its Crossref/Semantic Scholar/Unpaywall metadata clients.
   Also its local Tantivy BM25 stack = the independent lexical retrieval baseline.  [IMMEDIATE prototype]
C. INCEpTION (Apache-2.0) — the annotation/adjudication workbench for gold building (speaker/commitment/
   proposition/premise/inference/scope + Corroboration relations) → canonical gold JSON → Inspect.  [VERY HIGH]
```
Also added to the borrow list: **Docling** (general doc parser beside GROBID) · **AnyStyle** (bibliography
fallback, cheap win) · **Hypothesis** (inline public annotation → ReviewProposal → ReviewEvent) · **CRAG mock-API
pattern** (frozen corpus snapshot for reproducible benchmarks) · **CiteVQA** (Strict Epistemic Accuracy metric:
answer ∧ evidence ∧ attribution ∧ scope) · **S2ORC/SciAtlas/Valsci/PaperQA2** (modern-science + baselines later).
If A/B/C work, Pāṭala builds only the epistemic objects + Pāṭala-specific datasets/scorers/UX.

### S0.6 — The final assembled architecture (tool-integration3): what Pāṭala owns
After stripping every reusable piece, Pāṭala owns **only** the fine-grained epistemic dependency graph:
`SourceAssertion · EvidenceUse · CorroborationEvent · SemanticAlignment · Proposition · Commitment · DebateFrame ·
EpistemicRegime · InferenceApplication · Argument · Attack · Crux · ArgumentSynthesis · ReviewEvent · ImpactReport ·
epistemic ceiling · dependency propagation · staleness/supersession` + Pāṭala-specific benchmark
definitions/scorers. Everything else is orchestration/adapters:
```
parse GROBID/Docling · biblio Zotero · search PaperQA2/SciRAG · perspectives STORM · annotate Recogito ·
gold/adjudication INCEpTION · eval Inspect · review OpenReview/Kotahi · review federation COAR Notify ·
publishing Manubot/PubPub/Janeway · identity ORCID · roles CRediT · project PID RAiD · review DOI Crossref
```

### S0.7 — The ruthless integration order (each experiment asks: "does this delete a subsystem we planned to write?")
```
1. Inspect AI      port one existing benchmark + laundering mutations
2. PaperQA2        point it at ~20 local Ratié/Sanderson sources, compare retrieval
3. INCEpTION       create one Argument/Corroboration annotation project
4. Recogito        embed in one passage page; turn a highlight into a ReviewProposal
5. STORM/Co-STORM  replace its retrieval with Pāṭala/PaperQA; test the Vision-07 Perspective Collector
6. COAR Notify     document the adapter contract only (no infrastructure)
7. Manubot         prove one EssayObject exports into a citable versioned manuscript
8. RAiD/Crossref/ORCID/CRediT   design the scholar-credit projection (runtime later)
```
If yes → adopt; if no → discard. The vision is not "build the mammoth product" — it is "remove everything that
isn't the vision": the epistemic dependency graph.

### S0.0 — Freeze the contract (per tool-integration.md)
The minimal end-to-end contract is frozen before more code:
```
RawSource → BibliographicRecord → Witness → SourceSpan → SourceAssertion → CorroborationEvent → consumer
```
Pāṭala owns only `pt:source_id · pt:witness_id · pt:span_id · SourceAssertion · CorroborationEvent · resolver()`.
External systems own the rest where possible. **Acceptance criterion: replacing Zotero/GROBID/OpenAlex later must
not invalidate Pāṭala IDs or epistemic objects.**

### S0 immediate implementation sequence (from tool-integration.md)
```
1. source-evidence/adapters/grobid.py    2. adapters/zotero.py    3. adapters/crossref.py    4. adapters/openalex.py
5. source-evidence/resolver.py           6. SourceAssertion schema+validator
7. CorroborationEvent schema+validator   8. fixtures/ 5-10 ugly docs   9. test_scholar_vertical.py   10. one product proof
```
External-tool testing rule: every adapter has **LIVE / RECORDED / UNAVAILABLE** modes and Pāṭala behaves sensibly
in all three (e.g. Crossref/OpenAlex unavailable must not crash source resolution; GROBID failure affects
extraction but not registered witnesses). Tests run offline by default; real API tests opt-in (`-m integration`).

### S0 execution order (integration/proof exercise — do NOT rebuild scholarly infra)
```
S0.1 EXTERNAL-TOOL PILOT  5-10 messy sources -> Zotero bibliographic identity -> GROBID extraction ->
     Crossref/OpenAlex/OpenCitations enrichment -> Pāṭala stable span/resolver -> SourceAssertion
S0.2 ONLY THE MISSING SEMANTICS  SourceAssertion · CorroborationEvent · independence/lineage classification ·
     rights pointer/status (NOT engines)
S0.3 PRODUCT PROOF  one assertion resolves correctly in: bibliography · scholar assistant · argument
     corroboration · site citation · education citation (same IDs, agnostic consumers)
S0.4 F1  false-positive-tested scholarly corroboration
```

**Don't-build-it-yourself guardrails (the point of S0.1):**
- **Dedup:** first use external IDs (DOI / OpenAlex work / OpenCitations / ISBN / Zotero item / file SHA); then
  only resolve the remaining cases via a **tiny relation table**
  `SAME_PUBLICATION · DERIVED_FROM · REPRINT_OF · PREPRINT_OF · EXCERPT_FROM · UNKNOWN` — no general
  entity-resolution system.
- **Rights:** no rights engine. Store enough to prevent misuse — `rights_status · license · source_url ·
  redistributable? · asset_reproduction_allowed? · attribution` — populated from Zotero/GROBID/Crossref metadata;
  unresolved stays `UNKNOWN` (**`UNKNOWN` is a valid state**).
- **Assertions:** do NOT pre-extract from the whole corpus. SourceAssertion generation is **demand-driven**
  (question/proposition → retrieve relevant passages → propose assertions → bind to exact spans → cache/version).
  The graph grows around actual Pāṭala research, not a low-value machine-claim dump.

**S0 HARD STOP — done when you can demonstrate:**
```
1. arbitrary scholarly PDF -> stable publication identity
2. exact passage resolved reproducibly
3. passage -> an attributed SourceAssertion
4. SourceAssertion supports/opposes a Pāṭala proposition
5. bibliography / site / assistant / education resolve the SAME IDs
6. moving/renaming the source file breaks none of those references
```
Then STOP source infrastructure. Do NOT wait for all-Sanderson-normalized / all-213-PDFs-deduplicated /
complete-citation-graph / perfect-rights / every-assertion-extracted / full-IIIF / full-RO-Crate — those happen
lazily when products demand them.

---

### F1 — SCHOLAR CORROBORATION (run as an EXPERIMENT, not assumed to work; now consumes the S0 substrate)
Build proposition-level `CorroborationEvent`s for ARG-001/002/004/005 against the scholar oracle, deriving
per-argument ceilings by weakest-governs. The research question is testable, with its own **false-positive test**:

> Can Pāṭala map a structured proposition/reconstruction to exact published scholarly support with sufficiently
> high precision to justify `SCHOLARLY_CORROBORATED`?

- **Protocol:** per proposition, a `CorroborationEvent` with `relation`, `scope`, `semantic_relation`,
  `independence`, `method`, `defeaters`; multiple sources preserved as separate events; disagreement → 
  `SCHOLARLY_CONTESTED` / active defeater. **False-positive test:** for a held-out set of propositions, an
  independent reviewer (or an adversarially-constructed near-miss set: same term wrong sense, same topic wrong
  relation) must confirm the mapped scholar passage genuinely bears on the exact claim — or the mapping is
  rejected.
- **Leakage guard (for F3):** keep clean splits — `construction sources ≠ corroboration sources ≠ held-out
  extraction evaluation`. Do not use the same scholar corpus to both generate the gold and evaluate the
  extractor in a way that leaks answers.
- **Checkpoint:** CP4 · **Object:** the argument golds → `ARG-REFERENCE` (see §2) · **Proof:** N
  `CorroborationEvent`s with false-positive rate measured; evidence matrix scholar column populated.

### F2 — Scale the argument packs (the compounding asset)
Run synthesis → EO → essay over MORE passages (beyond the reflexion-core), corroborating each against the
scholar oracle. The value is **many provenance-linked, scholar-corroborated packs**, not one demo.
- **Checkpoint:** CP4/CP6 · **Object:** many ArgumentSyntheses · **Proof:** N packs each with a corroboration
  block + a `BenchmarkRun`.

### F3 — Build the extractor into the corroborated substrate (the real capability gap)
Automatic argument reconstruction is `NOT_ESTABLISHED` (baseline 0.36/0.0). Build it **after** the substrate it
writes into is scholar-corroborated, so extraction is measured against corroborated gold — not machine-guessed
gold.
- **Checkpoint:** CP4 · **Object:** a real extractor · **Proof:** blind eval vs corroborated gold, beats the
  lexical-overlap baseline, with abstention.

### F4 — Agent 2 / the autonomous factory (the scale enabler)
Shared infra (`registry idempotency → single-writer lock → Hermes timeout/orphan cleanup → stable passage_id +
source-hash binding → bounded batching → ASCII-avagraha → OCR→SOURCE_BLOCKED → crash/resume + adversarial tests →
Sanskrit-only replay certificate → a small Kramasadbhāva canary`), then the **generic L0 controller** reused
across the canonical production stack `L0/L1 → L2 READ → L200 AUDIT → C1 → THEMES → ESSAYS → EDUCATION`, so the
next Argument Gold does not rest on bespoke manual derivation.

### F5 — The product (what this all compounds to)
A **provenance-linked, scholar-corroborated scholarly graph at scale** — every proposition resolves to source,
every reconstruction is corroborated against published scholars, every downstream rendering is monotone. That is
the moat: `D × P × V × N × A`, with the verified scholarly judgments supplied by the scholars we already hold.

---

## 2. TERMINOLOGY: `ARG-REFERENCE`, not `ARG-GOLD`

`ARG-GOLD` is misleading — these are machine-built, model-reviewed objects, not independently-adjudicated gold.
Rename the canonical structured reconstructions used as benchmark targets to **`ARG-REFERENCE`**, with status
held separately: `MACHINE_REFERENCE · SCHOLARLY_CORROBORATED_REFERENCE · INDEPENDENT_REVIEWED_REFERENCE ·
ADJUDICATED_REFERENCE`. This prevents "the filename says GOLD → subconscious assumption it is correct." (The
existing `ARG-GOLD-00X` filenames stay as historical identifiers; the *status* language uses `REFERENCE`.)

## 2b. THE HONEST STATUS (what is real vs not)

**REAL / DONE:** the vertical architecture (synthesis → EO → essay → audit) · the active Nyāya audit · the
k-core/Louvain baseline · ARG-002 corroborated to `SCHOLARLY_CORROBORATED_PRELIMINARY` · the scholar oracle on
disk.

**REAL / NOT YET:** ARG-001/004/005 corroboration (F1) · many packs (F2) · the extractor (F3) · the autonomous
factory (F4).

**NOT ESTABLISHED (honestly):** automatic argument reconstruction (0.36/0.0) · accepted themes · a generalized
essay/philosophy engine · `INDEPENDENT_REVIEWED` (the one state we can't reach — and no longer the gate).

---

## 3. GUARDRAILS (unchanged)

1. Route everything through `benchmarks/v0/` + record a `BenchmarkRun`. 2. Join on `Ref` IDs — never fuzzy.
3. Do NOT hack viruddha into the frozen `nyayagate.py`. 4. `k_core != theme`; no claim of philosophical
centrality. 5. Semantic-relation labels are reviewer-assigned assertions, not machine-proven facts.
6. Do NOT reopen the frozen argument-pack architecture to retrofit L200 now — wire L200 when Agent 2 makes it
autonomous. 7. Git discipline: canonical line = `origin/agent1-argument-layer-a1b`; never force-push/rewrite
another lane.

---

## 4. THE ONE-SENTENCE CARRY-FORWARD

**We are not waiting for a human — the published scholars we already own (the full Sanderson corpus + Ratié +
Torella + Bäumer) are the scalable scholarly corroboration oracle. But that oracle is only usable once it is a
provenance-addressable evidence corpus, not a folder of excellent PDFs. So the forward plan is: (S0) build the
generic `source-evidence/` substrate — Publication → Witness → StableSpan → SourceAssertion, with bibliography as
the identity spine, dedup/derivation lineage, rights, and stable dual locators, done vertically against 5–10
messy sources — then (F1) run scholar corroboration as a false-positive-tested experiment, (F2) scale the
argument packs, (F3) build the extractor into that corroborated substrate, (F4) enable scale via Agent 2's
autonomous factory. The result is a provenance-linked, scholar-corroborated scholarly graph at scale — the moat —
that needs nothing more than what we already hold, once it becomes addressable.**
