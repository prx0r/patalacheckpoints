# essays.tantrafiles.xyz — the Tantra Hub

*The Śaiva Tantra Atlas — a research workstation for medieval Śaiva texts, and the living bibliography + text-reader + translation-workshop + API/MCP layer. Built to make the textual landscape of Tantra navigable.*

## For a new agent — read these first (in order)

1. **`HANDOVER.md`** — the COMPLETE STATE: every layer assigned (ACTIVE/ARCHIVED), how to use the
   existing translation asset, the canonical indexes, and the priority list. **Read this FIRST — it tells
   you what exists, what's real, and what to continue.**
2. **`AGENTS.md`** — the GOVERNING rule: the anti-theatre doctrine (a tested schema ≠ a result; only
   independent gold + blind eval + metric + human adjudication makes something real). Also read
   `machinelearning/_ACTIVE/AGENTS-DOCTRINE.md` + `machinelearning/_ACTIVE/CLAIMS.md` + run
   `python3 machinelearning/theatre_check.py --status`. **Read this before ANY build.**
3. **`NAVIGATION.md`** — the MASTER INDEX: resolve ANYTHING (site surface, API, data file, script, doc)
   to its layer + canonical ref + implementation + docs + run command + Hermes usage. Read this to
   navigate the whole project. (Its §0b is the code map — every dir in plain words.)
4. **`docs/process/README.md`** — the end-to-end infra reference (ingestion → atlas → factory → R2).
   **Read this before writing any infra code** — if a piece is listed as REUSABLE, extend it, don't
   redefine it. Layer guides: `docs/process/{01-ingestion,02-atlas,03-factory,04-r2-storage}.md`.
5. **`VISION_AND_NAVIGATION.md`** — THE vision + logical progression + navigation.
6. **`docs/INDEX.md`** — the canonical docs index (the ONE source of truth per concern; archived
   stale handovers are in `handover/archive/`).
7. **`handover/README.md`** — the coordination folder for both lanes (Agent 1 ML / Agent 2 integration);
   current state per lane lives in `handover/agent-1-ml/INDEX.md` and `handover/agent-2-integration/INDEX.md`.
8. **`machinelearning/_ACTIVE/MLUSEINPATALA.md`** — the frozen ML strategy.
9. **`docs/CHANGELOG.md`** — the API/data/scholarly changelog.
10. **`../docs/endgame2.md`** — the spec (the Tantra Hub vision, the machine-facing plan, the
   FoJin-comparison). Also `../docs/endgame1.md` and `../corpus/learning/ENDGAME_SITE_SPEC.md`.

> The full-system onboarding (how the whole scholarly factory works) is `THE_COMPANION.md` in
> `sanskritree/translations/_stack/ipvv/specs/`.

## The stack

- **Next.js 16** (Turbopack) + **Tailwind v4** (CSS-first config — the palette vars are in `app/globals.css`; use `text-[color:var(--bone)]`/`var(--saffron)`, not `text-ivory`).
- **Data** (`data/atlas/`): `traditions.ts`, `texts.ts`, `people.ts`, `concepts.ts`, `relations.ts` (the atlas graph) + `bibliographyTypes.ts` (the bibliography schema), `audited.ts` (the Trika-10 at full depth), `bibliographySeed.ts` (the 70-text seed, verified:false).
- **Routes**: `/` (the atlas graph), `/bibliography` (the bibliography list), the `app/{traditions,texts,concepts,people}/` folders scaffolded-but-empty (the per-entity pages — next to fill).

## The current routes

```
/               the atlas graph (ReactFlow, draggable retro-windows)
/bibliography   the bibliography — the audited Trika-10 + the seed
```

## The build commands

```bash
npm run dev      # local dev (localhost:3000)
npm run build    # the verification (must be clean)
```

## The discipline
- **Data is king; components are dumb.** Edit `data/atlas/*` to grow the site.
- Relations are NOT `parent:` fields — typed + confidence + evidence.
- Every translation-status claim carries its evidence + `status_checked`.
- Every research milestone should touch `data/atlas/` (the "site-update" line).
- The API is the single source of truth; the site is a render of it.
