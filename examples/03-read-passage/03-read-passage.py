#!/usr/bin/env python3
"""Example 03 — Read a passage.

Docs: docs/api/recipes/read-a-passage.md
Usage: python3 03-read-passage.py [base_url]
"""
import json, sys, urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"


def get(p):
    with urllib.request.urlopen(BASE + p, timeout=30) as r:
        return json.loads(r.read())


def main():
    p = get("/api/passages/kramasadbhava:1.2")["data"]
    assert p["id"] == "tantra:text:kramasadbhava:1.2", p["id"]
    assert p["work_id"] == "kramasadbhava"
    assert p["location"] == {"chapter": 1, "verse": 2}
    assert p["sanskrit"], "empty sanskrit"
    assert p["source_edition"], "no edition"
    print("Passage:", p["id"])
    print("  sanskrit:", p["sanskrit"][:60], "...")
    print("  edition:", p["source_edition"])

    # 404 on miss
    try:
        get("/api/passages/doesnotexist")
        assert False, "expected 404"
    except urllib.error.HTTPError as e:
        assert e.code == 404, f"expected 404 got {e.code}"
    print("  miss → 404 ✓")

    print("OK")


if __name__ == "__main__":
    import urllib.error
    main()
