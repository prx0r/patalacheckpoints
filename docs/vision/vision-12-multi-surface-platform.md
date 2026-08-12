# Vision 12 — The Multi-Surface Platform: one scholarly core, many role-based surfaces

*2026-08-12. The product-architecture vision: **not two separate sites, but one scholarly core (the
epistemic graph + MCP/API + the executable-corrections review engine) rendered through distinct surfaces
for different users.** Consumer (educational), Scholar (research), Contributor (manuscripts), Developer
(API/MCP), and Reviewer (adjudication). The surfaces differ by *who* and *what they're allowed to do* —
never by what the underlying truth is. Grounded in Vision 03 (one infra, many interfaces) + Vision 09
(the core → projections) + the review-engine authorization policy already built (`patala_submit_review`
requires actor_kind + scope). See `docs/vision/INDEX.md`.*

---

## 0. THE ARCHITECTURAL MOVE (one line)

> **Pāṭala owns the truth underneath. Each surface is a permission-scoped projection of the same core.
> The content never changes — only who can see it and what they may do.**

This is Vision 03 ("one scholarly knowledge infrastructure, several interfaces") + Vision 09 ("the
scholarly core rendered as projections") made concrete at the *product* level. The executable-corrections
engine we built is the permission spine: `patala_submit_review` already requires an authenticated
actor_kind + authorization_scope, and the `effective_state` ladder already determines what each surface
may see/do.

---

## 1. THE SHAPE (one core, five surfaces)

```
                    THE SCHOLARLY CORE
        (epistemic graph + MCP/API + executable-corrections engine)
                                    │
        ┌──────────────┬────────────┼────────────┬─────────────┐
        ▼              ▼            ▼            ▼             ▼
   CONSUMER        SCHOLAR       CONTRIBUTOR   DEVELOPER     REVIEWER
   (learn)        (research)     (manuscript)  (API)         (adjudicate)
```

Each surface is the SAME core with a different permission profile + projection. They are NOT separate
codebases — they are routes/dashboards over one shared substrate (the current Next.js app + the MCP +
the review engine).

---

## 2. THE FIVE SURFACES

### CONSUMER (educational) — the current site, read-only + guided
- What they see: the atlas graph, bibliography, read, concepts, learning, texts, traditions — the
  ORIGINAL / READ / GUIDE / STUDY projections (Vision 09).
- What they never see: raw review state, unresolved cruxes, the machinery. Just polished, grounded content.
- Permissions: read-only. MCP `corpus:read` only.
- **This is the current `app/` today.**

### SCHOLAR (research) — the peer-review / Scholar Workbench surface
- What they see: the Scholar Workbench (Phase 3E) — inspect one object, see its evidence + impact,
  submit a correction → the executable-corrections loop (`patala_get_review_state` /
  `patala_propose_review` / `patala_submit_review` / `patala_get_impact`).
- They see the honest state ladder (CANDIDATE → SINGLE_REVIEWED → ...), cruxes, open questions.
- Permissions: `review:read` + `proposal:write` + scoped `review:submit`. An authenticated scholar may
  submit a review within their authorization_scope; a machine/copilot may only PROPOSE.
- **This is where the review engine we built becomes the product.**

### CONTRIBUTOR (manuscripts) — the ingestion / acquisition surface
- What they do: upload a manuscript / scan / transcription → the acquisition pipeline (Vision 11 corpus),
  metadata + rights + provenance.
- Feeds Agent 2's corpus inventory (`corpus_state.py`) → the translation factory.
- Permissions: `manuscript:write`, `acquisition:read`. (This is the Agent-8 / Vision-11 surface.)

### DEVELOPER (API/MCP) — the programmatic surface
- `mcp.patala.org` + the full API + OAuth scopes (BYOA). External agents and scholars build on Pāṭala.
- **This is already real**: `/api/*` (34 routes), the MCP server (21 tools), now the 5 review tools.
- Permissions: OAuth scopes (`corpus:read`, `bibliography:read`, `review:read`, `proposal:write`,
  `review:submit`).

### REVIEWER (adjudication) — the A4 / editorial surface
- A focused queue of objects needing judgment, with reviewer identity + scope + authority.
- Permissions: `review:submit` + `review:adjudicate` — the promotion-policy surface, the strongest
  boundary. Only an editor/adjudicator can promote (`editorially_accepted`).

---

## 3. WHY THIS NATURALLY FOLLOWS WHAT WE BUILT

The multi-surface idea is **not speculative** — the permission model behind it already exists:

| Built piece | Powers the surfaces |
|---|---|
| The **epistemic graph + `corpus_state.py` ledger** | the shared core every surface reads |
| **`patala_submit_review` (actor_kind + scope)** | the surface-permission system (who may do what) |
| The **`effective_state` ladder** | what each surface is allowed to see/do |
| The **ImpactReport** | the scholar + reviewer surface's killer feature |
| The **MCP tools (21 + 5 review)** | the developer surface (and the agent access for all) |
| **Vision 09 projections** (ORIGINAL/READ/GUIDE/STUDY/CRITICAL) | the consumer vs. scholar renderings |

---

## 4. THE CLEAN RULE (guardrails)

1. **One core, many surfaces** — never duplicate the scholarly state or the review logic into a second site.
2. **The permission boundary is the constitution** — a machine/copilot can only PROPOSE; a scholar submits
   scoped; an adjudicator promotes. This is `patala_submit_review`'s policy, extended to the UI.
3. **A consumer never sees unresolved state; a scholar always sees it honestly.** Abstain / OPEN are
   first-class (the abstention principle).
4. **The reviewer surface has the strongest boundary** — promotion is a scoped human policy action.
5. **Build order**: the developer surface already exists; the scholar surface (Phase 3E Workbench) is
   next; the contributor surface follows the acquisition pipeline (Vision 11); the consumer site is current.
6. **Don't build a second codebase now** — surfaces are routes/dashboards over the one substrate.

---

## 5. THE BUILD SEQUENCE (relative to the current priorities)

```
NOW    developer surface (MCP/API) ✅ exists · consumer site ✅ exists
NEXT   scholar surface (Phase 3E Workbench: one object, one correction, see the impact)
       — but DEFERRED behind the autonomous-translation priority
THEN   reviewer surface (A4 queue) + contributor surface (Vision 11 acquisition)
```

---

## 6. THE ONE-SENTENCE CARRY-FORWARD

**Pāṭala is one scholarly core (the epistemic graph + MCP/API + the executable-corrections engine) rendered
through five permission-scoped surfaces — consumer (educational, read-only), scholar (Workbench, can
propose + submit scoped), contributor (manuscript ingestion), developer (MCP/API, already real), and
reviewer (adjudication, strongest boundary) — where the surfaces differ by who and what they may do, never
by what the underlying truth is; and the review-engine authorization policy already built is the spine that
makes this possible. Build the surfaces as routes over one substrate, not separate sites, and defer the
scholar surface (Phase 3E) until after the autonomous-translation priority.**
