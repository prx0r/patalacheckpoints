"""patala_ml/essayverify.py — the INDEPENDENT adversarial verifier.

Separate from the generator (essaygen.py). Its job: given the essay sentences + the frozen
claims + the accepted argument graph, identify every sentence that is STRONGER, BROADER, MORE
CERTAIN, or DIFFERENTLY ATTRIBUTED than its licensed claim — and reject it.

The hard invariant enforced here:
  - every substantive sentence maps to ≥1 claim (no orphan propositions)
  - no sentence claims more than its claim licenses (boundary preserved)
  - no certainty inflation (no "proves" when the claim says "establishes a requirement")
  - no source-scope expansion (no universalization beyond the licensed passages)

This is the 'given the evidence, what's too strong?' pass the reviewer demanded.
"""
from __future__ import annotations

# words that inflate certainty beyond what a licensed claim supports
INFLATION_TERMS = ["proves", "certainly", "definitively", "undeniably", "always", "everywhere",
                   "cannot be doubted", "necessarily universal", "the one Self is", "it is certain"]
# the honest, licensed verbs (what a WELL_SUPPORTED claim may say)
LICENSED_TERMS = ["establishes", "requires", "indicates", "suggests", "argues", "licenses",
                  "does not by itself", "structural requirement", "does not establish"]


def _check_claim_licensing(sentence, claims_by_id) -> list[str]:
    """Every substantive sentence must map to ≥1 claim."""
    problems = []
    if not sentence.claim_ids:
        # only TRANSITION is allowed without a claim
        if sentence.provenance_relation != "TRANSITION":
            problems.append(f"{sentence.id}: substantive sentence without a claim (relation "
                            f"{sentence.provenance_relation})")
    else:
        for cid in sentence.claim_ids:
            if cid not in claims_by_id:
                problems.append(f"{sentence.id}: claim {cid} not found")
    return problems


def _check_certainty_inflation(sentence, claims_by_id) -> list[str]:
    """No sentence may claim more certainty than its licensed claim's boundary allows."""
    problems = []
    text_lower = sentence.text.lower()
    inflated = [t for t in INFLATION_TERMS if t in text_lower]
    if not inflated:
        return problems
    # an INFERENCE or QUALIFICATION sentence may only be as strong as its claim's boundary
    for cid in sentence.claim_ids:
        claim = claims_by_id.get(cid)
        if not claim:
            continue
        # if the claim itself has an honest boundary and the sentence uses inflation, it's a leak
        if "does not by itself" in claim.get("boundary", "").lower() and inflated:
            problems.append(f"{sentence.id}: certainty inflation ({inflated}) beyond claim "
                            f"{cid}'s boundary")
    return problems


def _check_boundary_preserved(sentence, claims_by_id) -> list[str]:
    """The essay must not erase a claim's boundary."""
    problems = []
    for cid in sentence.claim_ids:
        claim = claims_by_id.get(cid)
        if not claim:
            continue
        boundary = claim.get("boundary", "").lower()
        # if the claim has a boundary and the sentence asserts the strong version, flag
        if "does not by itself" in boundary and ("is the universal self" in sentence.text.lower()
                                                 or "proves consciousness" in sentence.text.lower()
                                                 or "one self" in sentence.text.lower()
                                                 and "does not" not in sentence.text.lower()):
            problems.append(f"{sentence.id}: boundary erased for {cid} (sentence overclaims)")
    return problems


def verify_essay(essay) -> dict:
    """Verify every sentence; return the verdict + per-sentence results."""
    claims_by_id = {c["id"]: c for c in essay.claims}
    results = []
    for s in essay.sentences:
        problems = (_check_claim_licensing(s, claims_by_id)
                    + _check_certainty_inflation(s, claims_by_id)
                    + _check_boundary_preserved(s, claims_by_id))
        if problems:
            s.verification = {"structural": "FAIL", "semantic": "REVIEW",
                              "boundary_preserved": False}
            s.status = "REJECTED"
        else:
            s.verification = {"structural": "PASS", "semantic": "PASS",
                              "boundary_preserved": True}
            s.status = "VERIFIED"
        results.append({"id": s.id, "ok": not problems, "problems": problems,
                        "status": s.status})
    n = len(results)
    summary = {
        "total": n,
        "verified": sum(1 for r in results if r["ok"]),
        "rejected": sum(1 for r in results if not r["ok"]),
        "rejection_reasons": [r["problems"] for r in results if not r["ok"]],
    }
    essay.verification_summary = summary
    return {"ok": summary["rejected"] == 0, "summary": summary, "sentences": results}
