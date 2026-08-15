"""lib/organism.py — the Pāṭala organism layer (Layer 09, from patala organism vision).

The consumer app becomes a SENSOR for what humans fail to understand. Key objects:
  UserKnowledgeState — per-user epistemic state (concept mastery, arguments understood, confusions)
  MisconceptionGraph — structured demand + misconception data feeding the flywheel

The magic edges (from the vision): Question──about──>Concept · Confusion──misreads──>Claim ·
Objection──attacks──>Premise.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class UserKnowledgeState:
    user_id: str
    interests: dict = field(default_factory=dict)            # topic -> interest (0-1)
    concept_mastery: dict = field(default_factory=dict)      # concept -> mastery (0-1)
    arguments_understood: dict = field(default_factory=dict) # arg_id -> strong/partial
    known_confusions: list = field(default_factory=list)     # [(wrong, correct)]
    questions_asked: list = field(default_factory=list)
    positions_explored: list = field(default_factory=list)

    def record_interaction(self, concept, correct, mastery_delta=0.05):
        if correct:
            self.concept_mastery[concept] = min(1.0, self.concept_mastery.get(concept, 0) + mastery_delta)
        else:
            self.concept_mastery[concept] = max(0.0, self.concept_mastery.get(concept, 0) - mastery_delta * 2)
        return self.concept_mastery[concept]


@dataclass
class MisconceptionNode:
    wrong_concept: str
    correct_concept: str
    failure_type: str = ""
    learner_count: int = 0
    explanation: str = ""


class MisconceptionGraph:
    """The demand + misconception graph: learner mistakes as structured data."""
    def __init__(self):
        self.nodes = {}          # (wrong, correct) -> MisconceptionNode
        self.question_edges = [] # Question about Concept
        self.confusion_edges = []  # Confusion misreads Claim
        self.objection_edges = []  # Objection attacks Premise

    def record_confusion(self, wrong, correct, failure_type=""):
        key = (wrong, correct)
        if key not in self.nodes:
            self.nodes[key] = MisconceptionNode(wrong, correct, failure_type)
        self.nodes[key].learner_count += 1
        self.confusion_edges.append((wrong, correct))

    def record_objection(self, objection, premise):
        self.objection_edges.append((objection, premise))

    def top_misconceptions(self, n=3):
        return sorted(self.nodes.values(), key=lambda x: -x.learner_count)[:n]

    def demand_signals(self):
        """What the flywheel consumes: which confusions are most frequent, which objections attack which premises."""
        return {
            "most_confused": [(w, c) for w, c, _ in [(k[0], k[1], v.learner_count) for k, v in self.nodes.items()]],
            "objections": self.objection_edges,
            "n_misconceptions": len(self.nodes),
        }
