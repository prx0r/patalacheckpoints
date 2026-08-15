#!/usr/bin/env python3
"""products/collation/test.py — collation proof (Saktumiva's witness->variant process).
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/products/collation/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))

from products.collation.engine import collate  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("COLLATION — proof (witness -> variant apparatus)\n")
    w = {
        "W1": "kālī tu bhairavārūḍhā śivaprasādaghaṭī",
        "W2": "kālīṃ tu bhairavārūḍhā śivaprasādaghaṭī",   # kālī -> kālīṃ
        "W3": "kālī eva bhairavārūḍhā śivaprasādaghaṭī",   # tu -> eva
    }
    r = collate(w, base_siglum="W1")
    gate("base is W1", r["base"] == "W1", r["base"])
    gate("all witnesses counted", len(r["witnesses"]) == 3, str([x["siglum"] for x in r["witnesses"]]))
    gate("variants detected", r["variant_loci"] >= 2, f"{r['variant_loci']} variant loci")

    # the specific variants (W2 kālīṃ, W3 eva)
    by_locus = {v["locus"]: v for v in r["apparatus"]}
    reads = {l: {x["siglum"]: x["reading"] for x in v["variants"]} for l, v in by_locus.items()}
    # W2 differs from W1 at locus 0 (kālī vs kālīṃ)
    gate("W2 variant detected", any("W2" in v and v["W2"] == "kālīṃ" for v in reads.values()),
         "kālī -> kālīṃ (W2)")
    # W3 differs at the tu/eva locus
    gate("W3 variant detected", any("W3" in v and v["W3"] == "eva" for v in reads.values()),
         "tu -> eva (W3)")

    # base siglum must exist
    try:
        collate(w, base_siglum="W9")
        gate("unknown base rejected", False, "should raise")
    except KeyError:
        gate("unknown base rejected", True, "raises on bad siglum")

    gate("MACHINE_PROPOSED honesty", "MACHINE_PROPOSED" in r["note"], "collation surfaces, editor decides")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
