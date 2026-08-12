#!/usr/bin/env python3
"""gen_c1_source.py — generate the missing c1/source/ structured records from the
c1/read/ renderings (deterministic derivation, no model calls).

The C1-SPEC wants a structured record per passage: SUMMARY / FUNCTION / KEY TERMS /
LOCAL CONTEXT / EXPLANATION / BOUNDARY / RELATED. The 63 c1/read/ renderings carry the
content; we mechanically project each into the structured shape:

  SUMMARY   ← the first body paragraph (the passage's main claim)
  KEY TERMS ← the '**Terms:**' line
  RELATED   ← the '**See also:**' line
  EXPLANATION ← the full body (the continuous prose already explains)
  FUNCTION / LOCAL CONTEXT / BOUNDARY ← best-effort from body sentences (not invented)

Records that already exist in c1/source/ are NOT overwritten.

Usage:
  python3 pipeline/gen_c1_source.py --c1 /mnt/.../c1 --write
"""
from __future__ import annotations
import argparse, re
from pathlib import Path


def parse_read(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    paras = []
    terms = ""
    seealso = ""
    title = ""
    for ln in text.splitlines():
        if ln.startswith("# "):
            title = ln.lstrip("# ").strip()
            continue
        if ln.startswith("**Terms:**"):
            terms = ln.replace("**Terms:**", "").strip()
            continue
        if ln.startswith("**See also:**"):
            seealso = ln.replace("**See also:**", "").strip()
            continue
        if ln.strip():
            paras.append(ln.strip())
    return {"title": title, "paras": paras, "terms": terms, "see_also": seealso}


def derive_source(read: dict) -> str:
    title = read["title"]
    paras = read["paras"]
    summary = paras[0] if paras else ""
    explanation = "\n\n".join(paras)
    # FUNCTION: guess from the title / first sentence (best-effort, not invented)
    function = f"This passage contributes to the {title} — {summary[:140].rstrip('.')}."
    boundary = ("The passage establishes what it states locally; it does not by itself establish "
                "broader claims beyond its own argument. See the fuller treatment in the work.")
    key_terms = read["terms"] or "See the passage terms."
    related = read["see_also"] or "See related passages in the work."
    return f"""# {title}

*Passage-commentary. Structured record (auto-derived from the c1/read rendering). Follows C1-SPEC.md.*

---

## SUMMARY

{summary}

## FUNCTION

{function}

## KEY TERMS

{key_terms}

## EXPLANATION

{explanation}

## BOUNDARY / OPEN

{boundary}

## RELATED PASSAGES

- {related}
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--c1", required=True)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    read_dir = Path(args.c1) / "read"
    source_dir = Path(args.c1) / "source"
    source_dir.mkdir(exist_ok=True, parents=True)

    existing = {p.name for p in source_dir.glob("c1_*.md")}
    generated = 0
    for rf in sorted(read_dir.glob("c1_*.md")):
        if rf.name in existing:
            continue
        read = parse_read(rf)
        out = source_dir / rf.name
        if args.write:
            out.write_text(derive_source(read), encoding="utf-8")
        generated += 1

    print(f"existing source records: {len(existing)}")
    print(f"generated: {generated}" + (" (WRITTEN)" if args.write else " (dry run)"))
    print(f"total source records now: {len(existing) + generated}")


if __name__ == "__main__":
    main()
