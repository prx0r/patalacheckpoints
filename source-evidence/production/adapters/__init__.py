"""production/adapters/__init__.py — the borrowed document-ingestion boundary.

Commodity document processing lives BELOW this boundary (PDF parsing, layout, reference
extraction, OCR). Pāṭala-owned epistemic ingestion lives ABOVE it (Witness identity, exact
Span, SourceAssertion, Proposition linkage, corroboration).

Every adapter (GrobidAdapter / DoclingAdapter / ExistingTextAdapter) emits the SAME
Pāṭala-neutral intermediate `DocumentParse` — so the epistemic layer never depends on which
borrowed tool produced the parse, and a tool can be swapped without touching Pāṭala objects.

External parsing is NOT epistemic authority: we always preserve parser + version + hashes +
extraction failures. SourceAssertion creation is a SEPARATE, Pāṭala-owned stage.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SpanLoc:
    """A located span in the parse output with resilient anchors."""
    text: str
    span_sha256: str
    page: int | None = None
    section: str | None = None
    paragraph: int | None = None
    char_start: int | None = None
    char_end: int | None = None
    prefix: str | None = None
    suffix: str | None = None


@dataclass
class DocumentParse:
    """The Pāṭala-neutral intermediate every adapter must emit.

    provenance captures WHO produced the parse + how + failures — never treated as epistemic
    authority (that is decided above, by SourceAssertion creation).
    """
    witness_id: str
    pub_ref: str
    raw_path: str
    raw_sha256: str
    parser: str                      # 'grobid' | 'docling' | 'existing-text' | 'pdf-fallback'
    parser_version: str | None = None
    text: str = ""
    sections: list[dict] = field(default_factory=list)     # [{id, heading, char_start, char_end}]
    paragraphs: list[dict] = field(default_factory=list)   # [{id, char_start, char_end}]
    spans: list[SpanLoc] = field(default_factory=list)
    references: list[dict] = field(default_factory=list)   # [{citation, doi, authors, ...}]
    page_anchors: list[dict] = field(default_factory=list) # [{page, char_start, char_end}]
    extraction_failures: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)           # parser-specific extras

    def to_dict(self) -> dict:
        return {
            "witness_id": self.witness_id, "pub_ref": self.pub_ref,
            "raw_path": self.raw_path, "raw_sha256": self.raw_sha256,
            "parser": self.parser, "parser_version": self.parser_version,
            "text": self.text,
            "sections": self.sections, "paragraphs": self.paragraphs,
            "spans": [{"text": s.text, "span_sha256": s.span_sha256, "page": s.page,
                       "section": s.section, "paragraph": s.paragraph,
                       "char_start": s.char_start, "char_end": s.char_end,
                       "prefix": s.prefix, "suffix": s.suffix} for s in self.spans],
            "references": self.references, "page_anchors": self.page_anchors,
            "extraction_failures": self.extraction_failures,
            "metadata": self.metadata,
        }
