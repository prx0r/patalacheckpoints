#!/usr/bin/env python3
"""pipeline/freeze_argrec_pilot.py — freeze IPVV-ARGREC-PILOT-001 (the bounded recovery experiment).

The reviewer's gate #3: do NOT launch all 48 V2L units. Run a bounded discovery experiment:
   IPVV-ARGREC-PILOT-001 — 5 contiguous units covering ONE known hard argument (the V2L apohana /
   'I'-recollection is not a construction, kārikās 1-5).

This FREEZES the inputs BEFORE inference so the run is reproducible and gold-independent:
    - source hashes (the Sanskrit chunk hashes)
    - argctx membership (the contiguous window the ARGMAP consumes)
    - worker SHA / prompt hash / model  (filled at generation time)
    - NO-GOLD-LEAKAGE guarantee: the generator may use Sanskrit/T1/L0/C1 + generic argument
      instructions, but must NOT retrieve the gold ARGMAP for ipvv:V2L.

We freeze the WINDOW that covers the known hard argument (k1-k5 = argctx:001). The frozen packet is
what Agent 2's ARGMAP run consumes and what Agent 1's blind recovery scorer later scores.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

sys.path.insert(0, "/root/projects/patala/pipeline")
import object_registry as R  # noqa: E402

OUT = "/root/projects/patala/data/evaluation/argrec-pilot-001-freeze.json"

PILOT_ID = "IPVV-ARGREC-PILOT-001"
PASSAGE = "ipvv:V2L"
# the contiguous window covering the known hard argument (apohana / I-recollection, kārikās 1-5)
ARGCTX = "ipvv:V2L:argctx:001"
WINDOW = ["ipvv:V2L:k1", "ipvv:V2L:k2", "ipvv:V2L:k3", "ipvv:V2L:k4", "ipvv:V2L:k5"]


def freeze() -> dict:
    # freeze the source hashes for the window's units
    src_hashes = {}
    for unit in WINDOW:
        cur = R.current("SOURCE", unit)
        src_hashes[unit] = {"input_hash": cur["input_hash"], "status": cur["status"]} if cur else None
    # freeze the argctx membership (the registered ArgumentContext object)
    ctx = R.current("ARGUMENT", ARGCTX)
    freeze = {
        "pilot_id": PILOT_ID,
        "passage": PASSAGE,
        "known_hard_argument": ("V2L apohana / ahaṃ-pratyavamarśa: the 'I'-recollection is NOT a "
                                "construction (vikalpa); it is the two-throwing (dvayākṣepī) self-grasp"),
        "gold_ref": "pt:passage:ipvv:V2L (independent gold — must NOT be fed to the generator)",
        "context_window": {"argctx": ARGCTX, "members": WINDOW,
                           "members_contiguous": True,
                           "membership_from_registry": bool(ctx)},
        "source_hashes": src_hashes,
        "generation_inputs": {
            "allowed": ["Sanskrit", "T1", "L0", "C1", "generic argument instructions"],
            "forbidden": ["the gold ARGMAP for ipvv:V2L (NO GOLD LEAKAGE)"],
        },
        "worker": {"sha": None, "prompt_hash": None, "model": None},  # filled at generation time
        "scoring": "ARGUMENT-RECOVERY-BENCH-v1 (blind) on the frozen gold for ipvv:V2L",
        "catastrophic_metrics": ["UNSUPPORTED_BRIDGE_RATE", "SPEAKER_COLLAPSE_RATE"],
        "frozen_at": "2026-08-13",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(freeze, f, indent=2, ensure_ascii=False)
    return freeze


if __name__ == "__main__":
    f = freeze()
    print(f"{f['pilot_id']} frozen:")
    print(f"  passage={f['passage']} window={f['context_window']['members']}")
    print(f"  argctx registered={f['context_window']['membership_from_registry']}")
    print(f"  source units with hashes: {sum(1 for v in f['source_hashes'].values() if v)}/{len(WINDOW)}")
    print(f"  wrote {OUT}")
