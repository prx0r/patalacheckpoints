# Endgame Spec 3 — one scholarly knowledge infrastructure, several interfaces

*The strongest vision: **one underlying scholarly knowledge infrastructure with several interfaces on top of it**. Not separate projects.*

```text
                    TANTRAKOŚA
                        │
             ONE STRUCTURED CORPUS
                        │
      ┌─────────────────┼─────────────────┐
      │                 │                 │
   CONSUMER          SCHOLAR           MACHINE
     APP            WORKSPACE          API / MCP
      │                 │                 │
 learning          translation       ChatGPT
 listening         annotation        Claude
 courses           editions          research agents
 retreats          collaboration     institutional tools
```

That architecture is the big idea.

## 1. Yes: absolutely make a consumer app eventually

The consumer app should **not look like the scholar interface**.

A normal person doesn't care about:

> NAK 5-358, NGMPP B30/26, apparatus reading β.

They want:

> What is Krama?
> What does this verse mean?
> Can I hear the Sanskrit?
> What should I read next?

So the app becomes something closer to a high-quality learning environment:

```text
HOME

Continue reading
Vijñānabhairava
Verse 27 →

Today's concept
SPANDA →

Listen
Sanskrit recitation →

Watch
Bäumer on Recognition →

Explore
Trika · Krama · Śrīvidyā · Kubjikā
```

Then a text page might have two layers:

**Simple**

```text
Sanskrit

English

▶ Listen

What this means
```

and:

**Go deeper**

```text
Word analysis
Other translations
Traditional commentary
Academic commentary
Related passages
Manuscripts
```

Same data. Different interface.

---

# 2. Consumer accounts

Consumer profiles could support:

```text
saved texts
reading history
bookmarks
annotations
playlists
courses
Sanskrit vocabulary
lecture history
study streak/progress
personal collections
retreats/events
```

Eventually:

> **Learn Trika**

could be a structured pathway.

```text
1. What is Śiva?
2. Śakti
3. 36 tattvas
4. Recognition
5. Spanda
6. Śivasūtra
7. Pratyabhijñāhṛdaya
8. Vijñānabhairava
9. Tantrāloka
```

But every lesson can descend into actual primary sources.

That's an unusually strong educational proposition.

---

# 3. Scholar accounts should be fundamentally different

This could be one of your best ideas.

A scholar account isn't:

> premium user.

It is:

> **identified contributor to the corpus.**

Profile:

```text
DR ISABELLE EXAMPLE

University ...
ORCID ...

Expertise
Pratyabhijñā
Buddhist epistemology
Kashmir Śaivism

PUBLICATIONS
23 →

CONTRIBUTIONS TO TANTRAKOŚA

Translations             143 passages
Translation reviews       87
Textual corrections       19
Manuscript readings        8
Bibliographic additions   31
Lectures                    4
```

Click a contribution:

> Corrected translation of ĪPVV 2.3.14
> accepted by editor · 14 March 2028.

That creates **academic credit**.

This is much better than asking scholars to volunteer into a black hole.

---

# 4. Contributions should themselves be citable

This could be genuinely novel.

Suppose a scholar produces a translation of an untranslated passage.

Give it something permanent:

```text
tantrakosha:translation:kubjikamata:3.14:v4
```

with:

```text
translator
reviewers
date
source edition
version
citation
```

Then the site generates:

> Prior, Thomas & Smith, Jane. "Kubjikāmatatantra 3.14: Translation and Notes." *Pāṭala*, version 4, 2028.

BibTeX button.

RIS.

Permanent URL.

Potential DOI later for substantial editions/projects.

Then contributing becomes academically useful.

---

# 5. Your "free if you cite us" idea is close, but I'd modify it

I wouldn't make basic human access conditional on citation.

Instead:

## Open scholarly core

Researchers can freely:

* read
* search
* cite
* use public API within reasonable limits
* export individual passages
* use MCP
* build scholarship from the corpus

with very clear **citation guidance**.

For example:

> If research materially relies upon Pāṭala's structured text, translation, alignment or dataset, please cite the relevant work/version.

That's normal scholarly behavior.

For datasets/API use, you could have something like:

