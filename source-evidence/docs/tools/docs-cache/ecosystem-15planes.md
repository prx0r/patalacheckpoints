# THE 15-PLANE PĀṬALA ECOSYSTEM REVIEW

*2026-08-14. A comprehensive review of the GitHub ecosystem for building Pāṭala as "a stack of narrow
systems around a small kernel, with Hermes as the execution plane." Every plane lists what to pinch,
what to clone, and what Pāṭala must own. This is the raw research that sharpens `docs/layers/12-live-system.md`
(the live-system spec) and the `githubclones.md` registry.*

**The thesis:** the cleanest endgame is NOT one giant agent framework. It is a stack of narrow systems
around a small Pāṭala kernel, with Hermes as the execution plane. **Build the kernel brutally well; make
Hermes its nervous system; make these GitHub projects its organs.**

**The golden rule (unchanged):** Pāṭala decides what is true and what matters. Hermes decides who should
do the work and how it gets executed.

---

## The 15 planes (what to pinch)

### 0. Governing architecture
```
HERMES (execution/lifecycle) → worker lanes + observers → PĀṬALA CAPABILITY API (domain verbs, not CRUD)
→ PĀṬALA KERNEL (identity/evidence/passage/claim/argument/review/trajectory/event/permissions/provenance)
→ append-only event ledger → TRUTH GRAPH / CONSUMER GRAPH / WORK GRAPH
```

