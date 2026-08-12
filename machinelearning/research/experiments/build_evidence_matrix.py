#!/usr/bin/env python3
"""build_evidence_matrix.py — the proposition × evidence matrix for the 5 argument golds.

Produces the matrix that exposes WHERE evidence stops and reconstruction begins:

                 Sanskrit   L0   Scholar   Rival   Historical   Status
ARG1-G1             ✓       ✓      ?        ?          ?          ...

The point is NOT five ACCEPT/REJECT labels. It is the provenance-rich map: what the Sanskrit
establishes, what scholarship independently establishes, where reconstruction begins, and where
readings diverge. This is the core dataset behind Pāṭala Review and the T3/T4 benchmarks.

Driven from the review packet (which holds primary-Sanskrit spans + explicitness labels). A
proposition is:
  - corroborated  if it has a scholarly_corroboration block passing the protocol
  - primary-grounded if it has resolving primary spans
  - reconstructed   if explicitness is RECONSTRUCTED_NECESSARY / INTERPRETIVE_EXTENSION
  - unknown / ?      where no scholarship has been mined yet
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PACKET = os.path.join(ROOT, "benchmarks/v0/review/ARG-GOLD-REVIEW-PACKET-v2.json")

EXPLICITNESS_RECONSTRUCTED = {"RECONSTRUCTED_NECESSARY", "INTERPRETIVE_EXTENSION"}
RECONSTRUCTED_KINDS = {"CONCLUSION", "IMPLICIT_PREMISE"}


def classify(p: dict) -> dict:
    expl = p.get("explicitness", "")
    kind = p.get("kind", "")
    has_primary = bool(p.get("primary_evidence"))
    corr = p.get("scholarly_corroboration")

    state = "OPEN"
    if corr:
        state = "CORROBORATED" if corr.get("level") in ("DOSSIER_CORROBORATED", "PUBLICATION_VERIFIED") else "CORROB_PRELIM"
    elif expl in EXPLICITNESS_RECONSTRUCTED or kind in RECONSTRUCTED_KINDS:
        state = "RECONSTRUCTED"
    elif has_primary:
        state = "PRIMARY_GROUNDED"
    return {
        "id": p.get("proposition_id"), "kind": kind, "explicitness": expl,
        "primary": "✓" if has_primary else "—",
        "scholar": ("✓" if corr else "?"),
        "state": state,
    }


def main() -> int:
    with open(PACKET, encoding="utf-8") as f:
        packet = json.load(f)

    rows = []
    summary = {"primary_grounded": 0, "corroborated": 0, "reconstructed": 0, "open": 0, "total": 0}
    for arg in packet["arguments"]:
        gid = arg["gold_id"]
        for p in arg.get("propositions", []):
            c = classify(p)
            summary["total"] += 1
            summary[{"PRIMARY_GROUNDED": "primary_grounded", "CORROBORATED": "corroborated",
                     "CORROB_PRELIM": "corroborated", "RECONSTRUCTED": "reconstructed",
                     "OPEN": "open"}[c["state"]]] += 1
            rows.append([gid, c["id"], c["kind"], c["explicitness"], c["primary"], c["scholar"], c["state"]])

    print("PROPOSITION × EVIDENCE MATRIX (all 5 arguments)")
    print(f"{'Arg':9} {'Prop':10} {'Kind':22} {'Explicitness':26} {'San':3} {'Sch':4} {'State'}")
    print("-" * 90)
    for r in rows:
        print(f"{r[0]:9} {r[1]:10} {r[2]:22} {r[3]:26} {r[4]:3} {r[5]:4} {r[6]}")

    print(f"\nSUMMARY: {summary['total']} propositions = "
          f"{summary['primary_grounded']} primary-grounded · "
          f"{summary['corroborated']} corroborated · "
          f"{summary['reconstructed']} reconstructed · "
          f"{summary['open']} open")
    print("\nWHERE EVIDENCE STOPS / RECONSTRUCTION BEGINS:")
    print(f"  {summary['primary_grounded']} propositions are textually grounded but not yet scholar-corroborated")
    print(f"  {summary['reconstructed']} propositions are reconstruction (explicitness/kind) — these are the "
          f"OPEN review targets")
    print(f"  {summary['open']} propositions have no corroboration mined yet (the mining campaign target)")

    out = os.path.join(ROOT, "benchmarks/v0/review/ARG-EVIDENCE-MATRIX.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"arguments": [{  # compact serializable form
            "gold_id": a["gold_id"], "propositions": [classify(p) for p in a["propositions"]]
        } for a in packet["arguments"]], "summary": summary}, f, indent=2)
    print(f"\nmatrix written: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
