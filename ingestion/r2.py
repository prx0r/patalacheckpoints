"""ingestion/r2.py — the reusable R2 Bronze-snapshot store (the immutable data lake).

The permanent, reusable primitive for the FIRST step of every ingestion: get the source on R2 as an
immutable Bronze snapshot + manifest. Everything downstream (SourceAsserter, reconcile, the sites)
reads from R2 rather than scattering source files.

ALIGNED with existing infra (do not reinvent):
  - byte store : infra/r2_assets.py (content-addressed SHA-256, the 'patala' bucket)
  - This module adds the SNAPSHOT layer on top: a versioned, immutable
    `source/ingestion/<source>/snapshots/<snapshot_id>/` namespace + manifest.json.

Layout (under the `patala` R2 bucket):
    source/ingestion/PANDIT/snapshots/pandit-2026-08-14/works.csv
    source/ingestion/PANDIT/snapshots/pandit-2026-08-14/manifest.json

Rules (from ingestion-refinery.md §1-§2):
  - Never mutate a snapshot. A new upstream state = a NEW snapshot_id; both survive.
  - Every snapshot carries a manifest {source, snapshot_id, retrieved_at, files:[{path,sha256,bytes}]}.
  - Content-addressed blobs: same bytes = same key (idempotent upload).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Optional

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from infra import r2_assets  # noqa: E402


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class SnapshotStore:
    """Reusable snapshot store on R2 (and a local mirror for dry-run/offline/tests)."""

    def __init__(self, r2_bucket: str = "patala", local_dir: Optional[str] = None):
        self.r2_bucket = r2_bucket
        self.local_dir = Path(local_dir) if local_dir else None
        # snapshot files are content-addressed under the 'source' prefix
        self._prefix = "source/ingestion"

    # ---- key layout ----
    def _prefix_for(self, source: str, snapshot_id: str) -> str:
        return f"{self._prefix}/{source.upper()}/snapshots/{snapshot_id}"

    def _local_dir_for(self, source: str, snapshot_id: str) -> Path:
        return self.local_dir / source.upper() / "snapshots" / snapshot_id

    # ---- put (Bronze) ----
    def put_snapshot(self, source: str, snapshot_id: str, files: dict[str, bytes],
                     *, dry_run: bool = False,
                     retrieved_at: str | None = None,
                     upstream_version: str | None = None,
                     license: str | None = None,
                     adapter_version: str | None = None) -> dict:
        """Upload a snapshot's files (content-addressed) + manifest. Idempotent by content.

        files: {logical_path: bytes}. The manifest records sha256 per file.
        Returns the manifest dict.
        """
        retrieved_at = retrieved_at or __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ",
                                                                  __import__("time").gmtime())
        file_meta = []
        for path, data in files.items():
            sha = _sha256(data)
            file_meta.append({"path": path, "sha256": sha, "bytes": len(data)})
            if not dry_run:
                # content-addressed: same bytes = same key under the snapshot prefix (idempotent)
                key = f"{self._prefix_for(source, snapshot_id)}/{path}"
                r2_assets._client().put_object(
                    Bucket=self.r2_bucket, Key=key, Body=data,
                    ContentType="application/octet-stream")
        manifest = {
            "schema": "patala.ingestion.source-snapshot.v1",
            "source": source.upper(),
            "snapshot_id": snapshot_id,
            "retrieved_at": retrieved_at,
            "upstream_version": upstream_version,
            "adapter_version": adapter_version,
            "license": license,
            "files": file_meta,
            "bucket": self.r2_bucket,
            "prefix": self._prefix_for(source, snapshot_id),
        }
        if not dry_run:
            r2_assets._client().put_object(
                Bucket=self.r2_bucket,
                Key=f"{self._prefix_for(source, snapshot_id)}/manifest.json",
                Body=json.dumps(manifest, indent=2, ensure_ascii=False).encode("utf-8"),
                ContentType="application/json")
        # local mirror (for offline/tests)
        if self.local_dir and not dry_run:
            d = self._local_dir_for(source, snapshot_id)
            d.mkdir(parents=True, exist_ok=True)
            for path, data in files.items():
                (d / path).write_bytes(data)
            (d / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False),
                                             encoding="utf-8")
        return manifest

    # ---- get / list ----
    def manifest(self, source: str, snapshot_id: str) -> Optional[dict]:
        """Fetch a snapshot manifest from R2 (or the local mirror)."""
        key = f"{self._prefix_for(source, snapshot_id)}/manifest.json"
        try:
            obj = r2_assets._client().get_object(Bucket=self.r2_bucket, Key=key)
            return json.loads(obj["Body"].read().decode("utf-8"))
        except Exception:  # noqa: BLE001
            if self.local_dir:
                p = self._local_dir_for(source, snapshot_id) / "manifest.json"
                if p.exists():
                    return json.loads(p.read_text(encoding="utf-8"))
            return None

    def list_snapshots(self, source: str) -> list[dict]:
        """List all snapshot manifests for a source (both survive — nothing is mutated)."""
        prefix = f"{self._prefix}/{source.upper()}/snapshots/"
        c = r2_assets._client()
        keys = []
        paginator = c.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self.r2_bucket, Prefix=prefix):
            keys += [o["Key"] for o in page.get("Contents", []) if o["Key"].endswith("/manifest.json")]
        out = []
        for k in keys:
            try:
                obj = c.get_object(Bucket=self.r2_bucket, Key=k)
                out.append(json.loads(obj["Body"].read().decode("utf-8")))
            except Exception:  # noqa: BLE001
                continue
        return out


def put_file_snapshot(source: str, snapshot_id: str, paths: list[str],
                      *, dry_run: bool = False, **kw) -> dict:
    """CLI convenience: put one or more local files as a Bronze snapshot.

    paths: local files (their basenames become the snapshot's logical paths).
    """
    files = {}
    for p in paths:
        data = Path(p).read_bytes()
        files[Path(p).name] = data
    store = SnapshotStore(local_dir=None)
    return store.put_snapshot(source, snapshot_id, files, dry_run=dry_run, **kw)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Put a source snapshot onto R2 (Bronze data lake).")
    ap.add_argument("--source", required=True, help="PANDIT / GRETIL / SARIT / ...")
    ap.add_argument("--snapshot-id", required=True, help="e.g. pandit-2026-08-14")
    ap.add_argument("--file", action="append", default=[], help="local file(s) to include (repeatable)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--license")
    ap.add_argument("--upstream-version")
    ap.add_argument("--adapter-version")
    a = ap.parse_args()
    if not a.file:
        raise SystemExit("need at least one --file")
    m = put_file_snapshot(a.source, a.snapshot_id, a.file, dry_run=a.dry_run,
                          license=a.license, upstream_version=a.upstream_version,
                          adapter_version=a.adapter_version)
    print("mode:", "DRY-RUN (no upload)" if a.dry_run else "UPLOADED")
    print(json.dumps(m, indent=2, ensure_ascii=False))
