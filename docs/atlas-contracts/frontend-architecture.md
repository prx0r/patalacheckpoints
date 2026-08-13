# Pāṭala Frontend Architecture — the law (default architecture now)

*2026-08-13. The frozen frontend rule. This is the default architecture for all surfaces, not a
per-product split.*

## The law

> **Astro owns documents. React owns interactions. Pāṭala objects own semantics.**

```
Astro            = page/document shell (server-rendered static HTML)
React/Preact     = localized interactivity (islands)
Cloudflare Worker= API / runtime (all data)
Pāṭala objects   = canonical semantics (the API serves these; the frontend never invents them)
```

## The decision rule (per page/component, NOT per product)

Don't split rigidly by "consumer" vs "scholar." Split by **interaction density**.

```text
static until proven interactive    → Astro page
island when local state is needed  → <X client:visible />
SPA-like island only when the whole surface genuinely behaves like an app
```

A scholar workbench page can still be **Astro** if most of it is static metadata/evidence and only the
graph/review controls are islands. A full education exercise sequence can be **one large React island**
inside an Astro route. The rule is per-surface, not per-audience.

## Why React (not Preact) initially

Use **React** first. The bundle saving from Preact matters less than compatibility with the interaction
libraries we may want (argument manipulation, editors, visualizations, accessibility tooling, education
components). Astro only hydrates islands, so React's cost is **localized**. If measurement later shows a
real problem, Preact becomes an optimization — not an architectural dependency.

## The surface map (frozen)

```text
STATIC / ASTRO-FIRST
  /texts/*  /works/*  /editions/*  /manuscripts/*
  /scholars/*  /essays/*  /timeline/*  /bibliography/*

ASTRO + SMALL ISLANDS
  translation comparison   alternate reading selector   term inspector
  citation popover         timeline controls            search
  source zoom              manuscript folio viewer

ASTRO + LARGE APP ISLAND
  /learn/*   /review/*   /arguments/* (interactive mode)   /scholar/workbench/*
```

Example: the normal argument page stays mostly server-rendered — title, question, premises, conclusion,
evidence, cruxes, review status — with `<ArgumentManipulator client:visible />` only when someone wants to
retract a premise or explore the inference graph. Don't make every visitor boot the entire argument app
just to read the claim.

## Canonical data must drive the UI (never the reverse)

**Translation alternatives are versioned `Translation` / `TranslationDecision` objects**, not UI-only data.
The island queries/renders those canonical objects. Same for education:

```text
LearningBundle → InteractionDefinition JSON → React renderer
```

```json
{ "interaction_type": "CRUX_IDENTIFICATION", "argument_ref": "PTARG...",
  "prompt": "...", "options": [...], "feedback_rules": [...] }
```

- The canonical education layer is **framework-independent**; React merely renders it.
- Translation compare = `TranslationCompareBundle → React component`, never `React component → owns its
  own scholarly rules`.
- The same comparison object powers Review, API, essays, and education later.

## Migration posture

Scaffold a **proof-of-concept before any broad migration**; do not stop feature development for a
"rewrite." The PoC must prove four things:

```text
1. A passage route renders fully readable with JS disabled.
2. TranslationCompare hydrates independently (island).
3. Data comes from the same API/bundle contract future agents use.
4. Lighthouse/bundle measurements materially beat the existing Next page.
```

If those four hold, migrate reader surfaces incrementally. Keep the frontend **subordinate** to the
canonical graph/API work — never a standalone frontend rewrite.

## Why this is best for agents too

Agents consume the **API/bundle contract**, not the website. So this law keeps the frontend from ever
becoming the source of truth: the Worker serves canonical objects, and both the human UI (Astro+islands)
and agents (MCP over the API) read the same contract. The frontend is one consumer among many.
