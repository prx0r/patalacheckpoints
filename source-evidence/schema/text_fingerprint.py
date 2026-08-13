#!/usr/bin/env python3
"""source-evidence/schema/text_fingerprint.py — manuscript text-fingerprint primitive (P4 depth / §5).

The reviewer's §5: for any manuscript transcription/OCR, generate multiple cheap fingerprints for
candidate retrieval (millions of records cannot be compared exhaustively):

    incipit fingerprint      the opening words (normalized)
    explicit fingerprint     the closing words
    n-gram fingerprint       character/syllable n-grams
    MinHash-style           locality-sensitive hashing for cheap Jaccard

Not because embeddings are magically authoritative — because you want cheap candidate retrieval:
    unknown manuscript -> nearest-100 candidates (fingerprints) -> stronger sequence compare -> scholar.

This is the cheap-CANDIDATE-GENERATION layer that feeds the reconciliation engine (P3) + the
MANUSCRIPT-RESOLUTION-GOLD benchmark (P4). Fingerprints are EVIDENCE, never identity truth.
"""
from __future__ import annotations

import hashlib
import re


def _norm(t: str) -> str:
    t = re.sub(r"[^a-z0-9 ]", "", (t or "").lower())
    return " ".join(t.split())


def _ngrams(s: str, n: int) -> set:
    s = s.replace(" ", "")
    return {s[i:i + n] for i in range(len(s) - n + 1)}


def incipit(text: str, n_words: int = 12) -> str:
    """The opening normalized words (a stable textual anchor)."""
    w = _norm(text).split()
    return " ".join(w[:n_words])


def explicit(text: str, n_words: int = 12) -> str:
    """The closing normalized words (the colophon/explicit anchor)."""
    w = _norm(text).split()
    return " ".join(w[-n_words:])


def char_ngram_set(text: str, n: int = 5) -> set:
    return _ngrams(text, n)


def minhash_fingerprint(text: str, n: int = 5, n_hashes: int = 16) -> list[str]:
    """MinHash-style signature: the min of n independent hash seeds over the char-ngram set.

    Cheap Jaccard proxy: two similar texts share ~the same min-hashes. Uses sha256 with salt seeds.
    """
    grams = _ngrams(text, n)
    sig = []
    for seed in range(n_hashes):
        m = None
        for g in grams:
            h = int(hashlib.sha256((str(seed) + g).encode()).hexdigest()[:8], 16)
            m = h if m is None else min(m, h)
        sig.append(m if m is not None else 0)
    return sig


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def minhash_sim(sig_a: list[int], sig_b: list[int]) -> float:
    if not sig_a or not sig_b:
        return 0.0
    return sum(1 for x, y in zip(sig_a, sig_b) if x == y) / len(sig_a)


def fingerprint(text: str) -> dict:
    """The composite fingerprint of a text (all cheap signals, evidence-only)."""
    return {
        "incipit": incipit(text),
        "explicit": explicit(text),
        "char_ngrams": sorted(char_ngram_set(text)),
        "minhash": minhash_fingerprint(text),
    }


def candidate_rank(unknown: str, corpus: list[str], k: int = 3) -> list[dict]:
    """Cheap candidate retrieval: rank corpus texts against an unknown manuscript by fingerprints."""
    fu = fingerprint(unknown)
    ranked = []
    for i, txt in enumerate(corpus):
        f = fingerprint(txt)
        incipit_sim = 1.0 if fu["incipit"] == f["incipit"] else (0.5 if fu["incipit"] and f["incipit"]
                                                                  and fu["incipit"].split()[0] == f["incipit"].split()[0] else 0.0)
        gram_sim = jaccard(set(fu["char_ngrams"]), set(f["char_ngrams"]))
        min_sim = minhash_sim(fu["minhash"], f["minhash"])
        blended = 0.4 * incipit_sim + 0.3 * gram_sim + 0.3 * min_sim
        ranked.append({"index": i, "incipit_sim": round(incipit_sim, 3),
                       "ngram_jaccard": round(gram_sim, 3), "minhash_sim": round(min_sim, 3),
                       "blended": round(blended, 3)})
    ranked.sort(key=lambda r: r["blended"], reverse=True)
    return ranked[:k]


if __name__ == "__main__":
    # self-test: two transcriptions of the SAME verse match; a different verse does not
    v1 = "atha mālinīvijayottaram nama mahāyogini jñānakāṇḍaṃ bṛhat tantraṃ ārabhate"
    v1b = "atha malinivijayottaram namah mahayogini jnanakandam brhat tantram arabhate"  # a variant transcription
    v2 = "yadā tu saṃsāraṃ kṣayayati tadā śivaḥ svena bhāti"  # a different verse
    f1, f1b, f2 = fingerprint(v1), fingerprint(v1b), fingerprint(v2)
    print("v1 incipit:", f1["incipit"])
    print("v1 vs v1b (same verse, variant): minhash_sim =", minhash_sim(f1["minhash"], f1b["minhash"]))
    print("v1 vs v2  (different verse):     minhash_sim =", minhash_sim(f1["minhash"], f2["minhash"]))
    r = candidate_rank(v1, [v2, v1b])
    print("candidate rank (should put v1b first):", [(x["index"], x["blended"]) for x in r])
    assert minhash_sim(f1["minhash"], f1b["minhash"]) > minhash_sim(f1["minhash"], f2["minhash"]), \
        "same-verse variants must be closer than different verses"
    print("SELF-TEST PASS (fingerprints: cheap candidate retrieval, same-verse > different-verse)")
