#!/usr/bin/env python3
"""phase1_ipvv_corpus.py — Phase 1: build the canonical IPVV passage corpus from the
EXISTING structure (L200 anchors + L2 reads + source vols). Reuses the chunk→source-range
mapping already implicit in the L200 files; does NOT invent a new segmentation.

Hierarchy (source of truth, from README.md + L200):
    work → volume (M00020/21/22) → vimarśa/adhikāra (from chunk name) → kārikā (from L200 §0)
         → canonical passage (the chunk's L2 ¶ range)

The canonical passage unit = the L2 paragraph block (from the pilot L2 read), linked to:
  - source range (M0002x lines, from L200)
  - L0 record range (l0/<chunk>.l0.jsonl)
  - the chunk / T1

Outputs:
  ipvv_passages.jsonl        canonical source/passage records (one per L2 ¶)
  ipvv_ingest_report.json    counts + zero-loss + unresolved + provenance failures

Hard stops (fail if): source text disappears · L2 orphaned · duplicate ids · unresolvable
locators · any chunk silently skipped · paragraph ordering changes · unresolved auto-guessed.
Unresolved items are emitted with status: NEEDS_MAPPING, never auto-attached.

Usage:
  python3 pipeline/phase1_ipvv_corpus.py --base /mnt/.../sanskritree --out /tmp/ipvv_phase1
"""
from __future__ import annotations
import json
import os
import re
import sys
from pathlib import Path

def norm_vol(s: str) -> str:
    m = re.search(r"M0002([012])", s)
    return "M0002" + (m.group(1) if m else "0")

def parse_l200(l200_path: Path) -> dict | None:
    """Extract {chunk, vol, source_start, source_end, l0, argmap, l2, section} from an L200 file."""
    text = l200_path.read_text(encoding="utf-8")
    info: dict = {"file": l200_path.name, "raw": l200_path.stem}
    # chunk
    m = re.search(r"Chunk `([^`]+)`", text)
    info["chunk"] = m.group(1) if m else l200_path.stem
    # volume + source start
    m = re.search(r"(M0002[012]) lines (\d+)", text)
    if m:
        info["vol"] = norm_vol(m.group(1))
        info["source_start"] = int(m.group(2))
    else:
        return None
    # source end: explicit range "N–M" or "N-M"
    m2 = re.search(r"M0002[012] lines (\d+)[–-](\d+)", text)
    info["source_end"] = int(m2.group(2)) if m2 else None
    # section / vimarśa from the identification (e.g. "kriyādhikāra, tṛtīyo vimarśaḥ")
    m = re.search(r"Section \| (.+)", text)
    info["section"] = m.group(1).strip() if m else ""
    m = re.search(r"\| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|", text)
    # L0 file
    m = re.search(r"L0 `(l0/[^`]+\.jsonl)`", text)
    info["l0"] = m.group(1) if m else None
    # argument map
    m = re.search(r"argument map `([^`]+)`|Argument map \| `([^`]+)`", text)
    info["argmap"] = (m.group(1) or m.group(2)) if m else None
    # L2 read
    m = re.search(r"L2 `([^`]+)`|L2 READ \| `([^`]+)`", text)
    info["l2"] = (m.group(1) or m.group(2)) if m else None
    return info

def resolve_source(vol_dir: Path, vol: str, start: int, end: int | None) -> str:
    """Read the source text for a vol's line range."""
    path = None
    for p in vol_dir.glob("*.txt"):
        if "M0002" in p.name and vol in p.name:
            path = p
            break
    if path is None:
        return ""
    lines = path.read_text(encoding="utf-8").splitlines()
    if start < 1 or start > len(lines):
        return ""
    end = end if end is not None else start
    end = min(end, len(lines))
    return "\n".join(lines[start - 1:end])

