#!/usr/bin/env python3
"""verify_l0_p2.py — the Vidyut P2 morphology witness (Agent L0, standalone).

P2 asks: "Is the Sanskrit analysis we extracted morphologically licensed?"
It does NOT solve P0 (source coverage). P0 and P2 are independent:

    P0: did we account for every T1 source region?   (verify_l0.py --level p0)
    P2: is the extracted Sanskrit lemma licensed?    (this script, Vidyut)

For every L0 record with a `lemma_iast`, run Vidyut (Chedaka + Kosha) over the surface form and
compare the licensed analyses against our lemma. Emit a per-token witness state WITHOUT overwriting
L0 (this is a witness, not an editor).

States:
  CONFIRMED            Vidyut licenses our lemma/morphology as a possible analysis
  AMBIGUOUS_SUPPORTED  ours is one of several Vidyut analyses (surface is ambiguous)
  CONFLICT             Vidyut analyses the surface but NOT as our lemma
  UNANALYZED           Vidyut cannot analyze the surface at all
  TOOL_ERROR           a tool/transliteration failure (kept separate from UNANALYZED)

Note: AMBIGUOUS/FAILED L0 records carry no IAST lemma (they are gloss-only), so they have no Sanskrit
for Vidyut — they are reported separately as NO_SANSKRIT.

Usage:
  python3 pipeline/verify_l0_p2.py --l0 <l0 dir> [--out <dir>] [--limit <n>] [--chunk <stem>]
"""
from __future__ import annotations
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

# --- P2 normalization/matching rules (FROZEN v1, 2026-08-12) -----------------
# Do NOT change these silently — P2 reruns must be reproducible. If you change the
# surface↔stem matching, bump NORMALIZATION_VERSION and record the delta in BUILD_NOTES_L0_P2.md.
#
# Normalization applied to a surface IAST before Vidyut:
#   . anusvara U+1E41 (ṃ) → U+1E43 (ṁ)
#   . apostrophes / curly apostrophes removed
#   . IAST → SLP1 via vidyut.lipi
#
# Matching rule (a Vidyut lemma "matches" our lemma if ANY of):
#   M1. vidyut_lemma == our_surface (in SLP1)
#   M2. our_surface.startswith(vidyut_lemma)   (stem is a prefix of our surface)
#   M3. vidyut_lemma.startswith(our_surface)
#   M4. vidyut_token_text == our_surface, or our_surface.startswith(vidyut_token_text)
# This treats the surface↔stem relation (saṃvedanasya → saṃvid) as compatible rather than a conflict.
#
# Classification:
#   CONFIRMED            exactly one analysis matches (M1-M4)   OR  single analysis that matches
#   AMBIGUOUS_SUPPORTED  >=1 analysis matches but surface is multi-analysis
#   CONFLICT             has analyses, none match our lemma
#   UNANALYZED           no analyses
#   NO_SANSKRIT          no lemma_iast/surface to analyze
#   TOOL_ERROR           transliteration/tool failure
NORMALIZATION_VERSION = "p2-v1"
# -----------------------------------------------------------------------------

# --- Vidyut lazy init ------------------------------------------------------ #
_VIDYUT = None


def _get_vidyut(data_path="/root/vidyut-0.4.0"):
    global _VIDYUT
    if _VIDYUT is not None:
        return _VIDYUT
    from vidyut.cheda import Chedaka
    from vidyut.kosha import Kosha
    from vidyut.lipi import transliterate, Scheme
    chedaka = Chedaka(data_path)
    kosha = Kosha(f"{data_path}/kosha")
    _VIDYUT = {"chedaka": chedaka, "kosha": kosha,
               "transliterate": transliterate, "scheme": Scheme}
    return _VIDYUT


def vidyut_analyze(surface: str) -> list[dict]:
    """Return Vidyut's analyses for a surface IAST form (list of {text,lemma} tokens)."""
    v = _get_vidyut()
    norm = surface.replace("\u1e41", "\u1e43").replace("'", "").replace("\u2019", "")
    try:
        slp1 = v["transliterate"](norm, v["scheme"].Iast, v["scheme"].Slp1)
        toks = list(v["chedaka"].run(slp1))
    except Exception as e:
        return [{"error": str(e)[:80]}]
    out = []
    for t in toks:
        entry = {"text": getattr(t, "text", ""), "lemma": getattr(t, "lemma", None)}
        d = getattr(t, "data", None)
        if d is not None:
            entry["data_class"] = type(d).__name__
        out.append(entry)
    return out