```text
Public research licence
Free for non-commercial scholarly use
Attribution required where applicable
Source-specific rights preserved
```

But you need to be careful because **you cannot apply one blanket licence to material you don't own**.

Your own:

* metadata
* annotations
* working translations
* alignments
* relationships

can have your chosen licence.

Third-party editions/translations retain their own rights.

That's why the rights/provenance architecture we've discussed matters.

---

# 6. Scholars could get the serious tools free

This is actually strategically smart.

Imagine:

### Scholar account — free

```text
private translation workspace
corpus search
historical term search
translation memory
MCP
annotations
bibliography
limited AI audits
public scholar profile
collaboration
```

Why give this away?

Because their work **improves your corpus**.

They're contributing the scarce thing you need:

> expert validation.

Your network effect becomes:

```text
better tools
   ↓
more scholars
   ↓
more corrections/translations
   ↓
better corpus
   ↓
better API
   ↓
better AI tools
   ↓
more scholars
```

That's considerably more valuable than squeezing £10/month from an Indologist.

---

# 7. Then institutions pay

That's where I'd monetize scholarly infrastructure.

A university gets:

```text
Pāṭala Institutional

SSO
private projects
private manuscripts
unpublished text storage
teams
permissions
large API quotas
bulk corpus analysis
private MCP
IIIF manuscript integration
TEI export
audit logs
backups
support
project dashboards
```

Example:

> University of Hamburg — Jayadrathayāmala Project

```text
12 researchers
3 editors
2,441 passages
7 manuscript witnesses

PUBLIC
published translations

PRIVATE
draft transcriptions
unpublished apparatus
research notes
```

That is something a grant can actually pay for.

---

# 8. Research projects become mini-sites

This is another really strong possibility.

A funded project gets:

```text
tantrakosha.org/projects/jayadrathayamala
```

with:

```text
PROJECT

Critical Edition of the Jayadrathayāmala

Principal investigator
...

Participating institutions
...

Manuscripts
12

Progress
████████░░ 78%

Latest publication
...

Read current edition →
```

When the grant ends, the project's digital infrastructure **doesn't disappear**.

It remains part of Pāṭala.

That solves a real digital-humanities problem.

---

# 9. A reputation system, without gamifying scholarship stupidly

Don't do:

> 900 Tantra Points!!!

Instead use factual contribution metrics:

```text
Reviewed by
Dr X

Expertise
Krama textual history

Pāṭala contributions
• 61 reviewed passages
• 14 accepted emendations
• 2 critical editions
```

You can display:

```text
Verified scholar
Contributor
Text editor
Project editor
```

based on actual role rather than arbitrary levels.

---

# 10. Scholar translation rooms

Imagine opening:

> `Kubjikāmata — Paṭala 3`

Scholar workspace:

```text
┌ SOURCE ────────────┬ TRANSLATION ───────────┐
│ Sanskrit           │ Working English         │
│                    │                         │
│ variant readings   │ v7                      │
└────────────────────┴─────────────────────────┘

TERM CONTEXT
kula — 84 occurrences →

PARALLELS
3 candidates →

OTHER TRANSLATIONS
2 excerpts →

COMMENTS
Scholar A
Scholar B

AUDIT
2 issues →

HISTORY
v1 … v7
```

This is almost **GitHub + CAT software + digital critical edition**.

But domain-specific.

---

# 11. Translation projects can be opened to the public

Different permission levels:

```text
VIEWER
read

COMMENTER
suggest

CONTRIBUTOR
submit translation

REVIEWER
approve/reject

EDITOR
publish
```

Then a project can decide:

> public suggestions allowed

or:

> scholars-only.

That's very buildable.

---

# 12. Community translations become a pipeline, not a wiki free-for-all

You do not want:

> someone replaces *vimarśa* with "cosmic vibes."

Instead:

```text
Published translation
        │
        └── Suggest change
                  ↓
           proposed revision
                  ↓
            evidence required
                  ↓
                review
                  ↓
          accepted / rejected
```

Original text remains untouched until reviewed.

That's basically pull requests for translations.

---

# 13. Translation bounties / funding

This could become very interesting.

Page:

```text
UNTRANSLATED

Ṣaṭsāhasrasaṃhitā
0% English

Kubjikāmata
18%

Śrīmatottara
0%
```

Then:

> Fund this translation.

Users/donors contribute.

Eventually:

```text
£4,200 funded
Target £8,000

Lead translator:
Dr X

Reviewer:
Dr Y
```

Money goes toward actual scholarship.

Pāṭala could retain a small administrative/platform percentage.

That is a much more compelling donation model than:

> Please support our website.

---

# 14. Scholar sponsorships

Imagine somebody deeply interested in Krama funds:

> **The Devīpañcaśataka Translation Project**

Pāṭala hires/contracts a scholar.

Result:

* open Sanskrit
* translation
* notes
* API data
* glossary
* lectures
* course
* public edition

One funded translation produces **six products**.

That's the platform leverage.

---

# 15. Lectures should attach to passages

This remains one of my favourite ideas from our discussion.

Rather than:

> Videos

have:

```text
Tantrāloka 3.1–3.42

LECTURES

Mark Dyczkowski
Tantrāloka Chapter 3
01:23:17

Relevant segment
▶ 32:14–46:08
```

Transcribe with permission.

Then attach transcript fragments to concepts.

Selecting:

`vimarśa`

could return:

```text
PRIMARY TEXT
37 passages

COMMENTARIES
8 passages

SCHOLARSHIP
14 papers

LECTURES
Bäumer 3 clips
Dyczkowski 9 clips
Lakshman Joo 4 clips
```

That's an incredible research/learning interface.

---

# 16. Scholar interviews can become structured knowledge

If you eventually live around Varanasi/BHU and interview scholars, don't just upload:

> Interview #14.

Ask focused questions:

> What does *kula* mean in the Kubjikā tradition?

The video becomes:

```text
resource_type: scholar_interview
speaker: X

concepts:
kula
kubjikā
paścimāmnāya

texts:
Kubjikāmata
Ṣaṭsāhasra

transcript:
...
```

Now the interview enriches the corpus.

---

# 17. Retreats can be much more intelligent than retreat listings

Eventually:

## Pāṭala Study Retreats

Not:

> awaken your inner goddess for $3,000.

Instead:

> **Vijñānabhairava: Text and Practice**
>
> Five days.
>
> Sanskrit reading with scholar X.
> Historical introduction with Y.
> Practice sessions with teacher Z.

The participant receives an in-app programme:

```text
DAY 1

Read
VBh 1–23

Listen
Sanskrit audio

Watch
Historical introduction

Notes
...

Practice
Teacher-led session
```

Afterward:

> Continue studying the text →

The retreat is simply a physical extension of the platform.

---

# 18. Eventually teachers can have profiles too

Separate **scholar** from **teacher/practitioner**.

That's important.

```text
SCHOLAR
academic expertise

TEACHER
practice instruction

TRANSLATOR
textual work

TRADITIONAL HOLDER
lineage-specific knowledge
```

One person can hold several roles.

Then users understand the source of authority.

Someone might be an exceptional meditation teacher but not a philologist.

The platform shouldn't blur those.

---

# 19. Consumer subscription is still plausible

I'd probably keep the actual corpus broadly open.

Consumer premium could be:

```text
£5–10/month

offline app
full courses
guided learning paths
audio library
Sanskrit TTS
personal notes
AI tutor
advanced concept explorer
retreat discounts
```

The texts themselves aren't the paywall.

**Experience and compute are.**

---

# 20. The AI tutor could be extremely good

Because unlike ChatGPT normally, it knows exactly what source layer it is using.

Consumer asks:

> Explain spanda like I'm new to Kashmir Shaivism.

It answers from your corpus.

Then:

> Show me where this actually appears.

```text
Spandakārikā 1.2 →
Kṣemarāja →
Tantrāloka →
```

Then:

> More academic explanation.

Same underlying graph, different response level.

---

# 21. Scholar AI becomes a different mode

Scholar asks:

> Find early instances where *krama* appears to mean something more technical than ordinary succession.

Instead of friendly explanation:

```text
27 candidate occurrences

850–950
...

950–1050
...

Ranked by:
date
tradition
lexical context
commentarial support
```

