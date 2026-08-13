# PĀṬALA — LIVE REPOSITORY ARCHITECTURE SPEC

**Date:** 2026-08-13  
**Repository audited:** `prx0r/patala`  
**Mode:** read-only repository reconciliation; no Git tree was edited.  
**Purpose:** turn the existing multi-agent implementation into one coherent scholarly kernel and one executable product loop.

## Executive verdict

Pāṭala should not be organized around agents, products, or external standards. It should be organized around one canonical, versioned scholarly state:

> **stable source identity → evidence → interpretation → proposition/commitment → argument-under-frame → review → dependency consequences**

Agents propose changes to that state. Products project or review it. Benchmarks test machines against frozen snapshots of it. External systems provide replaceable execution and interoperability.

The strongest existing implementation is not any isolated parser, benchmark, or UI. It is the **executable-corrections vertical**: a review over a versioned scholarly object changes derived downstream state without rewriting history. The live Agent1 test demonstrates the intended semantics on `ARG-002 / G2-TC2`: revision preserves v1, creates v2, marks `G2-INF1` and `G2-CONC` `NEED_REVIEW`, leaves unrelated `ARG-004` untouched, and remains deterministic.

The immediate architectural problem is semantic duplication. Today:
- `data/corpus/primitives.ts` carries an epistemic-state vocabulary.
- `data/corpus/graph.ts` carries overlapping graph/annotation state.
- `pipeline/review_engine.py` carries another review/effective-state vocabulary and its own `ReviewEvent`.
- source/evidence code has more specialized source authority semantics.
- benchmark gold has a separate review ladder.
- RAW-L0 uses `VERIFIED` for a workflow state that is not equivalent to scholarly verification.

These are not merely naming issues. If left unresolved, every product will implement its own meaning of “reviewed”, “verified”, “supported”, and “accepted”.

## The design in one diagram

```text
                      REPLACEABLE INFRASTRUCTURE
     OCR/HTR · Sanskrit analyzers · retrieval · annotation · review UX
       bibliography · PIDs · benchmark runner · agent runtime · export
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    PĀṬALA CANONICAL KERNEL                         │
│                                                                     │
│  IDENTITY        EVIDENCE          INTERPRETATION                   │
│  Work            SourceAssertion   PhilologicalProof                │
│  Witness         EvidenceUse       TranslationDecision              │
│  Passage/Span    Corroboration     TermSense                        │
│  ObjectVersion                    SemanticAlignment                 │
│                                   Proposition + derivation          │
│                                   Commitment                        │
│                                                                     │
│  REASONING                       AUTHORITY + TEMPORALITY             │
│  ResearchQuestion               Contributor / Credential            │
│  DebateFrame                    ReviewEvent                          │
│  Inference / Argument           DependencyEdge                      │
│  Attack / Defeater              DerivedState                        │
│  Crux                           ImpactReport                         │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
            ┌───────────────────┼────────────────────┐
            ▼                   ▼                    ▼
        PRODUCTS            BENCHMARKS              API/MCP
      Audit/Review         frozen fixtures      commands + views
      Workbench/Hub        Inspect adapter
```

## First system to ship

Do not build five disconnected products. Build one closed loop:

```text
AUTONOMOUS FACTORY
        ↓
  candidate scholarly objects
        ↓
  hard-case extraction
        ↓
PĀṬALA-IPVV BENCHMARK ←──────────────┐
        ↓                            │
TRANSLATION AUDIT                    │
        ↓                            │
SCHOLAR REVIEW / CORRECTION          │
        ↓                            │
ReviewEvent + ObjectVersion          │
        ↓                            │
dependency recomputation             │
        ↓                            │
reviewed before/after fixture ───────┘
```

This miniature already contains the future company: unique data, difficult cases, expert decisions, correction history, evaluation, agent improvement, and product utility.

## Recommended execution order

1. **Kernel reconciliation** — shared `ObjectRef`, version binding, authority axes, one review command boundary.
2. **RAW-L0 hardening** — no surface-token-as-lemma, passage completeness, explicit partial state.
3. **Review engine v2 hardening** — append-only persistence, authorization, independence, concurrency, reducer/version lineage.
4. **Benchmark adapter** — preserve `benchmarks/v0` as evaluation plane; execute through Inspect.
5. **Translation Audit v0** — deterministic findings first, exact spans, canonical refs, no semantic overclaim.
6. **Audit → Review → Benchmark loop** — reviewed findings manufacture candidate benchmark fixtures through a one-way exporter.
7. **Model-proposed Audit v1** — only after deterministic/product plumbing is real.
8. **Calibration v2** — detector-by-detector against reviewed fixtures.
9. **Pāṭala Review** — compile native arguments first; arbitrary PDFs much later.
10. **Workbench** — once repeated Audit/Review use proves which scholar actions matter.

See the remaining files for exact contracts, migrations, and backlog.
