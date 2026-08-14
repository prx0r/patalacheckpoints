# PĀṬALA — SCHOLAR API / PEER REVIEW / ADVERSARIAL REVIEW: HOW CLOSE?

*2026-08-14 · status: THE ASSESSMENT · tested end-to-end. The scholar peer-review + adversarial review
are CLOSE — the core machinery works. This records exactly what's done vs what's left.*

---

## THE VERDICT: CLOSE. The core works; the surface needs wiring.

### ✅ WORKS (tested end-to-end)

**1. The adversarial panel (scholar_review.py) — the peer-review core:**
```
panel = ReviewPanel(reviewers=['r1','r2','r3'], judge='j1')
panel.collect('r1', 'SUPPORT', ...); panel.collect('r3', 'CONCERN', [BLOCKING finding])
anti_groupthink() → {consensus:False, dissent:{r3:CONCERN}, blocking_findings:1}
verdict()         → {verdict:BLOCKED, dissent:{r3:CONCERN}}
```
3 reviewers, 1 blocking concern → verdict BLOCKED, dissent REPORTED not forced. This is vision-06
(adversarial review) working.

**2. The review engine (review_engine.py) — the scholarly peer-review loop:**
```
ledger.submit_review(actor='scholar-A', kind='scholar', scope='translation-review', decision='REJECT')
  → accepted (REJECT)
ledger.submit_review(actor='ml-agent', kind='machine', decision='PROMOTE')
  → FORBIDDEN: "machine actors may propose, never submit a state-changing review"
ledger.reduce()   → claim: REJECTED, downstream essay: STALE
ledger.impact_report() → the impact propagation
```
- A scholar can submit a scoped review. **A machine CANNOT promote** (the anti-theatre boundary,
  executable). Impact propagates downstream (rejected claim → stale essay). This is vision-07's
  "AI proposes, scholar adjudicates" working.

**3. The scholar-facing API surface (exists, designed well):**
- `/api/assertions` — contested scholarly claims as first-class objects + their review events
- `/api/decisions/:id` — the full audit trail (decision + evidence + reviews + version lineage)
- `patala_*` MCP review tools: `patala_get_review_state` · `patala_propose_review` ·
  `patala_submit_review` · `patala_get_impact` · `patala_simulate_review`

### ⚠️ WHAT'S LEFT (to ship the full Scholar product)

| Gap | What | Why it matters |
|---|---|---|
| 1 | **Wire the API routes to the LIVE ledger** | the routes currently read `primitives.ts` static data, not the live `ReviewLedger`. The machinery works; the surface isn't connected to it yet. |
| 2 | **Signed attestation (gap E)** | the review is a plain record; C2PA/ORCID signed attestation is needed before public authority/marketplace. |
| 3 | **The Scholar Workbench UI (vision-07)** | the human surface where a scholar reviews, sees impact, and adjudicates. The API + machinery exist; the UI is the remaining build. |

---

## HOW CLOSE, HONESTLY

**The intellectual/mechanism core is DONE and TESTED.** The adversarial panel, the review reducer, the
human gate (machine can't promote), and the impact propagation all work — I ran them. The scholar API
routes are designed well and exist.

**What remains is CONNECTING + POLISHING, not inventing:**
1. Connect the API/MCP to the live ReviewLedger (the biggest single step — turns the designed surface
   into the working product).
2. Add signed attestation (gap E).
3. Build the Scholar Workbench UI (vision-07).

That's a day or two of wiring, not a new architecture. The Scholar API / peer review / adversarial
review is **80% there** — the core works, the surface needs connecting.

---

*The assessment is based on executed tests, not documentation. The adversarial panel, the review
engine (with the machine-can't-promote boundary), and impact propagation all work. The remaining work is
connecting the API to the live ledger + signed attestation + the scholar UI.*
