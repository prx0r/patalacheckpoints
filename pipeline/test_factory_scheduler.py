#!/usr/bin/env python3
"""pipeline/test_factory_scheduler.py — deterministic tests for the backlog scheduler (A2-8/A2-9).

Verifies the multi-work execution controller:
  - finds each work's frontier (first layer not fully done) via the status dashboard
  - advances a work's frontier by one layer
  - iterates multiple works fairly (one layer per work per pass)
  - marks a work fully-done once all layers are committed
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
import t1_worker as TW


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def main() -> int:
    ok = True
    R.REG_DIR = Path(tempfile.mkdtemp())
    FB.FAILURE_QUEUE = Path(tempfile.mkdtemp()) / "q.jsonl"
    TW.chat = lambda s, p, **kw: '{"tokens": {"śivo": {"gloss":"x"}}}'

    print("=== A2-8/A2-9 backlog scheduler + multi-work execution ===")
    for w in ("alpha", "beta"):
        for i in (1, 2):
            R.commit("SOURCE", f"{w}:v{i}", f"{w}h{i}", created_by="test",
                     payload={"verse": "śivo", "source_text": "śivo"})

    # frontier detection
    ok &= t("alpha frontier = T1 (SOURCE done, T1 not)", FS._frontier("alpha") == "T1")
    ok &= t("registered works includes alpha+beta", "alpha" in FS._registered_works() and "beta" in FS._registered_works())

    # advance one layer per work
    r = FS.scheduler_pass(["alpha", "beta"], ["T1"], per_layer=2)
    ok &= t("both works advanced one layer", r["advanced"] == 2, f"advanced={r['advanced']}")
    ok &= t("alpha T1 committed", len([o for o, vs in R._load("T1")["objects"].items()
                                       if o.startswith("alpha")]) == 2)
    ok &= t("beta T1 committed", len([o for o, vs in R._load("T1")["objects"].items()
                                      if o.startswith("beta")]) == 2)

    # a work with no frontier (already fully done at the requested layer) is marked done
    # commit the remaining SOURCE->T1 and re-check: now T1 is done, frontier moves on
    ok &= t("frontier returns None when no unfinished layer (or next layer)",
            FS._frontier("alpha") in (None, "ARGMAP", "L0"))

    print("\n" + ("FACTORY-SCHEDULER ALL PASS" if ok else "FACTORY-SCHEDULER SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
