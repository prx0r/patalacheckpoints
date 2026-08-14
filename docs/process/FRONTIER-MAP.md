# THE FRONTIER MAP — every layer's best-version, why, and how to build it

*2026-08-14. The capstone: for EVERY Pāṭala layer, what it is now, what external tools/githubs/repos
we've gathered that apply, what the FRONTIER best-version is, why (the frontier reasoning), and the
concrete build path to get there. This is "we have good homegrown mechanisms — here's how each becomes
industry/frontier-aligned using the ecosystem we've catalogued."*

**Sources:** the 69 external tools (`external-tools.md`), the 11 githubclones sections (A-K), the
`INDUSTRY-ALIGNMENT.md` standard map, and the live state (`docs_state.py`).

---

## LAYER 00 — GOVERNANCE ✅ BUILT

**Now:** anti-theatre doctrine, authority ladder, operating axioms, DAG (`CANONICAL-DAG.yaml`), Hermes.
**Tools/repos:** Hermes `/goal` + quality gates · agtx (`get_allowed_actions`) · the peer reviews.
**Frontier best-version:** the constitution + the **live-state projection** (docs derive from
`object_registry`, never hand-written). The "Pāṭala decides what matters; Hermes decides how" boundary.
**Why:** governance is the anti-theatre guard; the frontier is making it *enforced*, not advisory.
**Build:** finish `docs_state()` + `check_docs_stale.py` (Piece 1-2 of Layer 12) so the doctrine is
machine-checked, not hoped.

## LAYER 01 — INGESTION ✅ BUILT

**Now:** SourceAsserter, 8 adapters, R2 Bronze, entity reconciliation. 32k SOURCE objects.
**Tools/repos:** Kraken/eScriptorium (OCR) · pe-ocr-sanskrit (benchmark) · Docling/GROBID/Zotero
Translation Server (document) · CTS (identity) · `register_sources`/`acquire_*`.
**Frontier best-version:** a metadata-first acquisition pipeline: **discover → resolve identity (CTS/PANDiT) →
decide rights/value → fetch bytes (R2) → reconcile → SOURCE** — with every OCR model tested by
`OCRProofBenchmark` before entering the factory.
**Why:** the review showed much of the Sanskrit substrate is already machine-readable; the frontier is
*not* re-parsing but *resolving identity + rights first*, then acquiring.
**Build:** wire Kraken→PageXML→passage; add `cts_urn` to identity; the OCRProofBenchmark gate.

## LAYER 02 — ATLAS ✅→PARTIAL

**Now:** 22-table Postgres, resolver, API, crosswalk, deterministic UUID. 254 works, 268 authority_evidence.
**Tools/repos:** CTS/CapiTainS (passage identity) · Saktumiva (critical edition) · knowledgeProvenance +
nanopub + Eigenius (provenance) · **Stencila** (schema compilation) · OpenAlex/Crossref/VIAF.
**Frontier best-version:** the textual-transmission graph (Work→Edition→Witness→Surrogate→E-text→Source
kept distinct) + per-dimension authority + **CTS URN on every passage** + **Stencila-compiled schemas**
(solving the SCHEMA-AUDIT divergence).
**Why:** the identity distinction + provenance are the moat; CTS + Stencila make it *interoperable* and
*drift-free*.
**Build:** add `cts_urn`; adopt Stencila (one YAML schema → compiled TS/Python/JSON-Schema); consolidate
the diverged ReviewEvent/Authority/Proposition.

## LAYER 03 — FACTORY ✅→PARTIAL (SOURCE→C1 real; SYNTHESIS/ESSAY/EDUCATION empty)

