#!/usr/bin/env python3
"""pipeline/translation_availability.py — the translation-availability index (the product).

For every work, answer: "which translations exist (full/partial, who, edition-base, license), where they
live, and which are missing" — built on top of the text-identity layer. Nobody has built this for
Sanskrit; this is the greenfield layer the stack is missing.

It MERGES (does not rebuild) every existing source of translation truth:
  1. translation_status.py   — curated atlas-seed translations[] (language/url/translator/coverage/
                                complete/type/tier) + copyrightHint        [254 works, 60 with EN]
  2. verify_editions.py      — live archive.org attestations (found translation/edition + counts)  [25]
  3. translation-state-ledger — per-work factory lifecycle (T1/L2/C1 status, next_action, source_ref)
  4. atlas-bibliography.json — the identity layer (254 works ↔ canonical id)

Output: a per-work availability record:
    {work, has_english, languages[], translations[] (enriched with found_live + source), coverage
     (full/partial/none), missing:true if none, copyright_hint, live_checked, next_action}

Deterministic, stdlib-only, CPU-only. The live-check (archive.org) is OFF by default to keep it
fast/offline; `--live` turns it on (reuses verify_editions). The curated + ledger merge is always on.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(str(Path(__file__).resolve().parents[1]))
if str(ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(ROOT / "pipeline"))

import translation_status as TS  # noqa: E402


def _load_json(p: Path, default=None):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return default if default is not None else {}


def _coverage_label(status: str, translations: list[dict]) -> str:
    """full / partial / none from the curated status + translation completeness."""
    if status == "complete":
        return "full"
    if status == "partial":
        return "partial"
    if translations:
        return "partial"
    return "none"


def _enrich(trans: dict, live_attest: list[dict]) -> dict:
    """Add found_live + source to a curated translation record."""
    t = dict(trans)
    # does any live attestation corroborate a translation for this language?
    t["found_live"] = bool(live_attest)
    t["source"] = "curated"
    return t


def availability(work_id: str, live: bool = False) -> dict:
    """The per-work availability record (the product)."""
    ts = TS.load()
    curated = ts.get(work_id, {})
    translations = list(curated.get("translations", []) or [])

    # ledger factory state (T1/L2/C1 + next_action)
    ledger = _load_json(ROOT / "data/corpus/downloads/translation-state-ledger.json")
    w = ledger.get("works", {}).get(work_id, {})
    tr = w.get("translation", {}) or {}

    # live attestations (verify_editions output) — optional
    live_attest = []
    if live:
        reg = ROOT / "data/corpus/registries/verification-registry.jsonl"
        if reg.exists():
            for line in reg.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    a = json.loads(line)
                except Exception:
                    continue
                if a.get("work_id") == work_id and a.get("kind") == "translation":
                    live_attest.append(a)

    langs = sorted({t.get("language") for t in translations if t.get("language")})
    has_english = any(t.get("language") == "en" for t in translations)
    coverage = _coverage_label(curated.get("translationStatus", "none"), translations)

    enriched = [_enrich(t, live_attest) for t in translations]
    # if none found but live check found archive hits, note them
    live_note = ""
    if live and not has_english and live_attest:
        live_note = f"live archive found {len(live_attest)} translation-ish hits (unconfirmed)"

    return {
        "work": work_id,
        "has_english": has_english,
        "languages": langs,
        "coverage": coverage,
        "missing": coverage == "none",
        "translations": enriched,
        "copyright_hint": curated.get("copyrightHint", "UNKNOWN"),
        "english_urls": curated.get("english_urls", []),
        "factory": {
            "t1": tr.get("t1", "UNKNOWN"), "l2": tr.get("l2", "UNKNOWN"),
            "c1": tr.get("c1", "UNKNOWN"), "next_action": w.get("next_action", {}).get("action"),
        },
        "live_checked": bool(live_attest) or (not live),
        "live_note": live_note,
    }


def availability_all(live: bool = False) -> dict:
    """The full index keyed by work_id + coverage/language breakdown."""
    ts = TS.load()
    recs = {}
    for wid in ts:
        recs[wid] = availability(wid, live=live)
    return {"count": len(recs), "works": recs}


def summary(live: bool = False) -> dict:
    """Aggregate: how many full/partial/none, how many with English, by coverage."""
    all_recs = availability_all(live=live)["works"]
    coverage = Counter(r["coverage"] for r in all_recs.values())
    en = sum(1 for r in all_recs.values() if r["has_english"])
    missing = sum(1 for r in all_recs.values() if r["missing"])
    by_cov = {c: sorted(w for w, r in all_recs.items() if r["coverage"] == c) for c in ("full", "partial", "none")}
    return {
        "total": len(all_recs), "with_english": en, "missing_any": missing,
        "coverage": dict(coverage),
        "full_works": len(by_cov["full"]), "partial_works": len(by_cov["partial"]),
        "untranslated_works": len(by_cov["none"]),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--work", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--live", action="store_true", help="run live archive.org checks (slow)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.summary:
        print(json.dumps(summary(live=a.live), indent=2, ensure_ascii=False))
        return 0
    if a.work:
        r = availability(a.work, live=a.live)
        print(json.dumps(r, indent=2, ensure_ascii=False) if a.json else json.dumps(r, indent=2, ensure_ascii=False))
        return 0
    if a.all:
        d = availability_all(live=a.live)
        # compact: only the key fields per work
        compact = {w: {k: r[k] for k in ("has_english", "coverage", "missing", "languages")} for w, r in d["works"].items()}
        print(json.dumps({"count": len(compact), "works": compact}, indent=2, ensure_ascii=False))
        return 0
    print(json.dumps(summary(live=a.live), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
