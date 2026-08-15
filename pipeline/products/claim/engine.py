"""products/claim/engine.py — Claim (#4).

Real IPVV C1 passage -> a Proposition with an HONEST epistemic envelope. This is the proposition
floor beneath Argument. It keeps the three epistemic statuses visibly distinct (never inflated):
  SOURCE-SAYS         the passage literally asserts it (verbatim, source-grounded)
  SCHOLAR-RECONSTRUCTS  a scholar's reading (attributed)
  PĀṬALA-INFERS        what the engine derives (explicitly machine, lowest ceiling)

Every Claim carries: text · scope · modality · epistemic_ceiling · authority · evidence_quote ·
source_refs. The envelope NEVER inflates: a machine-inferred claim stays MACHINE_PROPOSED; only a
review/scholar event can raise it. Deterministic + stdlib, CPU-only.

Reuses the KG2Code + epistemic-envelope patterns proven in fuck-off's lib/ (query.py, epistemic.py),
re-expressed against real IPVV data.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(_ROOT / "pipeline"))

from products._shared import ipvv  # noqa: E402


def _clean(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip()


def _thesis_of(c1_body: str) -> str:
    """The central claim of a real C1: the first substantive sentence, verbatim-ish."""
    clean = _clean(c1_body)
    clean = clean.lstrip("> ")
    sentences = re.split(r"(?<=[.!?]) ", clean)
    # skip trivial opening/mangala filler; prefer a sentence with substantive technical content
    filler = {"the very opening", "the mangala has been made", "the commentary begins", "now abhinavagupta",
              "the closing", "the upoddhāta's", "this is the"}
    substantive = [s for s in sentences if not any(f in s.strip().lower()[:30] for f in filler)]
    for s in (substantive or sentences):
        s = s.strip().lstrip("> ")
        if len(s) > 25:
            return s[:280]
    return clean[:280]


def _scope_of(c1_body: str) -> str:
    """Scope honesty: 'in this passage X' vs 'always X' — never over-generalize."""
    low = c1_body.lower()
    if any(w in low for w in ("in this passage", "here", "this kārikā", "this karika")):
        return "PASSAGE_LOCAL"
    if any(w in low for w in ("always", "in general", "universally", "every")):
        return "GENERAL"
    return "PASSAGE_LOCAL"  # conservative default: never claim more than the passage


def _modality_of(c1_body: str) -> str:
    low = c1_body.lower()
    if any(w in low for w in ("necessarily", "must", "cannot", "impossible")):
        return "NECESSITY"
    if any(w in low for w in ("may", "could", "possibly", "perhaps")):
        return "POSSIBILITY"
    return "ACTUALITY"


def make_claim(passage: dict, status: str = "PĀṬALA-INFERS") -> dict:
    """Build a Claim from a real IPVV passage, with an honest envelope.

    status controls the epistemic ceiling:
      SOURCE-SAYS          -> SCHOLARLY_CORROBORATED (source literally asserts; grounded)
      SCHOLAR-RECONSTRUCTS -> SCHOLARLY_CORROBORATED_PRELIMINARY
      PĀṬALA-INFERS        -> MACHINE_PROPOSED (the honest default — never inflated)
    """
    c1 = passage.get("c1") or {}
    body = c1.get("body") or passage.get("l2_text") or ""
    thesis = _thesis_of(body)
    source_ref = ipvv.passage_id(passage)

    ceiling = {
        "SOURCE-SAYS": "SCHOLARLY_CORROBORATED",
        "SCHOLAR-RECONSTRUCTS": "SCHOLARLY_CORROBORATED_PRELIMINARY",
        "PĀṬALA-INFERS": "MACHINE_PROPOSED",
    }.get(status, "MACHINE_PROPOSED")

    return {
        "claim_id": f"C:{source_ref}",
        "text": thesis,
        "scope": _scope_of(body),
        "modality": _modality_of(body),
        "epistemic_status": status,
        "epistemic_ceiling": ceiling,
        "authority": {"generation": "MACHINE_PROPOSED", "evidence": "NONE",
                      "review": "NOT_REVIEWED", "publication": "PRIVATE"},
        "evidence_quote": body[:200],
        "source_refs": [source_ref],
        "work_id": passage.get("work_id"),
        "_body": body,   # FULL body, so the gate validates modality/scope against the true source
        "note": "honest envelope: never inflate a ceiling; only a scholar/review event raises it",
    }


def claims(passage_id: str | None = None) -> list[dict]:
    """All Claims over real IPVV passages (PĀṬALA-INFERS default — the honest floor)."""
    ps = [p for p in ipvv.passages() if p.get("id") == passage_id] if passage_id else ipvv.passages()
    return [make_claim(p, "PĀṬALA-INFERS") for p in ps]


def gate_scope(claim: dict, body: str | None = None) -> dict:
    """Honesty gate (borrowed discipline, deterministic).

    Checks the DERIVATION, not the summary: the scope/modality were classified from the C1 body;
    the gate re-verifies they aren't inflated relative to that same body. Flags:
      - SCOPE_STRENGTHENING: body is passage-local but the claim text over-generalizes.
      - MODALITY_STRENGTHENING: body lacks necessity language but the claim was tagged NECESSITY.
    The body is passed in so the gate validates against the true source (never re-derives from the
    shortened thesis).
    """
    c1 = claim.get("_body") or body or ""
    low = c1.lower()
    text = claim["text"].lower()
    flags = []

    # scope: if the BODY is passage-local, a claim text that over-generalizes is inflated
    body_local = any(w in low for w in ("in this passage", "here", "this kārikā", "this karika"))
    if body_local and any(w in text for w in ("always", "universally", "every ", "in general")):
        flags.append("SCOPE_STRENGTHENING: passage-local body, over-generalized claim")

    # modality: NECESSITY is only honest if the BODY uses necessity language
    if claim["modality"] == "NECESSITY" and not any(w in low for w in ("must", "necessarily", "cannot", "impossible")):
        flags.append("MODALITY_STRENGTHENING: necessity tagged without body necessity language")

    claim["gate_flags"] = flags
    claim["gated_ok"] = len(flags) == 0
    return claim


if __name__ == "__main__":
    import sys as _s
    all_claims = claims()
    gated = [gate_scope(c) for c in all_claims]
    ok = [c for c in gated if c["gated_ok"]]
    flagged = [c for c in gated if not c["gated_ok"]]
    print(json.dumps({
        "claims": len(all_claims), "gated_ok": len(ok), "flagged": len(flagged),
        "sample": gated[0] if gated else None,
        "flagged_sample": flagged[0] if flagged else None,
    }, indent=2, ensure_ascii=False))
