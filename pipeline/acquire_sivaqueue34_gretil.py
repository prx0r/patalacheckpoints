#!/usr/bin/env python3
"""pipeline/acquire_sivaqueue34_gretil.py — download the clean machine-readable GRETIL e-texts.

The sivaqueue3/4 census (data/corpus/sivaqueue34-targets.json) lists many Vedic source materials.
Most are scan PDFs needing OCR; a subset are clean, machine-readable GRETIL e-texts (transliterated
IAST) that fit the factory's per-work translation queue directly.

This downloads each GRETIL e-text, strips the HTML to the IAST Sanskrit body, and writes it to
data/corpus/sources/<work_id>/<work_id>.txt — the canonical addressable source location. The
factory's corpus_state discovery auto-registers any such file, so the work enters the queue.

Usage:
  python3 pipeline/acquire_sivaqueue34_gretil.py [--dry-run] [--work <id>]
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data/corpus/sources"

# sivaqueue34 GRETIL e-text -> (work_id, short title)
# Verified direct e-text URLs from the census (deduplicated, no utm params).
TARGETS = {
    "maitrayanisamhita": ("https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/1_veda/1_sam/maitrs_pu.htm", "Maitrāyaṇī Saṃhitā"),
    "kausitakibrahmana": ("https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/1_veda/2_bra/kausibru.htm", "Kauṣītaki Brāhmaṇa"),
    "pancavimsabrahmana": ("https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_paJcaviMzabrAhmaNa.htm", "Pañcaviṃśa Brāhmaṇa"),
    "sankhayanaaranyaka": ("https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_zaGkhAyana-AraNyaka.htm", "Śāṅkhāyana Āraṇyaka"),
    "atharvasiraupanisad": ("https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/1_veda/4_upa/sirup_u.htm", "Atharvaśira Upaniṣad"),
    "siraupanisad": ("https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_zira-upaniSad.htm", "Śira Upaniṣad (Atharvaśira)"),
    "kaivalyaupanisad": ("https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/1_veda/4_upa/kaivup_u.htm", "Kaivalya Upaniṣad"),
    "sivaupanisad": ("https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/4_rellit/saiva/sivup_pu.htm", "Śiva Upaniṣad"),
    "lingapurana": ("https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/3_purana/lip_2__u.htm", "Liṅga Purāṇa (2,1–55)"),
    "kurmapurana": ("https://gretil.sub.uni-goettingen.de/gretil/1_sanskr/3_purana/kurmp2_u.htm", "Kūrma Purāṇa Part 2"),
}


def _strip_html(html: str) -> str:
    """Extract the IAST Sanskrit body from a GRETIL HTML page."""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "head", "title"]):
            tag.decompose()
        text = soup.get_text("\n")
    except Exception:
        # stdlib fallback: drop tags, keep text
        text = re.sub(r"<[^>]+>", "\n", html)
    lines = []
    for line in text.splitlines():
        s = line.strip()
        # keep lines that are mostly transliterated Sanskrit
        iast = len(re.findall(r"[āīūṛṝḷḹṃñṅśṣṭḍḥṁ]", s))
        if iast >= 3 and len(re.findall(r"[A-Za-zāīūṛṝḷḹṃñṅśṣṭḍḥ]", s)) > 10:
            lines.append(s)
    return "\n".join(lines)


def fetch(url: str, out: Path) -> bool:
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["curl", "-sL", "-m", "240", "-A", "Mozilla/5.0 (X11; Linux x86_64)",
           "-o", str(out), url]
    r = subprocess.run(cmd)
    return r.returncode == 0 and out.exists() and out.stat().st_size > 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="report targets only (no download)")
    ap.add_argument("--work", default=None, help="download just this work_id")
    a = ap.parse_args()

    ids = [a.work] if a.work else sorted(TARGETS.keys())

    for wid in ids:
        if wid not in TARGETS:
            print(f"unknown work_id {wid}; known: {sorted(TARGETS)}")
            continue
        url, title = TARGETS[wid]
        if a.dry_run:
            print(f"{wid:24} would fetch {title} from {url}")
            continue
        raw = OUT / wid / f"{wid}.html"
        if not fetch(url, raw):
            print(f"FAIL {wid}: could not fetch {url}")
            continue
        text = _strip_html(raw.read_text(encoding="utf-8", errors="ignore"))
        if not text:
            print(f"FAIL {wid}: no IAST Sanskrit extracted from {raw}")
            continue
        (OUT / wid).mkdir(parents=True, exist_ok=True)
        (OUT / wid / f"{wid}.txt").write_text(text, encoding="utf-8")
        print(f"OK   {wid}: {len(text)} chars, {title}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
