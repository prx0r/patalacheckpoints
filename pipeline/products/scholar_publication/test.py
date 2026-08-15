#!/usr/bin/env python3
"""products/scholar_publication/test.py — scholar-publication proof.
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/products/scholar_publication/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))

from products.scholar_publication.engine import profile_record, attestation_record, all_profiles, publish_all  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("SCHOLAR PUBLICATION — proof\n")
    ap = all_profiles()
    gate("compiled scholar index", ap["n_scholars"] >= 1, f"{ap['n_scholars']} scholars")

    # a profile record is valid JSON-LD
    pr = profile_record("Dr-Scholar")
    gate("profile is JSON-LD Person", pr["@type"] == "Person" and "@context" in pr,
         f"{pr['identifier']}")
    gate("profile has citeAs (CV-legible)", bool(pr.get("citeAs")), pr["citeAs"][:50])

    # attestation record is valid JSON-LD (synthesize a minimal one — tests the SHAPE, not ledger state)
    import products.scholar_publication.engine as E
    E._load_attestations = lambda: [{"attestation_id": "SA-TEST", "target_ref": "t:1",
                                      "reviewer": "r", "verdict": "ACCEPT",
                                      "rationale": "x", "created_at": "2026-08-15"}]
    ar = attestation_record("SA-TEST")
    gate("attestation is JSON-LD Review", ar and ar["@type"] == "Review",
         (ar or {}).get("identifier", "none"))

    # publish emits files
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        res = publish_all(Path(td))
        files = list(Path(td).glob("*.json"))
        gate("publish emits JSON files", len(files) >= 1, f"{len(files)} records emitted")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