**Now:** workers t1-l200-c1, object_registry, scheduler, DAG, event ledger. 32k SOURCE, 791 L0, 10 ARG.
**Tools/repos:** Vidyut (Sanskrit kernel) · ByT5-Sanskrit + Heritage (proof generators) · Mitrasamgraha +
MITRA (translation benchmarks) · awesome-align/bertalign (alignment) · MQM (error vocab).
**Frontier best-version:** the **proof-carrying compiler** — every object is a `TranslationProof`/derived
object carrying source_identity → analysis → alignment → semantic_obligations → unverified → checks, with
**no single aggregate score** + redundant independent auditors. Plus the DAG extending to SYNTHESIS/ESSAY/
EDUCATION (currently 0).
**Why:** `L200`/proof-carrying is the novel moat; the upper layers are declared-but-empty.
**Build:** design the `TranslationProof` schema; wire the Mitrasamgraha error-family validators; enable
ARGUMENT→SYNTHESIS→ESSAY→EDUCATION workers (the audit's #1 gap).

## LAYER 04 — EVIDENCE ✅ BUILT

**Now:** contracts (external_record, derived_scholarly_object, source_evidence_profile), 69 tools, eval plane.
**Tools/repos:** Stencila (schema) · PROV-O/FaBiO/W3C/CiTO (already aligned) · the standards map.
**Frontier best-version:** Stencila-compiled contracts + the `assertion-evidence-paper` ontology survey
ingested (avoid 20 yrs of evidence-vocab reinvention).
**Why:** the contracts are already standards-composed; the frontier is *compiling* them (no drift) + learning
from existing evidence ontologies.
**Build:** adopt Stencila for contract compilation; ingest the assertion-evidence survey.

## LAYER 05 — RESEARCH / EPISTEMIC CORE ✅→PARTIAL (the moat)

**Now:** argument/crux/synthesis compilers + golds; 10 ARG objects, 0 SYNTHESIS/ESSAY/EDUCATION.
**Tools/repos:** EleutherIA (dual-layer primary-vs-reception graph) · Debate Map + Because (argument UI) ·
Text Annotation Graphs (hypergraph) · xAIF/oAMF (interop) · SocraticKG (QA extraction).
**Frontier best-version:** the **epistemic kernel** — proposition identity + argument reconstruction +
semantic-strength ceilings + crux propagation, made **xAIF-interoperable** and expressed as **hyperedges**
(relationships participate in relationships, per TAG).
**Why:** this is the true moat; the frontier is making it interoperable + hypergraph-expressive + blind-adjudicated.
**Build:** enable SYNTHESIS/ESSAY/EDUCATION; add xAIF export; study TAG for the argument-annotation hypergraph.

## LAYER 06 — COMMENTARIAL 🔴 DESIGN

**Now:** design only (paper → ScholarContributionPacket).
**Tools/repos:** Docling/GROBID (substrate) · SocraticKG (QA extraction) · instagraph/seventeen-centuries
(KG candidates) · DSPy (measurable extraction) · RARR/RefChecker/GraphCheck/CIBER (verifier ensemble) ·
Vouch (review-gate — we have it better).
**Frontier best-version:** the paper→ScholarContributionPacket compiler, with the QA-intermediate
(SocraticKG) → DSPy-optimized extraction → verifier-ensemble → MACHINE_PROPOSED → scholar attestation.
**Why:** the secondary-scholarship layer is the biggest untapped asset; the frontier is candidate-generation
beneath Pāṭala's epistemic gates.
**Build:** the 11-step paper→packet pipeline (from `06-commentarial-graph.md`).

## LAYER 07 — VERIFICATION ✅ BUILT

**Now:** Inspect eval plane, 10 self-tests, benchmarks.
**Tools/repos:** Inspect (runtime) · RefChecker/FActScore (atomic claims) · AlignScore (cheap entailment) ·
CIBER (refutation retrieval) · GraphCheck (relational drift) · MQM (translation errors) · conformal (abstention).
**Frontier best-version:** the **verifier ensemble** — atomic decomposition → cheap entailment → escalate
borderline to LLM → calibrated abstention (OPEN) → certificate — with the L2/C1/Essay-License atomic-support
evaluator shared.
**Why:** "external methods test Pāṭala, they never define it" — the two-plane architecture.
**Build:** compose RefChecker/FActScore/AlignScore/CIBER into the ensemble behind Inspect.

## LAYER 08 — HUMAN AUTHORITY ✅→PARTIAL

**Now:** ReviewEvent ledger + review_engine + contracts. The Scholar Attestation Vertical is the frontier.
**Tools/repos:** TeamTat (blind adjudication) · RepoTrace (evidence-attached judgments) · OpenReview/COAR
Notify (publication) · CRediT/ORCID (credit) · knowledgeProvenance.
**Frontier best-version:** the **Scholar Attestation Vertical** — a real scholar adjudicates one gold
argument at the right epistemic level, and the correction **propagates** through the graph. Blind
reviewers (TeamTat) + evidence-attached judgments (RepoTrace) + named credit (CRediT/ORCID).
**Why:** the review-gate is built; the frontier is *operationalizing independent human scholarship over it*.
**Build:** the Scholar Attestation Vertical (Layer 12 Piece 5) — one gold argument, real scholar, correction propagation.

## LAYER 09 — ORGANISM 🔴 DESIGN

**Now:** design only (human-understanding graph). Education = 0 objects.
**Tools/repos:** **Engram** (education runtime — dependency-graph learning, FSRS, receipts) · learn-codebase ·
Graphiti (temporal user graph) · pyBKT/pyKT (learner) · DeepTutor (L1/L2/L3 memory) · adaptive-kg (interfaces).
**Frontier best-version:** the immutable interaction ledger → discrete graph projections (temporal user /
learner / question-gap) → the education compiler over the epistemic graph, with **Engram-style predict→act→
explain + FSRS + receipts-not-enthusiasm**, and UNKNOWN as a first-class object.
**Why:** the Q moat variable; the consumer app as a sensor. Engram makes the education half concrete.
**Build:** clone+adapt Engram for the education runtime; the interaction ledger (from `consumerorganismtech`).

## LAYER 10 — SURFACES ✅→PARTIAL

**Now:** app/ (Next.js), mcp/, openpatala, Astro. 43 API routes, 29 MCP tools.
**Tools/repos:** Mirador 4 (+TextOverlay) (manuscripts) · Remotion/OpenMontage (media) · Postiz (distribution) ·
Datasette (read plane) · RO-Crate (export) · DTS (text API) · IIIF.
**Frontier best-version:** the surfaces are **projections over one canonical graph** (Vision 12), with the
agent-native API (one-question=one-call bundles), Mirador-embedded manuscript viewing, and the Datasette-style
immutable read-plane.
**Why:** "one core, five permission-scoped surfaces" — never two databases; agents get precompiled bundles.
**Build:** the agent-bundle compiler + Mirador embed + the Datasette-style immutable read-plane experiment.

## LAYER 11 — ORG & ECONOMICS 🔴 DESIGN

**Now:** documented strategy only (credit, market, partnerships).
**Tools/repos:** CRediT/ORCID/ROR (credit) · Postiz Agent (distribution) · the partnership docs · the
AttributionEvent design (from `06-commentarial-graph.md`).
**Frontier best-version:** the **scholarly-verification network** — atomic contributions (a scholar
adjudicates span X, another rejects warrant W) that are small/citable/attributable/version-bound/machine-
readable/compensable, with **expertise modeled graphically** (not one Elo score) + `credit ≠ permission`.
**Why:** the scholar-economics moat; fifty high-value adjudications > one six-month paper.
**Build:** the AttributionEvent + scholar-expertise graph (from the agenticideas review).

## LAYER 12 — LIVE SYSTEM ✅→PARTIAL

**Now:** Tier-1 truth (registry/review/events) real; projection/staleness/MCP/queue pending.
**Tools/repos:** Hermes (execution) · Agetor (Task≠Run) · Beads-Viewer (graph triage) · mcp_agent_mail (leases) ·
coordinate + agenticideas peer reviews.
**Frontier best-version:** Pāṭala decides what matters (graph-aware `patala_next_action`), Hermes decides
how; docs project from truth (never stale); the Scholar Attestation Vertical is the priority.
**Why:** the live system makes everything else non-theatre.
**Build:** the 7 pieces (projection, staleness, MCP verbs, scholar vertical, Task≠Run, work queue, profiles).

---

## THE ONE-LINE STRATEGIC POSITION (the whole thing)

> **Pāṭala = a small typed epistemic kernel + compiler, made frontier by: (1) proof-carrying objects
> (TranslationProof/L200), (2) industry-aligned adapters (IGT/TEI/CTS/MQM/xAIF/RO-Crate/C2PA), (3) the
> Scholar Attestation Vertical (independent human adjudication that propagates), and (4) the Q-moat
> organism (Engram-style learning + the human-understanding graph). Everything else is an adapter around
> world-class existing infrastructure.**

## THE BUILD PRIORITY (dependency-ordered, high-leverage first)

1. **Layer 12 Pieces 1-4** (projection + staleness + MCP verbs) — makes everything non-theatre.
2. **Layer 12 Piece 5 — the Scholar Attestation Vertical** — the proof (the frontier differentiator).
3. **L200/TranslationProof schema** (Layer 03) — the novel translation moat.
4. **Stencila schema compilation** (Layer 02/04) — kills schema drift (SCHEMA-AUDIT).
5. **Enable SYNTHESIS/ESSAY/EDUCATION** (Layer 05) — the declared-but-empty upper layers.
6. **Engram education runtime** (Layer 09) — makes the organism concrete.
