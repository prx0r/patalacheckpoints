#!/usr/bin/env python3
"""inspect_l200_detector_nat.py — PĀṬALA-L200-DETECTOR-NAT v0.1 (future NAT task, harness only).

The second L200 NAT claim (per Agent 0 review). Distinct from L200-CHECKER-NAT:

  L200-CHECKER-NAT   (inspect_l200_nat.py)
    input:   proposal + independently adjudicated reference
    SUT:     check_dim
    claim:   does the deterministic checker correctly APPLY the adjudicated reference?

  L200-DETECTOR-NAT  (THIS file)
    input:   L0/L1/L2 + proposal (NO reference)
    SUT:     a semantic detector/model
    claim:   can the system INDEPENDENTLY identify MT/IA/open-item defects WITHOUT being
             handed the answer? This requires an actual semantic detector (not check_dim),
             which does not exist yet. Hence: HARNESS ONLY.

This file is intentionally empty (no SUT yet) and MUST NOT be run as a result until a semantic
detector exists and a natural corpus is collected + independently adjudicated. It exists to make
the claim boundary explicit and to reserve the schema.
"""
from __future__ import annotations

import hashlib
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

BENCH = "PĀṬALA-L200-DETECTOR-NAT"
VERSION = "v0.1"
PINNED_INSPECT = "inspect-ai==0.3.258"

NAT_DIR = os.path.join(os.path.dirname(__file__), "nat", "l200-detector")


def main() -> int:
    print(f"{BENCH} {VERSION}: HARNESS ONLY — no semantic detector SUT exists yet.")
    print(f"  corpus dir: {NAT_DIR}")
    print("  This is NOT a runnable result. Build the independent semantic detector, collect")
    print("  natural L0/L1/L2 + proposal candidates, adjudicate independently, then implement.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
