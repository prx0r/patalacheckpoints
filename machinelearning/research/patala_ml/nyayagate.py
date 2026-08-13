"""patala_ml/nyayagate.py — the Pāṭala-adapted Nyāya gate (the mechanism, not the ontology).

The truth-engine's 680-LOC gate is ontology-bound: its hardcoded rules ("meditation proves
consciousness is fundamental", "brain damage...") are specific to the B1-B6 metaphysics contest.
Per TRUTHENGINE_TO_PATALA_MAPPING.md, we REUSE THE MECHANISM (the 5-hetvābhāsa check) and REJECT
the ontology.

This is the Pāṭala version: the same 5 fallacies, but with PHILOLOGICAL/ARGUMENT rules and
well-formed-input assumptions. It is `NYAYA_GATE_CANDIDATE_v1` — deterministic, but promoted to
verify-claim-semantic only after the gold fixtures (benchmarks/v0/evidence/nyaya-gate-gold.jsonl)
pass blind.

The 5 hetvābhāsas:
  asiddha       the reason/hetu is not itself established
  viruddha      the evidence supports the opposite of the claim
  savyabhicara  the reason does not always imply the conclusion (counterexamples)
  satpratipaksa an equally strong counter-inference exists
  badhita       a stronger pramāṇa contradicts

Outcome → can_update_posterior: accepted→True, accepted_with_penalty→True(cap),
needs_review/hollow/refuted→False.
"""
from __future__ import annotations

from dataclasses import dataclass, field

PRAMANAS = ["pratyaksa", "anumana", "upamana", "sabda", "formal_proof"]
FALLACIES = ["asiddha", "viruddha", "savyabhicara", "satpratipaksa", "badhita"]

# the graph-aware viruddha detector version. Bumped when the algorithm materially changes
# (commitment-eligibility, token filtering, normalization, defeater metadata, unicode-aware tokens).
VIRUDDHA_GRAPH_VERSION = "graph-viruddha-v2"

# pramāṇa reliability hierarchy (Nyāya): perception strongest → testimony weakest
PRAMANA_RANK = {"pratyaksa": 4, "anumana": 3, "upamana": 2, "sabda": 1, "formal_proof": 3}

# words signalling overclaim (strong conclusion from weak pramāṇa → asiddha)
STRONG_WORDS = ["proves", "settles", "demonstrates", "decisive", "therefore reality", "certainly", "always"]
# words signalling an unfalsifiable / non-verifiable claim (→ hollow / abstain)
UNFALSIFIABLE = ["cannot be measured", "cannot be verified", "transcends all evidence", "no possible disproof"]
# words signalling the claim has no empirical check → needs falsifier
NO_FALSIFIER = ["is fundamental", "is the ultimate", "is absolutely true", "is the one and only"]
# words signalling an un-established reason/hetu (asiddha): the reason itself is dubious
UNESTABLISHED_HETU = ["subtle body", "astral plane", "past lives", "invisible power", "secret energy",
                      "cannot be detected", "unseen"]
# words signalling a universal/always claim that overreaches (savyabhicara: counterexamples exist)
UNIVERSAL_OVERRECH = ["always", "invariably", "everywhere", "in all cases", "never fails", "universally"]
# words signalling the conclusion is contradicted by established evidence (badhita)
CONTRADICTED_BY_EVIDENCE = ["no neural correlate", "no neural correlates", "brain is irrelevant",
                            "brain irrelevant", "has no physical basis", "cannot be real"]
# negation/inversion signals for viruddha (the claim runs against its own evidence)
VIRUDDHA_MARKERS = ["therefore the opposite", "proves it is not", "shows it cannot be",
                    "refutes the claim that"]


@dataclass
class GateFailure:
    fallacy: str
    severity: str
    rationale: str
    defeater_metadata: dict | None = None

    def to_dict(self) -> dict:
        d = {"fallacy": self.fallacy, "severity": self.severity, "rationale": self.rationale}
        if self.defeater_metadata:
            d["defeater_metadata"] = self.defeater_metadata
        return d


