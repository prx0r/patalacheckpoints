#!/usr/bin/env python3
"""pipeline/t1_session.py — PERSISTENT-SESSION STREAMING for the T1 layer.

The design tension this solves (the "long context essential + document as it goes" problem):

  - Long context IS essential: T1 needs the work's full context packet + accumulated verses to
    gloss correctly.
  - But ONE giant `hermes -z` call is a single point of failure: 10+ min, one timeout, everything
    lost, no partial output, no observability.

Solution: a LONG-LIVED Hermes session per work. Hermes persists sessions (SQLite) and `--resume
SESSION` continues them WITH the accumulated context (verified: a fact told in one resumed call is
recalled in the next). So we:

  1. Open ONE session per work, seeded with the work's context packet (term-senses, school/period,
     translation neighbourhood, companion guides) — the "long context" lives here.
  2. Feed verse-CHUNKS via `--resume <session>` — each call adds new verses while Hermes RETAINS the
     prior context (it "documents as it goes").
  3. Commit + stream-log each chunk immediately as it returns — failure of one chunk loses only that
     chunk (retryable), never the whole text, and every output is recorded as produced.

This gives long-context correctness AND failure isolation AND incremental documentation.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

sys_path = "/root/projects/patala/pipeline"
import sys
if sys_path not in sys.path:
    sys.path.insert(0, sys_path)

from model import chat

# Per-work session state: {work_id: session_id}. Persisted so a factory restart reuses a session.
SESSION_STATE = Path(os.environ.get("PATALA_SESSION_STATE",
                                    "/root/projects/patala/data/corpus/downloads/t1-sessions.json"))
# The streaming output log: one JSON line per verse as it is produced/committed.
STREAM_LOG = Path(os.environ.get("PATALA_T1_OUT_LOG",
                                 "/root/projects/patala/data/corpus/downloads/t1-stream.jsonl"))

CHUNK = int(os.environ.get("PATALA_FACTORY_CHUNK", "50"))   # verses per call (context-filled, isolated)


def _load_sessions() -> dict:
    if SESSION_STATE.exists():
        try:
            return json.loads(SESSION_STATE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_sessions(sessions: dict) -> None:
    SESSION_STATE.parent.mkdir(parents=True, exist_ok=True)
    SESSION_STATE.write_text(json.dumps(sessions, indent=2, ensure_ascii=False), encoding="utf-8")


def _term_packet_for(work_id: str) -> str:
    try:
        from agentic_gloss import _term_packet_for as _packet
        return _packet(work_id)
    except Exception:
        return ""


def open_session(work_id: str) -> str:
    """Open (or reuse) a persistent Hermes session for a work, seeded with the context packet."""
    sessions = _load_sessions()
    if work_id in sessions:
        return sessions[work_id]
    packet = _term_packet_for(work_id)
    seed = (
        "You are the Pāṭala T1 translator (the transliteral word-gloss producer) for the work "
        f"'{work_id}'. You maintain this session's context across calls: the term-context packet, "
        "the verses already glossed, and their canonical [and]-GLOSS (IAST) forms stay in your "
        "working memory so later verses are glossed with consistent senses. Gloss ONLY the verses "
        "presented in each call, and return the JSON contract exactly as instructed.\n\n"
        f"{packet}"
    )
    # first call creates the session (no --resume); returns the session id echoed via a sentinel
    sid = chat("You are the Pāṭala T1 session initializer.",
               seed + "\n\nReply with ONLY the word: SESSION_READY",
               timeout=120)
    sessions = _load_sessions()  # reload: the session id must be discovered from hermes
    # hermes assigns the session id; we capture it from the most recent CLI session (this call).
    sid_new = _discover_session_id(work_id)
    if sid_new:
        sessions[work_id] = sid_new
        _save_sessions(sessions)
        return sid_new
    # fallback: keep the echoed value (unlikely) — session still works, just not tracked by id here
    sessions[work_id] = "session-seeded"
    _save_sessions(sessions)
    return "session-seeded"


def _discover_session_id(work_id: str) -> str | None:
    """Capture the session id hermes just created/used for this call from `hermes sessions list`."""
    try:
        out = __import__("subprocess").run(
            ["hermes", "sessions", "list"], capture_output=True, text=True, timeout=30).stdout
        # lines like: <preview...> <time> cli 20260813_202621_0fe56d
        for line in out.splitlines():
            parts = line.split()
            if parts and parts[-1].startswith("20") and len(parts[-1]) >= 14 and "cli" in line:
                return parts[-1]
    except Exception:
        pass
    return None


def stream_gloss_work(work_id: str, verses: list[dict], on_verse=None) -> dict:
    """Feed a work's verses through its persistent session in chunks, committing/logging incrementally.

    verses: [{object_id, verse, tokens, input_hash}]. Returns {committed, failed, chunk_calls}."""
    sid = open_session(work_id)
    committed, failed = [], []
    chunk_calls = 0
    for start in range(0, len(verses), CHUNK):
        chunk = verses[start:start + CHUNK]
        prompt = _chunk_prompt(work_id, chunk)
        try:
            raw = chat("You are the Pāṭala T1 translator (transliteral word-gloss).", prompt,
                       timeout=600, session=sid)
            gloss_by_oid = _parse_batch(raw)
            for e in chunk:
                gloss_map = gloss_by_oid.get(e["object_id"]) or {}
                if gloss_map:
                    _stream_log(e["object_id"], "MACHINE_PROPOSED", gloss_map)
                    committed.append({"object_id": e["object_id"], "gloss_map": gloss_map,
                                      "verse": e["verse"], "tokens": e["tokens"]})
                else:
                    _stream_log(e["object_id"], "ABSTAIN", {})
                    failed.append({"object_id": e["object_id"]})
            chunk_calls += 1
        except Exception as ex:
            for e in chunk:
                _stream_log(e["object_id"], "GENERATION_FAILED", {}, error=str(ex)[:80])
                failed.append({"object_id": e["object_id"]})
    return {"committed": committed, "failed": failed, "chunk_calls": chunk_calls,
            "session": sid}


def _chunk_prompt(work_id: str, chunk: list[dict]) -> str:
    blocks = []
    for e in chunk:
        tokens = e["tokens"]
        blocks.append(
            f"--- VERSE ---\nobject_id: {e['object_id']}\nVERSE: {e['verse']}\n"
            f"TOKENS: {json.dumps(tokens, ensure_ascii=False)}\n"
        )
    return (
        "Gloss each verse below in the canonical [and]-GLOSS (IAST) form, consistent with this "
        "session's established term senses. Return JSON ONLY:\n"
        "{\"verses\": [{\"object_id\": \"<echoed>\", \"tokens\": {\"<surface>\": "
        "{\"gloss\": \"<literal>\", \"quoted\": <bool>}}}]}\n"
        "covering EVERY verse and EVERY token. Echo each object_id exactly.\n\n"
        + "\n".join(blocks)
    )


def _parse_batch(raw: str) -> dict:
    raw = (raw or "").strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        raw = raw.rsplit("```", 1)[0]
    start, end = raw.find("{"), raw.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("no JSON object in T1 session output")
    data = json.loads(raw[start:end + 1])
    out = {}
    for item in (data.get("verses") or []):
        if not isinstance(item, dict):
            continue
        oid = item.get("object_id")
        if oid:
            out[oid] = item.get("tokens") or {}
    return out


def _stream_log(object_id: str, status: str, gloss_map: dict, error: str = "") -> None:
    try:
        STREAM_LOG.parent.mkdir(parents=True, exist_ok=True)
        rec = {"ts": time.strftime('%Y-%m-%dT%H:%M:%S'), "object_id": object_id,
               "status": status, "gloss_count": len(gloss_map), "error": error or None}
        with STREAM_LOG.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass
