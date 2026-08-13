#!/usr/bin/env python3
"""pipeline/test_factory_scheduler.py — deterministic tests for the DAG-based backlog scheduler.

A2-13a (DAG scheduling): enumerates ALL eligible (object,layer) jobs across the graph (not T1-only),
ranks them, and executes within the model budget.
A2-13b (free-draining): deterministic L0 jobs run immediately WITHOUT consuming the model budget.

Verifies:
  - eligible-job enumeration across layers (not just the frontier)
  - model budget spent across the whole graph
  - deterministic L0 drains free (model_calls doesn't count it)
  - downstream advancement (T1 -> L0/ARGMAP become eligible once T1 committed)
Run: python3 pipeline/test_factory_scheduler.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import factory_batch as FB
import factory_scheduler as FS


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def _stub_model():
    import t1_worker as TW
    import argument_map_worker as AM
    TW.chat = lambda s, p, **kw: '{"tokens": {"śivo": {"gloss":"x"}, "śivaṃ": {"gloss":"y"}}}'
    AM.chat = lambda s, p, **kw: '{"what_is_at_issue":"q","argument_steps":["s1"],"open_items":[],"decision_for_l2":"d"}'


def main() -> int:
    ok = True
    R.REG_DIR = Path(tempfile.mkdtemp())
    FB.FAILURE_QUEUE = Path(tempfile.mkdtemp()) / "q.jsonl"
    _stub_model()

    print("=== A2-13a/b DAG scheduling + free-draining deterministic layers ===")
    # A: SOURCE done (T1 eligible). B: SOURCE+T1 done (L0 + ARGMAP eligible)
    R.commit("SOURCE", "A:v1", "Ah1", created_by="test", payload={"verse": "śivo", "source_text": "śivo"})
    R.commit("SOURCE", "B:v1", "Bh1", created_by="test", payload={"verse": "śivaṃ", "source_text": "śivaṃ"})
    R.commit("T1", "B:v1", "Bh1", created_by="test",
             payload={"t1": {"tokens": [{"sanskrit": "śivaṃ", "gloss": "x"}], "source_text": "śivaṃ"}})

    jobs = FS._eligible_jobs(["A", "B"], ["T1", "ARGMAP", "L0", "L2", "L200", "C1"])
    jobs_key = sorted((j["layer"], j["object_id"]) for j in jobs)
    ok &= t("DAG enumerates all eligible jobs across layers", jobs_key ==
            [("ARGMAP", "B:v1"), ("L0", "B:v1"), ("T1", "A:v1")], str(jobs_key))

    r = FS.scheduler_pass(["A", "B"], ["T1", "ARGMAP", "L0", "L2", "L200", "C1"],
                          per_layer=2, max_model_calls=2)
    ok &= t("model budget spent across the graph (2 calls: A:T1 + B:ARGMAP)",
            r["model_calls"] == 2, f"{r['model_calls']}")
    ok &= t("deterministic L0 drained free (counted separately)", r["deterministic"] == 1,
            f"{r['deterministic']}")
    ok &= t("T1 A:v1 committed", R.current("T1", "A:v1") is not None)
    ok &= t("ARGMAP B:v1 committed", R.current("ARGMAP", "B:v1") is not None)
    ok &= t("downstream unlocked: L0 eligible after T1", "L0" in
            [j["layer"] for j in FS._eligible_jobs(["B"], ["L0"])])

    print("\n" + ("FACTORY-SCHEDULER(DAG) ALL PASS" if ok else "FACTORY-SCHEDULER(DAG) SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
