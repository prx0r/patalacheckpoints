"""patala_ml/retrieval.py — the retrieval baselines (CPU-only).

BM25 · dense · hybrid. These are the *things to beat* per the frozen strategy — no learned
model is adopted until it beats these on a fixed held-out set.

Dense is optional (needs the sentence-transformers package + a model). BM25 and hybrid run
with zero heavy deps.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable

import numpy as np
from rank_bm25 import BM25Okapi

from .corpus import PassageDoc


def tokenize(text: str) -> list[str]:
    """A conservative tokenizer for the C1/L2 scholarly prose (lowercase word tokens)."""
    return re.findall(r"[a-zā-īūṛḷṅñṭḍṇśṣḥ'’\-]+", text.lower())


@dataclass
class Retriever:
    """Base retriever: build an index over docs, then rank by a score fn."""
    docs: list[PassageDoc]
    score_fn: Callable[[str], np.ndarray]  # query -> per-doc scores
    name: str = "retriever"
    field: str = "full"  # full | l2 | c1 — which representation is indexed

    def build(self):
        return self

    def search(self, query: str, k: int = 10) -> list[tuple[str, float]]:
        scores = self.score_fn(query)
        order = np.argsort(-scores)
        return [(self.docs[i].id, float(scores[i])) for i in order[:k]]


def _doc_text(d: PassageDoc, field: str) -> str:
    if field == "l2":
        return d.l2_text
    if field == "c1":
        return d.c1_body
    return d.full_text()


def make_bm25(docs: list[PassageDoc], field: str = "full") -> Retriever:
    corpus = [tokenize(_doc_text(d, field)) for d in docs]
    bm = BM25Okapi(corpus)
    return Retriever(
        docs=docs,
        name=f"BM25:{field}",
        field=field,
        score_fn=lambda q: np.array(bm.get_scores(tokenize(q)), dtype=float),
    )


def make_dense(docs: list[PassageDoc], model_name: str = "sentence-transformers/all-MiniLM-L6-v2", field: str = "full") -> Retriever:
    """Dense (sentence-BERT) retriever — CPU-friendly for ~60 docs. Requires sentence-transformers."""
    from sentence_transformers import SentenceTransformer  # heavy, lazy import
    texts = [_doc_text(d, field) for d in docs]
    model = SentenceTransformer(model_name)
    vecs = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)

    def score(query: str) -> np.ndarray:
        qv = model.encode([query], normalize_embeddings=True, convert_to_numpy=True)[0]
        return vecs @ qv  # cosine (normalized)

    return Retriever(docs=docs, name=f"dense:{model_name.split('/')[-1]}", field=field, score_fn=score)


def make_hybrid(docs: list[PassageDoc], bm25_w: float = 0.5, dense_w: float = 0.5, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", field: str = "full") -> Retriever:
    """Hybrid = weighted sum of (min-max-normalized BM25) + (cosine dense)."""
    bm = make_bm25(docs, field=field)
    # precompute dense matrix
    from sentence_transformers import SentenceTransformer
    texts = [_doc_text(d, field) for d in docs]
    model = SentenceTransformer(model_name)
    vecs = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)

    def norm(x: np.ndarray) -> np.ndarray:
        lo, hi = x.min(), x.max()
        return (x - lo) / (hi - lo) if hi > lo else x * 0

    def score(query: str) -> np.ndarray:
        b = norm(bm.score_fn(query))
        qv = model.encode([query], normalize_embeddings=True, convert_to_numpy=True)[0]
        d = (vecs @ qv - vecs.min()) / (vecs.max() - vecs.min() + 1e-9)
        return bm25_w * b + dense_w * d

    return Retriever(docs=docs, name="hybrid", field=field, score_fn=score)


RETRIEVERS = {
    "bm25": make_bm25,
    "dense": make_dense,
    "hybrid": make_hybrid,
}
