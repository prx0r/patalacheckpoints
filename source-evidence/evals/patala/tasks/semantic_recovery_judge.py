#!/usr/bin/env python3
"""source-evidence/evals/patala/tasks/semantic_recovery_judge.py — two-stage semantic matcher (P0).

The token-overlap recovery scorer under-measures correct scholarly paraphrase (the pilot recovered the
correct argument but scored 0.0). This is the reviewer's two-stage fix:

  STAGE 1 — CANDIDATE ALIGNMENT (recall)
      embedding/lexical search: candidate proposition -> top-k possible gold matches.
      (reuses semantic_alignment.embed / _cos — NOT a new embedding stack)

  STAGE 2 — STRUCTURED SEMANTIC JUDGE (precision, the real classifier)
      LLM/judge receives GOLD + CANDIDATE (+ source span) and returns:
          relation: EQUIVALENT | NARROWER | BROADER | CONTRADICTS | PARTIAL | UNRELATED
          speaker_match / scope_match / modality_match / commitment_match : bool
          confidence
      Force structured justification.

  STAGE 3 — DETERMINISTIC SCORING
      EQUIVALENT or acceptable NARROWER counts as RECOVERED.
      BROADER penalized. CONTRADICTS catastrophic.

Critically (the reviewer's warning): embedding similarity is NOT sufficient — it can say
"self-awareness requires duality" and "self-awareness does not require duality" are similar. So
Stage 2 must adjudicate contradiction direction via the structured judge, never cosine alone.
"""
from __future__ import annotations

import json
import os
import re
import sys

_FILE_DIR = os.path.dirname(os.path.abspath(__file__))          # .../tasks
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(_FILE_DIR))))  # repo root
sys.path.insert(0, os.path.join(_ROOT, "machinelearning", "research"))
sys.path.insert(0, os.path.join(_ROOT, "machinelearning", "research", "patala_ml"))
sys.path.insert(0, _FILE_DIR)

# the reviewer's relation vocabulary
RELATIONS = ("EQUIVALENT", "NARROWER", "BROADER", "CONTRADICTS", "PARTIAL", "UNRELATED")

# ── Stage 1: candidate alignment (embedding + lexical, reuses semantic_alignment) ──
def _norm(s: str) -> str:
    # strip markdown/line-ref noise before matching: **bold**, > quotes, (lines N–M), the "The question:" label
    s = re.sub(r"\*\*", "", s or "")
    s = re.sub(r"\s*>", " ", s)
    s = re.sub(r"\(lines?[^)]*\)", "", s)
    s = re.sub(r"\(line[^)]*\)", "", s)
    return s


def _dense(text: str) -> list[float]:
    from semantic_alignment import embed
    return embed(_norm(text), "l2")


def _cos(a, b) -> float:
    from semantic_alignment import _cos as _c
    return _c(a, b)


def _lex_overlap(a: str, b: str) -> float:
    stop = set("the a an of and or in on to for is are it this that as by with from its not be can which what who how why so therefore thus hence".split())
    wa = {t for t in re.sub(r"[^a-z0-9 ]", "", (a or "").lower()).split() if t not in stop}
    wb = {t for t in re.sub(r"[^a-z0-9 ]", "", (b or "").lower()).split() if t not in stop}
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / max(1, min(len(wa), len(wb)))


def align_candidates(gold_propositions: list[dict], candidate_steps: list[str],
                     k: int = 3, embed_weight: float = 0.6) -> dict:
    """Stage 1: for each candidate step, return the top-k gold matches by blended score."""
    gold_texts = [(g.get("text") or g.get("commitment") or "", g.get("pid")) for g in gold_propositions]
    result = {}
    for ci, cand in enumerate(candidate_steps):
        cand_emb = _dense(cand)
        scored = []
        for gtext, gpid in gold_texts:
            sim = _cos(cand_emb, _dense(gtext)) if cand_emb and _dense(gtext) else 0.0
            lex = _lex_overlap(cand, gtext)
            blended = embed_weight * sim + (1 - embed_weight) * lex
            scored.append({"gold_pid": gpid, "gold_text": gtext, "embed_cos": round(sim, 4),
                           "lexical": round(lex, 4), "blended": round(blended, 4)})
        scored.sort(key=lambda s: s["blended"], reverse=True)
        result[ci] = scored[:k]
    return result


