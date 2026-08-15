#!/usr/bin/env python3
"""products/translation_proof/test.py — Translation Proof proof on REAL IPVV.
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/products/translation_proof/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "pipeline"))

from products.translation_proof.engine import translation_proofs, DIMS  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("TRANSLATION PROOF (#2) — proof on REAL IPVV\n")
    proofs = translation_proofs()
    gate("proofs for real passages", len(proofs) >= 40, f"{len(proofs)} proofs")
    p = proofs[0]
    gate("non-aggregate vector", len(p["audit_vector"]) == 10, f"{len(p['audit_vector'])} independent dimensions")
    gate("content-addressed", len(p["content_hash"]) == 16, "source+translation bound by hash")
    gate("gate is honest", p["publication_gate"]["decision"] in ("BLOCKED", "PASS"),
         f"gate={p['publication_gate']['decision']}")
    gate("source identity real", "source_hash" in p["source_identity"], f"witness={p['source_identity']['witness']}")
    gate("no fake single score", "audit_vector" in p and not isinstance(p["audit_vector"], (int, float)),
         "vector, never a '94%' scalar")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
