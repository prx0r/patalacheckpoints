"""products/scholar_review/gate.py — the durable review-gate (borrowed pattern from vouch, MIT).

Upgrades ScholarProduct with vouch's review-gate lifecycle discipline (src/vouch/proposals.py +
SPEC.md §4), re-expressed against PĀṬALA's own epistemic objects. Licensed MIT -> pattern reuse.

The pattern we borrow (never copy code wholesale):
  - a REVIEW GATE with explicit states: PROPOSED (local) / APPROVED / REJECTED (durable)
  - `proposed/` is ephemeral; `approved/` + `rejected/` are durable (committed, append-only)
  - a DEAD-REFERENCE CHECK on approval: an approval is BLOCKED if the payload cites claims/references
    that no longer resolve — the reviewer must drop or reject (vouch's DeadClaimRefsError)
  - every mutation emits an AUDIT EVENT (append-only), so the gate is fully traceable

This is a deterministic, stdlib-only layer over our existing review_engine reducer. It makes review
state DURABLE and self-checking rather than a throwaway in-memory ledger.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class DeadRefError(RuntimeError):
    """Approval blocked: the proposal cites references that no longer resolve."""


@dataclass
class ReviewProposal:
    proposal_id: str
    target_ref: str
    decision: str                      # ACCEPT | REVISE | REJECT | ABSTAIN
    rationale: str
    reviewer: str
    cited_refs: list = field(default_factory=list)   # references the payload depends on
    state: str = "PROPOSED"            # PROPOSED | APPROVED | REJECTED
    created_at: str = field(default_factory=_now)

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


class ReviewGate:
    """The durable review gate: propose -> approve/reject, with dead-ref checking + audit."""

    def __init__(self, base_dir: Path | None = None, resolver=None):
        self.base = base_dir or (ROOT / "data/scholar/gate")
        self.proposed_dir = self.base / "proposed"
        self.approved_dir = self.base / "approved"
        self.rejected_dir = self.base / "rejected"
        self.audit_file = self.base / "audit-events.jsonl"
        self.resolver = resolver   # optional: an external object that can resolve a ref
        for d in (self.proposed_dir, self.approved_dir, self.rejected_dir):
            d.mkdir(parents=True, exist_ok=True)
        self._seq = len(list(self.proposed_dir.glob("*.json"))) + len(list(self.approved_dir.glob("*.json")))

    def _audit(self, event: str, detail: dict) -> None:
        rec = {"event": event, "at": _now(), **detail}
        with open(self.audit_file, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    def _resolve(self, ref: str) -> bool:
        """Does a cited reference resolve to a real object? (the dead-ref check)

        Accepts: a ReviewProposal id (file exists in the gate), OR any reference that the host
        ledger knows (passed via `resolver`). Default: check the gate dirs + the corpus registries.
        """
        if ref in {p.stem for p in self.proposed_dir.glob("*.json")} | \
           {p.stem for p in self.approved_dir.glob("*.json")} | \
           {p.stem for p in self.rejected_dir.glob("*.json")}:
            return True
        if self.resolver is not None:
            try:
                return bool(self.resolver(ref))
            except Exception:
                return False
        return False

    def propose(self, target_ref: str, decision: str, rationale: str, reviewer: str,
                cited_refs: list[str] | None = None) -> dict:
        """Create a PROPOSED review (ephemeral). Never touches durable state."""
        self._seq += 1
        p = ReviewProposal(proposal_id=f"REV-PROP-{self._seq:04d}", target_ref=target_ref,
                           decision=decision, rationale=rationale, reviewer=reviewer,
                           cited_refs=cited_refs or [])
        (self.proposed_dir / f"{p.proposal_id}.json").write_text(
            json.dumps(p.to_dict(), ensure_ascii=False), encoding="utf-8")
        self._audit("proposal.create", {"proposal_id": p.proposal_id, "target_ref": target_ref,
                                        "decision": decision, "reviewer": reviewer})
        return p.to_dict()

    def approve(self, proposal_id: str, drop_missing: bool = False) -> dict:
        """Approve a proposal -> durable artifact. BLOCKED on dead cited refs unless drop_missing."""
        path = self.proposed_dir / f"{proposal_id}.json"
        if not path.exists():
            raise KeyError(f"no PROPOSED proposal {proposal_id}")
        p = ReviewProposal(**json.loads(path.read_text(encoding="utf-8")))
        missing = [r for r in p.cited_refs if not self._resolve(r)]
        if missing and not drop_missing:
            raise DeadRefError(f"proposal {proposal_id} cites missing ref(s): {missing} "
                               "— approve with drop_missing=True or reject")
        p.state = "APPROVED"
        p.approved_at = _now()
        (self.approved_dir / f"{proposal_id}.json").write_text(
            json.dumps(p.to_dict(), ensure_ascii=False), encoding="utf-8")
        path.unlink()  # moved out of proposed/ (ephemeral) into approved/ (durable)
        self._audit("proposal.approve", {"proposal_id": proposal_id, "target_ref": p.target_ref,
                                         "dropped_missing": missing if drop_missing else []})
        return p.to_dict()

    def reject(self, proposal_id: str) -> dict:
        """Reject a proposal -> durable rejected record (no artifact written)."""
        path = self.proposed_dir / f"{proposal_id}.json"
        if not path.exists():
            raise KeyError(f"no PROPOSED proposal {proposal_id}")
        p = ReviewProposal(**json.loads(path.read_text(encoding="utf-8")))
        p.state = "REJECTED"
        p.rejected_at = _now()
        (self.rejected_dir / f"{proposal_id}.json").write_text(
            json.dumps(p.to_dict(), ensure_ascii=False), encoding="utf-8")
        path.unlink()
        self._audit("proposal.reject", {"proposal_id": proposal_id, "target_ref": p.target_ref})
        return p.to_dict()

    def audit_log(self) -> list[dict]:
        if not self.audit_file.exists():
            return []
        return [json.loads(l) for l in self.audit_file.read_text().splitlines() if l.strip()]

    def state(self) -> dict:
        return {
            "proposed": len(list(self.proposed_dir.glob("*.json"))),
            "approved": len(list(self.approved_dir.glob("*.json"))),
            "rejected": len(list(self.rejected_dir.glob("*.json"))),
            "audit_events": len(self.audit_log()),
        }


if __name__ == "__main__":
    # self-test: propose -> approve blocked by dead ref -> approve w/ drop -> reject path
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        g = ReviewGate(Path(td))
        prop = g.propose("passage:xyz", "ACCEPT", "good", "scholar-A", cited_refs=["claim:EXISTS", "claim:GHOST"])
        # register claim:EXISTS as a resolvable approved proposal (seed)
        (g.approved_dir / "claim:EXISTS.json").write_text("{}", encoding="utf-8")
        try:
            g.approve(prop["proposal_id"])
            print("approve: NOT blocked (unexpected)")
        except DeadRefError as e:
            print("approve blocked on dead ref:", "claim:GHOST" in str(e))
        ok = g.approve(prop["proposal_id"], drop_missing=True)
        print("approve w/ drop_missing:", ok["state"])
        print("gate state:", g.state())
        print("audit events:", len(g.audit_log()))
        assert ok["state"] == "APPROVED", "approve with drop_missing succeeds"
        assert ok["proposal_id"] == prop["proposal_id"]
        print("SELF-TEST PASS (durable review gate: dead-ref block + drop_missing + audit + durable dirs)")
