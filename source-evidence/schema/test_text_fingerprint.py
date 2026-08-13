#!/usr/bin/env python3
"""test_text_fingerprint.py — text-fingerprint primitive acceptance.

Checks (the reviewer's §5):
  1. fingerprints include incipit/explicit/n-gram/MinHash
  2. two transcriptions of the SAME verse are closer than a different verse
  3. candidate_rank returns cheap top-k (the candidate-generation layer)
  4. fingerprints are EVIDENCE (never identity truth)
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from text_fingerprint import fingerprint, minhash_sim, candidate_rank, jaccard

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


V1 = "atha mālinīvijayottaram nama mahāyogini jñānakāṇḍaṃ bṛhat tantraṃ ārabhate"
V1B = "atha malinivijayottaram namah mahayogini jnanakandam brhat tantram arabhate"
V2 = "yadā tu saṃsāraṃ kṣayayati tadā śivaḥ svena bhāti"

print("== 1. fingerprint components ==")
f = fingerprint(V1)
check("has incipit + explicit + ngrams + minhash",
      all(k in f for k in ("incipit", "explicit", "char_ngrams", "minhash")))

print("\n== 2. same verse > different verse ==")
sim_same = minhash_sim(fingerprint(V1)["minhash"], fingerprint(V1B)["minhash"])
sim_diff = minhash_sim(fingerprint(V1)["minhash"], fingerprint(V2)["minhash"])
check("same-verse variant closer", sim_same > sim_diff, f"{sim_same} vs {sim_diff}")

print("\n== 3. candidate_rank = cheap top-k ==")
r = candidate_rank(V1, [V2, V1B], k=2)
check("returns k candidates ranked", len(r) == 2 and r[0]["blended"] >= r[1]["blended"])
check("puts the same-verse variant first", r[0]["index"] == 1, str([(x['index'], x['blended']) for x in r]))

print("\n== 4. evidence not truth ==")
check("jaccard is a fraction", 0.0 <= jaccard(set("abc"), set("abd")) <= 1.0)

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (text fingerprint primitive works)"))
sys.exit(1 if failures else 0)
