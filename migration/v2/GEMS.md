# PĀṬALA — THE GEMS (the distilled insights per layer, from all the research)

*2026-08-14 · status: THE INSIGHTS · the highest-signal findings across the mixxii review, the external
research (EXTERNAL-REPOS/EXTERNAL-EVIDENCE), the renderr/renderio insight, and the whole migration/v2
package. Each gem: the insight · why it matters · the detailed note. This is the "aha" layer — read when
you want to think, not when you want to execute.*
*Sources: `migration/mixxii` · `migration/v2/renderr.md` · `EXTERNAL-REPOS.md` · `EXTERNAL-EVIDENCE.md` ·
`CURRENT-TO-VISION.md` · the `docs-cache/` research.*

---

## LAYER 00 — GOVERNANCE (the anti-theatre core)

**GEM 0.1 — The doctrine is the moat, and the ecosystem validates it.**
The research found that KG-generation tools (instagraph, kg-gen) all output `MACHINE_PROPOSED` triples —
*candidates*, never canonical truth. Every competitor can extract; almost none can review-and-gate.

> **The value is not extraction. It's the epistemic gate on top of extraction.**

**GEM 0.2 — When the ecosystem converges on your architecture from many directions, lock it.**
Vouch, Beads, Agetor, Gastown all independently orbit the "small typed kernel + organs" model. The
mixxii review reached the same "one graph does many jobs" conclusion. **This is the strongest argument
against churning the design.**

---

## LAYER 01 — INGESTION (harvest)

**GEM 1.1 — fojin proves the harvest is tractable at scale.**
One developer normalized **613 heterogeneous Buddhist sources** into one cross-canon system (10,500+
texts). The gem is the *source-registry pattern* (mine `ARCHITECTURE.md` + `DECISIONS.md`), not pluggable
code. **If one person normalized 613 sources, your harvest of PANDiT/Muktabodha/GRETIL is eminently doable.**

**GEM 1.2 — the PANDiT rule is the model for every harvest.**
License firewall (CC BY-NC-SA → discovery/provenance, never unrestricted commercial) · crosswalk-IDs are
never canonical identity · raw preserved forever · reconciliation produces NEW objects. **Lossless, every
source column retained.** This is exactly how a harvest should work.

---

## LAYER 02 — ATLAS / IDENTITY

**GEM 2.1 — CTS + SARIT are the interoperability targets, not the architecture.**
Adopt CTS citation semantics (passage IDs), not the server stack. SARIT is the TEI export target.
**These are crosswalks outward — Pāṭala's identity stays native, richer.**

**GEM 2.2 — Stencila is the schema-drift answer.**
Canonical YAML schema → compiled TS/Python/Rust/JSON-Schema + C2PA signed provenance. **This is the
mechanism that kills the four-divergent-ReviewEvent problem** — one schema, compiled everywhere.

---

## LAYER 03 — FACTORY / COMPILER

**GEM 3.1 — The projection DAG is the single most important abstraction.**
One graph simultaneously: correctness, staleness propagator, incremental-rebuild scheduler, and part of
retrieval. `hash(inputs + transformation + config)` is the cache key; unchanged → DO NOTHING.

> **Performance and correctness become the same system.**

**GEM 3.2 — Do NOT use Kafka/Airflow/Dagster.**
Pāṭala's DAG is unusually deterministic and domain-specific. A small custom incremental compiler is more
valuable than a generic workflow scheduler. The dependency semantics live in Pāṭala, not Airflow.

---

## LAYER 04 — EVIDENCE / ADAPTERS

**GEM 4.1 — the honest external-tool truth: built ≠ wired.**
Of 69 tools, only vidyut + the ingestion adapters are in production. The bibliography adapters
(crossref/openalex/grobid/opencitations) are **built but imported by 0 production files**. The manifest
overstates reality. **The gem: distinguish BUILT from WIRED — it's the anti-theatre accuracy that matters.**

---

## LAYER 05 — THE SCHOLARLY SPINE (Source → Commentary)

**GEM 5.1 — The three-version translation is the scholarship.**
*"One translation can be wrong in ways that look right. Three translations, composed independently,
cannot be wrong in the same way — where they agree is the hard core; where they differ is the
interpretation-space; the adjudication is the commentary."* **This is the deep value — protect it.**

**GEM 5.2 — Don't go Sanskrit→English directly.**
Translation needs an **intermediate representation** + a **TranslationProof** first-class object, with
no single aggregate score. The ecosystem (MITRA, MQM, Mitrasamgraha) supplies the audit dimensions.

**GEM 5.3 — text-fabric is the L0 substrate model.**
"Stable text-position primitive + annotation layers." **Your Tokenization layer has an external, proven
reference architecture.**

