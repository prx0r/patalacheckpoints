#!/usr/bin/env python3
"""products/passage_workbench/test.py — Passage Workbench proof on REAL passages.
Run: cd patala && python3 pipeline/products/passage_workbench/test.py
"""
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))

from products.passage_workbench.engine import PassageWorkbench, DISAGREEMENT_KINDS  # noqa: E402
from products.scholar_review.gate import ReviewGate  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("PASSAGE WORKBENCH — proof on REAL passages\n")
    with tempfile.TemporaryDirectory() as td:
        wb = PassageWorkbench()
        wb.gate = ReviewGate(Path(td), resolver=lambda ref: wb.passages.resolve(ref) is not None)

        prop = wb.disagree("chunkD", "sandhi should resolve to ātmā here",
                           kind="sandhi_resolution", rationale="preferred reading",
                           evidence_refs=["pt:pid:ipvv:80f9c7f414ed"])
        gate("disagreement proposed on real passage", prop["state"] == "PROPOSED",
             f"{prop['proposal_id']} target={prop['target_ref']}")
        gate("target is a real immutable", prop["target_ref"].startswith("pt:pid:ipvv:"),
             prop["target_ref"])

        approved = wb.approve(prop["proposal_id"])
        gate("approve succeeds (cited passage resolves)", approved["state"] == "APPROVED",
             "the real passage is not a dead ref")

        # a proposal citing a GHOST ref must be blocked
        bad = wb.disagree("chunkD", "x", kind="reading_variant",
                          evidence_refs=["pt:pid:ipvv:GHOST"])
        from products.scholar_review.gate import DeadRefError
        try:
            wb.approve(bad["proposal_id"])
            gate("dead-ref blocks approval", False, "should raise DeadRefError")
        except DeadRefError:
            gate("dead-ref blocks approval", True, "ghost citation blocked")

        gate("disagreement kinds closed", "sandhi_resolution" in DISAGREEMENT_KINDS,
             f"{len(DISAGREEMENT_KINDS)} kinds")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
