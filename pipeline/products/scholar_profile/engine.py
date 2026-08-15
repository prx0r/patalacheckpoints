"""products/scholar_profile/engine.py — the scholar profile (the contribution ledger).

A scholar's value is their accumulated judgment. This aggregates by reviewer the reviews + attestations
that the scholar has contributed — the "Dr X — 37 manuscript identifications, 12 adjudicated
translations" record from the vision (globalaccess.md). The data is already produced (append-only
reviews + signed attestations carry a reviewer); the AGGREGATION is what's new.

What it provides (CPU-only, deterministic):
  - profile(scholar_id) -> the scholar's contributions (reviews by decision, attestations, scope)
  - activity(scholar_id) -> the chronological ledger of what they did
  - leaderboard() -> the contribution overview across scholars (the institution/scholar page)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(_ROOT / "pipeline"))

from products.scholar_review.engine import ScholarProduct  # noqa: E402
from products.scholar_review.gate import ReviewGate  # noqa: E402


def _load_gate_events() -> list[dict]:
    g = ReviewGate()
    return g.audit_log()


def _load_reviews(ledger_dir: str | None = None) -> list[dict]:
    """Load the persisted contribution ledger (reviews.jsonl) — accumulates across sessions.

    ledger_dir: override the ledger location (tests use a temp dir to avoid polluting the real one).
    """
    base = Path(ledger_dir) if ledger_dir else _ROOT / "data/scholar"
    p = base / "reviews.jsonl"
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def _load_attestations(ledger_dir: str | None = None) -> list[dict]:
    base = Path(ledger_dir) if ledger_dir else _ROOT / "data/scholar"
    p = base / "attestations.jsonl"
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def profile(scholar_id: str, ledger_dir: str | None = None) -> dict:
    """Aggregate a scholar's contributions from the PERSISTED ledger: reviews + attestations."""
    reviews = [r for r in _load_reviews(ledger_dir) if r.get("reviewer") == scholar_id]
    atts = [a for a in _load_attestations(ledger_dir) if a.get("reviewer") == scholar_id]

    from collections import Counter
    by_decision = Counter(r.get("decision") for r in reviews)

    return {
        "scholar_id": scholar_id,
        "n_reviews": len(reviews),
        "reviews_by_decision": dict(by_decision),
        "n_attestations": len(atts),
        "recent_activity": sorted(
            [{"at": r.get("created_at"), "type": "review", "target": r.get("target_ref"),
              "decision": r.get("decision")} for r in reviews]
            + [{"at": a.get("created_at"), "type": "attestation", "target": a.get("target_ref"),
                "verdict": a.get("verdict")} for a in atts],
            key=lambda x: str(x.get("at")), reverse=True)[:10],
        "note": "MACHINE_COMPILED contribution ledger (persisted reviews + signed attestations)",
    }


def activity(scholar_id: str) -> dict:
    """The chronological contribution ledger."""
    p = profile(scholar_id)
    return {"scholar_id": scholar_id, "activity": p["recent_activity"], "count": len(p["recent_activity"])}


def leaderboard(limit: int = 10, ledger_dir: str | None = None) -> dict:
    """The contribution overview across scholars (from the persisted ledger)."""
    from collections import Counter
    by_reviewer = Counter(r.get("reviewer") for r in _load_reviews(ledger_dir))
    top = [{"scholar": r, "n_reviews": c} for r, c in by_reviewer.most_common(limit)]
    return {"leaderboard": top, "total_reviews": sum(by_reviewer.values()),
            "total_attestations": len(_load_attestations(ledger_dir)),
            "note": "reviews + attestations by reviewer (persisted ledger)"}


if __name__ == "__main__":
    import sys as _s
    verb = _s.argv[1] if len(_s.argv) > 1 else "leaderboard"
    if verb == "profile":
        print(json.dumps(profile(_s.argv[2]), indent=2, ensure_ascii=False))
    elif verb == "activity":
        print(json.dumps(activity(_s.argv[2]), indent=2, ensure_ascii=False))
    else:
        print(json.dumps(leaderboard(int(_s.argv[2]) if len(_s.argv) > 2 else 10),
                         indent=2, ensure_ascii=False))
