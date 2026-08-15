"""products/manuscript_routing/engine.py — the manuscript routing diagnostic (vision E3).

The "what transformation does this manuscript need" step from vision-14 §4. Given a manuscript's
metadata (script, language, whether it has OCR text, source quality, work match), it LABELS it (the
quality fingerprint) and ROUTES it (the transformation needed): OCR → clean → re-derive → unrouteable.

This is the piece that makes manuscript onboarding "easy": the system doesn't just dump text in — it
diagnoses each manuscript and tells it exactly what it needs (kraken OCR? straight to the factory?).

CPU-only, deterministic. It consumes the OCHS-format manuscript metadata (data/corpus/manuscripts.ts
shape) and the pe-ocr-sanskrit quality signal. On this box the raw OCHS JSON may be absent
(data-boundary); the routing logic works on any well-formed manuscript record.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]

# scripts that need OCR (Devanagari/bengali/etc = needs HTR); IAST/roman = clean
DEVANAGARI = {"devanagari", "deva", "sanskrit", "nagari"}
ROMAN = {"latin", "roman", "iast", "transliteration"}


def _script_of(m: dict) -> str:
    return (m.get("script") or m.get("language") or "").lower()


def route_manuscript(m: dict) -> dict:
    """Label + route a manuscript record (OCHS-format). Returns the quality fingerprint + routing."""
    mid = m.get("id") or m.get("ochs_slug") or "unknown"
    script = _script_of(m)
    title = m.get("title") or m.get("titleIndic") or m.get("titleTranslation") or ""
    author = m.get("author") or ""
    tradition = m.get("tradition") or ""
    has_text = bool(m.get("text"))          # does OCHS hold a transcription?
    has_photos = bool(m.get("photos"))      # images available?
    has_incipit = bool(m.get("incipit"))    # a text anchor for identity
    condition = (m.get("condition") or "").lower()

    # -- label: the quality fingerprint --
    if script in DEVANAGARI:
        label = "DEVANAGARI_SCAN" if has_photos else "DEVANAGARI_ETEXT"
        ocr_needed = has_photos and not has_text
    elif script in ROMAN or script in ("latin", "iast"):
        label = "IAST_ETEXT"
        ocr_needed = False
    else:
        label = "UNKNOWN_SCRIPT"
        ocr_needed = has_photos and not has_text

    # -- route: the transformation needed --
    if ocr_needed:
        route = "OCR_THEN_FACTORY"          # kraken/eScriptorium → post-OCR check → SOURCE → T1
    elif has_text and label in ("IAST_ETEXT", "DEVANAGARI_ETEXT", "DEVANAGARI_SCAN"):
        route = "FACTORY_READY"             # clean text (incl. OCR'd) → SOURCE → T1
    elif label in ("IAST_ETEXT", "DEVANAGARI_ETEXT", "DEVANAGARI_SCAN"):
        route = "NEEDS_TEXT"                # has photos but no transcription → needs OCR or manual
    elif has_incipit:
        route = "IDENTIFY_THEN_ROUTE"       # an incipit anchors identity → resolve work first
    else:
        route = "UNROUTEABLE"               # no text, no photos, no anchor — needs a human decision

    # the identity signal: can we guess the work from title/incipit?
    identity = {"title": title, "author": author, "tradition": tradition,
                "work_match": "UNRESOLVED",
                "note": "title/incipit match to a canonical work is a RESOLVE step, never fuzzy-auto"}

    return {
        "manuscript_id": mid,
        "label": label,
        "script": script,
        "has_photos": has_photos, "has_text": has_text, "has_incipit": has_incipit,
        "condition": condition,
        "route": route,
        "ocr_tool": "kraken+eScriptorium (adopt, don't rebuild)" if ocr_needed else None,
        "quality_gate": "pe-ocr-sanskrit post-OCR benchmark" if ocr_needed else None,
        "identity": identity,
        "note": "MACHINE_PROPOSED routing: diagnoses the transformation needed, never fabricates "
                "a work identity (resolve first).",
    }


def route_catalog(records: list[dict]) -> dict:
    """Route a batch of manuscripts (the 'get a bunch in easily' path)."""
    from collections import Counter
    routed = [route_manuscript(m) for m in records]
    by_route = Counter(r["route"] for r in routed)
    return {
        "n_manuscripts": len(routed),
        "by_route": dict(by_route),
        "routed": routed,
        "note": "batch routing: each manuscript labeled + routed to the transformation it needs",
    }


def demo() -> dict:
    """Route a few OCHS-format manuscript records (representative of the real data)."""
    samples = [
        {"id": "pt:ms:ochs_000_000_039_kubjikamatatantra", "ochs_slug": "ochs_000_000_039_kubjikamatatantra",
         "script": "Devanagari", "title": "Kubjikāmatatantra", "photos": True, "text": False,
         "tradition": "Kubjikā", "author": "—", "incipit": "namaḥ śivāya"},
        {"id": "pt:ms:ochs_000_000_002_amrtesatantram", "ochs_slug": "ochs_000_000_002_amrtesatantram",
         "script": "Devanagari", "title": "Amṛteśatantram", "photos": True, "text": True,
         "tradition": "Netra", "incipit": "om namaḥ"},
        {"id": "pt:ms:example-iast", "ochs_slug": "example-iast", "script": "IAST",
         "title": "Tantrasadbhāva", "photos": False, "text": True, "tradition": "Bhairava",
         "incipit": "prathamaṃ"},
    ]
    return route_catalog(samples)


if __name__ == "__main__":
    import sys as _s
    verb = _s.argv[1] if len(_s.argv) > 1 else "demo"
    if verb == "demo":
        print(json.dumps(demo(), indent=2, ensure_ascii=False))
    else:
        # route a single manuscript JSON passed as argv[2]
        print(json.dumps(route_manuscript(json.loads(_s.argv[2])), indent=2, ensure_ascii=False))
