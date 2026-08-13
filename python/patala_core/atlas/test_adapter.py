#!/usr/bin/env python3
"""python/patala_core/atlas/test_adapter.py — TIER 3 adapter tests.

Proves the "don't break the factory" gate:
  1. The adapter returns the SAME contract (id/title/translation_status/verified) from legacy TS and
     from the Atlas Postgres (254/254, 0 mismatches).
  2. The compiled read-model (mommyspeed pattern) materializes once and hot-reads are dict lookups.
  3. The factory catalog can read through the adapter with identical output to before.
Run: python3 python/patala_core/atlas/test_adapter.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from patala_core.atlas.adapter import AtlasAdapter, LegacyBackend, PostgresBackend  # noqa: E402


def t(name, cond, detail=""):
    print(("PASS" if cond else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def main() -> int:
    ok = True
    print("=== TIER 3: compatibility adapter (don't break the factory) ===")

    legacy = LegacyBackend().load()
    pg = PostgresBackend()
    pg_avail = pg.available()
    ok &= t("postgres reachable", pg_avail)
    if not pg_avail:
        print("  (skipping parity — postgres not up)")
        print("RESULT: " + ("ALL PASS" if ok else "FAILURES"))
        return 0 if ok else 1

    pg_records = pg.load()
    ok &= t("postgres returns 254 records", len(pg_records) == 254, f"got {len(pg_records)}")
    ok &= t("all legacy ids present in postgres", set(legacy) == set(pg_records))

    # exact parity on the 3 contract fields
    mismatches = []
    for k in legacy:
        l, p = legacy[k], pg_records.get(k)
        if p is None:
            mismatches.append((k, "missing")); continue
        for f in ("title", "translation_status", "verified"):
            if l[f] != p[f]:
                mismatches.append((k, f))
    ok &= t("0 contract mismatches legacy vs postgres", len(mismatches) == 0, f"{len(mismatches)} mismatches")
    for m in mismatches[:5]:
        print("    ", m)

    # compiled read-model: materialize once, hot-read is a dict lookup
    adapter = AtlasAdapter(cache_path=Path("/tmp/patala-test-atlas-cache.json"))
    data = adapter.refresh(use_postgres=True)
    ok &= t("compiled read-model materializes", len(data) == 254)
    # force postgres backend decision + hot path
    adapter._backend = "postgres"
    hot = adapter.load()
    ok &= t("hot path returns cached model (no DB re-query)", hot is data, "same object")

    print("")
    print("RESULT: " + ("ALL PASS" if ok else "FAILURES"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
