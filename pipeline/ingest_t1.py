#!/usr/bin/env python3
"""ingest_t1.py — the agnostic T1 → pāṭala ingest bridge (the repeatable factory).

Runs the token-T1 converter across ANY work whose T1 chunks use the token-gloss
format ([and]-GLOSS (IAST)), segments each chunk into canonical passages, and writes:

  1. data/corpus/passages/<work>.jsonl                (the passage index)
  2. data/corpus/units/<work>-{chunk}-generated.ts    (published translation objects)

This is TEXT-AGNOSTIC: any Sanskrit work with token-gloss T1 flows through the same
bridge. IPVV is the first instantiation; Kubjikā, Tantrāloka, a Buddhist text, a
ritual manual all reuse it unchanged.

Each T1 chunk becomes one or more canonical passages (chunk + kārikā-section =
passage at paragraph granularity; kārikā = container). Deterministic — no model calls.
Validation via token_t1_to_published.validate (no dangling spans/decisions).

Usage:
  python3 pipeline/ingest_t1.py --work <work_id> --t1-dir <path> [--vol 3] [--chunks V3-C,V2-O] [--write]
  python3 pipeline/ingest_t1.py --work isvarapratyabhijnavivrtivimarsini \
      --t1-dir /mnt/.../sanskritree/translations/_stack/ipvv/02_t1 --vol 3 --write
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from token_t1_to_published import parse_tokens, build_published, validate  # noqa: E402

# default pāṭala output roots (overridable for tests)
DEFAULT_BASE = Path("/root/projects/patala")


def chunk_locator(name: str, vol: int | None = None) -> str:
    """Derive a stable locator from a T1 chunk filename. Agnostic: falls back to the
    name without the 'chunk' prefix. Prefers a {V}{vol}-{LETTER} pattern when present."""
    m = re.match(r"chunk(V[0-9](?:-[A-Z]|V[A-Z0-9]*-[A-Z]?))-", name)
    if m:
        return m.group(1)
    # fallback: any leading V# token
    m2 = re.match(r"chunk(V[0-9]+[A-Z]?)", name)
    if m2:
        return m2.group(1)
    return name.replace("chunk", "").split(".")[0]


def extract_karikas(text: str) -> list[tuple[str, str]]:
    """Split a T1 chunk into (section-label, section-text) blocks by '## ' headings.
    Works for kārikā-headed (IPVV) and any other ## -sectioned T1."""
    sections = []
    cur_label = "opening"
    cur = []
    for line in text.splitlines():
        if line.startswith("## "):
            if cur:
                sections.append((cur_label, "\n".join(cur)))
                cur = []
            cur_label = line.lstrip("# ").strip()
        else:
            cur.append(line)
    if cur:
        sections.append((cur_label, "\n".join(cur)))
    return sections


def build_passage_record(chunk_name: str, klabel: str, ktext: str,
                         work_id: str, locator: str) -> dict | None:
    """One canonical passage = one section of one chunk."""
    tokens = parse_tokens(ktext)
    if not tokens:
        return None
    loc = f"{locator}:{re.sub(r'[^A-Za-z0-9]+', '_', klabel)[:40]}"
    passage_id = f"pt:passage:{work_id}:{loc}"
    sanskrit = " ".join(t["iast"] for t in tokens if t["iast"])
    pub = build_published(tokens, passage_id, work_id, sanskrit,
                          f"our T1 ({chunk_name})", f"{work_id}:{loc}:v1")
    problems = validate(pub)
    return {"passage_id": passage_id, "work_id": work_id,
            "chunk": chunk_name, "section": klabel, "locator": loc,
            "sanskrit": sanskrit, "source_edition": f"our T1 ({chunk_name})",
            "published": pub, "validation": problems, "token_count": len(tokens)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--work", required=True, help="pāṭala work id (e.g. isvarapratyabhijnavivrtivimarsini)")
    ap.add_argument("--t1-dir", required=True, help="directory of token-gloss T1 chunk files")
    ap.add_argument("--base", default=str(DEFAULT_BASE), help="pāṭala repo root (default /root/projects/patala)")
    ap.add_argument("--chunks", default="", help="comma-separated locators to ingest (default: all)")
    ap.add_argument("--write", action="store_true", help="emit passage index + published units")
    args = ap.parse_args()

    base = Path(args.base)
    t1_dir = Path(args.t1_dir)
    work = args.work
    only = set(args.chunks.split(",")) if args.chunks else None

    passages_out = base / "data/corpus/passages" / f"{work}.jsonl"
    units_out = base / "data/corpus/units"

    records = []
    for path in sorted(t1_dir.glob("chunk*.md")):
        loc = chunk_locator(path.name)
        if only and loc not in only:
            continue
        text = path.read_text(encoding="utf-8")
        for klabel, ktext in extract_karikas(text):
            rec = build_passage_record(path.name, klabel, ktext, work, loc)
            if rec:
                records.append(rec)

    total_problems = sum(len(r["validation"]) for r in records)
    total_tokens = sum(r["token_count"] for r in records)
    print(f"work: {work}")
    print(f"passages: {len(records)} · total tokens: {total_tokens} · validation problems: {total_problems}")

    if not args.write:
        for r in records[:3]:
            print(f"  {r['locator']} | {r['section']} | {r['token_count']} tokens | "
                  f"spans {len(r['published']['source_spans'])} | "
                  f"alignments {len(r['published']['alignments'])}")
        print("\n(dry run — pass --write to emit files)")
        return

    # 1) passage index jsonl (the site's passage index format)
    passages_out.parent.mkdir(exist_ok=True, parents=True)
    with open(passages_out, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps({
                "id": r["passage_id"].replace("pt:passage:", "tantra:text:"),
                "work_id": work,
                "location": {"chapter": 0, "verse": 0, "locator": r["locator"]},
                "sanskrit": r["sanskrit"],
                "source_edition": r["source_edition"],
            }, ensure_ascii=False) + "\n")
    print(f"wrote {len(records)} passages → {passages_out}")

    # 2) published units (per chunk, keyed by pt:passage:)
    by_chunk: dict[str, dict] = {}
    for r in records:
        obj = r["published"]
        obj["passage_id"] = r["passage_id"]
        by_chunk.setdefault(r["chunk"], {})[r["passage_id"]] = obj
    for chunk, pubs in by_chunk.items():
        loc = chunk_locator(chunk)
        out = units_out / f"{work}-{loc}-generated.ts"
        out.write_text(
            "// Auto-generated published translation objects for " + work + " chunk " + chunk + ".\n"
            "// Source: token-gloss T1. Deterministic.\n"
            "export const generated = " + json.dumps(pubs, ensure_ascii=False, indent=2) + ";\n",
            encoding="utf-8")
        print(f"wrote {len(pubs)} published objects → {out}")


if __name__ == "__main__":
    main()
