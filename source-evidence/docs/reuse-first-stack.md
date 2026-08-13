# REUSE-FIRST STACK — borrow actual open-source systems, not just align to standards

*2026-08-13. The S0 execution doctrine: **reuse mature open-source projects**, not merely Pāṭala schemas aligned to
standards. Pāṭala owns ONLY the narrow layer nobody else provides — `source assertion → evidence role →
proposition → argument → crux → review/adjudication → downstream consequences`. Almost everything below and
around that can be borrowed.*

> **The criterion for every new infrastructure ticket:** *Before building this, find out whether GROBID, Zotero,
> OpenAlex, OpenCitations, RO-Crate, ORKG, OpenReview, IIIF/TEI or another mature open project already solves it.
> If yes, integrate it. Spend Pāṭala engineering effort only where epistemic structure and philosophical reasoning
> begin.*

## The stack to assemble

| Need | Reuse | Build ourselves? |
|---|---|---|
| PDF → structured scholarly text | **GROBID** (Apache-2.0; metadata, references, citation contexts, sections, paragraphs, figures, footnotes, coordinates, DOI resolution, license) | No |
| Bibliography / library management | **Zotero** (items/collections/attachments/versioning/`since=` sync/CSL/BibTeX/TEI export/web+local API) | Almost no |
| DOI/author/work enrichment | **OpenAlex + Crossref/DataCite** | No |
| citation graph | **OpenCitations Meta** | No |
| portable corpus packaging | **RO-Crate** (Apache-2.0) | No |
| scholarly KG patterns | **ORKG** | Borrow heavily (precedent/interop, NOT backend) |
| provenance vocabulary | **PROV-O** | No |
| span annotations | **W3C Web Annotation** | No |
| article XML | **JATS** | Consume only (JATS → HTML → born-digital PDF → OCR PDF) |
| Sanskrit/critical editions | **TEI** | Consume/export |
| manuscripts/images | **IIIF** | Integrate when needed |
| citations/bibliographies | **CSL/citeproc via Zotero** | No |
| claim-verification benchmark design | **SciFact / FEVER** | Fork concepts |
| peer-review workflow | **OpenReview / PREreview / Kotahi/Janeway** | Integrate |
| **Pāṭala epistemic graph** | **Pāṭala** | **Yes** |
| **TantraFact** | Pāṭala, using SciFact/FEVER patterns | **Yes** |
| **adversarial philosophical review** | **Pāṭala** | **Yes** |

## The thin Pāṭala resolver (the custom subsystem shrinks dramatically)

Custom code roughly becomes:
```
source/
  ids.py       stable pt:* ids + Zotero/DOI/OpenAlex/OpenCitations crosswalks
  resolver.py  thin resolution service (the only thing we write)
  span.py      Web-Annotation-compatible SourceSpan + Pāṭala hash selectors
  assertion.py SourceAssertion (Pāṭala-native epistemic object)
  crosswalk.py ORCID/ROR/DOI/OpenAlex/OpenCitations mapping
```
Everything else is borrowed:
`PDF parsing → GROBID · bibliography → Zotero · metadata → Crossref/OpenAlex · citation graph → OpenCitations ·
package/export → RO-Crate · citation formatting → CSL · provenance → PROV-O · span → Web Annotation`.

## The ingest pipeline (very small)

```
RAW PDF → GROBID → {TEI full text, references/metadata/coordinates} → Zotero identity
  → OpenAlex/OpenCitations enrichment → Pāṭala SourceSpan → Pāṭala SourceAssertion
```
Only the last two are really ours.

## What this extends to (the products)

- **TantraFact**: use FEVER/SciFact conventions + existing eval tooling; Pāṭala adds `scope / modality /
  attribution / semantic alignment / argument role / defeaters / UNDERDETERMINED` — build the *difficult
  philosophical benchmark*, not another benchmark framework.
- **Peer-review adversary**: use OpenReview/Kotahi/Janeway for the workflow; Pāṭala contributes claim
  decomposition / source verification / argument reconstruction / scope-attribution attacks / counterevidence /
  minimal cruxes, exporting/importing structured ReviewEvents.
- **Scholar Hub**: a **view over the Pāṭala epistemic graph + those systems** (OpenAlex/Zotero metadata +
  OpenCitations citation graph + local sources + Pāṭala SourceAssertions/positions/conflicts/ReviewEvents). Only
  the bottom half is the moat.
- **Scholar Assistant**: an orchestrator over existing infra (Pāṭala graph + GROBID-indexed full text + Zotero +
  OpenAlex/OpenCitations → exact passages → SourceAssertions → SemanticAlignments → structured comparison).

## The rule of thumb

> **"Do as little work as possible."** For every infra ticket, find the mature open project that already solves
> it. Integrate it. Spend Pāṭala engineering effort only where **epistemic structure and philosophical reasoning**
> begin.
