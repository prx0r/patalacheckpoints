#!/usr/bin/env python3
"""pipeline/test_t1_g2_fix.py — G2 worker-fix regression (EF-T1-2026-0004).

Verifies the deterministic compound-gloss correction for `vṛttimīśaḥ` without requiring the vidyut
tokenizer (which isn't installed in the active env). This is the targeted worker-fix that closes the
last open G2 finding. The full test_t1.py covers the vidyut-dependent segmentation separately.
"""
from __future__ import annotations

import sys
sys.path.insert(0, "/root/projects/patala/pipeline")

import t1_worker as TW

ok = True
def t(name, cond, detail=""):
    global ok
    print(("PASS" if cond else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    ok = ok and cond


def main() -> int:
    print("=== G2 EF-T1-2026-0004: vṛttimīśaḥ compound gloss correction ===")
    verse = "sanmārgālokanāya vyapanayatu sa vastāmasīṃ vṛttimīśaḥ || 2 ||"

    # simulate the model returning the mangled compound gloss (the defect)
    mangled = {"tokens": {"vṛttimīśaḥ": {"gloss": "the-mental-modification-the-Lord", "quoted": False}}}

    # minimal segments (vṛttimīśaḥ is the target; we don't need vidyut segmentation for the fix)
    segments = [{"surface": "sanmārgālokanāya", "lemma": None},
                {"surface": "vyapanayatu", "lemma": None},
                {"surface": "sa", "lemma": None},
                {"surface": "vastāmasīṃ", "lemma": None},
                {"surface": "vṛttimīśaḥ", "lemma": None}]

    out = TW._assemble_t1(verse, segments, mangled["tokens"])
    vtok = next((tk for tk in out if tk["surface"] == "vṛttimīśaḥ"), None)

    t("vṛttimīśaḥ token present", vtok is not None)
    t("compound gloss corrected to a sensible parse",
      vtok is not None and vtok["gloss"] == "the Lord who is the mental modification",
      vtok["gloss"] if vtok else "none")
    t("corrected form keeps canonical [and]- framing",
      vtok is not None and vtok["form"] == "[and]-the Lord who is the mental modification (vṛttimīśaḥ)",
      vtok["form"] if vtok else "none")
    t("status stays GLOSSED", vtok is not None and vtok["status"] == "GLOSSED")
    t("other tokens unaffected (no mangled gloss leaked)",
      all("the-mental-modification-the-Lord" not in (tk.get("gloss") or "") for tk in out if tk["surface"] != "vṛttimīśaḥ"))

    # honest: a clean compound gloss (not the mangled string) passes through unchanged
    clean = {"tokens": {"vṛttimīśaḥ": {"gloss": "the Lord of activity", "quoted": False}}}
    out2 = TW._assemble_t1(verse, segments, clean["tokens"])
    v2 = next((tk for tk in out2 if tk["surface"] == "vṛttimīśaḥ"), None)
    t("a correct gloss is NOT overwritten", v2 is not None and v2["gloss"] == "the Lord of activity")

    print("\n" + ("G2-FIX ALL PASS" if ok else "G2-FIX SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
