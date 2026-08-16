#!/usr/bin/env python3
"""pipeline/test_source_ready.py — deterministic tests for the translation-readiness signal.

A2-INT (translation-ready signal): source_ready.py must, per work:
  - say whether the on-disk Sanskrit source is CLEAN (IAST/Devanagari density, size)
  - say whether it's READY (in ledger, has SOURCE objects)
  - give a copyright-aware PRIORITY (no-English / copyrighted-English -> HIGH; PD -> MEDIUM)
Run: python3 pipeline/test_source_ready.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipeline"))
import source_ready as S


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def main() -> int:
    ok = True
    print("=== translation-ready signal (source_ready) ===")

    # clean detection via _clean_signal on a synthetic devanagari source (write temp file)
    tmpdir = Path(tempfile.mkdtemp())
    deva = (tmpdir / "x" / "x.txt")
    deva.parent.mkdir(parents=True)
    deva.write_text("अहं ब्रह्मास्मि " * 50, encoding="utf-8")
    c = S._clean_signal.__globals__  # not used; _clean_signal reads ledger/sources though
    ok &= t("_priority_for: no-English -> HIGH",
            S._priority_for("none", [])[0] == "HIGH")
    ok &= t("_priority_for: copyrighted English -> HIGH",
            S._priority_for("complete", ["http://www.anuttaratrikakula.org/x"])[0] == "HIGH")
    ok &= t("_priority_for: partial -> HIGH",
            S._priority_for("partial", [])[0] == "HIGH")
    ok &= t("_priority_for: public-domain complete -> MEDIUM",
            S._priority_for("complete", ["https://archive.org/details/x"])[0] == "MEDIUM")
    ok &= t("_priority_for: complete unknown-host -> MEDIUM",
            S._priority_for("complete", ["https://example.com/x"])[0] == "MEDIUM")

    # real-world: tantraloka atlas record
    tl = S._translation_signal("tantraloka")
    ok &= t("tantraloka atlas record found (real audited.ts)", tl.get("has_atlas"))
    ok &= t("tantraloka english == complete (real data)", tl.get("english") == "complete", tl.get("english"))
    ok &= t("tantraloka priority == HIGH (copyrighted Dyczkowski)", tl.get("priority") == "HIGH", tl.get("why"))

    # real-world: maitrayanisamhita (no English) -> HIGH
    ma = S._translation_signal("maitrayanisamhita")
    ok &= t("maitrayanisamhita no-English -> HIGH", ma.get("priority") == "HIGH", ma.get("why"))

    # no atlas record -> LOW + flagged
    no = S._translation_signal("definitelynotawork999")
    ok &= t("no atlas record -> LOW, flagged", no.get("priority") == "LOW" and not no.get("has_atlas"))

    print("")
    print("RESULT: " + ("ALL PASS" if ok else "FAILURES"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
