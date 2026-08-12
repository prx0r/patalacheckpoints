#!/usr/bin/env python3
"""pipeline/l0_registry.py — the versioned L0 registry (immutable, superseding).

Per the canonical L0 schema (specs/l0_schema.json): "Never edit an emitted record in place —
a fix emits a new version." This registry tracks L0 VERSIONS per work, so we can see what
versions exist, which is current, and what superseded what.

This is the "track what versions of it exist" piece the autonomous agent needs: an agent
produces a version, marks it committed, and the ledger records it — so the versioned L0 is
immutable history, not an overwritten blob.

Shape:
  l0_versions = {
    "<work_id>": {
      "versions": [ {"version": "v1", "sha256": "...", "committed_by": "...",
                     "committed_at": "...", "status": "MACHINE_PROPOSED",
                     "supersedes": null, "n_records": 0, "n_verses": 0} ],
      "current": "v1"
    }
  }
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

LEDGER_PATH = "/root/projects/patala/data/corpus/downloads/translation-state-ledger.json"
REGISTRY_PATH = "/root/projects/patala/data/corpus/downloads/l0-version-registry.json"


def _load() -> dict:
    if os.path.exists(REGISTRY_PATH):
        return json.load(open(REGISTRY_PATH))
    return {"version": 1, "works": {}}


def _save(reg: dict) -> None:
    with open(REGISTRY_PATH, "w") as fh:
        json.dump(reg, fh, indent=2, ensure_ascii=False)


def l0_versions(work_id: str) -> dict:
    """Return the version history for a work (or an empty entry)."""
    reg = _load()
    return reg["works"].get(work_id, {"versions": [], "current": None})


def commit_l0(work_id: str, records: list[dict], committed_by: str,
              status: str = "MACHINE_PROPOSED", n_verses: int = 0) -> dict:
    """Commit a new immutable L0 version for a work. A fix emits a NEW version (never edit in place).

    records: the canonical L0 records produced by raw_l0.
    Returns the committed version entry.
    """
    reg = _load()
    work = reg["works"].setdefault(work_id, {"versions": [], "current": None})
    # a new version supersedes the current one
    prev = work["current"]
    vnum = len(work["versions"]) + 1
    sha = hashlib.sha256(
        json.dumps([r["id"] for r in records], ensure_ascii=False).encode("utf-8")).hexdigest()[:16]
    entry = {
        "version": f"v{vnum}",
        "sha256": sha,
        "committed_by": committed_by,
        "committed_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "supersedes": prev,
        "n_records": len(records),
        "n_verses": n_verses,
    }
    # immutable: if an identical sha already exists, do NOT duplicate
    if any(v["sha256"] == sha for v in work["versions"]):
        return {"duplicate": True, "work_id": work_id, "version": work["current"], "sha256": sha}
    work["versions"].append(entry)
    work["current"] = f"v{vnum}"
    reg["works"][work_id] = work
    _save(reg)
    return {"work_id": work_id, "version": f"v{vnum}", "sha256": sha,
            "supersedes": prev, "n_records": len(records)}


def mark_reviewed(work_id: str, version: str, reviewed_by: str) -> dict:
    """Mark a specific L0 version as reviewed (a real review event, not code)."""
    reg = _load()
    work = reg["works"].get(work_id, {})
    for v in work.get("versions", []):
        if v["version"] == version:
            v["status"] = "REVIEWED"
            v["reviewed_by"] = reviewed_by
            v["reviewed_at"] = datetime.now(timezone.utc).isoformat()
            break
    else:
        return {"error": f"version {version} not found for {work_id}"}
    reg["works"][work_id] = work
    _save(reg)
    return {"work_id": work_id, "version": version, "status": "REVIEWED"}


def summary() -> dict:
    """A compact view: per work, current L0 version + count + status."""
    reg = _load()
    out = {}
    for wid, w in reg["works"].items():
        out[wid] = {"current": w["current"],
                    "n_versions": len(w["versions"]),
                    "versions": [v["version"] for v in w["versions"]]}
    return out


if __name__ == "__main__":
    import sys
    print(json.dumps(summary(), indent=2))
