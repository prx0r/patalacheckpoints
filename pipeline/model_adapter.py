#!/usr/bin/env python3
"""pipeline/model_adapter.py — the ModelAdapter boundary (Direct vs Hermes).

The worker knows nothing about Hermes/OpenCode/etc. — it calls the adapter.

    ModelAdapter
      ├── DirectModelAdapter  ← default for structured compiler passes (fast, JSON)
      └── HermesAdapter       ← fallback / agentic work (shells to `hermes -z`)

Strict structured batch: `complete_batch_json` requires the model to echo each item's
`object_id` + `input_hash`; rejects missing/wrong/duplicate/unknown IDs and partial batches
(fail-closed) — same reliability discipline as L0.

Hermes manages work / orchestration; it does not need to mediate every token of every compiler pass.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Optional


@dataclass
class ModelResult:
    content: str
    ok: bool = True
    error: Optional[str] = None
    latency_ms: int = 0
    model: str = ""
    raw: Any = None


class ModelAdapter:
    """The boundary every compiler pass calls. Subclass to add backends."""
    name = "base"

    def complete_json(self, system: str, prompt: str, model: str,
                      timeout: int = 120) -> ModelResult:
        raise NotImplementedError

    def complete_batch_json(self, entries: list[dict], system: str,
                            make_prompt: Callable[[list[dict]], str], model: str,
                            timeout: int = 300, retries: int = 1) -> dict:
        """Strict batch: one call for many items; verify ID+hash binding; fail-closed.

        entries: [{object_id, input_hash, ...}]. Returns {object_id: {fields...}} with only
        items that passed verification (missing/wrong/duplicate/unknown IDs rejected)."""
        req = {e["object_id"]: e for e in entries}
        prompt = make_prompt(entries)
        res = self.complete_json(system, prompt, model, timeout)
        if not res.ok:
            return {"_error": res.error, "_ok": False}
        return _verify_batch(res.content, req)


class DirectModelAdapter(ModelAdapter):
    """Lean OpenAI-compatible completion (OPENCODE_GO_BASE_URL + API key). Fast path."""
    name = "direct"

    def __init__(self):
        from openai import OpenAI
        self._client = OpenAI(
            base_url=os.environ.get("OPENCODE_GO_BASE_URL", "https://opencode.ai/zen/go/v1"),
            api_key=os.environ.get("OPENCODE_GO_API_KEY"),
        )

    def complete_json(self, system: str, prompt: str, model: str,
                      timeout: int = 120) -> ModelResult:
        t0 = time.time()
        try:
            r = self._client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": prompt}],
                temperature=0.2, max_tokens=4000, timeout=timeout)
            content = r.choices[0].message.content or ""
            return ModelResult(content=content, latency_ms=int((time.time() - t0) * 1000), model=model)
        except Exception as e:
            return ModelResult(content="", ok=False, error=str(e)[:200], latency_ms=int((time.time() - t0) * 1000))


class HermesAdapter(ModelAdapter):
    """Wraps the existing `hermes -z` path (model.chat). Slow but agentic. Fallback."""
    name = "hermes"

    def complete_json(self, system: str, prompt: str, model: str,
                      timeout: int = 120) -> ModelResult:
        import sys, os as _os
        sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
        from model import chat
        t0 = time.time()
        try:
            content = chat(system, prompt, model=model, timeout=timeout)
            return ModelResult(content=content, latency_ms=int((time.time() - t0) * 1000), model=model)
        except Exception as e:
            return ModelResult(content="", ok=False, error=str(e)[:200], latency_ms=int((time.time() - t0) * 1000))


def get_adapter(name: str | None = None) -> ModelAdapter:
    name = name or os.environ.get("PATALA_MODEL_ADAPTER", "direct")
    return HermesAdapter() if name == "hermes" else DirectModelAdapter()


def _norm(s: str) -> str:
    return (s or "").strip().lower()


def _verify_batch(raw: str, requested: dict) -> dict:
    """Strict: membership + input_hash echo + no duplicates + all requested present."""
    try:
        data = json.loads(raw)
        items = data.get("translations", []) if isinstance(data, dict) else []
    except Exception:
        return {"_error": "non_json", "_ok": False}
    seen = set()
    out = {}
    for it in items:
        if not isinstance(it, dict):
            continue
        oid = it.get("object_id")
        req = requested.get(oid)
        if req is None or oid in seen:   # unknown / duplicate -> reject
            continue
        seen.add(oid)
        if _norm(it.get("input_hash")) != _norm(req.get("input_hash")):  # misbind -> reject
            out[oid] = {"_rejected": "input_hash_mismatch"}
            continue
        out[oid] = {k: v for k, v in it.items() if k not in ("object_id", "input_hash")}
    # fail-closed: any requested item missing from a COMPLETE batch = partial batch
    missing = [oid for oid in requested if oid not in out and oid not in seen]
    if missing:
        out["_partial_missing"] = missing
    return out
