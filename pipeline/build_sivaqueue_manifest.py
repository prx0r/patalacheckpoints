#!/usr/bin/env python3
"""pipeline/build_sivaqueue_manifest.py — build the sivaqueue download/access manifest.

For each of the 100 "Śiva before Abhinava" targets, record:
  - on_disk: is a Sanskrit text for it already on the sanskritree mount? (with the file path)
  - access_source / download_url: where to get it (from the original sivaqueue guide's Source column)
  - source_gateway: the gateway (muktabodha / gretil / ifpindia / vishvasa / shivadharmaproject / ...)

This is the quick-access map: a target whose text is already on disk can go straight to RAW-L0; a
target that isn't has its acquisition link recorded. Companion guides (G1-G14) are editions (IFP
books) — recorded separately as translation-memory references, not raw-source downloads.

Output: data/corpus/sivaqueue-access-manifest.json
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = "/root/projects/patala"
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import sivaqueue_targets as SQ

GUIDE = os.path.join(ROOT, "docs/corpus/sivaqueue-translation-guide.md")
OUT = os.path.join(ROOT, "data/corpus/sivaqueue-access-manifest.json")

SOURCES_ROOT = "/mnt/HC_Volume_106427611/sanskritree/sources"

# gateway root URLs (the quick-access homes)
GATEWAYS = {
    "muktabodha": "https://muktabodha-digital-library.org",
    "gretil": "https://gretil.sub.uni-goettingen.de",
    "ifpindia": "https://ifpindia.org/bookstore",
    "digitalcollections.ifpindia": "https://digitalcollections.ifpindia.org/s/manuscripts",
    "vishvasa": "https://vishvasa.github.io/AgamaH_shaivaH",
    "shivadharmaproject": "https://shivadharmaproject.com",
    "springer": "https://link.springer.com",
    "shaivism.net": "https://shaivism.net",
    "sarit": "https://sarit.indology.info",
    "wisdomlib": "https://www.wisdomlib.org",
}


def _norm(s: str) -> str:
    t = {'ā':'a','ī':'i','ū':'u','ṛ':'r','ṝ':'r','ḷ':'l','ḹ':'l','ṃ':'m','ñ':'n','ṅ':'n',
         'ś':'s','ṣ':'s','ṭ':'t','ḍ':'d','ḥ':'h','ṁ':'m'}
    s = ''.join(t.get(c, c) for c in s.lower())
    return re.sub(r'[^a-z0-9]', '', s)


def _on_disk_pool() -> list[tuple[str, str]]:
    pool = []
    for d in ['muktabodha-lib', 'gretil2', 'round2', 'round3']:
        base = os.path.join(SOURCES_ROOT, d)
        if os.path.isdir(base):
            pool += [(os.path.join(d, f), _norm(f)) for f in os.listdir(base) if f.endswith('.txt')]
    for f in os.listdir(SOURCES_ROOT):
        if f.endswith('.txt'):
            pool.append((f, _norm(f)))
    return pool


def _find_on_disk(name: str, pool: list[tuple[str, str]]) -> str | None:
    nm = _norm(name)
    best = None
    for path, pn in pool:
        for size in (14, 12, 10, 8):
            a = nm[:size]
            if len(a) >= 8 and a in pn:
                best = path
                break
        if best:
            break
    return best


def _extract_url(target_num: int, guide_text: str) -> str | None:
    """Find the first http URL on the guide line mentioning this target number."""
    # lines look like '|  **1** | **Pañcārthabhāṣya...** | ... | [url](url) |'
    for line in guide_text.splitlines():
        if f"**{target_num}**" in line and "http" in line:
            m = re.search(r'\[(https?://[^\s)]+)\]', line)
            if m:
                return m.group(1)
    return None


def build() -> dict:
    targets = SQ.all_targets()
    guide_text = Path(GUIDE).read_text(encoding="utf-8")
    pool = _on_disk_pool()
    rows = {}
    for wid, m in targets.items():
        disk = _find_on_disk(m["name"], pool)
        url = _extract_url(m["num"], guide_text)
        source = m.get("source", "")
        gateway = source if source in GATEWAYS else ("muktabodha" if "mukta" in source else source)
        rows[wid] = {
            "work_id": wid, "name": m["name"], "num": m["num"], "section": m["section"],
            "tradition": m["tradition"], "period": m["period"],
            "translation_status": m["translation_status"],
            "on_disk": bool(disk), "disk_path": disk,
            "source_gateway": gateway, "download_url": url,
            "companion_guides": m.get("companion_guides", []),
        }
    manifest = {
        "$schema": "patala:corpus:sivaqueue:access:v1",
        "note": "Quick-access map for the 100 'Śiva before Abhinava' targets. on_disk=true means a "
                "Sanskrit text is already on the sanskritree mount (go straight to RAW-L0); "
                "download_url is the acquisition link from the original sivaqueue guide. "
                "Companion guides G1-G14 are IFP/edition translation-memory references, not raw downloads.",
        "gateways": GATEWAYS,
        "n_targets": len(rows),
        "n_on_disk": sum(1 for r in rows.values() if r["on_disk"]),
        "targets": rows,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
    return manifest


if __name__ == "__main__":
    m = build()
    print(json.dumps({k: m[k] for k in ("n_targets", "n_on_disk", "gateways")}, indent=2, ensure_ascii=False))
    print(f"wrote {OUT}")
