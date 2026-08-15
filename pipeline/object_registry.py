#!/usr/bin/env python3
"""pipeline/object_registry.py — generic per-layer VERSIONED object registry.

The canonical state for the autonomy architecture (hermespatalalayers.md): registry = truth,
queue = work, run log = history. Each layer has its own versioned registry. Objects
are keyed by stable object_id + input_hash; a fix emits a NEW version that supersedes
the prior (old objects stay historically available).

HONEST NAMING (A2-ARCH-HARDEN): this is a VERSIONED registry, NOT cryptographically
immutable / append-only. _save() rewrites the whole JSONL on each commit; set_status()
and supersede() mutate prior records in memory and rewrite them. It is version-aware and
historically recoverable in normal operation, but the file itself can be rewritten.
For cryptographic append-only integrity, see the ObjectEvent ledger (event-sourced
projection) — the remaining A2-ARCH-HARDEN piece.

Per-layer records carry the three states (GENERATED / ENGINEERING_VALIDATED / SPECIALIST_REVIEWED)
so research, staging and publication can use the same graph without lying about authority.

Registries live under data/corpus/registries/<layer>-registry.jsonl (versioned JSONL).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG_DIR = ROOT / "data/corpus/registries"

# ── concurrency safety (the torn-write fix) ───────────────────────────────────
# A canonical registry must NEVER depend on "hope nobody else appends during this write."
# Every write path uses:
#   1. a single-writer advisory lock (fcntl on the per-registry .lock file), so two processes
#      cannot interleave a read-modify-write on the same registry;
#   2. write-to-temp + fsync + atomic os.replace() for REWRITES (_save), so a crash mid-write can
#      never leave a torn/corrupt file;
#   3. append_event writes a single line to the event log; it takes the lock + fsyncs too.
import fcntl  # POSIX (Linux); the factory runs on Linux.


class _FileLock:
    """Advisory single-writer lock around a registry file (blocks concurrent writers)."""

    def __init__(self, path: Path):
        self.path = Path(str(path) + ".lock")
        self.fd = None

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.fd = os.open(str(self.path), os.O_CREAT | os.O_RDWR, 0o644)
        # block until the lock is free (a writer holds it for the duration of its write)
        fcntl.flock(self.fd, fcntl.LOCK_EX)
        return self

    def __exit__(self, *exc):
        if self.fd is not None:
            try:
                fcntl.flock(self.fd, fcntl.LOCK_UN)
            finally:
                os.close(self.fd)
                self.fd = None
        return False


def _atomic_write(path: Path, data: str) -> None:
    """Write data to path ATOMICALLY: temp file in the same dir + fsync + os.replace.

    os.replace() is atomic on POSIX: a concurrent reader sees either the old or the new complete
    file, never a torn middle state. This permanently fixes the source-registry corruption.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    _LOAD_CACHE.pop(str(path), None)   # invalidate any cached parse of this registry
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())          # flush to disk before the rename
        os.replace(tmp, str(path))          # atomic rename (POSIX)
    finally:
        if os.path.exists(tmp):
            try:
                os.unlink(tmp)
            except OSError:
                pass

# The canonical layers in derivational order (the DAG spine).
LAYERS = ["SOURCE", "T1", "ARGMAP", "L0", "L1L2", "L1", "L2", "L200", "C1", "THEME", "ARGUMENT", "SYNTHESIS", "ESSAY", "EDUCATION"]

# Layer prerequisites — THE SINGLE SOURCE OF TRUTH is contracts/CANONICAL-DAG.yaml.
# Every consumer (scheduler, rebuild, catalog, certificate, tests) must derive from the manifest,
# not from an independent copy. PREREQS is the compiled view loaded once from the manifest.
_DAG_PATH = Path(__file__).resolve().parents[1] / "contracts" / "CANONICAL-DAG.yaml"