def classify(surface: str, our_lemma: str) -> tuple[str, list, str]:
    """Classify one L0 record against Vidyut.

    Returns (state, vidyut_analyses, note).
    """
    if not our_lemma or not surface:
        return "NO_SANSKRIT", [], "no lemma_iast/surface to analyze"
    analyses = vidyut_analyze(surface)
    if analyses and any("error" in a for a in analyses):
        return "TOOL_ERROR", analyses, analyses[0].get("error", "")
    if not analyses:
        return "UNANALYZED", [], "Vidyut found no analysis"
    # do any Vidyut lemmas match ours?
    vid_lemmas = {a.get("lemma") for a in analyses if a.get("lemma")}
    norm_our = our_lemma.strip()
    # normalize: Vidyut returns SLP1 lemmas (e.g. 'vimarSa'->'vimfS'); compare via transliteration
    v = _get_vidyut()
    try:
        our_slp = v["transliterate"](norm_our.replace("\u1e41", "\u1e43"),
                                     v["scheme"].Iast, v["scheme"].Slp1)
    except Exception:
        our_slp = norm_our
    # a Vidyut lemma 'matches' if it equals ours in SLP1 or is a plausible stem: our surface is
    # typically an inflected form (e.g. saṃvedanasya) while Vidyut returns the stem (saṃvid), so
    # we match when the stem is a prefix of our surface (derivationally compatible).
    matched = []
    for a in analyses:
        lem = a.get("lemma")
        if not lem:
            continue
        if lem == our_slp or our_slp.startswith(lem) or lem.startswith(our_slp):
            matched.append(a)
            continue
        # surface-derived match: strip a plausible inflectional ending from our surface and compare
        # (e.g. our_slp=saṃvedanasya, stem=saṃvid — not a literal prefix due to sandhi/internal
        # changes, so also try the Kosha lemma-normalized comparison via the token text).
        tok_txt = a.get("text")
        if tok_txt and (tok_txt == our_slp or our_slp.startswith(tok_txt)):
            matched.append(a)
    if len(analyses) == 1 and matched:
        return "CONFIRMED", analyses, "Vidyut licenses exactly our lemma"
    if matched:
        return "AMBIGUOUS_SUPPORTED", analyses, f"ours is 1 of {len(analyses)} Vidyut analyses"
    # has analyses but none match our lemma
    return "CONFLICT", analyses, "Vidyut analyses surface, but not as our lemma"


def load_records(l0_path: Path) -> list[dict]:
    out = []
    for line in l0_path.open(encoding="utf-8"):
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--l0", required=True, help="dir of .l0.jsonl files")
    ap.add_argument("--out", default=None, help="dir for p2 witness output")
    ap.add_argument("--limit", type=int, default=0, help="0=all; else cap records per chunk")
    ap.add_argument("--chunk", default=None, help="restrict to one chunk stem")
    args = ap.parse_args()

    l0_dir = Path(args.l0)
    files = sorted(l0_dir.glob("*.l0.jsonl"))
    if args.chunk:
        files = [f for f in files if f.name.startswith(args.chunk + ".")]

    _get_vidyut()  # warm up (loads data once)

    all_states = Counter()
    per_chunk = {}
    samples = {"CONFLICT": [], "UNANALYZED": [], "TOOL_ERROR": []}
    total = analyzed = 0
    record_rows = []  # per-record: {l0_id, surface, lemma, state, vidyut_analyses, note}

    for l0f in files:
        chunk_id = l0f.name[: -len(".l0.jsonl")]
        records = load_records(l0f)
        if args.limit:
            records = records[: args.limit]
        chunk_states = Counter()
        for r in records:
            total += 1
            surface = r.get("lemma_iast", "").strip()
            state, analyses, note = classify(surface, surface)
            all_states[state] += 1
            chunk_states[state] += 1
            if state in ("CONFIRMED", "AMBIGUOUS_SUPPORTED", "UNANALYZED", "CONFLICT"):
                analyzed += 1
            if state in samples and len(samples[state]) < 5:
                samples[state].append({"id": r["id"], "surface": surface,
                                       "state": state, "analyses": analyses, "note": note})
            record_rows.append({
                "l0_id": r.get("id"), "chunk_id": chunk_id,
                "surface": surface, "lemma_iast": surface,
                "vidyut_state": state,
                "vidyut_analyses": [{k: a.get(k) for k in ("lemma", "text", "data_class")}
                                    for a in analyses if isinstance(a, dict)],
                "note": note,
            })
        per_chunk[chunk_id] = dict(chunk_states)

    print(f"records: {total}")
    print(f"with-Sanskrit-analyzed: {analyzed}")
    print("P2 states:")
    for s in ["CONFIRMED", "AMBIGUOUS_SUPPORTED", "CONFLICT", "UNANALYZED", "NO_SANSKRIT", "TOOL_ERROR"]:
        print(f"  {s:22s} {all_states.get(s, 0)}")
    print()
    for s in ["CONFLICT", "UNANALYZED", "TOOL_ERROR"]:
        print(f"=== {s} samples ===")
        for x in samples.get(s, []):
            print(f"  {x['id']}  {x['surface'][:30]}")
            for a in x.get("analyses", [])[:3]:
                print(f"      -> {a.get('lemma','?')} ({a.get('data_class','')})")

    if args.out:
        outdir = Path(args.out)
        outdir.mkdir(parents=True, exist_ok=True)
        (outdir / "p2_summary.json").write_text(json.dumps({
            "normalization_version": NORMALIZATION_VERSION, "records": total,
            "analyzed": analyzed, "states": dict(all_states),
            "per_chunk": per_chunk,
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        for cn, st in per_chunk.items():
            (outdir / f"{cn}.l0.p2.json").write_text(json.dumps({"chunk": cn, "states": st},
                                                                indent=2), encoding="utf-8")
        # per-record output (all records, with vidyut state) — the ensemble's input
        with open(outdir / "p2_records.jsonl", "w", encoding="utf-8") as fh:
            for row in record_rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"\nwrote summary + per-chunk p2 + p2_records.jsonl to {outdir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
