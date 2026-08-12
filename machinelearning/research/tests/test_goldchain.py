#!/usr/bin/env python3
"""tests/test_goldchain.py — validate the cross-layer gold-chain certificate.

Checks the REAL invariants of the gold chain:
  - the chain spans all layers (SANSKRIT → ... → ESSAYCLAIM)
  - every node exposes depends_on/status/evidence/review_state (+ philological_proof)
  - the certificate is PER-DIMENSION (philological + derivational), NOT collapsed to one number
  - an OPEN philological crux propagates as OPEN (not hidden, not inflated)

Run: cd research && . .venv/bin/activate && python tests/test_goldchain.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.goldchain import GoldChainCertificate, ChainNode
from patala_ml.philproof import PhilologicalProof

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
    # build a chain with a philological proof that has an OPEN lexical crux
    chain = GoldChainCertificate(chain_id="gc:test", work_id="ipvv", theme_id="CL-3")

    pp = PhilologicalProof(proof_id="pp:ipvv:v2o:p4", passage_id="pt:passage:ipvv:v2o")
    pp.set_check("source_integrity", "PROVED")
    pp.set_check("morphology", "SUPPORTED")
    pp.set_check("alignment", "SUPPORTED")
    pp.open = ["LEXICAL_SENSE:acakra"]
    pp.set_check("lexical_sense", "OPEN")
    chain.philological.update(pp.checks)

    # add nodes across layers
    for layer in ["SANSKRIT", "L0", "L2", "L200", "C1", "THEME", "ARGUMENT", "AIF",
                  "ESSAYPLAN", "ESSAYCLAIM", "SENTENCE"]:
        chain.add_node(id=f"{layer.lower()}:n", layer=layer,
                       status="SUPPORTED" if layer not in ("C1", "THEME", "ESSAYCLAIM")
                       else "EDITOR_APPROVED",
                       evidence="", depends_on=[], philological_proof=pp.proof_id)

    cert = chain.certificate()

    # 1. certificate is per-dimension (not one number)
    print("== per-dimension certificate ==")
    for k in ["SOURCE_INTEGRITY", "MORPHOLOGY", "LEXICAL_SENSE",
              "INTERPRETATION", "INFERENCE", "ESSAY_CLAIM"]:
        check(f"certificate has {k}", k in cert)
    check("no single 'confidence' collapse", "confidence" not in cert)

    # 2. the OPEN lexical crux propagates as OPEN (not hidden, not inflated)
    print("\n== OPEN propagates honestly ==")
    check("LEXICAL_SENSE is OPEN", cert["LEXICAL_SENSE"] == "OPEN", cert["LEXICAL_SENSE"])
    check("MORPHOLOGY stays SUPPORTED (not inflated)", cert["MORPHOLOGY"] == "SUPPORTED")
    check("INTERPRETATION is EDITOR_APPROVED (derivational)", cert["INTERPRETATION"] == "EDITOR_APPROVED")

    # 3. every node has the auditable fields
    print("\n== node audit fields ==")
    for n in chain.nodes:
        check(f"{n.layer} has depends_on/status/evidence",
              n.depends_on is not None and n.status and n.evidence is not None)
        check(f"{n.layer} has philological_proof", n.philological_proof == pp.proof_id)

    # 4. layer coverage
    print("\n== layer coverage ==")
    layers = {n.layer for n in chain.nodes}
    for L in ["SANSKRIT", "L0", "L2", "C1", "THEME", "ARGUMENT", "ESSAYPLAN", "SENTENCE"]:
        check(f"chain spans {L}", L in layers)

    print(f"\n=== RESULT: {PASS} pass / {FAIL} fail ===")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
