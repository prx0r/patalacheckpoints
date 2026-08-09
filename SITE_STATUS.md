# essays.tantrafiles.xyz — site status & update protocol

*The Śaiva Tantra Atlas — a research workstation for medieval Śaiva texts, reinterpreted from chaining.dev's retro-computing interaction architecture into a "retro research workstation for medieval Śaiva texts" (charcoal/ivory/saffron/vermilion, manuscript-tech, not Windows XP). This file records WHERE the site is and WHEN to update it — so it grows with the translation project instead of drifting away from it.*

---

## 1. What the site is (the current state)

**The one page (for now):** the atlas graph — traditions, texts, ācāryas, and concepts as draggable retro-windows, with saffron/vermilion particles flowing along typed relationship-edges. Click any node → the dossier panel opens (systemic function, doctrinal core, problems, outputs, relations, resources).

**The data model** (`lib/atlas.ts`): the chaining.dev project-model replaced with an entity-relation graph:
- `AtlasEntity` — `tradition | text | person | concept`, with `sanskrit`, `period`, `summary`, `concepts`, `resources`, `dossier`
- `AtlasRelation` — `develops-from | textual-borrowing | influence | synthesis | commentary | contains | conceptual-parallel`, each with `confidence: established | strong | possible` + `evidence`

**The crucial design rule (from the reference map):** relations are NOT `parent:` fields. History is not a family tree. Every edge is typed, confidence-weighted, and separately stored in `data/atlas/relations.ts` — so the canonical research we're building can populate the edges.

**Data populated so far** (`data/atlas/`):
| File | Entities | Source |
|---|---|---|
| `traditions.ts` | 7 (Trika, Krama, Kubjikā, Kaula, Spanda, Pratyabhijñā, Sarvāmnāya) | the reference map's taxonomy |
| `texts.ts` | 6 (Tantrāloka, Mahānayaprakāśa, Mahārthamañjarī, Kubjikāmata, Kaulajñānanirṇaya, Spandakārikā) | our translated/open texts |
| `people.ts` | 7 (Abhinavagupta, Utpaladeva, Somānanda, Jñānanetra, Jayaratha, Maheśvarānanda, Dyczkowski) | the reference map's timeline |
| `concepts.ts` | 6 (kula, krama, recognition, spanda, vimarśa, mālinī) | the glossary dossiers |
| `relations.ts` | 44 edges | the reference map's influence graph + our research |

**Deployment:** NOT yet deployed. Build passes (`next build` clean). The env `CLOUDFLARE_API_TOKEN` is invalid; the R2 `cfat_` token is R2-scoped (S3 API) and cannot create Pages deployments. The site runs locally (`npm run start` → `localhost:3000`).

---

## 2. When to update the site (the growth rules)

The site is a **render of the translation project's progress** — it grows when the project's research grows. The update triggers, in priority order:

### A. When a text's T3 is complete (HIGH — the primary trigger)
When a text finishes its pipeline (T1 → R1 → T2 → R2 → T3):
1. Add it to `data/atlas/texts.ts` — `summary` from the T3's provenance, `dossier.doctrinalCore` from the R2's adjudications, `resources` pointing to the translation.
2. Add the `contains` edge to its tradition; add `commentary`/`develops-from` edges to its author.
3. If it names sources (e.g. the Kulapradīpa→Kulārṇava), add the `textual-borrowing` edge with the evidence.

### B. When a new dossier is built (MEDIUM)
The reference map's 24-lemma backlog (kula, akula, krama, śakti, spanda, saṃvit, vimarśa, parāmarśa, prakāśa, visarga, anuttara, khecarī, mālinī, mātṛkā, svātantrya, āveśa, samāveśa, uccāra, vyāpti, śūnya, saṃhāra, sṛṣṭi, cakra, mantra):
- Each completed dossier → a `concepts.ts` entry + `conceptual-parallel` edges to its traditions/texts.

### C. When a tradition's map changes (MEDIUM)
- A new anchor acquired → add to the tradition's `resources` + a `dyczkowski`-style curation edge if relevant.
- A new text acquired (e.g. Kramasadbhāva when found) → new `texts.ts` entry + edges.

