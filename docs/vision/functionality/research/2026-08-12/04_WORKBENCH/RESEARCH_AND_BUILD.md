# Project 04 — Pāṭala Workbench

## Thesis
The Workbench is not the wedge. It is the eventual high-lock-in environment where scholars create research directly inside Pāṭala’s evidence/argument graph.

Change the workflow from:
`write prose → later reconstruct sources/reasoning`
to:
`ResearchQuestion → evidence → readings → terms → propositions → arguments → counterevidence → cruxes → review → prose/export`.

## Mature systems to mine rather than rebuild

### INCEpTION
https://github.com/inception-project/inception

This is the strongest precedent for the human/machine annotation loop:
- multi-user annotation;
- configurable layers;
- machine recommendations;
- human correction;
- knowledge bases;
- adjudication;
- project-oriented workflow.

Copy the interaction principle: machine suggestion is visually and structurally distinct from accepted annotation, and user corrections become structured data.

Do not inherit its entire generic NLP backend unless necessary.

### Hypothesis
Backend:
https://github.com/hypothesis/h

Client:
https://github.com/hypothesis/client

Useful for robust span annotation, provenance, discussion and browser/PDF interaction. Pāṭala should anchor canonically to stable Pāṭala refs rather than only URL/text quotes.

### ORKG
Docs:
https://docs.orkg.org/

Backend:
https://github.com/TIBHannover/orkg-backend

Python client docs:
https://orkg.readthedocs.io/en/latest/introduction.html

Academy:
https://academy.orkg.org/

ORKG validates the broad thesis that research contributions should be structured and machine-actionable, with comparisons/templates/graph views. Pāṭala’s differentiation is philological grounding, historically situated semantics, argument-under-interpretation and executable corrections.

### Recogito
https://recogito.abm.uu.se/

Useful humanities UX precedent: shared collections, text/image annotation, collaboration, provenance/version history.

## Scholarly graph literature

Semantic Scholar Open Data:
https://arxiv.org/abs/2301.10140

Do not rebuild general academic citation discovery; integrate it later.

NLPContributionGraph:
https://arxiv.org/abs/2106.07385

Warning: end-to-end structured scholarly extraction remains hard. This reinforces gold-first/human-correction design.

LLM + scholarly KG query processing:
https://arxiv.org/abs/2405.15374

LLM + cognitive KG/ORKG:
https://arxiv.org/abs/2409.06433

These support natural-language graph querying and expert-verified graph data as a basis for better structured extraction.

## Product references
Elicit:
https://elicit.com/

ResearchRabbit:
https://www.researchrabbit.ai/

Do not compete on broad literature search. Borrow:
- traceable research workflows;
- seed→explore interaction;
- collections;
- visual navigation.

Pāṭala’s seed should be a passage/term/proposition/ResearchQuestion—not merely a paper.

## Object-first UX

Primary workspace root: `ResearchQuestion`.

Suggested navigation:
- Evidence
- Readings
- Terms
- Propositions
- Positions
- Arguments
- Counterevidence
- Cruxes
- Review history
- Outputs

Core surface:
- source viewer;
- evidence tray;
- graph;
- reading comparison;
- machine proposals;
- review controls;
- impact preview.

## Typed scholar actions
Every meaningful interaction should become an event/object:
- ADD_EVIDENCE
- PROPOSE_TRANSLATION
- PROPOSE_TERM_SENSE
- PROPOSE_PROPOSITION
- ATTRIBUTE_COMMITMENT
- ADD_SUPPORT
- ADD_ATTACK
- ADD_RIVAL_READING
- MARK_SCOPE
- OPEN_QUESTION
- ACCEPT / REJECT / REVISE / ABSTAIN

This event stream is the moat. A generic AI text editor is not.

## Workbench versions
v0: tiny reviewer screen only—object, evidence, current state, proposal, impact, submit.
v1: ResearchQuestion workspace + pinned sources + term dossier + argument map + rival position + output renderer.
v2: collaboration, permissions, adjudication, ORCID/CRediT/export/interoperability.

Do not start with dashboards, social features, discovery networks or gamification.

## Interoperability
Potential adapters:
- Hypothesis/W3C-like annotation concepts;
- xAIF for argument exchange;
- ORKG contribution export;
- TEI for textual/manuscript layers;
- JSON-LD/RDF only where external interoperability justifies it.

Never let an external interchange format force the canonical Pāṭala ontology.
