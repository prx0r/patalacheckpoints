#!/usr/bin/env python3
"""Compile Kramasadbhāva 1.1–1.25 into published auditable translation objects.

This is the "T3 stack → publishable object compiler" — deterministic, no model calls.
It assembles each passage into the canonical PublishedTranslation schema used by 1.8:

  source_spans, target_spans, alignments, decisions, evidence, provenance

For passages where we have a working T1 (gold_records) or known decisions (1.8), those
are used. For everything else, it emits a conservative Level-1 object:
  - source spans = the Sanskrit split into word/pāda spans
  - target spans = a single whole-verse span (no word-level translation yet)
  - alignment = the whole source → whole target (1:1 coarse)
  - no decisions (or an OPEN/evidence_missing marker where we know a crux exists)
  - provenance from the edition

It NEVER invents evidence to satisfy the schema. Validation is built in: every
span/decision/evidence reference must resolve; failures are reported, not fatal.
"""
from __future__ import annotations
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASSAGES = os.path.join(BASE, "data", "corpus", "passages", "kramasadbhava.jsonl")
GOLD = os.path.join(BASE, "pipeline", "gold_records")
OUT = os.path.join(BASE, "data", "corpus", "units", "kramasadbhava-1-25-generated.ts")

WORK = "pt:work:kramasadbhava"
EDITION = "Dyczkowski ed., Muktabodha (NGMPP A 209/23)"
BASE_SOURCE = "pt:src:kramasadbhava:dyczkowski-ed"
RANGE = list(range(1, 26))

# Known crux verses where we KNOW a decision exists (seed from 1.8's lesson).
KNOWN_CRUX = {8: "nirānande", 3: "devadeveśi"}

def load_sanskrit() -> dict[int, str]:
    out = {}
    for line in open(PASSAGES, encoding="utf-8"):
        p = json.loads(line)
        if p["location"]["chapter"] == 1 and p["location"]["verse"] in RANGE:
            out[p["location"]["verse"]] = p["sanskrit"]
    return out

def load_gold_translation(verse: int) -> str | None:
    path = os.path.join(GOLD, f"tantra_text_kramasadbhava_1_{verse}.json")
    if os.path.exists(path):
        try:
            d = json.load(open(path, encoding="utf-8"))
            t = d.get("stages", {}).get("T1", {}).get("close_translation")
            return t or None
        except Exception:
            return None
    return None

def split_source_spans(sanskrit: str) -> list[str]:
    """Split Sanskrit into word-ish spans (honest: whitespace/pāda split, not morphology)."""
    text = re.sub(r"[|।॥]+", " ", sanskrit)
    words = [w for w in text.split() if w.strip()]
    return words or [sanskrit.strip()]

def split_target_spans(translation: str) -> list[str]:
    """Split the English into sentence-ish spans."""
    if not translation:
        return []
    text = translation.strip()
    parts = re.split(r"(?<=[.]) +", text)
    return [p for p in parts if p.strip()] or [text]

