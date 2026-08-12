# HERMES × PĀṬALA — THE INTEGRATION (backend infra + advanced recipes)

*2026-08-12. The single canonical reference for how Hermes becomes Pāṭala's agentic backend. Merges the
backend-infrastructure model (verified feature→vision mapping, 2026-08-12) with the advanced integration
recipes (`hermespatala2.md`, from R2). **Thesis: Hermes is the cognitive execution fabric; Pāṭala is the
epistemic state machine. Hermes does not replace the agent architecture — it operationalizes it.***

---

## THE MENTAL SEPARATION (the core principle)

```text
PĀṬALA
= epistemic state machine
  objects / provenance / review / status /
  dependencies / claims / transitions

HERMES
= cognitive execution fabric
  sessions / skills / delegation / tools /
  scheduling / hooks / messaging / trajectories
```

Pāṭala tells Hermes *what kinds of transformations are epistemically legal*. Hermes gives Pāṭala the
machinery to perform those transformations repeatedly, concurrently, persistently, and increasingly well.

---

## PART I — HERMES AS THE BACKEND (verified feature → vision mapping)

*Every feature below was verified against `hermes --help` / subcommand help on 2026-08-12. Hermes already
provides the A0 governance primitives the agent-architecture vision specced as bespoke build work.*

| Hermes feature (verified) | Realizes the vision's... |
|---|---|
| **`kanban`** | **Agent 0's scheduler/constitution** — durable SQLite board, atomic task claims, dependencies, named-profile execution in isolated workspaces. Replaces bespoke typed-handoff + lane-ownership + gating. |
| **`--worktree`** | **The git-isolation fix for INCIDENT-2026-08-12-01** — "run in an isolated git worktree (for parallel agents)." Built-in; Agent 1 can never stage Agent 2's files. |
| **`cron`** | The "translate while I sleep" factory loop (scheduled A3 jobs, with `--skill --workdir --deliver`). |
| **`hooks` + `webhook`** | Dependency/staleness propagation (source change → invalidate L0 proof). Scholarly CI. |
| **`memory` + `memory-graph`** | Durable epistemic state (the Pāṭala soul in MEMORY.md; memory-graph = timeline of learned skills/memories). |
| **`checkpoints`** | Rollback — the mechanical guard behind "mistakes don't compound." |
| **`mcp` (tantrakosa server)** | The corpus as a native tool surface (21 tools: resolve, verify, themes, recommend, ...). |
| **`fallback` + `moa`** | Model resilience (no single point of failure; mixture-of-agents). |
| **`skills`** | The doctrine as executable procedure. |
| **`sessions`** | Persistent, searchable work (SQLite + FTS5; list/export/archive). |

**The thesis:** Hermes IS the kernel/A0 runtime. Pāṭala layers its epistemic state (the corpus ledger +
gold) and doctrine-carrying skills on top. It does NOT rebuild the agent runtime.

---

## PART II — THE REALIZED ARCHITECTURE

```
                HERMES (the kernel / A0 runtime)
   kanban(board+atomic claims+dep) · cron · hooks/webhook
   worktree(isolation) · memory · checkpoints · mcp · fallback/moa
                        │
   ┌────────────────────┼────────────────────┐
   ▼                    ▼                    ▼
 A2 patala profile   A3 patala profile    A1 patala profile
 (corpus compiler)  (translation factory) (philosophy)
 owns corpus_state   consumes NEXT_       owns gold/ARG/
 ledger + /api/corpus VALID_ACTION from    vertical objects
 + skills: prove      A2; cron executes    + skills: analyze
   │                    the eligible work    │
   └─────────┬──────────┴─────────┬─────────┘
             ▼                    ▼
         A4 review          A5 synthesis
         (skills: review)   (skills: research)
             └────────┬────────┘
                      ▼
                 A6 projection (skills: publish)
                 A7 scholar network (later)
```

And the end-state (from the architecture vision):

```
HUMAN / TELEGRAM → HERMES GATEWAY → Agent 0 → A1/A2/A3 → PĀṬALA MCP/API → EPISTEMIC GRAPH
                                                                    (review state · crux graph · corpus state)
Hermes = execution/reasoning/isolation/scheduling/tool-routing/procedural-learning/communication/trajectory
Pāṭala = identity/truth/status/provenance/dependencies/review/scholarly-ontology
```