Same platform, completely different UX.

---

# 22. Public API could create an ecosystem beyond you

This may ultimately matter more than your own app.

Other developers could build:

* Sanskrit readers
* translation apps
* academic tools
* visual maps
* AI tutors
* educational games
* lexicons
* research agents

against:

```text
api.tantrakosha.org
```

All returning provenance to your corpus.

Your website then becomes one client among many.

That's the **infrastructure endgame**.

---

# 23. MCP is potentially your distribution channel

This is another genuinely big idea.

A scholar doesn't necessarily visit Pāṭala.

They open ChatGPT and say:

> Translate this Kubjikā passage with parallels from contemporary Kaula sources.

ChatGPT uses:

```text
Pāṭala MCP
```

and returns citations.

At bottom:

> Sources provided by Pāṭala.

Now you don't have to acquire every researcher as a website user.

**Your corpus travels into their existing tools.**

---

# 24. Your translations can become the training/evaluation corpus

As expert-reviewed translations accumulate:

```text
Sanskrit
↕
English
+
morphology
+
term senses
+
parallels
+
review history
```

you end up possessing a uniquely valuable aligned dataset for **Tantric Sanskrit translation**.

That could eventually support:

* specialized retrieval models
* rerankers
* term-sense disambiguation
* translation quality evaluation
* perhaps specialist language models

without needing to train some giant foundational model yourself.

This is one reason the structured translation protocol matters so much.

---

# 25. A "Tantra Graph" could become a standalone research contribution

Over time:

```text
TEXT
↓ cites
TEXT

TEXT
↓ shares passage with
TEXT

SCHOLAR
↓ discusses
PASSAGE

TERM
↓ occurs in
PASSAGE

MANUSCRIPT
↓ witnesses
WORK

TRANSLATION
↓ translates
PASSAGE
```

Eventually you can visualize:

> **Show the textual formation of Trika between 850–1050.**

And dynamically construct it from evidence.

That's not merely a website feature.

That could support papers and discoveries.

---

# 26. You could eventually become a publisher

Once you have versioned reviewed translations:

> **Pāṭala Editions**

Digital edition:

```text
Kubjikāmatatantra
Translated by X
Edited by Y

Sanskrit
English
apparatus
glossary
interactive edition
```

Then optional print-on-demand book.

The canonical edition remains living online.

Book sales are secondary.

---

# 27. And potentially a small institute

This is where the brand gets genuinely interesting.

Long-term:

# Pāṭala Institute

Activities:

```text
digital preservation
critical editions
translations
research grants
fellowships
public education
lectures
conferences
study retreats
software
```

The `.org` suddenly makes perfect sense.

It begins as software and a bibliography.

It can gradually become an **institution around the corpus**.

---

# I think there are really four user classes

I'd design the foundation for these now:

| User             | Wants                                    |
| ---------------- | ---------------------------------------- |
| **Reader**       | understand Tantra                        |
| **Practitioner** | historically grounded teachings/practice |
| **Scholar**      | research, translate, edit, publish       |
| **Machine**      | structured corpus/API/MCP                |

Then later add:

| User            | Wants                               |
| --------------- | ----------------------------------- |
| **Institution** | host/manage/fund scholarly projects |

Everything we've discussed fits one of those.

## The flywheel is the most exciting part

```text
                  READERS
                     │
          subscriptions/donations
                     ↓
                TRANSLATIONS
                     ↓
SCHOLARS ───────► CORPUS ◄─────── INSTITUTIONS
   ▲                 │                  │
   │                 ↓                  │
   │              API/MCP               │
   │                 │                  │
   └──── corrections ◄──── AI ──────────┘
                     │
                     ↓
               better learning
                     │
                     ↓
                more readers
```

That's the vision I'd optimize around.

The product is **not primarily a Tantra website**.

It's a system in which:

> **preservation creates texts → texts create translations → translations create structured knowledge → structured knowledge powers research and AI → research improves the texts → public education funds and disseminates the whole cycle.**

And because you've already built the bibliography, corpus manifest, stable passage IDs, API and translation protocol foundations, this isn't "maybe one day we build some huge platform." You're already constructing the bottom layer of that system.
