#!/usr/bin/env python3
"""pipeline/ingest_sivaqueue34.py — compile the sivaqueue3/4 censuses into the target registry.

A2-NEXT (the intake step): turn the sivaqueue3 (pre-tantric historical spine) + sivaqueue4 (20
Vedic/transitional works) census docs into COMPILED target entries, so they can be acquired + ingested
into the factory queue. The original sivaqueue-targets.json holds the first 100; this adds sivaqueue3/4.

This is DETERMINISTIC (no network): it parses the census docs and writes a compiled manifest that the
acquisition step (acquire_sivaqueue_targets.py, extended) consumes. The actual source-fetch (GRETIL /
archive.org) is a separate, network-dependent step.

Output:
  data/corpus/sivaqueue34-targets.json     {targets: {work_id: {section, tradition, translation_status, source_links, note}}}
  data/corpus/downloads/sivaqueue34-intake-report.json   {compiled, by_section, acquirable_hint}

Usage:
  python3 pipeline/ingest_sivaqueue34.py [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path("/root/projects/patala")
OUT = ROOT / "data/corpus/sivaqueue34-targets.json"
REPORT = ROOT / "data/corpus/downloads/sivaqueue34-intake-report.json"
DOCS = ROOT / "docs/corpus"

# acquirable-hint: sources that are public machine-readable e-texts (GRETIL, archive.org) vs
# editions needing manual acquisition. Keyed by substring; conservative.
PUBLIC_ETEXT_HINTS = ["gretil", "archive.org", "vedicheritage.gov.in", "titus.uni-frankfurt"]


def _slug(title: str) -> str:
    """work_id slug from a title: lowercase, keep alpha, underscores."""
    s = title.lower()
    s = re.sub(r"[^a-zāīūṛṝḷḹṃñṅśṣṭḍḥṁ0-9 ]", " ", s)
    s = re.sub(r"\s+", "_", s).strip("_")
    # strip diacritics for a safe id
    for a, b in [("ā", "a"), ("ī", "i"), ("ū", "u"), ("ṛ", "r"), ("ṝ", "r"), ("ḷ", "l"),
                 ("ḹ", "l"), ("ṃ", "m"), ("ñ", "n"), ("ṅ", "n"), ("ś", "s"), ("ṣ", "s"),
                 ("ṭ", "t"), ("ḍ", "d"), ("ḥ", "h"), ("ṁ", "m")]:
        s = s.replace(a, b)
    return s[:50]


def _parse_section(doc: Path) -> list[dict]:
    """Parse a census doc into {section, title, sources, translation_status, verdict}."""
    entries = []
    text = doc.read_text(encoding="utf-8")
    lines = text.splitlines()
    cur_section = None
    cur_title = None
    cur_sources = []
    cur_status = ""
    cur_verdict = ""

    def flush():
        if cur_title:
            entries.append({"section": cur_section or "?", "title": cur_title,
                            "sources": cur_sources, "translation_status": cur_status,
                            "verdict": cur_verdict})

    for ln in lines:
        s = ln.strip()
        m = re.match(r"^#{1,2}\s+(.+)$", s)
        if m:
            flush()
            cur_section = m.group(1).strip()
            cur_title = None; cur_sources = []; cur_status = ""; cur_verdict = ""
            continue
        # a bold work title like "## 1. Maitrāyaṇī Saṃhitā" (already section) or "**Title**"
        m = re.match(r"^\*\*(.+?)\*\*\s*$", s)
        if m and not s.startswith("#"):
            flush()
            cur_title = m.group(1).strip()
            cur_sources = []; cur_status = ""; cur_verdict = ""
            continue
        # "Verdict:" line
        m = re.match(r"^Verdict:\s*(.+)$", s)
        if m:
            cur_verdict = m.group(1).strip()
            continue
        # source link lines
        if "http" in s:
            cur_sources.append(s)
        # status lines
        if re.match(r"^(English|Sanskrit e-text|Verdict):", s):
            cur_status = s
    flush()
    return entries


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    targets = {}
    by_section = {}
    for fn in ("sivaqueue3-translation-guide.md", "sivaqueue4-translation-guide.md"):
        doc = DOCS / fn
        if not doc.exists():
            print(f"missing {fn}", file=sys.stderr)
            continue
        for e in _parse_section(doc):
            wid = _slug(e["title"])
            if not wid:
                continue
            links = " ".join(e["sources"]).lower()
            acquirable = any(h in links for h in PUBLIC_ETEXT_HINTS)
            targets[wid] = {
                "source_census": fn.replace("-translation-guide.md", ""),
                "title": e["title"],
                "section": e["section"],
                "sources": e["sources"],
                "translation_status": e["translation_status"][:80] if e["translation_status"] else "unknown",
                "verdict": e["verdict"][:120] if e["verdict"] else "",
                "public_e_text_hint": acquirable,
            }
            by_section.setdefault(e["section"] or "?", 0)
            by_section[e["section"] or "?"] += 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"source": ["sivaqueue3", "sivaqueue4"],
                               "compiled": "2026-08-13", "targets": targets},
                              indent=2, ensure_ascii=False), encoding="utf-8")
    report = {"compiled": len(targets), "by_section": by_section,
              "public_e_text_hint": sum(1 for t in targets.values() if t["public_e_text_hint"]),
              "needs_manual": sum(1 for t in targets.values() if not t["public_e_text_hint"])}
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    if a.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"compiled {len(targets)} sivaqueue3/4 targets")
        print(f"  public e-text hint (acquirable): {report['public_e_text_hint']}")
        print(f"  needs manual acquisition:       {report['needs_manual']}")
        print(f"  wrote {OUT}")
        print(f"  wrote {REPORT}")
        print("\nsample targets:")
        for wid, t in list(targets.items())[:8]:
            print(f"  {wid:35s} {t['section'][:30]:32s} e-text={t['public_e_text_hint']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