---

## LAYER 05 — TRANSLATIONPROOF (the moat)

**GEM 5.4 — The moat is already grounded externally.**
*"A translation can't be proven equivalent to source, but it CAN be made proof-carrying."* The ecosystem
independently supports it: **MITRA** (1.74M S↔T↔C parallel pairs → cross-source verification, Tibetan/
Chinese as independent witnesses) · **Mitrasamgraha** (391k bitext → the Translation Benchmark + error
families: negation loss, scope loss) · **MQM** (the error taxonomy).

> **You don't need to invent the audit dimensions — they already exist.**

**GEM 5.5 — Separate proof from policy.**
`proof = facts` (the vector) · `policy = requirements` (per surface) · `gate = evaluate(proof, policy)`.
A scholar edition needs adjudication; a public machine translation needs negation PASS + coverage. **The
same proof serves every surface.**

---

## LAYER 06 — ARGUMENT / CRUX (the philosophy engine)

**GEM 6.1 — Own the IR, borrow the engines.**
*"Pāṭala should not reinvent computational argumentation. It should own the historically grounded
philosophical IR that existing engines cannot provide."* ASPIC/AIF/RARR are the *verification*; the IR
is Pāṭala's.

**GEM 6.2 — EleutherIA is the nearest neighbouring vertical.**
~69k passages / 19k KG nodes, CTS IDs, dual-layer graph (primary-source vs modern-reception). **Clone it
and study — it's the closest thing anyone has built to your commentarial layer.**

**GEM 6.3 — Crux is the executable version of "what would change our mind."**
`Crux { proposition, alternatives, decisive_evidence, downstream_arguments, current_status }`. This is
vastly more useful than another literature review — and it's the scholar-acquisition mechanism.

---

## LAYER 06 — REVIEW / ADJUDICATION

**GEM 6.4 — The reducer is the architecture, and Vouch validates it.**
`state + event/evidence → deterministic reducer → next state`. Agents submit *claims about state*, never
state itself. Vouch ("proposal→validation→review→accept, cited evidence, append-only") is the closest
external match — **Pāṭala's `review_engine.py` is the native version, already built.**

**GEM 6.5 — `evidence_ok: bool` is too lossy.**
Use typed events (EvidenceAttached, ContradictionRaised, FindingResolved, AdjudicationRecorded). **The
reducer decides what events imply; agents submit claims, not state.**

---

## LAYER 07 — VERIFICATION (the eval plane)

**GEM 7.1 — The verification ensemble, not one big prompt.**
RARR (retrieve→check→revise) + RefChecker (atomic claim) + GraphCheck (relationship structure) + DSPy
(optimize against Pāṭala gold) + IAM (argument-mining). **Compose them; don't prompt one model.**

**GEM 7.2 — Valsci + literature-review-toolkit prove the Audit product.**
Claim → literature search → support/contradiction report already exists (Valsci); literature-review-
toolkit separates mechanical-verification from agent-judgment. **The Audit product has a proven external
model — it's not speculative.**

---

## LAYER 08 — SCHOLAR ATTESTATION

**GEM 8.1 — The fatal framing is "free AI cleanup for scholars."**
*"Get scholars in early, BEFORE Pāṭala becomes the AI project scholars correct for free."* The scholar
must feel **"leverage, credit, money, data, platform"** — not "someone generated 100,000 lines and wants
me to clean it up."

**GEM 8.2 — Attest to granular objects, not "the project."**
A scholar attests to a specific TranslationRevision / scope / verdict (ACCEPT WITH QUALIFICATIONS). This
creates the **expert verification network** — the real network effect.

---

## LAYER 09 — ORGANISM / HUMAN-UNDERSTANDING GRAPH

**GEM 9.1 — The consumer is the probe.**
User interaction is structured epistemic data, not chat logs. **The consumer-as-probe closes the loop:
questions reveal the missing graph.**

**GEM 9.2 — Graphiti is a projection, not canonical.**
Temporal facts + episode provenance are useful, but extraction can be wrong. **Use it as a compiled
projection from the event ledger, never as canonical user history.**

**GEM 9.3 — The Library is the demand-side organism.**
The renderr insight: *"Pāṭala determines what can responsibly be said. The Library determines what is
worth communicating. Renderio determines how it should be seen."* **Three distinct responsibilities —
don't blur them.**

---

## LAYER 10 — SURFACES / PRODUCTS

**GEM 10.1 — The products are projections, never separate systems.**
One core, five permission-scoped surfaces (Vision 12). Every product is a projection of the same graph +
MCP + review engine. **A product is REAL only when implemented and a user can touch it.**

