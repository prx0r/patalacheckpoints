#!/usr/bin/env python3
"""emit_published_json.py — publish the phase-1 OK passages as lazy JSON assets.

Reads the phase-1 canonical records (ipvv_passages.jsonl) and emits:

  data/published/ipvv/index.json                 (structural only: work, passages[id,locator,order,file])
  data/published/ipvv/pt-passage-<slug>.json     (one per OK passage, the canonical record)

The index is small and structural — no huge source/target arrays. Each passage JSON is the
canonical phase-1 record (source range + text, l2_text, l0, argmap, vol, section, status). The
pāṭala loader (published.ts) reads the index lazily and shapes each record into the PublishedTranslation
the reader/API expect, so /read and /api/resolve consume the SAME canonical object.

Usage:
  python3 pipeline/emit_published_json.py --in /tmp/ipvv_phase1/ipvv_passages.jsonl \
      --out /root/projects/patala/data/published/ipvv
"""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path


def slugify(pid: str) -> str:
    """Stable filename from a passage id: pt:passage:ipvv:... -> pt-passage-ipvv-....json"""
    return re.sub(r"[^A-Za-z0-9]+", "-", pid.replace("pt:passage:", "pt-passage-")).strip("-")


def immutable_from_id(pid: str) -> str:
    """The immutable passage id (stable hash), independent of mutable locator aliases."""
    h = hashlib.sha1(pid.encode("utf-8")).hexdigest()[:12]
    return f"pt:pid:ipvv:{h}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out", dest="out", required=True)
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(exist_ok=True, parents=True)

    records = []
    for line in Path(args.src).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("status") == "OK":
            records.append(r)

    index = {
        "work_id": "isvarapratyabhijnavivrtivimarsini",
        "count": len(records),
        "passages": [],
    }
    for i, r in enumerate(sorted(records, key=lambda x: (x["vol"], x.get("source", {}).get("start", 0)))):
        pid = r["id"]
        fid = slugify(pid)
        # canonical file: store the record + add immutable id
        record = dict(r)
        record["immutable_id"] = immutable_from_id(pid)
        fpath = out_dir / f"{fid}.json"
        fpath.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        index["passages"].append({
            "id": pid,
            "immutable_id": record["immutable_id"],
            "locator": r.get("chunk", ""),
            "order": i,
            "file": f"{fid}.json",
            "vol": r.get("vol"),
        })

    (out_dir / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {len(records)} passage JSON + index.json → {out_dir}")


if __name__ == "__main__":
    main()
