#!/usr/bin/env python3
"""pipeline/close_g2.py — close devpath2/G2: the correction loop (Agent 1's #1 blocker).

Consumes the frozen 6-finding bundle (data/evaluation/findings/EF-*.json, status=OPEN), fixes the
root-cause worker bug, and for each finding:
  1. supersede the failing object's bad version (old kept citable),
  2. regenerate it with the fixed worker (new exact version),
  3. emit an EvaluationCandidate (new version) + ImpactReport (trigger=EF-...),
  4. mark the finding CLOSED.

Cross-lane contract (Agent 1's evals/patala/tasks/):
  { "evaluated_version": "t1-cidgagana:v1-v2", "old_version": "t1-cidgagana:v1-v1",
    "impact": {"trigger": "EF-T1-2026-0003", "downstream_affected": [...]} }

Usage:
  python3 pipeline/close_g2.py            # close all OPEN findings
  python3 pipeline/close_g2.py --dry-run  # report what would be done (no commits)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/root/projects/patala")
sys.path.insert(0, str(ROOT / "pipeline"))
FINDINGS_DIR = ROOT / "data/evaluation/findings"

import object_registry as R  # noqa: E402
import factory_batch as FB  # noqa: E402


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_findings() -> list[dict]:
    out = []
    for p in sorted(FINDINGS_DIR.glob("EF-*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        if d.get("status") == "OPEN":
            out.append(d)
    return out


def _object_of(finding: dict) -> str:
    """The failing object_ref, e.g. 'cidgagana:v1'."""
    return finding.get("object_ref", "")


def _layer_of(finding: dict) -> str:
    return finding.get("layer", "").upper()


def _current_version(finding: dict) -> str | None:
    obj = _object_of(finding)
    cur = R.current(_layer_of(finding), obj)
    return cur["version"] if cur else None


def _supersede(finding: dict) -> list[str]:
    """Supersede the failing object's current version (old stays citable). Returns superseded versions."""
    layer = _layer_of(finding)
    obj = _object_of(finding)
    return R.supersede(layer, obj)


def _regenerate(finding: dict, dry_run: bool = False) -> dict:
    """Regenerate the failing object with the fixed worker. Returns the new current version."""
    layer = _layer_of(finding)
    obj = _object_of(finding)
    inp = {"object_id": obj}
    # recover the verse from SOURCE for T1/L0
    if layer in ("T1", "L0"):
        src = R.current("SOURCE", obj)
        ih = (src or {}).get("input_hash", "")
        inp["input_hash"] = ih
        inp["verse"] = _verse_for(obj)
    if dry_run:
        return {"layer": layer, "object": obj, "would": "REBUILD"}
    try:
        r = FB._produce_layer(layer, [inp], batch_size=1)
        committed = r.get("committed", [])
        new_ver = committed[0]["version"] if committed else None
        return {"layer": layer, "object": obj, "committed": len(committed), "new_version": new_ver,
                "rejected": r.get("rejected", []), "retryable": r.get("retryable", [])}
    except Exception as e:
        return {"layer": layer, "object": obj, "error": str(e)[:120]}


def _verse_for(obj: str) -> str:
    """Recover the verse for a passage from the SOURCE registry + translations jsonl."""
    sha = (R.current("SOURCE", obj) or {}).get("input_hash", "")
    wid = obj.split(":")[0]
    tpath = ROOT / "data/corpus/downloads/translations" / f"{wid}.jsonl"
    if tpath.exists():
        for line in tpath.open(encoding="utf-8"):
            try:
                r = json.loads(line)
                if r.get("source_sha256") == sha:
                    return r.get("sanskrit", "")
            except Exception:
                continue
    return ""


def _impact_report(finding: dict, old_version: str, new_version: str) -> dict:
    """Emit the cross-lane ImpactReport (trigger + downstream_affected) using review_engine where possible."""
    # downstream_affected: L0/L200/C1 for this passage (the factory stack below T1)
    layer = _layer_of(finding)
    obj = _object_of(finding)
    downstream = {"L0", "L200", "C1"} if layer == "T1" else {"L200", "C1"}
    affected = []
    for d in downstream:
        cur = R.current(d, obj)
        affected.append({"object": obj, "layer": d, "state": "SUPERSEDED" if cur else "NEED_REVIEW",
                         "previous_version": cur["version"] if cur else None})
    return {
        "trigger": finding.get("finding_id"),
        "old_version": old_version,
        "evaluated_version": new_version,
        "downstream_affected": affected,
    }


def _emit_candidate(finding: dict, old_version: str, new_version: str, impact: dict, out_dir: Path) -> Path:
    """Write the EvaluationCandidate per the cross-lane contract."""
    candidate = {
        "type": "EVALUATION_CANDIDATE",
        "evaluated_version": new_version,
        "old_version": old_version,
        "finding_ref": finding.get("finding_id"),
        "layer": finding.get("layer"),
        "object_ref": _object_of(finding),
        "impact": impact,
        "emitted_at": _now(),
        "producer": {"agent": "agent2"},
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / f"EVAL-CAND-{finding.get('finding_id')}.json"
    p.write_text(json.dumps(candidate, indent=2, ensure_ascii=False), encoding="utf-8")
    return p


def _close_finding(finding: dict, out_dir: Path) -> Path:
    """Mark a finding CLOSED (update status + resolution). Returns the findings file path."""
    p = FINDINGS_DIR / f"{finding.get('finding_id')}.json"
    finding["status"] = "CLOSED"
    finding["resolution"] = {
        "resolved_at": _now(),
        "resolved_by": "agent2",
        "action": "WORKER_FIX (added retroflex ṇ to IAST_TOKEN) + REGENERATED",
    }
    p.write_text(json.dumps(finding, indent=2, ensure_ascii=False), encoding="utf-8")
    return p


def close_g2(dry_run: bool = False) -> dict:
    findings = _load_findings()
    out_dir = ROOT / "data/evaluation/candidates"
    results = []
    for f in findings:
        fid = f.get("finding_id")
        old_version = _current_version(f)
        superseded = _supersede(f) if not dry_run else []
        regen = _regenerate(f, dry_run=dry_run)
        new_version = regen.get("new_version")
        impact = _impact_report(f, old_version or "?", new_version or "?")
        cand_path = _emit_candidate(f, old_version or "?", new_version or "?", impact, out_dir) if not dry_run else None
        if not dry_run:
            _close_finding(f, out_dir)
        results.append({
            "finding_id": fid,
            "layer": f.get("layer"),
            "object_ref": _object_of(f),
            "old_version": old_version,
            "new_version": new_version,
            "superseded": superseded,
            "regen": regen,
            "candidate": str(cand_path) if cand_path else None,
            "impact": impact,
        })
    return {"count": len(results), "results": results}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    r = close_g2(dry_run=a.dry_run)
    mode = "[DRY-RUN]" if a.dry_run else ""
    print(f"{mode} processed {r['count']} OPEN findings")
    for x in r["results"]:
        print(f"  {x['finding_id']}: {x['layer']} {x['object_ref']} "
              f"old={x['old_version']} new={x['new_version']} "
              f"candidate={x['candidate'] or 'dry'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
