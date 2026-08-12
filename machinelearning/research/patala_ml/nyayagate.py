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

    def to_dict(self) -> dict:
        return {"fallacy": self.fallacy, "severity": self.severity, "rationale": self.rationale}


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
    """
    import re
    failures: list[GateFailure] = []
    claim_text = str(claim.get("claim_text", "")).lower()

    # normalize: strip 'not'/negation so we can test opposite-polarity overlap
    def _neg_polarity(s: str) -> bool:
        return bool(re.search(r"\b(not|no|never|is not|does not|isn't|doesn't)\b", s.lower()))

    def _core(s: str) -> str:
        # drop common negation words + particles for overlap matching
        s = s.lower()
        for w in [" not ", " no ", " never ", " is not ", " does not ", " the ", " a ", " an ",
                  " that ", " this ", " is ", " are ", " was ", " were "]:
            s = s.replace(w, " ")
        return re.sub(r"[^a-z ]", " ", s)

    claim_core = _core(claim_text)
    claim_neg = _neg_polarity(claim_text)

    for p in gold_propositions:
        commitment = str(p.get("commitment") or p.get("speaker") or "").upper()
        # only claims the gold actually ASSERTS/DERIVES count as 'established' (the text's position)
        if commitment in ("ASSERTS", "DERIVES", "RECONSTRUCTED", "SIDDHANTA", "ASSERTS_FOR_ARGUMENT"):
            p_text = str(p.get("proposition") or p.get("text") or "")
            p_neg = _neg_polarity(p_text)
            p_core = _core(p_text)
            # tokens shared between the claim and the gold proposition
            shared = set(claim_core.split()) & set(p_core.split())
            if len(shared) >= 3:
                # opposite polarity on an overlapping subject → the gold argues the opposite
                if claim_neg != p_neg:
                    failures.append(GateFailure(
                        "viruddha", "strong",
                        f"gold proposition {p.get('proposition_id', p.get('id'))} "
                        f"(commitment={commitment}) asserts the opposite: '{p_text[:80]}' "
                        f"[GRAPH viruddha candidate — semantic layer decides]"))
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
