# essays.tantrafiles.xyz — the Tantra Hub

*The Śaiva Tantra Atlas — a research workstation for medieval Śaiva texts, and the living bibliography + text-reader + translation-workshop + API/MCP layer. Built to make the textual landscape of Tantra navigable.*

## For a new agent — read these first (in order)

1. **`HANDOVER_SITE.md`** — the site-builder handover: the vision, the current state, the bibliography migration, the next steps (audit the school-passes, the reader, the per-entity routes).
2. **`HANDOVER_MCP_API.md`** — the **machine-facing layer** (the highest-priority build): the retrieval/audit API + the MCP server + the TTS + the formal translation-flow + the provenance hierarchy.
3. **`SITE_STATUS.md`** — the site's growth-rules + the sync-gap discipline.
4. **`../docs/endgame2.md`** — the spec (the Tantra Hub vision, the machine-facing plan, the FoJin-comparison). Also `../docs/endgame1.md` and `../corpus/learning/ENDGAME_SITE_SPEC.md`.

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