---

## PART III — THE ADVANCED RECIPES (from hermespatala2.md)

### 1. Pāṭala agents = persistent Hermes identities, state OUT of Hermes memory
Keep authoritative state (ARG-002 status, CP3 status, source hashes, accepted claims, review decisions)
in **Pāṭala**. Hermes memory holds only **operating doctrine** (the soul). Use `session_search` (FTS5)
for historical recall.
```
Hermes memory  = operating doctrine
Hermes session = experiential history
Pāṭala git/graph = truth
```

### 2. Every Pāṭala transformation = a Hermes Skill, with skill evolution under review
Formalize `/patala-source-ingest`, `/patala-build-l0`, `/patala-translation-pass`, `/patala-c1`,
`/patala-theme-discovery`, `/patala-argument-extract`, `/patala-argument-review`, `/patala-semantic-align`,
`/patala-evaluate-argument`, `/patala-crux`, `/patala-session-close`. **Skill evolution** = Hermes
self-improvement proposes a skill patch → Pāṭala review gate → frozen benchmark → only promote if the
benchmark improves. Institutional learning at the process level, not model fine-tuning.

### 3. Hermes subagents as EPISTEMIC ADVERSARIES, not workers
Blind, isolated contexts. For argument reconstruction:
```
SUBAGENT A (minimalist)  recover only what the text licenses
SUBAGENT B (strong)      strongest coherent reconstruction
SUBAGENT C (adversary)   falsify A and B (reversed entailments, imported doctrine, scope jumps)
A cannot see B. Parent derives: agreement · disagreement · crux.
```
Generic recipe: `BLIND GENERATE → BLIND COUNTERGENERATE → ADVERSARIAL AUDIT → SYNTHESIZE DIFFERENCE → STORE DISAGREEMENT, NOT JUST WINNER`.

### 4. Blind adjudication tournaments
5 reconstruction agents → 3 critic agents (anonymized candidates) → 2 judge agents (no candidate
provenance) → parent records consensus/minority/exact-disputed-premises. **Don't average scores** — derive
stable claims, unstable claims, interpretive forks, load-bearing disagreements. A machine pre-review
dossier that compresses human attention.

### 5. `execute_code` as the deterministic tissue between reasoning steps
The model writes Python calling Hermes tools; only final output returns. For Agent 2: enumerate manifests,
query bibliography, hash sources, resolve IDs, compute missing transitions → print only anomalies
("17 stale source deps, 8 missing L0 artifacts..."). `LLM = judgment · execute_code = computation · Pāṭala = state`.

### 6. A Pāṭala Hermes plugin exposing the graph as VERBS, not files
Tools like `patala_resolve`, `patala_get_work_state`, `patala_next_action`, `patala_get_passage`,
`patala_propose_annotation`, `patala_record_review`, `patala_get_dependencies`, `patala_mark_stale`,
`patala_query_theme`, `patala_get_open_cruxes`. **Write verbs are PROPOSE / RECORD_REVIEW — never
SET_TRUTH / ACCEPT.** "AI proposes ≠ Pāṭala asserts" enforced at the tool boundary: a confused prompt
cannot call `patala_accept_claim` because it doesn't exist.

### 7. MCP/tool filtering = capability security per agent
Lane ownership becomes **permissions**, not documentation. Agent 1: read corpus, propose argument/theme,
run evaluator (NO source mutation, NO accepted-status). Agent 2: read/write corpus state, run source
verification, mark stale (NO philosophical acceptance). Agent 3: read eligible jobs, write machine-proposed
translation + C1 proposal (NO accept, NO bibliography mutation). Agent 4 (later): read proposals, create
review event, promote only under policy.

### 8. Hermes hooks = database triggers for epistemic invariants
- `pre_tool_call`: verify source ref resolves / work eligible / correct lane / correct worktree / deps current.
- `post_tool_call`: hash artifact, attach provenance, emit state-transition event, queue validation.
- `subagent_stop`: persist agent-role/model/source-hash/output-hash/result.
- `on_session_end`: run staleness check, theatre check, uncommitted-artifact check, skill-learning proposal, handoff summary.

