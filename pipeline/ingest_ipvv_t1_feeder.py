#!/usr/bin/env python3
"""pipeline/ingest_ipvv_t1_feeder.py — wire the IPVV -> factory ARGMAP production path.

The bottleneck (the directive): SOURCE -> ARGMAP. The factory ARGMAP generator requires a committed
T1 (it fails closed DEPENDENCY_BLOCKED without one). The IPVV passages have full Sanskrit but no
factory T1 except ipvv:V2O:k1.

This feeder registers the IPVV passages' Sanskrit as SOURCE objects (so the T1 worker can consume
them) and prepares the ARGMAP batch. It does NOT execute model calls (those are the Agent 2 / factory
run, which shares the live model API and must be launched deliberately, not by an autonomous agent
while the overnight factory is running).

Run (after the overnight factory is quiescent, or as the factory's intake step):
    python3 pipeline/ingest_ipvv_t1_feeder.py --prepare
    # then feed each passage's Sanskrit to the T1 worker, then ARGMAP generator:
    python3 pipeline/argmap_production.py --passage ipvv:V2L

Design: the passages are multi-kārikā prose, not single verses. The T1 worker's single-verse
_segment expects IAST verse tokens. For long prose we chunk the passage into kārikā-sized units and
register each as its own SOURCE object (ipvv:V2L:k1, :k2, ...) — matching the existing ipvv:V2O:k1
convention — so the existing single-verse T1 worker can process them unchanged.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, "/root/projects/patala/pipeline")
import object_registry as R  # noqa: E402

IPVV_DIR = "/root/projects/patala/data/published/ipvv"


def _sha256(s: str) -> str:
    return hashlib.sha256(s.strip().encode("utf-8")).hexdigest()


def _passages() -> list[dict]:
    """Load all published IPVV passages with their Sanskrit source text."""
    out = []
    idx = os.path.join(IPVV_DIR, "index.json")
    if not os.path.exists(idx):
        return out
    for p in json.load(open(idx, encoding="utf-8"))["passages"]:
        f = os.path.join(IPVV_DIR, p["file"])
        if not os.path.exists(f):
            continue
        d = json.load(open(f, encoding="utf-8"))
        src = d.get("source", {})
        text = src.get("text", "") if isinstance(src, dict) else ""
        if text:
            out.append({"locator": d.get("chunk") or p["locator"], "sanskrit": text})
    return out


def _kārikā_chunks(text: str, max_chars: int = 1200) -> list[str]:
    """Chunk long IPVV prose into kārikā-sized units for the single-verse T1 worker.

    Splits on double-newline or sentence boundaries within max_chars. Each chunk becomes a unit.
    """
    # strip page markers
    text = re.sub(r"\(page \d+\)", "", text)
    units = []
    cur = ""
    for para in re.split(r"\n\s*\n", text):
        para = " ".join(para.split())
        if not para:
            continue
        if len(cur) + len(para) <= max_chars:
            cur = (cur + " " + para).strip()
        else:
            if cur:
                units.append(cur)
            # further split if a single paragraph is huge
            while len(para) > max_chars:
                units.append(para[:max_chars])
                para = para[max_chars:]
            cur = para
    if cur:
        units.append(cur)
    return [u for u in units if len(u) > 80]


def prepare(passage_locator: str | None = None) -> dict:
    """Register IPVV passage Sanskrit as SOURCE objects (idempotent), chunked into kārikā units."""
    passages = _passages()
    if passage_locator:
        norm = passage_locator.replace("-", "").lower()
        passages = [p for p in passages if norm in p["locator"].replace("-", "").lower()]
    registered = 0
    chunks_total = 0
    for p in passages:
        # locator like 'chunkV2-L-sastho...' -> passage tag 'V2L'
        m = re.match(r".*?(V\d+)[-]?([A-Z]+)", p["locator"])
        base = (m.group(1) + (m.group(2) if m.group(2) else "")) if m else p["locator"].replace("chunk", "").split("-")[0]
        chunks = _kārikā_chunks(p["sanskrit"])
        for i, chunk in enumerate(chunks, 1):
            oid = f"ipvv:{base}:k{i}"
            if R.current("SOURCE", oid):
                continue
            h = _sha256(chunk)
            R.commit("SOURCE", oid, h, created_by="ipvv-t1-feeder", status="RAW_SANSKRIT",
                     payload={"verse": chunk, "source_text": chunk})
            registered += 1
            chunks_total += 1
    return {"passages": len(passages), "chunks_registered": registered, "chunks_total": chunks_total}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepare", action="store_true")
    ap.add_argument("--passage", help="optional locator filter")
    a = ap.parse_args()
    if a.prepare:
        r = prepare(a.passage)
        print(f"IPVV -> factory ARGMAP path prepared: {r['passages']} passages, "
              f"{r['chunks_registered']} kārikā SOURCE units registered "
              f"(total {r['chunks_total']})")
        print("Next (Agent 2 / factory run): T1 worker on ipvv:V*:k* -> ARGMAP generator.")
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
