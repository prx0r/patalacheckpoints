"""patala_ml/semantic_alignment.py — Stage A: benchmarkable coarse semantic alignment (MACHINE_PROPOSED).

The foundational symbolic layer of the "semantic microscope". Given two CONTEXTUALIZED occurrences of a
concept, `align(A, B)` returns a proposal for the semantic relation, with evidence + scores + an
abstention reason.

It is deliberately NOT an engine — it is a benchmarkable function:
    align(occurrence_A, occurrence_B) -> {
        relation_proposal,       # one of the 6 labels below
        evidence,                # per-representation cosine + lexical overlap
        model_scores,            # raw scores
        abstain_reason,          # non-null only when it abstains (AMBIGUOUS / NOT_ENOUGH_CONTEXT)
    }

Labels (preserved, never collapsed to SAME/NEAR/DIFFERENT):
    SAME_SENSE · NEAR_SAME · PARTIAL_OVERLAP · DIFFERENT_SENSE · AMBIGUOUS · NOT_ENOUGH_CONTEXT
The last two are abstentions: a good scholarly aligner knows when similarity is not enough to decide.

Three representation spaces are tested SEPARATELY + combined (the empirical question is which space
catches false similarity vs true NEAR_SAME):
    sanskrit   — the Sanskrit/IAST window
    l2         — the English reading
    c1         — the commentary/conceptual space

HARD RULE (freeze): a neural similarity score NEVER becomes a scholarly relation by itself. It may
NOMINATE a relation; only the Pāṭala layer records what relation is asserted + at what review_status.
This module returns MACHINE_PROPOSED proposals for a benchmark.
"""
from __future__ import annotations

import hashlib
import math
import re

LABELS = ["SAME_SENSE", "NEAR_SAME", "PARTIAL_OVERLAP", "DIFFERENT_SENSE", "AMBIGUOUS",
          "NOT_ENOUGH_CONTEXT"]
SPACES = ["sanskrit", "l2", "c1"]

# ---- embedding: dense (sentence_transformers if a model loads) + offline lexical fallback ----
_encoder = None


def _get_dense_encoder():
    global _encoder
    if _encoder is not None:
        return _encoder
    try:
        from sentence_transformers import SentenceTransformer
        # a small general model; try to load, fall back to None if unavailable (no network/model)
        _encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    except Exception:
        _encoder = False
    return _encoder if _encoder is not False else None


def _tokenize(s: str) -> list[str]:
    return re.findall(r"[a-zāīūṛṣṭṇḥ]+", (s or "").lower())


def _hashed_ngram_vec(s: str, dim: int = 512, n: int = 3) -> list[float]:
    """Offline lexical embedding: hashed character n-gram bag (captures transliteration)."""
    v = [0.0] * dim
    s = re.sub(r"[^a-zāīūṛṣṭṇḥ]", " ", (s or "").lower())
    s = re.sub(r"\s+", "", s)
    if len(s) < n:
        return v
    for i in range(len(s) - n + 1):
        g = s[i:i + n]
        h = int(hashlib.md5(g.encode()).hexdigest(), 16)
        v[h % dim] += 1.0
    norm = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / norm for x in v]


def _cos(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def embed(text: str, space: str) -> list[float]:
    """Embed text in a representation space. Dense if available, else offline lexical fallback."""
    dense = _get_dense_encoder()
    if dense is not None:
        try:
            vec = dense.encode(text or " ")
            return [float(x) for x in vec]
        except Exception:
            pass
    return _hashed_ngram_vec(text)


# ---- occurrence ───────────────────────────────────────────────────────────────
def occurrence(lemma: str, sanskrit: str, l2: str, c1: str, passage_id: str, scope: str = "") -> dict:
    return {"lemma": lemma, "sanskrit": sanskrit, "l2": l2, "c1": c1,
            "passage_id": passage_id, "scope": scope}


# ---- the align function ──────────────────────────────────────────────────────
def align(A: dict, B: dict) -> dict:
    """Propose the semantic relation between two contextualized occurrences. MACHINE_PROPOSED."""
    # NOT_ENOUGH_CONTEXT: if either occurrence has too little text to judge in ANY usable space
    if len(_tokenize(A.get("c1", ""))) < 6 and len(_tokenize(B.get("c1", ""))) < 6:
        return {"relation_proposal": "NOT_ENOUGH_CONTEXT", "evidence": {},
                "model_scores": {}, "abstain_reason": "both C1s too short to judge",
                "status": "MACHINE_PROPOSED"}

    sims = {}
    for sp in SPACES:
        va, vb = embed(A.get(sp, ""), sp), embed(B.get(sp, ""), sp)
        sims[sp] = round(_cos(va, vb), 4)

    # lexical overlap of the Sanskrit windows (transliteration-level) as a separate signal
    a_tok, b_tok = set(_tokenize(A.get("sanskrit", ""))), set(_tokenize(B.get("sanskrit", "")))
    lex = round(len(a_tok & b_tok) / max(1, len(a_tok | b_tok)), 4)

    # only average over spaces that have usable text
    usable = [s for s in SPACES if len(_tokenize(A.get(s, ""))) >= 4 and len(_tokenize(B.get(s, ""))) >= 4]
    used_sims = {s: sims[s] for s in usable} or {SPACES[2]: sims[SPACES[2]]}
    mean = sum(used_sims.values()) / len(used_sims)
    spread = max(used_sims.values()) - min(used_sims.values())
    variance = sum((x - mean) ** 2 for x in used_sims.values()) / len(used_sims)

    evidence = {"per_space_cosine": sims, "sanskrit_lexical_overlap": lex,
                "mean": round(mean, 4), "spread": round(spread, 4)}
    scores = {**sims, "sanskrit_lexical_overlap": lex, "mean": round(mean, 4)}

    # proposal logic (deliberately simple + interpretable; tune ONLY against gold, never by hand-feel)
    if mean >= 0.82:
        proposal = "SAME_SENSE"
    elif mean >= 0.62:
        proposal = "NEAR_SAME"
    elif mean <= 0.32:
        proposal = "DIFFERENT_SENSE"
    else:
        proposal = "PARTIAL_OVERLAP"

    # abstain: high disagreement among spaces -> AMBIGUOUS
    abstain_reason = None
    if variance > 0.05 or spread > 0.35:
        proposal = "AMBIGUOUS"
        abstain_reason = f"representations disagree (spread={spread:.2f}, var={variance:.3f})"

    return {"relation_proposal": proposal, "evidence": evidence, "model_scores": scores,
            "abstain_reason": abstain_reason, "status": "MACHINE_PROPOSED"}
