#!/usr/bin/env python3
"""verify_l0_ensemble.py — the P2 ensemble validation (Vidyut × Heritage).

An INDEPENDENT INSTRUMENT CALIBRATION experiment, NOT "another parser in the stack."
Question: how trustworthy is the morphological witness, and what does disagreement mean?

Input sets (from verify_l0_p2.py per-record output):
  A. all Vidyut CONFLICT
  B. all Vidyut UNANALYZED
  C. ~N Vidyut CONFIRMED        (stratified control)
  D. ~N Vidyut AMBIGUOUS_SUPPORTED (stratified control)

For each sampled record, run Heritage (independent witness) and classify:
  heritage_state:  SUPPORTS_L0 | CONFLICTS | NO_ANALYSIS | TOOL_ERROR
  agreement_class: V+/H+ · V-/H+ · V+/H- · V-/H- · V?/H? ...
  relation_class:  EXACT_LEMMA_AGREEMENT | STEM_EQUIVALENT | COMPOUND_SEGMENTATION_DIFFERENCE
                   | MORPHOLOGICAL_FEATURE_DIFFERENCE | NO_ANALYSIS | TOOL_ERROR

Artifacts:
  p2_ensemble_report.json    the summary + benchmark-style rates
  p2_ensemble_confusion.csv  the Vidyut×Heritage confusion matrix
  p2_disagreements.jsonl     per-record rows (all sampled)
  p2_review_queue.jsonl      high-value disagreements for manual review
  P2-ENSEMBLE.md             the human-readable writeup (written by the caller or auto)

Honest status labels (never PROVED):
  SUPPORTED_BY_ENSEMBLE · SUPPORTED_BY_SINGLE_WITNESS · CONFLICTING_WITNESSES · UNANALYZED

Usage:
  python3 pipeline/verify_l0_ensemble.py --records <p2_records.jsonl> --out <dir>
      [--control-n 500] [--limit 4000] [--sample-other] [--seed 42]
"""
from __future__ import annotations
import argparse
import json
import random
import sys
from collections import Counter
from pathlib import Path

# --- Heritage client (reuse the hardened client from the old engine) ------- #
_HERITAGE = None


def _get_heritage():
    global _HERITAGE
    if _HERITAGE is not None:
        return _HERITAGE
    sys.path.insert(0, "/mnt/HC_Volume_106427611/sanskritree/src")
    from sanskritree.integrations.heritage_client import HeritageClient
    _HERITAGE = HeritageClient(timeout=60, max_attempts=2)
    return _HERITAGE


def heritage_analyze(surface: str) -> dict:
    """Run Heritage over a surface IAST. Returns {state, roots, analyses, error}."""
    from vidyut.lipi import transliterate, Scheme
    try:
        deva = transliterate(surface.replace("\u1e41", "\u1e43"), Scheme.Iast, Scheme.Devanagari)
    except Exception as e:
        return {"state": "TOOL_ERROR", "roots": [], "analyses": [], "error": f"translit: {e}"}
    h = _get_heritage()
    result = h.analyze(deva, surface)
    if result.status.value != "SUCCESS" or not result.words:
        return {"state": "NO_ANALYSIS" if result.status.value != "TIMEOUT" else "TOOL_ERROR",
                "roots": [], "analyses": [], "error": result.status.value}
    return {"state": "SUCCESS", "roots": result.words, "analyses": result.words,
            "error": None}


def heritage_classify(surface: str, our_lemma: str) -> tuple[str, list]:
    """Classify Heritage's analysis relative to our L0 lemma.

    Returns (heritage_state, roots).
      SUPPORTS_L0  Heritage roots match our lemma (exact or stem-equivalent)
      CONFLICTS    Heritage analyzes but not as our lemma
      NO_ANALYSIS  Heritage returns nothing
      TOOL_ERROR   tool/transliteration failure
    """
    r = heritage_analyze(surface)
    if r["state"] == "NO_ANALYSIS":
        return "NO_ANALYSIS", []
    if r["state"] == "TOOL_ERROR":
        return "TOOL_ERROR", []
    roots = r["roots"]
    if not our_lemma:
        return "NO_ANALYSIS", roots
    # compare Heritage Devanagari roots against our IAST lemma via transliteration
    from vidyut.lipi import transliterate, Scheme
    try:
        our_deva = transliterate(our_lemma.replace("\u1e41", "\u1e43"), Scheme.Iast, Scheme.Devanagari)
    except Exception:
        our_deva = our_lemma
    norm_our = our_deva.replace(" ", "").replace("\u200b", "")
    matched = False
    for root in roots:
        nr = root.replace(" ", "").replace("\u200b", "")
        if nr == norm_our or norm_our.startswith(nr) or nr.startswith(norm_our):
            matched = True
            break
        # stem-equivalent: Heritage root is a stem of our inflected surface
        # (e.g. our surface saṃvedanasya → Heritage root saṃvedana)
    if matched:
        return "SUPPORTS_L0", roots
    return "CONFLICTS", roots


