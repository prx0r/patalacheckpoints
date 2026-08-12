#!/usr/bin/env python3
"""test_vertical.py — validation of the vertical-object serializer (the CP4 gate #3 demo)."""
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.gold import build_gold_v0, V2O_PROOF_ID
from patala_ml.vertical import build_vertical, load_l0, resolve_terms, extract_sanskrit, norm

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)

print("== term matching primitives ==")
check("norm strips diacritics", norm("pratibhā") == "pratibha", norm("pratibhā"))
check("extract_sanskrit from fragment", extract_sanskrit("[and]-the-pratibhā (pratibhā)") == "pratibhā")

print("\n== L0 loading ==")
recs = load_l0("chunkV2-O-saptamo-vimarsa")
check("L0 records load for V2-O", len(recs) > 0, f"n={len(recs)}")
anchors = resolve_terms(recs, ["pratibhā", "akrama"])
check("'pratibhā' resolves to L0 anchors", len(anchors["pratibhā"]) > 0)
check("'akrama' resolves (via compound akramānantacidrūpaḥ)", len(anchors["akrama"]) > 0)
check("anchors carry source_span + sanskrit",
      all(a.get("source_span") and a.get("sanskrit") for a in anchors["pratibhā"][:1]))

print("\n== the vertical object resolves all the way down ==")
gold = build_gold_v0()
v = build_vertical(gold, "G-TC2", ["pratibhā", "rūṣitā", "akrama"], "pilot_V2O_L2_read.md", V2O_PROOF_ID)
for arrow in ["passage", "c1", "l2", "l0_anchor", "source_span", "sanskrit"]:
    check(f"arrow resolved: {arrow}", arrow in v["resolved_arrows"], v["unresolved_arrows"])
check("proposition carried through", v["proposition"]["proposition_id"] == "G-TC2")
check("G-TC2 used by an inference (G-INF1)", any(i["inference_id"] == "G-INF1" for i in v["inferences_using_proposition"]))
check("sanskrit spans extracted", len(v["sanskrit_spans"]) > 0)
check("C1 excerpt present", bool(v["c1"]["excerpt"]))
check("L2 excerpt present", bool(v["l2"]["excerpt"]))
check("philological_proof attached (proof_id)", v["philological_proof"]["proof_id"] == V2O_PROOF_ID)

print(f"\n=== RESULT: {len(failures)} fail ===")
sys.exit(1 if failures else 0)
