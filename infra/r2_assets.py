#!/usr/bin/env python3
"""infra/r2_assets.py — the Pāṭala content-addressed R2 asset store (I2 primitive).

The Atlas storage rule: **Postgres stores what things ARE and how they relate. R2 stores the bytes.**
This module is the artifact-truth layer — the four operations the blueprint specifies, keyed by
SHA-256 so the same bytes always have the same identity (immutable artifact history, no blockchain).

    put_asset(data, media_type, bucket='source', rights=None) -> asset record
    get_asset(sha256, bucket='source')                -> bytes
    verify_asset(sha256, data, bucket='source')       -> bool
    presign_upload(...)                               -> (url, form) for direct browser->R2 upload

Object layout under the `patala` R2 bucket:
    patala/{bucket}/objects/sha256/{first2}/{rest}/blob

    patala/public/       rights-cleared texts, TEI, snapshots, released translations
    patala/source/       factory source files, e-texts, OCR, transcriptions, source PDFs (private)
    patala/manuscripts/  user uploads, scans, TIFF/JPEG, HTR inputs (very controlled)
    patala/artifacts/    T1/L0/ARGMAP/L2/L200/C1, proof, benchmark outputs (private until promoted)
    patala/releases/     versioned open-data snapshots

Usage:
    python3 infra/r2_assets.py put --file data/corpus/sources/x/x.txt
    python3 infra/r2_assets.py get --sha <sha256> [--bucket source] [--out -]
    python3 infra/r2_assets.py verify --file data/corpus/sources/x/x.txt --sha <sha256>
"""
from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path

ENDPOINT = os.environ.get(
    "R2_ENDPOINT",
    "https://954612afb5a97bb15dddcdc70176813d.r2.cloudflarestorage.com",
)
BUCKET = os.environ.get("PATALA_R2_BUCKET", "patala")
ACCESS_KEY = os.environ.get("R2_ACCESS_KEY_ID", os.environ.get("AWS_ACCESS_KEY_ID", ""))
SECRET_KEY = os.environ.get("R2_SECRET_ACCESS_KEY", os.environ.get("AWS_SECRET_ACCESS_KEY", ""))

# canonical prefix folders
ALLOWED = {"public", "source", "manuscripts", "artifacts", "releases", "objects"}


def _client():
    import boto3
    if not ACCESS_KEY or not SECRET_KEY:
        raise RuntimeError("set R2_ACCESS_KEY_ID + R2_SECRET_ACCESS_KEY (or AWS_*)")
    return boto3.client(
        "s3",
        endpoint_url=ENDPOINT,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name="auto",
    )


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _key(sha: str, bucket: str) -> str:
    return f"{bucket}/objects/sha256/{sha[:2]}/{sha[2:]}/blob"


def put_asset(data: bytes, media_type: str = "application/octet-stream",
              bucket: str = "source", rights: dict | None = None) -> dict:
    """Upload bytes content-addressed by SHA-256. Idempotent — same bytes = same key."""
    if bucket not in ALLOWED:
        raise ValueError(f"bucket must be one of {sorted(ALLOWED)}, got {bucket!r}")
    sha = _sha256(data)
    key = _key(sha, bucket)
    c = _client()
    c.put_object(Bucket=BUCKET, Key=key, Body=data, ContentType=media_type)
    return {
        "asset_id": f"pt:asset:{sha[:12]}",
        "sha256": sha,
        "storage_key": key,
        "media_type": media_type,
        "byte_count": len(data),
        "bucket": bucket,
        "rights": rights,
    }


def get_asset(sha: str, bucket: str = "source", out: str | None = None) -> bytes:
    c = _client()
    obj = c.get_object(Bucket=BUCKET, Key=_key(sha, bucket))
    data = obj["Body"].read()
    if out and out != "-":
        Path(out).write_bytes(data)
    return data


def verify_asset(sha: str, data: bytes, bucket: str = "source") -> bool:
    """Verify stored bytes match the claimed SHA-256."""
    return _sha256(data) == sha and get_asset(sha, bucket) == data


