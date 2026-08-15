"""products/passage_workbench/engine.py — Passage Workbench (disagreement recording).

The vision's philology primitive (vision-15 / vision-14, PRODUCTS-VISIONS #3): a Sanskritist disagrees
with a reading/sandhi/translation and RECORDS it as a structured GraphProposal, which then enters the
durable review gate (propose -> approve/reject). "AI proposes, scholar adjudicates" — but here the
SCHOLAR is the one proposing a correction to a passage, and it must survive the same review gate.

What it provides (deterministic, CPU-only):
  - disagree(passage_ref, claim, kind, rationale, evidence) -> a ReviewProposal (PROPOSED)
  - approve_proposal(id, drop_missing) -> durable APPROVED (only if cited refs resolve)
  - reject_proposal(id) -> durable REJECTED
  - list_disagreements() -> the open/decided proposals

This composes: the passage product (resolve the passage) + the durable review gate (scholar_review/gate.py).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(_ROOT / "pipeline"))

from products.scholar_review.gate import ReviewGate, DeadRefError  # noqa: E402
from products.passage.engine import make_query  # noqa: E402

DISAGREEMENT_KINDS = {
    "sandhi_resolution", "reading_variant", "translation_fidelity",
    "morphology", "scope", "attribution", "edition_choice",
}


def _resolve_passage(ref: str) -> dict | None:
    q = make_query()
    p = q.get(ref)
    return p


class PassageWorkbench:
    def __init__(self):
        self.passages = make_query()
        # the gate resolves cited refs against the REAL passages (dead-ref check is meaningful)
        self.gate = ReviewGate(resolver=lambda ref: self.passages.resolve(ref) is not None)

    def disagree(self, passage_ref: str, claim: str, kind: str = "reading_variant",
                 rationale: str = "", evidence_refs: list[str] | None = None) -> dict:
        """A scholar records a disagreement with a passage -> a PROPOSED review.

        The proposal cites the passage (resolves) + any evidence. It does NOT change canonical state.
        """
        if kind not in DISAGREEMENT_KINDS:
            raise ValueError(f"unknown disagreement kind {kind}; use one of {sorted(DISAGREEMENT_KINDS)}")
        p = self.passages.get(passage_ref)
        if not p:
            raise KeyError(f"passage {passage_ref} not found")
        # the cited refs include the passage itself + evidence; the dead-ref check applies
        cited = [p["immutable_id"]] + (evidence_refs or [])
        return self.gate.propose(p["immutable_id"], "REVISE", claim, "scholar",
                                 cited_refs=cited)

    def approve(self, proposal_id: str, drop_missing: bool = False) -> dict:
        """Approve a disagreement proposal -> durable (blocked if cited refs don't resolve)."""
        return self.gate.approve(proposal_id, drop_missing=drop_missing)

    def reject(self, proposal_id: str) -> dict:
        return self.gate.reject(proposal_id)

    def list_disagreements(self) -> dict:
        return {
            "open": [p.stem for p in self.gate.proposed_dir.glob("*.json")],
            "approved": [p.stem for p in self.gate.approved_dir.glob("*.json")],
            "rejected": [p.stem for p in self.gate.rejected_dir.glob("*.json")],
            "kinds": sorted(DISAGREEMENT_KINDS),
        }


def run_demo() -> dict:
    """A controlled demo on a REAL passage: record a disagreement, then approve it."""
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        wb = PassageWorkbench()
        wb.gate = ReviewGate(Path(td), resolver=lambda ref: wb.passages.resolve(ref) is not None)
        prop = wb.disagree("chunkD", "the sandhi should resolve to ātmā not ātman here",
                          kind="sandhi_resolution", rationale="preferred reading",
                          evidence_refs=["pt:pid:ipvv:80f9c7f414ed"])
        # the cited passage immutable resolves (it's the target), so approval works
        approved = wb.approve(prop["proposal_id"])
        return {"proposal": prop, "approved": approved, "state": wb.list_disagreements()}


if __name__ == "__main__":
    import sys as _s
    verb = _s.argv[1] if len(_s.argv) > 1 else "demo"
    wb = PassageWorkbench()
    try:
        if verb == "disagree":
            res = wb.disagree(_s.argv[2], _s.argv[3], _s.argv[4] if len(_s.argv) > 4 else "reading_variant",
                              _s.argv[5] if len(_s.argv) > 5 else "")
        elif verb == "approve":
            res = wb.approve(_s.argv[2])
        elif verb == "reject":
            res = wb.reject(_s.argv[2])
        elif verb == "list":
            res = wb.list_disagreements()
        elif verb == "demo":
            res = run_demo()
        else:
            res = {"error": f"unknown verb {verb}"}
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        _s.exit(1)
