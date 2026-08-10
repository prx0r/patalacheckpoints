"""Pāṭala model client — drives the translator model VIA THE HERMES AGENT.

Instead of calling the OpenAI-compatible API directly, we shell out to `hermes -z`
(the agent CLI), which handles model selection, retries, and reliability with its
own infrastructure. We keep ALL the Pāṭala logic here: the lean JSON schemas, the
capability mode (kept for compatibility), the contract-format repair, and parsing.

This means the pipeline's epistemic logic (contracts, schemas, audit) stays ours;
only the "call the model" step is delegated to hermes.
"""
from __future__ import annotations
import json
import os
import subprocess
import time
from dataclasses import dataclass
from typing import Any, Optional

BASE_URL = "https://opencode.ai/zen/go/v1"
DEFAULT_MODEL = "deepseek-v4-flash"
HERMES_BIN = os.environ.get("HERMES_BIN", "hermes")


@dataclass
class ModelResult:
    content: str
    finish_reason: Optional[str] = None
    latency_ms: int = 0
    model: str = ""
    request_id: Optional[str] = None
    raw: Optional[Any] = None


class StageOutputError(Exception):
    """Raised when a core stage returns non-structured (prose) output that was
    required to be JSON. NOT a silent fallback — the state machine must surface it."""


def _hermes_call(prompt: str, model: str = DEFAULT_MODEL, timeout: int = 420) -> str:
    """Run hermes -z with the given prompt; return its stdout (the model response).
    timeout: research tasks (C1, file-reading) legitimately take minutes; the default
    is generous. A trivial reply is fast; a full C1 research call may take several minutes."""
    env = dict(os.environ)
    env.setdefault("HERMES_MODEL", model)
    proc = subprocess.run(
        [HERMES_BIN, "-z", prompt],
        capture_output=True, text=True, env=env,
        timeout=timeout, cwd="/root/projects/patala",
    )
    out = (proc.stdout or "").strip()
    return out


def chat(system: str, user: str, model: str = DEFAULT_MODEL,
         temperature: float = 0.3, max_tokens: int = 4000,
         response_format: Optional[dict] = None,
         seed: Optional[int] = None) -> str:
    """A single model call via hermes -z. Returns just the text content.

    The full instruction (system + user) is passed to hermes as one prompt;
    hermes's own skill layer handles the house style. We ask it to return ONLY
    the requested artifact (JSON for structured stages)."""
    prompt = f"{system}\n\n{user}"
    if response_format is not None:
        prompt += "\n\nReturn ONLY the requested JSON object. No prose, no markdown fences, no commentary."
    return _hermes_call(prompt, model=model)


def chat_result(system: str, user: str, model: str = DEFAULT_MODEL,
                temperature: float = 0.3, max_tokens: int = 4000,
                response_format: Optional[dict] = None,
                seed: Optional[int] = None) -> ModelResult:
    """A single model call via hermes -z returning a ModelResult with metadata."""
    t0 = time.time()
    content = chat(system, user, model=model, temperature=temperature,
                   max_tokens=max_tokens, response_format=response_format, seed=seed)
    latency = int((time.time() - t0) * 1000)
    return ModelResult(content=content, finish_reason="stop", latency_ms=latency, model=model)


def _extract_json(raw: str) -> dict[str, Any]:
    """Strip fences and parse. Raises ValueError if no object is found."""
    raw = (raw or "").strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        raw = raw.rsplit("```", 1)[0]
    start, end = raw.find("{"), raw.rfind("}")
    if start >= 0 and end > start:
        return json.loads(raw[start:end + 1])
    raise ValueError("no JSON object found in model output")


def parse_json(raw: str, repair_fn=None) -> dict[str, Any]:
    """Parse a model output as JSON, stripping fences and finding the object block.
    If it fails and a repair_fn is given, it runs ONE bounded repair retry (the
    repair must itself return JSON — it never accepts prose)."""
    try:
        return _extract_json(raw)
    except Exception as first_err:
        if repair_fn is not None:
            repaired = repair_fn(raw)
            try:
                return _extract_json(repaired)
            except Exception as repair_err:
                raise ValueError(f"JSON repair failed: {repair_err} (original: {first_err})") from repair_err
        raise ValueError(str(first_err))


# ── structured-output capability (kept for compatibility; hermes handles it) ─

def structured_mode(model: str = DEFAULT_MODEL) -> str:
    """Hermes handles structured output; we report prompt_only (we rely on the
    lean contract + contract validation on our side)."""
    return "prompt_only"


def stage_format(stage: str, model: str = DEFAULT_MODEL) -> Optional[dict]:
    """No native response_format via hermes; rely on the lean contract + prompt."""
    return None


def stage_json_schema(stage: str) -> Optional[dict]:
    """Retained for reference/diagnostics; not sent to hermes."""
    return None


# ── semantic backoff helper (caller uses for empty/contract failures) ───────

def semantic_backoff(attempt: int, max_sleep: int = 20) -> None:
    """Jittered exponential backoff for semantic (empty/contract) retries."""
    import random as _r
    base = min(2 ** attempt, max_sleep)
    time.sleep(base + _r.uniform(0, 1))

