"""patala_ml/adjudicate.py — the human-review → accepted promotion (completes the loop).

The gold chain is only SCHOLARSHIP when a human ACCEPTS it. This module:
  1. loads the adjudication package (adjudicate_cl3.py output)
  2. records the reviewer's decisions on D-THEME-ACCEPT / D-ARG-ACCEPT / D-LEXICAL-OPEN
  3. if all accepted, promotes the theme + argument to `editorially_accepted` in the record
  4. returns the final signed certificate (the auditable, human-backed artifact)

This is the 'human-in-the-loop' step — the difference between automation and scholarship.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field


@dataclass
class Adjudication:
    adjudication_id: str
    record: dict
    decisions: dict = field(default_factory=dict)   # {decision_id: choice}
    reviewer: str = ""
    status: str = "AWAITING_REVIEW"

    @property
    def all_accepted(self) -> bool:
        return all(
            self.decisions.get(d["id"]) == d.get("default", "ACCEPT")
            or self.decisions.get(d["id"]) == "ACCEPT"
            or self.decisions.get(d["id"]) == "APPROVE_AS_OPEN"
            for d in self.record.get("decisions_required", [])
        )

    def sign(self, reviewer: str, decisions: dict) -> dict:
        """Apply a reviewer's decisions. Promotes if all accepted."""
        self.reviewer = reviewer
        self.decisions = decisions
        for d in self.record.get("decisions_required", []):
            if d["id"] not in decisions:
                return {"ok": False, "error": f"missing decision {d['id']}"}

        self.record["reviewed_by"] = reviewer
        self.record["decisions"] = decisions

        if self.all_accepted:
            self.status = "EDITORIALLY_ACCEPTED"
            self.record["status"] = "EDITORIALLY_ACCEPTED"
            self.record["accepted_theme"] = self.record["proposed_theme"]["label"]
            self.record["accepted_argument"] = self.record["proposed_argument"]["argument_id"]
        else:
            self.status = "MODIFIED"
            self.record["status"] = "MODIFIED"
        return {"ok": True, "status": self.status}


def load_adjudication(path: str) -> Adjudication:
    return Adjudication(
        adjudication_id=json.load(open(path)).get("adjudication_id"),
        record=json.load(open(path)),
    )
