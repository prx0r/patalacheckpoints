# PĀṬALA PRODUCT PORTFOLIO — aligned by user base (the cohesive product map)

*2026-08-12. The consolidation that aligns every vision doc to a concrete **user base / product surface**.
Reads the whole vision (Vision 01–12 + the endgames + the lens folders) and organizes it as **who buys/uses
what**, completing Vision 12 (Multi-Surface Platform). For each surface: the products, the vision docs they
come from, and the concrete feature. This is the product catalog — the "what do we actually build for whom".*
**This is the CURRENT PRODUCT DOCTRINE for Pāṭala.** The most important distinction: **substrate readiness
(the 63/63 floor) vs semantic capability readiness (what is actually measured)**. Never overstate what the
floor proves.

---

## THE ALIGNMENT (every vision → a surface)

| Surface | User | Products | Sources |
|---|---|---|---|
| **CONSUMER** | learners, practitioners, general readers | Tantra Hub · reader · atlas graph · learning/courses · media (shorts/video/AI-teacher) | V01/02, V09, `education/LEARNING_STRATEGY.md`, `education/EDUCATION_VISION.md`, `education/PATALA-EDUCATION-SYNTHESIS.md` |
| **SCHOLAR** | Sanskritists, philosophers, digital-humanities researchers | **Pāṭala Review** · Scholar Workbench · research compiler · translation QA · benchmark/rating | V06, V07, V08 |
| **CONTRIBUTOR** | manuscript holders, editors, translators | acquisition pipeline · manuscript upload · translation memory · critical editions | V11, `endgame1.md` |
| **DEVELOPER** | external agents, researchers building tools | Pāṭala API · MCP (`mcp.patala.org`) · OAuth · BYOA · executable-corrections protocol | V12, `apideas.md`, `hermes-execution.md` |
| **REVIEWER** | editorial board, specialist adjudicators | review queue · adjudication · promotion policy · review credit (ORCID/Crossref) | V06, V08, `PEER-REVIEW.md` |

**The rule (Vision 12):** one scholarly core, five permission-scoped surfaces. The products below are
projections of the SAME graph + MCP + review engine.

---

## SCHOLAR-FACING PRODUCTS (the full catalog — including new brainstorm)

These are the scholar products, grouped by the job they do for a scholar.

### A. Translation quality (the biggest new opportunity — rating, correcting, benchmarking)
The scholar's #1 pain is translation uncertainty. Pāṭala can offer, all on top of the 63/63 L0 floor:

1. **Translation Rating / Audit** — a scholar pastes their translation of a Sanskrit span; Pāṭala returns a
   structured assessment: source-integrity PASS/FAIL, morphology analyses, alignment (which English maps to
   which Sanskrit), term-policy consistency, parallels, external readings, and **flags** (omission,
   overtranslation, polarity shift, referent issue, term-sense drift). *This is Vision 06 §1, now
   operational via `verify_l0` + `l0_align` + the review engine.*
   **Make it an AUDIT, not a single score** — a "74/100 translation" would undermine the epistemic philosophy.
   **Honest capability tiers:**
   ```
   Audit v0  deterministic checks only — source coverage, omissions, alignment bookkeeping,
             terminology consistency.  (product plumbing ✅ + source auditing ✅ — available now)
   Audit v1  model-proposed interpretive flags (rival readings, scope, referent) — PROPOSED, not asserted
   Audit v2  calibrated against PĀṬALA-IPVV expert gold   (semantic translation judgment — NOT YET ESTABLISHED)
   ```
   **Do NOT claim sophisticated semantic correctness until benchmarked** — the alignment baseline has not yet
   demonstrated robust semantic judgment. Audit v0 (deterministic) is real; semantic correctness waits for v2.
2. **Adversarial Translation Review** — "attack this reading." Pāṭala generates the strongest rival parse
   and returns objections (referent, term-sense, scope). *Vision 06 §2 — the `/adversarial-translation-review` product.*
3. **Translation Comparison** — same Sanskrit, translations A/B/C → agreement/divergence + why it matters
   (`/compare-readings`). *Vision 06 §10.*
