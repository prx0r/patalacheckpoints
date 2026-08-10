# Recipe — Explore terminology

The term ledger is Pāṭala's evidence-backed glossary: **accepted senses** are review-promoted; **proposals** are separate and never auto-accepted. A lemma has different senses in different texts/periods/traditions — there is no single global meaning.

## 1. The accepted ledger

```bash
curl "http://localhost:3000/api/terms"
```

Returns each lemma with its accepted sense labels and preferred renderings.

## 2. Accepted senses for one lemma

```bash
curl "http://localhost:3000/api/terms/kula/senses"
```

```json
{
  "lemma": "kula",
  "senses": [
    { "id": "kula.lineage", "label": "lineage / family" },
    { "id": "kula.body.power", "label": "body / power / totality" }
  ],
  "preferred_renderings": ["totality", "lineage", "body of powers", "the Kula (school)"],
  "proposals": 1
}
```

`accepted` = current editorial position, not universal consensus. These are **not** a dictionary and not evidence of occurrence.

## 3. Surface occurrences (honest about method)

```bash
curl "http://localhost:3000/api/terms/kula/occurrences?work_id=kubjikamata"
```

```json
{
  "lemma": "kula",
  "match_method": "substring",
  "lemmatized": false,
  "count": 207,
  "occurrences": [ ... ]
}
```

**This is substring matching, not lemma retrieval.** Sanskrit inflects — `śakti / śaktiḥ / śaktim` are different surface forms. The `lemmatized: false` field is Pāṭala being honest that this is a raw concordance, not a morphological search.

## 4. Machine/human proposals (separate)

```bash
curl "http://localhost:3000/api/term-proposals?lemma=kula"
```

Proposals live here. A proposal **never** promotes itself into the accepted ledger — only a human review event does (`proposed → reviewed → accepted`).

---

**MCP:** `get_term_senses({ lemma })`, `find_term_occurrences({ lemma })`, `concordance({ q })`.
