"""lib/misconception.py — the repair cascade (DEV_PLAN §1.1, closes the organism's flywheel).

MisconceptionLikelihood = f(cluster_size, persistence, ambiguity_signal, novice_rate)
  -> cross threshold -> source flagged for scholar review
  -> RKA propagate fix -> confusion measured to dissolve.

This is the kernel that closes the organism loop (SPEC-20/21/29 + DEV_PLAN Phase 1.1): a misconception
detected across many learners, persisting across exposures, with a high novice rate and ambiguity in the
teaching signal, is a signal to flag the SOURCE (claim/passage/explanation) for scholar review, then
propagate the fix downstream (the RKA blast-radius: a corrected fact re-queues every dependent
explanation), then measure whether the confusion dissolves.

Reuses lib/staleness.blast_radius (the RKA dependency walk) — never re-implement the propagation.
Grounded in: organism.py (MisconceptionGraph), pedagogy.py (distractors from epistemic neighbors),
SPEC-20 (wrong_answer_to_neighbor), SPEC-21 (Gap Engine), SPEC-29 (Misconception as first-class).
"""
from __future__ import annotations

from staleness import build_dependency_index, blast_radius


def misconception_likelihood(cluster_size, persistence, ambiguity_signal, novice_rate,
                             w=(0.3, 0.3, 0.2, 0.2)):
    """MisconceptionLikelihood in [0,1] = weighted signal that a confusion is a REAL misconception
    (structural, reproducible) vs an isolated learner error.

    cluster_size  : how many distinct learners/responses share the same confusion (0+)
    persistence   : how many exposures the confusion survived unchanged (0+)
    ambiguity_signal : how ambiguous the teaching/evidence is (0..1); a muddy source hides confusion
    novice_rate   : fraction of novices hitting it (0..1)
    Returns a real 0..1 score. A HIGH score = flag the source for scholar review.
    """
    c, p, a, n = w
    # normalize cluster_size/persistence into [0,1] via a soft saturating scale
    cs = 1.0 if cluster_size <= 0 else min(1.0, cluster_size / 25.0)
    ps = 1.0 if persistence <= 0 else min(1.0, persistence / 8.0)
    score = c * cs + p * ps + a * ambiguity_signal + n * novice_rate
    return round(min(1.0, score), 3)


class Misconception:
    """A first-class misconception: a confusion with its signal, review flag, and dissolution state."""

    def __init__(self, claim_id, confusion, *, cluster_size=0, persistence=0, ambiguity_signal=0.0,
                 novice_rate=0.0, threshold=0.7):
        self.claim_id = claim_id
        self.confusion = confusion
        self.cluster_size = cluster_size
        self.persistence = persistence
        self.ambiguity_signal = ambiguity_signal
        self.novice_rate = novice_rate
        self.threshold = threshold
        self.likelihood = misconception_likelihood(
            cluster_size, persistence, ambiguity_signal, novice_rate)
        self.flagged = self.likelihood >= threshold
        self.review_state = "FLAGGED_FOR_REVIEW" if self.flagged else "MONITORING"


class MisconceptionRepairCascade:
    """The repair cascade: flag -> propagate fix -> measure dissolution.

    Given a dependency graph (which explanations/claims depend on a source claim), a misconception
    above threshold flags the source for scholar review; the fix, once applied, is propagated through
    the RKA blast-radius to every dependent explanation (marking them stale); dissolution is then
    measured as the confusion's likelihood dropping below threshold after re-exposure.
    """

    def __init__(self, dag=None, threshold=0.7):
        # dag: {claim/layer_id: {'requires': [upstream_ids]}} — the canonical DAG shape.
        # The index is built via staleness.build_dependency_index (upstream -> downstream) so that
        # blast_radius can walk downstream. Reuse, don't rebuild.
        self.dag = dag or {}
        self.depends_on = build_dependency_index(self.dag)
        self.threshold = threshold
        self.misconceptions = {}
        self.propagated_stale = set()
        self.dissolved = []

    def record(self, claim_id, confusion, **signals):
        """Record/update a misconception for a claim; flag if above threshold."""
        m = Misconception(claim_id, confusion, threshold=self.threshold, **signals)
        self.misconceptions[claim_id] = m
        return m

    def flag_for_review(self):
        """Return all misconceptions currently above threshold (flagged for scholar review)."""
        return [m for m in self.misconceptions.values() if m.flagged]

    def propagate_fix(self, source_claim_id):
        """After the source is corrected, propagate staleness to every downstream dependent
        (RKA blast-radius). Returns the set of now-stale dependent ids."""
        # blast_radius(depends_on, changed) walks downstream from the changed node
        stale = blast_radius(self.depends_on, {source_claim_id})
        stale.discard(source_claim_id)
        self.propagated_stale |= stale
        return stale

    def measure_dissolution(self, claim_id, **new_signals):
        """Re-measure a confusion after the fix; record it dissolved if it now falls below threshold."""
        old = self.misconceptions.get(claim_id)
        if old is None:
            return None
        new = Misconception(claim_id, old.confusion, threshold=self.threshold, **new_signals)
        dissolved = new.likelihood < self.threshold and old.likelihood >= self.threshold
        new.review_state = "DISSOLVED" if dissolved else new.review_state
        self.misconceptions[claim_id] = new
        if dissolved:
            self.dissolved.append({"claim_id": claim_id, "before": old.likelihood,
                                   "after": new.likelihood})
        return new

    def summary(self):
        flagged = len(self.flag_for_review())
        return {
            "total": len(self.misconceptions),
            "flagged_for_review": flagged,
            "propagated_stale": len(self.propagated_stale),
            "dissolved": len(self.dissolved),
            "below_threshold": sum(1 for m in self.misconceptions.values() if not m.flagged),
        }
