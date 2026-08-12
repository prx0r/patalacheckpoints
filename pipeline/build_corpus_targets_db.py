#!/usr/bin/env python3
"""pipeline/build_corpus_targets_db.py — consolidate the disparate target/lead/source docs into a DB.

The mess: translation targets + leads + acquisition state + downloaded-source manifests are scattered
across patala and sanskritree (corpus/targets/*, sources/round{2,3}/, sources/gretil2/, truth/, ref/).
This compiles them into ONE queryable structure under data/corpus/targets/:

  data/corpus/targets/sources.json   — downloaded source files (from the source manifests + inventory)
  data/corpus/targets/targets.json   — the actionable RAW-L0 targets (from translation_targets.TARGETS)
  data/corpus/targets/leads.json     — the register I/II/III leads (from translation_targets.LEADS)
  data/corpus/targets/anchors.json   — translation anchors/status (from translation_status_audit.md)
  data/corpus/targets/index.json     — the master index: every doc + where it lives (links)

This is the "compile and sort it all into links and specific targets, almost like a DB" ask.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

sys_path = "/root/projects/patala"
OUT = Path(sys_path) / "data/corpus/targets"
OUT.mkdir(parents=True, exist_ok=True)

# where the original source docs live (the links we point to)
DOC_ROOTS = {
    "sanskritree_corpus_targets": "/mnt/HC_Volume_106427611/sanskritree/corpus/targets/",
    "sanskritree_sources": "/mnt/HC_Volume_106427611/sanskritree/sources/",
    "sanskritree_truth": "/mnt/HC_Volume_106427611/sanskritree/truth/",
    "sanskritree_ref": "/mnt/HC_Volume_106427611/sanskritree/ref/",
    "sanskritree_translations_meta": "/mnt/HC_Volume_106427611/sanskritree/translations/_meta/",
    "patala_downloads": "/root/projects/patala/data/corpus/downloads/",
    "patala_vision_expansion": "/root/projects/patala/docs/vision/expansion/",
}

# the source docs we index (name -> {path, note}) — the links
SOURCE_DOCS = {
    "untranslated.md":        {"path": "sanskritree_corpus_targets/untranslated.md", "note": "register I — the 20 highest-value targets"},
    "untranslated2.md":       {"path": "sanskritree_corpus_targets/untranslated2.md", "note": "register II — the sources behind the famous sources"},
    "untranslated3.md":       {"path": "sanskritree_corpus_targets/untranslated3.md", "note": "register III — the next 20 (#41-60) + 6 discoveries"},
    "targetacquired.md":      {"path": "sanskritree_corpus_targets/targetacquired.md", "note": "acquisition board — ACQ / LANDED / MS-request / locate"},
    "round2_sources.md":      {"path": "sanskritree_corpus_targets/round2_sources.md", "note": "round-2 sources — verification + commentary anchors"},
    "translation_status_audit.md": {"path": "sanskritree_corpus_targets/translation_status_audit.md", "note": "don't-duplicate — which texts already have English translations"},
    "translation_atlas.md":   {"path": "sanskritree_corpus_targets/translation_atlas.md", "note": "the translation atlas"},
    "canonical_reference_map.md": {"path": "sanskritree_corpus_targets/canonical_reference_map.md", "note": "the reference map (traditions/transfer-nodes)"},
    "tradition_anchors.md":   {"path": "sanskritree_corpus_targets/tradition_anchors.md", "note": "tradition-conditional term senses + anchors"},
    "canonical_reference_map.md": {"path": "sanskritree_corpus_targets/canonical_reference_map.md", "note": "THE master substrate: taxonomy/timeline, canonical corpus with ingestion waves (A+/A/B), the semantic-shift glossary (kula/krama/śakti/vimarśa...), the auditable translation architecture, the tool map. The single most important reference for the autonomous translator."},
    "markguidance.md":       {"path": "sanskritree_corpus_targets/markguidance.md", "note": "the Recognition Enquiry research doc: passage dossiers (ĪPK/TA/Vākyapadīya...), the A/B/C thesis levels (reflexive presence / diachronic subjectivity / universal identity), cross-tradition mapping, discriminating predictions, the 50-70 verse passage-book deliverable. The argument-layer goldmine."},
    "leapfrog_map.md":        {"path": "sanskritree_corpus_targets/leapfrog_map.md", "note": "the corpus-ladder route"},
    "leapfrog_guide.md":      {"path": "sanskritree_corpus_targets/leapfrog_guide.md", "note": "the corpus-ladder engine design"},
    "markguidance.md":        {"path": "sanskritree_corpus_targets/markguidance.md", "note": "guidance"},
    "nonsaivatranslate.md":   {"path": "sanskritree_corpus_targets/nonsaivatranslate.md", "note": "non-Śaiva translation"},
    "batch_9_plan.md":        {"path": "sanskritree_corpus_targets/batch_9_plan.md", "note": "batch-9 plan"},
    "atlasflaws.md":          {"path": "sanskritree_corpus_targets/atlasflaws.md", "note": "atlas flaws"},
    "targetslogic.md":        {"path": "sanskritree_ref/targetslogic.md", "note": "targets logic"},
    "rasaleads.md":           {"path": "sanskritree_truth/rasaleads.md", "note": "rasa-thesis leads (different project?)"},
    "rasa-top-leads.md":      {"path": "sanskritree_truth/rasa-top-leads.md", "note": "rasa frontier leads"},
    "round2/MANIFEST.md":     {"path": "sanskritree_sources/round2/MANIFEST.md", "note": "round-2 downloaded sources"},
    "round3/MANIFEST.md":     {"path": "sanskritree_sources/round3/MANIFEST.md", "note": "round-3 downloaded sources"},
    "gretil2/MANIFEST.md":    {"path": "sanskritree_sources/gretil2/MANIFEST.md", "note": "GRETIL downloaded sources"},
    "siva-corpus-download-manifest.json": {"path": "patala_downloads/siva-corpus-download-manifest.json", "note": "the 15-work Śiva corpus download manifest"},
    "siva-corpus-inventory.json": {"path": "patala_downloads/siva-corpus-inventory.json", "note": "on-disk corpus inventory"},
    "translation-pipeline-inventory.json": {"path": "patala_downloads/translation-pipeline-inventory.json", "note": "existing T1/R1/T2/R2/T3/C1 works (easy wins)"},
    "translation-state-ledger.json": {"path": "patala_downloads/translation-state-ledger.json", "note": "the corpus-state ledger (NEXT_VALID_ACTION)"},
    "vision-11-siva-before-abhinava-corpus-manifest.md": {"path": "patala_vision_expansion/vision-11-siva-before-abhinava-corpus-manifest.md", "note": "the Śiva corpus acquisition plan (Vision 11)"},
}


def resolve(path: str) -> str:
    root = path.split("/", 1)[0]
    rest = path.split("/", 1)[1]
    return os.path.join(DOC_ROOTS[root], rest)


def build() -> dict:
    # sources.json: scan the actual downloaded source files
    sources = []
    for rel, note in [("round2", "round-2 verification+commentary"), ("round3", "round-3 acquisitions"),
                      ("gretil2", "GRETIL acquisitions")]:
        d = DOC_ROOTS["sanskritree_sources"] + rel
        if os.path.isdir(d):
            for f in sorted(os.listdir(d)):
                if f.endswith(".txt") or f.endswith(".pdf") or f.endswith(".json"):
                    sources.append({"file": f"{rel}/{f}", "group": rel, "note": note})
    # also the top-level sources/
    d = DOC_ROOTS["sanskritree_sources"]
    for f in sorted(os.listdir(d)):
        if f.endswith(".txt") or f.endswith(".pdf"):
            sources.append({"file": f, "group": "sources-root", "note": ""})

    # targets.json + leads.json from the registry
    import sys
    sys.path.insert(0, "/root/projects/patala/pipeline")
    import translation_targets as TT
    targets = {wid: meta for wid, meta in TT.TARGETS.items()}
    leads = {wid: meta for wid, meta in TT.LEADS.items()}

    # anchors.json: from translation_status_audit.md (parsed lightly — the anchor/status table)
    anchors = _parse_anchors()

    # index.json: the master doc index with links
    index = {"source_docs": {}, "count": 0}
    for name, meta in SOURCE_DOCS.items():
        p = resolve(meta["path"])
        exists = os.path.exists(p)
        index["source_docs"][name] = {
            "link": meta["path"], "note": meta["note"], "exists": exists,
            "exists_on_disk": exists,
        }
        if exists:
            index["count"] += 1

    # the second-corpus sivaqueue registry (100 targets + companion guides + term context)
    import sivaqueue_targets as SQ
    sivaqueue = {"targets": SQ.all_targets(), "n_targets": len(SQ.all_targets()),
                 "guides": SQ.guides(), "n_guides": len(SQ.guides()),
                 "summary": SQ.summary()}

    db = {
        "compiled": "2026-08-12",
        "sources": sources, "n_sources": len(sources),
        "targets": targets, "n_targets": len(targets),
        "leads": leads, "n_leads": len(leads),
        "anchors": anchors, "n_anchors": len(anchors),
        "sivaqueue": sivaqueue, "n_sivaqueue_targets": sivaqueue["n_targets"],
        "index": index,
    }
    for name, data in [("sources", sources), ("targets", targets), ("leads", leads),
                       ("anchors", anchors), ("sivaqueue", sivaqueue), ("index", index)]:
        with (OUT / f"{name}.json").open("w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
    return db


def _parse_anchors() -> dict:
    """Parse translation_status_audit.md into a structured anchor table (best-effort)."""
    anchors = {}
    p = resolve("sanskritree_corpus_targets/translation_status_audit.md")
    if not os.path.exists(p):
        return anchors
    for line in open(p, encoding="utf-8"):
        if line.startswith("|") and "Text" not in line and "---" not in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 4:
                text, status, anchor, loc = cells[0], cells[1], cells[2], cells[3] if len(cells) > 3 else ""
                if text and text != "Text":
                    anchors[text] = {"translation_status": status, "anchor": anchor, "location": loc}
    return anchors


if __name__ == "__main__":
    db = build()
    print(f"compiled corpus-targets DB:")
    print(f"  sources: {db['n_sources']}  targets: {db['n_targets']}  leads: {db['n_leads']}  anchors: {db['n_anchors']}")
    print(f"  source docs indexed: {db['index']['count']}")
    print(f"  -> {OUT}")
