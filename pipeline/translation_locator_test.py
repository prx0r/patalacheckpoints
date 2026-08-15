#!/usr/bin/env python3
"""pipeline/translation_locator_test.py — proof for the live translation-location resolver.
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/translation_locator_test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "pipeline"))
sys.path.insert(0, str(ROOT / "python"))

import translation_locator as TL  # noqa: E402
import metadata_resolver as MR  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("TRANSLATION-LOCATOR — proof (live multi-API translation location)\n")

    # OpenAlex resolver returns OA/location fields (added)
    oa = MR.resolve_openalex("Tantraloka", "Abhinavagupta")
    gate("openalex resolves", oa["status"] == "RESOLVED", oa.get("doi"))
    gate("openalex has locations field", "locations" in oa, f"{len(oa.get('locations', []))} locations")
    gate("openalex has oa_status", "oa_status" in oa, oa.get("oa_status"))

    # Unpaywall: works for an OA DOI, honest for non-OA
    up = MR.resolve_unpaywall("10.1038/s41586-020-2649-2")
    gate("unpaywall resolves an OA DOI", up["status"] == "RESOLVED", f"is_oa={up.get('is_oa')}")
    up_nodoi = MR.resolve_unpaywall("")
    gate("unpaywall handles no-DOI", up_nodoi["status"] == "NO_DOI", "does not crash on empty DOI")

    # the merged live locator on a real work
    r = TL.availability_with_live("kiranatantra")
    gate("live merge keeps curated", r["has_english"] is True, f"coverage={r['coverage']}")
    gate("live providers present", "providers" in r["live"], str(r["live"]["providers"]))
    gate("live resolved a record", r["live"]["resolved"] is True, f"doi={r['live']['doi']}")
    gate("live returns locations", isinstance(r["live"]["locations"], list))

    # fail-closed: the locator never crashes the pipeline on API issues
    try:
        _ = TL.live_locations("definitely-not-a-real-work-xyz123")
        gate("locator is fail-closed (no crash)", True)
    except Exception as e:
        gate("locator is fail-closed (no crash)", False, str(e)[:80])

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
