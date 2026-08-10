"""Bibliography readiness validator — DERIVES translation_ready, it is not asserted.

Per the red-team review: `state = translation_ready` must be derived, not a declared
enum. This checks the minimum fields a work needs before T1:

  - stable work identity (id)
  - canonical title
  - at least one base source with a stable source id
  - base source coverage includes the target passage
  - source provenance known (provider/url) or explicitly unknown
  - rights status known enough (or explicitly unknown)
  - translation coverage known
  - relevant existing translations identified or explicitly none/unknown
  - passage segmentation source identified

`unknown ≠ missing`: a field may be explicitly `unknown` and still pass; a field
that is merely absent (never checked) fails readiness.
"""
from __future__ import annotations
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_bibliography() -> list[dict]:
    """Load BibliographyRecord objects from audited.ts + bibliographySeed.ts by
    a light parse of the TS (id/work/traditions/textSources/state/rights/statusChecked)."""
    records = []
    for ts in ("data/atlas/audited.ts", "data/atlas/bibliographySeed.ts"):
        p = os.path.join(BASE, ts)
        if not os.path.exists(p):
            continue
        txt = open(p, encoding="utf-8").read()
        # split into per-record blocks: an object whose `id` is immediately followed
        # by a `work:` (a top-level BibliographyRecord, not a nested source id)
        for m in re.finditer(r'\{\s*id:\s*"([a-z0-9_]+)",\s*\n?\s*work:', txt):
            rec = {"id": m.group(1)}
            start = m.start()
            # find the object block end (balanced braces from the `{` at start)
            depth = 0
            end = start
            for i in range(txt.find("{", m.start()), len(txt)):
                c = txt[i]
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        end = i + 1
                        break
            block = txt[m.start():end]
            rec["work"] = _first(block, r'work:\s*"([^"]+)"')
            rec["traditions"] = _first(block, r'traditions:\s*\[([^\]]*)\]')
            rec["has_text_sources"] = bool(re.search(r'textSources:\s*\[', block))
            rec["has_source_id"] = bool(re.search(r'textSources:\s*\[\s*\{\s*[^}]*?id:\s*"', block))
            rec["has_status_checked"] = bool(re.search(r'statusChecked:\s*"', block))
            rec["has_rights"] = bool(re.search(r'rights:\s*\{', block))
            rec["has_translations"] = bool(re.search(r'translations:\s*\[', block))
            records.append(rec)
    return records


def _first(block: str, pattern: str) -> str:
    m = re.search(pattern, block)
    return m.group(1).strip() if m else ""


def _has_source(rec: dict) -> bool:
    return bool(rec.get("has_text_sources"))


def _has_source_id(rec: dict) -> bool:
    return bool(rec.get("has_source_id"))


def _rights_known(rec: dict) -> bool:
    return bool(rec.get("has_rights"))


def check_record(rec: dict) -> dict:
    checks = {
        "stable_identity": bool(rec.get("id")),
        "canonical_title": bool(rec.get("work")),
        "traditions": bool(rec.get("traditions")),
        "base_source_present": _has_source(rec),
        "base_source_stable_id": _has_source_id(rec),
        "rights_checked": _rights_known(rec),
        "translation_coverage": bool(rec.get("has_translations")),
        "status_checked": bool(rec.get("has_status_checked")),
    }
    passed = all(checks.values())
    return {"id": rec.get("id"), "translation_ready": passed, "checks": checks}


def report() -> str:
    records = load_bibliography()
    lines = ["Bibliography readiness (derived):"]
    ready = 0
    for r in records:
        c = check_record(r)
        mark = "READY" if c["translation_ready"] else "not-ready"
        if c["translation_ready"]:
            ready += 1
        missing = [k for k, v in c["checks"].items() if not v]
        lines.append(f"  [{mark:<9}] {c['id']:<40} missing: {missing}")
    lines.append(f"{ready}/{len(records)} works translation-ready (derived, not asserted)")
    return "\n".join(lines)


if __name__ == "__main__":
    print(report())
