#!/usr/bin/env python3
"""build_static_patala.py — the OG patala projection compiler → static site (0-JS read plane).

Turns the REAL patala data into a fully static, deployable site (Astro serves it):
  web/static/
    index.json          the site manifest (bibliography + clusters + passages)
    bibliography.json   254 works
    clusters.json       9 themes
    passages.json       49 IPVV published passages
    lemma.json          the term/lemma data
    timeline.json       the school/tradition chronology
  All static bytes — compute on write, read from CDN (the perf doctrine).

Grounded in the REAL patala data (data/corpus/ + data/published/ + data/atlas/), not synthetic.
"""
import os, sys, json
from pathlib import Path

ROOT = Path("/root/projects/patala")
OUT = ROOT / "web" / "static"
DATA = {
    "bibliography": ROOT / "data" / "corpus" / "atlas-bibliography.json",
    "clusters": ROOT / "data" / "published" / "ipvv" / "clusters.json",
    "published_index": ROOT / "data" / "published" / "ipvv" / "index.json",
    "lemma": ROOT / "data" / "corpus" / "terms.ts",
    "trajectories": ROOT / "data" / "corpus" / "trajectories.ts",
    "timeline": ROOT / "data" / "atlas" / "historyTimeline.json",
}

def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # 1. bibliography (254 works)
    bib = json.load(open(DATA["bibliography"]))
    works = []
    for wid, rec in bib.get("records", {}).items():
        works.append({
            "id": wid,
            "title": rec.get("canonical_title") or rec.get("title") or wid,
            "verified": rec.get("verified", False),
            "translation_status": rec.get("translation_status") or rec.get("translationStatus") or "none",
            "traditions": rec.get("traditions", []),
        })
    works.sort(key=lambda x: x["title"].lower())
    json.dump({"count": len(works), "works": works}, open(OUT / "bibliography.json", "w"), ensure_ascii=False, indent=1)

    # 2. clusters (9 themes)
    cl = json.load(open(DATA["clusters"]))
    json.dump(cl, open(OUT / "clusters.json", "w"), ensure_ascii=False, indent=1)

    # 3. published IPVV passages (49)
    idx = json.load(open(DATA["published_index"]))
    passages = []
    pdir = ROOT / "data" / "published" / "ipvv"
    for p in idx.get("passages", []):
        f = pdir / p["file"]
        if f.exists():
            d = json.load(open(f))
            passages.append({
                "id": d.get("id"), "chunk": d.get("chunk"), "vol": d.get("vol"),
                "reading": (d.get("l2_text") or d.get("l2") or "")[:400],
                "has_c1": d.get("c1") is not None,
            })
    json.dump({"count": len(passages), "passages": passages}, open(OUT / "passages.json", "w"), ensure_ascii=False, indent=1)

    # 4. lemma (the accepted term ledger)
    lemma_terms = []
    try:
        tj = json.load(open(ROOT / "data" / "terms.json"))
        terms = tj.get("terms", {})
        if isinstance(terms, dict):
            for lemma, senses in terms.items():
                lemma_terms.append({"lemma": lemma, "senses": len(senses) if isinstance(senses, list) else 1})
        elif isinstance(terms, list):
            for t in terms:
                lemma_terms.append({"lemma": t.get("lemma", t.get("id", "")), "senses": len(t.get("senses", []))})
    except Exception as e:
        print("  lemma parse note:", e)
    json.dump({"count": len(lemma_terms), "terms": lemma_terms}, open(OUT / "lemma.json", "w"), ensure_ascii=False, indent=1)

    # 5. timeline
    try:
        tl = json.load(open(DATA["timeline"]))
        json.dump(tl, open(OUT / "timeline.json", "w"), ensure_ascii=False, indent=1)
    except Exception:
        json.dump({"count": 0}, open(OUT / "timeline.json", "w"))

    # 6. manifest
    manifest = {
        "schema": "patala.og.static-site.v1",
        "counts": {"works": len(works), "clusters": cl.get("cluster_count", 0),
                   "passages": len(passages), "terms": len(lemma_terms)},
        "generated": True,
    }
    json.dump(manifest, open(OUT / "index.json", "w"), indent=1)
    print("=== OG patala static projections built ===")
    print(json.dumps(manifest, indent=1))

if __name__ == "__main__":
    main()