def make_published(verse: int, sanskrit: str, gold_tr: str | None) -> dict:
    pid = f"pt:passage:kramasadbhava:1.{verse}"
    version = f"pt:translation:kramasadbhava:1.{verse}:v1"
    src_words = split_source_spans(sanskrit)
    source_spans = [
        {"id": f"pt:srcspan:krs:1.{verse}:{i+1}", "passage_id": pid, "text": w}
        for i, w in enumerate(src_words)
    ]
    # translation: use gold T1 if present, else empty (no translation yet)
    target_words = split_target_spans(gold_tr) if gold_tr else []
    target_spans = [
        {"id": f"pt:tgtspan:krs:1.{verse}:{i+1}", "translation_version_id": version, "text": t}
        for i, t in enumerate(target_words)
    ]
    # alignment: coarse whole→whole if a translation exists; else none
    alignments = []
    if target_spans:
        alignments.append({
            "id": f"pt:align:krs:1.{verse}:1",
            "source_span_ids": [s["id"] for s in source_spans],
            "target_span_ids": [t["id"] for t in target_spans],
            "type": "merged",
            "decision_ids": [],
            "method": "pipeline",
        })

    # decisions: known cruxes get an OPEN/evidence_missing marker; nothing invented
    decisions = []
    crux = KNOWN_CRUX.get(verse)
    if crux:
        decisions.append({
            "id": f"pt:decision:krs:1.{verse}:LEX:1",
            "passage_id": pid,
            "translation_version_id": version,
            "source_span_ids": [source_spans[0]["id"]] if source_spans else [],
            "target_span_ids": [],
            "type": "LEXICAL",
            "claim": f"{crux} — sense unresolved",
            "surface_rendering": gold_tr or "",
            "alternatives": [],
            "status": "OPEN",
            "evidence_state": "evidence_missing",
            "editorial_status": "proposed",
            "reason": f"Known crux ({crux}) at 1.{verse}; no research yet. Honest marker, not a resolution.",
            "method": "pipeline",
            "evidence": [],
            "review_events": [],
            "origin": "machine",
            "created_at": "2026-08-10",
            "created_by": "compiler",
        })

    return {
        "passage_id": pid,
        "work_id": WORK,
        "text": gold_tr or "",
        "version_id": version,
        "version": 1,
        "source_spans": source_spans,
        "target_spans": target_spans,
        "alignments": alignments,
        "decisions": decisions,
        "evidence": [],
        "review_state": "proposed",
        "provenance": {"base_source": BASE_SOURCE, "edition": EDITION, "translation_version_id": version},
    }

def validate(pub: dict) -> list[str]:
    problems = []
    sid = {s["id"] for s in pub["source_spans"]}
    tid = {t["id"] for t in pub["target_spans"]}
    for a in pub["alignments"]:
        for s in a["source_span_ids"]:
            if s not in sid: problems.append(f"{pub['passage_id']}: align source {s} missing")
        for t in a["target_span_ids"]:
            if t not in tid: problems.append(f"{pub['passage_id']}: align target {t} missing")
    for d in pub["decisions"]:
        for s in d["source_span_ids"]:
            if s and s not in sid: problems.append(f"{pub['passage_id']}: decision source {s} missing")
        for e in d["evidence"]:
            # no evidence pool in Level-1 objects yet — not a dangling ref, just unpopulated
            pass
    return problems

def main():
    sans = load_sanskrit()
    pubs = []
    problems_total = []
    for v in RANGE:
        s = sans.get(v, "")
        tr = load_gold_translation(v)
        if not s:
            print(f"  [warn] no sanskrit for 1.{v} — skipping")
            continue
        pub = make_published(v, s, tr)
        problems = validate(pub)
        problems_total += problems
        pubs.append(pub)
    # emit TS
    lines = [
        "// Generated by pipeline/compile_published.py — do not edit by hand.",
        "// Kramasadbhāva 1.1–1.25 published auditable translation objects (Level 1).",
        "import type { PublishedTranslation } from \"../translation\";",
        "",
        "export const kramasadbhava_1_25: Record<string, PublishedTranslation> = {",
    ]
    for p in pubs:
        lines.append(f"  \"{p['passage_id']}\": {json.dumps(p, ensure_ascii=False, indent=2)},")
    lines.append("};")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {len(pubs)} published passages -> {OUT}")
    print(f"Validation: {len(problems_total)} problems")
    for p in problems_total[:15]:
        print(f"  {p}")
    # summary
    open_dec = sum(1 for p in pubs for d in p["decisions"] if d["status"] == "OPEN")
    with_tr = sum(1 for p in pubs if p["target_spans"])
    print(f"\n{len(pubs)} passages | {with_tr} with working translation | {open_dec} OPEN decisions")

if __name__ == "__main__":
    main()
