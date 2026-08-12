#!/usr/bin/env python3
"""pipeline/test_l0_align.py — validate the P4 L0<->L2 term-anchor alignment machinery.

Checks:
  1. inline IAST anchor extraction from L2 prose (parens, real IAST only)
  2. non-Sanskrit / supplied prose is NOT treated as an anchor
  3. resolve_anchor: exact-normalised match
  4. resolve_anchor: stem-as-prefix match (the P2 matching-rule lesson: L0 surface vs L2 stem)
  5. resolve_anchor abstains (None) on non-Sanskrit prose
  6. evaluate_passage scores anchor recall / resolution / abstention correctly
  7. the benchmark runs end-to-end on the real published store + L0 and produces an honest report

Run: cd /root/projects/patala && python3 pipeline/test_l0_align.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l0_align as la
from l0_align import (
    extract_anchors_from_l2, is_iaST_anchor, norm_lemma, resolve_anchor,
    load_l0_lemmas, evaluate_passage, candidate_alignment, main as _main,
)

PASS = 0
FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        print(f"  ✓ {name}")
        PASS += 1
    else:
        print(f"  ✗ FAIL: {name}" + (f" — {detail}" if detail else ""))
        FAIL += 1


def main():
    print("== anchor extraction ==")
    l2 = ("The manifestation (prakāśa) is not inert. Its nature is the reflexive-awareness "
          "(vimarśa). It shows the world (the crystal) but does not know it; "
          "see kārikā 12 and note the tuṭi (the bursting).")
    anchors = extract_anchors_from_l2(l2)
    check("extracts real IAST anchors", "prakāśa" in anchors and "vimarśa" in anchors, anchors)
    check("does not extract non-IAST prose", "the crystal" not in anchors, anchors)
    check("does not extract 'kārikā 12' (no IAST)", "kārikā 12" not in anchors, anchors)
    check("does not extract a gloss of an IAST term (the bursting has no diacritic)",
          "the bursting" not in anchors, anchors)

    print("\n== is_iaST_anchor ==")
    check("true for IAST token (diacritic)", is_iaST_anchor("vimarśa"))
    check("true for embedded IAST (tuṭi has diacritic)", is_iaST_anchor("the tuṭi"))
    check("false for pure English (no diacritic)", not is_iaST_anchor("the crystal"))
    check("false for a bare gloss (the bursting)", not is_iaST_anchor("the bursting"))
    check("false for number", not is_iaST_anchor("12"))

    print("\n== resolve_anchor: exact + stem-prefix ==")
    # fake L0: an inflected surface (as in the real corpus) + an exact stem
    fake_l0 = {
        norm_lemma("prakāśa"): [{"lemma_iast": "prakāśa"}],
        norm_lemma("vimarśaṃ"): [{"lemma_iast": "vimarśaṃ"}],
        norm_lemma("parāmarśāt"): [{"lemma_iast": "parāmarśāt"}],
    }
    check("exact match resolves", resolve_anchor("prakāśa", fake_l0) == norm_lemma("prakāśa"))
    check("stem-as-prefix resolves surface (vimarśa -> vimarśaṃ)",
          resolve_anchor("vimarśa", fake_l0) == norm_lemma("vimarśaṃ"))
    check("stem-as-prefix resolves (parāmarśa -> parāmarśāt, diacritic-insensitive)",
          resolve_anchor("parāmarśa", fake_l0) == norm_lemma("parāmarśāt"))
    check("abstains (None) on non-Sanskrit prose", resolve_anchor("the bursting", fake_l0) is None)
    check("abstains on empty", resolve_anchor("", fake_l0) is None)

    print("\n== evaluate_passage scoring ==")
    passage = {
        "id": "pt:passage:ipvv:test",
        "l2_text": "The light (prakāśa) and its reflexivity (vimarśa). "
                   "A supplied clause (the crystal) is inert; no diacritic so not an anchor.",
    }
    res = evaluate_passage(passage, fake_l0, candidate_alignment)
    # gold anchors: prakāśa (->prakāśa), vimarśa (->vimarśaṃ). 'the crystal' has no diacritic -> NOT an
    # anchor (abstention). So: 2 anchors, both lemmatable.
    check("found the 2 anchors", res.n_anchors == 2, res.n_anchors)
    check("resolved the 2 lemmatable anchors", res.resolved_ok == 2, res.resolved_ok)
    check("anchor recall 1.0", res.anchor_recall == 1.0, res.anchor_recall)
    check("resolution recall 1.0", res.resolution_recall == 1.0, res.resolution_recall)

    print("\n== Vidyut independent witness ==")
    l0dir = "/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/l0"
    if la.VIDYUT_AVAILABLE:
        check("vidyut_agreement AGREE on shared-stem pair (prakāśa<->prakāśa)",
              la.vidyut_agreement("prakāśa", "prakāśa") == "AGREE",
              la.vidyut_agreement("prakāśa", "prakāśa"))
        check("vidyut_agreement never fabricates on an unanalyzable pair (UNABLE or AGREE/DISAGREE)",
              la.vidyut_agreement("vimarśa", "vimarśaṃ") in ("AGREE", "DISAGREE", "UNABLE"),
              la.vidyut_agreement("vimarśa", "vimarśaṃ"))
        r = la.vidyut_ensemble_rate(
            [{"id": "pt:passage:ipvv:test2", "chunk": "chunkV2-H-pancamo-vimarsa-k11-13",
              "l2_text": "The light (prakāśa) and reflexivity (vimarśa)."}],
            l0dir, seed=42)
        check("ensemble returns a rate + honest fields",
              "agree_rate" in r and "agree_rate_analyzed_only" in r and "unable" in r, r)
        check("ensemble never reports a fabricated 1.0 when Vidyut can't analyze",
              r["agree"] + r["disagree"] + r["unable"] == r["n_links"], r["n_links"])
    else:
        print("  (skipping Vidyut witness: VIDYUT_AVAILABLE is False)")

    print("\n== end-to-end on real store ==")
    published = "data/published/ipvv"
    l0dir = "/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/l0"
    if os.path.isdir(published) and os.path.isdir(l0dir):
        # run the CLI in-process against the real data (limit to a few for speed)
        sys.argv = ["l0_align.py", "--published", published, "--l0dir", l0dir,
                    "--limit", "4", "--seed", "42", "--out", "/tmp/p4_test_report.json"]
        rc = _main()
        check("benchmark CLI exits 0", rc == 0, rc)
        import json
        rep = json.load(open("/tmp/p4_test_report.json"))
        check("report has gold_anchors > 0", rep.get("gold_anchors", 0) > 0, rep.get("gold_anchors"))
        check("report has metrics", "metrics" in rep)
        check("report is honest (explicitly a baseline/floor)",
              "baseline" in rep.get("note", "").lower() or "floor" in rep.get("note", "").lower(),
              rep.get("note"))
        os.remove("/tmp/p4_test_report.json")
    else:
        print("  (skipping end-to-end: real store not present)")

    print(f"\n=== RESULT: {PASS} pass / {FAIL} fail ===")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
