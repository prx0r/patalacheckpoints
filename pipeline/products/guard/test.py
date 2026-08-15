#!/usr/bin/env python3
"""products/guard/test.py — the serve-time guard proof (enforce UNANCHORED -> reject).
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/products/guard/test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "pipeline"))

from products.guard.engine import (  # noqa: E402
    guard_answer,
    verify_quoted_content,
    enforce_citation_whitelist,
    _normalise,
    _windowed_ratio,
)

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


SRC = [
    {
        "title": "ipvv",
        "locus": "1.1.1",
        "text": "The spontaneity of the Lord is self-aware light (svācchandya). This is where the whole vimarśinī begins, the recognition that consciousness is never inert.",
    }
]


def main():
    print("GUARD — serve-time verification proof (UNANCHORED -> reject)\n")

    # a REAL quote (verbatim from source, quoted) is verified and stays served
    real = guard_answer(
        "As Abhinavagupta writes, 'The spontaneity of the Lord is self-aware light' (ipvv:1.1.1), and this is where the whole vimarśinī begins.",
        SRC,
    )
    gate("real quote served (safe)", real["safe_to_serve"] is True,
         f"citation preserved, gloss untouched")
    gate("real quote verified", real["quote_guard"]["verified"] >= 1,
         f"verified={real['quote_guard']['verified']}")

    # a FABRICATED quote (not in source) is downgraded -> not safe
    fab = guard_answer(
        "Abhinavagupta says 'the spontaneity is completely inert matter' (ipvv:1.1.1) — which changes everything.",
        SRC,
    )
    gate("fabricated quote blocked (not safe)", fab["safe_to_serve"] is False,
         "must never serve a false verbatim quote")
    gate("fabricated quote downgraded", len(fab["quote_guard"]["downgraded"]) >= 1,
         f"reason={fab['quote_guard']['downgraded'][0]['reason']}, bucket={fab['quote_guard']['downgraded'][0]['bucket']}")

    # normalisation: Sanskrit diacritics fold so a dropped macron doesn't false-fail
    gate("sanskrit fold (ā->a)", _normalise("svācchandya") == _normalise("svacchandya"),
         "diacritic-insensitive quote match")
    gate("windowed ratio of a real quote = 1.0", _windowed_ratio(
        "spontaneity of the Lord is self-aware light", SRC[0]["text"]) >= 1.0,
         "verbatim quote inside source matches exactly")

    # citation whitelist: a hallucinated work is stripped, a real (work:locus) kept
    cg_real = enforce_citation_whitelist("the reading (ipvv:1.1.1)", SRC)
    gate("real citation kept", cg_real["corrected_count"] == 0, "whitelisted (work, locus) preserved")
    # a gloss parenthetical is NOT treated as a citation
    cg_gloss = enforce_citation_whitelist("self-aware light (svācchandya)", SRC)
    gate("gloss parenthetical not stripped", cg_gloss["corrected_count"] == 0,
         "a bare parenthetical is not a citation")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
