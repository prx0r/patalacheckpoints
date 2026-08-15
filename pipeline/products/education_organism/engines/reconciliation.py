#!/usr/bin/env python3
"""kernels/reconciliation.py — GEM-C: the reconciliation gate (from Ambuda).

The anti-theatre gate for LLM-derived layers: prove the model "preserved source while adding structure."
The prompt contract is "add tags, NEVER change text"; a thresholded diff-check (line-count preservation,
grapheme-level diff) catches bulk corruption of LLM output. Mirrors Ambuda's reconciliation_check.py.

Deterministic + stdlib. Returns PASS/BLOCK for a generated layer against its source.
"""
from __future__ import annotations
import re


def _count_lines(text: str) -> int:
    return len([l for l in text.split("\n") if l.strip()])


def _content_words(text: str) -> set[str]:
    """Strip XML/markup tags + punctuation, return the set of content words (the provenance essence)."""
    no_tags = re.sub(r"<[^>]+>", " ", text)
    return set(re.findall(r"[a-zA-Zā-īūṛṝḷḹṃṁñṅśṣṭḍḥ]+", no_tags.lower()))


def reconciliation_check(source_text: str, generated_text: str,
                         *, line_tolerance: int = 1, max_fragment_drift: float = 0.05) -> dict:
    """Check that the LLM preserved the source content words while adding structure.

    source_text      — the real committed passage/claim
    generated_text   — the LLM's derived layer (may add tags/structure)
    line_tolerance   — allowed difference in line count (absolute)
    max_fragment_drift — allowed fraction of source content-words missing (relative)

    Returns {pass, line_delta, missing_fragments, drift, note}.
    """
    src_lines = _count_lines(source_text)
    gen_lines = _count_lines(generated_text)
    line_delta = abs(gen_lines - src_lines)

    src_words = _content_words(source_text)
    gen_words = _content_words(generated_text)
    missing = src_words - gen_words
    drift = len(missing) / max(1, len(src_words))

    ok = (line_delta <= line_tolerance) and (drift <= max_fragment_drift)
    return {"pass": bool(ok),
            "line_delta": line_delta, "missing_fragments": len(missing),
            "drift": round(drift, 4),
            "note": "source preserved while adding structure" if ok
            else f"BULK CHANGE: {len(missing)} source words missing, drift {round(drift,3)} > {max_fragment_drift}"}


if __name__ == "__main__":
    # demo: a good derivation preserves the source; a corrupt one drops content
    src = "The flashing has an order-less support, the great Lord, required by ordered experience."
    good = "<claim>The flashing has an order-less support, the great Lord, required by ordered experience.</claim>"
    corrupt = "The flashing has an order-less support."  # dropped the rest
    print("good:", reconciliation_check(src, good))
    print("corrupt:", reconciliation_check(src, corrupt))
