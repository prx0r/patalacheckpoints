# Docling — general document parser (beside GROBID)

**What Pāṭala borrows:** a wide document world parser — PDF, DOCX, PPTX, XLSX, HTML, EPUB, audio, WebVTT, images,
LaTeX, email, JATS — with layout, tables, formulas, reading order, images, and a unified lossless document
representation. **Use beside GROBID, not instead of it:** GROBID stays the scholarly-PDF specialist (references,
citation contexts, bibliographic consolidation, coordinates); Docling handles everything else.

**License:** MIT.

## API / usage
- Python: `pip install docling`; `DocumentConverter().convert(src)` → a unified `Document` (tables, reading
  order, layout, images). Export to Markdown/JSON/TEI-like.

## Rate limiting / etiquette
Local library — no server/rate limit. Etiquette = record the converter version + input hash as the extraction
witness provenance.

## How Pāṭala consumes it
```
                  INPUT
        ┌──────────┴──────────┐
   scholarly PDF          everything else
        │                       │
     GROBID                 Docling
        └──────────┬──────────┘
                   ▼
            normalized witness  →  Pāṭala SourceSpan / SourceAssertion
```
Avoids writing format-specific loaders for books/EPUBs, lecture transcripts, presentations, interview audio,
education content, manuscript images.

**Priority: HIGH as the general/fallback adapter.**
