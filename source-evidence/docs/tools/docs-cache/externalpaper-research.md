I went through the external research/tooling landscape and the strongest mechanisms already present across patala, blogengine, geometricengine, and the relevant parts of Ochema.

The main conclusion is strong:

Do not build a new “paper graph system.” You already have about half of it scattered across your repos. External projects can supply the document parsing, QA-mediated extraction, claim verification and optimization machinery. What Pāṭala needs is a clean compiler joining them.

The target should be:

PDF / BOOK / ESSAY
       │
       ▼
DOCUMENT REPRESENTATION
       │
       ▼
SOURCE-SPAN LEDGER
       │
       ▼
SCHOLARLY INTERROGATION
"What questions is this author answering?"
       │
       ▼
SCHOLAR CONTRIBUTION GRAPH
       │
       ├── Questions
       ├── Claims
       ├── Interpretations
       ├── Arguments
       ├── EvidenceUses
       ├── Definitions
       ├── Distinctions
       ├── Objections
       ├── Agreements
       ├── Disagreements
       ├── Research gaps
       └── Quotes
       │
       ▼
PĀṬALA ALIGNMENT
primary sources / concepts / arguments / scholars
       │
       ▼
VERIFIER ENSEMBLE
       │
       ▼
GRAPH PROPOSAL
       │
       ▼
REVIEW / ACCEPT / CONTEST
       │
       ▼
CANONICAL SCHOLAR GRAPH
       │
       ├── Ask
       ├── Learn
       ├── Essays
       ├── Video
       ├── Scholar pages
       └── Discovery Engine
1. Paper/PDF → structured document: reuse these, don't rebuild
GROBID — essential

GitHub:

https://github.com/grobidOrg/grobid

GROBID is specifically designed for scholarly documents. It extracts headers, bibliographic information, references and structured TEI from PDFs. This is particularly useful for Pāṭala because references and bibliography structure matter as much as ordinary text.

Reuse:

PDF
→ sections
→ paragraphs
→ footnotes
→ bibliography entries
→ inline citations
→ authors
→ metadata

Pāṭala should preserve the TEI/source coordinates rather than convert immediately to one Markdown blob.

S2ORC doc2json — extremely relevant schema reference

GitHub:

https://github.com/allenai/s2orc-doc2json

S2ORC's parser explicitly does:

PDF
→ GROBID
→ TEI XML
→ structured scholarly JSON

and keeps paper metadata, body sections and citation links in a reusable representation.

This is very close to the paper normalization layer Pāṭala needs.

I would steal the architectural distinction:

RawDocument
StructuredDocument
BibliographyEntry
CitationMention
BodySpan
Section

rather than their ontology wholesale.

Docling — best general document normalization candidate

GitHub:

https://github.com/docling-project/docling

Paper:

https://arxiv.org/abs/2408.09869

Docling currently handles PDFs and many other formats, understands layout/reading order/tables/formulas, and exposes a unified DoclingDocument plus lossless JSON-style export.

My preference: use Docling as the general structural parser and GROBID alongside it for specifically scholarly/bibliographic structure.

                    PDF
                     │
            ┌────────┴────────┐
            ▼                 ▼
         Docling            GROBID
      layout/content    scholarly metadata
            │                 │
            └────────┬────────┘
                     ▼
              Pāṭala SpanLedger

Don't make one parser win everything.

Marker — strong fallback / extraction adapter

GitHub:

https://github.com/datalab-to/marker

Marker converts documents to Markdown, JSON, chunks or HTML, preserves things like equations/references, and even offers schema-guided structured extraction.

Good for difficult PDFs and rapid ingestion.

But there is a licensing consideration for commercial reuse around its current code/model setup, so I would not make it the irreplaceable centre of Pāṭala.

Nougat — useful for difficult academic equations/layouts

GitHub:

https://github.com/facebookresearch/nougat

Paper:

https://arxiv.org/abs/2308.13418

Nougat is specialized for academic-document parsing and mathematical/table-heavy PDFs.

Lower priority for humanities papers, but useful as a fallback parser.

2. Paper → questions → graph: SocraticKG is probably the most important paper here

GitHub:

https://github.com/LABA-SNU/SocraticKG

Paper:

https://arxiv.org/abs/2601.10003

