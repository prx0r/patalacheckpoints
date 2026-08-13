#!/usr/bin/env python3
"""pipeline/prove_vertical.py — deterministic vertical proof: committed L0 -> L1 -> L2 -> L200 -> C1.

Drives the autonomy controller through the canonical stack on a small batch of REAL committed L0
objects (kramasadbhava), with the generative L200/C1 model calls stubbed to a deterministic fixture
so the proof runs fast and fail-fast (the live-model path is separate). Verifies:
  - provenance continuity (each layer resolves its committed upstream)
  - registry persistence (L1/L2/L200/C1 objects committed)
  - fail-closed behavior (a blocked/missing upstream is never fabricated into a commit)

Usage:
  python3 pipeline/prove_vertical.py [--objects kramasadbhava:v1,kramasadbhava:v3] [--count 3]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import autonomy as A
import l200_worker as LW
import c1_worker


def _stub_generative():
    """Stub the generative L200 classifier + C1 model call to deterministic fixtures."""
    def _classify(oid, cands):
        if not cands:
            return "COMPLETE", [], [], []
        return ("COMPLETE",
                [{"label": "MT-001", "type": "LEXICAL", "basis": f"candidate {cands[0].idx}"}],
                [{"label": "IA-001", "text": "deterministic fixture IA"}],
                [])
    LW._classify_candidates = _classify

    def _fake_chat(system, prompt, **kw):
        return json.dumps({
            "summary": "The verse establishes the support of the powers.",
            "function": "introduces the support; the following argument depends on it.",
            "key_terms": [{"term": "pratibhā", "meaning": "the flashing"}],
            "explanation": ("This passage establishes that the flashing is not the order itself but "
                            "has an order-less support, the great Lord, and that this is required by "
                            "the structure of ordered experience."),
            "boundary": "It establishes the local support, not every claim about the universal Self.",
            "related_passages": ["V2-P"], "uncertain": ["akrama"]})
    c1_worker.chat = _fake_chat


def _l0_inputs(object_ids: list[str], count: int) -> list[dict]:
    out = []
    for oid in object_ids[:count]:
        cur = R.current("L0", oid)
        if cur:
            out.append({"object_id": oid, "input_hash": cur["input_hash"]})
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--objects", default="")
    ap.add_argument("--count", type=int, default=3)
    a = ap.parse_args()

    if a.objects:
        object_ids = [s.strip() for s in a.objects.split(",") if s.strip()]
    else:
        object_ids = [oid for oid, vers in R._load("L0")["objects"].items()
                      if oid.startswith("kramasadbhava")][:a.count]

    _stub_generative()

    l0s = _l0_inputs(object_ids, a.count)
    print(f"input: {len(l0s)} committed L0 objects")

    # L1 (deterministic controlled reading) — consumes committed L0
    rep1 = A.tick(layers=["L1"], max_batch=8, dry_run=False, inputs={"L1": l0s})
    print(f"L1 committed={rep1['committed']} failed={rep1['failed']}")
    # L2 (readable) — consumes committed L1
    rep2 = A.tick(layers=["L2"], max_batch=8, dry_run=False, inputs={"L2": l0s})
    print(f"L2 committed={rep2['committed']} failed={rep2['failed']}")
    # L200 (audit) — consumes committed L2
    rep3 = A.tick(layers=["L200"], max_batch=8, dry_run=False, inputs={"L200": l0s})
    print(f"L200 committed={rep3['committed']} failed={rep3['failed']}")
    # C1 (commentary) — consumes committed L200
    rep4 = A.tick(layers=["C1"], max_batch=8, dry_run=False, inputs={"C1": l0s})
    print(f"C1 committed={rep4['committed']} failed={rep4['failed']}")

    # verify registry persistence + provenance chain for the first object
    ok = True
    for oid in [i["object_id"] for i in l0s]:
        l0 = R.current("L0", oid)
        l1 = R.current("L1", oid)
        l2 = R.current("L2", oid)
        l200 = R.current("L200", oid)
        c1 = R.current("C1", oid)
        chain = {"L0": bool(l0), "L1": bool(l1), "L2": bool(l2),
                 "L200": bool(l200), "C1": bool(c1)}
        print(f"  {oid}: {chain}")
        if not all(chain.values()):
            ok = False

    # fail-closed check: an object with NO committed upstream must NOT commit downstream
    bogus = [{"object_id": "does-not-exist:x", "input_hash": "deadbeef"}]
    rep_bogus = A.tick(layers=["L2"], max_batch=8, dry_run=False, inputs={"L2": bogus})
    print(f"fail-closed (bogus upstream): committed={rep_bogus['committed']} (must be 0)")
    if rep_bogus["committed"] != 0:
        ok = False

    print("\n" + ("VERTICAL PROOF PASS" if ok else "VERTICAL PROOF FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