**GEM 10.2 — Agents need a different projection from humans.**
Humans want narrative + visual hierarchy; agents want minimal tokens + canonical IDs + evidence +
relations. **Compile both from the same object** — and the **Context Bundle** (micro 2k / standard 8k /
deep 32k) is the agent cache line.

**GEM 10.3 — The first-product doctrine: start narrow.**
Translation Audit + IPVV Benchmark + Autonomous Factory. **Start with the narrowest honest product that
creates structured correction data.**

---

## LAYER 11 — ORG / ECONOMICS

**GEM 11.1 — The scarce assets are the moat, not the data.**
`unique source data · rights · provenance · expert judgment · trusted relationships · human corrections`.
The economics pays the scholars whose corrections are the moat. **Build the institution around the
scarce assets, not "we raise money to translate obscure texts."**

**GEM 11.2 — The 84000 lesson.**
Credible leader + credible scholars + mission, seeded by ~108 sponsors ($5M). **Pāṭala's funding path
mirrors this: mission + scholars + institutional seed, not feature-SaaS.**

---

## LAYER 12 — LIVE SYSTEM (orchestration)

**GEM 12.1 — Hermes is the nervous system, not the brain.**
*"Hermes executes. Pāṭala decides."* The deterministic graph/factory is the orchestrator; Hermes is the
general-purpose cognitive executor underneath. **Make Hermes default but replaceable** (a `RuntimeRouter`).

**GEM 12.2 — Task ≠ Run ≠ Event.**
A task's run history is gold (Run 1 failed → Run 2 candidate → Run 3 rejected → Run 4 revised → ReviewEvent
882 accepted). **Agetor validates this** (durable task identity vs reproducible runs pinned to base commit).

**GEM 12.3 — `patala_next_action()` should CALCULATE, not LLM-guess.**
`P(v) = w1·D + w2·B + w3·U + w4·Q + w5·R − w6·C` (downstream, betweenness, uncertainty, question demand,
review deficit, cost). **Beads Viewer supplies the deterministic graph analysis.**

**GEM 12.4 — Compile the read plane.**
`HTTP → CDN → bytes` instead of `HTTP → app → reasoning graph → DB → reconstruction`. **The normal read
path should be static bytes on R2/CDN, not a request-time graph query.**

---

## THE MEDIA / RENDER LAYER (from `renderr.md`) — the video frontier

**GEM R.1 — Renderio is not a renderer.**
It's the catalogue, style system, process, derivation contract and review loop *above* the actual
renderers. **Make the next SCENE-PACK renderer-independent** — the scene describes what to communicate,
not which model renders it.

**GEM R.2 — The 2026 video frontier (the practical picks).**
- **LTX-2.x** — best for controlled hero shots (but 32GB+ VRAM; don't make it Renderio)
- **HunyuanVideo 1.5** — the practical open workhorse (benchmark this against LTX)
- **Wan 2.2** — cheap generic inserts
- **OmniWeaving** — the exciting research frontier (closest to what Renderio does)

**GEM R.3 — Generative video should be only 10–25% of a film.**
Evidence → Explanation → Atmosphere → Hero imagery (in that order). **The deterministic render layer
(typography, diagrams, manuscript assets) is the base; generative video is the accent.**

**GEM R.4 — Deterministic renderers: Motion Canvas, Revideo, Remotion.**
Create adapters for all three; **don't rewrite Renderio around any one of them.** The composition is the
moat, not the renderer.

---

## THE CROSS-CUTTING GEMS (the ones that matter most)

**GEM X.1 — "Pāṭala decides. Hermes executes. Renderio shows."** Three clean responsibilities.

**GEM X.2 — Everything Pāṭala needs the *machinery* for already exists.**
Kraken (OCR), eScriptorium (OCR UI), SARIT (TEI), CTS (IDs), Vidyut (mechanics), RO-Crate (packaging),
Stencila (schema), FSRS (scheduler), pyBKT (learner). **The moat is the epistemic gate on top — build the
kernel + the gate + the proof, strip-mine the rest.**

**GEM X.3 — The anti-theatre rule cuts both ways.**
Don't present visionary as implemented (the honest finding: 33/43 routes read `.ts`, 0 hit Postgres;
L200=5 vs 63 golds). **But also don't build work that produces no observable result** — the gold-ingest
matters only if it reaches the read plane.

---

*These are the insights distilled from all the research. They converge on one architecture: a small typed
kernel + the epistemic gate + the proof, with everything else strip-mined from the ecosystem. The gems
are the "why" that grounds the build order in CURRENT-TO-VISION.md.*
