#!/usr/bin/env python3
"""attach_c1.py — attach the C1 read/ renderings into the IPVV lazy-JSON store.

The reader's Commentary toggle renders `pub.c1.body`. The 63 finished C1 read/ renderings
live in the Sanskritree stack (translations/_stack/ipvv/c1/read/). This attaches each to
the matching passage in data/published/ipvv/, keyed by chunk label (e.g. c1_V3C-one-light.md
→ chunkV3-C-...; c1_V1A-svatyandya.md → chunkA-...).

The c1/source/ structured record (if present) is also attached as pub.c1_source so the API/MCP
has both the continuous rendering and the structured fields.

Usage:
  python3 pipeline/attach_c1.py --store /root/projects/patala/data/published/ipvv \
      --c1 /mnt/.../sanskritree/translations/_stack/ipvv/c1 --write
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path


def chunk_label_to_match(label: str) -> str:
    """Normalize a chunk label to the store's passage-id fragment.
    c1_V3C-one-light.md -> 'V3C' ; store id 'chunkV3-C-...' contains 'V3-C' -> we strip the dash.
    Also V1A -> 'chunkA-...' (store) vs c1 label 'V1A'."""
    # label like V2A, V3C, V1A, or V1-k1.1, V1-upoddhata-...
    return label


def c1_label_from_file(name: str) -> str:
    """c1_V3C-one-light.md -> 'V3C' ; c1_V1-k1.1-kathamcit.md -> 'V1-k1.1-kathamcit'"""
    stem = name.removeprefix("c1_").removesuffix(".md")
    return stem


def store_label_matches(label: str, passage_id: str) -> bool:
    """Match a C1 label to a store passage id.
    - V3C label ↔ 'chunkV3-C-...' (drop the dash)
    - V1A label ↔ 'chunkA-...'
    - V1-k1.1 ↔ 'chunkV1-k1.1' or the legacy '01_t1/k1.1-...' — fall back to substring.
    """
    # normalize the passage id: strip 'pt:passage:ipvv:', 'chunk', dashes, to compare
    pid = passage_id.replace("pt:passage:ipvv:", "").replace("chunk", "")
    norm_pid = pid.replace("-", "")
    # V1A label ↔ 'chunkA-...' (store has no V1 prefix)
    m = re.match(r"V1([A-Z])", label)
    if m and norm_pid.startswith(m.group(1)):
        return True
    # V2A/V3C ↔ chunkV2-A / chunkV3-C
    m = re.match(r"V(\d)([A-Z])", label)
    if m and f"V{m.group(1)}{m.group(2)}" in norm_pid:
        return True
    # V1 legacy: label 'V1-upoddhata-k6-k8-caitanyamajada' ↔ 'chunkH-k1.8-caitanyamajada-pratibimba'
    #   — match on a shared distinctive content word (>=6 chars, not a V1/number token).
    def _content_words(s: str) -> set:
        return {w for w in re.split(r"[^a-z0-9]+", s) if len(w) >= 6 and not w.startswith(("k1", "upoddhata")) and not w.isdigit()}
    shared = _content_words(label) & _content_words(passage_id)
    if shared:
        return True
    return False


def parse_c1_read(path: Path) -> dict:
    """Extract body + terms + see-also from a c1/read file into the C1Block shape."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    body_lines = []
    terms = ""
    seealso = ""
    for ln in lines:
        if ln.startswith("# "):
            continue
        if ln.startswith("**Terms:**"):
            terms = ln.replace("**Terms:**", "").strip()
            continue
        if ln.startswith("**See also:**"):
            seealso = ln.replace("**See also:**", "").strip()
            continue
        body_lines.append(ln)
    body = "\n".join(body_lines).strip()
    return {"body": body, "terms": terms, "see_also": seealso}


def parse_c1_source(path: Path) -> dict:
    """Extract the structured c1/source record (SUMMARY/FUNCTION/KEY TERMS/...) into a dict."""
    text = path.read_text(encoding="utf-8")
    out = {}
    current = None
    buf = []
    for ln in text.splitlines():
        if ln.startswith("## "):
            if current:
                out[current] = "\n".join(buf).strip()
            current = ln.lstrip("# ").strip().lower().replace(" ", "_")
            buf = []
        else:
            buf.append(ln)
    if current:
        out[current] = "\n".join(buf).strip()
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", required=True)
    ap.add_argument("--c1", required=True)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    store = Path(args.store)
    c1_root = Path(args.c1)
    read_dir = c1_root / "read"
    source_dir = c1_root / "source"

    index_path = store / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))

    read_files = sorted(read_dir.glob("c1_*.md")) if read_dir.exists() else []
    print(f"c1/read files: {len(read_files)}")

    attached = 0
    for entry in index["passages"]:
        pid = entry["id"]
        # collect ALL covering C1s (a V1 chunk may have several sub-commentaries)
        covers = []
        for rf in read_files:
            label = c1_label_from_file(rf.name)
            if store_label_matches(label, pid):
                covers.append(rf)
        if not covers:
            continue
        # build verse_commentary[] (one entry per covering C1) + the first's source record
        verse = []
        source_record = None
        for rf in covers:
            c1 = parse_c1_read(rf)
            verse.append({"locator": rf.name.removeprefix("c1_").removesuffix(".md"), "commentary": c1["body"]})
            if source_record is None:
                sp = source_dir / rf.name
                if sp.exists():
                    source_record = parse_c1_source(sp)
        # load the passage json, attach c1 (verse_commentary shape the reader renders) + write
        fpath = store / entry["file"]
        rec = json.loads(fpath.read_text(encoding="utf-8"))
        first = parse_c1_read(covers[0])
        rec["c1"] = {
            "body": first["body"],
            "terms": first["terms"],
            "see_also": first["see_also"],
            "verse_commentary": verse,
        }
        if source_record:
            rec["c1_source"] = source_record
        if args.write:
            fpath.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
        attached += 1
        entry["has_c1"] = True

    if args.write:
        index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"attached C1 to {attached} passages" + (" (WRITTEN)" if args.write else " (dry run)"))
    print(f"unmatched store passages without C1: {len(index['passages']) - attached}")


if __name__ == "__main__":
    main()
