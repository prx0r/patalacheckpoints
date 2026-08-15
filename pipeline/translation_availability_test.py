#!/usr/bin/env python3
"""pipeline/translation_availability_test.py — proof for the translation-availability index.
Run: cd patala && PYTHONPATH=pipeline python3 pipeline/translation_availability_test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "pipeline"))

import translation_availability as TA  # noqa: E402

GATES = []


def gate(name, ok, detail=""):
    GATES.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    print("TRANSLATION-AVAILABILITY — proof (the 'which translations exist + missing' index)\n")

    # a work WITH English (partial coverage, has url)
    k = TA.availability("kramasadbhava")
    gate("known work resolves", k["work"] == "kramasadbhava")
    gate("has_english detected", k["has_english"] is True, f"languages={k['languages']}")
    gate("coverage is partial", k["coverage"] == "partial")
    gate("missing is False when partial", k["missing"] is False)
    gate("english_url carried", len(k["english_urls"]) >= 1,
         k["english_urls"][0] if k["english_urls"] else "none")
    gate("factory state present", k["factory"]["next_action"] in ("BUILD_L0_SOURCE_MODE", "ACQUIRE_SOURCE", "GENERATE_TRANSLATION"),
         k["factory"]["next_action"])

    # a work with NO English (the missing list)
    n = TA.availability("sardhatrisatikalottara")
    gate("untranslated work flagged missing", n["missing"] is True, f"coverage={n['coverage']}")

    # the full index + summary are internally consistent
    s = TA.summary()
    gate("index covers the corpus", s["total"] >= 200, f"{s['total']} works")
    gate("sums reconcile", s["full_works"] + s["partial_works"] + s["untranslated_works"] == s["total"],
         f"full={s['full_works']} partial={s['partial_works']} none={s['untranslated_works']}")
    gate("with_english <= total", s["with_english"] <= s["total"], f"{s['with_english']} with EN")
    gate("untranslated is the biggest bucket (the product)", s["untranslated_works"] > s["full_works"],
         f"{s['untranslated_works']} untranslated > {s['full_works']} full")

    passed = sum(1 for _, ok in GATES if ok)
    print(f"\n=== SUMMARY: {passed}/{len(GATES)} PASS ===\n")
    return 0 if passed == len(GATES) else 1


if __name__ == "__main__":
    sys.exit(main())
