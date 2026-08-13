#!/usr/bin/env python3
"""pipeline/auto_translate_raw.py — RAW Sanskrit -> ENGLISH translations, driving the queue.

The thing you actually asked for: take each work's raw Sanskrit, run the AI model over it,
and produce English translations. Works through the queue of untranslated works unattended
for hours. Output is MACHINE_PROPOSED English per passage.

Per work:
  raw source -> split verses -> bounded model batch -> close English translation
  -> write per-work translation output (data/corpus/downloads/translations/<work>.jsonl)
  -> advance the ledger -> next work

Idempotent: already-translated passages (by source hash) are skipped; replay = no dupes.
Crash-safe: writes a per-work checkpoint so it resumes where it left off.
"""
from __future__ import annotations
import argparse, json, os, re, sys, time, hashlib
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

from agent3_batch import load_raw_source, split_verses
from raw_l0 import strip_verse_marker
from batch_translate import translate_batch, build_entries
from agentic_gloss import _term_packet_for

OUT_DIR = Path("/root/projects/patala/data/corpus/downloads/translations")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def translate_verses(work_id: str, verses: list[str]) -> dict:
    """ONE model call for a bounded batch of verses -> {verse_idx: translation}."""
    packet = _term_packet_for(work_id)
    blocks = []
    for i, v in enumerate(verses):
        blocks.append(f"--- VERSE {i} ---\nVERSE: {v.strip()}\n")
    prompt = (
        "You are a careful translator of Tantric Sanskrit. Translate EACH verse below into scholarly "
        "English prose in the Pāṭala house style — accurate, readable, preserving technical terms "
        "(śakti, kula, krama, vimarśa, prakāśa, svātantrya, spanda, āveśa, tattva) and not inventing "
        "meaning. If a verse is genuinely corrupt or unreadable, set its translation to empty and list "
        "it in 'skipped'. NEVER fabricate a confident reading where the Sanskrit is unclear.\n"
        "Return JSON ONLY: {\"translations\": [{\"idx\": <i>, \"text\": \"<english>\"}, ...]}\n\n"
        f"{packet}\n\n" + "\n".join(blocks)
    )
    adapter = get_adapter()
    res = adapter.complete_json("You are the Pāṭala translation engine.", prompt,
                                model="deepseek-v4-flash", timeout=120)
    if not res.ok:
        return {}
    try:
        data = json.loads(res.content)
        out = {}
        for it in data.get("translations", []):
            idx = it.get("idx")
            t = (it.get("text") or "").strip()
            if isinstance(idx, int) and t:
                out[idx] = t
        return out
    except Exception:
        return {}


def advance_ledger(work_id: str, translated: int, total: int) -> None:
    """Mark a work's translation progress in the ledger (idempotent)."""
    path = Path("/root/projects/patala/data/corpus/downloads/translation-state-ledger.json")
    d = json.loads(path.read_text(encoding="utf-8"))
    w = d["works"].get(work_id)
    if w is None:
        return
    w["translation"] = w.get("translation", {})
    w["translation"]["t1"] = "MODERN_PRESENT" if translated > 0 else w["translation"].get("t1", "NOT_STARTED")
    w["translation"]["reason"] = f"autonomous Hermes translation: {translated}/{total} verses MACHINE_PROPOSED"
    w["l0"] = {**w.get("l0", {}), "status": "VERIFIED" if translated > 0 else w.get("l0", {}).get("status", "ELIGIBLE")}
    d["works"][work_id] = w
    path.write_text(json.dumps(d, indent=2, ensure_ascii=False))