### D. When the site's structure evolves (LOW — the roadmap)
Per the ENDGAME site-spec, the site grows outward:
- **Now:** one atlas page (this state).
- **Next layer:** the per-entity routes (`/traditions/[slug]`, `/texts/[slug]`, `/concepts/[slug]`, `/people/[slug]`) — the static-per-entity pages. The `app/[type]/[slug]/` folders are scaffolded but empty.
- **The reader:** the translated corpus as a content layer (`content/texts/...` — the Bilara-style segment view with the concordance evidence panels).
- **The wider map:** zoom out to "Tantric India" (Śaiva · Buddhist · Śākta · Nātha) — the backend being a graph (not a tree) makes this correct.

---

## 3. How to update (the mechanical steps)

**Data is king — the components are dumb.** The site's components (AtlasNode, AtlasEdge, EntityDossier) read only from `data/atlas/`. To grow the site, you almost always only edit the data files:

1. `data/atlas/traditions.ts` / `texts.ts` / `people.ts` / `concepts.ts` — add/edit entities.
2. `data/atlas/relations.ts` — add/edit edges (typed + confidence + evidence).
3. Run `npm run build` to verify types.
4. Commit.

**Never hard-code research into the components.** If a dossier needs a new section type, extend `lib/atlas.ts`'s `dossier` shape, then render it — don't fork a component per text.

**The relation rule when adding edges:** every edge needs a `confidence` and an `evidence` string. If the evidence is "the reference map says" that's fine; if it's "we verified in the concordance" even better. No confidence-less edges (the map's Dyczkowski-effect: don't let curation masquerade as history).

---

## 4. The alignment guarantee (how it stays in sync)

The site and the translation project stay aligned through **one discipline**: every translation milestone (a T3, a dossier, an anchor) carries a "site-update" line in its commit — the equivalent of a checkbox that says "the atlas now knows about this." Concretely:

- The **T3-commit** → also commits the `texts.ts` entry + edges (trigger A).
- The **dossier-commit** → also commits the `concepts.ts` entry + edges (trigger B).
- The **anchor-commit** → also commits the `resources`/curation edges (trigger C).

If a milestone's commit does NOT touch `data/atlas/`, that's a signal the milestone was research-only (fine) or the site-update was forgotten (fix it).

**The current sync gap:** the T3s and dossiers we've produced (Jñānakārikā, Ajaḍapramātṛsiddhi, Mahārthamañjarī, the school-batch T1s) are NOT yet in the site data — the site currently shows only the six "seed" texts. The next site-update should add them (see the checklist below).

---

## 5. Deployment status & how to go live

- **Blocked on:** a Cloudflare API token with `Cloudflare Pages: Edit` (or Workers) permission for account `954612afb5a97bb15dddcdc70176813d`. The current `cfat_` token is R2-scoped (S3) only.
- **The command once a token exists:** `wrangler pages deploy .next --project-name <name> --commit-dirty=true` (or a git-connected Pages project, mirroring `tantrafiles-hub`'s `deploy` script).
- **Until then:** `npm run dev` / `npm run start` for local viewing; the R2 bucket can hold a static export (`next build && npx next export`) ready to wire to a domain the moment a Pages/Workers token exists.

---

## 6. The immediate update checklist (next time you touch the site)

- [ ] Add the **Jñānakārikā** text-entry + edges (T3-FINAL, the Matsyendra bundle).
- [ ] Add the **Ajaḍapramātṛsiddhi** text-entry + the Utpaladeva/recognition edges (T3-FINAL, key verses).
- [ ] Add the **Kaularahasya** + **Kulapradīpa** text-entries (the Kaula school's continuations).
- [ ] Add **Kubjikātantra** (the 17-paṭala T1'd text) — it's a separate text from the Kubjikāmata.
- [ ] Add the **Śivasūtra** (T3'd, anchored by Dyczkowski) — the Trika's foundational text.
- [ ] Add the remaining dossier-lemmas as they're built (the 24-lemma backlog).
- [ ] When the token exists: deploy to Pages and record the URL here.

*The site is the translation project's living map. It should never be more than one research-milestone behind the corpus — and the discipline above keeps it that way.*
