"""production/adapters/grobid_live.py — live GROBID adapter (B0/B1).

Real GROBID integration: PDF -> processFulltextDocument -> TEI -> DocumentParse.
Pāṭala does NOT need to understand GROBID TEI above this boundary; we convert once here.

Provenance always preserved: grobid version, raw PDF hash, raw TEI hash, runtime, failures.
GROBID output is a COMMODITY parse, never epistemic authority.

Run when GROBID is reachable at base_url (default localhost:8070). The adapter is used
through the shared `adapter_for()` boundary; when GROBID is down it fails closed (recorded),
so the epistemic layer never depends on GROBID being up.
"""
from __future__ import annotations

import hashlib
import io
import os
import re
import subprocess
import time
import urllib.request
import xml.etree.ElementTree as ET

from . import DocumentParse, SpanLoc
from .scholar_document import ScholarDocumentAdapter

TEI_NS = "{http://www.tei-c.org/ns/1.0}"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class GrobidLiveAdapter(ScholarDocumentAdapter):
    """Calls GROBID processFulltextDocument and maps TEI -> DocumentParse."""

    parser_name = "grobid-live"

    def __init__(self, witness_id: str, pub_ref: str, path: str,
                 base_url: str = "http://localhost:8070"):
        super().__init__(witness_id, pub_ref, path)
        self.base_url = base_url
        self.grobid_version = None

    def is_alive(self) -> bool:
        try:
            req = urllib.request.Request(self.base_url + "/api/isalive",
                                         headers={"Accept": "text/plain"})
            with urllib.request.urlopen(req, timeout=5) as r:
                return r.status == 200
        except Exception:  # noqa: BLE001
            return False

    def process(self) -> bytes:
        """POST the PDF to processFulltextDocument; return raw TEI XML bytes."""
        # multipart/form-data upload
        boundary = "----grobidboundarypatala"
        with open(self.path, "rb") as f:
            pdf = f.read()
        body = io.BytesIO()
        body.write(f"--{boundary}\r\n".encode())
        body.write(b'Content-Disposition: form-data; name="input"; '
                   b'filename="doc.pdf"\r\nContent-Type: application/pdf\r\n\r\n')
        body.write(pdf)
        body.write(b"\r\n")
        body.write(f"--{boundary}--\r\n".encode())
        req = urllib.request.Request(
            self.base_url + "/api/processFulltextDocument",
            data=body.getvalue(),
            headers={
                "Content-Type": f"multipart/form-data; boundary={boundary}",
                "Accept": "application/xml",
            },
        )
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.read()

    def _parse_tei(self, tei: bytes) -> DocumentParse:
        raw_tei_hash = sha256_bytes(tei)
        dp = DocumentParse(
            witness_id=self.witness_id, pub_ref=self.pub_ref, raw_path=self.path,
            raw_sha256=self.raw_sha256, parser=self.parser_name,
            parser_version=self.grobid_version,
        )
        dp.metadata["raw_tei_hash"] = raw_tei_hash
        try:
            root = ET.fromstring(tei)
        except Exception as e:  # noqa: BLE001
            dp.extraction_failures.append(f"TEI parse failed: {e}")
            return dp

        # ── text + paragraphs ──
        texts = []
        paragraphs = []
        for p in root.iter(TEI_NS + "p"):
            txt = "".join(p.itertext())
            if not txt.strip():
                continue
            start = sum(len(t) + 1 for t in texts)
            texts.append(txt)
            paragraphs.append({"id": f"p{len(paragraphs)}", "char_start": start,
                               "char_end": start + len(txt)})
        dp.text = "\n".join(texts)
        dp.paragraphs = paragraphs

        # ── sections (div/head) ──
        for div in root.iter(TEI_NS + "div"):
            heads = list(div.iter(TEI_NS + "head"))
            if heads:
                dp.sections.append({"id": f"sec{len(dp.sections)}",
                                    "heading": "".join(heads[0].itertext()).strip()})

        # ── bibliography ──
        for bibl in root.iter(TEI_NS + "biblStruct"):
            entry = {}
            title = bibl.find(f".//{TEI_NS}title")
            if title is not None:
                entry["title"] = "".join(title.itertext()).strip()
            pers = [p.text for p in bibl.findall(f".//{TEI_NS}persName/{TEI_NS}forename")] + \
                   [p.text for p in bibl.findall(f".//{TEI_NS}persName/{TEI_NS}surname")]
            if pers:
                entry["authors"] = [x for x in pers if x]
            idno = bibl.find(f".//{TEI_NS}idno")
            if idno is not None:
                entry["idno"] = idno.text
                entry["idno_type"] = idno.get("type")
            if entry:
                dp.references.append(entry)

        # ── page anchors (pb) — may be absent in some GROBID outputs ──
        for pb in root.iter(TEI_NS + "pb"):
            n = pb.get("n")
            dp.page_anchors.append({"page": n, "char_start": None, "char_end": None})

        return dp

    def parse(self) -> DocumentParse:
        failures = []
        if not os.path.exists(self.path):
            return DocumentParse(witness_id=self.witness_id, pub_ref=self.pub_ref,
                                 raw_path=self.path, raw_sha256=self.raw_sha256,
                                 parser=self.parser_name,
                                 extraction_failures=[f"file not found: {self.path}"])
        if not self.is_alive():
            return DocumentParse(witness_id=self.witness_id, pub_ref=self.pub_ref,
                                 raw_path=self.path, raw_sha256=self.raw_sha256,
                                 parser=self.parser_name,
                                 extraction_failures=["GROBID not alive at " + self.base_url])
        t0 = time.time()
        try:
            tei = self.process()
        except Exception as e:  # noqa: BLE001
            return DocumentParse(witness_id=self.witness_id, pub_ref=self.pub_ref,
                                 raw_path=self.path, raw_sha256=self.raw_sha256,
                                 parser=self.parser_name,
                                 extraction_failures=[f"GROBID process failed: {e}"])
        dp = self._parse_tei(tei)
        dp.metadata["runtime_s"] = round(time.time() - t0, 2)
        dp.metadata["raw_tei_bytes"] = len(tei)
        return dp