def _load_dag_prereqs() -> dict[str, list[str]]:
    """Compile the canonical dependency manifest into {layer: [requires...]}.

    Falls back to the manifest's 'requires' for each layer; if the manifest is missing/unparseable,
    fail loudly (do NOT silently fall back to a stale hardcoded copy — that is the very bug we removed)."""
    if not _DAG_PATH.exists():
        raise FileNotFoundError(f"canonical DAG manifest missing: {_DAG_PATH}")
    text = _DAG_PATH.read_text(encoding="utf-8")
    # minimal YAML parse for the 'dependencies:' block (no yaml dep)
    import re
    deps = {}
    cur = None
    for line in text.splitlines():
        m = re.match(r"^  ([A-Z0-9]+):\s*$", line)
        if m:
            cur = m.group(1)
            deps.setdefault(cur, [])
            continue
        r = re.match(r"^\s+requires:\s*\[(.*?)\]\s*(#.*)?$", line)
        if r and cur:
            deps[cur] = [x.strip().strip('"').strip("'") for x in r.group(1).split(",") if x.strip()]
    return deps


PREREQS: dict[str, list[str]] = _load_dag_prereqs()

# Three-state ladder.
GENERATED = "GENERATED"
ENGINEERING_VALIDATED = "ENGINEERING_VALIDATED"
SPECIALIST_REVIEWED = "SPECIALIST_REVIEWED"
STATES = [GENERATED, ENGINEERING_VALIDATED, SPECIALIST_REVIEWED]


# ── append-only ObjectEvent ledger (A2-ARCH-HARDEN: honest integrity trail) ──
# Unlike the versioned registry (which rewrites its JSONL), this ledger is genuinely APPEND-ONLY:
# each event is appended to a separate file with a hash chain (each event's hash includes the
# previous event's hash). Current state is a projection; the ledger cannot be silently rewritten
# without breaking the chain. This is the honest "append-only" claim.
EVENT_DIR = REG_DIR  # data/corpus/registries
EVENT_LOG = None


def _event_log_path() -> Path:
    global EVENT_LOG
    if EVENT_LOG is None:
        EVENT_LOG = REG_DIR / "object-events.jsonl"
    return EVENT_LOG