def relation_class(vidyut_state: str, heritage_state: str, vidyut_analyses, heritage_roots):
    """Classify the relationship (the disagreement taxonomy, normalized)."""
    if heritage_state == "TOOL_ERROR":
        return "TOOL_ERROR"
    if heritage_state == "NO_ANALYSIS":
        return "NO_ANALYSIS" if vidyut_state == "UNANALYZED" else "VIDYUT_ONLY_ANALYSIS"
    if heritage_state == "SUPPORTS_L0" and vidyut_state == "CONFIRMED":
        return "EXACT_LEMMA_AGREEMENT"
    if heritage_state == "SUPPORTS_L0" and vidyut_state == "AMBIGUOUS_SUPPORTED":
        return "STEM_EQUIVALENT"
    if vidyut_state == "CONFLICT" and heritage_state == "SUPPORTS_L0":
        return "VIDYUT_REPRESENTATION_MISMATCH"
    if vidyut_state == "CONFLICT" and heritage_state == "CONFLICTS":
        return "DOUBLE_CONFLICT"
    if vidyut_state in ("CONFIRMED", "AMBIGUOUS_SUPPORTED") and heritage_state == "CONFLICTS":
        return "HERITAGE_DISAGREES_WITH_L0"
    if vidyut_state == "UNANALYZED" and heritage_state == "SUPPORTS_L0":
        return "VIDYUT_COVERAGE_GAP"
    return "OTHER"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", required=True, help="p2_records.jsonl from verify_l0_p2.py")
    ap.add_argument("--out", required=True, help="output dir for ensemble artifacts")
    ap.add_argument("--control-n", type=int, default=500, help="control sample size per supported class")
    ap.add_argument("--limit", type=int, default=0, help="0=all CONFLICT+UNANALYZED; else cap")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    random.seed(args.seed)

    # load per-record rows
    rows = [json.loads(l) for l in open(args.records, encoding="utf-8")]
    by_state = {}
    for r in rows:
        by_state.setdefault(r["vidyut_state"], []).append(r)

    # build the input sets
    conflict = by_state.get("CONFLICT", [])
    unanalyzed = by_state.get("UNANALYZED", [])
    confirmed = by_state.get("CONFIRMED", [])
    ambig = by_state.get("AMBIGUOUS_SUPPORTED", [])

    if args.limit:
        conflict = conflict[: args.limit]
        unanalyzed = unanalyzed[: args.limit]
    ctrl_conf = random.sample(confirmed, min(args.control_n, len(confirmed)))
    ctrl_amb = random.sample(ambig, min(args.control_n, len(ambig)))

    input_sets = {"CONFLICT": conflict, "UNANALYZED": unanalyzed,
                  "CTRL_CONFIRMED": ctrl_conf, "CTRL_AMBIGUOUS_SUPPORTED": ctrl_amb}
    print(f"input sizes: { {k: len(v) for k, v in input_sets.items()} }")

    all_rows = []
    review_queue = []
    confusion = Counter()
    relation_counts = Counter()

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    # stream output incrementally so a partial run is still useful
    fh_disc = open(outdir / "p2_disagreements.jsonl", "w", encoding="utf-8")
    fh_queue = open(outdir / "p2_review_queue.jsonl", "w", encoding="utf-8")
    processed = 0

    for set_name, records in input_sets.items():
        for r in records:
            surface = r.get("surface", "")
            if not surface:
                continue
            vidyut_state = r["vidyut_state"]
            heritage_state, hroots = heritage_classify(surface, r.get("lemma_iast", surface))
            rel = relation_class(vidyut_state, heritage_state,
                                 r.get("vidyut_analyses", []), hroots)
            # agreement_class: the V/H sign taxonomy
            v_sign = "+" if vidyut_state in ("CONFIRMED", "AMBIGUOUS_SUPPORTED") else (
                "-" if vidyut_state == "CONFLICT" else "?")
            h_sign = "+" if heritage_state == "SUPPORTS_L0" else (
                "-" if heritage_state == "CONFLICTS" else "?")
            agreement = f"V{v_sign}/H{h_sign}"
            row = {
                "l0_id": r.get("l0_id"), "chunk_id": r.get("chunk_id"),
                "surface": surface, "lemma_iast": r.get("lemma_iast"),
                "vidyut_state": vidyut_state, "vidyut_analyses": r.get("vidyut_analyses"),
                "heritage_state": heritage_state, "heritage_roots": hroots,
                "agreement_class": agreement, "relation_class": rel,
                "input_set": set_name,
            }
            all_rows.append(row)
            confusion[agreement] += 1
            relation_counts[rel] += 1
            fh_disc.write(json.dumps(row, ensure_ascii=False) + "\n")
            fh_disc.flush()
            # review queue: the most valuable cells
            if rel in ("DOUBLE_CONFLICT", "HERITAGE_DISAGREES_WITH_L0",
                       "VIDYUT_REPRESENTATION_MISMATCH"):
                review_queue.append(row)
                fh_queue.write(json.dumps(row, ensure_ascii=False) + "\n")
                fh_queue.flush()
            processed += 1
            if processed % 50 == 0:
                print(f"  processed {processed}...", flush=True)
    fh_disc.close()
    fh_queue.close()

    # benchmark-style summary rates
    total_sampled = len(all_rows)
    ctrl = [r for r in all_rows if r["input_set"].startswith("CTRL")]
    conflict_rows = [r for r in all_rows if r["input_set"] == "CONFLICT"]
    unan_rows = [r for r in all_rows if r["input_set"] == "UNANALYZED"]
    ctrl_agree = sum(1 for r in ctrl if r["agreement_class"].endswith("+"))
    conflict_resolved = sum(1 for r in conflict_rows
                            if r["relation_class"] in ("VIDYUT_REPRESENTATION_MISMATCH",
                                                       "EXACT_LEMMA_AGREEMENT"))
    double_conflict = sum(1 for r in conflict_rows if r["relation_class"] == "DOUBLE_CONFLICT")
    double_unanal = sum(1 for r in all_rows if r["agreement_class"] == "V?/H?")
    tool_err = sum(1 for r in all_rows if r["relation_class"] == "TOOL_ERROR")

    summary = {
        "input_sizes": {k: len(v) for k, v in input_sets.items()},
        "confusion_matrix": dict(confusion),
        "relation_classification": dict(relation_counts),
        "rates": {
            "control_agreement_rate": round(ctrl_agree / max(len(ctrl), 1), 4),
            "conflict_resolution_rate": round(conflict_resolved / max(len(conflict_rows), 1), 4),
            "double_conflict_rate": round(double_conflict / max(len(conflict_rows), 1), 4),
            "double_unanalyzed_rate": round(double_unanal / max(total_sampled, 1), 4),
            "tool_error_rate": round(tool_err / max(total_sampled, 1), 4),
        },
    }

    # emit artifacts
    (outdir / "p2_ensemble_report.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    with open(outdir / "p2_ensemble_confusion.csv", "w", encoding="utf-8") as fh:
        fh.write("agreement_class,count\n")
        for k, v in confusion.most_common():
            fh.write(f"{k},{v}\n")
    with open(outdir / "p2_disagreements.jsonl", "w", encoding="utf-8") as fh:
        for r in all_rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(outdir / "p2_review_queue.jsonl", "w", encoding="utf-8") as fh:
        for r in review_queue:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    print("\n=== P2 ENSEMBLE RESULT ===")
    print(f"sampled: {total_sampled}")
    print("confusion matrix (V/H sign):")
    for k, v in confusion.most_common():
        print(f"  {k:8s} {v}")
    print("\nrelation classification:")
    for k, v in relation_counts.most_common():
        print(f"  {k:35s} {v}")
    print("\nrates:", json.dumps(summary["rates"], indent=1))
    print(f"\nartifacts written to {outdir}  (review queue: {len(review_queue)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