### 9. Agent 4 = a review scheduler driven by graph conditions (not a to-do list)
Nightly NO-AGENT cron script queries Pāṭala (new proposals, stale artifacts, failed factory jobs,
unreviewed high-centrality claims, new cruxes) → only if meaningful, launch a review session ranked by
downstream impact / uncertainty / centrality / source quality. Graph-aware review allocation.

### 10. Webhook-driven scholarly CI ("GitHub CI for epistemology")
On a push to translations/ c1/ argument-gold/ theme-gold/ bibliography → Hermes determines affected
objects → runs the right audit (source change → A2 dependency audit; C1 change → A1 theme impact;
argument change → evaluator rerun; review event → projection regeneration) → posts a PR comment
(SCHOLARLY IMPACT: 2 source proofs stale, 4 propositions downstream, ...).

### 11. Hermes trajectories = a dataset of scholarly cognition (a moat)
Save source → machine reconstruction → tools consulted → alternative → criticism → revision → review →
human correction → final accepted object. 10,000 passages of "how difficult Sanskrit/philosophical
judgments get corrected" = training/eval data for translation, extraction, alignment, uncertainty
calibration, review prioritization. Hermes already has session/trajectory export — don't invent capture.

### 12. Counterfactual research swarms
Given a crux (e.g. vimarśa = SAME_SENSE vs NEAR_SAME vs DIFFERENT_SENSE), spawn isolated subagents each
on a graph snapshot with one variable changed; ask what arguments/themes/contradictions/claims change.
Parent compares worlds → CRUX IMPACT. Structured Monte Carlo over interpretation space.

### 13. Scholar simulation before scholar review
Skills = review methodologies, not fake personalities: `/textual-philologist`,
`/historian-of-philosophy`, `/formal-argument-reviewer`, `/translation-auditor`,
`/tradition-comparison-reviewer`. Apply several methodological lenses to every object. Human then sees
a machine pre-review (2 scope issues, 1 unsupported inference, ...) + remaining questions. Expert
attention compression.

### 14. Separate discovery models from adjudication models
Cheap/high-recall model for discovery (many themes/alignments/alternatives) → strong reasoning model for
critique → separate model to compress disagreement → human final. `cheap recall → expensive precision →
scarce human judgment`. Economic scaling.

### 15. Model disagreement itself as evidence
Run the same structured task with models A/B/C; store disagreement as a feature
(MODEL_CONSENSUS_HIGH / MODEL_DISAGREEMENT_HIGH). Correlate later with human corrections → an empirical
review-prioritization signal, better than raw LLM confidence.

### 16. Self-improving procedures from correction history (gated)
ReviewEvents → analyze recurring correction patterns → propose changes to `/patala-translation` /
`/patala-commitment-extraction` → run frozen benchmark before/after → **only promote if the benchmark
improves**. Never let Hermes self-improvement directly rewrite production procedures. Controlled drift.

---

## PART IV — THE THREE INTEGRATIONS TO BUILD FIRST

### A. Pāṭala skill pack (external skill dir)
Hermes supports `skills.external_dirs` — so `patala/skills/` (translate-passage, build-l0, write-c1,
theme-discovery, argument-review, session-close) stays the repo source of truth and becomes native Hermes
procedural memory without copying into Hermes.

### B. Pāṭala MCP/plugin capability layer
Expose structured graph verbs (`patala_*`) and whitelist them differently per agent. Gets agents away from
arbitrary filesystem reasoning.

### C. Blind adversarial delegation recipe
One canonical `/patala-adversarial-review` skill that auto-launches minimal reconstruction + strong
reconstruction + adversarial critic + synthesis, returning a structured disagreement object. Immediately
improves theme/argument/translation/semantic-alignment review.

---

## THE CARRY-FORWARD

> **Hermes should not replace the Pāṭala agent architecture. It should operationalize it.** Hermes is the
> cognitive execution fabric (sessions, skills, delegation, tools, scheduling, hooks, trajectories, isolation,
> resilience); Pāṭala is the epistemic state machine (identity, truth/status, provenance, dependencies,
> review, scholarly ontology). Build the three integrations first (skill pack, MCP capability layer, blind
> adversarial delegation); keep authoritative state in Pāṭala, doctrine in Hermes memory, history in Hermes
> sessions; and use `--worktree`, `kanban`, `cron`, and `hooks` for the A0 governance the vision specced.