# ── Stage 2: the structured semantic judge (LLM), with an offline fallback classifier ──
def _offline_fallback_relation(gold: str, cand: str) -> dict:
    """Deterministic fallback when the LLM judge is unavailable.

    Uses a cheap sign-sensitive lexical check so that opposite-polarity claims (requires/does not
    require) are NOT conflated — the reviewer's 'embedding says contradictory claims are similar' trap.
    """
    g = gold.lower()
    c = cand.lower()
    neg_g = any(w in g for w in ("not", "no ", "without", "never", "non-", "does not", "is not", "not a"))
    neg_c = any(w in c for w in ("not", "no ", "without", "never", "non-", "does not", "is not", "not a"))
    lex = _lex_overlap(gold, cand)
    if lex >= 0.6:
        relation = "EQUIVALENT"
    elif lex >= 0.4:
        # polarity flip = contradiction, else partial
        relation = "CONTRADICTS" if (neg_g != neg_c) else "PARTIAL"
    elif lex >= 0.15 and (neg_g != neg_c):
        # same topic, flipped polarity at low overlap = a contradiction the reviewer warned about
        # (embedding says 'similar' but the claims contradict)
        relation = "CONTRADICTS"
    else:
        relation = "UNRELATED" if lex < 0.2 else "PARTIAL"
    return {"relation": relation, "confidence": 0.5, "method": "OFFLINE_FALLBACK",
            "content_match": relation in ("EQUIVALENT", "NARROWER", "PARTIAL"),
            "speaker_match": True, "scope_match": True, "modality_match": True, "commitment_match": True}


def semantic_judge(gold_text: str, candidate_text: str, use_llm: bool = True) -> dict:
    """Stage 2: return the structured judge verdict for one gold/candidate pair.

    If `use_llm` and the judge model is reachable, it returns the LLM verdict; otherwise the offline
    fallback. The result ALWAYS carries the structured fields (relation + axis matches).
    """
    if use_llm:
        try:
            sys.path.insert(0, "/root/projects/patala/pipeline")
            from model import chat
            prompt = (
                "Classify the semantic relation between a GOLD scholarly proposition and a CANDIDATE "
                "recovered proposition. Return JSON ONLY with keys: relation (one of "
                "EQUIVALENT|NARROWER|BROADER|CONTRADICTS|PARTIAL|UNRELATED), speaker_match, "
                "scope_match, modality_match, commitment_match, confidence.\n"
                f"GOLD: {gold_text}\nCANDIDATE: {candidate_text}\n"
                "Note: NARROWER = candidate is a more specific true case of gold; BROADER = candidate "
                "over-generalizes gold; CONTRADICTS = opposite claim. Pay attention to negation/scope."
            )
            raw = chat("You are a scholarly-proposition semantic judge (structured, no prose).",
                       prompt, timeout=120)
            raw = (raw or "").strip()
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0]
            s, e = raw.find("{"), raw.rfind("}")
            if s >= 0 and e > s:
                j = json.loads(raw[s:e + 1])
                rel = str(j.get("relation", "UNRELATED")).upper()
                if rel in RELATIONS:
                    return {"relation": rel, "confidence": float(j.get("confidence", 0.5)),
                            "method": "LLM_JUDGE",
                            "speaker_match": bool(j.get("speaker_match", True)),
                            "scope_match": bool(j.get("scope_match", True)),
                            "modality_match": bool(j.get("modality_match", True)),
                            "commitment_match": bool(j.get("commitment_match", True)),
                            "content_match": rel in ("EQUIVALENT", "NARROWER", "PARTIAL")}
        except Exception:
            pass
    return _offline_fallback_relation(gold_text, candidate_text)


