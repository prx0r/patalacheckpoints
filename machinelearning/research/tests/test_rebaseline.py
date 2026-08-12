#!/usr/bin/env python3
"""tests/test_rebaseline.py — validate the CP2 re-baseline (frozen-suite retrieval).

Checks:
  1. the retrieval fixtures were validated + moved into benchmarks/v0/retrieval/
  2. they carry honest fields (split_class, review_state)
  3. the immutable run record has benchmark version / split / config / metrics / commit
  4. the fixtures pass the ingest gate (schema)

Run: cd research && . .venv/bin/activate && python tests/test_rebaseline.py
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PASS = 0
FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        print(f"  ✓ {name}")
        PASS += 1
    else:
        print(f"  ✗ {name} {detail}")
        FAIL += 1


def main():
    # 1. fixtures in the frozen benchmark
    print("== retrieval fixtures in frozen suite ==")
    fixtures = glob.glob("/root/projects/patala/benchmarks/v0/retrieval/*.jsonl")
    check("fixtures seeded in benchmarks/v0/retrieval/", len(fixtures) >= 1, len(fixtures))
    n = 0
    if fixtures:
        for line in open(fixtures[0]):
            if line.strip():
                d = json.loads(line)
                check("fixture has relevant passage_ids", "relevant" in d)
                check("fixture has split_class", "split_class" in d)
                check("fixture has review_state", "review_state" in d)
                n += 1
    check("fixtures are non-trivial count", n >= 10, n)

    # 2. immutable run record
    print("\n== immutable run record ==")
    runs = glob.glob("/root/projects/patala/benchmarks/v0/runs/*/metrics.json")
    # runs/ may hold runs of different task types (retrieval, extraction, ...) append-only.
    # This test validates the RETRIEVAL rebaseline run specifically (it has 'results.retrievers').
    ret_runs = [r for r in runs if "retrievers" in json.load(open(r)).get("results", {})]
    check("a retrieval run record exists", len(ret_runs) >= 1)
    if ret_runs:
        d = json.load(open(ret_runs[0]))
        for k in ["run_id", "benchmark_version", "split_policy", "config", "git_commit", "results"]:
            check(f"run has {k}", k in d)
        check("benchmark_version is v0", d.get("benchmark_version") == "v0")
        check("git_commit is a real sha", len(d.get("git_commit", "")) == 40)
        check("results has retrievers", "retrievers" in d.get("results", {}))
        if "retrievers" in d.get("results", {}):
            check("has BM25", "BM25-l2" in d["results"]["retrievers"])
            check("has hybrid", "hybrid-l2" in d["results"]["retrievers"])

    # 3. honest labeling (not claimed as gold/verified)
    print("\n== honest labeling ==")
    if fixtures:
        first = json.loads(open(fixtures[0]).readline())
        check("fixtures are CANDIDATE (not gold)", first.get("review_state") == "CANDIDATE")

    print(f"\n=== RESULT: {PASS} pass / {FAIL} fail ===")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
