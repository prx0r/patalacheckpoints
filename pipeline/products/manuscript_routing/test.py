#!/usr/bin/env python3
"""products/manuscript_routing/test.py — manuscript-routing proof (vision E3).
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/products/manuscript_routing/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))

from products.manuscript_routing.engine import route_manuscript, route_catalog  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("MANUSCRIPT ROUTING — proof (vision E3)\n")

    # scan-no-text -> OCR
    scan = route_manuscript({"id": "m1", "script": "Devanagari", "photos": True, "text": False})
    gate("scan-no-text -> OCR_THEN_FACTORY", scan["route"] == "OCR_THEN_FACTORY",
         f"{scan['label']} -> {scan['route']}")
    gate("OCR routes to kraken + pe-ocr gate", scan["ocr_tool"] and "kraken" in scan["ocr_tool"]
         and scan["quality_gate"] and "pe-ocr" in scan["quality_gate"], "adopt, don't rebuild")

    # scan-with-text -> FACTORY_READY
    txt = route_manuscript({"id": "m2", "script": "Devanagari", "photos": True, "text": True})
    gate("scan-with-text -> FACTORY_READY", txt["route"] == "FACTORY_READY", txt["route"])

    # IAST -> FACTORY_READY
    iast = route_manuscript({"id": "m3", "script": "IAST", "text": True})
    gate("IAST etext -> FACTORY_READY", iast["route"] == "FACTORY_READY", iast["route"])

    # no text/photos/anchor -> UNROUTEABLE
    none = route_manuscript({"id": "m4", "script": "unknown"})
    gate("empty record -> UNROUTEABLE", none["route"] == "UNROUTEABLE", none["route"])

    # batch routing (raw manuscript records, not routed dicts)
    cat = route_catalog([
        {"id": "m1", "script": "Devanagari", "photos": True, "text": False},
        {"id": "m2", "script": "Devanagari", "photos": True, "text": True},
        {"id": "m3", "script": "IAST", "text": True},
    ])
    gate("batch routing works", cat["n_manuscripts"] == 3 and "FACTORY_READY" in cat["by_route"]
         and "OCR_THEN_FACTORY" in cat["by_route"], str(cat["by_route"]))

    gate("MACHINE_PROPOSED honesty", "MACHINE_PROPOSED" in scan["note"],
         "routing never fabricates a work identity")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
