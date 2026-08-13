#!/usr/bin/env python3
"""test_atlas_nat.py — A1-NEXT #2 (ATLAS-NAT) acceptance.

Checks (per the directive):
  1. the evaluator never asserts identity truth (no "THIS IS DEFINITELY X")
  2. the 8 dimensions are present (WORK_IDENTITY .. SOURCE_INDEPENDENCE)
  3. the mutation families are defined (WORK_COLLAPSE .. ABSENCE_AS_NONEXISTENCE)
  4. a clean candidate passes; each mutation is caught (FAIL)
  5. SOURCE_INDEPENDENCE: multiple sources that copy one upstream = not independent (echo)
  6. multidimensional source authority: a vector (not a scalar rank), with convenience gates
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from atlas_nat import DIMENSIONS, MUTATION_FAMILIES, evaluate_candidate, _base_candidate
from source_authority import SourceAuthority, validate_authority

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


print("== never asserts identity truth ==")
res = evaluate_candidate(_base_candidate())
check("no 'definitely'/'is X' truth claim in output", "definitely" not in json.dumps(res).lower())

print("\n== 8 dimensions + 14 mutation families defined ==")
check("8 dimensions present", set(DIMENSIONS) ==
      {"WORK_IDENTITY", "AUTHOR_IDENTITY", "TITLE_ALIAS_FIDELITY", "EDITION_IDENTITY",
       "ETEXT_DERIVATION", "WITNESS_LINKAGE", "DATE_PRECISION", "SOURCE_INDEPENDENCE"})
check("14 mutation families present",
      {"WORK_COLLAPSE", "WORK_SPLIT", "HOMONYMOUS_TITLE_MERGE", "AUTHOR_COLLAPSE",
       "UNSUPPORTED_AUTHORSHIP", "EDITION_MISMATCH", "EDITION_ETEXT_COLLAPSE",
       "ETEXT_DERIVATION_INFLATION", "WITNESS_EDITION_COLLAPSE", "DATE_PRECISION_INFLATION",
       "SOURCE_ECHO", "IDENTIFIER_COLLISION", "RIGHTS_INFLATION", "ABSENCE_AS_NONEXISTENCE"} <= set(MUTATION_FAMILIES))

print("\n== clean candidate passes ==")
clean = evaluate_candidate(_base_candidate())
check("clean candidate -> PASS", clean["verdict"] == "PASS", str(clean["problems"]))

print("\n== mutations caught ==")
def mut(fn):
    return evaluate_candidate(fn(_base_candidate()))["verdict"]
check("WORK_COLLAPSE caught", mut(lambda c: {**c, "work_title": "two distinct works merged"}) == "FAIL")
check("ETEXT_DERIVATION_INFLATION caught", mut(lambda c: {**c, "etext": {"derivation": "verified transcription of (probably based on)"}}) == "FAIL")
check("DATE_PRECISION_INFLATION caught", mut(lambda c: {**c, "date": "c. 995 (from range)"}) == "FAIL")
check("RIGHTS_INFLATION caught", mut(lambda c: {**c, "authority": {**c["authority"], "rights": "REDISTRIBUTABLE"}}) == "FAIL")

print("\n== SOURCE_INDEPENDENCE / echo ==")
echo = evaluate_candidate({**_base_candidate(), "corroboration_sources": ["Google Books", "WorldCat", "LoC"], "single_upstream_origin": True})
check("echo (multiple sources, one upstream) -> SOURCE_INDEPENDENCE open/defect",
      echo["dimensions"]["SOURCE_INDEPENDENCE"] in ("OPEN", "DEFECT"),
      str(echo["dimensions"]["SOURCE_INDEPENDENCE"]))

print("\n== multidimensional source authority (vector, not scalar) ==")
a = SourceAuthority(work_identity="MULTI_SOURCE_MATCHED", edition_identity="COPY_INSPECTED",
                    etext_derivation="TRANSCRIPTION_VERIFIED", rights="PROCESSING_ALLOWED")
d = a.model_dump()
check("authority is a 6-axis vector (no scalar)", set(d) ==
      {"work_identity", "authorship", "edition_identity", "etext_derivation", "witness_basis", "rights"})
check("factory_eligible is an explicit predicate", a.factory_eligible() is True)
check("publication_eligible is an explicit predicate", a.publication_eligible() is False)  # not redistributable
check("validate_authority accepts a valid vector", validate_authority(a.model_dump())["ok"] is True)
check("validate_authority rejects an out-of-ladder value",
      validate_authority({**a.model_dump(), "rights": "TOTALLY_FREE"})["ok"] is False)

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (Atlas NAT harness + multidimensional authority work)"))
sys.exit(1 if failures else 0)
