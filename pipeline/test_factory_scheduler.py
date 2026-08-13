#!/usr/bin/env python3
"""pipeline/test_factory_scheduler.py — deterministic tests for the DAG scheduler + canonical DAG (A2-ARCH-HARDEN).

A2-13a (DAG scheduling): enumerates ALL eligible (object,layer) jobs across the graph.
A2-13b (free-draining): deterministic L0 runs free.
A2-ARCH-HARDEN (canonical DAG): eligibility derives from contracts/CANONICAL-DAG.yaml (multi-parent):
  - ARGMAP requires [SOURCE, L0]
  - L2 requires [L0, ARGMAP]
  - no L2 eligibility without L0 + ARGMAP; no ARGMAP eligibility without L0 + SOURCE
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

    print("=== A2-ARCH-HARDEN canonical DAG + A2-13a/b scheduling ===")
    # A: SOURCE only (T1 eligible). B: SOURCE+T1 (L0 eligible; ARGMAP NOT yet — needs L0).
    R.commit("SOURCE", "A:v1", "Ah1", created_by="test", payload={"verse": "śivo", "source_text": "śivo"})
    R.commit("SOURCE", "B:v1", "Bh1", created_by="test", payload={"verse": "śivaṃ", "source_text": "śivaṃ"})
    R.commit("T1", "B:v1", "Bh1", created_by="test",
             payload={"t1": {"tokens": [{"sanskrit": "śivaṃ", "gloss": "x"}], "source_text": "śivaṃ"}})

    # eligibility check (A2-ARCH-HARDEN): ARGMAP needs L0 (not just T1); L2 needs L0+ARGMAP
    ok &= t("ARGMAP NOT eligible for B (no L0 yet — canonical DAG)",
            "ARGMAP" not in [j["layer"] for j in FS._eligible_jobs(["B"], ["ARGMAP"])])
    ok &= t("L0 eligible for B (L0 requires T1, committed)",
            "L0" in [j["layer"] for j in FS._eligible_jobs(["B"], ["L0"])])
    ok &= t("L2 NOT eligible for B (no L0 + ARGMAP — canonical multi-parent)",
            "L2" not in [j["layer"] for j in FS._eligible_jobs(["B"], ["L2"])])
    ok &= t("T1 eligible for A", "T1" in [j["layer"] for j in FS._eligible_jobs(["A"], ["T1"])])

    # full pass: A:T1 (model) + B:L0 (free) commit; ARGMAP for B still blocked (no L0 yet at pass time)
    r = FS.scheduler_pass(["A", "B"], ["T1", "ARGMAP", "L0", "L2", "L200", "C1"],
                          per_layer=2, max_model_calls=2)
    ok &= t("T1 A:v1 committed", R.current("T1", "A:v1") is not None)
    ok &= t("L0 B:v1 committed (free-draining deterministic)", R.current("L0", "B:v1") is not None)
    ok &= t("ARGMAP B:v1 still NOT committed (was blocked: no L0 at eligibility time)",
            R.current("ARGMAP", "B:v1") is None)

    # once L0 IS committed for B, ARGMAP becomes eligible (canonical: needs SOURCE + L0)
    ok &= t("ARGMAP eligible for B once L0 committed",
            "ARGMAP" in [j["layer"] for j in FS._eligible_jobs(["B"], ["ARGMAP"])])

    # downstream: L2 requires L0 AND ARGMAP — only eligible when both committed
    R.commit("ARGMAP", "B:v1", "Bh1", created_by="test",
             payload={"argument_map": {"what_is_at_issue": "q", "argument_steps": ["s1"],
                                       "open_items": [], "decision_for_l2": "d"}})
    ok &= t("L2 eligible for B once L0 + ARGMAP committed (multi-parent)",
            "L2" in [j["layer"] for j in FS._eligible_jobs(["B"], ["L2"])])

    print("\n" + ("FACTORY-SCHEDULER(CANONICAL-DAG) ALL PASS" if ok else "SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
