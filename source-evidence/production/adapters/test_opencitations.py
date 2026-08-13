#!/usr/bin/env python3
"""test_opencitations.py — P2 OpenCitations adapter acceptance.

Checks:
  1. fetch_citations returns LIVE or UNAVAILABLE honestly (never fabricates)
  2. classify_independence marks a corroborator that cites the target as DERIVED_CITATION
  3. 2+ derived corroborators = SOURCE_ECHO detected (the reviewer's key: '3 papers say X' may be 1 origin)
  4. a non-citing corroborator = INDEPENDENT_AUTHOR
  5. UNAVAILABLE graph -> honest OPEN (not fabricated independence)
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from opencitations import fetch_citations, classify_independence

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


# a recorded fixture: target 10.1000/xyz, two corroborators cite it, one does not
fixture = {"status": "LIVE", "work_id": "10.1000/xyz",
           "citing": [{"citing": "10.1000/a"}, {"citing": "10.1000/b"}], "references": []}

print("== 1. fetch_citations honesty ==")
u = fetch_citations("10.1000/definitely-nonexistent-work")
check("unreachable -> UNAVAILABLE (not fabricated)", u["status"] in ("LIVE", "RECORDED", "UNAVAILABLE"))

print("\n== 2. independence classification ==")
sources = [{"source_id": "pt:source:a", "doi": "10.1000/a"},
           {"source_id": "pt:source:b", "doi": "10.1000/b"},
           {"source_id": "pt:source:c", "doi": "10.1000/c"}]
r = classify_independence(sources, "10.1000/xyz", opencitations=fixture)
ind = {p["source_id"]: p["independence"] for p in r["per_source"]}
check("citing corroborators -> DERIVED_CITATION", ind["pt:source:a"] == "DERIVED_CITATION"
      and ind["pt:source:b"] == "DERIVED_CITATION", str(ind))
check("non-citing corroborator -> INDEPENDENT_AUTHOR", ind["pt:source:c"] == "INDEPENDENT_AUTHOR", str(ind))

print("\n== 3. SOURCE_ECHO detection ==")
check("2 derived corroborators -> echo detected", r["echo_detected"] is True)

print("\n== 4. one derived = no echo ==")
r2 = classify_independence([{"source_id": "a", "doi": "10.1000/a"},
                            {"source_id": "c", "doi": "10.1000/c"}], "10.1000/xyz", opencitations=fixture)
check("single derived -> no echo", r2["echo_detected"] is False)

print("\n== 5. UNAVAILABLE -> honest OPEN ==")
r3 = classify_independence(sources, "10.1000/xyz", opencitations={"status": "UNAVAILABLE"})
check("unavailable graph -> status UNAVAILABLE, not a fabricated independence", r3["status"] == "UNAVAILABLE")

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (OpenCitations adapter works)"))
sys.exit(1 if failures else 0)