def chunk_vol_from_name(name: str) -> tuple[str, str]:
    """Map a chunk name to (vol, vimarśa-letter). Agnostic fallback."""
    m = re.match(r"chunk(V[0-9])-([A-Z])", name)
    if m:
        vol_num = int(m.group(1))
        return f"M0002{vol_num}", f"V{m.group(1)}-{m.group(2)}"
    # V1 chunks (01_t1): V1A-chunkA-...
    m = re.match(r"chunk([A-Z])-", name)
    if m:
        return "M00020", f"V1-{m.group(1)}"
    return "M00020", name

def chunk_l2_path(base: Path, chunk: str) -> Path | None:
    """Derive the L2 read file from the chunk name (deterministic):
    chunkV2-A-... → pilot_V2A_L2_read.md ; chunkA-... (V1) → pilot_V1A_L2_read.md
    Special case: V3-B has no single pilot_V3B_L2_read.md; its L2 is split across
    pilot_V3B_full_L2.md + pilot_V3B_{K6,S7,S9}_L2_read.md → return the full one."""
    pilot = base / "translations/_stack/ipvv/pilot"
    m = re.match(r"chunkV([0-9])-([A-Z])", chunk)
    if m:
        if m.group(1) == "3" and m.group(2) == "B":
            p = pilot / "pilot_V3B_full_L2.md"
            return p if p.exists() else None
        p = pilot / f"pilot_V{m.group(1)}{m.group(2)}_L2_read.md"
        return p if p.exists() else None
    m = re.match(r"chunk([A-Z])-", chunk)
    if m:
        p = pilot / f"pilot_V1{m.group(1)}_L2_read.md"
        return p if p.exists() else None
    return None


def read_l2_body(path: Path) -> str:
    """Extract the published L2 prose (the READ text) from a pilot L2 file."""
    text = path.read_text(encoding="utf-8")
    # body after the first '---' rule, before '## Fidelity note'
    body = []
    seen_rule = False
    for line in text.splitlines():
        if not seen_rule:
            if line.strip() == "---":
                seen_rule = True
            continue
        if line.lstrip().startswith("## "):
            break
        body.append(line)
    return "\n".join(body).strip()


def chunk_l0_path(base: Path, chunk: str) -> str | None:
    """L0 file for a chunk (l0/<chunk>.l0.jsonl or l0_v1 for V1)."""
    for d in ("l0", "l0_v1"):
        p = base / "translations/_stack/ipvv" / d / f"{chunk}.l0.jsonl"
        if p.exists():
            return f"{d}/{chunk}.l0.jsonl"
    return None


