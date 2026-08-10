#!/usr/bin/env python3
"""Example 05 — Manuscript witnesses.

Docs: docs/api/recipes/manuscript-witnesses.md
Usage: python3 05-manuscript-witnesses.py [base_url]
"""
import json, sys, urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"


def get(p):
    with urllib.request.urlopen(BASE + p, timeout=30) as r:
        return json.loads(r.read())


def main():
    m = get("/api/works/netratantra/manuscripts")
    assert m["count"] > 0, "no witnesses for netratantra"
    print("netratantra witnesses:", m["count"])
    for rec in m["manuscripts"][:3]:
        assert rec["id"].startswith("pt:ms:"), rec["id"]
        assert rec["source_url"], "no source_url"
        assert rec["licence"] == "CC-BY-NC-SA-4.0", rec["licence"]
        print(f"  - {rec['title']} | {rec['source_url']} | {rec['licence']}")

    # search works too
    s = get("/api/manuscripts?q=netra")
    assert s["count"] > 0
    print("search 'netra':", s["count"])
    print("OK")


if __name__ == "__main__":
    main()
