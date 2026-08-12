#!/usr/bin/env python3
"""test_scholarly_corroboration.py — the SCHOLARLY_CORROBORATED_PRELIMINARY promotion protocol.

Verifies the mechanical freeze (goldutil.validate_scholarly_corroboration) enforces the six rules:
PRIMARY / INDEPENDENCE / RELEVANCE / RELATION / TRACEABILITY / SCOPE. Well-formedness only.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from patala_ml.goldutil import validate_scholarly_corroboration

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


def wellformed_node():
    return {
        "proposition_id": "G4-CRYSTAL", "kind": "TEXTUAL_CLAIM",
        "scholarly_corroboration": {
            "primary": {"span_id": "chunkV2-H:...:T0", "edition_ref": "Ipk_1,5.11"},
            "scholarship": [
                {"origin": "scholar", "addresses": "manifestation without vimarśa is inert",
                 "relation": "SUPPORTS", "publication": "vimarsa dossier",
                 "passage": "IPK 1.5.11"}
            ],
            "promotes_to": "SCHOLARLY_CORROBORATED_PRELIMINARY", "level": "DOSSIER_CORROBORATED",
        },
    }


print("== a well-formed corroboration passes ==")
g = {"nodes": [wellformed_node()]}
check("valid corroboration is OK", validate_scholarly_corroboration(g)["ok"])

print("\n== each violated rule is caught ==")

# PRIMARY: no edition ref
n = wellformed_node(); n["scholarly_corroboration"]["primary"]["edition_ref"] = ""
check("missing edition address -> FAIL (PRIMARY)",
      not validate_scholarly_corroboration({"nodes": [n]})["ok"])

# INDEPENDENCE: source is the reconstruction itself
n = wellformed_node(); n["scholarly_corroboration"]["scholarship"][0]["origin"] = "patala_argument_reconstruction"
check("reconstruction-as-source -> FAIL (INDEPENDENCE)",
      not validate_scholarly_corroboration({"nodes": [n]})["ok"])

# RELEVANCE: source addresses nothing (just the term)
n = wellformed_node(); n["scholarly_corroboration"]["scholarship"][0].pop("addresses")
check("source lacks 'addresses' -> FAIL (RELEVANCE)",
      not validate_scholarly_corroboration({"nodes": [n]})["ok"])

# RELATION: invalid relation
n = wellformed_node(); n["scholarly_corroboration"]["scholarship"][0]["relation"] = "AGREES"
check("invalid relation -> FAIL (RELATION)",
      not validate_scholarly_corroboration({"nodes": [n]})["ok"])

# TRACEABILITY: no publication location (remove every page/section/passage)
n = wellformed_node()
src = n["scholarly_corroboration"]["scholarship"][0]
src["page"] = "p.1"  # give it a location first so removal tests the requirement
src.pop("page"); src.pop("section", None); src.pop("passage", None)
check("no traceability (page/section/passage) -> FAIL (TRACEABILITY)",
      not validate_scholarly_corroboration({"nodes": [n]})["ok"])

# SCOPE: full SCHOLARLY_CORROBORATED without PUBLICATION_VERIFIED
n = wellformed_node(); n["scholarly_corroboration"]["promotes_to"] = "SCHOLARLY_CORROBORATED"
n["scholarly_corroboration"]["level"] = "DOSSIER_CORROBORATED"
check("full status without PUBLICATION_VERIFIED -> FAIL (SCOPE)",
      not validate_scholarly_corroboration({"nodes": [n]})["ok"])

# SCOPE: propagation blocked structurally (a dependent node with no block must not be corroborated)
g = {"nodes": [wellformed_node(), {"proposition_id": "I4-1", "kind": "CONCLUSION"}]}
check("dependent conclusion with no corroboration block is not promoted",
      "I4-1" not in validate_scholarly_corroboration(g)["corroborated_nodes"])

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (scholarly-corroboration protocol enforced)"))
sys.exit(1 if failures else 0)
