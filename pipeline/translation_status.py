#!/usr/bin/env python3
"""pipeline/translation_status.py — materialized per-work translation-existence + location registry.

Closes the organizational gap found in the ASSESS-FLOW audit: the "does an English translation exist +
where" data lives ONLY in the atlas TS seeds (bibliographySeed.ts, sivaqueueSeed.ts, audited.ts) and is
parsed on-demand. It is never stored, never joined into the ledger/queue/assess records, never surfaced
as a queryable field.

This module MATERIALIZES it into one machine-readable registry: for every work, merge
  translationStatus (complete/partial/none), translations[] (language/url/translator/coverage/
  complete/type/tier), statusLabel, rights -> {copyrightHint}.

Mechanisms surveyed: buda-base owl-schema copyrights.ttl (copyright enum) + csl-standards
EVIDENCE_LABEL_CROSSWALK (evidence/review status). Pure stdlib, CPU-only.

Use: --write-cache -> data/corpus/translation-status.json (the audit trail, same as assess.json).
     load() -> {work_id: {translationStatus, translations[], copyrightHint, ...}} for assess + queue.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(str(Path(__file__).resolve().parents[1]))
if str(ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(ROOT / "pipeline"))

_SEEDS = ("bibliographySeed.ts", "sivaqueueSeed.ts", "sivaqueue34Seed.ts", "sivaqueueGapSeed.ts", "audited.ts")
_CACHE = ROOT / "data/corpus/translation-status.json"

# buda-base owl-schema copyrights.ttl (adapted): the controlled copyright enum
PUBLIC_DOMAIN_HINTS = ("archive.org", "sacred-texts", "gutenberg", "wisdomlib", "gretil", "ia")
COPYRIGHT_HINTS = ("oup.com", "pupress", "sunypress", "cambridge", "academic", "efeo.fr",
                   "ifpindia.org", "brill", "doi.org", "taylorfrancis", "anuttaratrikakula")


def _extract_braced(txt: str, m_start: int) -> str | None:
    """Return the balanced '{...}' block starting at/after m_start."""
    start = txt.rfind("{", 0, m_start)
    depth = 0
    for i in range(start, len(txt)):
        c = txt[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return txt[start:i + 1]
    return None


def _find_record(txt: str, wid: str) -> str | None:
    for m in re.finditer(r'"?id"?\s*:\s*"' + re.escape(wid) + r'"', txt):
        return _extract_braced(txt, m.start())
    return None


def _js_val(rec: str, key: str) -> str:
    """Best-effort scalar value for a JS key."""
    m = re.search(r'"?%s"?\s*:\s*"([^"]*)"' % re.escape(key), rec)
    if m:
        return m.group(1).strip()
    m = re.search(r'"?%s"?\s*:\s*(\w+)' % re.escape(key), rec)
    return (m.group(1).strip() if m else "")


def _parse_translations(rec: str) -> list[dict]:
    """Parse the translations: [...] array into a list of {language,url,translator,coverage,complete,type,tier}."""
    out = []
    m = re.search(r'"?translations"?\s*:\s*\[(.*?)\]\s*,', rec, re.S)
    if not m:
        m = re.search(r'"?translations"?\s*:\s*\[(.*?)\]\s*\}', rec, re.S)
    if not m:
        return out
    body = m.group(1)
    for em in re.finditer(r"\{([^{}]*)\}", body):
        obj = em.group(1)
        if "language" not in obj:
            continue
        out.append({
            "language": _js_val(obj, "language"),
            "translator": _js_val(obj, "translator"),
            "coverage": _js_val(obj, "coverage"),
            "complete": (_js_val(obj, "complete").lower() == "true"),
            "type": _js_val(obj, "type"),
            "tier": _js_val(obj, "tier"),
            "url": _js_val(obj, "url"),
        })
    return out


def _copyright_hint(status: str, translations: list[dict], rights: str) -> str:
    """Deterministic copyright hint from translation status + urls + rights (buda-base enum)."""
    if "open" in rights.lower() or any("open" in t.get("rights", "").lower() for t in translations):
        pass
    urls = [t.get("url", "") for t in translations]
    if any(any(h in u for h in COPYRIGHT_HINTS) for u in urls):
        return "IN_COPYRIGHT"
    if status in ("complete", "partial") and any(any(h in u for h in PUBLIC_DOMAIN_HINTS) for u in urls):
        return "PUBLIC_DOMAIN"
    if status in ("none",):
        return "PUBLIC_DOMAIN" if rights.lower().startswith("open") else "UNDETERMINED"
    return "UNDETERMINED"


def materialize() -> dict:
    """Merge all atlas seeds into one per-work translation-status registry."""
    records: dict[str, dict] = {}
    for fn in _SEEDS:
        p = ROOT / "data/atlas" / fn
        if not p.exists():
            continue
        txt = p.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r'"?id"?\s*:\s*"([A-Za-z0-9_-]+)"', txt):
            wid = m.group(1)
            rec = _find_record(txt, wid)
            if not rec or wid in records:
                continue
            trans = _parse_translations(rec)
            status = _js_val(rec, "translationStatus") or "none"
            rights = _js_val(rec, "rights") or _js_val(rec, "rights.status") or ""
            records[wid] = {
                "translationStatus": status,
                "translations": trans,
                "statusLabel": _js_val(rec, "statusLabel"),
                "copyrightHint": _copyright_hint(status, trans, rights),
                "has_english": any(t.get("language") == "en" for t in trans),
                "english_urls": [t.get("url") for t in trans if t.get("language") == "en" and t.get("url")],
                "source_seed": fn,
            }
    return records


def load(force: bool = False) -> dict:
    if not force and _CACHE.exists():
        return json.loads(_CACHE.read_text(encoding="utf-8"))
    return materialize()


def english_location(wid: str) -> dict | None:
    """Queryable: does work X have an English translation, and where is it?"""
    r = load().get(wid)
    if not r:
        return None
    return {
        "work": wid,
        "translationStatus": r["translationStatus"],
        "has_english": r["has_english"],
        "english_urls": r["english_urls"],
        "copyrightHint": r["copyrightHint"],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write-cache", action="store_true")
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    if a.write_cache:
        recs = materialize()
        _CACHE.write_text(json.dumps(recs, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
        en = sum(1 for r in recs.values() if r["has_english"])
        print(f"wrote {_CACHE} with {len(recs)} works ({en} with English)")
        return 0
    if a.work:
        print(json.dumps(english_location(a.work), indent=2, ensure_ascii=False))
        return 0
    recs = materialize()
    from collections import Counter
    print(f"{len(recs)} works | status: {dict(Counter(r['translationStatus'] for r in recs.values()))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
