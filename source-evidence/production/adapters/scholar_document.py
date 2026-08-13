"""production/adapters/scholar_document.py — the ScholarDocumentAdapter boundary.

Three adapters emit the SAME DocumentParse intermediate:
  - GrobidAdapter       preferred scholarly-PDF parser (GROBID; subprocess/HTTP when available)
  - DoclingAdapter      fallback/general document parser
  - ExistingTextAdapter already-extracted / plain-text (the working fallback today, since neither
    GROBID nor Docling is installed in this environment)

LIVE / RECORDED / UNAVAILABLE rule (from DEVPLAN S0.1):
  - LIVE       the external tool responded -> parse recorded with parser + version
  - UNAVAILABLE the tool is absent/failed -> we degrade to the next fallback and RECORD the
                limitation (extraction_failures), never silently pretend the commodity layer ran.

External parsing is NOT epistemic authority. Adapters preserve raw hashes, parser identity,
version, and failures; SourceAssertion creation is a separate Pāṭala-owned stage above.
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
from abc import ABC, abstractmethod

from . import DocumentParse, SpanLoc

PDF = "PDF"
TXT = "TXT"


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def sha256_text(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


class ScholarDocumentAdapter(ABC):
    """Base: parse a document into the Pāṭala-neutral DocumentParse."""

    parser_name: str = "abstract"

    def __init__(self, witness_id: str, pub_ref: str, path: str):
        self.witness_id = witness_id
        self.pub_ref = pub_ref
        self.path = path
        self.raw_sha256 = sha256_file(path) if os.path.exists(path) else ""

    @abstractmethod
    def parse(self) -> DocumentParse:
        ...

    def _base(self, text: str, parser_version: str | None = None) -> DocumentParse:
        return DocumentParse(
            witness_id=self.witness_id, pub_ref=self.pub_ref, raw_path=self.path,
            raw_sha256=self.raw_sha256, parser=self.parser_name,
            parser_version=parser_version, text=text,
        )


class ExistingTextAdapter(ScholarDocumentAdapter):
    """Read an already-extracted .txt (plain text) file. The working fallback today."""

    parser_name = "existing-text"

    def parse(self) -> DocumentParse:
        failures = []
        if not os.path.exists(self.path):
            return DocumentParse(witness_id=self.witness_id, pub_ref=self.pub_ref,
                                 raw_path=self.path, raw_sha256=self.raw_sha256,
                                 parser=self.parser_name,
                                 extraction_failures=[f"file not found: {self.path}"])
        try:
            with open(self.path, encoding="utf-8", errors="replace") as f:
                text = f.read()
        except Exception as e:  # noqa: BLE001
            return DocumentParse(witness_id=self.witness_id, pub_ref=self.pub_ref,
                                 raw_path=self.path, raw_sha256=self.raw_sha256,
                                 parser=self.parser_name,
                                 extraction_failures=[f"read failed: {e}"])
        dp = self._base(text)
        dp.metadata["note"] = "existing plain-text extraction (source of extraction unknown; not GROBID)"
        return dp


class PdfTextFallbackAdapter(ScholarDocumentAdapter):
    """Direct pdftotext as a LAST-RESORT fallback. Records that GROBID/Docling were NOT used.

    We do NOT build a bespoke PDF parser; pdftotext is a thin commodity fallback and its
    provenance is recorded so the epistemic layer can weigh it accordingly.
    """

    parser_name = "pdf-fallback"

    def parse(self) -> DocumentParse:
        failures = []
        if not os.path.exists(self.path):
            return DocumentParse(witness_id=self.witness_id, pub_ref=self.pub_ref,
                                 raw_path=self.path, raw_sha256=self.raw_sha256,
                                 parser=self.parser_name,
                                 extraction_failures=[f"file not found: {self.path}"])
        try:
            r = subprocess.run(["pdftotext", self.path, "-"], capture_output=True,
                               text=True, check=False)
            if r.returncode != 0:
                failures.append(f"pdftotext returncode {r.returncode}")
            text = r.stdout
        except Exception as e:  # noqa: BLE001
            return DocumentParse(witness_id=self.witness_id, pub_ref=self.pub_ref,
                                 raw_path=self.path, raw_sha256=self.raw_sha256,
                                 parser=self.parser_name,
                                 extraction_failures=[f"pdftotext failed: {e}"])
        dp = self._base(text)
        dp.extraction_failures = failures
        dp.metadata["note"] = ("pdftotext fallback (GROBID/Docling unavailable); NOT a GROBID parse. "
                               "Weigh provenance accordingly.")
        # record page anchors from form feeds
        running = 0
        pg = 1
        for chunk in text.split("\f"):
            dp.page_anchors.append({"page": pg, "char_start": running,
                                    "char_end": running + len(chunk)})
            running += len(chunk) + 1
            pg += 1
        return dp


class GrobidAdapter(ScholarDocumentAdapter):
    """Preferred scholarly-PDF parser (GROBID). Emits DocumentParse from GROBID TEI.

    GROBID is a local service (default :8070). When unavailable, we FAIL CLOSED into the
    fallback path and record the limitation — we never pretend GROBID ran.
    """

    parser_name = "grobid"

    def __init__(self, witness_id: str, pub_ref: str, path: str, base_url: str = "http://localhost:8070"):
        super().__init__(witness_id, pub_ref, path)
        self.base_url = base_url

    def parse(self) -> DocumentParse:
        # If GROBID is not running, record it and fail closed to fallback handled by caller.
        try:
            import urllib.request
            req = urllib.request.Request(self.base_url + "/api/isalive",
                                         headers={"Accept": "text/plain"})
            with urllib.request.urlopen(req, timeout=3) as r:
                alive = r.status == 200
        except Exception as e:  # noqa: BLE001
            return DocumentParse(witness_id=self.witness_id, pub_ref=self.pub_ref,
                                 raw_path=self.path, raw_sha256=self.raw_sha256,
                                 parser=self.parser_name,
                                 extraction_failures=[f"GROBID unavailable: {e}"])
        if not alive:
            return DocumentParse(witness_id=self.witness_id, pub_ref=self.pub_ref,
                                 raw_path=self.path, raw_sha256=self.raw_sha256,
                                 parser=self.parser_name,
                                 extraction_failures=["GROBID not alive"])
        # GROBID processPDF -> TEI. This env has no running GROBID; wire the real call here.
        # Placeholder returns fail-closed with a clear limitation (do not fake a GROBID parse).
        return DocumentParse(witness_id=self.witness_id, pub_ref=self.pub_ref,
                             raw_path=self.path, raw_sha256=self.raw_sha256,
                             parser=self.parser_name,
                             extraction_failures=["GROBID parse not wired in this environment"])


class DoclingAdapter(ScholarDocumentAdapter):
    """Fallback/general-document parser (Docling). Emits DocumentParse (text, paragraphs, pages).

    Used for books/scans/mixed docs where GROBID is less suited. Pāṭala does not understand
    Docling's internal model above this boundary; we convert once here. Docling unavailable
    (not installed / no models) -> fail-closed, recorded.
    """

    parser_name = "docling"

    def parse(self) -> DocumentParse:
        try:
            from docling.document_converter import DocumentConverter
        except Exception as e:  # noqa: BLE001
            return DocumentParse(witness_id=self.witness_id, pub_ref=self.pub_ref,
                                 raw_path=self.path, raw_sha256=self.raw_sha256,
                                 parser=self.parser_name,
                                 extraction_failures=[f"Docling unavailable: {e}"])
        try:
            converter = DocumentConverter()
            result = converter.convert(self.path)
            doc = result.document
            text = doc.export_to_markdown() if hasattr(doc, "export_to_markdown") else ""
            # paragraphs: split markdown on blank lines
            paras = [p.strip() for p in text.split("\n\n") if p.strip()]
            dp = self._base(text)
            dp.metadata["docling_format"] = "markdown"
            for i, p in enumerate(paras):
                dp.paragraphs.append({"id": f"p{i}", "text": p, "char_start": None, "char_end": None})
            return dp
        except Exception as e:  # noqa: BLE001
            return DocumentParse(witness_id=self.witness_id, pub_ref=self.pub_ref,
                                 raw_path=self.path, raw_sha256=self.raw_sha256,
                                 parser=self.parser_name,
                                 extraction_failures=[f"Docling conversion failed: {e}"])


def adapter_for(witness_id: str, pub_ref: str, path: str, prefer: str = "auto") -> ScholarDocumentAdapter:
    """Select the best available adapter, falling back gracefully (LIVE/UNAVAILABLE rule).

    prefer: 'auto' (existing-text for .txt, grobid-live for .pdf when reachable, else pdf-fallback),
            'grobid' (force live GROBID), 'docling', 'pdf-fallback', 'existing-text'.
    """
    from .grobid_live import GrobidLiveAdapter
    ext = os.path.splitext(path)[1].lower()
    if prefer == "grobid":
        return GrobidLiveAdapter(witness_id, pub_ref, path)
    if prefer == "docling":
        from .scholar_document import DoclingAdapter
        return DoclingAdapter(witness_id, pub_ref, path)
    if prefer == "pdf-fallback":
        from .scholar_document import PdfTextFallbackAdapter
        return PdfTextFallbackAdapter(witness_id, pub_ref, path)
    if prefer == "existing-text":
        from .scholar_document import ExistingTextAdapter
        return ExistingTextAdapter(witness_id, pub_ref, path)
    # auto: text -> existing-text; PDF -> live GROBID if reachable, else pdftotext fallback
    if ext in (".txt", ".md"):
        return ExistingTextAdapter(witness_id, pub_ref, path)
    return GrobidLiveAdapter(witness_id, pub_ref, path)


def parse_with_fallback(witness_id: str, pub_ref: str, path: str) -> DocumentParse:
    """Try the commodity path (live GROBID for PDFs), else pdftotext fallback, recording provenance.

    This is the scaling entry point: preferred parser first, graceful fail-closed fallback,
    provenance always recorded. The epistemic layer is invariant to which one ran.
    """
    from . import DocumentParse
    ext = os.path.splitext(path)[1].lower()
    if ext in (".txt", ".md"):
        return adapter_for(witness_id, pub_ref, path, prefer="existing-text").parse()
    adapter = adapter_for(witness_id, pub_ref, path, prefer="auto")  # grobid-live for pdf
    dp = adapter.parse()
    if dp.extraction_failures or not dp.text.strip():
        # GROBID failed/absent -> pdftotext fallback, preserving the recorded limitation
        fb = PdfTextFallbackAdapter(witness_id, pub_ref, path).parse()
        fb.metadata["fell_back_from"] = adapter.parser_name
        fb.extraction_failures = (["GROBID unavailable/failed; used pdftotext fallback"] +
                                  dp.extraction_failures + fb.extraction_failures)
        return fb
    return dp