This is uncannily aligned with what we just designed.

Instead of:

document
→ LLM
→ triples

SocraticKG does roughly:

DOCUMENT
   ↓
QUESTION / ANSWER EXPANSION
   ↓
semantic scaffolding
   ↓
atomic facts
   ↓
knowledge graph

The authors' central finding is that the QA intermediate representation helps retain document-level relationships that direct triple extraction can lose.

For Pāṭala, change generic 5W1H questions into a Scholarly Interrogator:

What question is being answered?


What position does the author adopt?


What evidence is offered?


Which primary passage is interpreted?


What existing scholar is followed?


What existing scholar is rejected?


What distinction is necessary?


What alternative interpretation is considered?


What objection is answered?


What remains uncertain?


What would follow if this interpretation were correct?

This is probably the single external mechanism I'd implement first after PDF normalization.

3. ORKG — closest existing project to our scholarly contribution layer

Main project:

https://www.orkg.org/

Foundational paper:

https://arxiv.org/abs/1901.10816

System walkthrough:

https://arxiv.org/abs/2206.01439

Literature-comparison paper:

https://arxiv.org/abs/2006.01747

Knowledge-acquisition paper:

https://arxiv.org/abs/2308.12981

ORKG's premise is exactly that knowledge remains trapped in document-shaped publications and should instead be represented as machine-actionable research contributions. It also supports comparisons across contributions.

What Pāṭala should steal is the publication ≠ contribution distinction.

Paper
   │
   ├─ contribution 1
   ├─ contribution 2
   ├─ contribution 3
   └─ contribution 4

But ORKG's science-oriented structures tend toward things such as problem/method/result.

Ours becomes humanities-native:

ScholarContribution


Question
Position
Interpretation
TextualReading
Argument
EvidenceUse
TermSense
Distinction
Objection
Reply
HistoricalClaim
Comparison
Crux
OpenQuestion

That's effectively ORKG for philosophy/intellectual history with source-level provenance.

4. SciClaim — steal the fine-grained relational annotation idea

Paper:

https://arxiv.org/abs/2109.10453

SciClaim shows why bare triples are insufficient: scholarly claims contain qualifications, causal/comparative relations and attributes that modify the relation itself.

That matters massively for humanities.

Bad:

Ratié → says → recognition is memory

Better:

ScholarPosition


subject:
recognition


relation:
compared_with


object:
memory


stance:
DISTINGUISHES_FROM


scope:
context X


modality:
qualified


source_span:
p. 42 ¶3

Use qualified hyperedges, not GraphRAG-style toy triples.

5. SciCo — directly useful for canonicalizing concepts across papers

Paper:

https://arxiv.org/abs/2104.12979

This is a cross-document scientific concept linking/coreference task.

Mechanism worth reusing:

paper A: "reflexive awareness"
paper B: "self-awareness"
paper C: "self-cognition"
        ↓
candidate cross-document concept clusters

For Pāṭala this becomes enormously important because scholars' vocabulary varies.

You need:

Mention
     ↓
candidate canonical concept
     ↓
semantic alignment type

not simply embedding similarity.

6. Argument mining: use it as decomposed tasks, not one magical extractor

Relevant projects/papers:

IAM GitHub:

https://github.com/LiyingCheng95/IAM

Scholarly argument mining:

https://aclanthology.org/2021.sdp-1.7/

https://aclanthology.org/2022.wiesp-1.7/

Knowledge-based graph argument mining:

https://arxiv.org/abs/2102.02086

The useful lesson from this literature is that detecting argumentative units and detecting relations between them are separate tasks. Full-paper argumentative structure remains difficult enough that extraction should stay candidate/reviewable rather than becoming canonical automatically.

For Pāṭala:

PASS 1 proposition candidates
PASS 2 proposition role
PASS 3 cited evidence spans
PASS 4 proposition → evidence
PASS 5 proposition → proposition
PASS 6 support / attack / qualify
PASS 7 argument reconstruction
PASS 8 adversarial check

Do not use one prompt: "extract the argument graph."

7. RefChecker — steal atomic claim decomposition

GitHub:

https://github.com/amazon-science/RefChecker

Paper:

https://arxiv.org/abs/2405.14486

