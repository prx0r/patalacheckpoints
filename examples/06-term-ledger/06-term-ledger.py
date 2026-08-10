#!/usr/bin/env python3
"""Example 06 — Term ledger.

Docs: docs/api/recipes/terminology.md
Usage: python3 06-term-ledger.py [base_url]
"""
import json, sys, urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"


def get(p):
    with urllib.request.urlopen(BASE + p, timeout=30) as r:
        return json.loads(r.read())


def main():
    # accepted senses
    s = get("/api/terms/kula/senses")
    labels = [x["label"] for x in s["senses"]]
    print("kula accepted senses:", labels)
    assert len(s["senses"]) == 2, "expected 2 accepted kula senses"

    # proposals are separate (never auto-accepted)
    props = get("/api/term-proposals?lemma=kula")
    prop_lemmas = {p["lemma"] for p in props["proposals"]}
    print("kula proposals:", len(props["proposals"]))
    assert "kula" in prop_lemmas

    # occurrences are honest substring
    occ = get("/api/terms/kula/occurrences?work_id=kubjikamata")
    print(f"occurrences: method={occ['match_method']} lemmatized={occ['lemmatized']} count={occ['count']}")
    assert occ["match_method"] == "substring"
    assert occ["lemmatized"] is False
    print("OK")


if __name__ == "__main__":
    main()
