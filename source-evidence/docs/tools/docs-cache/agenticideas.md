# THE AGENTIC-IDEAS PEER REVIEW (correcting the Layer 12 build order)

*2026-08-14. A critical reconciliation of the agentic-build plan against the actual Pāṭala state. The
headline correction: **we already built the epistemic control plane (Vouch is redundant); the missing
layer is operationalizing independent human scholarship over the machinery we already possess.** This
sharply reorders the Layer 12 pieces and redefines the moat. Source: `docs-cache/agenticideas.md`.*

---

## THE HEADLINE CORRECTION

> The missing layer is NO LONGER "how does Pāṭala decide whether an assertion is trustworthy?" (we built
> that: review_engine, adjudication, epistemic ceilings, crux propagation). The missing layer is **"how
> does Pāṭala operationalize independent human scholarship at scale over the epistemic machinery it
> already possesses?"**

| Previous advice (coordinate/15-plane) | Revised verdict |
|---|---|
| Build a Vouch-like proposal/review substrate | **Mostly wrong — duplicate architecture** (we have it) |
| Adopt Vouch invariants | Yes, selectively (no silent mutation, decisions persist, reviewer independence, reproducible validation) |
| Adopt Agetor Task≠Run | **Strong yes — operations only, outside the epistemic graph** |
| Add generic multi-axis review states | Already present conceptually — keep the domain-specific richness |
| Build `patala_next_action()` | Yes, but **lexicographic policy, not weighted; AFTER the scholar bottleneck** |
| Weighted graph score now | **Too early** — no outcome data yet; Goodhart risk |
| Scholar review as one stage | **Massively understates it — it's THE product** |
| Docling/Zotero | Still sensible, but fall dramatically in priority |
| Education graph + mastery | Correct, but downstream — freeze until the scholar vertical works |

---

## THE REORDERED PIECES (what we should actually build next)

