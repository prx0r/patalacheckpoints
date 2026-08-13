#!/usr/bin/env python3
"""pipeline/object_registry.py — generic per-layer immutable object registry.

The canonical state for the autonomy architecture (hermespatalalayers.md): registry = truth,
queue = work, run log = history. Each layer has its own immutable/versioned registry. Objects
are keyed by stable object_id + input_hash; commits are append-only; a fix emits a NEW version
that supersedes the prior (old objects stay historically available).

Per-layer records carry the three states (GENERATED / ENGINEERING_VALIDATED / SPECIALIST_REVIEWED)
so research, staging and publication can use the same graph without lying about authority.

Registries live under data/corpus/registries/<layer>-registry.jsonl (append-only).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/root/projects/patala")
REG_DIR = ROOT / "data/corpus/registries"

# The canonical layers in derivational order (the DAG spine).
LAYERS = ["SOURCE", "T1", "ARGMAP", "L0", "L1L2", "L1", "L2", "L200", "C1", "THEME", "ARGUMENT", "SYNTHESIS", "ESSAY", "EDUCATION"]

# Layer prerequisites (all must be committed before this layer is eligible).
PREREQS: dict[str, list[str]] = {
    "T1": ["SOURCE"],
    "ARGMAP": ["T1"],      # the lateral guide: reconstruct the argument from the transliteral floor
    "L0": ["T1"],
    "L1L2": ["L0"],
    "L1": ["L0"],
    "L2": ["L1", "ARGMAP"],
    "L200": ["L2"],
    "C1": ["L200"],
    "THEME": ["C1"],
    "ARGUMENT": ["C1"],
    "SYNTHESIS": ["ARGUMENT", "THEME"],
    "ESSAY": ["SYNTHESIS"],
    "EDUCATION": ["ESSAY"],
}

# Three-state ladder.
GENERATED = "GENERATED"
ENGINEERING_VALIDATED = "ENGINEERING_VALIDATED"
SPECIALIST_REVIEWED = "SPECIALIST_REVIEWED"
STATES = [GENERATED, ENGINEERING_VALIDATED, SPECIALIST_REVIEWED]


def _path(layer: str) -> Path:
    layer = layer.upper()
    return REG_DIR / f"{layer.lower()}-registry.jsonl"


def _load(layer: str) -> dict:
    p = _path(layer)
    reg = {"layer": layer.upper(), "objects": {}}
    if not p.exists():
        return reg
    for line in p.open(encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except Exception:
            continue
        oid = rec.get("object_id")
        if oid:
            reg["objects"].setdefault(oid, []).append(rec)
    return reg


def _save(layer: str, reg: dict) -> None:
    REG_DIR.mkdir(parents=True, exist_ok=True)
    with open(_path(layer), "w", encoding="utf-8") as fh:
        for oid, versions in reg["objects"].items():
            for v in versions:
                fh.write(json.dumps(v, ensure_ascii=False) + "\n")


def input_hash(obj) -> str:
    """A stable input hash for an object (by stable id fields)."""
    canonical = json.dumps(obj, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def versions(layer: str, object_id: str) -> list[dict]:
    return _load(layer)["objects"].get(object_id, [])


def current(layer: str, object_id: str) -> dict | None:
    vs = versions(layer, object_id)
    for v in reversed(vs):
        if not v.get("superseded"):
            return v
    return vs[-1] if vs else None


def is_committed(layer: str, object_id: str, input_hash_val: str) -> bool:
    """F1 idempotency: an acceptable committed output exists for this input (never dedup by
    byte-identical model output — dedup by input hash + committed status)."""
    for v in versions(layer, object_id):
        if v.get("input_hash") == input_hash_val and not v.get("superseded") \
           and v.get("status") in (GENERATED, ENGINEERING_VALIDATED, SPECIALIST_REVIEWED):
            return True
    return False


def commit(layer: str, object_id: str, input_hash_val: str, created_by: str,
           status: str = GENERATED, payload: dict | None = None,
           input_refs: list[str] | None = None) -> dict:
    """Commit a new immutable version. A fix emits a NEW version (never edit in place)."""
    reg = _load(layer)
    vs = reg["objects"].get(object_id, [])
    prev = None
    for v in vs:
        if not v.get("superseded"):
            prev = v["version"]
    vnum = len(vs) + 1
    version = f"{layer.lower()}-{object_id}-v{vnum}"
    rec = {
        "layer": layer.upper(),
        "object_id": object_id,
        "version": version,
        "input_hash": input_hash_val,
        "input_refs": input_refs or [],
        "status": status,
        "created_by": created_by,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "supersedes": prev,
        "superseded": False,
        "payload": payload or {},
        "review_events": [],
    }
    vs.append(rec)
    reg["objects"][object_id] = vs
    _save(layer, reg)
    return rec


def set_status(layer: str, object_id: str, version: str, status: str, actor: str) -> dict:
    """Move a committed version to a higher state on the ladder (VALIDATED / REVIEWED)."""
    reg = _load(layer)
    for v in reg["objects"].get(object_id, []):
        if v["version"] == version:
            v["status"] = status
            v[f"{status}_by"] = actor
            v[f"{status}_at"] = datetime.now(timezone.utc).isoformat()
            break
    else:
        return {"error": f"{version} not found in {layer}"}
    _save(layer, reg)
    return {"layer": layer, "object_id": object_id, "version": version, "status": status}


def supersede(layer: str, object_id: str) -> list[dict]:
    """Mark the current version stale (an upstream input changed). Old versions stay citable."""
    reg = _load(layer)
    changed = []
    for v in reg["objects"].get(object_id, []):
        if not v.get("superseded"):
            v["superseded"] = True
            v["superseded_at"] = datetime.now(timezone.utc).isoformat()
            changed.append(v["version"])
    _save(layer, reg)
    return changed


def objects_at_status(layer: str, status: str) -> list[dict]:
    return [v for v in _load(layer)["objects"].values()
            for v in v if v.get("status") == status and not v.get("superseded")]


def summary() -> dict:
    out = {}
    for layer in LAYERS:
        reg = _load(layer)
        out[layer] = {"objects": len(reg["objects"]),
                      "versions": sum(len(v) for v in reg["objects"].values())}
    return out


if __name__ == "__main__":
    import sys
    print(json.dumps(summary(), indent=2))
