#!/usr/bin/env python3
"""products/manuscript_ingest/test.py — manuscript -> SOURCE adapter proof (honest quality ladder).
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/products/manuscript_ingest/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))

from products.manuscript_ingest.engine import to_source, ingest_batch, QUALITY_LADDER  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("MANUSCRIPT INGEST — proof (honest quality ladder)\n")

    # raw scan (photos, no text, no OCR) -> raw_scan, not ready, needs OCR
    scan = to_source({"id": "m1", "script": "Devanagari", "photos": True, "text": False})
    gate("raw scan -> raw_scan, not ready", scan["quality"] == "raw_scan" and not scan["ready_for_translate"],
         f"{scan['quality']} ready={scan['ready_for_translate']}")
    gate("raw scan -> PENDING_OCR status", scan["status"] == "PENDING_OCR", scan["status"])
    gate("OCR is an adapter boundary (adopt, not rebuild)", "OCR adapter boundary" in scan["payload"]["provenance"]["derived_by"],
         "kraken/escriptorium adopted, not reimplemented")

    # OCR text present -> ocr_done, needs review, still not factory-ready (honest)
    ocr = to_source({"id": "m2", "script": "Devanagari", "photos": True, "text": False},
                    ocr_text="namaḥ śivāya iti prathamakhaṇḍaḥ ...")
    gate("OCR text -> ocr_done, needs review (not auto-ready)",
         ocr["quality"] == "ocr_done" and not ocr["ready_for_translate"], f"{ocr['quality']} ready={ocr['ready_for_translate']}")

    # clean etext (has transcription) -> clean_etext, factory-ready
    clean = to_source({"id": "m3", "script": "IAST", "text": True})
    gate("clean etext -> factory-ready", clean["quality"] == "clean_etext" and clean["ready_for_translate"],
         f"{clean['quality']} ready={clean['ready_for_translate']}")

    # quality ladder is the canonical order
    gate("quality ladder correct", QUALITY_LADDER == ["raw_scan", "ocr_done", "clean_etext", "factory_ready"],
         str(QUALITY_LADDER))

    # batch
    cat = ingest_batch([
        {"id": "m1", "script": "Devanagari", "photos": True, "text": False},
        {"id": "m3", "script": "IAST", "text": True},
    ])
    gate("batch ingest works", cat["n_manuscripts"] == 2 and cat["ready_for_translate"] >= 1,
         str(cat["by_quality"]))

    gate("honest provenance", "MACHINE_PROPOSED" in cat["note"], "quality is proposed, not a verdict")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
