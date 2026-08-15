#!/usr/bin/env python3
"""products/scholar_identity/test.py — scholar-identity proof.
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/products/scholar_identity/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))

from products.scholar_identity.engine import register, authorize, verify_orcid, SCOPES, run_demo  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("SCHOLAR IDENTITY — proof\n")
    ident = register("0000-0000-0000-0000", "Scholar X", ["translation", "argument"])
    gate("identity registered", ident["scholar_id"].startswith("PT-scholar:"), ident["scholar_id"])
    gate("public key generated", bool(ident["public_key"]), "Ed25519 public key present")

    ident = verify_orcid(ident)
    gate("orcid-verified", ident["status"] == "ORCID_VERIFIED", ident["status"])

    ok = authorize(ident, "translation")
    deny = authorize(ident, "timeline")
    gate("authorized in scope", ok["allowed"], "translation")
    gate("denied out of scope", not deny["allowed"], deny.get("reason", ""))

    gate("closed scope set", "translation" in SCOPES and "all" in SCOPES, f"{len(SCOPES)} scopes")

    demo = run_demo()
    gate("attestation bound to identity verifies", demo["attestation"]["verified"],
         f"Ed25519 {demo['key_alg']}")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
