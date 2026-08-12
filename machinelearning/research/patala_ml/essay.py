"""patala_ml/essay.py — the canonical Essay object (JSON is the source of truth).

Per the review: essay.json is CANONICAL; essay.md is a deterministic projection, never an
independently-edited source. The essay carries its plan identity + plan_hash so staleness is
detectable (if the upstream EssayPlan changes, the essay is stale).

  essay_id · plan_id · plan_hash · theme_id · claims[] · sentences[] · verification_summary
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

from .essaysentence import EssaySentence


def plan_hash(plan_dict: dict) -> str:
    """A stable hash of the EssayPlan (for staleness detection)."""
    canon = json.dumps(plan_dict, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()[:16]


@dataclass
class Essay:
    essay_id: str
    plan_id: str
    plan_hash: str
    theme_id: str
    title: str
    claims: list[dict] = field(default_factory=list)        # the frozen EssayClaims
    sentences: list[EssaySentence] = field(default_factory=list)
    verification_summary: dict = field(default_factory=dict)

    def add_sentence(self, s: EssaySentence):
        self.sentences.append(s)

    def to_dict(self) -> dict:
        return {
            "essay_id": self.essay_id, "plan_id": self.plan_id, "plan_hash": self.plan_hash,
            "theme_id": self.theme_id, "title": self.title,
            "claims": self.claims,
            "sentences": [s.to_dict() for s in self.sentences],
            "verification_summary": self.verification_summary,
        }

    def to_markdown(self) -> str:
        """The DETERMINISTIC projection — never independently edited. Regenerate from JSON."""
        lines = [f"# {self.title}", ""]
        # render the claims first (the auditable spine)
        lines.append("## Claims")
        for c in self.claims:
            boundary = c.get("boundary", "")
            lines.append(f"- **{c['id']}** ({c.get('role','claim')}) — {c['text']}")
            if boundary:
                lines.append(f"  - *boundary:* {boundary}")
        lines.append("")
        # then the sentences
        lines.append("## Essay")
        for s in self.sentences:
            lines.append(s.text)
            lines.append("")
        return "\n".join(lines)