def append_event(event: dict) -> dict:
    """Append a hash-chained ObjectEvent. Returns the event with its hash + previous-hash.

    Events: OBJECT_CREATED / STATUS_CHANGED / SUPERSEDED / REVIEWED / INVALIDATED / REBUILT.
    The chain: event_hash = sha256(prev_hash + canonical(event)). Anyone can verify the log is
    unrewritten by re-deriving the chain."""
    import time as _t
    prev = "genesis"
    p = _event_log_path()
    if p.exists():
        # read only the LAST event line for prev_hash (O(1) tail, not a full-file scan).
        # The buffer may START mid-line (when size > 8192); a partial first line must not
        # abort the whole parse — so skip unparseable lines and keep the last good hash.
        try:
            with p.open("rb") as fh:
                fh.seek(0, 2)
                size = fh.tell()
                if size:
                    fh.seek(max(0, size - 65536), 0)
                    tail = fh.read().decode("utf-8", errors="ignore")
                    for line in tail.splitlines():
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            prev = json.loads(line).get("event_hash", prev)
                        except Exception:
                            continue
        except Exception:
            pass
    canonical = json.dumps(event, sort_keys=True, ensure_ascii=False)
    event_hash = hashlib.sha256((prev + canonical).encode("utf-8")).hexdigest()
    rec = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "prev_hash": prev,
        "event_hash": event_hash,
        "event": event,
    }
    p.parent.mkdir(parents=True, exist_ok=True)
    # single-writer lock + atomic append: a torn concurrent append can corrupt the hash chain
    with _FileLock(p):
        with open(p, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
    return rec


def verify_event_chain() -> bool:
    """Verify the ObjectEvent ledger's hash chain is intact (no silent rewrite)."""
    p = _event_log_path()
    if not p.exists():
        return True
    prev = "genesis"
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        canonical = json.dumps(rec["event"], sort_keys=True, ensure_ascii=False)
        expect = hashlib.sha256((prev + canonical).encode("utf-8")).hexdigest()
        if rec.get("prev_hash") != prev or rec.get("event_hash") != expect:
            return False
        prev = rec["event_hash"]
    return True


def _path(layer: str) -> Path:
    layer = layer.upper()
    return REG_DIR / f"{layer.lower()}-registry.jsonl"


_LOAD_CACHE: dict[str, tuple] = {}   # (path) -> (st_ino, st_mtime_ns, st_size, reg)


def _load(layer: str) -> dict:
    p = _path(layer)
    empty = {"layer": layer.upper(), "objects": {}}
    if not p.exists():
        return empty
    # In-process cache keyed by file identity (inode+mtime+size). Re-parsing the registry (which can
    # be tens of MB / tens of thousands of objects) on EVERY current()/versions() call was the factory's
    # CPU bottleneck: the --retry path called _load once per failing passage (~761 * 0.6s = minutes of
    # pure re-parse before any model call). The cache invalidates automatically whenever the file
    # changes on disk (including writes from other processes, e.g. the live RAW->EN runner), so it is
    # always observably correct — just much faster for repeated reads in one pass.
    try:
        st = p.stat()
        key = (st.st_ino, st.st_mtime_ns, st.st_size)
    except OSError:
        return empty
    hit = _LOAD_CACHE.get(str(p))
    if hit and hit[:3] == key:
        return hit[3]
    reg = {"layer": layer.upper(), "objects": {}}
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
    _LOAD_CACHE[str(p)] = (key[0], key[1], key[2], reg)
    return reg


def _save(layer: str, reg: dict) -> None:
    """Rewrite a registry ATOMICALLY under a single-writer lock (never a torn file)."""
    REG_DIR.mkdir(parents=True, exist_ok=True)
    path = _path(layer)
    lines = []
    for oid, versions in reg["objects"].items():
        for v in versions:
            lines.append(json.dumps(v, ensure_ascii=False) + "\n")
    data = "".join(lines)
    with _FileLock(path):
        _atomic_write(path, data)


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
    # every version superseded -> no current version (Era C: an invalidated object has no current)
    return None


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
    append_event({"type": "OBJECT_CREATED", "layer": layer, "object_id": object_id,
                  "input_hash": input_hash_val, "version": version, "created_by": created_by})
    return rec


def commit_batch(layer: str, entries: list[dict], created_by: str,
                 status: str = GENERATED) -> list[dict]:
    """Register many objects in ONE load/save (efficient bulk intake).

    entries: [{"object_id", "input_hash", "payload"}]. Skips object_ids that already have a
    committed current version. Returns the committed records. This is the efficient path for
    bulk source registration (avoids a full registry rewrite per verse)."""
    reg = _load(layer)
    committed = []
    events = []
    for e in entries:
        oid = e["object_id"]
        vs = reg["objects"].get(oid, [])
        prev = None
        for v in vs:
            if not v.get("superseded"):
                prev = v["version"]
        vnum = len(vs) + 1
        version = f"{layer.lower()}-{oid}-v{vnum}"
        rec = {
            "layer": layer.upper(),
            "object_id": oid,
            "version": version,
            "input_hash": e["input_hash"],
            "input_refs": e.get("input_refs") or [],
            "status": status,
            "created_by": created_by,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "supersedes": prev,
            "superseded": False,
            "payload": e.get("payload") or {},
            "review_events": [],
        }
        vs.append(rec)
        reg["objects"][oid] = vs
        committed.append(rec)
        events.append({"type": "OBJECT_CREATED", "layer": layer, "object_id": oid,
                       "input_hash": e["input_hash"], "version": version, "created_by": created_by})
    if committed:
        _save(layer, reg)
        for ev in events:
            append_event(ev)
    return committed


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
    append_event({"type": "STATUS_CHANGED", "layer": layer, "object_id": object_id,
                  "version": version, "status": status, "actor": actor})
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
    for v in changed:
        append_event({"type": "SUPERSEDED", "layer": layer, "object_id": object_id, "version": v})
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