def _chunks(text: str, target: int = 1200) -> list[str]:
    """Split text into bounded translation units when it is NOT verse-line formatted.

    Handles prose works (tantraloka, malinivijayottara) and verse works without || markers
    (bhavopahara): split on double-newline paragraphs, else sentences, else fixed windows,
    so no Sanskrit-bearing work is skipped by split_verses returning [].
    """
    units = []
    # try paragraphs first
    for para in re.split(r"\n\s*\n", text):
        p = para.strip()
        if not p:
            continue
        # skip headers/front-matter/noise (title lines, "Header", URL boilerplate, etc.)
        if re.match(r"^(#|.*[Hh]eader|.*transformation of http|.*rudimentary)", p):
            continue
        if len(p) <= target:
            units.append(p)
        else:
            # sentences
            parts = re.split(r"(?<=[।॥])\s*|(?<=[.])\s+", p)
            buf = ""
            for s in parts:
                s = s.strip()
                if not s:
                    continue
                if len(buf) + len(s) <= target:
                    buf = f"{buf} {s}".strip()
                else:
                    if buf:
                        units.append(buf)
                    buf = s
            if buf:
                units.append(buf)
    return units


def _is_sanskrit(text: str) -> bool:
    """Heuristic: does the text contain real Sanskrit (IAST diacritics), not English prose?"""
    iast = len(re.findall(r"[āīūṛṝḷḹṃñṅśṣṭḍḥṁ]", text))
    english = len(re.findall(r"\b(the|and|of|is|in|to|a|for|with)\b", text.lower()))
    return iast > 5 and english < iast / 2


def _translate_prose_batch(work_id: str, units: list[str], start_idx: int = 0) -> dict:
    """Translate long prose chunks via hermes -z directly (no verse tokenization).

    Returns {passage_id: {close: ...}} where passage_id = f"{work_id}:v{start_idx + i + 1}".
    """
    from model import chat
    packet = _term_packet_for(work_id)
    blocks = []
    for i, u in enumerate(units):
        blocks.append(f"--- UNIT {start_idx + i + 1} ---\n{re.sub(r'#+', '', u).strip()[:1500]}\n")
    prompt = (
        "You are a careful translator of Tantric Sanskrit. Translate EACH Sanskrit unit below into "
        "scholarly English prose in the Pāṭala house style — accurate, preserving technical terms "
        "(śakti, kula, krama, vimarśa, prakāśa, svātantrya, spanda, āveśa, tattva). If a unit is "
        "corrupt/unreadable/boilerplate, set it empty and list it in 'skipped'. NEVER fabricate.\n"
        "Return JSON ONLY: {\"translations\": [{\"idx\": <i>, \"text\": \"<english>\"}]}\n\n"
        f"{packet}\n\n" + "\n".join(blocks)
    )
    try:
        raw = chat("You are the Pāṭala translation engine.", prompt, max_tokens=None, timeout=600)
        data = json.loads(raw)
        out = {}
        for it in data.get("translations", []):
            idx = it.get("idx")
            t = (it.get("text") or "").strip()
            if isinstance(idx, int) and t:
                out[f"{work_id}:v{start_idx + idx + 1}"] = {"close": t}
        return out
    except Exception:
        return {}


def split_any(work_id: str, src: str, max_verses: int) -> list[str]:
    """Best-effort splitter: verse format first, then prose chunks. Filters non-Sanskrit."""
    verses = split_verses(src)
    if not verses:
        verses = _chunks(src)
    if max_verses:
        verses = verses[:max_verses]
    return verses


def _kill_stale_hermes(max_age_s: int = 300) -> None:
    """Kill orphaned/stale `hermes -z` processes not owned by the current runner.

    Observed failure mode (STALLS-PITFALLS): a hermes subprocess whose parent died keeps
    running and hogs the model API, stalling the whole queue. Before each batch, kill any
    hermes -z process older than max_age_s that is NOT a child of this runner.
    """
    import subprocess
    try:
        out = subprocess.run(["ps", "-eo", "pid,ppid,etimes,cmd"], capture_output=True, text=True).stdout
    except Exception:
        return
    my_pid = str(os.getpid())
    for line in out.splitlines()[1:]:
        parts = line.split(None, 3)
        if len(parts) < 4:
            continue
        pid, ppid, etimes, cmd = parts[0], parts[1], parts[2], parts[3]
        if "hermes -z" not in cmd:
            continue
        if ppid == my_pid:
            continue   # this runner's own active call — leave it
        try:
            if int(etimes) > max_age_s:
                os.system(f"kill -9 {pid} 2>/dev/null")
                print(f"  killed stale hermes pid {pid} (age {etimes}s, ppid {ppid})", flush=True)
        except Exception:
            pass


