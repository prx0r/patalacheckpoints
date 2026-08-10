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

## 4. The diachronic sense-trajectory (the signature feature)

The reference map's killer feature: a lemma does NOT have one meaning — it has a
**trajectory** across traditions and periods.

```bash
curl "http://localhost:3000/api/terms/kula/history"
```

```json
{
  "lemma": "kula",
  "trajectory": [
    { "period": "early Yoginī/Kaula", "tradition": "Yoginī cult", "sense": "family / lineage of Yoginīs or Mothers", "translation_policy": "translate 'family/lineage'..." },
    { "period": "developed Kaula", "tradition": "Kaula", "sense": "body; totality of power and phenomena" },
    { "period": "Kubjikā", "tradition": "Kubjikā", "sense": "the mantra-body / structured Kula", "evidence": ["KMT 17.80–82"] },
    { "period": "Abhinava/Trika", "tradition": "Trika", "sense": "the manifest pole vs the transcendent akula", "evidence": ["TĀ 3.143"] }
  ],
  "accepted_senses": [ ... ]
}
```

These are **evidence-backed hypotheses** (the reference map + dossiers), not settled
facts. The trajectory is why a lemma should be rendered *by context*, not by a
dictionary's first gloss — **semantic consistency is the goal, not lexical uniformity.**

## 5. Machine/human proposals (separate)

```bash
curl "http://localhost:3000/api/term-proposals?lemma=kula"
```

Proposals live here. A proposal **never** promotes itself into the accepted ledger — only a human review event does (`proposed → reviewed → accepted`).

---

**MCP:** `get_term_senses({ lemma })`, `get_term_history({ lemma })`, `find_term_occurrences({ lemma })`, `concordance({ q })`.
