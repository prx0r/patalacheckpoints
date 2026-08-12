"""patala_ml/c1metrics.py — turn the C1 human checklist into machine-scored metrics.

The C1-SPEC has 10 human checkboxes. This makes the key ones measurable, so a C1 can be
validated deterministically — which is what reproducibility for any text AND the ML (Vertical
Fidelity, argument extraction) both need.

Metrics (each scored 0-1, with a threshold):
  novelty        does the C1 explain (add words/ideas) vs merely paraphrase L2?
  localness      do its cross-references point to nearby passages, not the whole tradition?
  no_anachronism is it free of banned modern-comparison terms?
  boundary       does it distinguish 'established' from 'stronger conclusion' (honesty)?
  hedge          are uncertainties visible (hedging markers present)?
  term_quality   are technical terms present and non-empty?

A C1 passes when each metric meets its threshold — turning subjective review into scored,
reproducible validation.
"""
from __future__ import annotations

import re

# terms that signal a modern comparison / essay-leak (C1-SPEC §8)
ANACHRONISM_TERMS = [
    "predictive processing", "self-model", "metacognition", "active inference",
    "illusionism", "contemporary idealism", "neuroscience", "nāgārjuna",
    "higher-order represent", "phenomenolog", "nāṇavīra", "solms", "am0",
]
# hedging / uncertainty markers (honesty)
HEDGE_TERMS = ["does not", "not by itself", "may", "might", "possibly", "not certain",
               "remains open", "does not establish", "deferred", "uncertain", "not prove"]
# terms that signal "stronger conclusion" being avoided (boundary honesty)
BOUNDARY_TERMS = ["does not", "not by itself", "alone", "only", "this passage", "locally",
                  "the passage establishes", "is not to say"]


def _words(s: str) -> set[str]:
    return set(re.findall(r"[a-zā-īūṛḷṅñṭḍṇśṣḥ']+", s.lower()))


def novelty(c1_body: str, l2_text: str) -> float:
    """Fraction of C1 content-words NOT in the L2 — explanation adds; paraphrase repeats."""
    c1w, l2w = _words(c1_body), _words(l2_text)
    if not c1w:
        return 0.0
    stop = {"the", "a", "an", "and", "or", "but", "of", "to", "in", "is", "are", "that",
            "this", "it", "as", "for", "on", "with", "by", "not", "be"}
    new = (c1w - l2w) - stop
    return round(len(new) / max(1, len(c1w - stop)), 3)


def no_anachronism(c1_body: str) -> float:
    """1.0 if no banned modern-comparison term; 0.0 if any present."""
    lower = c1_body.lower()
    hits = [t for t in ANACHRONISM_TERMS if t in lower]
    return 0.0 if hits else 1.0


def boundary(c1_body: str, boundary_text: str) -> float:
    """Presence + hedging of the BOUNDARY: does it separate established from stronger?"""
    text = (boundary_text + " " + c1_body).lower()
    hits = sum(1 for t in BOUNDARY_TERMS if t in text)
    # require at least 2 boundary signals (e.g. "does not" + "by itself")
    return min(1.0, hits / 2.0)


def hedge(c1_body: str, boundary_text: str = "") -> float:
    """Are uncertainties visible? For the IPVV genre, honesty lives in the BOUNDARY, not
    sprinkled as 'may/might' in the prose. So hedge looks at BOTH the boundary field (where
    the C1-SPEC puts it) and hedging markers in the body."""
    lower = (boundary_text + " " + c1_body).lower()
    hits = sum(1 for t in HEDGE_TERMS if t in lower)
    return min(1.0, hits / 2.0)  # 2+ markers = full credit


def term_quality(terms: list[str]) -> float:
    """Technical terms present and non-empty."""
    nonempty = [t for t in terms if t and str(t).strip()]
    return min(1.0, len(nonempty) / 3.0)  # 3+ terms = full credit


def localness(related: list[str]) -> float:
    """Cross-references are nearby (V-something) not whole-tradition (IPK is root, ok)."""
    if not related:
        return 0.0
    # local = references a specific passage (V2-X / kX) or the root kārikā
    local = [r for r in related if re.search(r"V[0-9]-?[A-Z]|IPK\s|[0-9]\.[0-9]", str(r))]
    return round(len(local) / len(related), 3)


def score_c1(c1_body: str, l2_text: str, *, terms=None, related=None,
             boundary_text="") -> dict:
    """Score a C1 against the machine metrics. Returns {metric: {score, threshold, pass}}."""
    m = {
        "novelty": (novelty(c1_body, l2_text), 0.15, "explains, not paraphrases"),
        "no_anachronism": (no_anachronism(c1_body), 1.0, "no modern comparison"),
        "boundary": (boundary(c1_body, boundary_text), 0.5, "distinguishes established from stronger"),
        "hedge": (hedge(c1_body, boundary_text), 0.5, "uncertainties visible"),
        "term_quality": (term_quality(terms or []), 0.5, "technical terms present"),
        "localness": (localness(related or []), 0.3, "stays local to the passage"),
    }
    out = {}
    for name, (score, thresh, desc) in m.items():
        out[name] = {"score": round(score, 3), "threshold": thresh, "pass": score >= thresh, "what": desc}
    out["overall"] = round(sum(v["score"] for v in out.values()) / len(out), 3)
    out["passes"] = all(v["pass"] for k, v in out.items() if k != "overall")
    return out
