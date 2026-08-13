> # AGENT 2 — AUTONOMOUS TRANSLATION FACTORY MISSION
>
> You are Agent 2. Your job is to deliver the autonomous Sanskrit translation factory.
>
> Your lane is:
>
> ```text
> SOURCE
>   ↓
> RAW-L0
>   ↓
> L0/L1
>   ↓
> L2
>   ↓
> L200
>   ↓
> C1
> ```
>
> with:
>
> ```text
> deterministic controller
> immutable registries
> provenance
> input hashes
> idempotency
> validation
> certificates
> fail-closed semantics
> crash/resume
> supersession/staleness
> unattended execution
> ```
>
> **Do not return after one implementation, one benchmark, one passing test, or one commit.**
>
> Work autonomously through the checkpoint ladder below until:
>
> * the terminal unattended vertical succeeds;
> * a genuine external blocker prevents further progress;
> * or the currently available corpus has been safely exhausted.
>
> ---
>
> # THE PRIMARY MISSION
>
> The terminal objective is not:
>
> ```text
> "we have workers for L0/L2/L200"
> ```
>
> It is:
>
> > **Pāṭala can be given raw Sanskrit, left running unattended, and reliably produce canonical provenance-bound translation objects through C1 without silently committing model failures, corrupt source material, stale derivations, duplicated work, or epistemic laundering.**
>
> The first immediate deliverable is the user's original priority:
>
> > **validated autonomous RAW→L0 production.**
>
> Do not let downstream L200 work pull focus until that checkpoint is real.
>
> ---
>
> # CHECKPOINT DOCTRINE
>
> Every checkpoint has four states:
>
> ```text
> NOT_BUILT
> BUILT
> VALIDATED
> AUTONOMOUSLY_PROVEN
> ```
>
> `BUILT` is not success.
>
> A layer reaches **VALIDATED** only when:
>
> ```text
> real inputs processed
> canonical outputs produced
> validator passes
> semantic quality measured where applicable
> known failure modes tested
> provenance/input binding verified
> replay/idempotency verified
> failure cases fail closed
> ```
>
> A layer reaches **AUTONOMOUSLY_PROVEN** only when:
>
> ```text
> controller drives it without manual intervention
> bounded real batch completes
> crash/resume works
> retries are bounded
> failed items remain failed/review-required
> no duplicate canonical commits occur
> run report is reviewable
> stale/upstream mutations behave correctly
> ```
>
> Do not proceed past a hard checkpoint until the checkpoint is genuinely achieved.
>
> ---
>
> # CHECKPOINT 0 — MODEL EXECUTION SUBSTRATE
>
> ## Goal
>
> Remove the current model-call bottleneck that affects both RAW-L0 glossing and downstream compiler stages.
>
> Build:
>
> ```text
> ModelAdapter
> ├── DirectModelAdapter
> └── HermesAdapter
> ```
>
> with:
>
> ```text
> complete_json()
> complete_batch_json()
> ```
>
> Required behavior:
>
> ```text
> strict structured output
> object_id binding
> input_hash binding
> bounded timeout
> bounded retry
> malformed JSON rejection
> unknown-id rejection
> duplicate-id rejection
> partial batch detection
> process/model failure surfaced explicitly
> no silent fallback to empty-success
> latency/runtime metadata
> model identity
> prompt hash
> ```
>
> Hermes remains the agentic execution backend.
>
> Direct structured calls should be available for bounded compiler tasks.
>
> Do not force every model token through `hermes -z` if direct structured completion is demonstrably safer/faster.
>
> ## Benchmark
>
> Compare:
>
> ```text
> Hermes single
> Hermes batch
> Direct single
> Direct batch
> ```
>
> on the same frozen development examples.
>
> Measure:
>
> ```text
> semantic acceptance
> JSON validity
> generation failure
> retries
> wrong-ID/hash errors
> median latency
> p95 latency
> total wall time
> ```
>
> Choose backend using:
>
> ```text
> QUALITY × RELIABILITY × LATENCY
> ```
>
> not latency alone.
>
> ### CHECKPOINT 0 PASSES WHEN
>
> One adapter configuration is demonstrably suitable for unattended structured compiler work and the alternative remains available as fallback/comparison.
>
> Continue automatically to Checkpoint 1.
>
> ---
>
> # CHECKPOINT 1 — VALIDATED WORKING RAW-L0
>
> **This is the immediate priority.**
>
> ## Input
>
> ```text
> raw Sanskrit source passage
> ```
>
> ## Output
>
> Canonical L0 containing the existing required:
>
> ```text
> source binding
> stable passage ID
> lossless Sanskrit representation
> tokenization
> morphology/lemma where available
> model-generated gloss layer
> provenance
> input hash
> generation status
> ```
>
> Preserve the deterministic floor already certified.
>
> Do not redesign L0 unnecessarily.
>
> Use the new ModelAdapter first for the gloss component that previously suffered Hermes nondeterminism.
>
> ## Validate on real Sanskrit
>
> Use:
>
> ```text
> existing certificate examples
> cross-work Kramasadbhāva material
> real IPVV passages
> ```
>
> Test:
>
> ```text
> losslessness
> avagraha preservation
> Unicode preservation
> passage binding
> input hash binding
> gloss semantic acceptability
> empty-model output
> malformed output
> wrong passage ID
> wrong hash
> duplicated records
> corrupted source
> OCR/source-blocked case
> timeout
> partial batch
> replay
> ```
>
> ### CHECKPOINT 1 = VALIDATED WORKING RAW-L0
>
> Declare this only when:
>
> ```text
> real RAW Sanskrit
> → real canonical L0
> → validator PASS
> ```
>
> repeatedly succeeds and the previously documented gloss nondeterminism is measured and bounded.
>
> Do not merely say:
>
> ```text
> "L0 certificate passes"
> ```
>
> Report:
>
> ```text
> n real passages
> semantic gloss acceptance
> generation failure rate
> malformed response rate
> latency
> replay duplicates
> source-blocked outcomes
> ```
>
> Then continue immediately to Checkpoint 2.
>
> ---
>
> # CHECKPOINT 2 — AUTONOMOUS RAW→L0
>
> Now prove the user's actual “translate while I sleep” requirement.
>
> Run a bounded but meaningful real corpus batch through:
>
> ```text
> SOURCE REGISTRY
>      ↓
> controller eligibility
>      ↓
> RAW-L0 worker
>      ↓
> ModelAdapter gloss batch
>      ↓
> validator
>      ↓
> COMMIT / FAIL / SOURCE_BLOCKED
>      ↓
> run report
> ```
>
> This must be driven by the real controller, not a hand-run helper script.
>
> Test:
>
> ```text
> unattended operation
> crash midway
> resume
> process kill
> timeout
> one malformed passage among good passages
> one corrupt source
> repeated controller tick
> repeated full run
> upstream source mutation
> wrong hash
> duplicate input
> ```
>
> ### HARD AUTONOMOUS RAW-L0 GATE
>
> Pass only if:
>
> ```text
> no silent failures committed
> no duplicate canonical L0 objects
> failures remain visible
> SOURCE_BLOCKED remains blocked
> valid items continue despite neighboring failures
> crash/resume does not restart completed work incorrectly
> replay produces zero duplicate canonical objects
> controller state agrees with registry truth
> output can be inspected after unattended run
> ```
>
> At this point explicitly record:
>
> # CHECKPOINT ACHIEVED: AUTONOMOUS RAW→L0 v1
>
> Create a certificate/report containing actual run evidence.
>
> **This is a major milestone.**
>
> Only after this is achieved may L200 again become the main development focus.
>
> ---
>
> # CHECKPOINT 3 — L1/L2 CONTINUITY
>
> Verify the existing downstream path from accepted L0 through controlled translation layers.
>
> Do not rebuild already-correct machinery.
>
> Confirm:
>
> ```text
> accepted L0
> → L1 controlled reading
> → L2 published/readable translation
> ```
>
> with:
>
> ```text
> exact upstream refs/hashes
> no orphan outputs
> version binding
> stale invalidation
> supersession
> replay safety
> ```
>
> If L1/L2 already satisfy these requirements, certify and move on.
>
> The goal is continuity, not polishing prose.
>
> ### CHECKPOINT 3 PASSES WHEN
>
> A real passage can traverse:
>
> ```text
> RAW SOURCE → L0 → L1 → L2
> ```
>
> with resolvable provenance and deterministic dependency state.
>
> ---
>
> # CHECKPOINT 4 — REDESIGN L200 AS A CONSTRAINED COMPILER
>
> Current honest DEV result exposed:
>
> ```text
> old apparent MT precision: 0.95
> actual instance-level MT precision: ~0.20
> false-positive MTs: 8
> ```
>
> Treat this as architectural evidence.
>
> Do **not** solve it by repeatedly telling the model to be “more conservative.”
>
> Replace:
>
> ```text
> L1 + L2
> → open-ended LLM asks "what changed?"
> ```
>
> with:
>
> ```text
> L0 + L1 + L2
>       ↓
> deterministic candidate generation
>       ↓
> candidate-level evidence packet
>       ↓
> model classification
>       ↓
> MT / IA / OPEN / IGNORE
> ```
>
> ## Candidate generation
>
> Generate bounded candidate differences for:
>
> ```text
> SUPPLIED
> REFERENT_SUPPLY
> STRUCTURAL_CONNECTIVE
> LEXICAL
> GRAMMATICAL
> possible IA
> possible OPEN
> ```
>
> Candidate generation does NOT assert a decision.
>
> It says:
>
> > this alignment location requires classification.
>
> Give the classifier only the relevant:
>
> ```text
> Sanskrit span
> token/lemma/morphology
> L1 controlled realization
> L2 published realization
> candidate difference
> ```
>
> ## Required classifier outcomes
>
> ```text
> SUPPLIED
> REFERENT_SUPPLY
> STRUCTURAL_CONNECTIVE
> LEXICAL
> GRAMMATICAL
> INTERPRETIVE_ASSERTION
> OPEN
> IGNORE
> ```
>
> **IGNORE should be the default prior.**
>
> Most English differences are not material translation decisions.
>
> The model must classify supplied candidates rather than invent arbitrary new MT records.
>
> Consider separating:
>
> ```text
> MT classification
> IA extraction/classification
> ```
>
> into distinct passes if DEV evidence supports it.
>
> ---
>
> # CHECKPOINT 5 — L200 DEV QUALITY GATE
>
> Use only:
>
> ```text
> benchmarks/l200/dev.jsonl
> ```
>
> while developing.
>
> Do not touch held-out TEST yet.
>
> Metrics must remain instance-level:
>
> ```text
> MT precision
> MT recall
> IA precision
> IA recall
> OPEN precision
> OPEN recall
> generation failure
> FALSE_POSITIVE_MT
> FALSE_NEGATIVE_MT
> FALSE_CERTAINTY
> LAUNDERING
> ```
>
> Use micro counts.
>
> Do not count empty fixtures as perfect recall.
>
> Do not return to type-only scoring.
>
> Improve DEV until the architecture demonstrates:
>
> ```text
> very high MT precision
> high IA precision
> zero or near-zero category laundering
> zero false certainty on known OPEN cases
> acceptable recall
> bounded generation failure
> substantially improved latency
> ```
>
> Preference ordering:
>
> ```text
> miss + OPEN
>     >
> confidently invented derivation
> ```
>
> ### CHECKPOINT 5 PASSES WHEN
>
> The L200 design is stable enough that you are willing to freeze:
>
> ```text
> candidate generator
> prompt
> classifier
> adapter
> model
> schemas
> worker implementation
> ```
>
> before seeing TEST results.
>
> ---
>
> # CHECKPOINT 6 — HELD-OUT L200 TEST
>
> Only now construct/finalize:
>
> ```text
> benchmarks/l200/test.jsonl
> ```
>
> Use:
>
> ```text
> 15–20 genuinely new real IPVV cases
> independently typed BEFORE model execution
> ```
>
> The TEST set must never have been used for:
>
> ```text
> prompt development
> candidate-generator development
> adapter choice
> model choice
> threshold choice
> ```
>
> Freeze:
>
> ```text
> test corpus hash
> gold hash
> worker SHA
> prompt hash
> model
> adapter
> candidate-generator SHA
> ```
>
> Run once.
>
> Do not silently tune after seeing results and keep calling it held-out.
>
> ### HARD L200 PRODUCTION GATES
>
> Prioritize:
>
> ```text
> very high semantic precision
> zero laundering on held-out test
> zero false certainty on held-out OPEN cases
> zero provenance/input-binding failures
> bounded generation failure
> ```
>
> Recall is secondary to precision but must be reported honestly.
>
> If TEST fails:
>
> ```text
> freeze result
> record failure
> move failing examples to future analysis/dev material
> create a NEW held-out set for any later production claim
> ```
>
> Never recycle failed TEST into the same held-out claim.
>
> ### CHECKPOINT ACHIEVED
>
> Only after passing:
>
> # VALIDATED L200 v1
>
> Then wire L200 into the autonomous controller.
>
> ---
>
> # CHECKPOINT 7 — AUTONOMOUS L200
>
> Run real accepted:
>
> ```text
> L0 + L1 + L2
> ```
>
> through controller-driven L200 production.
>
> Agent 2 must emit the frozen Agent2→Agent1 evaluation bundle for each natural candidate according to:
>
> ```text
> EVAL-CONTRACT-L200-EXPORT.md
> ```
>
> Bundle requirements include:
>
> ```text
> candidate_id
> SOURCE ref + hash
> L0 ref + hash
> L1 ref + hash
> L2 ref + hash
> model identity
> prompt hash
> worker SHA
> runtime
> run ID
> proposal
> structural validator result
> bundle hash
> ```
>
> Hash rule:
>
> ```text
> SHA256(
>   canonical JSON of bundle
>   excluding bundle_hash itself
> )
> ```
>
> Agent 1 consumes these read-only.
>
> Agent 2 does not adjudicate its own NAT gold.
>
> Test:
>
> ```text
> unattended L200 batch
> replay
> crash/resume
> malformed proposal
> failed candidate
> stale L2
> changed L0
> changed L1
> supersession
> export-bundle verification
> ```
>
> ### CHECKPOINT 7 PASSES WHEN
>
> L200 can run unattended without semantic/structural failures silently becoming canonical accepted audits.
>
> ---
>
> # CHECKPOINT 8 — C1 AUTONOMOUS COMMENTARY
>
> Only after L200 is stable.
>
> Build C1 as:
>
> ```text
> L0/L1
> + L2
> + L200
> + local context
> → passage-local commentary
> ```
>
> C1 must distinguish:
>
> ```text
> textual explanation
> translation explanation
> interpretive explanation
> scholarly/contextual addition
> unresolved issue
> ```
>
> No unsupported theological/philosophical invention.
>
> Required:
>
> ```text
> skill
> schema
> validator
> adversarial mutations
> certificate
> real canary
> controller integration
> ```
>
> Develop with conservative authority:
>
> ```text
> generation ≠ review
> commentary must not outrank its dependencies
> uncertainty propagates
> ```
>
> ### CHECKPOINT 8 PASSES WHEN
>
> Real passages produce C1 objects whose claims remain resolvable to lower layers and whose authority never exceeds those dependencies.
>
> Then prove autonomous C1 batch operation.
>
> ---
>
> # CHECKPOINT 9 — FULL UNATTENDED VERTICAL
>
> This is the terminal factory proof:
>
> ```text
> RAW SANSKRIT
>      ↓
> SOURCE
>      ↓
> L0
>      ↓
> L1
>      ↓
> L2
>      ↓
> L200
>      ↓
> C1
> ```
>
> driven by:
>
> ```text
> deterministic controller
> registry-derived eligibility
> bounded workers
> validation
> immutable commits
> supersession
> run reports
> ```
>
> Run on a meaningful real IPVV subset.
>
> Include adversarial events during the run:
>
> ```text
> kill process
> restart
> model timeout
> malformed output
> one corrupted source
> change upstream object
> repeated scheduler tick
> duplicate input
> stale downstream object
> ```
>
> Verify:
>
> ```text
> good work continues
> bad work fails closed
> no duplicates
> no stale masquerading
> dependency invalidation propagates
> exact provenance remains resolvable
> review-required objects remain review-required
> ```
>
> ### TERMINAL SUCCESS
>
> Declare success only when:
>
> > **A real raw Sanskrit batch can traverse SOURCE→L0→L1→L2→L200→C1 unattended, with provenance, validation, replay safety, failure isolation and staleness propagation demonstrably working.**
>
> At that point:
>
> # AUTONOMOUS TRANSLATION FACTORY v1 PROVEN
>
> ---
>
> # CHECKPOINT 10 — SCALE IPVV
>
> Only after terminal factory proof should you scale.
>
> Run larger IPVV production using bounded batches.
>
> Monitor:
>
> ```text
> throughput
> cost
> latency
> failure rate
> semantic review queue
> stale-object rate
> retry rate
> source-blocked rate
> ```
>
> Do not weaken validators to increase throughput.
>
> Scale is the consequence of reliability, not a substitute for it.
>
> ---
>
> # CROSS-LANE RULE — AGENT 1
>
> Agent 1 owns:
>
> ```text
> evidence evaluation
> NAT adjudication
> scholarly source corpus
> argument/evidence layer
> Inspect infrastructure
> ```
>
> Agent 2 owns:
>
> ```text
> translation production
> model execution adapters
> RAW-L0
> L1/L2 continuity
> L200 proposer/compiler
> C1
> factory controller
> production registries
> certificates
> unattended reliability
> ```
>
> Agent 2 may **export** natural L200 candidates to Agent 1.
>
> Agent 1 reports evaluation results.
>
> **Agent 1 does not modify Agent 2's proposer.**
>
> **Agent 2 does not manufacture or adjudicate Agent 1's NAT gold.**
>
> ---
>
> # ANTI-DRIFT RULES
>
> Do not:
>
> ```text
> return to scholar-oracle work
> build CorroborationBench
> build TantraFact
> build argument products
> reorganize Agent 1 eval infrastructure
> spend the session polishing architecture docs
> jump to C1 while RAW-L0 is not autonomous
> jump to scale while L200 is not validated
> claim semantic correctness from structural-validator success
> tune on TEST
> replace failed model calls with empty success
> ```
>
> If a lower checkpoint fails, work there until it passes.
>
> ---
>
> # AUTONOMY BEHAVIOR
>
> **Do not return because one task succeeded.**
>
> The sequence is:
>
> ```text
> implement
> → run
> → measure
> → attack
> → patch
> → regression test
> → rerun
> → checkpoint
> → continue
> ```
>
> A commit is a checkpoint, not completion.
>
> A certificate is evidence, not permission to stop.
>
> When a defect appears:
>
> ```text
> reproduce
> → classify
> → patch
> → add regression test
> → rerun affected checkpoint
> → continue
> ```
>
> Do not ask the user to choose obvious engineering decisions.
>
> Make the conservative choice consistent with:
>
> ```text
> provenance
> fail-closed semantics
> high precision
> bounded uncertainty
> idempotency
> immutable state
> ```
>
> ---
>
> # CHECKPOINT LOG
>
> Maintain a machine-readable or deterministic checkpoint ledger:
>
> ```text
> CP0 MODEL SUBSTRATE
> CP1 VALIDATED RAW-L0
> CP2 AUTONOMOUS RAW-L0
> CP3 RAW→L2 CONTINUITY
> CP4 L200 REDESIGN
> CP5 L200 DEV GATE
> CP6 L200 HELD-OUT
> CP7 AUTONOMOUS L200
> CP8 AUTONOMOUS C1
> CP9 FULL UNATTENDED VERTICAL
> CP10 IPVV SCALE
> ```
>
> Each checkpoint record must contain:
>
> ```text
> status
> commit SHA
> input corpus hash
> worker SHA
> validator SHA
> model/adapter
> prompt hash where applicable
> n inputs
> n committed
> n failed
> semantic metrics
> latency metrics
> replay result
> adversarial tests
> unresolved blocker
> ```
>
> Never mark a checkpoint PASS manually without corresponding artifacts/results.
>
> ---
>
> # STOP CONDITIONS
>
> Return only when one of these occurs:
>
> ## A. Terminal success
>
> `CP9 FULL UNATTENDED VERTICAL` passes.
>
> Prefer continuing into bounded IPVV scale if resources permit.
>
> ## B. Genuine external blocker
>
> Further work requires unavailable credentials, service access, corpus material, or infrastructure with no reasonable fallback.
>
> A single failing model/API is not automatically a blocker—try the alternate ModelAdapter/backend.
>
> ## C. Safety/reliability blocker requiring user decision
>
> Two or more reasonable architectures have materially different irreversible consequences and the frozen doctrine does not resolve the choice.
>
> Ordinary implementation choices do not count.
>
> ---
>
> # FINAL HANDOVER
>
> When you eventually return, give:
>
> ```text
> 1. commits pushed
>
> 2. checkpoint table:
>    CP0 ... PASS/FAIL
>    CP1 ... PASS/FAIL
>    ...
>
> 3. exact evidence for every PASS
>
> 4. autonomous RAW-L0 result:
>    corpus
>    n passages
>    success/failure
>    latency
>    semantic acceptance
>    replay
>    crash/resume
>
> 5. L200 semantic metrics:
>    DEV
>    held-out TEST if reached
>
> 6. C1 state
>
> 7. full vertical state
>
> 8. production throughput/cost if measured
>
> 9. unresolved failures
>
> 10. highest-value next moves
> ```
>
> Push safely to `agent2`.
>
> **Start at the earliest checkpoint not genuinely proven. At present that means the ModelAdapter/RAW-L0 reliability gap. Do not resume L200 as the primary task until autonomous RAW→L0 has actually passed its checkpoint.**
