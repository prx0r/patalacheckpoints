#!/usr/bin/env python3
"""Example 04 — Passage context (evidence bundle).

Docs: docs/api/recipes/read-a-passage.md
Usage: python3 04-passage-context.py [base_url]
Verifies the deterministic evidence bundle invariants (the graph, not just JSON).
"""
import json, sys, urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"


def get(p):
    with urllib.request.urlopen(BASE + p, timeout=30) as r:
        return json.loads(r.read())


def main():
    c = get("/api/context/passages/tantra:text:kramasadbhava:1.9")
    assert c["passage"]["id"] == "tantra:text:kramasadbhava:1.9"
    assert c["work"] and c["work"]["id"] == "kramasadbhava"
    # neighboring passages resolve
    for n in ("previous", "next"):
        nb = c["neighboring"].get(n)
        if nb:
            resolved = get("/api/passages/" + nb["id"].replace("tantra:text:", ""))["data"]
            assert resolved["id"] == nb["id"], f"{n} dangling"
    # tracked terms have accepted senses
    for t in c["tracked_terms"]:
        assert t.get("senses"), f"term {t.get('lemma')} has no senses"
    print("Passage:", c["passage"]["id"])
    print("  work:", c["work"]["title"])
    print("  neighbors:", c["neighboring"]["previous"]["id"], "<->", c["neighboring"]["next"]["id"])
    print("  tracked terms:", [t["lemma"] for t in c["tracked_terms"]])
    print("  manuscripts:", len(c["manuscripts"]))
    print("  provenance:", bool(c["provenance"].get("note")))
    assert c["provenance"].get("note"), "no provenance note"
    print("OK")


if __name__ == "__main__":
    main()
