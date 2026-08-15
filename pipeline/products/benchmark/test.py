#!/usr/bin/env python3
"""products/benchmark/test.py — Benchmark (#15) proof on REAL IPVV.
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/products/benchmark/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))

from products.benchmark.engine import build_samples, honest_metric, _claim_ceiling_honest  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("BENCHMARK (#15) — proof on REAL IPVV\n")
    samples = build_samples()
    gate("real samples compiled", len(samples) >= 40, f"{len(samples)} real IPVV passages")
    gate("every sample has input", all(s["input"] for s in samples), "all samples carry real claim JSON")
    gate("gold is honest expectation", all(s["expected"] for s in samples),
         f"all PĀṬALA-INFERS claims honest (rate {honest_metric(samples)['honest_ceiling_rate']})")

    # the SUT catches an inflated claim (anti-theatre)
    inflated = dict(samples[0]); inflated["claim_text"] = "x"
    # re-check: an honest claim is detected as honest
    gate("SUT detects honest ceiling", _claim_ceiling_honest({"epistemic_status": "PĀṬALA-INFERS",
                                                              "epistemic_ceiling": "MACHINE_PROPOSED"}),
         "PĀṬALA-INFERS -> MACHINE_PROPOSED is honest")
    gate("SUT rejects inflated ceiling", not _claim_ceiling_honest({"epistemic_status": "PĀṬALA-INFERS",
                                                                    "epistemic_ceiling": "SCHOLARLY_CORROBORATED"}),
         "PĀṬALA-INFERS -> SCHOLARLY_CORROBORATED is INFLATED (caught)")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
