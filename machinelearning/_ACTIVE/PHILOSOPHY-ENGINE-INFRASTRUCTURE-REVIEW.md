# SUPERSEDED AS WORKING DOC — External infrastructure review (input, not current)

> **⚠️ Reference input only.** This external review's "delegate to py-aspic/xAIF/oAMF/ALIAS, own the thin IR" is
> the *direction*, but its full Phase0–10 build order describes a finished engine and is aspirational. It is
> **reconciled into `machinelearning/_ACTIVE/ARGUMENT-IR-VISION.md`** (gold-first: build ARG-001..005, let the gold
> force the ontology). Superseded as the working doc by `ARGUMENT-IR-VISION.md` + `BRAINSTORM-PHILOSOPHY-ENGINE-VS-PATALA.md`.

I checked the current repositories and papers against the architecture we just designed. The main conclusion is: **Pāṭala should own the philosophical intermediate representation and provenance layer, while delegating standard argumentation computation, interchange, and much of argument mining to existing infrastructure.** ASPIC+, Dung-style semantics, xAIF, and LLM argument-mining already have usable implementations. ([GitHub][1])

## 1. Repositories and papers worth using

1. **py-aspic — primary structured argumentation backend**

   GitHub:
   [https://github.com/arg-tech/py-aspic](https://github.com/arg-tech/py-aspic)

   `py-aspic` implements ASPIC+ with strict/defeasible rules, rule preferences, contrariness, knowledge bases, and argumentation theories. It already exposes exactly the machinery we would otherwise have to implement ourselves. ([GitHub][1])

   **Use in Pāṭala:** build an adapter:

   ```text
   Patala Proposition
       → pyAspic formula

   Patala InferenceRule(strict)
       → pyAspic Rule.STRICT

   Patala InferenceRule(defeasible)
       → pyAspic Rule.DEFEASIBLE

   Patala Preference
       → add_rule_preference()

   Patala opposition/contrary
       → contrariness

   Patala EpistemicRegime
       → selected KB + rule/preference configuration
   ```

   Do **not** use py-aspic objects as Pāṭala's persistent schema. Treat it as an evaluator.

---

2. **xAIF — standard interchange**

   GitHub:
   [https://github.com/arg-tech/xaif](https://github.com/arg-tech/xaif)

   xAIF library docs/tutorial:
   [https://github.com/arg-tech/xaif/blob/main/docs/tutorial.md](https://github.com/arg-tech/xaif/blob/main/docs/tutorial.md)

   It provides Python tooling for AIF/xAIF JSON, including nodes, edges, locutions, participants and scheme structures. ([GitHub][2])

   **Use:**

   ```text
   Patala IR
      ↓
   export_xaif()
      ↓
   external argument tools/datasets

   xAIF
      ↓
   import_xaif()
      ↓
   candidate Patala objects
   ```

   This gives Pāṭala interoperability without constraining our ontology to AIF's model.

---

3. **oAMF — argument-mining orchestration framework**

   GitHub:
   [https://github.com/arg-tech/oAMF](https://github.com/arg-tech/oAMF)

   oAMF already orchestrates argument-mining modules and uses xAIF as its standard interchange representation. ([GitHub][3])

   **Use:** prototype the extraction side.

   ```text
   source commentary
       ↓
   oAMF / AM modules
       ↓
   xAIF candidate graph
       ↓
   Pāṭala enrichment
       ↓
   commitments + warrants + alignments + provenance
   ```

   We should test it before building our own generic AM orchestration layer.

---

4. **ARG-tech AIF datasets — training/evaluation corpus**

   GitHub:
   [https://github.com/arg-tech/aif-arg-datasets](https://github.com/arg-tech/aif-arg-datasets)

   This repository collects argumentation datasets using the AIF ecosystem. ([GitHub][4])

   **Use:** external benchmark data.

   Pāṭala Benchmark should have two tiers:

   ```text
   GENERIC ARGUMENTATION
   existing AIF / AM datasets

   HISTORICAL PHILOSOPHY
   our hand-reviewed IPVV gold
   ```

   This lets us distinguish:

   > “our extractor is bad at argument mining”

   from:

   > “ordinary argument mining does not capture historical philosophy.”

---

5. **Argumentative LLMs — closest architecture precedent**

   GitHub:
   [https://github.com/CLArg-group/argumentative-llms](https://github.com/CLArg-group/argumentative-llms)

   ArXiv:
   [https://arxiv.org/abs/2405.02079](https://arxiv.org/abs/2405.02079)

   ArgLLMs use an LLM to construct explicit argumentation frameworks and then reason formally over those structures, specifically so conclusions can be explained and contested. ([GitHub][5])

   **Use:** study and adapt the separation:

   ```text
   LLM
   = proposes argumentative structure

   formal argumentative layer
   = evaluates structure
   ```

   Their repo contains the argument miner, prompts, LLM managers, uncertainty estimation and experiment infrastructure. ([GitHub][5])

   This should strongly influence Pāṭala's AI reasoning service.

---

6. **DAMO LLM Computational Argumentation benchmark**

   GitHub:
   [https://github.com/DAMO-NLP-SG/LLM-argumentation](https://github.com/DAMO-NLP-SG/LLM-argumentation)

   Their ACL 2024 code standardizes multiple computational-argumentation tasks and datasets and provides zero/few-shot evaluation infrastructure. ([GitHub][6])

   **Use:** steal the benchmarking approach, not the ontology.

   We can add Pāṭala tasks beside their conventional tasks:

   ```text
   claim detection
   relation classification
   argument mining

   +

   commitment classification
   warrant reconstruction
   semantic alignment
   scope mismatch
   historical attribution
   crux detection
   ```

---

7. **An LLM-Based System for Argument Mining**

   ArXiv:
   [https://arxiv.org/abs/2605.13793](https://arxiv.org/abs/2605.13793)

   It develops an end-to-end LLM pipeline for reconstructing argument structures rather than relying on one monolithic extraction operation. ([arXiv][7])

   **Use:** methodological precedent for our staged extractor:

   ```text
   segmentation
   → proposition
   → commitment
   → relation
   → warrant
   → alignment
   → validation
   ```

   I would not collapse these into one LLM call.

---

8. **From Argumentative Text to Argument Knowledge Graph**

   ArXiv:
   [https://arxiv.org/abs/2506.00713](https://arxiv.org/abs/2506.00713)

   This moves from argument components/relations to a knowledge base, uses explicit inference rules, constructs arguments and then builds an argument knowledge graph. It also specifically addresses implicit rules and undercutting attacks. ([arXiv][8])

   **Use:** probably the closest paper to our **Argument IR → Argument Graph** layer.

   Compare our ontology against theirs when implementing `InferenceRule`, `InferenceApplication` and `Attack`.

---

9. **ALIAS — Dung abstract argumentation**

   GitHub:
   [https://github.com/Open-Argumentation/ALIAS](https://github.com/Open-Argumentation/ALIAS)

   It implements abstract argumentation frameworks and Dung-style evaluation semantics in Python. ([GitHub][9])

   **Use:** optional lightweight evaluator:

   ```text
   structured Pāṭala graph
        ↓ collapse
   abstract arguments + attacks
        ↓
   ALIAS
        ↓
   extension / acceptability result
   ```

   But py-aspic is more important because it retains internal argument structure. ALIAS should be an optional abstract-semantics adapter.

---

10. **Carneades 4 — workbench precedent**

GitHub:
[https://github.com/carneades/carneades-4](https://github.com/carneades/carneades-4)

Project:
[https://carneades.github.io/](https://carneades.github.io/)

Carneades is an established argument reconstruction, mapping, evaluation and interchange system. ([GitHub][10])

**Use:** interface and conceptual precedent.

I would **not** make it a runtime dependency. Study how it represents and visually communicates complex argumentative structures.

---

11. **Debate Map — UI precedent**

GitHub:
[https://github.com/debate-map/app](https://github.com/debate-map/app)

Site:
[https://debatemap.app](https://debatemap.app)

Debate Map provides an open-source claim/argument graph interface with ratings, tags and belief-tree-style functionality. ([GitHub][11])

**Use:** steal UI lessons for Scholar Workbench:

```text
collapse/expand argument branches
supporting/opposing branches
inspect node metadata
navigate chains
```

But Pāṭala's graph must be substantially richer.

---

12. **ACAL — multi-agent + quantitative argumentation prototype**

GitHub:
[https://github.com/loc110504/ACAL](https://github.com/loc110504/ACAL)

ArXiv:
[https://arxiv.org/abs/2602.18916](https://arxiv.org/abs/2602.18916)

ACAL combines multi-agent LLM reasoning with a quantitative bipolar argumentation framework and includes editable reasoning graphs and conflict-resolution machinery. Its code exposes graph, node, QBAF scoring, agents, RAG and semantic-relation modules. ([GitHub][12])

**Use:** experiment/reference only.

Especially inspect:

```text
graph.py
node.py
semantic_relation_analyzer.py
qbaf_scorer.py
legal_agents.py
```

But **do not adopt quantitative scores as Pāṭala's primary epistemology**.

---

13. **Deep Arguing**

ArXiv:
[https://arxiv.org/abs/2605.10569](https://arxiv.org/abs/2605.10569)

This is a current neuro-symbolic design where neural models construct argumentation structures and differentiable argumentation semantics participate in learning. ([arXiv][13])

**Use later**, when Pāṭala has enough gold data.

It gives a research direction for:

```text
learned structure construction
+
symbolic argumentative constraints
```

not for v1.

---

14. **GNNs for abstract argument acceptance**

ArXiv:
[https://arxiv.org/abs/2404.18672](https://arxiv.org/abs/2404.18672)

This tests GCN/GAT architectures for approximating argument acceptability. ([arXiv][14])

**Use later as a baseline** if exact argument evaluation becomes computationally expensive.

Do not use it instead of exact reasoning for our initial small debate graphs.

---

15. **Heterogeneous GNNs for Assumption-Based Argumentation**

ArXiv PDF:
[https://arxiv.org/pdf/2511.08982](https://arxiv.org/pdf/2511.08982)

This work explicitly models assumptions, claims and rules as different node types, with support/derive/attack as heterogeneous edge types, then applies GCN/GAT-style learning. ([arXiv][15])

This is extremely relevant to our future graph ML representation.

Our equivalent eventually becomes:

```text
Proposition nodes
Rule nodes
Inference nodes
Commitment nodes
Crux nodes

grounding
derives
attacks
aligns
commits
supports
```

---

16. **Toward AI Agents That Reason With Us, Not For Us**

ArXiv:
[https://arxiv.org/abs/2603.15946](https://arxiv.org/abs/2603.15946)

The paper explicitly discusses editable external argument graphs and computational argumentation as a way for users to modify the reasoning structure and observe changes in outcomes. ([arXiv][16])

**Use:** design philosophy for the Scholar Workbench.

Users should be able to say:

```text
reject this premise
change this alignment
remove this warrant
accept this Buddhist assumption
```

and see what changes downstream.

---

17. **Argument mining survey**

ArXiv:
[https://arxiv.org/abs/2506.16383](https://arxiv.org/abs/2506.16383)

This surveys LLM argument mining, datasets, tasks, prompting, fine-tuning, retrieval and current evaluation issues. ([arXiv][17])

**Use:** literature map and benchmark-design reference rather than runtime infrastructure.

---

18. **Awesome LLM Computational Argumentation**

GitHub:
[https://github.com/KashiwaByte/Awesome-LLM-Computational-Argumentation](https://github.com/KashiwaByte/Awesome-LLM-Computational-Argumentation)

This is a useful continuously maintained index of argumentation papers, datasets and benchmarks in the LLM era. ([GitHub][18])

**Use:** literature monitoring.

---

# Review of our previous ontology

Our previous 13-object design was directionally right:

```text
Proposition
Commitment
DebateFrame
SemanticAlignment
EpistemicRegime
ArgumentScheme
InferenceRule
InferenceApplication
Argument
Attack
Preference
EvaluationState
Crux
```

After looking at the available infrastructure, I would make **three corrections**.

### Correction 1 — `EvaluationState` should not be canonical data

It is derived.

The persistent object should be:

```ts
EvaluationProfile
```

which specifies:

```text
frame
epistemic regime
argumentation semantics
preference policy
logic
alignment version
```

Then:

```text
evaluate(graph, profile)
→ EvaluationState
```

That makes evaluations reproducible rather than treating their result as a fact about the argument.

---

### Correction 2 — don't duplicate ASPIC+

Our previous `InferenceRule`, `Attack` and `Preference` concepts are correct, but Pāṭala doesn't need its own bespoke computational semantics for all of them.

Our IR should be able to express them, but:

```text
Patala IR
   ↓ adapter
ASPIC+
   ↓
attack/defeat computation
```

should do standard structured argumentation.

Pāṭala-specific computation begins where ASPIC+ stops:

```text
semantic alignment
historical commitment
textual grounding
epistemic regimes
cross-tradition comparison
counterfactual dependency
crux extraction
```

---

### Correction 3 — `Warrant` survives, but as scholarly content inside `InferenceRule`

We don't need:

```text
Warrant
InferenceRule
```

as two independent primary objects.

Instead:

```ts
interface InferenceRule {
    id;

    warrant_text;
    logical_pattern?;

    strictness:
        STRICT | DEFEASIBLE;

    scheme_id?;

    grounding[];

    explicitness:
        EXPLICIT | RECONSTRUCTED | IMPLICIT;

    review_status;
}
```

This retains the philosophically crucial warrant while mapping naturally onto ASPIC+ rules.

---

# The final architecture I would actually build

The key is to have **one thin Pāṭala-owned philosophical IR**, not another entire argumentation framework.

```text
                         EXISTING PĀṬALA
                               │
             Sanskrit / edition / passage / translation
                               │
                        C1 / assertions
                               │
                               ▼
                    PHILOSOPHICAL EXTRACTION
                               │
                LLM + oAMF-style pipeline
                               │
                               ▼
                 ┌──────────────────────────┐
                 │   PĀṬALA PHILOSOPHY IR │
                 └──────────────────────────┘
                               │
       ┌───────────────────────┼─────────────────────────┐
       │                       │                         │
       ▼                       ▼                         ▼
    xAIF adapter           ASPIC+ adapter            Formal adapter
       │                       │                         │
       ▼                       ▼                         ▼
     xaif                  py-aspic                 Lean / Z3 later
       │                       │
       ▼                       ▼
interoperability        attacks / defeats /
                       acceptability / preferences
                               │
                               ▼
                    PĀṬALA ANALYSIS LAYER
                               │
           ┌───────────────────┼──────────────────┐
           ▼                   ▼                  ▼
    dependency tracing    counterfactuals      crux extraction
           │                   │                  │
           └───────────────────┼──────────────────┘
                               ▼
                       SCHOLAR WORKBENCH
```

## The persistent Pāṭala IR

I would freeze **12 canonical objects**.

```text
1. Proposition
2. Commitment
3. DebateFrame
4. SemanticAlignment
5. EpistemicRegime
6. ArgumentScheme
7. InferenceRule
8. InferenceApplication
9. Argument
10. Attack
11. Preference
12. Crux
```

And one configuration object:

```text
EvaluationProfile
```

Everything else should be derived.

---

## 1. `Proposition`

Not an RDF triple.

```ts
interface Proposition {
  id: string;

  canonical_text: string;

  semantic_form?: FormulaRef;

  concept_occurrences: ConceptOccurrence[];

  scope?: Scope;
  modality?: Modality;

  grounding: Grounding[];

  reconstruction_status:
    | "EXPLICIT"
    | "RECONSTRUCTED"
    | "IMPLICIT";

  review_status: ReviewStatus;
}
```

The formal representation is optional and versioned.

---

## 2. `Commitment`

Essential for historical philosophy.

```ts
interface Commitment {
  id: string;

  agent: EntityRef;
  proposition_id: PropositionId;

  force:
    | "ASSERTS"
    | "DENIES"
    | "PRESUPPOSES"
    | "CONCEDES"
    | "ASSUMES_FOR_ARGUMENT"
    | "ATTRIBUTES_TO_OPPONENT"
    | "REPORTS"
    | "QUOTES"
    | "RECONSTRUCTED";

  context: Ref[];
  grounding: Grounding[];

  review_status: ReviewStatus;
}
```

This is one of Pāṭala's genuinely distinctive pieces.

---

## 3. `DebateFrame`

```ts
interface DebateFrame {
  id: string;

  question: string;

  targets: ConceptRef[];

  level:
    | PHENOMENOLOGICAL
    | EPISTEMIC
    | SEMANTIC
    | CAUSAL
    | METAPHYSICAL
    | METHODOLOGICAL;

  scope: Scope;

  shared_ground: PropositionId[];
  contested_ground: PropositionId[];

  review_status: ReviewStatus;
}
```

A frame itself must be challengeable.

---

## 4. `SemanticAlignment`

This is another major Pāṭala-specific contribution.

```ts
interface SemanticAlignment {
  id: string;

  left: ConceptOccurrenceRef;
  right: ConceptOccurrenceRef;

  relation:
    | IDENTICAL_SENSE
    | NEAR_EQUIVALENT
    | SUBSUMES
    | SUBSUMED_BY
    | PARTIAL_OVERLAP
    | ANALOGICAL
    | CONTRASTIVE
    | FALSE_FRIEND
    | UNKNOWN;

  grounding: Grounding[];

  review_status: ReviewStatus;
}
```

**Conflict detection is forbidden before relevant alignments are evaluated.**

---

## 5. `EpistemicRegime`

```ts
interface EpistemicRegime {
  id: string;

  name: string;

  admissible_evidence: EvidenceClass[];

  accepted_pramanas?: PramanaRef[];

  assumptions: PropositionId[];

  preference_rules: PreferenceRule[];

  burden_rules?: BurdenRule[];
}
```

Examples:

```text
PRATYABHIJNA_INTERNAL
BUDDHIST_INTERNAL
SHARED_DEBATE_GROUND
MODERN_ANALYTIC
```

---

## 6. `ArgumentScheme`

Reusable reasoning pattern.

```text
TRANSCENDENTAL
ABDUCTION
ANALOGY
NYAYA_ANUMANA
REDUCTIO
TESTIMONY
CONCEPTUAL_NECESSITY
...
```

Each scheme contains **critical questions**.

---

## 7. `InferenceRule`

This is where our earlier `Warrant` goes.

```ts
interface InferenceRule {
  id: string;

  warrant_text: string;

  strictness:
    | STRICT
    | DEFEASIBLE;

  scheme_id?: ArgumentSchemeId;

  formal_pattern?: FormulaPattern;

  grounding: Grounding[];

  explicitness:
    | EXPLICIT
    | RECONSTRUCTED
    | IMPLICIT;

  review_status: ReviewStatus;
}
```

This object can be compiled into py-aspic. ([GitHub][1])

---

## 8. `InferenceApplication`

The actual computational atom:

[
{P_1,\ldots,P_n}\xrightarrow{R}C
]

```ts
interface InferenceApplication {
  id: string;

  rule_id: InferenceRuleId;

  premise_ids: PropositionId[];
  conclusion_id: PropositionId;

  assumptions?: PropositionId[];

  attribution?: EntityRef;

  review_status: ReviewStatus;
}
```

---

## 9. `Argument`

Not a premise bag.

A **named rooted subgraph**.

```ts
interface Argument {
  id: string;

  inference_ids: InferenceApplicationId[];

  focal_conclusion: PropositionId;

  frame_ids: DebateFrameId[];

  attribution?: EntityRef;

  review_status: ReviewStatus;
}
```

---

## 10. `Attack`

Store the objection.

```ts
interface Attack {
  id: string;

  source: ArgumentId;

  target:
    | PropositionId
    | InferenceApplicationId
    | InferenceRuleId
    | ArgumentId
    | DebateFrameId
    | SemanticAlignmentId;

  type:
    | UNDERMINE
    | UNDERCUT
    | REBUT
    | SCOPE_CHALLENGE
    | SEMANTIC_CHALLENGE
    | FRAME_CHALLENGE
    | ALTERNATIVE_EXPLANATION;

  grounding: Grounding[];
}
```

Whether it **succeeds** is derived under an EvaluationProfile.

---

## 11. `Preference`

Needed when valid considerations conflict.

```ts
interface Preference {
  preferred: Ref;
  dispreferred: Ref;

  regime_id: EpistemicRegimeId;

  basis:
    | EVIDENCE_STRENGTH
    | SOURCE_PRIORITY
    | PRAMANA_PRIORITY
    | SPECIFICITY
    | FORMAL_CERTAINTY
    | EDITORIAL_JUDGMENT;

  grounding: Grounding[];
}
```

ASPIC+ can handle much of the inferential preference computation. ([GitHub][1])

---

## 12. `Crux`

This is where we should innovate.

```ts
interface Crux {
  id: string;

  question: string;

  dependencies: Ref[];

  affected_arguments: ArgumentId[];
  affected_conclusions: PropositionId[];

  type:
    | SEMANTIC
    | EPISTEMIC
    | INFERENTIAL
    | EMPIRICAL
    | TEXTUAL
    | FRAME;

  status:
    | OPEN
    | PARTIALLY_RESOLVED
    | RESOLVED;
}
```

But **Crux candidates should be computed**, not simply authored.

For target outcome (q), find minimal disputed dependency sets (K) such that changing (K) changes the evaluated status of (q).

That's our key algorithmic research problem.

---

# `EvaluationProfile`

```ts
interface EvaluationProfile {
  id: string;

  frame_id: DebateFrameId;
  epistemic_regime_id: EpistemicRegimeId;

  semantics:
    | GROUNDED
    | PREFERRED
    | STABLE
    | OTHER;

  preference_policy?: string;

  semantic_alignment_version: string;
  formalization_version?: string;
}
```

Then:

```text
evaluate(argument_graph, profile)
```

returns—not stores as fundamental truth—

```text
SUPPORTED
SUPPORTED_WITH_QUALIFICATION
CONTESTED
UNDERDETERMINED
DEFEATED
NOT_COMPARABLE
```

with reasons.

---

# What existing infrastructure owns versus what Pāṭala owns

This is the cleanest boundary.

```text
EXISTING INFRASTRUCTURE
────────────────────────────────────────

xAIF
interchange representation

oAMF
generic argument-mining orchestration

py-aspic
structured defeasible reasoning

ALIAS / other Dung solvers
abstract semantics

LLM argument-mining systems
candidate extraction patterns

Lean/Z3
formal validity for selected encodings

GNN research
later approximation/representation learning


PĀṬALA OWNS
────────────────────────────────────────

philological provenance

historical commitments

semantic alignment

debate frames

cross-tradition epistemic regimes

philosophical reconstruction review

vertical grounding to Sanskrit

counterfactual dependency analysis

minimal support analysis

minimal crux extraction

Scholar Workbench

benchmark for historical philosophy
```

**That is the architectural boundary I would freeze.**

# Build order

I would now build the philosophy engine in this order:

```text
PHASE 0
Finish the IPVV scholarly substrate.

PHASE 1
Implement the 12-object Philosophy IR
+ EvaluationProfile.
No clever AI yet.

PHASE 2
Manually encode 5–10 exceptional IPVV disputes.

PHASE 3
Build:
export_xaif()
compile_aspic()
evaluate_aspic()

PHASE 4
Implement deterministic:
trace_dependencies()
minimal_support_sets()
counterfactual_intervention()

PHASE 5
Implement first crux detector.

PHASE 6
Build Scholar Workbench graph UI.

PHASE 7
Introduce LLM candidate extraction:
C1 → Proposition
C1 → Commitment
Propositions → candidate inference
Inference → candidate warrant
rivals → candidate alignment/attack

PHASE 8
Human-review these into gold.

PHASE 9
Benchmark against:
generic LLM
oAMF
ArgLLM-style pipeline
our staged Pāṭala pipeline.

PHASE 10
Only now investigate:
dense retrieval
graph embeddings
heterogeneous GNNs
Deep Arguing-style learning.
```

The important result of this research is that **the engine is now much cheaper to build than it looked**.

We do **not** need to implement computational argumentation.

We need to implement the missing layer between historical scholarship and computational argumentation.

That layer is:

```text
              PĀṬALA PHILOSOPHICAL IR

Sanskrit
   ↓
scholarly interpretation
   ↓
Proposition
Commitment
Alignment
Frame
Epistemic Regime
Rule
Inference
Argument
Attack
Preference
Crux
   ↓
existing formal machinery
```

That is where Pāṭala can actually contribute something new rather than spending a year reimplementing ASPIC+, AIF, Dung semantics and generic argument mining. ([GitHub][1])

Because this literature is moving quickly, I can also monitor new argumentation/LLM/graph papers and surface only ones that materially change this architecture.

[1]: https://github.com/arg-tech/py-aspic "GitHub - arg-tech/py-aspic: Python library for ASPIC+ · GitHub"
[2]: https://github.com/arg-tech/xaif "GitHub - arg-tech/xaif · GitHub"
[3]: https://github.com/arg-tech/oAMF "GitHub - arg-tech/oAMF · GitHub"
[4]: https://github.com/arg-tech/aif-arg-datasets?utm_source=chatgpt.com "arg-tech/aif-arg-datasets: The repository containing links ..."
[5]: https://github.com/CLArg-group/argumentative-llms "GitHub - CLArg-group/argumentative-llms: An official code repository for the paper \"Argumentative Large Language Models for Explainable and Contestable Claim Verification\" · GitHub"
[6]: https://github.com/DAMO-NLP-SG/LLM-argumentation "GitHub - DAMO-NLP-SG/LLM-argumentation: [ACL2024] Exploring the Potential of Large Language Models in Computational Argumentation · GitHub"
[7]: https://arxiv.org/abs/2605.13793?utm_source=chatgpt.com "[2605.13793] An LLM-Based System for Argument Mining"
[8]: https://arxiv.org/abs/2506.00713?utm_source=chatgpt.com "From Argumentative Text to Argument Knowledge Graph: A New Framework for Structured Argumentation"
[9]: https://github.com/Open-Argumentation/ALIAS?utm_source=chatgpt.com "Open-Argumentation/ALIAS: A Library for Implementing ..."
[10]: https://github.com/carneades?utm_source=chatgpt.com "The Carneades Project"
[11]: https://github.com/debate-map/app "GitHub - debate-map/app: Monorepo for the client, server, etc. of the Debate Map website. · GitHub"
[12]: https://github.com/loc110504/ACAL "GitHub - loc110504/ACAL: Adaptive Collaboration of Arena-Based Argumentative LLMs for Explainable and Contestable Legal Reasoning · GitHub"
[13]: https://arxiv.org/abs/2605.10569?utm_source=chatgpt.com "Deep Arguing"
[14]: https://arxiv.org/abs/2404.18672?utm_source=chatgpt.com "Graph Convolutional Networks and Graph Attention Networks for Approximating Arguments Acceptability -- Technical Report"
[15]: https://arxiv.org/pdf/2511.08982?utm_source=chatgpt.com "Heterogeneous Graph Neural Networks for Assumption- ..."
[16]: https://arxiv.org/html/2603.15946v1?utm_source=chatgpt.com "Toward AI Agents That Reason With Us, Not For Us"
[17]: https://arxiv.org/abs/2506.16383?utm_source=chatgpt.com "Large Language Models in Argument Mining: A Survey"
[18]: https://github.com/KashiwaByte/Awesome-LLM-Computational-Argumentation?utm_source=chatgpt.com "KashiwaByte/Awesome-LLM-Computational-Argumentation"
