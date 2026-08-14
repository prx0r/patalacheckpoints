# Ambuda DCS — corpus-grounded Sanskrit linguistic priors (S-tier dataset)

**What Pāṭala borrows:** the sanitized Digital Corpus of Sanskrit (DCS) dataset — 650k+ annotated
Sanskrit sentences from ~250 texts. Gives corpus-grounded linguistic priors: "how was this surface form
analyzed across actual Sanskrit texts?" instead of relying only on an LLM.

**License:** varies (Hellwig's data). Repo: `ambuda-org/dcs` (Ambuda's sanitized + corrected version over
Oliver Hellwig's DCS).

## What it powers
- translation confidence
- word segmentation
- lemma disambiguation
- grammatical explanations
- education questions
- detecting unusual technical usage

## How Pāṭala consumes it
**PLANNED.** Ingest as a corpus dataset → feed the linguistic/translation confidence layer and
education. Store as a Bronze snapshot on R2; derive frequency/analysis priors.

## Doctrine
A corpus prior is **evidence for a candidate analysis**, never an unquestionable answer. Combine with
cross-analyzer agreement (see `dcs-sh-alignment.md`) for confidence.
