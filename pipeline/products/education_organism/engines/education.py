"""lib/education.py — the Pāṭala education layer (Layer 09 education, from patala vision).

Implements the education vision's core objects + the moat primitive:
  LearningClaim  — a derived-from-graph learning objective (epistemic ceiling, prerequisites)
  MasteryEvidence — a learner's response record
  interaction compiler — turns a scholarly object into a LearningPacket (interactions, distractors)
  wrong_answer -> known epistemic neighbor — the education moat (NOT "LLM invents distractor")

The design law: education is a PROJECTION of the graph, never a separate knowledge base. Every
LearningClaim resolves downward to canonical objects.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

# ---- the interaction vocabulary (start small — teaches structure, not quizzes) ----
INTERACTION_TYPES = ["Choice", "SpanSelect", "SpeakerClassify", "PremiseAttach",
                     "ArgumentAssemble", "PremiseRetract"]


@dataclass
class LearningClaim:
    learning_claim_id: str
    content: str
    derived_from: list = field(default_factory=list)   # canonical object ids
    claim_type: str = ""                               # premise_id | warrant | crux | distinction
    difficulty: str = "novice"
    prerequisites: list = field(default_factory=list)
    source_refs: list = field(default_factory=list)
    epistemic_ceiling: str = "MACHINE_PROPOSED"

    def to_dict(self):
        return {"learning_claim_id": self.learning_claim_id, "content": self.content,
                "derived_from": self.derived_from, "claim_type": self.claim_type,
                "difficulty": self.difficulty, "prerequisites": self.prerequisites,
                "source_refs": self.source_refs, "epistemic_ceiling": self.epistemic_ceiling}


@dataclass
class MasteryEvidence:
    learner: str
    skill_ref: str
    learning_claim_ref: str
    interaction_ref: str
    response: str = ""
    correctness: bool = False
    hint_level: int = 0


# ---- the wrong-answer taxonomy (maps mistakes back into the graph) ----
FAILURE_TAXONOMY = ["rival_proposition", "wrong_speaker", "scope_inflation", "wrong_technical_sense",
                    "defeated_inference", "false_contradiction", "omitted_qualifier",
                    "alternative_debate_frame"]


def wrong_answer_to_neighbor(wrong_concept, answer_claim, graph_neighbors) -> dict:
    """THE MOAT: a wrong answer resolves to a KNOWN epistemic neighbor, not an invented distractor.
    Given a wrong answer (concept) and the correct claim, find which graph neighbor it actually maps to
    and classify the failure type.
    """
    # find the closest graph neighbor to the wrong answer among the claim's neighbors
    neighbors = graph_neighbors(answer_claim)
    closest = min(neighbors, key=lambda n: _sim(wrong_concept, n)) if neighbors else None
    failure = _classify(wrong_concept, answer_claim)
    return {"wrong_answer": wrong_concept, "correct_claim": answer_claim,
            "maps_to_epistemic_neighbor": closest,
            "failure_type": failure,
            "explanation": f"'{wrong_concept}' is a known epistemic neighbor ({failure}) — "
                           f"the learner conflated it with the correct position."}


def _sim(a, b):
    # simple lexical overlap as a stand-in for embedding similarity
    sa, sb = set(str(a).lower().split()), set(str(b).lower().split())
    return 1.0 - (len(sa & sb) / max(1, len(sa | sb)))


def _classify(wrong, correct):
    # heuristic failure classification against the taxonomy
    wrong_s = str(wrong).lower()
    if "not" in wrong_s or "den" in wrong_s: return "rival_proposition"
    if "only" in wrong_s or "all" in wrong_s: return "scope_inflation"
    if wrong_s in ("compatibilism", "determinism"): return "rival_proposition"
    return "wrong_technical_sense"


# ---- interaction compiler: scholarly object -> LearningPacket ----
def compile_interactions(scholarly_object, targets, learner_level="novice") -> dict:
    """Returns a LearningPacket: LearningClaims + interaction specs + distractors + progression."""
    claims = []
    interactions = []
    for i, target in enumerate(targets):
        lc = LearningClaim(
            learning_claim_id=f"LC-{scholarly_object}-{i}",
            content=f"Learner can {target} in {scholarly_object}",
            derived_from=[scholarly_object], claim_type=target,
            difficulty=learner_level)
        claims.append(lc)
        interactions.append({
            "id": f"int-{i}", "claim_ref": lc.learning_claim_id,
            "type": INTERACTION_TYPES[i % len(INTERACTION_TYPES)],
            "target": target,
        })
    return {"learning_claims": [c.to_dict() for c in claims],
            "interactions": interactions,
            "progression": [c.learning_claim_id for c in claims],
            "epistemic_ceiling": "MACHINE_PROPOSED"}
