#!/usr/bin/env python3
"""Example 01 — Find a work.

Docs: docs/api/recipes/find-a-work.md
Usage: python3 01-find-work.py [base_url]
Prints works by tradition + one full record. Exits non-zero on failure.
"""
import json, sys, urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"


def get(p):
    with urllib.request.urlopen(BASE + p, timeout=30) as r:
        return json.loads(r.read())


def main():
    # 1. list works by tradition
    works = get("/api/works?tradition=Krama")
    assert works["count"] > 0, "no Krama works"
    print(f"Krama works: {works['count']}")
    ids = [w["id"] for w in works["works"]]
    print("  sample:", ids[:5])
    assert "kramasadbhava" in ids, "kramasadbhava missing from Krama"

    # 2. each resolves individually
    w = get("/api/works/kramasadbhava")["data"]
    assert w["id"] == "kramasadbhava"
    assert w["urn"] == "tantra:text:kramasadbhava"
    print("  resolved:", w["id"], "| status:", w["translation_status"], "| verified:", w["verified"])

    # 3. the bibliography question
    untranslated = get("/api/texts?tradition=Krama&status=none")
    print(f"Krama texts with no complete EN located: {untranslated['count']}")
    for t in untranslated["texts"]:
        print("   -", t["id"])

    print("OK")


if __name__ == "__main__":
    main()
