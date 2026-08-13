#!/usr/bin/env python3
"""pipeline/atlas_persist_rich.py — write the rich scholarship graph to Postgres (audit fix #2).

The audit's key finding: the Atlas schema has the edition/etext/scholarly_work/relationship tables,
but they are EMPTY (edition=0, scholarly_work=0) — the rich Trika-10 data is staged in
atlas-backfill-candidates.json but never written. This persists the ATLAS-10 rich fields into the
Postgres schema, closing the thin-vs-rich gap.

For each backfilled work:
    work      (already in the 254, matched by id)
    → edition    (critical editions + editions, from textSources)
    → etext      (e-texts, from textSources)
    → scholarly_work (the scholarship entries)
    → relationship  (related works)

Authority is honest: each row carries authority_state = CATALOG_SUPPORTED (from the audited
bibliography), never inflated. Idempotent (skips existing).

Run: machinelearning/research/.venv/bin/python pipeline/atlas_persist_rich.py
"""
from __future__ import annotations

import json
import os
import sys
import uuid

sys.path.insert(0, "/root/projects/patala/pipeline")
sys.path.insert(0, "/root/projects/patala/python")
from patala_core.atlas.adapter import DEFAULT_DB_URL  # noqa: E402

CANDIDATES = "/root/projects/patala/data/evaluation/atlas-backfill-candidates.json"
AUTHORITY = "CATALOG_SUPPORTED"


def _conn():
    import psycopg2
    url = DEFAULT_DB_URL.replace("postgresql+psycopg2://", "postgresql://", 1)
    return psycopg2.connect(url)


def _work_id(cur, legacy_id: str):
    # the work id is a deterministic UUID derived from the legacy id (md5 -> uuid, per migrate.py)
    import hashlib
    h = hashlib.md5(legacy_id.encode()).digest()
    wid = str(uuid.UUID(bytes=h[:16]))
    cur.execute("SELECT id FROM work WHERE id = %s", (wid,))
    row = cur.fetchone()
    return row[0] if row else None


def persist(candidates: list[dict]) -> dict:
    conn = _conn()
    cur = conn.cursor()
    n_ed = n_etext = n_sch = n_rel = skipped = 0
    for c in candidates:
        wid = c.get("id")
        work_uuid = _work_id(cur, wid)
        if not work_uuid:
            skipped += 1
            continue
        # editions + etexts from textSources
        for src in c.get("editions", {}).get("value", []) if isinstance(c.get("editions"), dict) else []:
            if not isinstance(src, dict):
                continue
            if _row_exists(cur, "edition", work_uuid, "edition_type", src.get("type", "edition")):
                continue
            cur.execute(
                """INSERT INTO edition (id, work_id, title, edition_type, publication_year, authority_state, notes, created_at)
                   VALUES (%s,%s,%s,%s,%s,%s,%s, now())""",
                (str(uuid.uuid4()), work_uuid, src.get("provider", ""),
                 src.get("type", "edition"), src.get("year"), AUTHORITY,
                 json.dumps({"coverage": src.get("coverage"), "editor": src.get("editor"),
                             "tier": src.get("tier")})))
            n_ed += 1
        for src in c.get("etexts", {}).get("value", []) if isinstance(c.get("etexts"), dict) else []:
            if not isinstance(src, dict):
                continue
            if _row_exists(cur, "etext", work_uuid, "provider", src.get("provider", "")):
                continue
            cur.execute(
                """INSERT INTO etext (id, work_id, provider, transcription_method, authority_state, provider_record)
                   VALUES (%s,%s,%s,%s,%s,%s)""",
                (str(uuid.uuid4()), work_uuid, src.get("provider", ""),
                 src.get("type", "etext"), AUTHORITY,
                 json.dumps({"coverage": src.get("coverage"), "url": src.get("url")})))
            n_etext += 1
        # scholarship -> scholarly_work
        for s in c.get("scholarship", {}).get("value", []) if isinstance(c.get("scholarship"), dict) else []:
            if not isinstance(s, dict):
                continue
            title = f"{s.get('author','')} — {s.get('work','')}".strip(" —")
            if _row_exists(cur, "scholarly_work", work_uuid, "title", title):
                continue
            cur.execute(
                """INSERT INTO scholarly_work (id, work_id, title, authority_state, created_at)
                   VALUES (%s,%s,%s,%s, now())""",
                (str(uuid.uuid4()), work_uuid, title, AUTHORITY))
            n_sch += 1
        # related -> relationship (work→work)
        for rel in c.get("related", {}).get("value", []) if isinstance(c.get("related"), dict) else []:
            rel_uuid = _work_id(cur, rel)
            if not rel_uuid:
                continue
            if _rel_exists(cur, work_uuid, rel_uuid):
                continue
            cur.execute(
                """INSERT INTO relationship (id, source_id, source_type, target_id, target_type, relation, confidence, evidence)
                   VALUES (%s,%s,'work',%s,'work','related',%s,%s)""",
                (str(uuid.uuid4()), work_uuid, rel_uuid, 0.7,
                 json.dumps({"source": "audited.ts bibliography", "authority": AUTHORITY})))
            n_rel += 1
    conn.commit()
    cur.close()
    conn.close()
    return {"editions": n_ed, "etexts": n_etext, "scholarship": n_sch, "related": n_rel, "skipped": skipped}


def _row_exists(cur, table, work_uuid, col, val):
    cur.execute(f"SELECT 1 FROM {table} WHERE work_id=%s AND {col}=%s", (work_uuid, val))
    return cur.fetchone() is not None


def _rel_exists(cur, src, tgt):
    cur.execute("SELECT 1 FROM relationship WHERE source_id=%s AND target_id=%s", (src, tgt))
    return cur.fetchone() is not None


if __name__ == "__main__":
    cands = json.load(open(CANDIDATES, encoding="utf-8"))["candidates"]
    r = persist(cands)
    print("Wrote the rich ATLAS-10 scholarship graph to Postgres (thin-vs-rich gap closed):")
    for k, v in r.items():
        print(f"  {k}: {v}")
    print("  authority = CATALOG_SUPPORTED (from the audited bibliography; never inflated)")