def head_asset(sha: str, bucket: str = "source") -> dict | None:
    try:
        c = _client()
        r = c.head_object(Bucket=BUCKET, Key=_key(sha, bucket))
        return {"sha256": sha, "bucket": bucket, "byte_count": r["ContentLength"],
                "media_type": r.get("ContentType"), "storage_key": _key(sha, bucket)}
    except Exception:
        return None


def presign_upload(sha: str, media_type: str, bucket: str = "source", expires: int = 900) -> dict:
    """Return a presigned PUT URL for direct browser->R2 upload (never pipe bytes through the app)."""
    import boto3
    s3 = boto3.client("s3", endpoint_url=ENDPOINT,
                      aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY,
                      region_name="auto")
    url = s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": BUCKET, "Key": _key(sha, bucket), "ContentType": media_type},
        ExpiresIn=expires,
    )
    return {"url": url, "method": "PUT", "storage_key": _key(sha, bucket), "sha256": sha,
            "media_type": media_type, "expires_in_s": expires}


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("put", help="content-address + upload a file")
    p.add_argument("--file", required=True)
    p.add_argument("--bucket", default="source", choices=sorted(ALLOWED))
    p.add_argument("--media-type", default="text/plain; charset=utf-8")

    g = sub.add_parser("get", help="fetch by sha256")
    g.add_argument("--sha", required=True)
    g.add_argument("--bucket", default="source", choices=sorted(ALLOWED))
    g.add_argument("--out", default=None, help="file path or '-' for stdout")

    v = sub.add_parser("verify", help="verify a file's bytes match a stored sha256")
    v.add_argument("--file", required=True)
    v.add_argument("--sha", required=True)
    v.add_argument("--bucket", default="source", choices=sorted(ALLOWED))

    h = sub.add_parser("head", help="check a sha256 exists")
    h.add_argument("--sha", required=True)
    h.add_argument("--bucket", default="source", choices=sorted(ALLOWED))

    m = sub.add_parser("migrate", help="content-address + upload the on-disk Sanskrit source files")
    m.add_argument("--dir", default="data/corpus/sources", help="dir of <work>/<work>.txt works")
    m.add_argument("--bucket", default="source", choices=sorted(ALLOWED))
    m.add_argument("--dry-run", action="store_true")

    a = ap.parse_args()

    if a.cmd == "put":
        data = Path(a.file).read_bytes()
        rec = put_asset(data, media_type=a.media_type, bucket=a.bucket)
        print(f"put {rec['sha256']}  {rec['byte_count']}B  {rec['storage_key']}")
    elif a.cmd == "get":
        data = get_asset(a.sha, bucket=a.bucket, out=a.out)
        if a.out in (None, "-"):
            sys.stdout.buffer.write(data)
        else:
            print(f"wrote {a.out} ({len(data)}B)")
    elif a.cmd == "verify":
        data = Path(a.file).read_bytes()
        ok = verify_asset(a.sha, data, bucket=a.bucket)
        print("VERIFY PASS" if ok else "VERIFY FAIL")
        return 0 if ok else 1
    elif a.cmd == "head":
        rec = head_asset(a.sha, bucket=a.bucket)
        print(rec if rec else "not_found")
        return 0 if rec else 1
    elif a.cmd == "migrate":
        root = Path(a.dir)
        files = sorted(p for p in root.glob("*/*.txt") if p.is_file())
        migrated = skipped = 0
        for p in files:
            sha = _sha256(p.read_bytes())
            if head_asset(sha, a.bucket):
                skipped += 1
                continue
            if a.dry_run:
                print(f"[dry] {p.name:30} {p.stat().st_size:>9}B sha={sha[:12]}")
                continue
            data = p.read_bytes()
            put_asset(data, media_type="text/plain; charset=utf-8", bucket=a.bucket)
            print(f"put   {p.name:30} {len(data):>9}B sha={sha[:12]}")
            migrated += 1
        print(f"\n{migrated} uploaded, {skipped} already present, {len(files)} total")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