### 1. Agent control plane
- **Hermes Agent** — USE as primary orchestrator (kanban, profiles, worker lanes, skills, sessions).
- **Gas Town / Gas City** — study; pinch declarative workflow formulas (Bead/Rig), worktrees, role hierarchy.
- **Agetor** — pinch Task≠Run, pinned base commit, run history, SQLite events.
- **Overstory** (`jayminwest/overstory`) — typed agent mail, merge queues, watchdog hierarchy, permission enforcement.
- **agtx** — pinch state-machine transitions + `allowed_actions` over MCP.
- **mcp_agent_mail** — pinch identities, durable threads, file leases.
- **Weft** (`SoloJiang/weft`) — study remote questions, sidecar observation, skills mgmt.
- **Pāṭala primitives (don't invent Agent/Task):** `WorkItem · Run · Attempt · WorkerIdentity · Lease · Transition · ReviewGate · Artifact · Event`. A task's run history is gold (Run 1 failed → Run 2 candidate → Run 3 rejected → Run 4 revised → ReviewEvent 882 accepted).

### 2. Graph-aware work prioritization
- **Beads / Beads Viewer** — pinch deterministic graph analysis (PageRank, critical path, cycle detection, parallel tracks) returned as structured output.
- **`patala_next_action()`** should CALCULATE, not LLM-guess:
  `P(v) = w1·D + w2·B + w3·U + w4·Q + w5·R − w6·C` (downstream, betweenness, uncertainty, question demand, review deficit, cost).
- Return structured: `{object, priority, because: {blocked_arguments, affected_lessons, contradictory_reviews, evidence_grade}}`.

### 3. Canonical knowledge + review gating
- **Vouch** (`vouchdev/vouch`) — CLONE + dissect: agents propose durable knowledge, require cited evidence, separate proposal from approval, append-only audit, MCP. This is the closest to Pāṭala's central doctrine.
- **Sage Wiki** (`xoai/sage-wiki`) — pinch compiler model, alias resolution, fact→source citation, MCP retrieval, human-readable projection (don't use wiki as truth).
- **llm-wiki-newsroom** (`alfadur7/llm-wiki-newsroom`) — pinch the "reground" cycle (refresh published pages against source, don't assume docs stay correct).
- **llm-wiki** (`ddsyasas/llm-wiki`) — simple code to read.
- **Pāṭala proposals (each noncanonical until gated):** ClaimProposal · TranslationProposal · ArgumentProposal · RelationProposal · ConceptProposal · ReviewProposal.

### 4. Source-ingestion factory
- **Docling** + **Docling MCP** — the general document-normalization front end (PDF/Office/HTML/EPUB/images/audio/OCR/tables/formulas). Do NOT make DoclingDocument canonical.
- **GROBID** — academic PDFs (metadata, references, citation contexts, TEI).
- **S2ORC doc2json** — study normalization patterns.
- **Zotero Translation Server** — resolves DOI/ISBN/PMID/arXiv, parses webpages, BibTeX/RIS, normalizes metadata. "Boring piece that saves months."

### 5. Scholarly discovery + bibliography graph
- **Zotero MCP Plus** (`alisoroushmd/zotero-mcp`) — pinch graph-analysis + integration code.
- **Cita** (`diegodlh/zotero-cita`) — pinch sync/citation adapters (Wikidata/Crossref/SemanticScholar/OpenAlex), coauthorship networks.

### 6. Manuscripts + philology + scholar workbench
- **Mirador 4** (`ProjectMirador/mirador`) — embed/customize (IIIF, React 19), don't build a viewer.
- **Mirador TextOverlay** (`dbmdz/mirador-textoverlay`) — pinch manuscript OCR/transcription overlay.
- **Recogito Text Annotator** — embed selection/annotation UX (React/TEI).
- **INCEpTION** — study multi-annotator adjudication + machine-assisted suggestions; don't necessarily deploy.

### 7. Argument/evidence machine
- **ARG Tech AIF ecosystem** (`aif-arg-datasets`, `oAMF`) — build ADAPTERS to AIF/xAIF for interop; native representation stays richer.

### 8. Automated claim checking / research agents (the verification ensemble)
- **RARR** (retrieve→check→revise) · **RefChecker** (atomic claim) · **GraphCheck** (relationship structure) · **DSPy** (optimize against Pāṭala gold) · **IAM** (argument-mining decomposition). → an ensemble, not one big prompt.

### 9. Consumer temporal graph
- **Graphiti** (`getzep/graphiti`) — the temporal-facts + episode-provenance anchor, but as a PROJECTION from the event ledger, not canonical user history (extraction can be wrong).
- **CoWork OS** — study SQLite entity/relationship memory, temporal edges, `as_of` querying, confidence decay, memory-write governance.
- **DeepTutor** (`HKUDS/DeepTutor`) — pinch the L1/L2/L3 memory pipeline + KB version fingerprints (drift detection).

### 10. Learner model / education compiler
- **pyBKT** — interpretable mastery state.
- **Dialogue-KT** (`umass-ml4ed/dialogue-kt`) — tutor/student dialogue KT, turn annotation.
- **OATutor** — open-source BKT adaptive tutor patterns.
- **OpenTutor** (`zijinz456/OpenTutor`) — clone for consumer UX (source-grounded tutor, FSRS, concept graph).
- **adaptive-knowledge-graph** (`MysterionRise/adaptive-knowledge-graph`) — GOLD: Neo4j concept/prerequisite + OpenSearch + Ollama + SQLite learner state + BKT/IRT. Tear apart for the interfaces between components.

### 11. KG → human-readable projection
- **Epicenter** (`epicenter-md/epicenter`) — Markdown and DB as one truth (DB as the canonical, Markdown a view). Relevant to `project_state()`.
- **SQLite Sync** (`sqliteai/sqlite-sync`) — CRDT-backed SQLite replicas for offline scholars (LATER, not now).
- **sqlite-memory** — agent memory CRDT sync (reference only).

### 12. Observability
- **Phoenix** (`Arize-ai/phoenix`) — OpenTelemetry agent/LLM tracing + eval + experiments.
- **Langfuse** — self-hosted trace instrumentation. Preference: Phoenix/Langfuse for the external trace/obs plane; keep Pāṭala's epistemic review INSIDE Pāṭala.

### 13. Media organism
- **Remotion** — deterministic/data-driven video (React code as source of truth).
- **OpenMontage** (`calesthio/OpenMontage`) — MAJOR: agentic research→script→assets→editing, footage from Archive.org/NASA/Wikimedia, Remotion/FFmpeg. Do NOT build the video agent stack from scratch.
- **remotion-superpowers** — pinch director/media-scout/post-production agent job defs + MCP.
- **frankxai/remotion-video** — Hermes/Claude + Remotion short-form video factory. Definite clone.

### 14. Distribution + analytics
- **Postiz** (`gitroomhq/postiz-app`) — scheduling, analytics, multi-platform, public API.
- **Postiz Agent** (`gitroomhq/postiz-agent`) — the Hermes publishing lane should CALL this (CLI workflows).

### 15. The endgame feedback organism
The loop that closes: event ledger → research/agents → review-gated truth → products (scholar/education/media/personalized) → consumer interactions → new questions/gaps → back into the ledger.

---

## What Pāṭala must itself OWN (the moat — everything else is stolen)

- identity / provenance / permissions
- passage / claim / argument / review / trajectory / event semantics
- the epistemic review-gated promotion
- the capability API (domain verbs)
- the learner/education semantics
- the projection engine + staleness
- `patala_next_action()` triage

**Do NOT build:** PDF parsing, manuscript rendering, generic agent scheduling, generic trace observability, social upload adapters, BKT itself, basic annotation widgets, generic citation scraping.

---

## Immediate clone list (harvest implementations, don't vendor)

- Hermes Agent · Gas Town · Gas City · Overstory · agtx · mcp_agent_mail · Agetor · Beads · Beads Viewer · Vouch · Sage Wiki · llm-wiki-newsroom · Docling (+MCP) · GROBID · Zotero Translation Server · Zotero MCP Plus · Cita · Mirador 4 · Mirador TextOverlay · Recogito · AIF arg-datasets/oAMF · RARR · RefChecker · GraphCheck · DSPy · Graphiti · CoWork OS · DeepTutor · pyBKT · Dialogue-KT · OATutor · OpenTutor · adaptive-knowledge-graph · Epicenter · Phoenix · Langfuse · Remotion · OpenMontage · remotion-superpowers · frankxai/remotion-video · Postiz · Postiz Agent

*The objective is to harvest implementations, not to vendor everything. Pāṭala = a small kernel + Hermes
as nervous system + these projects as organs.*
