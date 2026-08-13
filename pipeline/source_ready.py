#!/usr/bin/env python3
"""pipeline/source_ready.py — quick "is this work clean + ready + worth translating?" signal.

One command, per work or all: answers the two questions we actually care about:

  1. CLEAN — is the on-disk Sanskrit source actually usable?
       * IAST or Devanagari density (real Sanskrit, not a scan/OCR-mess)
       * extractable verse/passage count
       * low noise (not mostly page headers/footnotes/English)
  2. READY — is it registered so the factory will process it?
       * in the ledger as RAW_SANSKRIT with an on-disk source
       * has committed SOURCE objects (in the factory queue)
  3. PRIORITY — copyright-aware translation value:
       * NO English at all          -> HIGH (fill the gap, own the translation)
       * English but under copyright -> HIGH (you want YOUR translation to publish on the site)
       * public-domain English      -> MEDIUM (you can link it; translating is optional)
       * unknown/no info            -> LOW (needs a human check)

Usage:
  python3 pipeline/source_ready.py --work tantraloka
  python3 pipeline/source_ready.py --all            # table, sorted by priority
  python3 pipeline/source_ready.py --all --json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path("/root/projects/patala")
sys.path.insert(0, str(ROOT / "pipeline"))

import object_registry as R

SOURCES = ROOT / "data/corpus/sources"
# indicators a translation is likely public-domain (old / archive / sacred-texts / web), vs
# a modern copyrighted scholarly translation (publisher site, paywall, recent academic edition).
_PD_HINTS = ("archive.org", "sacred-texts", "gutenberg", "wisdomlib", "upasanayoga",
             "ia", ".pdf", "gretil")
_CORY_HINTS = ("oup.com", "pupress", "sunypress", "cambridge", "academic", "efeo.fr",
               "ifpindia.org/bookstore", "brill", "doi.org", "taylorfrancis",
               "anuttaratrikakula", "personal", "wordpress", "blogspot")


def _work_source_file(wid: str) -> Path | None:
    # prefer the ledger's authoritative source_ref (may be on the mount or data/corpus/sources)
    ledger = json.loads((ROOT / "data/corpus/downloads/translation-state-ledger.json").read_text())["works"]
    w = ledger.get(wid, {})
    ref = (w.get("source") or {}).get("source_ref")
    if ref and os.path.exists(ref):
        return Path(ref)
    p = SOURCES / wid / f"{wid}.txt"
    return p if p.is_file() else None


def _clean_signal(wid: str) -> dict:
    p = _work_source_file(wid)
    if not p:
        return {"on_disk": False, "clean": False, "reason": "no on-disk source"}
    txt = p.read_text(encoding="utf-8", errors="ignore")
    iast = len(re.findall(r"[āīūṛṝḷḹṃñṅśṣṭḍḥṁ]", txt))
    deva = len(re.findall(r"[\u0900-\u097F]", txt))
    sanskrit_chars = iast + deva
    lines = [l for l in txt.splitlines() if l.strip()]
    # verse/passage markers
    verses = sum(1 for l in lines if re.search(r"[।|]{1,2}", l) or re.search(r"\d", l))
    size = len(txt)
    if sanskrit_chars == 0:
        clean, reason = False, "no Sanskrit chars (not IAST/Devanagari — maybe OCR-mess or English)"
    elif sanskrit_chars < 50 and size > 2000:
        clean, reason = False, f"very low Sanskrit density ({sanskrit_chars} chars)"
    elif size < 1000:
        clean, reason = False, f"too small ({size} chars)"
    else:
        clean, reason = True, "looks like clean Sanskrit"
    return {"on_disk": True, "size": size, "iast": iast, "devanagari": deva,
            "sanskrit_chars": sanskrit_chars, "lines": len(lines), "verse_hint": verses,
            "clean": clean, "reason": reason}


def _ready_signal(wid: str) -> dict:
    ledger = json.loads((ROOT / "data/corpus/downloads/translation-state-ledger.json").read_text())["works"]
    w = ledger.get(wid, {})
    src = w.get("source", {})
    in_ledger = bool(w) and src.get("available") and src.get("format") == "RAW_SANSKRIT"
    has_source_objs = any(oid.startswith(wid) for oid in R._load("SOURCE")["objects"])
    t1 = R._load("T1")["objects"]
    t1_count = sum(1 for oid in t1 if oid.startswith(wid) and R.current("T1", oid))
    return {"in_ledger": in_ledger, "next_action": w.get("next_action", {}).get("action") if w else None,
            "has_source_objects": has_source_objs, "t1_committed": t1_count}


def _priority_for(status: str, urls: list[str]) -> tuple[str, str]:
    """Copyright-aware priority from translation coverage + source urls."""
    pd = any(any(h in u for h in _PD_HINTS) for u in urls)
    cory = any(any(h in u for h in _CORY_HINTS) for u in urls)
    if status == "none":
        return "HIGH", "no English translation found — own translation fills the gap"
    if cory:
        return "HIGH", "English exists but under copyright — translate your own to publish"
    if status == "complete" and pd:
        return "MEDIUM", "complete public-domain English available — you can link it; translating optional"
    if status == "complete":
        return "MEDIUM", "complete English exists — check copyright; own translation still valuable for publishing"
    if status == "partial":
        return "HIGH", "only partial English — own translation fills the gap"
    return "LOW", "translation status unclear — verify before deciding"


def _translation_signal(wid: str) -> dict:
    """Determine English-coverage + copyright status from the atlas."""
    rec = None
    for fn in ("audited.ts", "bibliographySeed.ts", "sivaqueueSeed.ts", "sivaqueue34Seed.ts"):
        p = ROOT / "data/atlas" / fn
        if not p.exists():
            continue
        txt = p.read_text(encoding="utf-8")
        # find the record: an object whose id equals wid (either '"id": "wid"' or 'id: "wid"')
        for m in re.finditer(r'"?id"?\s*:\s*"' + re.escape(wid) + r'"(,?)', txt):
            # find the nearest '{' before the id (the record's opening brace)
            start = txt.rfind("{", 0, m.start())
            depth = 0
            for i in range(start, len(txt)):
                c = txt[i]
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        rec = txt[start:i + 1]
                        break
            if rec:
                break
        if rec:
            break
    if not rec:
        return {"has_atlas": False, "english": "unknown", "copyright": "unknown",
                "priority": "LOW", "why": "no atlas record — check manually"}
    status = "unknown"
    sm = re.search(r'"translationStatus"\s*:\s*"(\w+)"', rec) or re.search(r'translationStatus\s*:\s*"(\w+)"', rec)
    if sm:
        status = sm.group(1)
    # look at translation urls for copyright hints (only the translations[], not textSources)
    tblock = re.search(r'translations\s*:\s*\[(.*?)\]\s*,', rec, re.S)
    urls = re.findall(r'"(https?://[^"]+)"', tblock.group(1)) if tblock else []
    has_translation_urls = bool(urls)
    priority, why = _priority_for(status, urls)
    return {"has_atlas": True, "english": status, "has_translation_urls": has_translation_urls,
            "pd_hint": any(any(h in u for h in _PD_HINTS) for u in urls),
            "copyright_hint": any(any(h in u for h in _CORY_HINTS) for u in urls),
            "priority": priority, "why": why}


def analyze(wid: str) -> dict:
    c = _clean_signal(wid)
    r = _ready_signal(wid)
    t = _translation_signal(wid)
    return {"work": wid, **c, **r, **t}


def render(rec: dict) -> str:
    p = rec.get("priority", "LOW")
    flag = {"HIGH": ">> ", "MEDIUM": ">  ", "LOW": "   "}.get(p, "   ")
    clean = "CLEAN" if rec.get("clean") else "DIRTY"
    ready = "READY" if rec.get("in_ledger") else "no-ledger"
    q = rec.get("english", "?")
    return (f"{flag}[{p:<6}] {clean:<5} {ready:<9} {rec['work']:<38} "
            f"en={q:<8} src={rec.get('sanskrit_chars',0):>6} | {rec.get('why','')}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.work:
        recs = [analyze(a.work)]
    elif a.all:
        # all on-disk works + all atlas works (so new seeds show even without source)
        ids = set()
        if SOURCES.exists():
            ids |= {d.name for d in SOURCES.iterdir() if d.is_dir()}
        for fn in ("sivaqueueSeed.ts", "sivaqueue34Seed.ts", "bibliographySeed.ts", "audited.ts"):
            p = ROOT / "data/atlas" / fn
            if p.exists():
                txt = p.read_text(encoding="utf-8")
                ids |= set(re.findall(r'\{"id"\s*:\s*"([a-z0-9-]+)"', txt))
                ids |= set(re.findall(r'id\s*:\s*"([a-z0-9_-]+)"', txt))
        recs = sorted((analyze(w) for w in ids), key=lambda r: {"HIGH": 0, "MEDIUM": 1, "LOW": 2}.get(r.get("priority", "LOW")))
    else:
        print("usage: --work <id> | --all")
        return 1

    if a.json:
        print(json.dumps(recs, indent=2, ensure_ascii=False, default=str))
    else:
        for r in recs:
            print(render(r))
        from collections import Counter
        c = Counter(r.get("priority") for r in recs)
        clean = sum(1 for r in recs if r.get("clean"))
        print(f"\n{len(recs)} works | clean={clean} | priority: {dict(c)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