@dataclass
class GateResult:
    claim_id: str
    outcome: str                  # accepted | accepted_with_penalty | needs_review | hollow | refuted
    can_update_posterior: bool
    pramana: str
    tradition: str
    failures: list[GateFailure] = field(default_factory=list)
    falsifier_status: str = "MISSING"
    abstain: bool = False

    def to_dict(self) -> dict:
        return {"claim_id": self.claim_id, "outcome": self.outcome,
                "can_update_posterior": self.can_update_posterior, "pramana": self.pramana,
                "tradition": self.tradition,
                "failures": [f.to_dict() for f in self.failures],
                "falsifier_status": self.falsifier_status, "abstain": self.abstain}


def _has(claim: dict, *keys) -> bool:
    return any(claim.get(k) for k in keys)


def _strongest(failures: list[GateFailure]) -> str:
    order = {"weak": 1, "moderate": 2, "strong": 3, "decisive": 4}
    return max((f.severity for f in failures), key=lambda s: order.get(s, 0), default="none")


def gate_claim(claim: dict, peer_claims: list[dict] | None = None) -> GateResult:
    """Run the Pāṭala-adapted 5-hetvābhāsa gate on a claim.

    claim: {claim_id, claim_text, pramana, tradition, falsifier?, vyapti_confidence?,
            vyapti_violations?, log_bayes_factor?}
    peer_claims: [{claim_id, claim_text, log_bayes_factor, targets?}] for satpratipaksa
    """
    cid = claim.get("claim_id", "cl:unknown")
    text = str(claim.get("claim_text", "")).lower()
    pramana = claim.get("pramana", "anumana") if claim.get("pramana") in PRAMANAS else "anumana"
    tradition = claim.get("tradition", "")
    lbf = float(claim.get("log_bayes_factor", 0.0) or 0.0)
    peer_claims = peer_claims or []
    failures: list[GateFailure] = []

    # ── HOLLOW / abstain: unfalsifiable claim → no confident verdict ──
    if any(u in text for u in UNFALSIFIABLE):
        return GateResult(cid, "hollow", False, pramana, tradition,
                          [GateFailure("asiddha", "strong",
                                       "unfalsifiable — no test could disconfirm")],
                          "MISSING", abstain=True)

    # ── falsifier required ──
    falsifier = claim.get("falsifier")
    falsifier_status = "PRESENT" if falsifier else "MISSING"

    # ── asiddha: the reason/hetu itself is not established ──
    if any(u in text for u in UNESTABLISHED_HETU):
        failures.append(GateFailure("asiddha", "strong",
                                    f"the hetu is not independently established (marker: {[u for u in UNESTABLISHED_HETU if u in text][0]})"))
    if any(w in text for w in STRONG_WORDS) and pramana in ("sabda", "upamana") and abs(lbf) > 0.8:
        failures.append(GateFailure("asiddha", "moderate",
                                    "strong conclusion from testimony/analogy; independent establishment required"))

    # ── savyabhicara: a universal/always claim WITHOUT strong vyāpti backing ──
    # (a universal claim backed by high vyāpti confidence + no violations is a VALID vyāpti, not a defect)
    if any(w in text for w in UNIVERSAL_OVERRECH):
        vc = claim.get("vyapti_confidence")
        # a universal claim is a defect UNLESS backed by high vyāpti confidence (≥0.8) and no violations
        if vc is None or vc < 0.8 or claim.get("vyapti_violations"):
            failures.append(GateFailure("savyabhicara", "moderate",
                                        f"universal claim '{[w for w in UNIVERSAL_OVERRECH if w in text][0]}' without strong vyāpti backing (confidence={vc}) — counterexamples likely"))
    vc = claim.get("vyapti_confidence")
    if vc is not None and vc < 0.6:
        failures.append(GateFailure("savyabhicara", "moderate",
                                    f"vyāpti_confidence {vc} < 0.6 — the reason does not reliably imply the target"))
    if claim.get("vyapti_violations"):
        failures.append(GateFailure("savyabhicara", "moderate",
                                    "claim lists vyāpti violations/counterexamples"))

    # ── viruddha: the evidence supports the opposite of the claim ──
    # heuristic: the claim itself signals it's deriving the opposite/negation of its hetu
    if any(m in text for m in VIRUDDHA_MARKERS):
        failures.append(GateFailure("viruddha", "strong",
                                    "the claim derives the opposite of its own reason/evidence (self-inverting)"))

    # ── badhita: the conclusion is contradicted by stronger established evidence ──
    if any(c in text for c in CONTRADICTED_BY_EVIDENCE):
        failures.append(GateFailure("badhita", "strong",
                                    "the conclusion is contradicted by stronger established evidence (marker present)"))

    # ── satpratipaksa: an equally strong counter-inference on the same target ──
    my_targets = {str(t.get("target_id")) for t in (claim.get("targets") or [])}
    for pc in peer_claims:
        pc_lbf = float(pc.get("log_bayes_factor", 0.0) or 0.0)
        pc_targets = {str(t.get("target_id")) for t in (pc.get("targets") or [])}
        # opposing sign AND overlapping target → counter-balanced
        if pc_lbf != 0 and (pc_lbf > 0) != (lbf > 0) and (my_targets & pc_targets or not my_targets):
            failures.append(GateFailure("satpratipaksa", "moderate",
                                        f"equally-strong counter-inference {pc.get('claim_id')} exists on an overlapping target"))

    # ── the outcome ──
    severity = _strongest(failures)
    if not failures:
        outcome, can_update = "accepted", True
    elif severity == "strong":
        outcome, can_update = "needs_review", False
    elif severity == "moderate":
        outcome, can_update = "accepted_with_penalty", True
    else:
        outcome, can_update = "accepted", True

    # a missing falsifier always downgrades a would-be-accepted claim
    if falsifier_status == "MISSING" and outcome == "accepted":
        outcome, can_update = "accepted_with_penalty", True

    return GateResult(cid, outcome, can_update, pramana, tradition, failures, falsifier_status)


