#!/usr/bin/env python3
"""pipeline/build_release_snapshot.py — CP5: the open-data release snapshot (the OpenAlex differentiator).

Exports the ingested SOURCE registry + bibliography into an open downloadable dataset on R2
`releases/<date>/` — JSONL (universal) + Parquet (analytical). Researchers can download Pāṭala
without touching the API (the OpenAlex API + complete-snapshot model, `atlas-engineering-blueprint.md`
§16, `openpatala/reference/openalex/snapshots/`).

What it exports (from the live object_registry):
  works.jsonl / works.parquet   — the SOURCE objects (the harvested corpus, id + title + author + provenance)
  registry.json                — the per-layer counts + the release manifest (hashes, schema, date)

Design (the perf doctrine):
  compute on write, immutable, content-addressed. The release is a snapshot: a new commit = a NEW
  dated directory; both survive (never mutate). Each release is self-describing (manifest with hashes).

Usage:
  python3 pipeline/build_release_snapshot.py            # build to ./release-staging + upload to R2
  python3 pipeline/build_release_snapshot.py --dry-run  # build + print manifest, no R2 upload
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "pipeline"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def build_works():
    """Export the SOURCE registry -> list of work records (id, title, author, source, provenance)."""
    import object_registry as R
    src = R._load("SOURCE")["objects"]
    works = []
    for oid, versions in src.items():
        # the latest version's payload
        v = versions if isinstance(versions, dict) else {}
        payload = v.get("payload", {}) if isinstance(v, dict) else {}
        if isinstance(payload, dict) and "payload" in payload:
            payload = payload["payload"]
        title = payload.get("title") if isinstance(payload, dict) else ""
        author = payload.get("author", "") if isinstance(payload, dict) else ""
        source = payload.get("source", "") if isinstance(payload, dict) else ""
        prov = payload.get("provenance", {}) if isinstance(payload, dict) else {}
        works.append({
            "id": oid,
            "title": title or oid,
            "author": author,
            "source": source,
            "license": prov.get("license", ""),
            "status": prov.get("status", ""),
        })
    return works


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="build + print, no R2 upload")
    ap.add_argument("--out", default=str(Path(ROOT) / "release-staging"))
    a = ap.parse_args()

    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out = Path(a.out) / date
    out.mkdir(parents=True, exist_ok=True)

    # 1. the works (from the live SOURCE registry)
    works = build_works()
    jsonl_path = out / "works.jsonl"
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for w in works:
            f.write(json.dumps(w, ensure_ascii=False) + "\n")

    # 2. Parquet (analytical) — pyarrow
    parquet_path = out / "works.parquet"
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
        table = pa.Table.from_pylist(works)
        pq.write_table(table, parquet_path)
    except Exception as e:  # noqa: BLE001
        print(f"  (parquet skipped: {e})")
        parquet_path = None

    # 3. the registry summary + release manifest
    import object_registry as R
    s = R.summary()
    registry_json = {k: v.get("objects", 0) for k, v in s.items()}
    files = [{"path": jsonl_path.name, "bytes": jsonl_path.stat().st_size,
              "sha256": _sha(jsonl_path.read_bytes()), "rows": len(works)}]
    if parquet_path and parquet_path.exists():
        files.append({"path": parquet_path.name, "bytes": parquet_path.stat().st_size,
                      "sha256": _sha(parquet_path.read_bytes()), "rows": len(works)})
    manifest = {
        "schema": "patala.open-data.release.v1",
        "release": date,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "counts": registry_json,
        "n_works": len(works),
        "files": files,
        "design": "open downloadable dataset; a new release is a NEW dated dir (both survive)",
    }
    with open(out / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"=== RELEASE SNAPSHOT BUILT → {out} ===")
    print(f"  {len(works)} works (SOURCE registry)")
    print(f"  files: {[f['path'] for f in files]}")
    print(f"  registry: SOURCE={registry_json.get('SOURCE')}, T1={registry_json.get('T1')}, "
          f"L0={registry_json.get('L0')}")

    if a.dry_run:
        print("  DRY-RUN — not uploaded to R2")
        return 0

    # 4. upload to R2 releases/<date>/
    from infra.r2_assets import _client
    c = _client()
    for f in files:
        p = out / f["path"]
        c.put_object(Bucket="patala", Key=f"releases/{date}/{f['path']}", Body=p.read_bytes())
    c.put_object(Bucket="patala", Key=f"releases/{date}/manifest.json",
                 Body=json.dumps(manifest, ensure_ascii=False).encode())
    print(f"  UPLOADED to R2: patala://releases/{date}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
