#!/usr/bin/env python3
"""pipeline/build_sivaqueue_gap_atlas.py — generate data/atlas/sivaqueueGapSeed.ts.

One-time generator: adds BibliographyRecords for the on-disk works that were MISSING from the
atlas (the 'no atlas record' LOW bucket surfaced by source_ready.py). These are real Sanskrit
texts with on-disk sources but no bibliography entry, so they were invisible to the catalog/API
and mis-prioritised as LOW.

Metadata is transcribed from the sivaqueue access-manifest (sivaqueue-access-manifest.json) +
the on-disk source headers. verified:false = seed.

Run: python3 pipeline/build_sivaqueue_gap_atlas.py   (writes data/atlas/sivaqueueGapSeed.ts)
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("/root/projects/patala")
OUT = ROOT / "data/atlas" / "sivaqueueGapSeed.ts"

RECORDS = [
    dict(id="matangaparamesvara", work="Mataṅgapārameśvara",
         traditions=["Śaiva Siddhānta"], subschool="early Siddhānta",
         period=dict(start=700, end=1000, approximate=True), author="anonymous scripture",
         register="early Siddhānta Sanskrit",
         sources=[dict(type="etext", provider="Muktabodha", url="https://muktabodha-digital-library.org", note="Rāmakaṇṭha tradition; on-disk IAST", tier="C")],
         translations=[], verdict="TRANSLATE (early Siddhānta ontology/cosmology; partial English)"),
    dict(id="ramakantha_matangavrtti", work="Rāmakaṇṭha's Mataṅgavṛtti (untranslated sections)",
         traditions=["Kashmirian Śaiva Siddhānta"], subschool="early Siddhānta",
         period=dict(start=950, end=1050, approximate=True), author="Rāmakaṇṭha II",
         register="Classical Śaiva Siddhānta Sanskrit",
         sources=[dict(type="etext", provider="Muktabodha", url="https://muktabodha-digital-library.org", note="on-disk IAST", tier="C")],
         translations=[], verdict="TRANSLATE (untranslated sections of the Mataṅgavṛtti)"),
    dict(id="naresvarapariksa", work="Nareśvaraparīkṣā — Sadyojyotis + Rāmakaṇṭha's Prakāśa",
         traditions=["Śaiva Siddhānta"], subschool="Aṣṭaprakaraṇa",
         period=dict(start=800, end=1000, approximate=True), author="Sadyojyotis; Rāmakaṇṭha commentary",
         register="Classical Śaiva Siddhānta Sanskrit",
         sources=[dict(type="scan", provider="eGangotri/Sarayu Trust", url="https://www.egangotri.org/", note="on-disk Devanagari scan text", tier="D")],
         translations=[], verdict="TRANSLATE (Sadyojyotis philosophical verification)"),
    dict(id="siddhantasara", work="Siddhāntasāra",
         traditions=["Śaiva Siddhānta"], subschool="Aṣṭaprakaraṇa",
         period=dict(approximate=True), author="anonymous/commentarial",
         register="Classical Śaiva Siddhānta Sanskrit",
         sources=[dict(type="etext", provider="Muktabodha", url="https://muktabodha-digital-library.org", note="CC BY-NC 4.0; on-disk IAST", tier="C")],
         translations=[], verdict="TRANSLATE / VERIFY identity (Śaiva Siddhānta compendium)"),
    dict(id="aghorasiva_ashtaprakarana_corpus", work="Aghoraśiva's doctrinal commentarial corpus (Aṣṭaprakaraṇa)",
         traditions=["Śaiva Siddhānta"], subschool="Aṣṭaprakaraṇa",
         period=dict(start=1100, end=1200, approximate=True), author="Aghoraśivācārya",
         register="Classical Śaiva Siddhānta Sanskrit",
         sources=[dict(type="etext", provider="Muktabodha/SSI", url="https://muktabodha-digital-library.org", note="Yogatantra-granthamālā; on-disk", tier="C")],
         translations=[], verdict="INGEST (Aghoraśiva's 8-prakaraṇa commentary corpus)"),
    dict(id="aghorasiva_tattvaprakasika", work="Aghoraśiva's Tattvaprakāśikā",
         traditions=["Śaiva Siddhānta"], subschool="Aṣṭaprakaraṇa",
         period=dict(start=1100, end=1200, approximate=True), author="Aghoraśivācārya",
         register="Classical Śaiva Siddhānta Sanskrit",
         sources=[dict(type="etext", provider="Muktabodha/SSI", url="https://muktabodha-digital-library.org", note="on-disk", tier="C")],
         translations=[], verdict="TRANSLATE (Aghoraśiva on the Tattvaprakāśa)"),
    dict(id="aghorasiva_tattvasamgrahalaghutika", work="Aghoraśiva's Tattvasaṃgrahalaghuṭīkā",
         traditions=["Śaiva Siddhānta"], subschool="Aṣṭaprakaraṇa",
         period=dict(start=1100, end=1200, approximate=True), author="Aghoraśivācārya",
         register="Classical Śaiva Siddhānta Sanskrit",
         sources=[dict(type="etext", provider="Muktabodha/SSI", url="https://muktabodha-digital-library.org", note="on-disk", tier="C")],
         translations=[], verdict="TRANSLATE (Aghoraśiva's short commentary on the Tattvasaṃgraha)"),
    dict(id="ratnatrayapariksa_vyakhya", work="Anonymous Ratnatrayaparīkṣā-vyākhyā",
         traditions=["Śaiva Siddhānta"], subschool="Aṣṭaprakaraṇa",
         period=dict(approximate=True), author="anonymous (medieval Siddhānta)",
         register="Classical Śaiva Siddhānta Sanskrit",
         sources=[dict(type="etext", provider="Muktabodha/SSI", url="https://muktabodha-digital-library.org", note="on-disk", tier="C")],
         translations=[], verdict="TRANSLATE (commentary on Ratnatrayaparīkṣā)"),
    dict(id="aghorasivas_ullekhini_on_ratnatraya", work="Aghoraśiva's Ullekhinī on the Ratnatraya",
         traditions=["Śaiva Siddhānta"], subschool="Aṣṭaprakaraṇa",
         period=dict(start=1100, end=1200, approximate=True), author="Aghoraśivācārya",
         register="Classical Śaiva Siddhānta Sanskrit",
         sources=[dict(type="etext", provider="Muktabodha", url="https://muktabodha-digital-library.org", note="on-disk IAST", tier="C")],
         translations=[], verdict="TRANSLATE (Aghoraśiva's gloss on Ratnatraya)"),
    dict(id="anonymous_ratnatrayapariksavyakhya", work="Anonymous Ratnatrayaparīkṣā-vyākhyā (variant)",
         traditions=["Śaiva Siddhānta"], subschool="Aṣṭaprakaraṇa",
         period=dict(approximate=True), author="anonymous",
         register="Classical Śaiva Siddhānta Sanskrit",
         sources=[dict(type="etext", provider="Muktabodha", url="https://muktabodha-digital-library.org", note="on-disk IAST", tier="C")],
         translations=[], verdict="TRANSLATE / VERIFY identity (duplicate of Ratnatraya vyākhyā?)"),
    dict(id="mukuta_makutagama", work="Mukuṭa / Makuṭāgama (early recension)",
         traditions=["early Siddhānta"], subschool="Siddhānta Āgama",
         period=dict(start=600, end=900, approximate=True), author="anonymous scripture",
         register="Early Siddhānta Sanskrit",
         sources=[dict(type="etext", provider="Muktabodha", url="https://muktabodha-digital-library.org", note="on-disk Devanagari", tier="C")],
         translations=[], verdict="TRANSLATE (early Siddhānta ritual corpus)"),
    dict(id="devikalottaragama", work="Devīkālottarāgama",
         traditions=["Kālīkula/Śākta"], subschool="early Kālīkula",
         period=dict(start=700, end=900, approximate=True), author="anonymous scripture",
         register="early tantric Sanskrit",
         sources=[dict(type="etext", provider="Muktabodha", url="https://muktabodha-digital-library.org", note="on-disk", tier="C")],
         translations=[], verdict="TRANSLATE (Kālīkula ritual/theology)"),
    dict(id="matrkabhedatantra", work="Mātṛkābhedatantra",
         traditions=["Bhairava/Śākta"], subschool="Vidyāpīṭha",
         period=dict(start=800, end=1100, approximate=True), author="anonymous scripture",
         register="early tantric Sanskrit",
         sources=[dict(type="etext", provider="Muktabodha", url="https://muktabodha-digital-library.org", note="on-disk", tier="C")],
         translations=[], verdict="TRANSLATE (Mātṛkā mysticism)"),
    dict(id="visvaksenasamhita", work="Viṣvaksenasaṃhitā",
         traditions=["Vaiṣṇava Pāñcarātra"], subschool="Pāñcarātra saṃhitā",
         period=dict(start=700, end=1000, approximate=True), author="anonymous scripture",
         register="Pāñcarātra Sanskrit",
         sources=[dict(type="etext", provider="Muktabodha", url="https://muktabodha-digital-library.org", note="on-disk", tier="C")],
         translations=[], verdict="TRANSLATE (Pāñcarātra; Vaiṣṇava counterpart for control)"),
    dict(id="siraupanisad", work="Śira Upaniṣad (= Atharvaśira)",
         traditions=["early Rudra-Śaiva Upaniṣadic"], subschool="Atharvavedic affiliation",
         period=dict(start=-100, end=100, approximate=True), author="Anonymous",
         register="Late Upaniṣadic/sectarian Sanskrit",
         sources=[dict(type="etext", provider="GRETIL", url="https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_zira-upaniSad.htm", note="on-disk; duplicate of atharvasiraupanisad", tier="C")],
         translations=[], verdict="MERGE with atharvasiraupanisad (duplicate id)"),
    dict(id="pratisThakriyadipika", work="Pratiṣṭhākriyādīpikā",
         traditions=["Śaiva Siddhānta"], subschool="Pratiṣṭhā/ritual",
         period=dict(approximate=True), author="anonymous/ritual",
         register="Classical Śaiva Siddhānta Sanskrit",
         sources=[dict(type="etext", provider="Muktabodha", url="https://muktabodha-digital-library.org", note="CC BY-NC 4.0; on-disk IAST", tier="C")],
         translations=[], verdict="TRANSLATE (temple-consecration ritual)"),
    dict(id="pratisThalaksanasara", work="Pratiṣṭhālakṣaṇasāra",
         traditions=["Śaiva Siddhānta"], subschool="Pratiṣṭhā/ritual",
         period=dict(approximate=True), author="anonymous/ritual",
         register="Classical Śaiva Siddhānta Sanskrit",
         sources=[dict(type="etext", provider="Muktabodha", url="https://muktabodha-digital-library.org", note="CC BY-NC 4.0; on-disk IAST", tier="C")],
         translations=[], verdict="TRANSLATE (consecration-lakṣaṇa manual)"),
    dict(id="pratisThaparamesvara", work="Pratiṣṭhāparameśvara",
         traditions=["Śaiva Siddhānta"], subschool="Pratiṣṭhā/ritual",
         period=dict(approximate=True), author="anonymous/ritual",
         register="Classical Śaiva Siddhānta Sanskrit",
         sources=[dict(type="etext", provider="Muktabodha", url="https://muktabodha-digital-library.org", note="CC BY-NC 4.0; on-disk IAST", tier="C")],
         translations=[], verdict="TRANSLATE (temple-ritual manual)"),
    dict(id="ramakantha_moksakarikavrtti", work="Rāmakaṇṭha's Mokṣakārikāvṛtti",
         traditions=["Śaiva Siddhānta"], subschool="Aṣṭaprakaraṇa",
         period=dict(start=950, end=1050, approximate=True), author="Rāmakaṇṭha II",
         register="Classical Śaiva Siddhānta Sanskrit",
         sources=[dict(type="etext", provider="Muktabodha", url="https://muktabodha-digital-library.org", note="on-disk", tier="C")],
         translations=[], verdict="TRANSLATE (commentary on Mokṣakārikā)"),
]


def _period_json(p) -> str:
    parts = []
    if p.get("start") is not None:
        parts.append(f'"start": {p["start"]}')
    if p.get("end") is not None:
        parts.append(f'"end": {p["end"]}')
    if p.get("approximate"):
        parts.append('"approximate": true')
    return "{" + ", ".join(parts) + "}"


def _sources_js(sources) -> str:
    items = []
    for s in sources:
        parts = [f'"type": "{s["type"]}"', f'"provider": "{s["provider"]}"', f'"url": "{s["url"]}"']
        if s.get("note"):
            parts.append(f'"note": "{s["note"]}"')
        if s.get("tier"):
            parts.append(f'"tier": "{s["tier"]}"')
        items.append("{" + ", ".join(parts) + "}")
    return "[" + ", ".join(items) + "]"


def _record_js(r) -> str:
    lines = [
        '{', f'  "id": "{r["id"]}",',
        f'  "work": "{r["work"]}",',
        f'  "traditions": {json.dumps(r["traditions"], ensure_ascii=False)},',
    ]
    if r.get("subschool"):
        lines.append(f'  "subschool": "{r["subschool"]}",')
    if r.get("period"):
        lines.append(f'  "period": {_period_json(r["period"])},')
    lines.append('  "verified": false,')
    lines.append('  "state": "seed",')
    lines.append(f'  "author": "{r.get("author", "")}",')
    lines.append(f'  "register": "{r.get("register", "")}",')
    lines.append(f'  "textSources": {_sources_js(r.get("sources", []))},')
    lines.append('  "translations": [],')
    lines.append('  "translationStatus": "none",')
    lines.append('  "statusLabel": "No complete scholarly English translation located as of 2026-08-13",')
    lines.append('  "statusChecked": "2026-08-13",')
    lines.append(f'  "verdict": "{r.get("verdict", "")}",')
    lines.append('}')
    return "\n".join(lines)


def main() -> int:
    body = ",\n".join("  " + _record_js(r) for r in RECORDS)
    header = (
        "// Auto-generated 2026-08-13: on-disk works missing from the atlas (the source_ready\n"
        "// 'no atlas record' LOW bucket). Real Sanskrit texts with on-disk sources but no\n"
        "// bibliography entry. Metadata from sivaqueue-access-manifest.json + source headers.\n"
        "// verified:false = seed. Generated by pipeline/build_sivaqueue_gap_atlas.py.\n\n"
        'import { BibliographyRecord } from "./bibliographyTypes";\n\n'
        "export const sivaqueueGapSeed: BibliographyRecord[] = [\n"
    )
    footer = "\n];\n"
    OUT.write_text(header + body + footer, encoding="utf-8")
    print(f"wrote {OUT} with {len(RECORDS)} records")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