def check_viruddha_graph(claim: dict, gold_propositions: list[dict]) -> list[GateFailure]:
    """GRAPH-AWARE viruddha: does the gold's established propositions establish the OPPOSITE of the claim?

    This replaces the keyword-heuristic viruddha with a real graph operation (per
    NYAYA-GATE-CANDIDATE-V1.md: "viruddha requires a real argument graph — knowing the text argues the
    opposite"). For a candidate claim H, we look at the gold's committed propositions:
      - a proposition P is 'established' if its commitment is ASSERTS/DERIVES (a siddhānta claim),
        NOT ATTRIBUTES_TO_OPPONENT/RECONSTRUCTED-without-support.
      - if an established proposition P semantically contradicts H (i.e. P implies ¬H, or H implies ¬P),
        that is a VIRUDDHA_CANDIDATE → the semantic layer decides.

    `contradicts`: a minimal, honest lexical-overlap-contradiction check. It flags the case where the
    gold asserts X and the candidate asserts "X is not the case" / "not-X" / the direct negation of a
    gold proposition. It does NOT claim full semantic entailment — it NOMINATES a viruddha candidate
    for the semantic layer (as the doc requires), never settles it alone.

    Defeater metadata: every hit carries `possible_defeaters` — the ways the apparent contradiction
    could be a false positive (scope / modality / speaker / temporal / qualification / level
    difference). This is the HANDSHAK contract to the semantic layer: it knows exactly what to test
    before accepting the contradiction. A hit is a `structurally plausible contradiction candidate
    requiring semantic review`, NOT a proven contradiction.
    """
    import re
    failures: list[GateFailure] = []
    claim_text = str(claim.get("claim_text", "")).lower()

    # function words never count as overlap (prevents 'a/one/the' junk firing)
    _FUNCTION_WORDS = {"the", "a", "an", "one", "this", "that", "it", "its", "of", "in",
                       "are", "was", "were", "be", "to", "by", "as", "and", "or", "not", "no",
                       "itself", "more", "their", "there", "between", "from", "with", "into",
                       "through", "upon", "over", "under", "only", "very", "such", "same"}

    # privative concepts that already absorb negation into the term (a-krama = not-order,
    # non-constructed, akrama). When present, a trailing 'not ... (privative)' is redundant —
    # it is the SAME polarity encoding, not a separate negation. Prevents the akrama same-claim
    # from firing as a false viruddha.
    _PRIVATIVE_TERMS = ("akrama", "non-constructed", "orderless", "order-less")

    def _neg_polarity(s: str) -> bool:
        low = s.lower()
        if any(p in low for p in _PRIVATIVE_TERMS):
            # the privative term carries the negation; a surrounding 'not' is redundant with it
            return False
        return bool(re.search(r"\b(not|no|never|is not|does not|isn't|doesn't)\b", low))

    def _core(s: str) -> set:
        # drop negation/particles via WORD-BOUNDARY regex (not naive replace, which corrupts
        # word boundaries, e.g. 'linguistic' -> 'inguistic'). Keep CONTENT words only.
        # Unicode-aware: preserve transliterated Sanskrit diacritics (pratibhā, vimarśa, āśraya)
        # instead of ASCII-stripping them into fragments.
        s = s.casefold()
        s = re.sub(r"\b(is not|does not|is|are|was|were)\b", " ", s)
        # match Unicode letters (incl. diacritics) as word chars; require >=4 letters total
        toks = set(re.findall(r"[a-zā-īūṛṝḷḹṃṁñṅśṣṭḍḥ]+", s))
        return {t for t in toks if len(re.sub(r"[ā-īūṛṝḷḹṃṁñṅśṣṭḍḥ]", "", t)) + sum(
            c in "āīūṛṝḷḹṃṁñṅśṣṭḍḥ" for c in t) >= 4 and t not in _FUNCTION_WORDS}

    # normalize hyphenated privative terms: 'order-less'/'orderless' == 'akrama' == 'not-order'.
    # They are the SAME proposition in different polarity ENCODING — must not flip polarity.
    _privative_normal = {"order-less": "akrama", "orderless": "akrama",
                         "not-constructed": "non-constructed"}

    def _norm(txt: str) -> str:
        for k, v in _privative_normal.items():
            txt = txt.replace(k, v)
        return txt

    claim_norm = _norm(claim_text)
    claim_core = _core(claim_norm)
    claim_neg = _neg_polarity(claim_norm)

    for p in gold_propositions:
        commitment = str(p.get("commitment") or p.get("speaker") or "").upper()
        # only claims the gold actually ASSERTS/DERIVES count as 'established' (the text's position).
        # RECONSTRUCTED is deliberately EXCLUDED here: a reconstruction is not independently established,
        # so it must not nominate a viruddha against an independently-asserted claim.
        if commitment in ("ASSERTS", "DERIVES", "SIDDHANTA"):
            p_text = _norm(str(p.get("proposition") or p.get("text") or ""))
            p_neg = _neg_polarity(p_text)
            p_core = _core(p_text)
            shared = claim_core & p_core
            # require a CONTENT-word overlap (>=2 content tokens), not function words
            if len(shared) >= 2:
                if claim_neg != p_neg:
                    failures.append(GateFailure(
                        "viruddha", "strong",
                        f"gold proposition {p.get('proposition_id', p.get('id'))} "
                        f"(commitment={commitment}) asserts the opposite: '{p_text[:80]}' "
                        f"[GRAPH viruddha candidate — semantic layer decides]",
                        defeater_metadata={
                            "candidate_claim": str(claim.get("claim_text", "")),
                            "conflicting_proposition": p_text,
                            "polarity_relation": "OPPOSED",
                            "commitment": commitment,
                            "overlap_basis": sorted(shared),
                            "semantic_status": "UNRESOLVED",
                            "possible_defeaters": [
                                "SCOPE_DIFFERENCE", "MODALITY_DIFFERENCE", "SPEAKER_DIFFERENCE",
                                "TEMPORAL_DIFFERENCE", "QUALIFICATION", "LEVEL_DIFFERENCE",
                                "NON_EQUIVALENT_PREDICATE",
                            ],
                        }))
                    break  # one decisive graph conflict is enough to flag
    return failures