4. **Term Audit** — "audit my use of *śakti* across this translation" → 63 occurrences, rendering
   distribution, unexplained drift. *Vision 06 §11.*
5. **A Sanskrit translation BENCHMARK — PĀṬALA-IPVV** — the strongest strategic asset in the catalog.
   A curated set of difficult passages with expert gold. **Not BLEU-style** — it tests the hard dimensions
   generic benchmarks barely touch:
   ```
   segmentation · speaker attribution · omission/addition · negation/polarity · term sense
   syntactic attachment · translation choice · proposition recovery · ambiguity handling
   ```
   This **rates** a scholar's translation against gold AND **measures AI competence** in Sanskrit philosophy.
   It is a defensible dataset (not just an app feature), useful to scholars AND AI labs, gets better with
   expert corrections, and can be cited independently of Pāṭala. *From `visionai`/`historicalsiva` + the
   manifest — makes Pāṭala the place where Sanskrit-AI competence is measured.*

### B. Pāṭala Review (Vision 06 — the mega-product; the compiler is its engine)
6. **Pāṭala Review** — a scholar uploads a draft article/chapter/thesis → machine pre-review →
   claim extraction → citation resolution → argument graph → source-grounding audit → Reviewer-2 attack →
   impact/crux analysis. Returns "17 claims, 11 grounded, 2 unsupported, 1 load-bearing issue." Every
   criticism resolves to corpus objects. **Modes** (one product, not many): Translation · Argument ·
   Paper · Thesis · Terminology · Corpus.
   *(The Research Compiler is the UNDERLYING ENGINE — parse → type-check → source-check → dependency-check →
   warnings/errors → an AUDITABLE RESEARCH OBJECT — not a separate headline product. Merge them.)*
7. **Thesis stress test** — "in early Krama, kālī primarily functions as X" → supporting/qualifying/
   counterexample passages + chronological/scope problems (`/stress-test-thesis`). *Vision 06 §8.*
8. **Impact analysis** — "what depends on this reading?" → the executable-corrections ImpactReport
   (already built in Phase 3A/3D). *Vision 06 §13.*
   *(The "Philological Proof Certificate" is an OUTPUT/ARTIFACT of Translation Audit + Review, not a
   standalone product.)*

### C. The Scholar Workbench (Vision 07 — structured inquiry)
9. **Explore mode** — the scholar works in the research graph: test alternatives, map arguments, collect
   tensions, build themes, stress-test a thesis. The essay is one output.
10. **The review screen** (Phase 3E, minimal) — object · evidence · current state · proposal/review
    controls · impact preview · submit. The entry point to the executable-corrections loop.
11. **The AI research copilot** — a constrained profile that queries the MCP, compares readings, launches
    blind critics, constructs alternatives — but cannot accept/promote.

### D. Scholar economics (Vision 08 — makes it sustainable)
12. **Scholarly bounties** — tightly scoped, paid adjudication (not "review our corpus for free").
13. **Durable credit** — ORCID/CRediT/DOI: "I reviewed 63 Pratyabhijñā propositions for Pāṭala" becomes a
    citable scholarly service.
14. **Microgrants / commissions** — for neglected texts (Kubjikā microgrant, early-career fellowship).

---

## THE PRODUCT RANKING & SEQUENCE (what to actually prioritize)

Not all ideas are equal. The ranked build order, by strategic value:

```
1.  AGENT 3 FACTORY               (the autonomous-translation headline — the current priority)
2.  PĀṬALA-IPVV BENCHMARK          (the standout strategic asset: product + moat + research credibility
                                    + AI relevance + scholar network all at once)
3.  TRANSLATION AUDIT / RATING     (the best FIRST scholar product — clear job-to-be-done, low learning
                                    curve, exposes everything already built)
4.  TRANSLATION COMPARISON + TERM AUDIT   (immediately useful; comparison does what manual scholarship
                                    takes hours to do)
5.  PĀṬALA REVIEW                  (the largest eventual product — the destination of Agent 1)
6.  SCHOLAR WORKBENCH              (live inside the verification system)
```

