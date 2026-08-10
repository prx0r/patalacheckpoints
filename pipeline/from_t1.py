"""Build a passage record from an existing on-disk T1 markdown file.

Lets us create gold exemplars for any already-translated verse WITHOUT a model
call — we read the real house T1, extract the verse's Sanskrit + translation +
flags, and scaffold the record (T1 populated; the review stages left for the
model). This is how we bootstrap gold data from the 141 on-disk T1s.
"""
from __future__ import annotations
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from schema import new_passage, set_stage, stage_T1  # noqa: E402

# verse markers: **ch/verse**, **N**, **g.N**
_MARKERS = re.compile(r"^\*\*(\d+)\s*/\s*(\d+)\*\*\s*[—–-]?\s*(.*?)\s*$"
                      r"|^\*\*(\d+)\*\*\s*[—–-]?\s*(.*?)\s*$"
                      r"|^\*\*g\.(\d+)\*\*\s*[—–-]?\s*(.*?)\s*$")
_BQ = re.compile(r"^>\s*[—–-]?\s*(.+?)\s*[—–-]?\s*$")


def parse_t1_verse(md: str) -> list[dict]:
    """Parse a T1 markdown file into verse blocks {id, sanskrit, translation, flags}."""
    out = []
    cur = None
    seen_tr = False
    for line in md.splitlines():
        m = _MARKERS.match(line)
        if m:
            if cur and (cur["sanskrit"] or cur["translation"]):
                cur["flags"] = flags_of(cur["translation"])
                out.append(cur)
            if m.group(1) and m.group(2):  # ch/verse
                loc = f"{m.group(1)}.{m.group(2)}"; ch, vs = int(m.group(1)), int(m.group(2))
            elif m.group(4):  # verse-only
                loc = m.group(4); ch, vs = 1, int(m.group(4))
            else:  # gatha
                loc = f"g.{m.group(6)}"; ch, vs = 1, int(m.group(6))
            sanskrit = (m.group(3) or m.group(5) or m.group(7) or "").strip()
            cur = {"id": loc, "sanskrit": sanskrit, "translation": "", "flags": []}
            seen_tr = False
            continue
        if cur is None:
            continue
        b = _BQ.match(line)
        if b and b.group(1):
            cur["translation"] += (" " if cur["translation"] else "") + b.group(1).strip()
            seen_tr = True
            continue
        t = line.strip()
        if not t or t.startswith("#") or t.startswith("---"):
            continue
        if not seen_tr:
            cur["sanskrit"] += (" " if cur["sanskrit"] else "") + t
    if cur and (cur["sanskrit"] or cur["translation"]):
        cur["flags"] = flags_of(cur["translation"])
        out.append(cur)
    return out


def flags_of(text: str) -> list[str]:
    return list({m for m in re.findall(r"\[(X|TXT|GRAM|LEX|DOCT|WIT|SUP)", text)})


def record_from_t1(t1_path: str, work_id: str, verse_id: str,
                   edition: str = "our T1") -> dict:
    """Build a schema-valid record for one verse from an on-disk T1 file.
    Populates T1 from the real material; the review stages are left empty."""
    md = open(t1_path, encoding="utf-8").read()
    verses = parse_t1_verse(md)
    v = next((x for x in verses if x["id"] == verse_id), None)
    if v is None:
        raise ValueError(f"verse {verse_id} not found in {t1_path}; have {[x['id'] for x in verses][:20]}")

    loc = verse_id.split(".")
    ch, vs = (int(loc[0]), int(loc[1])) if len(loc) == 2 and loc[1].isdigit() else (1, int(loc[0].lstrip("g")))
    r = new_passage(work_id, ch, vs, v["sanskrit"], edition, t1_path)
    set_stage(r, stage_T1(
        close=v["translation"] or "(no close translation found)",
        flags=v["flags"] or flags_of(v["translation"]),
    ), created_by="t1-ingest", derived_from=None)
    return r


if __name__ == "__main__":
    path = sys.argv[1]
    work = sys.argv[2]
    verse = sys.argv[3]
    import json
    rec = record_from_t1(path, work, verse)
    print(json.dumps(rec, ensure_ascii=False, indent=2))
