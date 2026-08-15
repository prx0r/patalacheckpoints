#!/usr/bin/env python3
"""pipeline/assess.py test — the ASSESS-FLOW proof (deterministic decision engine).
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/assess_test.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "pipeline"))

import assess  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("ASSESS — the decision engine proof (deterministic, no LLM)\n")

    # a real acquired work routes to translate
    r = assess.assess("sivadharmasastra")
    gate("assessed work has all fields", all(k in r for k in
         ("tag", "state", "format", "verse", "identity", "priority", "route")), r["work"])
    gate("clean et-text routes to translate", "TRANSLATE" in r["route"],
         f"state={r['state']} fmt={r['format']} id={r['identity']}")
    gate("priority in enum", r["priority"] in assess.PRIORITIES, r["priority"])

    # scheme detection (T2) — the sanskrit-util lift
    gate("detect deva", assess._scheme("प्रभुः कालः") == "deva")
    gate("detect iast", assess._scheme("prabhuḥ kālaḥ") == "iast")
    gate("detect itrans", assess._scheme("prabhuh kaalah") == "itrans")
    gate("detect hk", assess._scheme("prabhuH kAlaH") == "hk")

    # format detection is deterministic + enum-valued
    fmt, _ = assess._detect_format("sivadharmasastra")
    gate("format is enum-valued", fmt in assess.FORMATS, fmt)

    # the routing table (T6) — each state/format/identity row maps correctly
    route_table = {
        ("CLEAN_ETEXT", "RAW_SANSKRIT", "EXACT"): "TRANSLATE",
        ("CLEAN_ETEXT", "AND_GLOSS", "EXACT"): "EXTRACT",
        ("CLEAN_ETEXT", "RAW_SANSKRIT", "POSSIBLE"): "SCHOLAR",
        ("NEEDS_OCR", "RAW_SANSKRIT", "EXACT"): "OCR",
        ("LACUNA_BLOCKED", "RAW_SANSKRIT", "EXACT"): "VERSE",
        ("NO_SOURCE", "UNKNOWN", "UNRESOLVED"): "ACQUIRE",
    }
    for (st, fm, id_), expect in route_table.items():
        route = assess._route(st, fm, id_)
        gate(f"route {st}/{fm}/{id_} -> {expect}", expect in route.upper(), route)

    # the full assessment is deterministic + auditable
    all_recs = assess.assess_all()
    gate("assesses the full corpus", len(all_recs) > 50, f"{len(all_recs)} works")
    gate("every record resolves", all(r["route"] and r["state"] in assess.STATES for r in all_recs))

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
