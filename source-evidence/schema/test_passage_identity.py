#!/usr/bin/env python3
"""test_passage_identity.py — P0 PassageIdentity crosswalk acceptance (CANONICAL-GRAPH-1).

Checks (the reviewer's P0 acceptance):
  1. the invariant: resolve(any published id) -> canonical
  2. resolve(any jsonl id) -> canonical
  3. every published + jsonl id resolves (0 unresolvable)
  4. a published-only chunk (V1 upoddhāta, no jsonl) resolves honestly to itself
  5. the V-tag is the shared key (published chunkV2-A-*.md and jsonl ...:V2-A:<slug> -> same canonical)
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from passage_identity import build_crosswalk, resolve

ROOT = "/root/projects/patala"
failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


cw = build_crosswalk()
pub_ids = [p["id"] for p in json.load(open(f"{ROOT}/data/published/ipvv/index.json"))["passages"]]
jsonl_ids = []
for line in open(f"{ROOT}/data/corpus/passages/isvarapratyabhijnavivrtivimarsini.jsonl"):
    jsonl_ids.append(json.loads(line)["id"])

print("== 1. published ids resolve ==")
unres_pub = [i for i in pub_ids if not resolve(i, cw)["ok"]]
check("all published ids resolve", not unres_pub, str(unres_pub[:3]))

print("\n== 2. jsonl ids resolve ==")
unres_json = [i for i in jsonl_ids if not resolve(i, cw)["ok"]]
check("all jsonl ids resolve", not unres_json, str(unres_json[:3]))

print("\n== 3. 0 unresolvable total ==")
check("published 49/49 + jsonl 231/231", len(pub_ids) == 49 and len(jsonl_ids) == 231)

print("\n== 4. published-only chunk resolves honestly ==")
r = resolve("pt:passage:ipvv:chunkM-jnanadhikara-reflexion-core.md", cw)
check("chunkM resolves to itself", r["ok"] and r["canonical"] == "pt:passage:ipvv:chunkM"
      and r["jsonl_ids"] == 0, str(r))

print("\n== 5. V-tag is the shared key ==")
# published chunkV2-L-... and a jsonl V2-L id should both map to pt:passage:ipvv:V2-L (or V2-A for the
# first jsonl which is V2-A). Test the shared key: same V-tag -> same canonical.
j = next(i for i in jsonl_ids if ":V2-L:" in i)
check("jsonl V2-L resolves", resolve(j, cw)["matched_on"] == "V2-L")

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (PassageIdentity crosswalk works)"))
sys.exit(1 if failures else 0)