RefChecker decomposes model outputs into fine-grained knowledge triplets and checks them against reference material, with localization back into reference snippets.

For Pāṭala:

AI-generated paragraph
         ↓
atomic propositions
         ↓
each must resolve to:
  ScholarPosition
  PrimaryClaim
  SynthesisClaim
         ↓
SUPPORTED / QUALIFIED / UNSUPPORTED

This is perfect for the essay/video renderer verification layer.

8. RARR — steal research → agreement → revision

GitHub:

https://github.com/anthonywchen/RARR

Its useful pattern is:

generated claim
→ formulate question about claim
→ retrieve evidence
→ assess agreement
→ revise

Pāṭala version:

generated sentence
      ↓
claim atomization
      ↓
Pāṭala graph query
      ↓
source / scholar evidence
      ↓
agreement check
      ↓
rewrite if unsupported

The key modification is that our trusted corpus becomes the evidence universe, not unrestricted web retrieval.

9. GraphCheck — use graph-vs-graph verification for long outputs

GitHub:

https://github.com/Yingjian-Chen/GraphCheck

GraphCheck specifically tackles fact-checking long-form text by extracting graph representations from claims and source material so relational errors can be detected rather than only sentence-local errors.

This is highly applicable to a 20-minute Pāṭala documentary.

CANONICAL GRAPH


A → qualifies → B
C → objects_to → B
B → supported_by → passage P

versus script extraction:

SCRIPT GRAPH


A → entails → B
C → agrees_with → B

Now you detect relationship drift, not just hallucinated nouns.

10. CIBER — retrieval should search for refutation deliberately

Paper:

https://arxiv.org/abs/2503.07937

CIBER specifically retrieves both corroborating and refuting evidence for scientific claims rather than using conventional one-directional RAG.

This should be native Pāṭala behavior:

Claim
  ├─ SUPPORT query
  ├─ QUALIFICATION query
  └─ REFUTATION query

This is stronger than:

find passages semantically similar to claim

because similarity retrieval naturally self-confirms.

11. CLAIM-BENCH — justification for our multi-pass compiler

Paper:

https://arxiv.org/abs/2506.08235

CLAIM-BENCH evaluates claim/evidence linking across scientific papers and reports better extraction/linking from deliberate multi-pass decomposition than simpler processing, at additional compute cost.

This directly supports:

paper
 ↓
claims
 ↓
evidence
 ↓
linkage
 ↓
arguments
 ↓
validation

instead of one-shot extraction.

12. CLAIMCHECK — blueprint for scholar-review objections

Paper:

https://arxiv.org/abs/2503.21717

CLAIMCHECK links review weaknesses to the paper claims they dispute and annotates critique type, validity and objectivity. Importantly, its evaluations still find human experts ahead of LLMs on important claim-centric review tasks.

So a Pāṭala AI review should generate:

Critique:
  target_claim:
  type:
  objection:
  source_support:
  alternative_reading:
  confidence:
  status: MACHINE_PROPOSED

not:

“This paper is flawed.”

Excellent fit with Pāṭala Review.

13. Vouch — external version of your review-gated graph mutation idea

GitHub:

https://github.com/vouchdev/vouch

Its relevant mechanism is conceptually:

agent proposes durable knowledge
→ proposal
→ review
→ accepted persistent knowledge

This maps almost directly onto:

GraphProposal
→ MACHINE_PROPOSED
→ review
→ ACCEPTED

We already have the stronger domain ontology, so steal workflow concepts rather than adopting its KB.

14. ARIA — steal uncertainty-triggered human escalation

GitHub:

https://github.com/yf-he/aria

The useful idea here is not generic agents; it is:

agent encounters uncertainty
      ↓
formulates targeted information request
      ↓
human supplies missing knowledge
      ↓
knowledge stored

For scholar work:

"I can resolve every dependency except whether
genitive X governs Y or Z."


                 ↓


SEND ONLY THAT CRUX TO SCHOLAR

This is exactly the human-labor efficiency Pāṭala wants.

15. Graph-R1 — future research-agent architecture

GitHub:

https://github.com/LHRLAB/Graph-R1

Graph-R1 trains agents to reason through iterative graph queries instead of retrieving one static context bundle; its repository is the ICML 2026 GraphRAG/RL implementation.

