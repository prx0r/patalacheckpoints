# THE LOGICAL ORDER — from IPVV to comparative essays (the zoomed-out build path)

*2026-08-12. The whole arc, in the order it should happen, using the IPVV as the working model for
everything. This is the "zoom out" — one coherent pipeline where each stage produces the substrate for
the next, all audited, all feeding the truth engine. Every stage is grounded in what already exists.*

---

## 0. The principle: one working model, driven through every stage

> **Correction (read first): `ML-ARGUMENT-REVIEW-CORRECTED.md`** — an external review corrected three
> framings in the earlier docs: (1) C1→Argument is NOT low-effort and C1 must only discover, never prove;
> (2) Lean is an optional instrument for strictly-formalizable subgraphs, verdict `FORMALLY_VALID_GIVEN_ENCODING`,
> not `PROVED`; (3) provenance ≠ support (4 levels), and disagreement needs attributed contexts not a flat
> graph. The stage order below is unchanged; those corrections refine HOW each stage is built.

The IPVV is the **working model** — the text we push through the entire pipeline first, so every stage
is proven before we touch other texts. When the IPVV pipeline works end-to-end, we replicate it on the
Tantrāloka, then the Spandakārikā, then across the tradition.

```
IPVV (working model)
  → C1          (commentary — EXISTS, 63)
  → CLUSTER     (group related C1s)
  → THEMES      (the recurring structures)
  → ARGUMENTS   (formal, from the themes + truth engine)
  → ARGUMENT PACKETS (the auditable objects)
  → ESSAYS      (from argument packets, provenance-carrying)
  → COMPARATIVE ESSAYS  (argument packets pitted across texts)
```

---

## 1. Stage by stage (in logical order)

### Stage 1 — C1 (exists, complete)
The 63 C1 read/ renderings + 10 structured c1_source records. This is the *local* meaning of each
passage. **Status: DONE.** This is the substrate.

### Stage 2 — CLUSTER (build)
Group the C1s by relation. The hybrid relation graph (semantic + curated `See also` + shared KEY TERMS +
sequence + interlocutor + function) → community detection (Louvain/Leiden, overlapping). A C1 lives in
several clusters (overlap, not partition).

**Why cluster before themes:** clustering is the *machine proposal*; themes are the *editorial result*.
You discover computationally, then adjudicate editorially. The pilot proved the mechanism on 25 C1s;
scale to all 63.

### Stage 3 — THEMES (build, editorial)
From the clusters, the editor names and accepts themes (overlapping; each with a THEME BOUNDARY — what it
does and does not claim). `themes/proposals/` (machine) → `themes/accepted/` (editorial).

**The question a theme answers:** *"what recurring structure emerges across these C1s?"* — e.g. Memory
and Recognition, Non-constructed Self, the Order-less Support, Causality as the Knower's Agency.

### Stage 4 — ARGUMENTS (build, the truth-engine stage)
From a theme + its member C1s, construct a formal argument. This is where the **truth engine** enters:
- the C1s/IAs → premises (each premise resolves to a passage via `/api/resolve`)
- the Nyāya gate (hetvābhāsa checks + falsifier-required) validates each claim
- the conclusion is the theme's core claim, with an honest boundary (what it does NOT establish)

**This is the audit point.** Every argument premise → passage → Sanskrit. No claim survives unless it
resolves and passes the gate.

### Stage 5 — ARGUMENT PACKETS (build, the auditable object)
Each argument becomes an `ArgumentTruthPacket`: conclusion ← premises ← passage_ids + inference + kind +
**derived claim-strength** (PROVED via Lean / REVIEWED / WELL_SUPPORTED / PLAUSIBLE / SPECULATIVE) +
`tension_id` (the PUSHING question it resolves).

This is the *first-class, citable* object — the thing essays and comparative matrices are built from.
Tracked on the hub (`pt:hub:<work>:argument:<slug>`).

### Stage 6 — ESSAYS (build, provenance-carrying)
From the argument packets, an essay is *derived* (not free-written): each sentence cites its argument
packet → premises → passages, tagged Quotation/Compression/Inference (the GenProve/TRACER pattern). The
**graph-derived state-of-play** (the `truthreview` acceptance test) is what the essay reports: which
candidates survive criticism, why, with every edge shown.

