---
name: Pāṭala C1 Scholarly Commentary Producer
version: 1.0.0
project: patala
kind: autonomous-layer-skill
layer: C1
status: canonical-proposal
inherits: ../../AUTONOMY_CONTRACT.md
---

# Purpose

Produce the capstone passage commentary from the entire translation/evidence stack. C1 is source-aware commentary, not a free-form essay and not a paraphrase of T3.

# Inputs

- source + committed L0 refs
- T1/R1/T2/R2/T3/T3.1 versions
- deterministic evidence packet
- tracked terms / parallels with provenance

# Required structure

A. core sense — what the passage says
B. why this reading — decisive evidence chain
C. crux/uncertainty — only if real
D. larger significance — evidence-tied

Every nontrivial claim is typed:
`TEXTUAL | GRAMMATICAL | INTERPRETIVE | HISTORICAL | ATTRIBUTED | SYNTHESIS`

# Output

```json
{"passage_id":"...","stack_versions":{},
 "interpretation":"...",
 "evidence_state":"C1_EVIDENCE_PARTIAL",
 "cruxes":[],
 "evidence":[{"id":"stable-id","supports":"...","source_refs":[]}],
 "open_questions":[],
 "proposals":[],
 "challenges":[]}
```

# Challenge rule

C1 may emit a `TranslationChallenge` against T3 with evidence and a proposed revision. It MUST NEVER mutate/supersede T3 directly. The challenge enters the review/correction workflow.

# Proposal rule

TermSenseAssignment, TermHistoryAssertion, ParallelAssertion, DoctrinalAssertion, CommentaryClaim, ResearchQuestion and similar generated objects are `origin=machine`, `status=proposed` until adjudicated.

# Evidence-state gate

Set `C1_EVIDENCE_COMPLETE` only if every required evidence item resolves and all mandatory uncertainty is represented. Otherwise use `C1_EVIDENCE_PARTIAL` and list missing items.

# Autonomy boundary

C1 generation may run autonomously as proposal production after its certificate. C1 acceptance remains review-gated. A fluent commentary never upgrades its own authority.