**The product cluster (the natural progression):**
```
TRANSLATION AUDIT ──┬── compare readings ──┬── adversarial review ──┬── term audit
                    └── proof / provenance ┘
        ↓
PĀṬALA-IPVV BENCHMARK
        ↓
PĀṬALA REVIEW
        ↓
SCHOLAR WORKBENCH
```
Each step increases user commitment: paste one translation → compare a passage → benchmark a system/person
→ upload a paper → live inside the workbench. Much better than launching a giant scholarly operating system.

**THE BENCHMARK IS THE STRATEGIC CENTRE — a data flywheel:**
```
Agent 3 factory
      ↓
benchmark gold expansion  ⇄  Translation Audit
```
Every expert review of Audit output adds benchmark data; every benchmark improvement improves the Audit;
every model evaluation generates failure cases. This is harder to copy than the UI.


---

## CONSUMER-FACING PRODUCTS (educational — the current site)

17. **Tantra Hub / Reader** (V02) — bibliography, reader, translation-workshop, commentary, media.
18. **The atlas graph** — the traditions/texts/concepts rendered as a navigable graph (the current homepage).
19. **Learning / courses** (V09 + `education/LEARNING_STRATEGY.md`) — knowledge packets → quizzes/courses; the
    graph-native teaching engine (`education/EDUCATION_VISION.md`). The most complete statement is the
    `education/PATALA-EDUCATION-SYNTHESIS.md` (imported from R2).
20. **Media layer** (V09) — the scholarly core rendered as shorts/video/essays/AI-teacher, reproduced
    across traditions (Tantra → Yogic → Vedānta → Greek).

---

## DEVELOPER-FACING (already real — the protocol surface)

21. **Pāṭala API** (34 routes) — stable primitives.
22. **Pāṭala MCP** (21 tools + 5 review tools) — `mcp.patala.org`, OAuth scopes, BYOA.
23. **The executable-corrections protocol** — machine→propose, authorized-scholar→review, Pāṭala→compute.
    The start of "Pāṭala as a scholarly protocol rather than a repo."

---

## CONTRIBUTOR-FACING (V11 — the corpus growth surface)

24. **Manuscript upload / acquisition** — upload a scan/transcription → metadata/rights → Agent 2's corpus
    inventory → the translation factory.
25. **Critical editions** — fork a reading → Pāṭala calculates dependencies, term-policy changes, proof
    obligations ("GitHub PRs for philology"). *Vision 06 §17.*

---

## REVIEWER-FACING (A4 — the adjudication surface)

26. **The review queue** — graph-aware ranking of objects needing judgment (impact/uncertainty/centrality).
27. **Adjudication + promotion policy** — the strongest boundary; only editors/adjudicators promote.
28. **Review credit** — Crossref `isReviewOf` + ORCID reviewer credit (the interop stack).

---

## THE PRODUCT-LED BUILD SEQUENCE (relative to the autonomous-translation priority)

**The two-part wedge (the strongest opportunity):**
> **Pāṭala becomes the authority that measures whether humans and machines actually understand and translate
> difficult Sanskrit philosophy. Benchmark = authority. Translation Audit = product.**

```
Phase A   PĀṬALA-IPVV v0.1 — the standard. Start with the first ~100 genuinely vicious cases (worth far
          more than 10,000 easy verses). Each fixture = expert-reviewed dimensions, not one "correct English."
Phase B   Audit a Translation — the wedge. One box for Sanskrit, one for translation, one button. Everything
          built becomes invisible machinery behind that interaction.
Phase C   three tabs: SOURCE FIDELITY · ATTACK THIS READING · TERM AUDIT · COMPARE READINGS. One product, not four.
Phase D   leaderboard — run major models on the hard set; publish "State of AI Sanskrit — 2026".
          Benchmark against/alongside Mitrasamgraha, IndicGenBench, IndicParam (don't pretend Pāṭala invented
          Sanskrit evaluation — the differentiator is classical philosophy + expert interpretive adjudication + provenance).
Phase E   private eval set — do NOT publish every question. Public set = legitimacy + leaderboard; private
          held-out set = anti-contamination + serious model evaluation.
```