### Stage 7 — COMPARATIVE ESSAYS (build, the cross-text payoff)
Now the argument packets are **pitted across texts**. The same question-shape (PUSHING DNA) is asked of
the IPVV, the Tantrāloka, the Spandakārikā:
- each text's argument packet → the answer-cell in a comparative matrix
- relations typed `OVERLAPS / BRIDGES / CONTRADICTS / DIFFERENT` (the truth-engine `correspondences`)
- a comparative essay is *derived* from the matrix column, not re-researched

**Example:** "Reflexivity" — IPVV packet (vimarśa = nature) vs Dharmakīrti packet (svasaṃvitti) vs
Ñāṇavīra packet (groundless) → a comparative essay that holds the three live positions, with each claim
auditable to its source text.

---

## 2. Why this order (the dependencies)

```
C1 ──► CLUSTER ──► THEMES ──► ARGUMENTS ──► PACKETS ──► ESSAYS ──► COMPARATIVE
  (substrate)  (proposal)   (editorial)  (truth engine) (auditable) (derived)   (cross-text)
```

- **Cluster before themes:** machine proposal before editorial acceptance (no contamination).
- **Themes before arguments:** an argument needs a theme's member-C1s as its premises.
- **Arguments before packets:** the packet is the auditable FORM of the argument.
- **Packets before essays:** an essay is *derived* from packets, never free-written.
- **Essays before comparative:** comparative needs each text's packets to pit them.

---

## 3. The truth engine's role (where it sits)

The truth engine is **not a stage** — it's the **audit layer that runs through stages 4–7**. It provides:
- the **Nyāya gate** (stage 4): does a claim pass hetvābhāsa + falsifier checks?
- the **Bayesian scorer** (stage 5): derived claim-strength from weighted log-Bayes-factors
- the **state-of-play** (stage 6): graph-derived essay verdict
- the **correspondences** (stage 7): typed cross-text relations

So the truth engine is the *engine of honesty* for the whole upper pipeline. Stages 1–3 build the
material; stages 4–7 audit it.

---

## 4. The IPVV as the working model (the proving loop)

For the IPVV specifically, the loop is:
1. **Cluster** the 63 C1s → communities
2. **Themes** → accepted (e.g. Memory-and-Recognition, Order-less-Support, Causality-as-Agency)
3. For each theme, **construct an argument** (premises from member C1s, gate via Nyāya)
4. **Packet** it (derived strength + resolve-able premises)
5. **Essay** it (provenance-carrying)
6. **Pit it** against the Tantrāloka's packet on the same question → a comparative essay

**Acceptance test (the `truthreview` standard):** the essay must be *derived from the argument graph*,
not copied from prose. If a human wrote it independently, the pipeline failed.

---

## 5. What to build, in order (the queue)

| # | Stage | Build | Depends on | Effort |
|---|---|---|---|---|
| **1** | Cluster | scale the pilot to all 63 C1s (community detection) | C1s (done) | medium |
| **2** | Themes | accept themes editorially from clusters | #1 | low (editorial) |
| **3** | **ArgumentTruthPacket type + parser** | type the argument from themes/C1s + the 3 existing LOGICAL-ARGUMENT files | #2 | low |
| **4** | Nyāya gate → `/verify/claim-semantic` | port the truth-engine gate as the semantic verify | #3 | low-medium |
| **5** | Derived strength scorer | port the Bayesian propagation as the scorer | #3 | low (code exists) |
| **6** | Graph-derived state-of-play | the `truthreview` acceptance test | #3 | medium |
| **7** | Provenance essay generation | GenProve/TRACER pattern | #6 | medium |
| **8** | Comparative matrix + essays | packets pitted across texts | #7 | medium |

**The critical path:** #1 (cluster) is the immediate next stage you identified; #3 (argument packet) is
the unlock that makes everything from #4 onward auditable. They're on the same path — cluster feeds
themes, themes feed arguments, arguments become packets.

---

## 6. The one-sentence version

Take the IPVV (working model): C1 → cluster → themes → arguments → argument packets → essays →
comparative essays, with the **truth engine auditing stages 4–7** (Nyāya gate, derived strength,
graph-derived state-of-play, typed cross-text relations). Build it on the IPVV first, prove it, then
replicate across the tradition — and every essay is a *derived, auditable* projection of the argument
graph, never free-written prose.