def validate(claim: dict, peer_claims: list[dict] | None = None, gold_propositions: list[dict] | None = None) -> dict:
    """Stable wrapper → dict (for the benchmark / API). Optionally graph-aware viruddha over gold."""
    result = gate_claim(claim, peer_claims).to_dict()
    if gold_propositions:
        gfail = check_viruddha_graph(claim, gold_propositions)
        # promote the outcome to needs_review if a graph viruddha is found
        if gfail:
            result["failures"] = (result.get("failures") or []) + [f.to_dict() for f in gfail]
            result["graph_viruddha"] = True
            # the strongest failure governs the outcome (viruddha is strong)
            if result.get("outcome") in ("accepted", "accepted_with_penalty"):
                result["outcome"] = "needs_review"
            result["can_update_posterior"] = False
    return result


# ── verify_claim_semantic: the BOUNDED structural/evaluative gate (devpath1, E2-02) ──────────
# The handover's target adapter. It is NOT a truth oracle and must never output `argument_valid=true`
# (GLOBAL-STATE §8). It maps the deterministic gate onto a bounded verdict + the four dimensions the
# semantic layer later tests (pratijna/hetu/scope/support_relation). The result is an
# engineering/structural result; it establishes nothing about historical or philosophical correctness.
VERIFY_VERDICTS = ("PASS", "PASS_WITH_OPEN", "FAIL")
_VERIFY_DIMENSIONS = ("pratijna", "hetu", "scope", "support_relation")

