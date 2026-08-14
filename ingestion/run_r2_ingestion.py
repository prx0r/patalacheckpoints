#!/usr/bin/env python3
"""ingestion/run_r2_ingestion.py — R2-driven full-file ingestion into the SOURCE registry.

The honest intake runner: register the R2 source snapshots (GRETIL / MUKTABODHA / SARIT / PANDiT)
as SOURCE objects in the object registry, WITH provenance + license, reusing the existing adapter
contract + the object_registry commit path. Reads the R2/local snapshot FILES (not the network).

Why not the strict gold-reconcile path:
  The SourceAsserter's EXACT/PROBABLE gold requires a RICH canonical set (title + author). The thin
  bibliography has only id/title, and the rich set is ~6 entries — so at scale the asserter produces
  almost all POSSIBLE (scholar queue), NOT gold. That is CORRECT and honest (no fake verified=true),
  but it does not fill the factory. The right move for "full file ingestion" is to register the
  e-texts as SOURCE objects with provenance + a MACHINE_PROPOSED identity, which the factory consumes.
  The gold-reconcile + human-adjudication pass is the LATER, separate step (data capital).

This runner is idempotent: it dedups against the committed SOURCE registry by external_id, so re-runs
are safe (no duplicate intake).

Usage:
  python3 -m ingestion.run_r2_ingestion --source GRETIL   [--dry-run] [--commit]
  python3 -m ingestion.run_r2_ingestion --all             [--dry-run] [--commit]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "pipeline", ROOT / "source-evidence" / "schema",
          ROOT / "source-evidence" / "evals" / "patala" / "tasks"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

# the extracted snapshot staging dirs (populated from R2, or a caller-provided local mirror)
STAGING = Path("/tmp/opencode/r2staging")


def _source_records(adapter):
    """Fetch + emit ExternalRecords from an adapter, returning list of dicts (emit() shape)."""
    raws = adapter.fetch({})
    recs = adapter.emit_external_records(raws)
    return [r.emit() for r in recs], raws


def _tei_header(path: Path):
    """Parse the TEI <title> + <author> from a file header (GRETIL/SARIT), never guessed."""
    try:
        from lxml import etree
        tree = etree.parse(str(path))
        ns = {"t": "http://www.tei-c.org/ns/1.0"}
        root = tree.getroot()
        title = " ".join((root.findall(".//t:title", ns)[0].text or "").split()) if root.findall(".//t:title", ns) else path.stem
        authors = [a.text for a in root.findall(".//t:author", ns) if a.text and a.text.strip()]
        return {"title": title, "author": " ; ".join(a.strip() for a in authors[:3])}
    except Exception:  # noqa: BLE001  (no lxml -> fallback regex)
        text = path.read_text(encoding="utf-8", errors="ignore")
        import re
        m = re.search(r"<title[^>]*>(.*?)</title>", text, re.S)
        title = re.sub(r"<[^>]+>", "", m.group(1)) if m else ""
        title = re.sub(r"\s+", " ", title).strip()[:200] or path.stem
        am = re.search(r"<author[^>]*>(.*?)</author>", text, re.S)
        author = re.sub(r"<[^>]+>", "", am.group(1)) if am else ""
        author = re.sub(r"\s+", " ", author).strip()[:100]
        return {"title": title, "author": author}


def _tei_records(source: str, dir_: Path):
    """Read all TEI files in a snapshot dir -> ExternalRecord-shaped dicts (file ingestion)."""
    from external_record import ExternalRecord
    import hashlib
    out = []
    for p in sorted(dir_.glob("*.xml")):
        h = _tei_header(p)
        text = p.read_text(encoding="utf-8", errors="ignore")
        incipit = re.sub(r"<[^>]+>", " ", text)[:200]
        rec = ExternalRecord(
            source=source,
            external_id=f"{source.lower()}:{p.stem}",
            title_raw=h["title"],
            author_raw=h["author"],
            incipit_raw=incipit,
            retrieved_at="snapshot",
            extra={"path": p.name, "license": "per-file", "url": f"r2://patala/source/ingestion/{source.upper()}/snapshots/",
                   "design_law": f"{source} e-text is a TextInstance, not a canonical Work (resolve separately)"},
        )
        out.append(rec.emit())
    return out


def _commit_source(records, source, created_by="r2-ingestion"):
    """Commit SOURCE objects, dedup by external_id against the existing registry."""
    import object_registry as R
    existing = set(R._load("SOURCE")["objects"].keys())
    entries = []
    for rec in records:
        eid = rec.get("external_id") or rec.get("id")
        if not eid:
            continue
        if eid in existing:
            continue  # already committed — idempotent
        fields = rec.get("fields", {})
        title = (fields.get("title") or rec.get("title_raw") or rec.get("title") or eid).strip()
        payload = {
            "title": title,
            "source": source,
            "author": fields.get("author") or rec.get("author_raw", ""),
            "provenance": {"external_id": eid, "license": rec.get("extra", {}).get("license", ""),
                           "source_authority": source, "retrieved_at": rec.get("retrieved_at", ""),
                           "external_url": (rec.get("extra", {}) or {}).get("url", ""),
                           "status": "MACHINE_PROPOSED"},
            "payload": rec,  # the full raw ExternalRecord
        }
        h = hashlib.sha256(json.dumps(rec, sort_keys=True, default=str).encode()).hexdigest()
        entries.append({"object_id": eid, "input_hash": h, "payload": payload})
    if not entries:
        return 0
    R.commit_batch("SOURCE", entries, created_by)
    return len(entries)


def _adapter_for(source: str, staging: Path):
    if source == "GRETIL":
        from ingestion.adapters.gretil import GretilAdapter
        return GretilAdapter()  # R2 snapshot read via a local dir below; see caller
    if source == "MUKTABODHA":
        from ingestion.adapters.muktabodha import MuktabodhaAdapter
        return MuktabodhaAdapter(local_dir=str(staging / "muktabodha"))
    if source == "SARIT":
        from ingestion.adapters.sarit import SaritAdapter
        return SaritAdapter()
    if source == "PANDIT":
        from ingestion.adapters.pandit import PanditBulkAdapter
        return PanditBulkAdapter(csv_path=str(staging / "pandit-export.csv"),
                                 content_types=["Work"])
    raise ValueError(f"unknown source {source}")


def _extract_tar(source: str, staging: Path):
    """Extract the source snapshot tarballs into staging (idempotent). Returns staging dir."""
    import tarfile
    jobs = {
        "GRETIL": ("gretil-tei.tar.gz", "gretil-tei"),
        "MUKTABODHA": ("muktabodha.tar.gz", "muktabodha"),
        "SARIT": ("sarit-tei.tar.gz", "sarit-tei"),
    }
    if source not in jobs:
        return staging
    tgz, out = jobs[source]
    tgz_path = staging / tgz
    out_dir = staging / out
    if tgz_path.exists() and not (out_dir.exists() and any(out_dir.iterdir())):
        out_dir.mkdir(parents=True, exist_ok=True)
        with tarfile.open(tgz_path, "r:gz") as t:
            t.extractall(out_dir)
    return staging


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["GRETIL", "MUKTABODHA", "SARIT", "PANDIT"])
    ap.add_argument("--all", action="store_true", help="ingest all four sources")
    ap.add_argument("--dry-run", action="store_true", help="report only, no registry writes")
    ap.add_argument("--commit", action="store_true", help="commit SOURCE objects to the registry")
    a = ap.parse_args()

    sources = ["GRETIL", "MUKTABODHA", "SARIT", "PANDIT"] if a.all else [a.source]
    total = 0
    for src in sources:
        staging = _extract_tar(src, STAGING)
        try:
            if src in ("GRETIL", "SARIT"):
                # file-based TEI ingestion (reads the R2/local snapshot files, not the network)
                tei_dir = staging / ("gretil-tei" if src == "GRETIL" else "sarit-tei")
                records = _tei_records(src, tei_dir)
            else:
                adapter = _adapter_for(src, staging)
                records, _ = _source_records(adapter)
        except Exception as e:  # noqa: BLE001
            print(f"[{src}] ERROR: {e}")
            continue
        print(f"[{src}] records from snapshot: {len(records)}")
        if a.commit and not a.dry_run:
            n = _commit_source(records, src)
            total += n
            print(f"[{src}] committed {n} SOURCE objects")
        else:
            print(f"[{src}] DRY-RUN — not committed (pass --commit to write)")
    if a.commit and not a.dry_run:
        print(f"TOTAL committed: {total}")
    else:
        print("DRY-RUN — no writes (pass --commit)")


if __name__ == "__main__":
    main()
