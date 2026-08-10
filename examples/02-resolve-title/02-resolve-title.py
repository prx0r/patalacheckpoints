#!/usr/bin/env python3
"""Example 02 — Resolve an uncertain title.

Docs: docs/api/recipes/resolve-a-title.md
Usage: python3 02-resolve-title.py [base_url]
Proves the resolver returns machine_proposed candidates, never accepted.
"""
import json, sys, urllib.request, urllib.error

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"


def post(p, body):
    req = urllib.request.Request(BASE + p, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def main():
    r = post("/api/resolve/work", {"title": "Amṛteśatantram"})
    assert r["status"] == "machine_proposed", f"resolver not machine_proposed: {r['status']}"
    cands = [c["work_id"] for c in r["candidates"]]
    assert "netratantra" in cands, f"netratantra missing: {cands}"
    print("Amṛteśatantram →", cands, f"(status: {r['status']})")
    assert not any(c.get("status") == "accepted" for c in r["candidates"]), "resolver returned accepted!"

    r2 = post("/api/resolve/work", {"title": "zzzqqqxxxnomatch"})
    assert r2["status"] == "machine_proposed"
    print("gibberish →", len(r2["candidates"]), "candidates (low, as expected)")
    assert not any(c.get("status") == "accepted" for c in r2["candidates"])

    print("OK — resolver never produces an accepted assertion")


if __name__ == "__main__":
    main()