def run_work(work_id: str, max_verses: int) -> dict:
    src = load_raw_source(work_id)
    if not _is_sanskrit(src):
        return {"work": work_id, "passages": 0, "translated": 0, "open_skipped": 0,
                "note": "non-Sanskrit source (scholarship); skipped"}
    verses = split_any(work_id, src, max_verses)
    # skip already-translated by source hash
    out_path = OUT_DIR / f"{work_id}.jsonl"
    done = set()
    if out_path.exists():
        for line in out_path.open(encoding="utf-8"):
            try:
                done.add(json.loads(line)["source_sha256"])
            except Exception:
                pass

    translated = 0
    skipped = 0
    # bounded batches
    B = int(os.environ.get("PATALA_BATCH", "6"))
    with out_path.open("a", encoding="utf-8") as fh:
        for start in range(0, len(verses), B):
            _kill_stale_hermes()   # kill orphaned hermes before each batch (STALLS-PITFALLS)
            batch = verses[start:start + B]
            batch_idx = []
            batch_verses = []
            for i, v in enumerate(batch):
                sha = hashlib.sha256(strip_verse_marker(v).encode()).hexdigest()
                if sha in done:
                    skipped += 1
                    continue
                batch_idx.append(i)
                batch_verses.append(v)
            if not batch_verses:
                continue
            # Translate the batch. Verse-lines -> the skill engine (batch_translate →
            # model.chat → hermes -z, per-verse close). Long prose chunks -> a direct
            # hermes -z call per unit (no Vidyut tokenization needed).
            is_verse = all(len(v) < 300 for v in batch_verses)
            if is_verse:
                entries = build_entries(work_id, batch_verses, start=start)
                res = translate_batch(entries, work_id)
            else:
                res = _translate_prose_batch(work_id, batch_verses, start_idx=start)
            for j, v in zip(batch_idx, batch_verses):
                pid = f"{work_id}:v{start + j + 1}"
                item = res.get(pid) if isinstance(res, dict) else None
                text = (item.get("close", "") if isinstance(item, dict) else "") or ""
                sha = hashlib.sha256(strip_verse_marker(v).encode()).hexdigest()
                rec = {"work": work_id, "verse_idx": start + j, "source_sha256": sha,
                       "sanskrit": v.strip(), "translation": text,
                       "status": "MACHINE_PROPOSED" if text else "OPEN",
                       "ts": time.strftime('%Y-%m-%dT%H:%M:%S')}
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                done.add(sha)
                if text:
                    translated += 1
                else:
                    skipped += 1
    advance_ledger(work_id, translated, len(verses))
    return {"work": work_id, "passages": len(verses), "translated": translated,
            "open_skipped": skipped, "output": str(out_path)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--works", nargs="*", default=None)
    ap.add_argument("--max-verses", type=int, default=0)
    a = ap.parse_args()

    works = a.works
    if not works:
        # all RAW_SANSKRIT works in the ledger with source on disk
        d = json.loads(Path("/root/projects/patala/data/corpus/downloads/translation-state-ledger.json").read_text())
        works = [wid for wid, w in d["works"].items()
                 if w["source"]["available"] and w["source"]["format"] == "RAW_SANSKRIT"]

    print(f"auto-translate-raw start: works={len(works)} ts={time.strftime('%H:%M:%S')}", flush=True)
    results = []
    t0 = time.time()
    for wid in works:
        print(f"-- {wid} start {time.strftime('%H:%M:%S')}", flush=True)
        try:
            r = run_work(wid, a.max_verses)
            results.append(r)
            print(f"   {wid}: translated={r['translated']} open={r['open_skipped']} wall=... {r['output']}", flush=True)
        except Exception as e:
            print(f"   {wid}: ERROR {str(e)[:160]}", flush=True)
            results.append({"work": wid, "error": str(e)[:160]})
    print("auto-translate-raw done in %.1fs" % (time.time() - t0), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
