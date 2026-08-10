"""Pāṭala model client — drives the translator model via the opencode-go API.

The same wiring the hermes project uses (https://opencode.ai/zen/go/v1,
OPENCODE_GO_API_KEY, OpenAI-compatible). The model is the *translator*; the
evidence sources (anchors, dossiers, term ledger, concordance) are ground truth.
This client only *calls* the model — it never invents scholarship.
"""
from __future__ import annotations
import json
import os
from typing import Any, Optional

from openai import OpenAI

BASE_URL = "https://opencode.ai/zen/go/v1"
DEFAULT_MODEL = "deepseek-v4-flash"

_client: Optional[OpenAI] = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        key = os.environ.get("OPENCODE_GO_API_KEY") or os.environ.get("DEEPSEEK_API_KEY")
        if not key:
            raise RuntimeError("set OPENCODE_GO_API_KEY (the opencode-go key) to use the pipeline")
        _client = OpenAI(api_key=key, base_url=os.environ.get("OPENCODE_GO_BASE_URL", BASE_URL))
    return _client


def chat(system: str, user: str, model: str = DEFAULT_MODEL,
         temperature: float = 0.3, max_tokens: int = 2000) -> str:
    """A single model call. Returns the text content. Never parses JSON itself
    unless asked — most stages want prose."""
    res = get_client().chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return res.choices[0].message.content or ""


def chat_json(system: str, user: str, model: str = DEFAULT_MODEL,
              temperature: float = 0.1) -> dict[str, Any]:
    """A model call that must return strict JSON. Strips code fences, parses."""
    raw = chat(system, user + "\n\nReturn ONLY a JSON object, no markdown fences.",
               model=model, temperature=temperature)
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        raw = raw.rsplit("```", 1)[0]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # try to find the first { ... } block
        start, end = raw.find("{"), raw.rfind("}")
        if start >= 0 and end > start:
            return json.loads(raw[start:end + 1])
        raise


def parse_json(raw: str) -> dict[str, Any]:
    """Parse a model output as JSON, stripping fences and finding the object block.
    Raises ValueError if no object is found."""
    raw = (raw or "").strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        raw = raw.rsplit("```", 1)[0]
    start, end = raw.find("{"), raw.rfind("}")
    if start >= 0 and end > start:
        return json.loads(raw[start:end + 1])
    raise ValueError("no JSON object found in model output")
