#!/usr/bin/env python3
"""pipeline/catalog.py — the unified Pāṭala catalog (the endgame tracking view).

The single queryable view of EVERY work in the pipeline, showing:

  WORK: <work_id>
    bibliography:  title / author / translation_status / verified      (from data/atlas)
    source:        on-disk source linked? + refs                      (from SOURCE registry)
    layers:        SOURCE/T1/ARGMAP/L0/L2/L200/C1/THEME/ARGUMENT/
                   SYNTHESIS/ESSAY/EDUCATION  done / total + status   (from each registry)
    latest_audit:  the most recent factory-audit events               (from factory-audit.jsonl)

This is how the whole pipeline — bibliography → source → translation → high layers — becomes auditable
and tracked. The registries are the authoritative per-layer state; the audit ledger is the in-order
action trail; the atlas is the bibliography; the catalog is the projection that ties them together.

Usage:
  python3 pipeline/catalog.py                     # all works
  python3 pipeline/catalog.py --work kramasadbhava
  python3 pipeline/catalog.py --json [--work x]   # machine-readable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R

ROOT = Path("/root/projects/patala")
AUDIT_LEDGER = ROOT / "data/corpus/downloads/factory-audit.jsonl"
LEDGER = ROOT / "data/corpus/downloads/translation-state-ledger.json"

# the full canonical layer set (incl. high layers) — SOURCE first, then the derivation chain
LAYERS = ["SOURCE", "T1", "ARGMAP", "L0", "L2", "L200", "C1",
          "THEME", "ARGUMENT", "SYNTHESIS", "ESSAY", "EDUCATION"]


def _load_atlas() -> dict:
    """Parse data/atlas/*.ts BibliographyRecord entries -> {id: record}."""
    records = {}
    for fn in ("bibliographySeed.ts", "audited.ts", "sivaqueueSeed.ts", "sivaqueue34Seed.ts"):
        p = ROOT / "data/atlas" / fn
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        # handle both 'id: "..."' and '"id": "..."' record forms
        for m in re.finditer(r"\{\s*\"?id\"?\s*:\s*\"([a-z0-9-]+)\"", text):
            oid = m.group(1)
            block = text[m.start():m.start() + 1600]
            title = re.search(r'work:\s*"([^"]+)"', block) or re.search(r'"work":\s*"([^"]+)"', block)
            status = re.search(r'translationStatus:\s*"([^"]+)"', block) or re.search(r'"translationStatus":\s*"([^"]+)"', block)
            verified = re.search(r'verified:\s*(true|false)', block) or re.search(r'"verified":\s*(true|false)', block)
            records[oid] = {
                "id": oid,
                "title": title.group(1) if title else oid,
                "translation_status": status.group(1) if status else "unknown",
                "verified": verified.group(1) if verified else None,
            }
    return records


def _work_source(work_id: str) -> dict:
    """Source linkage for a work: is a SOURCE registry object present? any on-disk ref?"""
    srcs = [oid for oid, vs in R._load("SOURCE")["objects"].items()
            if vs and not vs[-1].get("superseded") and oid.startswith(work_id)]
    return {"source_objects": len(srcs), "linked": len(srcs) > 0}


def _layer_counts(work_id: str) -> dict:
    """Per-layer committed counts (done/total/stale/status) for a work."""
    out = {}
    for L in LAYERS:
        n_done = n_stale = n_versions = 0
        for oid, vs in R._load(L)["objects"].items():
            if not oid.startswith(work_id):
                continue
            n_versions += len(vs)
            if vs and not vs[-1].get("superseded"):
                n_done += 1
            n_stale += sum(1 for v in vs if v.get("superseded"))
        out[L] = {"done": n_done, "stale": n_stale, "versions": n_versions}
    # denominator: for the derivation layers, the upstream count is the "of"
    return out


def _recent_audit(work_id: str, limit: int = 5) -> list[dict]:
    """The most recent factory-audit events for this work (in order)."""
    events = []
    if AUDIT_LEDGER.exists():
        for line in AUDIT_LEDGER.read_text(encoding="utf-8").splitlines():
            try:
                e = json.loads(line)
            except Exception:
                continue
            if e.get("object_id", "").startswith(work_id):
                events.append(e)
    return events[-limit:]


def _ledger_bibliographic(work_id: str) -> str | None:
    """The bibliographic_id from the operational ledger (if linked)."""
    try:
        d = json.loads(LEDGER.read_text(encoding="utf-8"))
        return d.get("works", {}).get(work_id, {}).get("bibliographic_id")
    except Exception:
        return None


def _all_works() -> list[str]:
    works = set()
    for L in LAYERS:
        for oid in R._load(L)["objects"]:
            if ":" in oid:
                works.add(oid.split(":")[0])
    return sorted(works)


def work_catalog(work_id: str, audit_limit: int = 5) -> dict:
    """The full catalog entry for one work."""
    atlas = _load_atlas()
    bib_id = _ledger_bibliographic(work_id) or (work_id if work_id in atlas else None)
    bib = atlas.get(bib_id, {}) if bib_id else {}
    layers = _layer_counts(work_id)
    return {
        "work": work_id,
        "bibliography": {
            "linked_id": bib_id,
            "title": bib.get("title", work_id),
            "translation_status": bib.get("translation_status", "unknown"),
            "verified": bib.get("verified"),
        } if bib_id else {"linked_id": None, "title": work_id, "translation_status": "not_in_atlas"},
        "source": _work_source(work_id),
        "layers": layers,
        "latest_audit": _recent_audit(work_id, audit_limit),
    }


def render(entry: dict) -> str:
    lines = [f"WORK: {entry['work']}"]
    b = entry["bibliography"]
    lines.append(f"  bibliography: {b.get('title')}  [status: {b.get('translation_status')}"
                 f"{' / verified' if b.get('verified')=='true' else ''}]"
                 f"  linked_id={b.get('linked_id')}")
    lines.append(f"  source: {entry['source']['source_objects']} object(s) "
                 f"({'LINKED' if entry['source']['linked'] else 'unlinked'})")
    for L, c in entry["layers"].items():
        tag = f"  {L:<9} {c['done']} current"
        if c["stale"]:
            tag += f" ({c['stale']} stale)"
        if c["versions"] > c["done"] + c["stale"]:
            tag += f" [{c['versions']} total ver]"
        lines.append(tag)
    if entry["latest_audit"]:
        lines.append("  latest_audit:")
        for e in entry["latest_audit"]:
            lines.append(f"    {e.get('ts','')[:19]} {e.get('event'):<9} {e.get('layer',''):<8} "
                         f"{e.get('object_id','')} {e.get('version','') or e.get('reason','')[:30]}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--audit-limit", type=int, default=5)
    a = ap.parse_args()

    works = [a.work] if a.work else _all_works()
    entries = [work_catalog(w, a.audit_limit) for w in works]
    if a.json:
        print(json.dumps(entries, indent=2, ensure_ascii=False))
    else:
        for e in entries:
            print(render(e))
            print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