**The sequence (sharpened):**
```
NOW (built)     L0 floor 63/63 · corpus state · review engine (3A+3D) · MCP (21+5) · API
NEXT (priority) Agent 3 translation factory → produces the machine-proposed drafts
THEN            PĀṬALA benchmark v0.1 (the strategic asset)  +  Translation Audit (the user wedge)
                with Adversarial Review + Term Audit INSIDE the Audit (not separate apps)
THEN            leaderboard ("State of AI Sanskrit") + private eval set
LATER           Pāṭala Review mega-product, Workbench, media, contributor, reviewer surfaces
```

**The logic:** the translation factory produces the raw machine-proposed material; the **benchmark** is the
strategic asset (product + moat + research credibility + AI relevance + scholar network), and **Translation
Audit** is the best first scholar product (clear job-to-be-done: "tell me what's wrong with my translation").
Adversarial Review + Term Audit are **modes inside the Audit**, not separate apps. Every Audit interaction
generates reviewed evaluation data that feeds the benchmark.

**The honest capability caveat:** Translation Audit v0 can reliably do *deterministic* things (source
coverage, omissions, alignment bookkeeping, terminology consistency) — the product plumbing + source auditing
exist. But **sophisticated semantic translation judgment is NOT YET ESTABLISHED** (the alignment baseline has
not demonstrated robust semantic correctness). Audit v1 = model-proposed interpretive flags (PROPOSED, not
asserted); Audit v2 = calibrated against expert gold. Do not claim semantic correctness until benchmarked.

---

## THE STRATEGIC RANKING (not all products are equal)

| Rank | Product | Demand | Moat | Revenue | Build now? |
|---|---|---|---|---|---|
| 1 | **PĀṬALA benchmark / eval suite** | 7 | **10** | 9 | **YES** |
| 2 | **Translation Audit / Rating** | **9** | 9 | 8 | **YES** |
| 3 | **Adversarial Translation Review** | 8 | **9** | 8 | **YES, inside Audit** |
| 4 | **Term Audit** | 8 | 9 | 7 | **YES, inside Audit** |
| 5 | Philological Proof Certificate | 6 | **10** | 8 B2B | Soon |
| 6 | Translation Comparison | 8 | 5 | 5 | Feature, not product |
| 7 | Pāṭala Review / research compiler | 7 | 9 | **9 eventually** | Later |
| 8 | Thesis Stress Test | 7 | 7 | 6 | Later |
| 9 | Scholar Workbench | 6 | **10 eventually** | 8 | Much later |
| 10 | Bounties + ORCID/CRediT | 4 | **10 network** | 5 | Ecosystem layer |

**The Benchmark is the most strategically valuable asset. Translation Audit is the best first product.**

### Why "we benchmark Sanskrit" is NOT the moat (2026 market)
Mitrasamgraha (391,548 Skt–EN bitext pairs), Google's IndicGenBench (Sanskrit among 29 Indic languages), and
BharatGen's IndicParam (Sanskrit among low-resource languages) all already benchmark Sanskrit translation.
**The moat is NOT another BLEU score.** Nobody owns **expert-adjudicated evaluation of difficult premodern
Sanskrit philosophy where correctness requires philology + philosophical interpretation + attribution + scope
+ terminology + argument structure.** That is radically more interesting — closer to "Humanity's Last Exam for
Sanskrit philosophy."

### The eval suite dimensions
```
Sanskrit Philosophy Evaluation Suite

A. TEXTUAL        segmentation · sandhi/morphology · compound analysis · syntactic attachment
B. TRANSLATIONAL  omission · addition · negation · modality · agency · technical-term handling · semantic alignment
C. PHILOSOPHICAL  speaker attribution · pūrvapakṣa vs siddhānta · reconstructed proposition
                  · explicit vs implicit premise · scope preservation · conceptual distinction
D. ARGUMENTATIVE  premise recovery · conclusion recovery · inference reconstruction
                  · objection/reply · defeater recognition
E. SCHOLARLY      rival-reading recognition · evidential justification · uncertainty/abstention · source traceability
```

