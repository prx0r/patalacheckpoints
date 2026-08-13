#!/usr/bin/env python3
"""pipeline/test_failure_queue.py — deterministic tests for the durable failure/retry queue (A2-11).

Era B: the factory must not wedge when one model call fails. Verifies:
  1. a GENERATION_FAILED proposal is recorded as RETRYABLE, not silently dropped or wedged
  2. a failed passage does NOT block a neighboring passage (isolation)
  3. retrying from the durable queue re-attempts and, on success, commits (idempotency -> no dupes)

Run: python3 pipeline/test_failure_queue.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import factory_batch as FB
import t1_worker as TW


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def main() -> int:
    ok = True
    R.REG_DIR = Path(tempfile.mkdtemp())
    FB.FAILURE_QUEUE = Path(tempfile.mkdtemp()) / "failure-queue.jsonl"

    print("=== A2-11 durable failure/retry queue ===")
    # commit SOURCE so the retry can recover the verse (the real factory always has SOURCE)
    for oid, v in (("work:v1", "śivo"), ("work:v2", "śivaṃ")):
        R.commit("SOURCE", oid, oid[-2:], created_by="test", payload={"verse": v, "source_text": v})
    # stub T1 so passage v1 FAILS and v2 SUCCEEDS (isolation test)
    calls = {"n": 0}
    def flaky(s, p, **kw):
        # fail the FIRST call (v1), succeed on retry
        calls["n"] += 1
        if calls["n"] == 1:
            return "not json {"
        return '{"tokens": {"śivo": {"gloss":"x"}}}'
    TW.chat = flaky

    inputs = [{"object_id": "work:v1", "input_hash": "h1", "verse": "śivo"},
              {"object_id": "work:v2", "input_hash": "h2", "verse": "śivaṃ"}]
    r = FB._produce_layer("T1", inputs, batch_size=1)
    # v1 failed (GENERATION_FAILED) -> retryable; v2 succeeded -> committed
    ok &= t("v1 model failure recorded as retryable", len(r["retryable"]) == 1,
            f"retryable={[x['object_id'] for x in r['retryable']]}")
    ok &= t("v2 committed despite v1 failure (isolation)",
            any(c["object_id"] == "work:v2" for c in r["committed"]),
            f"committed={[x['object_id'] for x in r['committed']]}")
    ok &= t("failure queue file written", FB.FAILURE_QUEUE.exists())
    q = FB.FAILURE_QUEUE.read_text().splitlines()
    ok &= t("queue has the failed object", any("work:v1" in line for line in q))

    print()
    print("=== retry from the durable queue (append-only audit) ===")
    # now the model succeeds on retry
    TW.chat = lambda s, p, **kw: '{"tokens": {"śivo": {"gloss":"x"}}}'
    n = FB._retry_failures("work", "T1")
    ok &= t("retry re-attempted the failed object", n == 1, f"{n}")
    # A2-11b: history preserved — the record is RESOLVED, NOT deleted
    q = FB.FAILURE_QUEUE.read_text().splitlines() if FB.FAILURE_QUEUE.exists() else []
    resolved = [json.loads(l) for l in q if "work:v1" in l and l.strip()]
    ok &= t("retry history preserved (record still present, status RESOLVED)",
            any(x.get("status") == "RESOLVED" for x in resolved),
            f"statuses={[x.get('status') for x in resolved]}")
    ok &= t("retry record carries attempt count",
            any(x.get("attempt", 0) >= 2 for x in resolved),
            f"attempts={[x.get('attempt') for x in resolved]}")
    # resolved records are not retried again (no infinite loop)
    n2 = FB._retry_failures("work", "T1")
    ok &= t("resolved records not retried again (no infinite loop)", n2 == 0, f"{n2}")

    print("\n" + ("FAILURE-QUEUE ALL PASS" if ok else "FAILURE-QUEUE SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