Long-term Pāṭala:

ResearchQuestion
      ↓
reason
      ↓
query graph
      ↓
inspect result
      ↓
identify unresolved dependency
      ↓
query different neighborhood
      ↓
repeat

This is much closer to scholarly research than:

top_k = 20
LLM(context)

High priority later, after graph density is high enough.

16. Agent Lightning — eventual research-agent training loop

GitHub:

https://github.com/microsoft/agent-lightning

Paper:

https://arxiv.org/abs/2508.03680

Agent Lightning separates the execution of existing agents from RL training and converts agent trajectories into training transitions with credit assignment.

This becomes fascinating once Pāṭala has thousands of reviewed research runs:

ResearchTask


graph search
→ paper retrieval
→ claim extraction
→ evidence check
→ wrong hypothesis
→ correction
→ scholar review
→ accepted result

Store everything.

Then train:

Which search/reasoning action tends to produce accepted scholarship?

That's a serious proprietary training set.

17. DSPy — probably the external software I'd adopt earliest for the AI compiler

GitHub:

https://github.com/stanfordnlp/dspy

Core paper:

https://arxiv.org/abs/2310.03714

MIPRO:

https://arxiv.org/abs/2406.11695

GEPA:

https://arxiv.org/abs/2507.19457

Instead of hardcoding giant prompts for:

QuestionExtractor
ScholarPositionExtractor
EvidenceLinker
ArgumentExtractor
CitationRoleClassifier
GapClassifier

make them typed modules with measurable outputs.

Then Pāṭala's gold review data becomes the optimizer target.

Example metric:

QuestionExtractor:
canonical question accuracy


EvidenceLinker:
exact source-span F1


PositionExtractor:
attribution correctness


ArgumentExtractor:
edge precision


TermSenseExtractor:
semantic-inflation failures

That gives you a path from prompt pipeline → measured program → optimized program.

18. TextGrad — complementary pipeline optimization

Paper:

https://arxiv.org/abs/2406.07496

Useful once one component fails systematically:

Reviewer:
"Your evidence retrieval keeps missing
qualifying statements in footnotes."


       ↓


feedback propagates back to
EvidenceSearch module

It provides a useful intermediate step before actual model training.

19. Scholarly graph QA benchmark worth keeping around

KG20C / KG20C-QA:

https://arxiv.org/abs/2512.21799

GitHub:

https://github.com/tranhungnghiep/KG20C/

It creates scholarly KG question-answer benchmarks from graph relations.

Not central to our extraction pipeline, but useful as an external QA/KG evaluation reference.

Personal GitHub: the really reusable stuff
A. blogengine is much more directly reusable than I expected

Repo:

https://github.com/prx0r/blogengine

You already have:

content/
  authors/
  commentaries/
  comparison-objects/
  ontology-engine/
  research-objects/
  factory/
  publishing/
  research/

and separate factory queues/registries linking Research Objects and essays.

The Research Object model should survive

Your actual RO objects already contain:

stable ro_id;
schema version;
status;
semantic version;
sources;
what each source contributes;
which sections a source affects;
passage-level body objects;
source/commentary distinctions;
topics;
coverage estimates;
explicit gaps;
issues;
auto-generated issues;
version history.

That is not throwaway work.

Turn this:

ResearchObject

into the outer container for:

ScholarContributionPacket
Specifically steal this pattern

Current:

{
  "source_id": "...",
  "contribution": [
    "emerald_tablet",
    "one_thing"
  ],
  "sections_affected": [...]
}

Upgrade:

WorkUse:
  work_id:
  scholar_id:
  source_span_ids:


  contributes:
    - ScholarPosition:POS-88
    - EvidenceUse:EV-34
    - Definition:DEF-19


  downstream:
    - Synthesis:S-3
    - Lesson:L-9

The source → contribution → affected downstream objects pattern is already there.

B. Blogengine's coverage + issues mechanism becomes the paper Gap Engine

The RO objects already record things such as:

coverage:
  status
  passage_count
  estimated_completeness
  gaps[]


issues:
  type
  description
  status
  auto_generated

This should become generic:

ScholarWorkCoverage


QUESTIONS
CLAIMS
PRIMARY-SOURCE REFERENCES
ARGUMENTS
CITATIONS
TERM SENSES
COUNTERPOSITIONS

