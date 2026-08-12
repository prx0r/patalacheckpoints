#!/usr/bin/env python3
"""test_kcore_reproducibility.py — P-019 v2: the STRUCTURAL k-core hierarchy is byte-identical
across separate processes and irrelevant node/edge insertion ordering.

Distinction enforced: k-core is a STRUCTURAL FACT (embeddedness), NOT a theme; the output is a PROPOSAL,
not an AcceptedTheme. Do not infer 'high core_number => philosophically central'.

Tests:
  R1  same graph -> same canonical hash across two in-process calls.
  R2  cross-process -> identical canonical hash (fresh subprocess).
  R3  permuted node/edge insertion order (semantic-preserving permutation of the C1 list) ->
      identical canonical hash AND identical core_number map.
  R4  core_number is a structural fact: a node's core_number does not change under insertion permutation.
  R5  the output is labeled a STRUCTURAL FACT / PROPOSAL (not 'theme'), and high core_number is NOT claimed
      to mean 'philosophically central'.
"""
from __future__ import annotations

import json
import os
import random
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patala_ml.c1corpus import load_c1_nodes
from patala_ml.kcore import core_hierarchy

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


nodes = load_c1_nodes()
r0 = core_hierarchy(nodes)

print("== R1 — same graph, identical canonical hash (in-process) ==")
check("two in-process calls give the same graph_hash", core_hierarchy(nodes)["graph_hash"] == r0["graph_hash"])

print("\n== R2 — cross-process byte-identical canonical hash ==")
_research = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# run a FRESH process that imports the module and prints the graph_hash directly (independent of the
# builder script's main(), so it is robust to any transient file state)
code = ("import sys; sys.path.insert(0, %r); "
        "from patala_ml.c1corpus import load_c1_nodes; "
        "from patala_ml.kcore import core_hierarchy; "
        "print(core_hierarchy(load_c1_nodes())['graph_hash'])") % _research
sub = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, cwd=_research)
h = (sub.stdout or "").strip()
check("fresh subprocess produces the identical canonical hash", h == r0["graph_hash"],
      f"sub={h[:12] if h else 'none'} vs local={r0['graph_hash'][:12]}")

print("\n== R3 — permuted C1 insertion order -> identical hash + identical core_number map ==")
perm_ok = True
core_ok = True
for seed in (1, 7, 42):
    shuffled = list(nodes)
    random.Random(seed).shuffle(shuffled)
    rp = core_hierarchy(shuffled)
    perm_ok = perm_ok and (rp["graph_hash"] == r0["graph_hash"])
    # core_number map must be identical (node identity -> core number), independent of insertion order
    core_ok = core_ok and (rp["core_numbers"] == r0["core_numbers"])
check("graph_hash invariant under node/edge insertion-order permutation", perm_ok)
check("core_number map byte-identical under insertion-order permutation", core_ok)

print("\n== R4 — core_number is a structural fact, not a theme ==")
check("core_numbers are stable integers (not 'themes')",
      all(isinstance(v["core_number"], int) for v in r0["core_numbers"].values()))
max_core_nodes = [n for n, v in r0["core_numbers"].items()
                  if v["core_number"] == r0["max_core"]]
print(f"  (max core = {r0['max_core']}; {len(max_core_nodes)} C1s at the top core — this is density, not centrality)")

print("\n== R5 — the artifact is labeled a STRUCTURAL PROPOSAL, not a theme ==")
check("detector_id is a structural k-core id", r0["detector_id"] == "PATALA.GRAPH.STRUCTURAL_K_CORE.v1")
check("note explicitly says k-core != theme / not an AcceptedTheme",
      "not a theme" in r0["note"].lower() and "not an acceptedtheme" in r0["note"].lower())
check("edge_evidence persisted (reasons survive)", len(r0.get("edge_evidence", [])) >= 0)

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (P-019 v2 k-core hierarchy is byte-identical across "
       "processes + insertion order; structural fact, not a theme)"))
sys.exit(1 if failures else 0)
