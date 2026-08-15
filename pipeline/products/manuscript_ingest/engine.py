"""products/manuscript_ingest/engine.py — the manuscript -> Pāṭala SOURCE adapter.

Completes the honest manuscript->translate path: a manuscript record + (optionally) its OCR text becomes
a labelled, source-quality-scored object ready to enter the factory SOURCE queue. The OCR itself is an
ADAPTER BOUNDARY (kraken/eScriptorium on a GPU box) — this product does NOT OCR; it turns OCR output
into a Pāṭala SOURCE with honest provenance + quality.

The quality ladder (vision-14 §3):
  raw_scan   -> image/PDF, needs OCR
  ocr_done   -> text extracted (by the OCR adapter), needs review
  clean_etext-> machine-readable, trustworthy (GRETIL/TITUS)
  factory_ready -> clean text, ready to enter the SOURCE queue -> T1

This is the "how do we go from shitty manuscript to clean labelled translate-queue" answer, made
honest: the ROUTING (manuscript_routing) + the QUALITY fingerprint (here) + the SOURCE adapter (here)
are the deterministic pieces that work on CPU; the OCR engine is the GPU boundary we adopt, not rebuild.

CPU-only, deterministic. Consumes OCHS-format manuscript metadata + optional OCR text.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(_ROOT / "pipeline"))

from products.manuscript_routing.engine import route_manuscript  # noqa: E402


# the honest quality ladder (vision-14)
QUALITY_LADDER = ["raw_scan", "ocr_done", "clean_etext", "factory_ready"]


def _quality_floor(has_photos: bool, has_text: bool, script: str, ocr_text: str) -> tuple[str, list[str]]:
    """Score a manuscript's quality honestly. Returns (quality, [notes])."""
    notes = []
    script_l = script.lower()
    is_iast = script_l in ("iast", "latin", "roman", "transliteration") or "iast" in script_l

    if ocr_text and len(ocr_text.strip()) > 10:
        quality = "ocr_done"
        notes.append("OCR text present, needs review")
        # OCR review signal: if the text has Devanagari/IAST markers + reasonable length, it's usable
        if is_iast or re.search(r"[āīūṛṝḷḹēōṃḥ]", ocr_text):
            notes.append("IAST/devanagari content detected — plausible Sanskrit OCR")
        if has_photos and has_text:
            quality = "clean_etext"
            notes.append("witness has a transcription (clean e-text level)")
    elif has_text:
        quality = "clean_etext"
        notes.append("witness holds a transcription (clean e-text)")
    elif has_photos:
        quality = "raw_scan"
        notes.append("image present, needs OCR (GPU boundary: kraken/eScriptorium)")
    else:
        quality = "raw_scan"
        notes.append("no text, no image — unrouteable without more info")

    if quality in ("clean_etext", "factory_ready"):
        notes.append("ready for the SOURCE queue -> T1")
    return quality, notes


def to_source(manuscript: dict, ocr_text: str | None = None) -> dict:
    """Turn a manuscript record + optional OCR text into a labelled, quality-scored SOURCE-ready object.

    Returns the object a factory worker would commit to the SOURCE registry (status honest).
    """
    routed = route_manuscript(manuscript)
    quality, notes = _quality_floor(
        routed["has_photos"], routed["has_text"], routed["script"], ocr_text or "")

    # the Pāṭala SOURCE object (mirrors the real source-registry shape)
    source = {
        "layer": "SOURCE",
        "object_id": f"src:{routed['manuscript_id']}",
        "status": "RAW_SANSKRIT" if quality in ("ocr_done", "clean_etext") else "PENDING_OCR",
        "payload": {
            "verse": ocr_text.strip()[:500] if ocr_text else "",
            "provenance": {
                "manuscript_id": routed["manuscript_id"],
                "custodian": manuscript.get("custodian", "OCHS"),
                "licence": manuscript.get("licence", "CC BY-NC-SA 4.0"),
                "source_url": manuscript.get("source_url", ""),
                "derived_by": "manuscript_ingest (OCR adapter boundary: kraken/eScriptorium)",
            },
            "source_type": "ocr" if quality == "ocr_done" else
                           ("manuscript_scan" if quality == "raw_scan" else "imported"),
        },
        "quality": quality,
        "quality_notes": notes,
        "route": routed["route"],
        "ready_for_translate": quality in ("clean_etext", "factory_ready"),
    }
    return source


def ingest_batch(records: list[dict], ocr_map: dict[str, str] | None = None) -> dict:
    """Ingest a batch of manuscripts -> SOURCE-ready objects (the 'get a bunch in easily' path)."""
    from collections import Counter
    sources = []
    for m in records:
        oid = m.get("id") or m.get("ochs_slug") or "unknown"
        src = to_source(m, (ocr_map or {}).get(oid))
        sources.append(src)
    by_quality = Counter(s["quality"] for s in sources)
    ready = sum(1 for s in sources if s["ready_for_translate"])
    return {
        "n_manuscripts": len(sources),
        "by_quality": dict(by_quality),
        "ready_for_translate": ready,
        "sources": sources,
        "note": "MACHINE_PROPOSED quality fingerprint; OCR is the adopted GPU boundary, not rebuilt",
    }


def demo() -> dict:
    """Route + quality-score a few OCHS-format manuscripts (representative)."""
    records = [
        {"id": "pt:ms:ochs_000_000_039_kubjikamatatantra", "ochs_slug": "ochs_000_000_039_kubjikamatatantra",
         "script": "Devanagari", "title": "Kubjikāmatatantra", "photos": True, "text": False,
         "tradition": "Kubjikā", "custodian": "OCHS"},
        {"id": "pt:ms:ochs_000_000_002_amrtesatantram", "ochs_slug": "ochs_000_000_002_amrtesatantram",
         "script": "Devanagari", "title": "Amṛteśatantram", "photos": True, "text": True,
         "tradition": "Netra", "custodian": "OCHS"},
        {"id": "pt:ms:example-iast", "ochs_slug": "example-iast", "script": "IAST",
         "title": "Tantrasadbhāva", "photos": False, "text": True, "tradition": "Bhairava"},
    ]
    # simulate OCR for the first (kubjika) so we show the ocr_done -> review path
    ocr_map = {"pt:ms:ochs_000_000_039_kubjikamatatantra":
               "namaḥ śivāya ... kubjikāmatatantram samāptaḥ iti ... prathamakhaṇḍaḥ pūrṇaḥ"}
    return ingest_batch(records, ocr_map)


if __name__ == "__main__":
    import sys as _s
    verb = _s.argv[1] if len(_s.argv) > 1 else "demo"
    if verb == "demo":
        print(json.dumps(demo(), indent=2, ensure_ascii=False))
    else:
        print(json.dumps(to_source(json.loads(_s.argv[2])), indent=2, ensure_ascii=False))
