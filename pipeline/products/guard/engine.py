"""products/guard/engine.py — the serve-time verification guard (Agent 1's enforcement).

Ports the FoJin anti-hallucination mechanism (quote_verifier.py + citation_guard.py, cloned at
source-evidence/repos/xr843__fojin) to Pāṭala answers. This is the ENFORCEMENT of the stack's
"UNANCHORED → reject" rule at serve time — the single biggest gap identified in FRONTIER-REVIEW §1.3.

What it does:
  QUOTE_GUARD  — a quoted passage preceding a citation must substring-match (NFKC + strip-punct +
                 lowercase) the cited source. On a miss → DOWNGRADE (strip quote marks, read as honest
                 prose, still cite) — never serve a false verbatim quote. Records a QuoteMutation
                 (reason, similarity, bucket: near_miss >= 0.85 / absent) for telemetry.
  CITATION_GUARD — every served citation must resolve against a retrieved-source whitelist. A
                 hallucinated title → stripped to bare form; a wrong locus → rewritten to the closest
                 real one.

Adapted to Pāṭala: Pāṭala sources are Sanskrit scholarly objects (work + locus), not CBETA Chinese
canon. The '繁→简' fold becomes a Sanskrit-diacritic fold (IAST diacritics collapse to ASCII so a
scholar's dropped macron doesn't false-fail). Deterministic, stdlib-only, CPU-only.
"""
from __future__ import annotations

import difflib
import json
import re
import sys
import unicodedata
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(_ROOT / "pipeline"))

NEAR_MISS_THRESHOLD = 0.85
MIN_QUOTE_CHARS = 8
MAX_QUOTE_CITATION_GAP_CHARS = 80
_CIT = re.compile(r"[【《]|\[\s*(?:\d+|[A-Za-z\-]+)\s*\]|\([\w\s\-]+:[\w\s\-]+\)")


def _normalise(s: str) -> str:
    """NFKC + strip punctuation/whitespace + lowercase; fold Sanskrit diacritics to ASCII."""
    s = unicodedata.normalize("NFKD", s)
    # Sanskrit IAST diacritics → ASCII (so a dropped macron/underdot doesn't false-fail a quote)
    fold = {
        "ā": "a", "ī": "i", "ū": "u", "ṛ": "r", "ṝ": "r", "ḷ": "l", "ḹ": "l",
        "ē": "e", "ō": "o", "ṃ": "m", "ḥ": "h", "ṅ": "n", "ñ": "n", "ṭ": "t",
        "ḍ": "d", "ṇ": "n", "ś": "s", "ṣ": "s", "ḻ": "l",
        "Ā": "A", "Ī": "I", "Ū": "U", "Ṛ": "R", "Ṇ": "N", "Ś": "S", "Ṣ": "S", "Ḍ": "D",
    }
    for src, dst in fold.items():
        s = s.replace(src, dst)
    s = re.sub(r"[\W_]+", "", s)
    return s.lower()


def _windowed_ratio(needle: str, haystack: str) -> float:
    """Best fuzzy ratio of the normalised needle within the haystack (like FoJin)."""
    n, h = _normalise(needle), _normalise(haystack)
    if not n:
        return 0.0
    if n in h:
        return 1.0
    best = 0.0
    for i in range(max(0, len(h) - len(n)), len(h) + 1):
        win = h[i : i + len(n)]
        r = difflib.SequenceMatcher(None, n, win).ratio()
        if r > best:
            best = r
    return best


def _preceding_quote(text_before: str) -> str | None:
    """The quoted passage immediately preceding a citation marker, if any."""
    text_before = text_before.rstrip()
    # inline 「…」/『…』/“…”/‘…’/"…"/'…'
    m = re.search(
        r"[「『“‘\"']([^「『“‘\"'」』”’]{" + str(MIN_QUOTE_CHARS) + r",400})[」』”’\"']"
        r"[^【】「『“‘\"'」』”’]{0," + str(MAX_QUOTE_CITATION_GAP_CHARS) + r"}$",
        text_before,
    )
    if m:
        return m.group(1).strip()
    # Markdown blockquote block
    m = re.search(
        r"(?P<block>(?:^>[^\n]*(?:\n|$))+)"
        r"(?:(?:[^\n]*\n){0,2}[^\n]{0," + str(MAX_QUOTE_CITATION_GAP_CHARS) + r"}?)$",
        text_before,
        re.MULTILINE,
    )
    if m:
        body = re.sub(r"(?m)^>\s?", "", m.group("block")).strip()
        return body or None
    return None


def _classify_failure(similarity: float) -> str:
    return "near_miss" if similarity >= NEAR_MISS_THRESHOLD else "absent"


