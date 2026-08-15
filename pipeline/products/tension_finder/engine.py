"""products/tension_finder/engine.py — the tension finder (the vision's /find-interesting-tension).

The headline research function from vision-07: instead of finding "the answer," surface WHERE
interpretations diverge — the places papers come from. Embeds the LOGICVID curiosity markers + the
pushing method (hound the text with why, decompose into problem/primitives/presuppositions/tensions),
all on REAL IPVV data + my built engines.

Tension kinds detected (each = a LOGICVID curiosity marker):
  - RIVAL/OBJECTION  : the passage engages an opponent (Buddhist/kṣaṇikavāda/rival) — adversarial
  - LIVE_ISSUE        : "does X explain Y or merely rename it?" (logicdog method)
  - DISTINCTION      : same term, divergent use / scope (logic5 distinction-forensics)
  - TRANSLATION_DIVERGENCE : two passages read a shared term differently
  - DOCTRINAL_SHIFT  : a term's sense changes across period/tradition (terminology trajectory)
  - CRUX             : two positions have a real load-bearing divergence (crux engine)
  - CONTRADICTION    : a C1 uses strong opposition/negation language

Each tension carries: kind · the passage(s) · the concrete quote/why · a score (how interesting, per
the curiosity markers). CPU-only, deterministic, MACHINE_PROPOSED (surfaces possibilities, never
decides truth).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(_ROOT / "pipeline"))

from products._shared import ipvv  # noqa: E402
from products.argument.engine import arguments  # noqa: E402
from products.crux.engine import crux_between  # noqa: E402
from products.comparison.engine import compare_between  # noqa: E402
from products.terminology.engine import sense_trajectory, lemmas  # noqa: E402

# ---- the LOGICVID curiosity markers (the tension taxonomy) ----
RIVAL_WORDS = ["buddhist", "opponent", "objection", "kṣaṇika", "momentar", "rival", "adversary"]
OPPOSITION_WORDS = ["cannot", "not", "reject", "deny", "impossible", "contradict", "refute"]
LIVE_ISSUE_PAT = re.compile(r"(explain|rename|redescribe|merely|just)\b", re.I)
MODAL_STRENGTHEN = re.compile(r"(necessarily|always|universally|in general|must)\b", re.I)
LOCAL_SCOPE = re.compile(r"(in this passage|here|this kārikā|this karika)\b", re.I)


def _c1(p: dict) -> str:
    return ipvv.c1_body(p)


def _find_contradictions() -> list[dict]:
    """Passages with strong opposition/negation language (the adversarial tension)."""
    out = []
    for p in ipvv.passages():
        c1 = _c1(p).lower()
        hits = [w for w in OPPOSITION_WORDS if w in c1]
        rivals = [w for w in RIVAL_WORDS if w in c1]
        if hits or rivals:
            out.append({
                "kind": "CONTRADICTION" if hits else "RIVAL",
                "passage_id": p.get("id"),
                "work_id": p.get("work_id"),
                "opposition_terms": hits[:5],
                "rival_terms": rivals[:5],
                "quote": _c1(p)[:200],
                "score": round(0.5 + 0.1 * (len(hits) + len(rivals)), 2),
            })
    return out


def _find_live_issue() -> list[dict]:
    """The logicdog method: does the passage explain or merely rename? (concept doing work?)"""
    out = []
    for p in ipvv.passages():
        c1 = _c1(p)
        if LIVE_ISSUE_PAT.search(c1):
            out.append({
                "kind": "LIVE_ISSUE",
                "passage_id": p.get("id"),
                "quote": c1[:200],
                "note": "concept may explain or merely rename — the live issue",
                "score": 0.8,
            })
    return out


def _find_distinction() -> list[dict]:
    """logic5 distinction-forensics: a term used with divergent scope/modality across passages."""
    out = []
    from collections import defaultdict
    term_uses = defaultdict(lambda: {"strong": 0, "local": 0, "passages": []})
    terms = ["vimarśa", "prakāśa", "saṃvit", "kula", "śakti", "spanda", "ātmā", "caitanya",
             "pratibhā", "jñāna", "anubhava", "bheda", "abheda", "ahaṃ", "svasthiti"]
    for p in ipvv.passages():
        c1 = _c1(p)
        low = c1.lower()
        for t in terms:
            if t in low:
                term_uses[t]["passages"].append(p.get("id"))
                if MODAL_STRENGTHEN.search(c1):
                    term_uses[t]["strong"] += 1
                if LOCAL_SCOPE.search(c1):
                    term_uses[t]["local"] += 1
    for term, u in term_uses.items():
        if u["strong"] > 0 and u["local"] > 0 and (u["strong"] + u["local"]) >= 2:
            out.append({
                "kind": "DISTINCTION",
                "term": term,
                "strong_uses": u["strong"], "local_uses": u["local"],
                "passages": list(dict.fromkeys(u["passages"]))[:4],
                "note": f"'{term}' is used with both strong (modal) and passage-local scope — "
                        f"distinction-forensics: is it one sense or several?",
                "score": 0.75,
            })
    return out


def _find_doctrinal_shift() -> list[dict]:
    """A term whose sense changes across period/tradition (terminology trajectory)."""
    out = []
    for lemma in lemmas():
        tr = sense_trajectory(lemma)
        senses = {s["sense_id"] for s in tr["trajectory"] if s.get("sense_id")}
        if len(senses) > 1:
            out.append({
                "kind": "DOCTRINAL_SHIFT",
                "term": lemma,
                "senses": sorted(senses),
                "periods": [s["period"] for s in tr["trajectory"]],
                "note": f"'{lemma}' shifts sense across {len(senses)} senses — a doctrinal shift",
                "score": 0.7,
            })
    return out


def _find_cruxes() -> list[dict]:
    """Real load-bearing divergences between positions (crux engine)."""
    out = []
    args = arguments()
    for i in range(min(3, len(args))):
        for j in range(i + 1, min(4, len(args))):
            try:
                cx = crux_between(args[i]["argument_id"], args[j]["argument_id"])
                if cx["crux_count"] > 0:
                    out.append({
                        "kind": "CRUX",
                        "a": cx["position_a"], "b": cx["position_b"],
                        "crux_count": cx["crux_count"],
                        "a_asserts": cx["crux_a_asserts"][:2],
                        "b_asserts": cx["crux_b_asserts"][:2],
                        "note": "two positions diverge on load-bearing premises",
                        "score": round(0.5 + 0.1 * min(cx["crux_count"], 5), 2),
                    })
            except Exception:
                continue
    return out


def find_tensions(kinds: list[str] | None = None, min_score: float = 0.0, limit: int = 20) -> dict:
    """Find interesting tensions across the real IPVV material.

    kinds: subset of the taxonomy; None = all. min_score filters weak tensions.
    """
    collectors = {
        "CONTRADICTION": _find_contradictions,
        "LIVE_ISSUE": _find_live_issue,
        "DISTINCTION": _find_distinction,
        "DOCTRINAL_SHIFT": _find_doctrinal_shift,
        "CRUX": _find_cruxes,
    }
    kinds = kinds or list(collectors.keys())
    all_t = []
    for k in kinds:
        if k in collectors:
            all_t.extend(collectors[k]())
    all_t = [t for t in all_t if t["score"] >= min_score]
    all_t.sort(key=lambda x: -x["score"])
    return {
        "tensions": all_t[:limit],
        "count": len(all_t),
        "kinds_found": sorted({t["kind"] for t in all_t}),
        "note": "MACHINE_PROPOSED tension surface (logicvid curiosity markers on real IPVV) — "
                "surfaces where interpretations diverge, never decides truth",
    }


if __name__ == "__main__":
    import sys as _s
    min_score = float(_s.argv[1]) if len(_s.argv) > 1 else 0.0
    limit = int(_s.argv[2]) if len(_s.argv) > 2 else 20
    print(json.dumps(find_tensions(min_score=min_score, limit=limit), indent=2, ensure_ascii=False))