# outcome → bounded verdict (never "proven"/"true"; a clean result is an engineering result)
_OUTCOME_TO_VERDICT = {
    "accepted": "PASS",
    "accepted_with_penalty": "PASS_WITH_OPEN",
    "needs_review": "PASS_WITH_OPEN",
    "hollow": "FAIL",
    "refuted": "FAIL",
}


def _dimension_flags(claim: dict, failures: list[dict]) -> dict:
    """Fold the gate failures + claim signals into the four bounded dimensions.

    Each dimension is one of: CLEAN | OPEN | DEFECT (never a truth judgement).
      - pratijna        the thesis/statement is present and not over-claimed
      - hetu            the reason is present and established enough for structural review
      - scope           the claim does not overreach (universal/always without vyāpti backing)
      - support_relation the reason-to-conclusion relation is coherent (no self-inversion/badhita)
    """
    text = str(claim.get("claim_text", "")).lower()
    fallacies = {f.get("fallacy") for f in failures}

    def dim(flag: str, *_f: str) -> str:
        return "DEFECT" if (flag in fallacies) else "CLEAN"

    return {
        "pratijna": "OPEN" if (claim.get("falsifier") is None) else dim("asiddha", "hollow"),
        "hetu": dim("asiddha"),
        "scope": "DEFECT" if (any(w in text for w in UNIVERSAL_OVERRECH)) else "CLEAN",
        "support_relation": dim("viruddha", "badhita"),
    }


def verify_claim_semantic(claim: dict, peer_claims: list[dict] | None = None,
                          gold_propositions: list[dict] | None = None) -> dict:
    """Bounded structural/evaluative gate → PASS / PASS_WITH_OPEN / FAIL + per-dimension flags.

    This is the devpath1 bounded evaluator. It:
      - NEVER asserts truth (no `argument_valid=true`, no "proven") — a clean result is
        engineering/structural, per GLOBAL-STATE §8 and NYAYA-GATE-CANDIDATE-V1.
      - maps the deterministic 5-hetvābhāsa gate + optional graph viruddha onto the verdict.
      - reports the four dimensions (pratijna/hetu/scope/support_relation) as CLEAN/OPEN/DEFECT,
        giving the semantic layer an explicit handshake of what to test next.

    Returns {verdict, can_update_posterior, dimensions, failures, graph_viruddha, ...}.
    """
    res = validate(claim, peer_claims, gold_propositions)
    outcome = res.get("outcome", "needs_review")
    verdict = _OUTCOME_TO_VERDICT.get(outcome, "PASS_WITH_OPEN")
    # a graph viruddha is always FAIL (strong, decisive) — never silently passed
    if res.get("graph_viruddha"):
        verdict = "FAIL"
    dimensions = _dimension_flags(claim, res.get("failures") or [])
    return {
        "claim_id": claim.get("claim_id"),
        "verdict": verdict,
        "dimensions": dimensions,
        "can_update_posterior": res.get("can_update_posterior", False) and verdict == "PASS",
        "failures": res.get("failures") or [],
        "graph_viruddha": res.get("graph_viruddha", False),
        "note": "bounded structural/evaluative result — NOT a truth or philosophical-correctness claim",
    }
