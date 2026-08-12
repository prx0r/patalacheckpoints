"""patala_ml/strength.py — the auditable Bayesian claim-strength scorer.

Maps the truth-engine's weighted-log-Bayes-factor onto Pāṭala's `Certainty` + claim-strength,
so a claim's strength is a DERIVED number, not a hand-label.

Formula (port of truthengine-propagation.py):
  weighted_lbf = w_rel × w_map × w_dep × w_aux × log_bayes_factor
  w_dep        = 1 / (1 + alpha · n_prior)     # paradigm-dependence discount
  posterior    = sigmoid(prior_log_odds + Σ weighted_lbf)

Alignment (ML-ALIGNMENT.md §2):
  posterior → Certainty → claim-strength
    0.85+  → certain        → WELL_SUPPORTED (or FORMALLY_VALID_GIVEN_ENCODING w/ Lean)
    0.65-0.85 → probable    → WELL_SUPPORTED / PLAUSIBLE
    0.45-0.65 → possible    → PLAUSIBLE
    < 0.45  → uncertain     → SPECULATIVE
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

# map onto Pāṭala's Certainty (primitives.ts) — calibrated so a strong multi-premise
# argument can reach 'certain' but a single moderate claim stays 'probable'
CERTAINTY = {
    "certain": (0.80, 1.01),
    "probable": (0.60, 0.80),
    "possible": (0.45, 0.60),
    "uncertain": (0.0, 0.45),
}
# claim-strength per certainty (ML-ALIGNMENT.md)
STRENGTH = {
    "certain": "WELL_SUPPORTED",   # or FORMALLY_VALID_GIVEN_ENCODING with Lean
    "probable": "WELL_SUPPORTED",
    "possible": "PLAUSIBLE",
    "uncertain": "SPECULATIVE",
}


@dataclass
class ClaimStrength:
    claim_id: str
    prior: float
    posterior: float
    weighted_lbf: float
    w_rel: float
    w_map: float
    w_dep: float
    w_aux: float
    log_bayes_factor: float
    paradigm: str = ""
    n_prior: int = 0
    alpha: float = 0.5

    @property
    def certainty(self) -> str:
        for c, (lo, hi) in CERTAINTY.items():
            if lo <= self.posterior < hi:
                return c
        return "uncertain"

    @property
    def strength(self) -> str:
        return STRENGTH[self.certainty]

    def audit_trace(self) -> dict:
        """The fully auditable derivation (the 'why this strength' record)."""
        return {
            "claim_id": self.claim_id,
            "prior_log_odds": round(math.log(self.prior / (1 - self.prior)), 4) if 0 < self.prior < 1 else None,
            "weighted_lbf_formula": (
                f"w_rel({self.w_rel}) × w_map({self.w_map}) × w_dep({self.w_dep}) "
                f"× w_aux({self.w_aux}) × lbf({self.log_bayes_factor})"
            ),
            "weighted_lbf": round(self.weighted_lbf, 4),
            "posterior": round(self.posterior, 4),
            "certainty": self.certainty,          # → Pāṭala Certainty
            "claim_strength": self.strength,      # → the auditable strength
            "paradigm_crowding": f"{self.n_prior} prior from '{self.paradigm}' → w_dep={self.w_dep:.3f}",
        }


def sigmoid(x: float) -> float:
    if x > 709:
        return 1.0 - 1e-15
    if x < -709:
        return 1e-15
    return 1.0 / (1.0 + math.exp(-x))


def log_odds(p: float) -> float:
    p = max(1e-15, min(1.0 - 1e-15, p))
    return math.log(p / (1.0 - p))


def dep_weight(n_prior: int, alpha: float = 0.5) -> float:
    return 1.0 / (1.0 + alpha * max(0, n_prior))


def score_claim(
    claim_id: str,
    *,
    log_bayes_factor: float,
    w_rel: float = 1.0,
    w_map: float = 1.0,
    w_aux: float = 1.0,
    prior: float = 0.5,
    paradigm: str = "",
    n_prior: int = 0,
    alpha: float = 0.5,
) -> ClaimStrength:
    """Score a claim's strength from its Bayesian factors (auditable)."""
    w_dep = dep_weight(n_prior, alpha)
    weighted = w_rel * w_map * w_dep * w_aux * log_bayes_factor
    posterior = sigmoid(log_odds(prior) + weighted)
    return ClaimStrength(
        claim_id=claim_id, prior=prior, posterior=posterior, weighted_lbf=weighted,
        w_rel=w_rel, w_map=w_map, w_dep=w_dep, w_aux=w_aux,
        log_bayes_factor=log_bayes_factor, paradigm=paradigm, n_prior=n_prior, alpha=alpha,
    )


def score_argument_premises(
    argument_id: str,
    premises: list[dict],
    *,
    paradigm_crowding: dict[str, int] | None = None,
    prior: float = 0.5,
) -> dict:
    """Score each premise of an argument; aggregate to the argument's claim strength.

    premises: [{premise_id, log_bayes_factor, w_rel, w_map, w_aux, paradigm}]
    paradigm_crowding: {paradigm: count_of_prior_claims} → w_dep per premise.
    """
    paradigm_crowding = paradigm_crowding or {}
    results = []
    combined_log_odds = log_odds(prior)
    for p in premises:
        n_prior = paradigm_crowding.get(p.get("paradigm", ""), 0)
        cs = score_claim(
            p["premise_id"],
            log_bayes_factor=p.get("log_bayes_factor", 0.0),
            w_rel=p.get("w_rel", 1.0), w_map=p.get("w_map", 1.0), w_aux=p.get("w_aux", 1.0),
            prior=prior, paradigm=p.get("paradigm", ""), n_prior=n_prior,
        )
        results.append(cs)
        combined_log_odds += cs.weighted_lbf
        # increment crowding for subsequent same-paradigm premises
        paradigm_crowding[p.get("paradigm", "")] = n_prior + 1

    agg_posterior = sigmoid(combined_log_odds)
    agg = ClaimStrength(
        claim_id=argument_id, prior=prior, posterior=agg_posterior,
        weighted_lbf=combined_log_odds - log_odds(prior),
        w_rel=1.0, w_map=1.0, w_dep=1.0, w_aux=1.0,
        log_bayes_factor=combined_log_odds - log_odds(prior),
    )
    return {
        "argument_id": argument_id,
        "aggregate": agg.audit_trace(),
        "premises": [cs.audit_trace() for cs in results],
    }