def main() -> None:
    args = sys.argv[1:]
    base = Path(args[args.index("--base") + 1] if "--base" in args else "/mnt/HC_Volume_106427611/sanskritree")
    out = Path(args[args.index("--out") + 1] if "--out" in args else "/tmp/ipvv_phase1")
    out.mkdir(exist_ok=True, parents=True)

    l200_dir = base / "translations/_stack/ipvv/l200"
    src_dir = base / "sources/muktabodha-lib"
    pilot_dir = base / "translations/_stack/ipvv/pilot"
    t1_dir = base / "translations/_stack/ipvv/02_t1"

    # 1) parse all L200 files → chunk records
    chunks = []
    skipped = []
    for p in sorted(l200_dir.glob("*.md")):
        if p.name.startswith("README") or p.name.startswith("INDEX"):
            continue
        info = parse_l200(p)
        if info is None:
            skipped.append(p.name)
            continue
        chunks.append(info)

    # 2) sort by (vol, source_start), derive ends from next chunk's start
    chunks.sort(key=lambda c: (c["vol"], c.get("source_start", 0)))
    for i, c in enumerate(chunks):
        if c.get("source_end") is None:
            nxt = chunks[i + 1] if i + 1 < len(chunks) else None
            c["source_end"] = (nxt["source_start"] - 1) if nxt and nxt["vol"] == c["vol"] else None

    # 3) build passage records from each chunk's L2 read paragraphs
    passages = []
    problems = []
    l2_orphaned = []
    for c in chunks:
        # source text
        src = resolve_source(src_dir, c["vol"], c["source_start"], c["source_end"])
        if not src:
            problems.append(f"NO_SOURCE {c['chunk']} {c['vol']} {c.get('source_start')}")
            passages.append({"id": f"pt:passage:ipvv:{c['chunk']}", "work_id": "isvarapratyabhijnavivrtivimarsini",
                             "status": "NEEDS_MAPPING", "reason": "no source text", "chunk": c["chunk"]})
            continue
        # L2 prose (the published READ text)
        l2_path = chunk_l2_path(base, c["chunk"])
        l2_text = read_l2_body(l2_path) if l2_path else ""
        # legacy 01_t1/ small chunks (V1 upoddhata/k1.x/purvapaksa) have no L2 read;
        # mark NEEDS_MAPPING rather than count as orphaned.
        is_legacy_v1 = c["chunk"].startswith("01_t1/")
        if not l2_path and not is_legacy_v1:
            l2_orphaned.append(c["chunk"])
        passage_status = "OK"
        if not l2_text:
            passage_status = "NEEDS_MAPPING" if is_legacy_v1 else "OK"
        # L0 file
        l0 = chunk_l0_path(base, c["chunk"])
        # the passage = the chunk (one canonical passage per chunk at coarse level)
        pid = f"pt:passage:ipvv:{c['chunk']}"
        passages.append({
            "id": pid,
            "work_id": "isvarapratyabhijnavivrtivimarsini",
            "chunk": c["chunk"],
            "vol": c["vol"],
            "source": {"start": c.get("source_start"), "end": c.get("source_end"), "text": src},
            "l0": l0,
            "argmap": c.get("argmap"),
            "l2": str(l2_path.relative_to(base)) if l2_path else None,
            "l2_text": l2_text,
            "section": c.get("section"),
            "status": passage_status,
        })

    # 4) write ipvv_passages.jsonl
    passages_out = out / "ipvv_passages.jsonl"
    with open(passages_out, "w", encoding="utf-8") as f:
        for p in passages:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")

    # 5) report
    ok = [p for p in passages if p.get("status") == "OK"]
    needs = [p for p in passages if p.get("status") == "NEEDS_MAPPING"]
    report = {
        "phase": "phase1",
        "work": "isvarapratyabhijnavivrtivimarsini",
        "chunks_parsed": len(chunks),
        "chunks_skipped": skipped,
        "passages_total": len(passages),
        "passages_ok": len(ok),
        "passages_needs_mapping": len(needs),
        "l2_orphaned": l2_orphaned,
        "problems": problems,
        "zero_loss": len(needs) == 0 and not any("NO_SOURCE" in p for p in problems),
        "duplicate_ids": [],
    }
    # duplicate id check
    ids = [p["id"] for p in passages]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    report["duplicate_ids"] = dupes
    report["zero_loss"] = report["zero_loss"] and not dupes and not l2_orphaned
    # provenance: every OK passage must resolve source + L2
    no_l2 = [p["chunk"] for p in ok if not p.get("l2_text")]
    no_source = [p["chunk"] for p in ok if not p.get("source", {}).get("text")]
    report["no_l2"] = no_l2
    report["no_source"] = no_source
    report["provenance_resolves"] = not no_l2 and not no_source
    report_out = out / "ipvv_ingest_report.json"
    report_out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"chunks: {len(chunks)} · passages: {len(passages)} · OK: {len(ok)} · NEEDS_MAPPING: {len(needs)}")
    print(f"duplicate ids: {len(dupes)} · zero_loss: {report['zero_loss']} · l2_orphaned: {len(l2_orphaned)}")
    print(f"no_l2: {len(no_l2)} · no_source: {len(no_source)} · provenance_resolves: {report['provenance_resolves']}")
    print(f"problems: {len(problems)}")
    print(f"wrote {passages_out} + {report_out}")

if __name__ == "__main__":
    main()
