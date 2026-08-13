#!/usr/bin/env python3
"""pipeline/download_sanderson.py — reproducible downloader for the Sanderson corpus.

Reads data/corpus/sources/sanderson/sanderson_manifest.json and fetches every work whose
`direct` flag is true (non-Academia, scriptable URL). Academia items (behind a Cloudflare
bot-challenge) are NOT fetched here — they are recorded as manual_academia in the manifest.

Usage:
  python3 pipeline/download_sanderson.py [--dir data/corpus/sources/sanderson]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def fetch(url: str, out: Path) -> bool:
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["curl", "-sL", "-m", "240", "-A", "Mozilla/5.0 (X11; Linux x86_64)",
           "-o", str(out), url]
    r = subprocess.run(cmd)
    ok = r.returncode == 0 and out.exists() and out.stat().st_size > 0
    print(("OK " if ok else "FAIL ") + str(out))
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(ROOT / "data/corpus/sources/sanderson"))
    a = ap.parse_args()
    d = Path(a.dir)
    manifest = json.load(open(d / "sanderson_manifest.json"))

    ok = fail = 0
    for w in manifest["works"]:
        if not w.get("direct"):
            continue
        url = w.get("url", "")
        if not url:
            continue
        name = w.get("downloaded_file") or (w["key"] + ".pdf")
        if fetch(url, d / name):
            ok += 1
        else:
            fail += 1
    print(f"\ndirect downloads: ok={ok} fail={fail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
