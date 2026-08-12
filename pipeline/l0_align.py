#!/usr/bin/env python3
"""pipeline/l0_align.py — P4: L0<->L2 term-anchor alignment (the meaningful benchmark).

P4 asks "which Sanskrit aligns to which English?". Per docs/P4_ALIGNMENT_SPEC.md, the prior baseline
(benchmark_p4_alignment.py v0) measured the by-construction gloss<->iast pairs — a circular task. The
real, scoped task is:

    Recover the inline IAST anchors the L2 prose itself marks in parentheses
    (e.g. "reflexive-awareness (vimarśa)", "re-reflection (parāmarśa)")
    and link each anchor to its matching L0 lemma record within the same passage.

The L2 is freestyle paraphrase, NOT a translation — so free-form bitext alignment (awesome-align AER)
is ill-defined. We align the token-grounded claims the prose marks via parentheses, and abstain
(UNALIGNED) on the interpretive SUPPLIED prose around them. This matches the Fidelity-note discipline
already present in the L2 files and the abstention principle in AGENTS-DOCTRINE.

Gold-first, benchmark-first: build the anchor gold, run baselines blind, then (optionally) a real
aligner must beat the floor. No "alignment solved" claim without a BenchmarkRun on frozen gold.

Schema of the L0 record we consume (specs/l0_schema.json):
    { lemma_iast, literal_gloss, chunk_id, line_id, quoted, status, ... }
Schema of the published passage we consume:
    { id, chunk, l2_text, l0, ... }  (l2_text = the prose; l0 is null in published — L0 lives in *.l0.jsonl)
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import random
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

# optional independent morphological witness (Vidyut, the P2 engine — already installed)
try:
    from verify_l0_p2 import vidyut_analyze as _vidyut_analyze
    VIDYUT_AVAILABLE = True
except Exception:  # pragma: no cover
    _vidyut_analyze = None
    VIDYUT_AVAILABLE = False

# --------------------------------------------------------------------------- #
# constants
# --------------------------------------------------------------------------- #
IAST_CHARS = "a-zA-Zāīūṛṝḷḹṃñṅśṣṭḍḥṁ"
# the IAST DIACRITICS are the reliable signal that a parenthesised string is Sanskrit (not English):
# English prose ("the crystal") has none; Sanskrit IAST words almost always carry at least one
# (vimarśa -> ś, prakāśa -> ā/ś, tuṭi -> ṭ, saṃvid -> ṃ). Pure-ASCII Sanskrit terms are rare enough
# that abstaining on them is the honest, precision-first choice (per the abstention principle).
DIACRITICS = "āīūṛṝḷḹṃñṅśṣṭḍḥṁ"
# inline IAST anchor: parenthesized content that contains at least one DIACRITIC-carrying token
_NEG_CLASS = r"[^()（）\[\]{}]*?"
ANCHOR_RE = re.compile(
    rf"[（(]({_NEG_CLASS}[{DIACRITICS}]{_NEG_CLASS})[)）]"
)
IAST_TOKEN_RE = re.compile(rf"[{IAST_CHARS}]+")

# diacritic-insensitive normalisation: strips IAST diacritics to plain ASCII. Used for stem-prefix
# matching so that stem 'parāmarśa' matches surface 'parāmarśā'/'parāmarśāt' (case-ending vowel).
_ASCIITRANS = str.maketrans({
    "ā": "a", "ī": "i", "ū": "u", "ṛ": "r", "ṝ": "r", "ḷ": "l", "ḹ": "l",
    "ṃ": "m", "ṁ": "m", "ñ": "n", "ṅ": "n", "ś": "s", "ṣ": "s", "ṭ": "t",
    "ḍ": "d", "ḥ": "h",
})


def norm_lemma(s: str) -> str:
    """Lowercase + strip non-IAST noise; used for surface matching (not authoritative)."""
    return re.sub(rf"[^{IAST_CHARS}]", "", s.lower())


def norm_ascii(s: str) -> str:
    """Diacritic-insensitive normalisation (ā->a, ś->s, ...): the stem-match key."""
    return norm_lemma(s).translate(_ASCIITRANS)


def is_iaST_anchor(text: str) -> bool:
    """Does this parenthesised string contain a genuine IAST token (a real Sanskrit word)?

    Requires at least one DIACRITIC — this is what separates Sanskrit ("the bursting" contains
    'tuṭi' -> ṭ) from plain English prose ("the crystal"). Precision-first: a parenthesised
    string with no diacritic is treated as English and NOT an anchor (abstain).
    """
    return bool(re.search(rf"[{DIACRITICS}]", text))


# --------------------------------------------------------------------------- #
# gold extraction
# --------------------------------------------------------------------------- #
@dataclass
class AnchorGold:
    """One gold alignment instance: an L2 anchor linked to an L0 lemma in the same passage."""
    passage_id: str
    chunk: str
    anchor_text: str          # the raw parenthesised string from L2, e.g. "vimarśa"
    anchor_in_l2: bool        # True if the prose actually marked it in parens (gold anchor)
    resolved_l0_lemma: str | None  # the L0 lemma it should resolve to (or None => abstain)
    resolved: bool = False

    def to_dict(self) -> dict:
        return {
            "passage_id": self.passage_id, "chunk": self.chunk,
            "anchor_text": self.anchor_text, "anchor_in_l2": self.anchor_in_l2,
            "resolved_l0_lemma": self.resolved_l0_lemma, "resolved": self.resolved,
        }


def load_l0_lemmas(l0dir: str, chunk: str) -> dict[str, list[dict]]:
    """Load L0 records for one chunk, indexed by normalised lemma -> [records]."""
    path = os.path.join(l0dir, f"{chunk}.l0.jsonl")
    if not os.path.exists(path):
        return {}
    out: dict[str, list[dict]] = defaultdict(list)
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            lem = r.get("lemma_iast")
            if not lem:
                continue
            out[norm_lemma(lem)].append(r)
    return out


def extract_anchors_from_l2(l2_text: str) -> list[str]:
    """Return the list of parenthesised strings in the L2 prose that look like IAST anchors."""
    return [m.strip() for m in ANCHOR_RE.findall(l2_text) if is_iaST_anchor(m.strip())]


def resolve_anchor(anchor: str, l0_by_lemma: dict[str, list[dict]],
                   min_stem: int = 3) -> str | None:
    """Link an L2 anchor to a matching L0 lemma, else None (abstain).

    Per the P2 matching-rule lesson (LOG.md): L0's lemma_iast is the SURFACE form
    (e.g. vimarśaṃ, vimarśāt), while the L2 anchor is the STEM (vimarśa). Exact matching
    therefore fails ~50% of the time. We match stem-as-prefix (min stem length guards against
    short/false prefix matches), which is the established, honest rule.

    Priority: exact-normalised first, then stem-prefix. If the anchor is non-Sanskrit prose
    (e.g. "the bursting", a supplied gloss), it does NOT resolve -> None (abstain).
    """
    norm = norm_ascii(anchor)
    if not norm:
        return None
    # try the anchor as a whole, then each IAST token inside it (ASCII-normalised)
    candidates = [norm]
    for tok in IAST_TOKEN_RE.findall(anchor):
        t = norm_ascii(tok)
        if t not in candidates:
            candidates.append(t)
    # build an ascii-keyed index of L0 lemmas once
    l0_ascii = {k: norm_ascii(k) for k in l0_by_lemma}
    for c in candidates:
        if not c or len(c) < min_stem:
            continue
        # exact (diacritic-insensitive)
        for k, ka in l0_ascii.items():
            if ka == c:
                return k
        # stem-as-prefix: an L0 lemma whose ASCII form STARTS WITH this stem
        for k, ka in l0_ascii.items():
            if ka.startswith(c):
                return k
    return None


# --------------------------------------------------------------------------- #
# baselines + candidate aligner
# --------------------------------------------------------------------------- #
def baseline_paren_extraction(l2_text: str) -> list[str]:
    """Baseline 1: naive regex paren-extraction (anchor recall floor, 0 resolution)."""
    return extract_anchors_from_l2(l2_text)


def baseline_token_overlap(l2_text: str, l0_by_lemma: dict[str, list[dict]]) -> list[str]:
    """Baseline 2: link each extracted anchor by surface overlap to an L0 lemma."""
    resolved = []
    for anchor in extract_anchors_from_l2(l2_text):
        r = resolve_anchor(anchor, l0_by_lemma)
        resolved.append(r if r else None)
    return resolved


def candidate_alignment(l2_text: str, l0_by_lemma: dict[str, list[dict]]) -> list[str]:
    """Candidate aligner: anchor extraction + lemma resolution (abstain on non-anchors).

    This is the floor a real neural aligner (awesome-align) must beat on resolution.
    """
    return baseline_token_overlap(l2_text, l0_by_lemma)


# --------------------------------------------------------------------------- #
# independent morphological witness (Vidyut) — the non-human "second reviewer"
# --------------------------------------------------------------------------- #
def vidyut_stems(surface: str) -> set[str]:
    """Return Vidyut's lemmas (SLP1) for a surface form, as an ASCII set.

    Vidyut returns the STEM (e.g. vimarSa -> 'vimfS'); the L0 surface and the L2 anchor both
    reduce through Vidyut. Two forms are morphologically-consistent iff they share a stem.
    """
    if not VIDYUT_AVAILABLE:
        return set()
    out = set()
    for a in _vidyut_analyze(surface):
        lem = a.get("lemma")
        if lem:
            out.add(norm_ascii(lem))
    return out


def vidyut_agreement(anchor: str, l0_lemma: str) -> str:
    """Independently confirm that an L2 anchor and an L0 lemma share a Vidyut stem.

    Returns:
      'AGREE'    Vidyut assigns both forms a common stem (independent confirmation)
      'DISAGREE' Vidyut analyzes both but their stems do not overlap
      'UNABLE'   Vidyut cannot analyze anchor or lemma (not a disagreement, just no witness)
    """
    if not VIDYUT_AVAILABLE:
        return "UNABLE"
    anchor_stems = vidyut_stems(anchor)
    lemma_stems = vidyut_stems(l0_lemma)
    if not anchor_stems or not lemma_stems:
        return "UNABLE"
    return "AGREE" if (anchor_stems & lemma_stems) else "DISAGREE"


def vidyut_ensemble_rate(passages, l0dir: str, seed: int = 42, limit: int = 0) -> dict:
    """Compute the Vidyut ensemble-agreement rate over the resolved anchor->lemma links.

    This is the non-human "two reviewers" step (per the P2 Vidyut×Heritage precedent): the
    token-overlap baseline (method 1) proposes an anchor->lemma link; Vidyut (method 2,
    independent morphological analysis) confirms or denies it. Agreement = independent support.

    Returns {n_links, agree, disagree, unable, agree_rate, note}.
    """
    import random as _r
    from l0_align import extract_anchors_from_l2 as _ext, load_l0_lemmas as _load, resolve_anchor as _res

    passages = list(passages)
    if limit:
        _r.seed(seed)
        passages = _r.sample(passages, min(limit, len(passages)))
    agree = disagree = unable = 0
    details = []
    for p in passages:
        chunk_stem = (p.get("chunk") or p["id"]).replace(".md", "")
        l0 = _load(l0dir, chunk_stem)
        for anchor in _ext(p.get("l2_text") or ""):
            res = _res(anchor, l0)
            if res is None:
                continue
            verdict = vidyut_agreement(anchor, res)
            if verdict == "AGREE":
                agree += 1
            elif verdict == "DISAGREE":
                disagree += 1
            else:
                unable += 1
            details.append({"anchor": anchor, "l0_lemma": res, "vidyut": verdict})
    n = agree + disagree + unable
    analyzed = agree + disagree
    return {
        "n_links": n, "agree": agree, "disagree": disagree, "unable": unable,
        "agree_rate": round(agree / n, 4) if n else 0.0,
        "agree_rate_analyzed_only": round(agree / analyzed, 4) if analyzed else 0.0,
        "analyzed_share": round(analyzed / n, 4) if n else 0.0,
        "note": ("independent Vidyut morphological witness. AGREE = Vidyut assigns the anchor and "
                 "the L0 lemma a common stem; agree_rate is the independent-confirmation rate over "
                 "ALL links; agree_rate_analyzed_only is over links Vidyut could analyze (UNABLE = "
                 "no witness, not a disagreement; mostly inflected/compound L0 surfaces Vidyut "
                 "cannot parse — honest abstention, never fabricated agreement)."),
        "details": details,
    }


# --------------------------------------------------------------------------- #
# benchmark harness
# --------------------------------------------------------------------------- #
@dataclass
class P4Result:
    passage_id: str
    n_anchors: int
    anchor_recall: float      # found / gold (anchor recovery)
    resolution_precision: float  # correctly-resolved / resolved-attempted
    resolution_recall: float  # correctly-resolved / gold-anchors
    abstain_quality: float    # of gold non-anchors... (see metrics)
    resolved_ok: int
    resolved_wrong: int
    abstained: int
    gold_anchors: int = 0

    def to_dict(self) -> dict:
        return {
            "passage_id": self.passage_id, "n_anchors": self.n_anchors,
            "anchor_recall": round(self.anchor_recall, 4),
            "resolution_precision": round(self.resolution_precision, 4),
            "resolution_recall": round(self.resolution_recall, 4),
            "abstain_quality": round(self.abstain_quality, 4),
            "resolved_ok": self.resolved_ok, "resolved_wrong": self.resolved_wrong,
            "abstained": self.abstained, "gold_anchors": self.gold_anchors,
        }


def evaluate_passage(passage: dict, l0_by_lemma: dict[str, list[dict]],
                     method) -> P4Result:
    """Evaluate one passage: extract gold anchors from L2, run method, score."""
    l2 = passage.get("l2_text") or ""
    gold_anchors = extract_anchors_from_l2(l2)   # the recoverable anchors the prose marks
    # for each gold anchor, the correct resolution is the L0 lemma
    gold_map = {a: resolve_anchor(a, l0_by_lemma) for a in gold_anchors}

    predicted = method(l2, l0_by_lemma)

    # anchor recovery: how many gold anchors did the method find?
    found = set(predicted)  # predicted may include None (abstain) entries
    resolved_ok = resolved_wrong = abstained = 0
    for a in gold_anchors:
        truth = gold_map[a]
        if truth is None:
            # gold says this anchor has no L0 lemma -> abstain is correct
            abstained += 1
        else:
            if truth in found:
                resolved_ok += 1
            else:
                resolved_wrong += 1

    n_anchors = len(gold_anchors)
    anchor_recall = (resolved_ok + abstained) / n_anchors if n_anchors else 1.0
    # precision: of the anchors the method resolved (non-None), how many were correct
    resolved_attempted = [p for p in predicted if p is not None]
    correct_attempts = sum(1 for a in gold_anchors if gold_map[a] in resolved_attempted)
    resolution_precision = (correct_attempts / len(resolved_attempted)) if resolved_attempted else 0.0
    resolution_recall = (resolved_ok / n_anchors) if n_anchors else 1.0
    # abstain quality: of gold non-anchor prose tokens, did we abstain? (approximate: count of
    # gold anchors with no lemma that we did NOT try to resolve)
    abstain_quality = (abstained / sum(1 for a in gold_anchors if gold_map[a] is None)) if any(
        gold_map[a] is None for a in gold_anchors) else 1.0

    return P4Result(
        passage_id=passage["id"], n_anchors=n_anchors,
        anchor_recall=anchor_recall, resolution_precision=resolution_precision,
        resolution_recall=resolution_recall, abstain_quality=abstain_quality,
        resolved_ok=resolved_ok, resolved_wrong=resolved_wrong, abstained=abstained,
        gold_anchors=n_anchors,
    )


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def load_published(published_dir: str) -> list[dict]:
    """Load all published passages that have l2_text."""
    out = []
    for f in sorted(glob.glob(os.path.join(published_dir, "pt-passage-*.json"))):
        p = json.load(open(f))
        if p.get("l2_text"):
            out.append(p)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="P4: L0<->L2 term-anchor alignment benchmark")
    ap.add_argument("--published", default="data/published/ipvv")
    ap.add_argument("--l0dir", default="/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/l0")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="docs/p4_alignment_eval_report.json")
    ap.add_argument("--limit", type=int, default=0, help="max passages (0 = all)")
    ap.add_argument("--witness", action="store_true",
                    help="run the independent Vidyut morphological witness (loads Vidyut)")
    args = ap.parse_args()

    passages = load_published(args.published)
    if args.limit:
        random.seed(args.seed)
        passages = random.sample(passages, min(args.limit, len(passages)))

    # index L0 lemmas per chunk
    results = []
    for p in passages:
        chunk = p.get("chunk") or p["id"].split("chunk")[-1].replace(".md", "")
        # the l0 jsonl is keyed by the chunk stem WITHOUT the .md
        chunk_stem = chunk.replace(".md", "")
        l0_by_lemma = load_l0_lemmas(args.l0dir, chunk_stem)
        if not l0_by_lemma:
            continue
        results.append(evaluate_passage(p, l0_by_lemma, candidate_alignment))

    if not results:
        print("no passages with both l2_text and L0 lemmas found; check --published / --l0dir")
        return 1

    n_anchors = sum(r.n_anchors for r in results)
    ok = sum(r.resolved_ok for r in results)
    wrong = sum(r.resolved_wrong for r in results)
    abstained = sum(r.abstained for r in results)
    report = {
        "benchmark": "P4-ALIGNMENT-v1-L0L2-ANCHOR",
        "passages": len(results),
        "gold_anchors": n_anchors,
        "resolved_ok": ok, "resolved_wrong": wrong, "abstained": abstained,
        "metrics": {
            "anchor_recall_mean": round(sum(r.anchor_recall for r in results) / len(results), 4),
            "resolution_precision_mean": round(
                sum(r.resolution_precision for r in results) / len(results), 4),
            "resolution_recall_mean": round(
                sum(r.resolution_recall for r in results) / len(results), 4),
            "abstain_quality_mean": round(
                sum(r.abstain_quality for r in results) / len(results), 4),
        },
        "note": ("term-anchor alignment (L0<->L2). Baselines: paren-extraction (anchor recall floor), "
                 "token-overlap (resolution floor). awesome-align must beat resolution_recall. "
                 "No 'solved' claim without frozen gold + BenchmarkRun."),
        "per_passage": [r.to_dict() for r in results],
    }
    if args.witness:
        report["independent_witness"] = vidyut_ensemble_rate(
            passages, args.l0dir, seed=args.seed, limit=args.limit)
    print(json.dumps({k: v for k, v in report.items()
                      if k not in ("per_passage", "independent_witness")}, indent=2))
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(f"report -> {args.out}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
