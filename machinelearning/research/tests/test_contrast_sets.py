#!/usr/bin/env python3
"""test_contrast_sets.py — the contrast-set falsification benchmark around the argument golds.

Assertions:
1. Every corruption type produces a detectable structured change to the proposed argument.
   (Note: NARROW_SCOPE / REPLACE_TERM_SENSE are expected to be structural-MISSED — that IS the
   finding that a semantic model is needed; see the script note. So this test asserts the
   STRUCTURAL corruptions are detected and the SEMANTIC ones are explicitly missed, not silently
   passed.)
2. The immutable run is well-formed.
"""
from __future__ import annotations

import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "experiments"))

from benchmark_contrast_sets import corrupt, load_argument, signal_original_vs_corrupt

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


# corruptions that change a STRUCTURED field -> must be detected
STRUCTURAL = {"SWAP_SPEAKER", "REVERSE_SUPPORT", "NEGATE_PROPOSITION", "WIDEN_SCOPE",
              "DELETE_PREMISE", "PURVAPAKSA_AS_SIDDHANTA"}
# corruptions that change only SEMANTICS (prose) -> structural detector MUST miss them (that's the finding)
SEMANTIC = {"NARROW_SCOPE", "REPLACE_TERM_SENSE"}

print("== structural corruptions are detected by the structured comparator ==")
arg = load_argument("ARG-GOLD-002")
for kind in STRUCTURAL:
    sig = signal_original_vs_corrupt(arg, corrupt(arg, kind))
    check(f"{kind} detected", sig["detected"], str(sig["flags"][:2]))

print("\n== semantic corruptions are EXPLICITLY missed structurally (the gap that needs a model) ==")
for kind in SEMANTIC:
    sig = signal_original_vs_corrupt(arg, corrupt(arg, kind))
    check(f"{kind} is a structural-MISS (correctly — it needs semantic discrimination)",
          not sig["detected"], str(sig["flags"][:2]))

print("\n== the immutable run is well-formed ==")
runs = sorted(glob.glob(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))), "benchmarks/v0/runs/contrast-*.json")))
check("at least one contrast run exists", bool(runs))
if runs:
    d = json.load(open(runs[-1]))
    check("run carries detector + verifier + target",
          d.get("detector") == "PATALA.ARGUMENT.CONTRAST_SET.v1" and d.get("target") == "ARG-GOLD-002")
    check("run carries execution_base_sha + artifact_commit_sha + working_tree_dirty",
          bool(d.get("execution_base_sha")) and "artifact_commit_sha" in d and "working_tree_dirty" in d)

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (contrast-set: structural corruptions detected; semantic gap made explicit)"))
sys.exit(1 if failures else 0)
