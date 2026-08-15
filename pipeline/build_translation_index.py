#!/usr/bin/env python3
"""pipeline/build_translation_index.py — the COMPILE step (compute-on-write, perf rule 1).

Materializes the full translation-availability index (curated + live-locator) into ONE compiled JSON
artifact that the atlas API + Astro serve as immutable bytes (perf rules 8/9: read from bytes, ETag).

This is the ONLY place the live external APIs (OpenAlex/Unpaywall/Crossref) are called — at BUILD time,
cached with provenance, NEVER per-request. A reader (API/Astro) gets the compiled bytes with ETag→304.

Emits:  data/corpus/translation-availability.json   (the compiled index, {count, works, meta})
        data/corpus/translation-availability-meta.json (build provenance: when, how many live calls)
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(str(Path(__file__).resolve().parents[1]))
if str(ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(ROOT / "pipeline"))
if str(ROOT / "python") not in sys.path:
    sys.path.insert(0, str(ROOT / "python"))

import translation_availability as TA  # noqa: E402

OUT = ROOT / "data/corpus/translation-availability.json"
META_OUT = ROOT / "data/corpus/translation-availability-meta.json"


def _compile(curated_only: bool = False, max_live: int | None = None) -> dict:
    """Compile the index. curated_only=True skips ALL live API calls (fast, offline).
    max_live caps how many works get a live-locator check (rate-limit courtesy)."""
    from translation_locator import availability_with_live  # noqa: E402

    # the works the index covers = translation_status's 254 works
    ts = __import__("translation_status").load()
    works = {}
    live_calls = 0
    started = time.time()

    for wid in ts:
        if curated_only:
            works[wid] = TA.availability(wid)
            continue
        if max_live is not None and live_calls >= max_live:
            # fall back to curated-only for the rest (courtesy)
            works[wid] = TA.availability(wid)
            continue
        try:
            works[wid] = availability_with_live(wid)  # curated + live merge
            live_calls += 1
        except Exception:  # noqa: BLE001
            works[wid] = TA.availability(wid)  # fail-closed to curated
        if live_calls % 10 == 0 and live_calls:
            print(f"  ...{live_calls} live checks done", flush=True)

    meta = {
        "schema": "patala.translation-availability.v1",
        "compiled_at": datetime.now(timezone.utc).isoformat(),
        "duration_s": round(time.time() - started, 2),
        "works": len(works),
        "curated_only": curated_only,
        "live_checks": live_calls,
        "providers": ["openalex", "crossref", "unpaywall"] if not curated_only else [],
        "note": "compute-on-write: the live APIs ran here, cached; readers get bytes + ETag",
    }
    return {"meta": meta, "count": len(works), "works": works}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--curated-only", action="store_true",
                    help="skip live API calls entirely (offline, fast)")
    ap.add_argument("--max-live", type=int, default=None,
                    help="cap live API checks (courtesy); rest fall back to curated")
    a = ap.parse_args()

    print(f"compiling translation-availability index "
          f"({'curated-only' if a.curated_only else 'curated + live'})...", flush=True)
    d = _compile(curated_only=a.curated_only, max_live=a.max_live)
    OUT.write_text(json.dumps(d, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    meta = {k: d["meta"][k] for k in ("compiled_at", "duration_s", "works", "live_checks", "curated_only")}
    META_OUT.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(meta, indent=2, ensure_ascii=False))
    print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