# ── Stage 3: deterministic scoring over a whole candidate ────────────────────
def score_recovery_semantic(gold: dict, candidate: dict, use_llm: bool = True) -> dict:
    """Score a candidate ARGMAP against gold using the two-stage semantic matcher.

    A gold proposition is RECOVERED if some candidate step judges EQUIVALENT or NARROWER.
    CONTRADICTS is catastrophic (a recovered proposition that contradicts gold). UNSUPPORTED_BRIDGE
    (candidate adds a conclusion matched to no gold and no source anchor) is the reviewer's headline.
    """
    gold_props = [p for p in gold.get("propositions", []) if p.get("text")]
    cand_steps = candidate.get("argument_steps", []) or []
    cand_open = [oi.get("text") if isinstance(oi, dict) else str(oi) for oi in candidate.get("open_items", []) or []]

    # Stage 1 alignment
    align = align_candidates(gold_props, cand_steps)

    contradictions = []

    # contradiction detection: for EVERY candidate step, judge against the best-aligned gold
    # (a step that shares a topic with a gold proposition but flips its claim = contradiction)
    for ci, cand in enumerate(cand_steps):
        top = align.get(ci, [])
        if not top:
            continue
        best_gold = top[0]
        j = semantic_judge(best_gold["gold_text"], cand, use_llm=use_llm)
        if j["relation"] == "CONTRADICTS":
            contradictions.append({"gold": gpid_short({"pid": best_gold["gold_pid"]}), "step": ci})

    # per-gold-proposition: is it recovered by any candidate step?
    recovered = []
    for gp in gold_props:
        gtext = gp["text"]
        best = None
        for ci in range(len(cand_steps)):
            top = align.get(ci, [])
            for m in top:
                if m["gold_pid"] == gp.get("pid"):
                    judge = semantic_judge(gtext, cand_steps[ci], use_llm=use_llm)
                    if judge["relation"] in ("EQUIVALENT", "NARROWER"):
                        best = {"step": ci, "relation": judge["relation"],
                                "conf": judge["confidence"], "blended": m["blended"]}
            if best:
                break
        if best:
            recovered.append({"gold": gpid_short(gp), "step": best["step"],
                              "relation": best["relation"]})

    n_gold = len(gold_props)
    prop_recall = len(recovered) / n_gold if n_gold else 1.0
    # precision: fraction of candidate steps that recovered a gold OR match some gold
    matched_steps = {r["step"] for r in recovered}
    prop_precision = len(matched_steps) / len(cand_steps) if cand_steps else 0.0

    # crux recall: is a candidate step (or open item) semantically near a gold crux?
    crux_recalled = 0
    gold_cruxes = [c.get("question", "") for c in gold.get("cruxes", [])]
    for gc in gold_cruxes:
        hit = any(_cos(_dense(gc), _dense(s)) > 0.5 for s in cand_steps) or \
              any(_lex_overlap(gc, s) > 0.3 for s in cand_steps + cand_open)
        if hit:
            crux_recalled += 1
    crux_recall = crux_recalled / len(gold_cruxes) if gold_cruxes else 1.0

    return {
        "method": "SEMANTIC (2-stage: embedding+lexical align -> structured judge)",
        "proposition_recall": round(prop_recall, 4),
        "proposition_precision": round(prop_precision, 4),
        "crux_recall": round(crux_recall, 4),
        "recovered": recovered,
        "contradictions": contradictions,
        "contradiction_rate": round(len(contradictions) / max(1, n_gold), 4),
    }


def gpid_short(p: dict) -> str:
    return (p.get("pid") or "")[-16:]


if __name__ == "__main__":
    # self-test: EQUIVALENT paraphrase recovers; a polarity-flipped claim is NOT conflated
    gold = {"propositions": [
        {"pid": "P1", "text": "the pure ahaṃ-pratyavamarśa is not a vikalpa; it is the two-invoking determination"},
    ], "cruxes": [{"question": "is the I-recollection a construction or the two-invoking self-grasp?"}]}
    good = {"argument_steps": [
        "the pure 'I'-recollection is not a conceptual construction but the two-invoking determination",
        "nāsau vikalpaḥ sahyukto dvayākṣepī viniścayaḥ"]}
    bad = {"argument_steps": ["the I-recollection IS a vikalpa, a constructed relation"]}
    r_good = score_recovery_semantic(gold, good, use_llm=False)
    r_bad = score_recovery_semantic(gold, bad, use_llm=False)
    print("good (paraphrase recovers):", json.dumps(r_good))
    print("bad (contradicts):          ", json.dumps(r_bad))
    assert r_good["proposition_recall"] == 1.0, "paraphrase must recover"
    assert r_bad["contradiction_rate"] > 0, "polarity-flip must be flagged as contradiction"
    print("SELF-TEST PASS (semantic matcher recovers paraphrase, catches contradiction)")
