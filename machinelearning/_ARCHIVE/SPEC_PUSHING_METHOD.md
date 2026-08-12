# SPEC — THE PUSHING METHOD (the mechanical deep-dive, reusable per source)

*2026-08-12. Formalizes the "Logicvid method" exemplified by `PUSHING-TANTRALOKA` and `PUSHING-IPVV`
into a reusable, agnostic deep-dive formula. Purpose: for any primary source, mechanically hound the
text with "why," force its OWN reasoning out, store the quoted passages, and expose the deep
arguments — which are exactly the input the logical-argument layer then formalizes.*

---

## 1. The one rule

> **Hound the text with "why," force its OWN reasoning — not our frameworks. Our frameworks only
> supply the questioning; the answers must come from the text itself.**

The extracted passages are the source of truth. Each question stores the full quoted passage (more
than needed) so the text's own argument can be re-read and re-pushed. Our frameworks (aperture,
MEPIT, pure-thesis, Solms/valence) enter ONLY AFTER the text has been allowed to speak.

---

## 2. The formula (per source, per region)

```
PUSHING — the deep-dive scaffold
1. PRIMARY SOURCE   name the text + its editions/commentaries + coverage.
2. TAKE THE CLAIMS  from the text's asserted claims.
3. WHY?             turn each into a hard "why" question (the ones scholars often skip).
4. HOUND THE TEXT   force the TEXT's own reasoning (its commentaries, its own dialectic) — NOT ours.
5. STORE THE PASSAGES  each question stores the full quoted passage + locator (the text speaks).
6. KEEP ASKING "WHY"   until the text's deepest reasoning is exposed.
7. THEN INTERPRET   bring our frameworks in only after the text has spoken.
```

---

## 3. The IPVV variant (PUSHING-IPVV)

For a commentary (like the IPVV), focus MORE on the text's own internal structure:
- the vimarśas (the reflexive examinations),
- the nanu→āha dialectical skeleton (every passage is objection → reply),
- the three adhikāras (books/sections).

Let Abhinavagupta's commentary speak on its own terms before bringing anything of ours in.

---

## 4. Why it's the discovery step

The PUSHING method finds:
- **tensions** (the text seems to pull two ways);
- **implicit commitments** (what the text must assume to make its claim);
- **the deepest arguments** (the reasoning the text gives when hounded).

These are exactly what the **formal logical-argument layer** then makes precise (§5). The method
is the *discovery*; the argument is the *formalization*; the essay is the *narration*.

---

## 5. The downstream pipeline (the gold)

```
PUSHING enquiry (finds a tension, quotes the passages)
   ↓  /api/resolve + the published store
FORMAL LOGICAL ARGUMENT (the gold)
   • premises from the quoted passages
   • inference typed (reductio / analogy / identity / entailment)
   • conclusion
   • tied to the truth engine (NYĀYA→LEAN decomposition)
   ↓
ESSAY (written from the argument — every claim cites the argument + its passages)
   ↓
LEARNING (taught from the essay)
```

All on the same passage IDs; all tracked on the source hub (`/api/hub`).

---

## 6. Validation — how we know a PUSHING enquiry is sound

- [ ] every question stores the full quoted passage (text speaks first)
- [ ] the answers come from the TEXT (its commentaries), not from our frameworks
- [ ] the tensions found are grounded in the quoted passages (resolvable via `/api/resolve`)
- [ ] frameworks are clearly marked as AFTER the text has spoken
- [ ] the passages link to the published corpus (the hub records passage_ids)

---

## 7. Seed resources (the exemplars)

| Source | PUSHING file | Status |
|---|---|---|
| IPVV | `research-library/recognition/pushing-ipvv/PUSHING-IPVV.md` | seed |
| Tantrāloka | `research-library/recognition/pushing-tantraloka/PUSHING-TANTRALOKA.md` | seed |

These are tracked on the source hub (`data/corpus/hub.ts` → `pt:hub:ipvv:pushing:main`, etc.).
