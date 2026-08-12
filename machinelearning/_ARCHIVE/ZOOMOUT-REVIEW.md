# ZOOM-OUT REVIEW — what we wanted vs. what we built (and what it means)

*2026-08-12. An honest, evidence-based review of the whole ML lane: what the strategy promised, what is
actually built, where we over-delivered, where we are off-target, and what the next real milestone is.
The discipline: judge against what we WANTED, not against an impressive-sounding pile of code.*

---

## 1. What we wanted (the promises)

From the frozen strategy + the vision + the external review:
1. **A provenance-preserving scholarly derivation spine** — Sanskrit → commentary → argument → essay,
   every claim resolving to source, no "AI proposes ≠ Pāṭala asserts" violations.
2. **The cross-layer gold chain** — ONE end-to-end artifact, lower-layer proof status propagated, NOT
   collapsed to a number.
3. **The two agents converge** — ML (interpretation) bottoms out in L0 (philology), not "C1 says X."
4. **Compare alternative systems** — don't trust one builder; measure several, validate the metrics.
5. **Make it "for any text"** — reproducible contracts, IPVV as the gold standard.

---

## 2. What we built (the reality, verified)

| # | Promise | Status | Evidence |
|---|---|---|---|
| 1 | provenance spine | **BUILT** | Claim-v3 ArgumentProposal (resolvable, gated), AIF graph, EssayPlan, all pointing to passages |
| 2 | cross-layer gold chain | **BUILT (CL-3)** | `goldchain-cl3.json`: 28 nodes, 10 layers, per-dimension certificate |
| 3 | two agents converge | **BUILT** | the `philological_proof` handshake (`pp:ipvv:v2o:p4`) — ML references L0 proof IDs |
| 4 | compare systems | **BUILT + RESULT** | B-STRUCT wins gt-overlap; **coverage is a real metric (Spearman +0.94), resolvability/diversity are noise** |
| 5 | for any text | **PARTIAL** | schemas defined, `contracts/` not yet consolidated, second work not tested |

**Test state: 124/124 passing** (argument 29, cluster 14, essayplan 17, goldchain 40, strength 24).

---

## 3. Where we genuinely over-delivered

1. **The gold-chain design rule is real, not aspirational.** The certificate propagates `LEXICAL_SENSE:
   OPEN` for V2-O's 134 ambiguous L0 tokens — it does NOT hide it or collapse it into "confidence 0.87."
   This is the external review's core requirement, met with real data. This is the strongest piece.

2. **The metric-validation experiment worked and gave a non-obvious answer.** We didn't just build
   alternative builders — we *proved* `coverage` is the metric that tracks ground-truth quality
   (Spearman +0.94) while `resolvability`/`diversity` are noise. That's exactly the "which metrics are
   bs" validation the user wanted, and it's a genuine result.

3. **The agent-convergence handshake is clean.** `philproof.py` defines a contract the ML lane consumes
   (by proof ID) without needing the L0 agent done. Concurrent work is now possible — the two spines
   join on passage IDs, not on trust.

---

## 4. Where we are OFF-TARGET (the honest gaps)

1. **Nothing is editorially ACCEPTED.** Every artifact is `MACHINE_PROPOSED` / `EDITOR_APPROVED` *in
   code* — but no human has actually accepted a theme or an argument. The reviewer's warning is real:
   the gold chain currently demonstrates *automation*, not *scholarship*, because CL-3 is still a
   machine proposal, not an accepted theme. **This is the biggest gap.**

2. **The essay prose doesn't exist yet.** We built the EssayPlan (the decision object) but not the
   actual essay sentences with sentence-level provenance. The "crown" (click a sentence → its claim →
   argument → passage → proof) is designed and the chain supports it, but it's not rendered.

3. **The two theme systems are still separate.** `themes.ts` (Agent 2, lemma-topics) and `clusters.json`
   (mine, graph-communities) are not unified. The reviewer said "don't unify yet" — correct — but it's
   still an outstanding debt.

4. **"For any text" is unproven.** The schemas generalize in principle, but `contracts/` isn't
   consolidated and no second work (Tantrāloka) has been run through. The IPVV proves the *spine*; it
   doesn't yet prove *transfer*.

5. **The `WHAT_NEXT_PATALA.md`, `CONTEXT_ENGINEERING.md`, `geometric.md`, `SYSTEM_GROWTH_AND_HERMES.md`
   docs exist but are not part of the verified build** — they're vision/other-agent, not tied to the
   124 passing tests. (Fine as vision; not evidence of a built capability.)

---

## 5. The honest assessment (against what we wanted)

**We built the SPINE correctly, but we have not yet proven the LOOP with a human in it.**

- The machinery (argument → AIF → plan → certificate) is real, tested, auditable, and aligned.
- The **missing human adjudication** is the thing that turns "demonstrates automation" into
  "demonstrates scholarship." This is the reviewer's exact point and it's where we must go next.
- The **metric-validation** gave us a genuine, non-obvious result (coverage is real; the others are bs).
- The **cross-layer handshake** is the architectural win that makes the two agents converge.

So: **delivered on the hard architecture, deferred the human step and the essay render.** Both are
required to complete the milestone, and neither is a code problem — CL-3 needs a human to say "yes, this
theme and argument are what the IPVV actually argues."

---

## 6. What the next real milestone is (and it's NOT more code)

**Adjudicate CL-3 into an accepted theme + accepted argument, then render the essay.**

The gold chain is the substrate. The milestone is:
1. A human reviews CL-3's theme + argument and ACCEPTS (or modifies) it — turning `MACHINE_PROPOSED`
   into `editorially_accepted` with a real review event.
2. Generate atomic essay claims (EVIDENCED/SYNTHETIC + support + boundary), each verified.
3. Render the essay with sentence-level provenance (the click-to-evidence crown).

This makes the gold chain a *scholarly* artifact, not an automated one. Everything after
(adjudicate 8 more themes, unify, contract, second work) follows the reviewer's order.

---

## 7. Bottom line (the zoom-out)

**We built the right spine and proved it works mechanically.** The 124-test suite, the gold-chain
certificate with honest OPEN propagation, and the metric-validation result (coverage real, resolvability
bs) are genuine, non-hallucinated deliverables that match the strategy's intent.

**But the milestone isn't complete** until a human accepts CL-3 and the essay is rendered from its
claims. That is the difference between "we have a working provenance pipeline" and "we have the
computable scholarly tradition the vision describes." The next step is not another module — it's the
**editorial acceptance of CL-3** (the human-in-the-loop step), then the essay render on top of the
proven chain.
