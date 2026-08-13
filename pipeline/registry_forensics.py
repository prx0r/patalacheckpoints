#!/usr/bin/env python3
"""pipeline/registry_forensics.py — REGISTRY-FORENSICS-v1 (CANONICAL-GRAPH-1 P1).

The audit found 789 bad_parent_hashes + 119 conflicts + 31 duplicates. The reviewer's directive: do
NOT run an indiscriminate repair script. CLASSIFY first, then fix by class.

This produces the categorized report (per class + counts), with an explicit
fix-by-class recommendation. It NEVER mutates the registry — it's a forensic classifier.

Classes (the reviewer's set):
    STALE_AFTER_REGENERATION   a downstream object's upstream was rebuilt/superseded but it wasn't
                               regenerated (e.g. L0 exists but its T1 was superseded)
    MISSING_PARENT             the upstream was never committed for this object (e.g. T1 with no SOURCE)
    LEGACY_PRE_VERSIONING      pre-versioning records (input_hash='hash1' style placeholders)
    WRONG_HASH_COMPUTATION     current input_hash doesn't match the committed upstream (parent-hash-mismatch)
    MALFORMED                  unparseable / missing required fields
    GENUINELY_CORRUPT          unexplainable (needs manual review)
    CONFLICT_SAME_ID           duplicates (same object_id, >1 current version)
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, "/root/projects/patala/pipeline")
import object_registry as R  # noqa: E402
from factory_certificate import _bad_parents, _conflicts  # noqa: E402


def classify_bad_parent(b: str) -> tuple[str, str]:
    """Classify one bad-parent string into (class, layer)."""
    layer = b.split(":")[0]
    oid = b.split(" ", 1)[0].split(":", 1)[1] if " " in b else ""
    if "missing upstream T1" in b:
        # A1 correction: check whether the T1 exists (superseded) or never existed
        # (orphaned L0). This distinguishes stale-after-regeneration from missing-historical-object.
        t1_versions = R.versions("T1", oid)
        if t1_versions:
            return "STALE_AFTER_REGENERATION", layer  # T1 exists (superseded) but L0 not regenerated
        return "MISSING_HISTORICAL_OBJECT", layer     # L0 orphaned: no T1 was ever produced
    if "missing upstream SOURCE" in b:
        return "MISSING_PARENT", layer
    if "missing upstream" in b:
        return "MISSING_PARENT", layer
    if "hash-mismatch" in b:
        return "WRONG_HASH_COMPUTATION", layer
    return "GENUINELY_CORRUPT", layer


def classify_conflict(c: str) -> str:
    layer = c.split(":")[0]
    if "parent-hash-mismatch" in c:
        return "WRONG_HASH_COMPUTATION"
    return "CONFLICT_SAME_ID"


def legacy_placeholder_count() -> int:
    """Count records whose input_hash looks like a pre-versioning placeholder ('hash1')."""
    n = 0
    for layer in R.LAYERS:
        reg = R._load(layer)
        for oid, versions in reg["objects"].items():
            for v in versions:
                if str(v.get("input_hash", "")) in ("hash1", "", "hash") or \
                   str(v.get("input_hash", "")).startswith("hash"):
                    n += 1
    return n


def run() -> dict:
    bad = _bad_parents()
    conf = _conflicts()

    # duplicates: >1 current (non-superseded) version per (object_id)
    dups = 0
    for layer in R.LAYERS:
        reg = R._load(layer)
        for oid, versions in reg["objects"].items():
            cur = [v for v in versions if not v.get("superseded")]
            if len(cur) > 1:
                dups += 1

    bad_class = Counter(classify_bad_parent(b)[0] for b in bad)
    bad_layer = Counter(classify_bad_parent(b)[1] for b in bad)
    conf_class = Counter(classify_conflict(c) for c in conf)
    legacy = legacy_placeholder_count()

    report = {
        "bench": "REGISTRY-FORENSICS-v1",
        "bad_parent_hashes": {
            "total": len(bad),
            "by_class": dict(bad_class),
            "by_layer": dict(bad_layer),
            "fix_by_class": {
                "MISSING_HISTORICAL_OBJECT": "orphaned L0 with no T1 ever produced — regenerate T1 from SOURCE, or quarantine the orphan L0",
                "STALE_AFTER_REGENERATION": "regenerate the affected L0/ARGMAP from the current T1 (targeted rebuild), or supersede the orphan",
                "MISSING_PARENT": "register/restore the missing SOURCE parent, or quarantine the orphan T1",
                "WRONG_HASH_COMPUTATION": "correct the input_hash to match the committed upstream version",
                "GENUINELY_CORRUPT": "manual review (unexplained — investigate before touching)",
            },
        },
        "registry_conflicts": {
            "total": len(conf),
            "by_class": dict(conf_class),
            "fix_by_class": {
                "WRONG_HASH_COMPUTATION": "recompute the current version's input_hash from its actual upstream",
                "CONFLICT_SAME_ID": "adjudicate the duplicate current versions; keep one canonical",
            },
        },
        "duplicates": {"total": dups},
        "legacy_pre_versioning_records": {"total": legacy,
                                           "note": "input_hash placeholders ('hash1'); pre-versioning"},
        "reads_only": True,
    }
    return report


if __name__ == "__main__":
    r = run()
    print(f"{r['bench']}:")
    print(f"  bad_parent_hashes: {r['bad_parent_hashes']['total']}")
    for k, v in r["bad_parent_hashes"]["by_class"].items():
        print(f"    {k}: {v}")
    print(f"  registry_conflicts: {r['registry_conflicts']['total']}")
    for k, v in r["registry_conflicts"]["by_class"].items():
        print(f"    {k}: {v}")
    print(f"  duplicates: {r['duplicates']['total']}")
    print(f"  legacy pre-versioning placeholder records: {r['legacy_pre_versioning_records']['total']}")
    print("  (read-only forensic report — no registry was mutated)")