### The three markets (not one)
- **Market A — Sanskrit scholars/students:** use Translation Audit to produce better translations.
- **Market B — institutions** (universities, publishers, archives, textual projects): Translation Audit +
  Proof Certificates + reviewer workflows. Defensible because "machine proposes → evidence exposed → human
  adjudicates → decision recorded" beats "GPT says 8/10."
- **Market C — AI labs / India AI ecosystem (potentially the highest value):** the Pāṭala Eval API — a model →
  private challenge set → expert rubric → dimension scores → error analysis. Tells a lab *where its system
  actually fails* (morphology 91, syntax 84, translation 78, scope 69, attribution 63, argument 48, rival
  readings 31).

### The Gyan Bharatam timing tailwind (India, through 2031)
The mission targets 1cr+ manuscripts, a national repository, AI-assisted transcription, provenance infra and
APIs, with Indology/philology experts in leadership. Positioning: not "Pāṭala translates Tantra" but
**"Pāṭala provides the expert evaluation and provenance infrastructure required to determine whether AI
systems can reliably operate on India's classical knowledge traditions."**

### What to downgrade
- **Translation Comparison** — build it, but it's a feature (LLMs already compare well; the moat is Pāṭala's
  evidence underneath).
- **Thesis Stress Test** — competitive (Elicit, Paperpal); Pāṭala's version must be the deep dependency-aware
  kind ("your claim depends on reading X, which conflicts with Z; removing premise P collapses sections 3 and 5").
- **Scholar Workbench** — the moat, not the wedge. Scholars don't wake up wanting an IR workbench; they want
  "is this translation right?" The interactions *become* the workbench.

### The benchmark + Audit flywheel (the accidental moat)
```
                 PĀṬALA BENCHMARK  ← hard reviewed cases ← scholar judgments ← TRANSLATION AUDIT
                 (term audit / attack / comparison) → corrections/decisions → evidence graph
                 → stronger benchmark → better evaluator → better Translation Audit
```
The consumer-facing interaction **manufactures the benchmark moat**.

### Naming: Pāṭala Classical Sanskrit Evals (not PĀṬALA-IPVV)
IPVV is suite #1, not the ceiling:
```
Pāṭala Classical Sanskrit Evals
  IPVV-Translate · IPVV-Philology · IPVV-Argument · IPVV-Terms
  later: Nyāya-Reason · Mīmāṃsā-Reason · Buddhist-Pramāṇa · Vedānta · Tantra · Kāvya
```

### The moat formula gains evaluation authority
```
Previously:   M = D × P × V × N × A
Now:          M = D × P × V × N × A × E
where E = the degree to which the outside world accepts Pāṭala as the standard for "good."
```
If a lab says "our Sanskrit model improved 47 → 63 on Pāṭala," if a translator says "this received Pāṭala
Verified," if a project says "machine translations must pass Pāṭala's attribution + source-fidelity checks" —
Pāṭala owns part of the **measurement layer**, far harder to displace than a corpus.

---

## THE THREE KINDS OF CHECKS (keep them separated — critical for Translation Audit)

Inside Translation Audit there are three distinct check classes. Never conflate them:

**1. Deterministic checks — available earliest (strong statements allowed, mechanically verifiable):**
```
source coverage · span resolution · missing material · extra-material candidates · token/segment alignment
term consistency · citation resolution · provenance completeness
```

**2. Model-proposed scholarly checks — MUST remain MACHINE_PROPOSED until reviewed:**
```
possible scope shift · possible mistranslation · possible wrong attachment
possible pūrvapakṣa attribution error · possible term-sense mismatch · possible rival parse
```

**3. Calibrated judgments — possible only once PĀṬALA-IPVV has enough reviewed gold:**
```
"On held-out expert-reviewed cases, this detector identifies polarity errors at X precision / Y recall."
```
That is when Translation Audit becomes substantially different from "an LLM commenting on your translation."