Example:

coverage:
  questions: 0.93
  claims: 0.88
  primary_source_alignment: 0.61
  citation_resolution: 0.97
  argument_reconstruction: 0.54

And:

issues:
  - type: UNRESOLVED_PRIMARY_REFERENCE


  - type: ATTRIBUTION_AMBIGUITY


  - type: ARGUMENT_GAP


  - type: POSSIBLE_OVERREADING

This is better than “paper successfully processed.”

C. Blogengine already has the right production abstraction

From the integrated architecture you built earlier, the system already conceptualizes:

user sends paper
→ acquisition
→ catalog
→ determine which Research Objects it affects
→ extract relevant passages
→ propose update
→ human reviews
→ merge
→ bump version

This is almost exactly the paper compiler we now want.

Change the unit from hand-curated RO section edits into:

Work
→ ScholarContributionPacket
→ ImpactAnalysis
→ GraphProposal[]
→ review

Keep the workflow.

D. geometricengine gives us the correct hyperedge representation

Repo:

https://github.com/prx0r/geometricengine

Its schema's best idea was:

hyperedge
+
typed incidences

instead of forcing complex events into pairwise graph edges.

For paper scholarship, one proposition might involve:

Scholar X
Work W
SourceSpan S
Question Q
Claim C
PrimaryPassage P
Concept K
Scholar Y

This is naturally:

SCHOLARLY CONTRIBUTION EVENT
             │
  ┌──────────┼────────────┐
  ↓          ↓            ↓
Scholar    Claim       Evidence
  ↓          ↓            ↓
Work      Question      Passage

The same mechanism in geometricengine currently connects a pedagogy event to state, function, mechanism, actions, intent and outcome. Its SQL schema also separates hyperedges, incidences, episodes, transitions and feedback events.

Reuse the data pattern, not the therapy vocabulary.

E. GeometricEngine's “episode” idea is useful for argument structure in papers

A paper isn't just a bag of claims.

Treat:

Paper
  ↓
SectionEpisode
  ↓
DiscourseMove
  ↓
next DiscourseMove

Possible moves:

POSE_QUESTION
STATE_POSITION
INTRODUCE_EVIDENCE
INTERPRET_PASSAGE
QUALIFY_POSITION
RAISE_OBJECTION
ANSWER_OBJECTION
SYNTHESIZE

Then transitions recover argumentative flow:

question
→ proposed interpretation
→ textual evidence
→ rival reading
→ objection
→ response
→ conclusion

This imports geometricengine's temporal-transition strength into scholarly discourse.

F. GeometricEngine's feedback objects map directly to scholar correction

Current patterns include:

feedback_events
preference_pairs
policy_weights

For scholarship:

ReviewEvent


proposal_id
reviewer
verdict
correction
reason
source_span

And:

PreferencePair


reading_A
reading_B
preferred
reason
reviewer

Then the extraction system learns eventually from actual reviewed errors.

That's valuable training data.

G. patala supplies the epistemic constraints the other repos lack

Repo:

https://github.com/prx0r/patala

The existing Evidence Policy already makes several distinctions the paper compiler absolutely needs:

base text vs textual evidence;
textual evidence vs interpretive evidence;
current-passage grammar vs external parallels;
machine-proposed term senses vs accepted senses;
rights-aware retrieval;
retrieval weighted by textual/scholarly relationship rather than simple similarity.

The crucial existing invariant is:

proposal
≠
accepted knowledge

Your term system already enforces:

machine proposal
→ proposed
→ reviewed
→ accepted

and explicitly warns against machine guesses feeding back into later retrieval as supposedly established knowledge.

Use exactly that doctrine for scholarly extraction:

ScholarPositionExtraction
MACHINE_PROPOSED


          ↓


MACHINE_CORROBORATED


          ↓


HUMAN_REVIEWED


          ↓


ACCEPTED
H. Pāṭala's rights distinction should become the universal paper-rights layer

Your evidence policy already says copyrighted non-open translations must not simply be dumped into model context and records rights/access at work level.

Apply that directly to Academia papers:

WorkRights:
  fulltext_internal_available:
  public_fulltext:
  license:
  quote_policy:
  attribution_required:
  source_url:

