# Pāṭala Content Modules — Foundation Index

*2026-08-10. The teaching layer, built per `docs/LEARNING_STRATEGY.md` (research once,
distill repeatedly) and `docs/STYLE_GUIDE.md` (house voice). Each module is a
**ConceptLesson / knowledge packet** for one school or concept, grounded in the on-disk
scholar material (Ratié, Torella, Bäumer, Biernacki, Dyczkowski). Everything bottoms out
in passages + evidence + review.

**They are modules, not site code** — nothing here edits the running site. They are the
foundation content that the site's `/learning`, `/traditions`, and `/concepts` pages can
later consume.

---

## The structure (per module)

Every module follows the three-depth model, one source:

```text
QUICK   — 3–4 min explanation (~400–600 words) — the school/concept in one idea
DEEP    — the full introduction (~1500–2500 words) — research-grade, scholar-grounded
SOURCE  — primary passages + citations + the audit trail (links to the reader)
```

Plus the packet fields: `question`, `core_claim`, `prerequisites[]`, `primary_passages[]`,
`claims[]`, `scholarly_support[]`, `key_distinctions[]`, `open_or_contested[]`,
`memory[]` (recall questions).

---

## The modules

### The recognition axis (Pratyabhijñā — the semantic control corpus)
| Module | File | Status | Scholar ground |
|--------|------|--------|----------------|
| **Recognition (the Pratyabhijñā thesis)** | `modules/recognition.md` | ✅ drafted | Ratié (*On reason and scripture*), Torella (*IPK*, *Studies in Utpaladeva*, *Utpaladeva*) |
| **Prakāśa & Vimarśa** (the reflexive pair) | `modules/prakasa-vimarsa.md` | planned | Ratié, Torella, Biernacki (*Vimarśa: Reflexivity*) |
| **Svātantrya** (creative freedom) | `modules/svatantrya.md` | planned | Ratié (*Freedom of Imagination*), Biernacki (*Svātantryavāda*) |

### The school axis (per tradition, in the atlas order)
| School | File | Status | Anchor |
|--------|------|--------|--------|
| **Trika** (the calibration layer) | `modules/school-trika.md` | ✅ drafted | Tantrāloka (Dyczkowski), Torella |
| **Krama** (cognition-sequence) | `modules/school-krama.md` | ✅ drafted | Mahānayaprakāśa, Wenta (twelve Kālīs) |
| **Kubjikā** (phonemic Western Transmission) | `modules/school-kubjika.md` | planned | Kubjikāmata, Biernacki |
| **Kaula** (the reformulation) | `modules/school-kaula.md` | planned | KJN bundle |
| **Spanda** (the pulse) | `modules/school-spanda.md` | ✅ drafted | Spandakārikā (Dyczkowski) |
| **Pratyabhijñā** (recognition) | `modules/school-pratyabhijna.md` | ✅ drafted | Torella IPK, Ratié |
| **Sarvāmnāya** (Newar synthesis) | `modules/school-sarvamnyaya.md` | planned | Newar paddhatis |

### The practice/synthetic axis (later, grown from the above)
Śaktipāta · upāyas · mantra · initiation · kula · the 36 tattvas · the kañcukas.

---

## The method (how each is produced)

1. **Read the anchor** (Ratié/Torella/Bäumer) for the concept's precise definition.
2. **Extract the claims** with their primary-passage anchors + the scholar citation.
3. **Write QUICK → DEEP → SOURCE**, following STYLE_GUIDE (IAST, retention, no anachronism).
4. **Flag open/contested** points honestly (the A/B/C stratification, contested readings).
5. Verify the module aligns with the existing `data/atlas` concepts/traditions ids.

---

*This is the foundation index. Recognition first (it anchors the whole vocabulary), then
the schools, then the practice/synthetic layer. Content is derived from the on-disk
scholarship — never free-floating.*