### Piece 5 (redefined) — the External Scholar Attestation Vertical
**Goal:** prove a real scholar can independently inspect + adjudicate ONE complete argument (e.g. a gold
IPVV argument). Not "AI proposes / scholar clicks approve" (that's a moderation queue) — the valuable
object is the **scholarly attestation itself**:
```
ScholarlyAttestation: scholar_id · target_id/version/hash · expertise_scope · review_dimension
  · stance (ACCEPT/ACCEPT_WITH_QUALIFICATION/REJECT/CONTEST/UNDERDETERMINED)
  · rationale · cited_evidence[] · proposed_correction[] · confidence
  · disclosed_conflicts[] · compensation_context · timestamp
```
**The critical rule:** a scholar does NOT turn something into Truth by clicking approve. They ADD a
high-value, attributable epistemic event. Three specialists can disagree and all three are preserved.

**The proof:** after a scholar adjudicates, **intentionally modify an upstream translation** and verify
which proposition/argument/synthesis/scholar-attestation becomes stale and propagates correctly. That is
the real moat — not collecting a review, but **propagating a scholarly correction through the
intellectual dependency graph.**

### Piece 6 — Operational Task/Run Provenance (Agetor-inspired, operations only)
```text
Task (id, kind, target_ids[], objective, dependencies[], policy)
Run (id, task_id, agent, model, input_snapshot, started_at, ended_at, outcome)
RunEvent (run_id, sequence, event_type, artifact_ref, timestamp)
→ Run generated→ C1:… / ArgumentProposal:…
```
**No epistemic ontology changes.** `execution success ≠ epistemic success` — a task can have ten
successful runs and zero accepted results. This is clean and NOT duplicative.

### Piece 7 (redefined) — the Epistemic Work Queue v0 (NOT ML)
Start with **lexicographic policy**, not weighted magic:
```
1. correctness blockers → 2. source/provenance blockers → 3. stale descendants from corrections →
4. high-propagation unresolved cruxes → 5. specialist-review bottlenecks → 6. gold-set expansion →
7. breadth/coverage → 8. speculative enrichment
```
Inside a bucket: `downstream exposure / expected scarce-resource cost`. Every recommendation explains
itself (the "why" is human-checkable). **Core quantity = epistemic exposure** `E(v) = U(v)×I(v)×P(v)`
(unresolved uncertainty × epistemic importance × propagation) + **review leverage**
`L(v) = Δtrusted-graph / expected-cost`. A 5-minute scholar decision on one Sanskrit reading that
controls 8 propositions/3 arguments/2 syntheses can outrank translating 50 easy passages.

**Piece 7 v0 is an INSTRUMENTATION project, not an optimization project.** Collect
predicted-vs-actual cost/uncertainty/descendants/reviewer-requirement per resolved task; only after
hundreds of events decide policy vs heuristic vs bandit vs learned.

**The Goodhart warning:** `next_action()` can affect the graph it later measures. Rewarding
"descendants unlocked" → agents inflate the graph; "uncertainty reduced" → manufactured uncertainty;
"claims accepted" → easy claims. Score from quantities agents can't cheaply manipulate: source-dependency
structure, existing downstream published use, independent review disagreement, staleness propagation,
external demand, manually-designated priority. **Deterministic policy before learned optimization.**

---

## THE REFINED MOAT

Earlier: `M = D×P×V×N×A`. Now make V explicit:
```
V = F × J × C
  F = transformation faithfulness
  J = independent adjudication
  C = correction propagation
M = D × P × F × J × C × N × A
```
Each alone is copyable (corpus, LLM translations, argument graph, UI, even scholar profiles). But
**versioned primary texts + exact derivation chains + semantic-strength controls + argument/crux graphs +
independent named scholarly adjudications + durable disagreement + automatic correction propagation + a
historical record showing how every public conclusion became warranted** is a very different asset.

**Commit C.1's lesson → the general law:**
```
valid provenance ⇏ valid semantic transmission
```
So every transformation boundary needs its own fidelity contract:
`Sanskrit→translation→proposition→argument role→synthesis→essay→educational explanation→generated video`.
The moat isn't provenance alone; it's **provenance + transformation-faithfulness**. Most future systems
can say "this answer cited source X"; far fewer can show "every semantic transformation from source X to
this sentence was individually constrained not to increase strength beyond its upstream support."

---

## OTHER CORRECTIONS

- **Scholar reputation:** never one `ScholarScore`. Model expertise graphically (tradition/language/
  period/capability/corpus) + accumulate evidence (reviews, agreement, upheld corrections, citations).
  No universal Elo.
- **"VERIFIED" should soften over time** as scholars enter. Keep the machine status but distinguish
  `mechanically_validated / internally_adjudicated / externally_reviewed / specialist_supported /
  contested / superseded` — let clients choose thresholds (consumer = internally_adjudicated; training
  benchmark = specialist_supported; critical edition = show all contested). Convert uncertainty into
  infrastructure.
- **Standards stay peripheral** (Vouch/Agetor/Docling/Zotero/Hermes, like SEPIO/xAIF/nanopubs). Pāṭala
  owns the intellectual operating system: scholarly identity, textual provenance, translation decisions,
  epistemic transformations, argument structures, cruxes, review history, scholar adjudication,
  correction propagation, epistemic ceilings.
- **The scholar network** is a scholarly-verification network: the atomic contribution is a small citable
  attributable version-bound machine-readable potentially-compensable adjudication ("Scholar A adjudicated
  Sanskrit span X; Scholar C rejected warrant W"), not a paper. Fifty high-value adjudications > one six-month
  publication.

---

## THE DEFENSIBLE ORDER (peer-review-first)

```
IPVV → one defensible translation vertical → one defensible proposition vertical →
one defensible argument vertical → INDEPENDENT SPECIALIST ATTACKS IT →
Pāṭala records disagreement/correction → correction propagates properly →
SECOND scholar can inspect that entire history
```
If that works, everything else gets easier. The demonstration: **machine-assisted scholarship can expose
its entire epistemic derivation to independent human adjudication without flattening disagreement or
losing provenance.** That's rarer than another research-agent framework.

---

## IMPACT ON LAYER 12 (docs/layers/12-live-system.md)

This does NOT rebuild the plan — it **reorders and sharpens it**:
1. Pieces 1-4 (state/projection/staleness/MCP) — unchanged, still build.
2. **Piece 5 becomes the Scholar Attestation Vertical** (not "the review gate" — we have the gate).
3. **Piece 6 (Task≠Run) becomes operations-only**, explicitly outside the epistemic graph.
4. **Piece 7 becomes the Epistemic Work Queue v0** — lexicographic policy + instrumentation, NOT ML.
5. The moat is refined: `M = D×P×F×J×C×N×A`.
6. The immediate frontier is **NOT making Pāṭala more agentic** — it's proving a serious scholar can enter,
   disagree at the right epistemic level, and make the whole graph more correct without destroying provenance.