Then the structural data can be useful without casually treating every PDF as republishable prose.

I. Ochema is useful mainly downstream, not as the extraction core

Repo:

https://github.com/prx0r/Ochema

Its current tree is heavy on synthesis, comparison, source manuals, practice layers and essay/AV representation rather than paper-parsing machinery.

That means its reusable role is projection, not canonical extraction:

Pāṭala structured scholarship
        ↓
Ochema comparative synthesis
        ↓
EssayViz
        ↓
film / visual / explanatory renderers

Don't move its free synthesis objects into canonical truth.

Move canonical truth into its renderers.

The best unified architecture from all this

This is what I would actually implement.

                 PDF / BOOK / ARTICLE
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
          DOCLING                GROBID
       layout/content        metadata/citations
             │                     │
             └──────────┬──────────┘
                        ▼
                 STRUCTURED WORK
                        │
                        ▼
                  SPAN LEDGER
          page / block / sentence / note
                        │
                        ▼
             SCHOLARLY INTERROGATOR
                  [SocraticKG]
                        │
             question-answer scaffold
                        │
                        ▼
             ATOMIC EXTRACTOR
           [DSPy optimized modules]
                        │
       ┌────────────────┼────────────────┐
       ↓                ↓                ↓
   Questions          Claims       Interpretations
   Arguments        EvidenceUses     TermSenses
   Objections       Citations       Distinctions
       │                │                │
       └────────────────┼────────────────┘
                        ▼
             HYPEREDGE COMPILER
              [geometricengine]
                        │
                        ▼
                CANONICALIZER
         concept / scholar / work / question
                        │
                        ▼
             PĀṬALA SOURCE ALIGNER
       primary passages / arguments / concepts
                        │
                        ▼
                 REVIEW ENSEMBLE


       RefChecker → atomic fidelity
       CIBER      → counterevidence
       GraphCheck → relationship fidelity
       CLAIMCHECK → critique validity
       RARR       → revise unsupported output


                        │
                        ▼
                  GraphProposal
                        │
                        ▼
          BLOGENGINE-STYLE IMPACT PASS


        What existing ROs/questions/arguments/
        essays/lessons does this alter?


                        │
                        ▼

That is the system.

The canonical paper object should therefore look roughly like this
ScholarContributionPacket:


  work:
    work_id:
    title:
    authors:
    rights:
    identifiers:


  source_document:
    parser_versions:
    spans:
    bibliography:
    citation_mentions:


  contributions:


    questions: []


    positions: []


    interpretations: []


    propositions: []


    arguments: []


    evidence_uses: []


    primary_source_links: []


    definitions: []


    term_senses: []


    distinctions: []


    objections: []


    replies: []


    agreements: []


    disagreements: []


    citation_uses: []


    comparisons: []


    research_gaps: []


  coverage:
    question_coverage:
    argument_coverage:
    evidence_coverage:
    citation_resolution:
    primary_alignment:


  issues: []


  review:
    extraction_version:
    verifier_results:
    human_events:


  attribution:
    scholars:
    downstream_uses:

Notice what's not canonical:

summary
essay
video script
chat answer

Those are projections.

External inventory — condensed link dump

These are the ones I would actually keep in a Pāṭala research-infrastructure document.

Document parsing
https://github.com/grobidOrg/grobid
https://github.com/allenai/s2orc-doc2json
https://github.com/allenai/s2orc
https://github.com/docling-project/docling
https://arxiv.org/abs/2408.09869
https://github.com/datalab-to/marker
https://github.com/facebookresearch/nougat
https://arxiv.org/abs/2308.13418

GROBID/S2ORC and Docling are the highest-value pieces here.

Scholarly → structured knowledge
https://github.com/LABA-SNU/SocraticKG
https://arxiv.org/abs/2601.10003


https://arxiv.org/abs/1901.10816
https://arxiv.org/abs/2206.01439
https://arxiv.org/abs/2006.01747
https://arxiv.org/abs/2308.12981


https://arxiv.org/abs/2109.10453
https://arxiv.org/abs/2104.12979
https://arxiv.org/abs/2102.02086
https://arxiv.org/abs/2512.21799
https://github.com/tranhungnghiep/KG20C/

