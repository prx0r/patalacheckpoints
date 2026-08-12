#!/usr/bin/env python3
"""emit_gold_fixtures.py — wrap the gold-argument dicts into CP0 BenchmarkFixtures + validate.

Mechanical (Build 1 + 3): takes the hand-constructed gold dicts (gold.py ARG-001, gold002.py
ARG-002, and any future ARG-00N added to the GOLDS registry) and:
  1. wraps each into the BenchmarkFixture envelope (wrap_fixture)
  2. validates each for internal consistency (validate_gold)
  3. writes benchmarks/v0/structure/PAT-STRUCT-00N.json
  4. reports the pass/fail

Run: cd research && . .venv/bin/activate && python experiments/emit_gold_fixtures.py
"""
from __future__ import annotations
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.gold import build_gold_v0
from patala_ml.gold002 import build_gold_002
from patala_ml.goldutil import wrap_fixture, validate_gold, validate_all_gold

OUT = "/root/projects/patala/benchmarks/v0/structure"

# the registry of gold builders — ADD future ARG-00N here
GOLDS = {
    "ARG-GOLD-001": build_gold_v0,
    "ARG-GOLD-002": build_gold_002,
}


def main():
    ok_all = True
    for gold_id, builder in GOLDS.items():
        gold = builder()
        # 1. validate the gold is internally consistent FIRST
        v = validate_gold(gold)
        # 2. wrap into a fixture
        fx = wrap_fixture(gold)
        fname = f"PAT-STRUCT-{gold_id.split('-')[-1]}.json"
        fpath = os.path.join(OUT, fname)
        json.dump(fx, open(fpath, "w"), indent=2, ensure_ascii=False)
        status = "✅" if v["ok"] else "❌"
        print(f"{status} {gold_id} ({fname}) — nodes={v['n_nodes']} inferences={v['n_inferences']}")
        if not v["ok"]:
            ok_all = False
            for p in v["problems"]:
                print(f"    - {p}")

    # 3. validate ALL fixtures in the dir (including any pre-existing)
    print("\n=== validate_all_gold (every PAT-STRUCT-*.json in the structure dir) ===")
    allr = validate_all_gold()
    for fname, r in allr.items():
        print(f"  {'✅' if r['ok'] else '❌'} {fname} — {r['n_nodes']} nodes, {r['n_inferences']} inferences")
        if not r["ok"]:
            ok_all = False
            for p in r["problems"]:
                print(f"      - {p}")

    print(f"\n{'ALL GOLD CONSISTENT ✅' if ok_all else 'SOME GOLD INCONSISTENT ❌ — fix before extraction'}")
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
