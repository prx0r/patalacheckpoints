#!/usr/bin/env python3
"""pipeline/test_object_events.py — deterministic tests for the append-only ObjectEvent ledger.

A2-ARCH-HARDEN #8-10: the ObjectEvent ledger is genuinely APPEND-ONLY + hash-chained (unlike the
versioned registry which rewrites its JSONL). Verifies:
  - commit/set_status/supersede each append a hash-chained event
  - the chain verifies intact (no silent rewrite)
  - tampering with a prior event breaks the chain verification
Run: python3 pipeline/test_object_events.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def main() -> int:
    ok = True
    R.REG_DIR = Path(tempfile.mkdtemp())
    R.EVENT_LOG = None

    print("=== A2-ARCH-HARDEN: append-only hash-chained ObjectEvent ledger ===")
    # commit -> OBJECT_CREATED event
    R.commit("T1", "work:v1", "h1", created_by="test", payload={"t1": {"tokens": []}})
    # set_status -> STATUS_CHANGED event
    c = R.current("T1", "work:v1")
    R.set_status("T1", "work:v1", c["version"], R.ENGINEERING_VALIDATED, "test")
    # supersede -> SUPERSEDED event
    R.supersede("T1", "work:v1")

    p = R._event_log_path()
    lines = [l for l in p.read_text().splitlines() if l.strip()]
    ok &= t("ledger has 3 events (created + status + superseded)", len(lines) == 3, f"{len(lines)}")
    ok &= t("events are hash-chained (prev_hash links)", all(
        json.loads(l)["prev_hash"] != "genesis" for l in lines[1:]))
    ok &= t("event chain verifies intact", R.verify_event_chain() is True)

    # tamper: rewrite the 2nd event's payload -> chain must break
    recs = [json.loads(l) for l in lines]
    recs[1]["event"] = {"type": "STATUS_CHANGED", "layer": "T1", "object_id": "work:v1",
                        "version": "v1", "status": "HACKED", "actor": "attacker"}
    p.write_text("\n".join(json.dumps(r) for r in recs) + "\n", encoding="utf-8")
    ok &= t("tampering with a prior event breaks the chain verification",
            R.verify_event_chain() is False)

    print("\n" + ("OBJECT-EVENTS ALL PASS" if ok else "OBJECT-EVENTS SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