SocraticKG + ORKG + SciClaim are the three most important conceptual references in that set.

Argument / scholarly discourse
https://github.com/LiyingCheng95/IAM
https://aclanthology.org/2021.sdp-1.7/
https://aclanthology.org/2022.wiesp-1.7/
https://arxiv.org/abs/2102.02086
Verification / adversarial review
https://github.com/amazon-science/RefChecker
https://arxiv.org/abs/2405.14486


https://github.com/anthonywchen/RARR


https://github.com/Yingjian-Chen/GraphCheck


https://arxiv.org/abs/2503.07937
https://arxiv.org/abs/2506.08235
https://arxiv.org/abs/2503.21717


https://github.com/vouchdev/vouch
https://github.com/yf-he/aria
https://github.com/Zhengsh123/SCI-Verifier

The highest-value mechanisms are atomic claim checking, refuting-evidence retrieval, graph-level relational checking and claim-targeted critique.

Agent / graph reasoning / optimization
https://github.com/LHRLAB/Graph-R1


https://github.com/microsoft/agent-lightning
https://arxiv.org/abs/2508.03680


https://github.com/stanfordnlp/dspy
https://arxiv.org/abs/2310.03714
https://arxiv.org/abs/2406.11695
https://arxiv.org/abs/2507.19457


https://arxiv.org/abs/2406.07496

Graph-R1 is the interesting long-term graph-reasoning direction; Agent Lightning is the long-term trajectory-training direction.

Consumer/learning graph stack from the adjacent investigation
https://github.com/getzep/graphiti


https://github.com/CAHLR/pyBKT
https://github.com/pykt-team/pykt-toolkit


https://github.com/jhljx/GKT
https://github.com/JJCui96/GRKT
https://arxiv.org/abs/2406.12896


https://github.com/umass-ml4ed/dialogue-kt
https://github.com/CAHLR/OATutor
https://github.com/zijinz456/OpenTutor

Those belong downstream of the scholarly compiler rather than inside paper extraction itself.

The personal code to reuse, ranked
Existing mechanism	Repo	New use	Keep?
Research Object + versions	blogengine	paper contribution container	10/10
coverage + gaps + issues	blogengine	extraction completeness / research gaps	10/10
source → affected sections	blogengine	dependency/impact propagation	10/10
RO → essay linkage/factory queue	blogengine	structured research → media	10/10
acquire → impact → PR → version	blogengine	scholar-paper ingestion workflow	10/10
hyperedge + typed incidences	geometricengine	ScholarContribution event	10/10
episode/transition graph	geometricengine	scholarly discourse structure	8/10
feedback/preference events	geometricengine	adjudication/training data	9/10
proposal ≠ accepted	patala	canonical scholarship gate	10/10
textual vs interpretive evidence	patala	source/scholar separation	10/10
rights-aware retrieval	patala	copyrighted paper handling	10/10
relationship-aware retrieval ranking	patala	relevant scholarship retrieval	9/10
Ochema synthesis	Ochema	output projection	7/10
GeometricEngine reward system	geometricengine	—	discard
GeometricEngine therapy ontology	geometricengine	—	discard

The strongest finding from inspecting the actual repositories is that this is not a new greenfield architecture. blogengine already contains the life-cycle object and factory; geometricengine already contains the generic event/hyperedge/transition ideas; patala already contains the epistemic and review constraints.

What external research adds is mainly:

Docling/GROBID
        =
reliable document substrate


SocraticKG
        =
QA-mediated semantic unfolding


ORKG
        =
research contribution abstraction


SciClaim
        =
fine-grained qualified relations


DSPy
        =
measurable extraction programs


RefChecker/CIBER/GraphCheck/CLAIMCHECK
        =
verification ensemble


Graph-R1
        =
future graph-native research policy


Agent Lightning
        =
future learning from reviewed research trajectories

So I would merge ideas, not repositories:

Blogengine's Research Object lifecycle + GeometricEngine's hyperedges + Pāṭala's epistemic kernel + SocraticKG's QA extraction + external verifier ensemble.

That gives us a very concrete path from the huge secondary-paper corpus to a machine-addressable commentarial graph where every scholar's actual intellectual contribution can power questions, comparisons, essays, videos, education, attribution, reviews and future research without reducing the paper to a summary blob.