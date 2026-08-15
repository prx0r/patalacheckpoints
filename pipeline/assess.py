#!/usr/bin/env python3
"""pipeline/assess.py — the CANONICAL ASSESS-FLOW decision engine (T0→T5 + routing).

The authoritative, deterministic process for deciding what to do with each Sanskrit work: from raw
acquisition through to queueing for translation. One deterministic pass per work → one machine-readable
record `{tag, state, format, verse, identity, priority, route}`.

AXIOM 3: eligibility is deterministic Python, never an LLM judgment. Hermes is NEVER in this decision
(only for GENERATION of content/rationale). This consolidates the scattered signals into one engine:
  T0 CATEGORY  tag           <- sivaqueue_targets.all_targets() metadata (period/tradition/genre/source)
  T1 STATE     clean         <- source_ready._clean_signal (IAST/Devanagari density, verse markers, size)
  T2 FORMAT    format        <- corpus_state.detect_source_format + scheme detection (deva/iast/itrans/hk/velthuis)
  T3 VERSE     verse         <- SOURCE registry verse payload present/recoverable/blocked
  T4 IDENTITY  identity      <- entity_reconciliation (EXACT/PROBABLE/POSSIBLE/CONFLICT/UNRESOLVED)
  T5 PRIORITY  priority      <- copyright-aware source_ready._priority_for + translation_targets
  ROUTE        route         <- the decision table mapping (state, format, identity) -> process

Mechanisms surveyed from the cloned ecosystem (source-evidence/repos/):
  - scheme detection (T2, UNKNOWN format): sanskrit-util tools/KeySwap/scheme_bridge.detect_scheme (pure stdlib)
  - copyright/status enums (T5): buda-base__owl-schema copyrights.ttl + status_types.ttl (controlled vocab)
  - status taxonomy: csl-standards EVIDENCE_LABEL_CROSSWALK.md (blocked/needs-review/derived)
  - deterministic disjoint routing: alfadur7 prefilter_ingest.classify (template)
All pure-stdlib, CPU-only, no numpy/GPU/DB.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(str(Path(__file__).resolve().parents[1]))
if str(ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(ROOT / "pipeline"))

import source_ready as SR  # noqa: E402
import object_registry as R  # noqa: E402
import translation_status as TS  # noqa: E402

try:
    import corpus_state as CS  # noqa: E402
    _HAS_CS = True
except Exception:
    _HAS_CS = False

# ---- the canonical tags (T0) ----
TAGS = ("KRAMA_PACKET", "TIER1", "E_TEXT_READY", "SCANNED_MANUSCRIPT", "IDENTITY_PENDING",
        "COPYRIGHT_RESTRICTED", "NO_SOURCE", "AMBIGUOUS")

# ---- the state ladder (T1) ----
STATES = ("CLEAN_ETEXT", "NEEDS_OCR", "LACUNA_BLOCKED", "AMBIGUOUS", "NO_SOURCE")

# ---- formats (T2) ----
FORMATS = ("AND_GLOSS", "RAW_SANSKRIT", "UNKNOWN")

# ---- identity (T4) ----
IDENTITIES = ("EXACT", "PROBABLE", "POSSIBLE", "CONFLICT", "UNRESOLVED")

# ---- priority (T5) ----
PRIORITIES = ("HIGH", "MEDIUM", "LOW", "BLOCKED")

# ---- copyright enum (from buda-base owl-schema copyrights.ttl, adapted) ----
COPYRIGHTS = ("PUBLIC_DOMAIN", "UNDETERMINED", "IN_COPYRIGHT", "UNKNOWN")

# ---- the T0 category tags: which are "registered + on disk + acquired" ----
_ACQUIRED = ("acquired", "available")


def _scheme(text: str) -> str:
    """Detect the transliteration/script scheme of a source (T2, pure stdlib).

    Ported from sanskrit-util tools/KeySwap/scheme_bridge.detect_scheme (surveyed lift).
    Returns deva | iast | itrans | hk | velthuis | unknown.
    """
    t = text.strip()
    if not t:
        return "unknown"
    if any("\u0900" <= c <= "\u097f" for c in t):
        return "deva"
    if re.search(r"[āīūṛṝḷḹṅñṭḍṇśṣṃṁḥĀĪŪṚṜḶḸṄÑṬḌṆŚṢṂḤ]", t):
        return "iast"
    if re.search(r'\.[a-zA-Z]|"n|"s|~n', t):
        return "velthuis"
    if re.search(r"~N|~n|\.n|\.m|aa|ii|uu|RRi|sh|Sh", t):
        return "itrans"
    if re.search(r"[AIURMGJTDNzSH]", t) and re.search(r"[a-z]", t):
        return "hk"
    return "unknown"


def _detect_format(wid: str) -> tuple[str, str]:
    """T2 — AND_GLOSS vs RAW_SANSKRIT vs UNKNOWN from the on-disk source."""
    p = SR._work_source_file(wid)
    if not p:
        return "UNKNOWN", "no on-disk source"
    txt = p.read_text(encoding="utf-8", errors="ignore")
    # AND_GLOSS has '[and]-GLOSS' markers
    if re.search(r"\[and\]-", txt):
        return "AND_GLOSS", "has [and]-GLOSS apparatus markers"
    scheme = _scheme(txt)
    if scheme in ("deva", "iast"):
        # red-team fix (FINDING 2): require a minimum Sanskrit density before declaring
        # RAW_SANSKRIT. A stray diacritic in noise isn't a Sanskrit source. Real e-texts
        # run 0.13-0.15; the red-team garbage was 0.003. 0.05 cleanly separates.
        iast = len(re.findall(r"[āīūṛṝḷḹṃñṅśṣṭḍḥṁṇ]", txt))
        deva = len(re.findall(r"[\u0900-\u097F]", txt))
        sanskrit = iast + deva
        density = sanskrit / len(txt) if txt else 0.0
        if density < 0.05:
            return "UNKNOWN", f"indeterminate script ({scheme}, density {density:.3f} — likely OCR-mess)"
        return "RAW_SANSKRIT", f"raw Sanskrit ({scheme}, density {density:.3f})"
    if scheme in ("itrans", "hk", "velthuis"):
        return "UNKNOWN", f"machine-readable but {scheme} transliteration — normalize first"
    return "UNKNOWN", f"indeterminate script ({scheme or 'none'})"


def _verse_signal(wid: str) -> tuple[str, str]:
    """T3 — is a verse payload present / recoverable / blocked?"""
    try:
        objects = R._load("SOURCE")["objects"]
    except Exception:
        objects = []
    committed = [o for o in objects if o.startswith(wid)]
    if committed:
        try:
            rec = R.current("SOURCE", committed[0]) or {}
            if rec.get("payload", {}).get("verse"):
                return "PRESENT", f"{len(committed)} committed SOURCE with verse"
            return "RECOVERABLE", "committed SOURCE but empty verse — recovery (P0)"
        except Exception:
            pass
    return "BLOCKED", "no committed SOURCE verse"


def _identity_signal(wid: str) -> tuple[str, str]:
    """T4 — identity reconciliation. Deterministic: no cross-candidate → UNRESOLVED (abstain, cheap)."""
    try:
        from source_evals_recon import reconcile  # noqa: F401
        return "POSSIBLE", "adapter record — needs crosswalk"
    except Exception:
        # deterministic fallback: well-known acquired works are EXACT; else UNRESOLVED (never overclaim)
        return "EXACT" if wid in _acquired_ids() else "UNRESOLVED", "registry identity, single source"


def _acquired_ids() -> set:
    try:
        import sivaqueue_targets as st
        return {k for k, v in st.all_targets().items() if v.get("acquisition_status") in _ACQUIRED}
    except Exception:
        return set()


def _priority_signal(wid: str) -> tuple[str, str]:
    """T5 — copyright-aware priority (source_ready._priority_for) + translation_targets.

    Now TRANSPARENT: the priority reason cites the materialized English-translation existence/location
    (from translation_status) instead of silently re-parsing the TS seeds.
    """
    t = TS.load().get(wid, {})
    en = t.get("has_english")
    try:
        rec = SR.analyze(wid)
        pri = rec.get("priority", "LOW")
        why = rec.get("why", "source_ready signal")
    except Exception:
        pri, why = "LOW", "no source_ready signal"
    # make the reason transparent about translation existence + location
    if en:
        urls = t.get("english_urls", [])
        loc = f" @ {urls[0]}" if urls else ""
        why = f"{why}; has_english({t.get('translationStatus')}){loc}"
    else:
        why = f"{why}; no_english({t.get('translationStatus') or 'none'})"
    return pri, why


def _tag(wid: str, clean: bool, fmt: str, identity: str, pri: str, meta: dict) -> str:
    """T0 — category tag."""
    if not clean:
        return "NEEDS_OCR" if fmt == "RAW_SANSKRIT" else "NO_SOURCE"
    if meta.get("translation_status") == "N":
        return "COPYRIGHT_RESTRICTED"
    if identity in ("CONFLICT", "UNRESOLVED"):
        return "IDENTITY_PENDING"
    if pri == "HIGH":
        return "TIER1"
    return "E_TEXT_READY"


def _route(state: str, fmt: str, identity: str) -> str:
    """The canonical routing table (FRONTIER ASSESS-FLOW §3)."""
    if state == "CLEAN_ETEXT" and fmt == "RAW_SANSKRIT" and identity in ("EXACT", "PROBABLE"):
        return "NORMALIZE → SOURCE → QUEUE → TRANSLATE"
    if state == "CLEAN_ETEXT" and fmt == "AND_GLOSS":
        return "EXTRACT_SANSKRIT → re-assess"
    if state == "CLEAN_ETEXT" and fmt == "RAW_SANSKRIT" and identity in ("POSSIBLE", "CONFLICT"):
        return "SCHOLAR_QUEUE (adjudicate identity first)"
    if state == "NEEDS_OCR":
        return "OCR_INTEGRATOR (Kraken/eScriptorium/Vidyut)"
    if state == "LACUNA_BLOCKED":
        return "VERSE_RECOVERY_P0 → harvest_to_factory → re-assess"
    if fmt == "UNKNOWN" and state in ("AMBIGUOUS", "CLEAN_ETEXT"):
        return "SCHOLAR_QUEUE (classify source)"
    if state == "NO_SOURCE":
        return "ACQUIRE (choose adapter) → re-ingest"
    return "SCHOLAR_QUEUE (manual review)"


def assess(wid: str) -> dict:
    """One deterministic pass per work → the machine-readable ASSESS record."""
    meta = {}
    try:
        import sivaqueue_targets as st
        meta = st.all_targets().get(wid, {})
    except Exception:
        pass

    # T1 clean signal
    clean_rec = SR._clean_signal(wid)
    on_disk = clean_rec.get("on_disk", False)
    clean = clean_rec.get("clean", False)
    sanskrit_chars = clean_rec.get("sanskrit_chars", 0)

    # T2 format
    fmt, fmt_why = _detect_format(wid)

    # T3 verse
    verse, verse_why = _verse_signal(wid)

    # T4 identity
    identity, id_why = _identity_signal(wid)

    # T5 priority
    pri, pri_why = _priority_signal(wid)

    # T1 state ladder (deterministic)
    if not on_disk:
        state = "NO_SOURCE"
    elif clean and sanskrit_chars > 0:
        state = "CLEAN_ETEXT"
    elif clean_rec.get("reason", "").startswith("no Sanskrit"):
        state = "AMBIGUOUS"
    elif verse == "BLOCKED":
        state = "LACUNA_BLOCKED"
    else:
        state = "NEEDS_OCR"

    tag = _tag(wid, clean, fmt, identity, pri, meta)
    route = _route(state, fmt, identity)

    # the materialized translation-existence + location (the organizational gap fix)
    trans = TS.load().get(wid, {})
    translation = {
        "translationStatus": trans.get("translationStatus", "none"),
        "has_english": trans.get("has_english", False),
        "english_urls": trans.get("english_urls", []),
        "copyrightHint": trans.get("copyrightHint", "UNKNOWN"),
    }

    # the ingestion-ROI projection (from project_translation.py): cost/time to translate this work.
    projection = None
    try:
        from project_translation import project
        p = project(work_id=wid)
        if p["rows"]:
            r = p["rows"][0]
            projection = {"verses": r["verses"], "calls": r["calls"], "hours": r["hours"],
                          "cost_miss_usd": r["cost_miss_usd"], "cost_hit_usd": r["cost_hit_usd"],
                          "model": p["model"]}
    except Exception:
        projection = None

    return {
        "work": wid,
        "tag": tag, "state": state, "format": fmt, "verse": verse,
        "identity": identity, "priority": pri, "route": route,
        "translation": translation,
        "projection": projection,
        "meta": {k: meta.get(k) for k in ("period", "tradition", "genre", "translation_status",
                                          "source", "acquisition_status") if k in meta},
        "signals": {
            "clean": clean_rec.get("reason"), "format": fmt_why,
            "verse": verse_why, "identity": id_why, "priority": pri_why,
        },
        "sanskrit_chars": sanskrit_chars,
    }


def assess_all() -> list[dict]:
    ids = set()
    if SR.SOURCES.exists():
        ids |= {d.name for d in SR.SOURCES.iterdir() if d.is_dir()}
    try:
        import sivaqueue_targets as st
        ids |= set(st.all_targets().keys())
    except Exception:
        pass
    return sorted((assess(w) for w in ids), key=lambda r: (PRIORITIES.index(r["priority"])))


def render(rec: dict) -> str:
    tr = rec.get("translation", {})
    en = "EN" if tr.get("has_english") else "no-EN"
    return (f"[{rec['priority']:<6}] {rec['state']:<13} {rec['format']:<12} "
            f"{rec['identity']:<10} {en:<6} {rec['tag']:<18} {rec['work']:<34} → {rec['route']}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--work", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--write-cache", action="store_true",
                    help="compute the full ASSESS once and save to data/corpus/assess.json (audit trail)")
    a = ap.parse_args()

    if a.write_cache:
        recs = assess_all()
        p = ROOT / "data/corpus/assess.json"
        p.write_text(json.dumps(recs, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
        print(f"wrote {p} with {len(recs)} assessed works")
        return 0
    if a.work:
        recs = [assess(a.work)]
    elif a.all:
        recs = assess_all()
    else:
        print("usage: --work <id> | --all | --write-cache")
        return 1
    if a.json:
        print(json.dumps(recs, indent=2, ensure_ascii=False, default=str))
    else:
        for r in recs:
            print(render(r))
        from collections import Counter
        print(f"\n{len(recs)} works | tags: {dict(Counter(r['tag'] for r in recs))} | "
              f"routes: {dict(Counter(r['route'] for r in recs))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
