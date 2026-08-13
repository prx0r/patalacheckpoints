# AGENT 1 (ML) — NEXT STEPS (current execution, 2026-08-13 · REVISION 7 — SCHOLAR-CORPUS FOUNDATION)

*The current near-term plan. **Read `handover/agent-1-ml/HANDOVER-2026-08-13.md` FIRST** — the full handover.
This revision reflects the pivot: the ML vertical is frozen + peer-review-clean; the forward work is the
**scholar-corpus foundation (S0)** — turning the on-disk published-scholar corpus into a provenance-addressable
corroboration oracle by **borrowing mature open tools** and adding only the epistemic dependency graph. **Agent 1
is no longer "frozen and done" — it now owns the source-evidence layer + the scholar oracle.***

> **The one-line pivot:** we do NOT need a live human reviewer — the published scholars we already own
> (Sanderson/Ratié/Torella/Bäumer) are the scalable scholarly corroboration oracle. Build the substrate that
> makes them addressable, borrowing tools, adding only the epistemic seam.

---

## WHERE WE ARE (the vertical is peer-review-clean relative to the current objects)

The full Pāṭala Review vertical is built, validated, and pushed on `origin/agent1-argument-layer-a1b` (all
tests green):

```
source
→ local arguments (ARG-GOLD-002/004)
→ ContextualArgumentAudit (Nyāya gate ACTIVE)
→ ArgumentSynthesis (SYN-IPVV-REFLEXION-CORE-001, canonical)
→ monotone EO projection
→ one readable essay + EssayPlan
→ SentenceEvidenceAudit (+ 6 adversarial prose/paraphrase mutation classes)
→ deterministic k-core structural hierarchy + Louvain stability ablation (P-019 v2)
```

Commits: `0efc1df` (A.1) · `32083e6`+`d8b123b` (B) · `a2c4591`+`398958f` (C) · `b1fb034` (C.1) ·
`6b19f2b`+`cfcd1c5`+`aef17dd` (C.1 review passes) · `7ea182c`+`76263d8` (k-core/Louvain).

**The honest claim (narrow):** for one IPVV synthesis, Pāṭala produces a provenance-linked essay and
deterministically catches specified epistemic-laundering mutations (strength inflation, authorship laundering,
boundary erasure, rival laundering, warrant erasure, paraphrase expansion). NOT "Pāṭala writes reliable
scholarly essays."

---

## THE ESSAY IS PEER-REVIEW-CLEAN (relative to the current objects)

Repeated adversarial review found increasingly subtle authority/semantic-representation mismatches, all
corrected:
- S001 EXPANSIVE-backed by the synthesis · S003/S004 conservative to their propositions (no neighbor-claim
  leakage) · S005 reconstructed not authorial · S009 no longer strengthens G2-CONC / no "conclusion follows" ·
  S010 UNRESOLVED (does not manufacture an unaudited structural result) · S007/S012 boundaries preserved.

**The key finding frozen:** Pāṭala now distinguishes (a) metadata correctness, (b) semantic surface fidelity
(`PARAPHRASE_EXPANSION / CLAIM_SURFACE_INFLATION`), and (c) `reconstructable argument ≠ structurally validated
argument`. The remaining boundary: **semantic-relation labels are reviewer-assigned assertions, not
independently machine-proven facts.** C.1's guard rejects *declared* unsupported expansion; it does not yet
automatically establish that a declared `CONSERVATIVE_PARAPHRASE` is semantically correct.

## k-CORE / LOUVAIN (P-019 v2)

- k-core = deterministic STRUCTURAL embeddedness; Louvain = heuristic modularity community; human adjudication
  decides if any become themes. `k_core != theme`; no claim of philosophical centrality.
- **Empirical finding:** on the actual 63-node IPVV C1 graph, Louvain is STABLE (11 communities across 20
  seeds, 0 unstable boundaries, 187 robust co-clustering pairs). So the rationale for k-core is **deterministic
  embeddedness + reproducible graph statistics, NOT because Louvain was empirically unstable here.**

---

## THE FORWARD WORK (S0 — the scholar-corpus foundation)

Do NOT reopen the frozen ML vertical (no C.2, no more clustering, no re-doing the argument layer). The new work is
the source-evidence substrate + scholar oracle, per `source-evidence/docs/`:

```
S0.0 freeze the contract (RawSource→BibliographicRecord→Witness→SourceSpan→SourceAssertion→CorroborationEvent→consumer)
S0.1 external-tool pilot (GROBID/Zotero/Crossref/OpenAlex adapters + thin resolver; LIVE/RECORDED/UNAVAILABLE rule)
S0.2 missing semantics (SourceAssertion + CorroborationEvent validators; adversarial tests)
S0.3 product proof (one proposition resolves across bibliography/assistant/argument/site/education)
S0.4 F1 corroboration experiment (false-positive-tested) → CorroborationBench → TantraFact
```

**The immediate next step: the Inspect AI prototype** — port one existing benchmark + the laundering mutations
into an Inspect task (the benchmark runtime). Then PaperQA2 → INCEpTION → Recogito → STORM → COAR Notify (doc) →
Manubot → RAiD/credit (the ruthless 8-experiment order: each asks "does this delete a subsystem we planned to
write?").

---

## THE NEXT MOVE — AGENT 2 / AUTONOMOUS FACTORY (shared infrastructure, in order)

The coordinator's directive. Build the shared infra in this order, then the generic L0 controller:

```
1. registry-derived per-passage idempotency
2. single-writer lock
3. Hermes process-group timeout/orphan cleanup
4. stable passage_id + source-hash response binding
5. bounded/adaptive batching
6. lossless ASCII-avagraha support
7. OCR → SOURCE_BLOCKED
8. crash/resume + wrong-ID adversarial tests
9. Sanskrit-only replay certificate
10. small Kramasadbhāva unattended canary
```

**Do not build separate autonomous runners per layer.** Build the generic controller once at L0, prove it under
failure, then reuse the same state machine with layer-specific skill + registry + validator contracts across the
**canonical production stack**:

```
L0/L1 → L2 READ → L200 AUDIT → C1 → THEMES → ESSAYS → EDUCATION
```
with every stage supplying its own contract/validator/certificate and every transition independently resumable,
versioned, provenance-bound, fail-closed. **L200 is the future derivational grounding seam** for
propositions/arguments: a Proposition should eventually ground Proposition → C1 InterpretiveAssertion /
MaterialTranslationDecision → L2 reading span → L0/source spans, rather than jumping around L200. Do not retrofit
Agent 1 for this now; wire it when Agent 2 makes L200 autonomous/canonical. At that point "autonomous translation"
undersells it — it is an **autonomous scholarly compiler whose intermediate representations remain inspectable
and corrigible at every layer.**

---

## GIT STATE (unchanged, critical)

- Canonical work on **`origin/agent1-argument-layer-a1b`**. `origin/agent1-argument-layer` still has the fork
  (Agent 0 reconciliation — `handover/agent-1-ml/GIT-RECONCILIATION-2026-08-12.md`).
- Local worktree on `/mnt/HC_Volume_106427611` is **unstable** (files/branch pointers periodically revert).
  Treat the remote branch as authoritative; re-restore from it after any suspected revert.

## GUARDRAILS (unchanged)

1. Route everything through `benchmarks/v0/` + record a `BenchmarkRun`. 2. Join on `Ref` IDs — never fuzzy.
3. Do NOT hack viruddha into the frozen `nyayagate.py`. 4. Git discipline: stage your own paths, commit
immediately, never force-push/rewrite another lane's commit. 5. Update `CLAIMS.md` + drop a `SESSION-<date>.md`.