**Roadmap (exactly right):** Audit v0 = deterministic · Audit v1 = proposed interpretation · Audit v2 =
benchmark-calibrated. The benchmark answers the product's uncomfortable question — *"why should I trust
Pāṭala's criticism?"* — not with "because our model is good" but with **"because this specific class of
check has been evaluated blind against independently reviewed Sanskrit-philosophy cases, and here is the
evidence."** That changes the product from AI advice to **measured scholarly tooling**.

---

## THE BENCHMARK AS THE EVALUATION SUBSTRATE FOR THE WHOLE ENGINE (not just translation)

Design PĀṬALA-IPVV so it becomes the evaluation substrate for the whole philosophy engine, not "translation
gold." It mirrors the evidence graph (Sanskrit → translation → interpretation → argument) and measures where
a model stops being reliable:
```
PĀṬALA-IPVV
├── T1 SOURCE        segmentation · morphology · syntax · alignment
├── T2 TRANSLATION   omission · unsupported addition · polarity · modality · agency · terminology
├── T3 INTERPRETATION speaker attribution · scope · rival reading · conceptual distinction · abstention
└── T4 ARGUMENT      proposition extraction · commitment · inference recovery · support/attack
                     · semantic alignment · crux
```
**One increasingly deep benchmark family** — no separate unrelated benchmarks for the philosophy engine later.

---

## THE REDUCED SCHOLAR CATALOG (one surface per job, modes/engines underneath)

Resist turning every useful interaction into a separate product. The catalog collapses to four surfaces:
```
PĀṬALA AUDIT        translation · comparison · terminology      (comparison + term = surfaces built from
                                                               Audit primitives, not separate cores)
PĀṬALA REVIEW       argument · paper · thesis                  (the compiler is the engine, not a product)
PĀṬALA WORKBENCH    research creation                          (the moat, not the wedge)
PĀṬALA BENCHMARKS   evaluation / certification                 (the strategic asset)
```
Everything else (proof certificate, thesis stress test, impact analysis) is a mode, artifact, or underlying
engine. **Translation Comparison** = two+ TranslationAudit objects + semantic diff + interpretive-consequence
analysis (a surface). **Term Audit** = all aligned occurrences + sense evidence + translation choices +
consistency analysis (a surface).

---

## THE TRUE FLYWHEEL (the most valuable loop in the project)

Not "more texts → more users → more texts." The real flywheel:
```
hard scholarly case → machine attempts → expert adjudication → structured correction
→ benchmark fixture → evaluation → better system → harder scholarly cases
```
This creates something increasingly scarce: **a growing record of where intelligent systems fail on
historically situated reasoning, together with expert judgments explaining why** — far more valuable than a
corpus of translations alone.

---

## THE FINAL BUILD ORDER (with the coupled-program nuance)

```
1. Factory
2. PĀṬALA benchmark      ┐
3. Translation Audit     ┘  ← develop #2 and #3 as ONE COUPLED PROGRAM
4. Comparison + Term Audit
5. Pāṭala Review
6. Workbench
```
The benchmark without the product risks becoming an academic dataset; the product without the benchmark
risks becoming generic AI criticism. **Together they are the wedge and the moat.**

---

## THE ONE-SENTENCE CARRY-FORWARD

**Pāṭala's products align to five user bases (consumer/scholar/contributor/developer/reviewer) as
permission-scoped projections of one scholarly core; the strategic centre is the two-part wedge —
**the Pāṭala benchmark = authority** (expert-adjudicated evaluation of difficult premodern Sanskrit
philosophy: textual, translational, philosophical, argumentative, scholarly — NOT another BLEU score) and
**Translation Audit = product** (the wedge that gets in front of scholars, with Adversarial Review + Term
Audit inside it, and every interaction manufacturing the benchmark moat). After the Agent 3 factory, build
the benchmark (the strategic asset) + Translation Audit (the user wedge), benchmark against the existing
Sanskrit-eval ecosystem rather than ignoring it, and hold the honest capability line: deterministic audit
is available now, semantic judgment only once calibrated against expert gold. This is the first Pāṭala
direction where product, research program, benchmark, scholar network, AI strategy and moat all point at
the same thing — evaluation authority (the moat formula becomes M = D×P×V×N×A×E).**
