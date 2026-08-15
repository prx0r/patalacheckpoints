#!/usr/bin/env python3
"""products/scholar_profile/test.py — scholar-profile (contribution ledger) proof.
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/products/scholar_profile/test.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))

from products.scholar_profile.engine import profile, leaderboard  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("SCHOLAR PROFILE — proof (contribution ledger)\n")
    import tempfile
    from pathlib import Path as _P
    with tempfile.TemporaryDirectory() as td:
        td = _P(td)
        # write a review to the TEMP ledger (isolated — never pollutes the real one)
        (td / "reviews.jsonl").write_text(json.dumps({
            "review_id": "REV-TEST", "reviewer": "profile-test-scholar", "target_ref": "t:1",
            "decision": "ACCEPT", "created_at": "2026-08-15"}, ensure_ascii=False) + "\n")

        p = profile("profile-test-scholar", ledger_dir=td)
        gate("profile aggregates reviews", p["n_reviews"] >= 1, f"{p['n_reviews']} reviews")
        gate("reviews by decision", p["reviews_by_decision"].get("ACCEPT", 0) >= 1,
             str(p["reviews_by_decision"]))
        gate("recent activity listed", len(p["recent_activity"]) >= 1,
             f"{len(p['recent_activity'])} activity items")

        lb = leaderboard(ledger_dir=td)
        gate("leaderboard has the scholar", any(s["scholar"] == "profile-test-scholar"
                                                for s in lb["leaderboard"]),
             str(lb["leaderboard"]))
        gate("total reviews counted", lb["total_reviews"] >= 1, f"{lb['total_reviews']}")

        gate("machine-compiled honesty", "MACHINE_COMPILED" in p["note"],
             "contribution ledger, never a truth claim")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