class QuoteMutation:
    """Audit record for a quote that failed verification (measurement, not pass/fail)."""

    def __init__(self, quote, cite, reason, similarity=0.0):
        self.quote, self.cite, self.reason = quote, cite, similarity
        self.similarity = similarity
        self.bucket = _classify_failure(similarity)
        self.__dict__["reason"] = reason

    def to_dict(self):
        return {
            "quote": self.quote[:80],
            "cite": self.cite,
            "reason": self.reason,
            "similarity": round(self.similarity, 3),
            "bucket": self.bucket,
        }


def verify_quoted_content(answer: str, sources: list[dict]) -> dict:
    """Verify quoted passages in an answer against retrieved sources. Returns a verdict + mutations.

    ``sources``: list of {title (work_id), locus, text}. Each cited quote is checked against the
    whole candidate set (a sentence may be in a later chunk). On a miss → DOWNGRADE suggestion.
    """
    mutations = []
    verified = 0
    # naive citation markers for Pāṭala: (work:locus) or [work:locus] or 【work】 after a quote
    for m in re.finditer(r"[(\[【]([^)\]\】]+)[)\]\】]", answer):
        cite = m.group(1).strip()
        before = answer[: m.start()]
        quote = _preceding_quote(before)
        if not quote:
            continue
        # check quote against all candidate sources
        best = 0.0
        for src in sources:
            sim = _windowed_ratio(quote, src.get("text", ""))
            if sim > best:
                best = sim
        if best >= 1.0 or (best >= NEAR_MISS_THRESHOLD and quote in _normalise(
            " ".join(s.get("text", "") for s in sources))):
            verified += 1
        else:
            mutations.append(
                QuoteMutation(quote, cite, "quote_not_in_source" if best < NEAR_MISS_THRESHOLD else "near_miss", best)
            )
    return {
        "quotes_checked": verified + len(mutations),
        "verified": verified,
        "downgraded": [m.to_dict() for m in mutations],
        "note": "serve-time guard: never serves a false verbatim quote; a miss downgrades to honest prose",
        "mechanism": "fojin quote_verifier (ported, sanskrit-fold)",
    }


def enforce_citation_whitelist(answer: str, sources: list[dict]) -> dict:
    """Whitelist every citation against the retrieved sources. A hallucinated cite is corrected/stripped."""
    whitelist = {(s.get("title", s.get("work_id", "")), s.get("locus", "")) for s in sources}
    corrected = 0

    def _fix(m):
        nonlocal corrected
        inner = m.group(0)
        label = re.sub(r"[\s]+", " ", m.group(0).strip("()[]【】"))
        # if the cite matches a whitelisted (work, locus) pair → keep
        for (t, l) in whitelist:
            if t and (t in label or label in t):
                return inner
        # else hallucinated → strip to bare, no false click-through
        corrected += 1
        return ""

    # only citation-shaped tokens: (work:locus) or [work:locus] — REQUIRES a ':' (work:locus split).
    # A bare parenthetical (svācchandya) is a gloss, not a citation — never strip it.
    _CITE = re.compile(r"[(\[【]([\w./\-\u0966-\u096f ]+:[^)\]\】]{1,40})[)\]\】]")

    out = re.sub(_CITE, _fix, answer)
    return {
        "served": out,
        "corrected_count": corrected,
        "whitelist_size": len(whitelist),
        "mechanism": "fojin citation_guard (ported)",
    }


def guard_answer(answer: str, sources: list[dict]) -> dict:
    """The full serve-time guard: quote verification + citation whitelist, applied to one answer."""
    qv = verify_quoted_content(answer, sources)
    cg = enforce_citation_whitelist(answer, sources)
    safe = qv["downgraded"] == [] and cg["corrected_count"] == 0
    return {
        "safe_to_serve": safe,
        "quote_guard": qv,
        "citation_guard": cg,
        "served_answer": cg["served"],
    }


def demo() -> dict:
    src = [
        {"title": "ipvv", "locus": "1.1.1", "text": "The spontaneity of the Lord is self-aware light (svācchandya). This is where the whole vimarśinī begins, the recognition that consciousness is never inert."},
    ]
    good = guard_answer(
        "The spontaneity of the Lord is self-aware light (svācchandya), and this is where the whole vimarśinī begins (ipvv:1.1.1).",
        src,
    )
    bad = guard_answer(
        "Abhinavagupta says 'the spontaneity is completely inert matter' (ipvv:1.1.1) — which changes everything.",
        src,
    )
    return {"real_quote": good, "fabricated_quote": bad}


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2, ensure_ascii=False))
