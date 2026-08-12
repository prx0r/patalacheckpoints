# The Leapfrog Guide — the corpus-ladder strategy

*Imported from the R2 bucket (`essayviz-videos/leapfrogguide`). The companion strategic doc to `leapfrog_map.md`: where the map is the route, this is the engine-design — the dialect-genealogy sequence, the Rosetta-corpus principle, the lexicon-entry architecture, and the phased corpus ladder. Read alongside the map before setting batch order.*

---

Yes. The key is not to translate "Tantra" as one undifferentiated corpus. Build a translation engine around a genealogy of mutually intelligible technical dialects. Dyczkowski is unusually useful as the seed because Muktabodha says he personally selected the collection in expanding circles to represent tantric literature, and more than 380 searchable e-texts there were edited/transcribed under his supervision. The collection explicitly spans Kashmir Śaivism, Śākta, Śrīvidyā, Nātha, Pāñcarātra and other materials.

The sequence I would use is:

Trika/Bhairava → Krama/Kālīkula → Kubjikā → Sarvāmnāya/Newar syntheses → broader Kaula/Śākta → Pratyabhijñā exegesis → Śaiva Siddhānta.

That gives you a continuously expanding lexicon rather than forcing the model to relearn tantric Sanskrit each time.

1. Start with Trika/Bhairava as your linguistic calibration layer

Don't begin by trying to machine-translate the weirdest Kubjikā manuscripts. First teach the system the tantric Sanskrit Dyczkowski himself explains extensively.

Your core training/alignment corpus should therefore include things like:

Tantrāloka + Jayaratha
Tantrasāra
Mālinīvijayottaratantra
Svacchandatantra
Vijñānabhairava
Parātriṃśikā / Parātriṃśikāvivaraṇa
Netra materials where useful
Kṣemarāja
Śivasūtra commentarial literature
Pratyabhijñā terminology where Abhinava imports it

You aren't translating these because they're the biggest untranslated prize. You're using them as your Rosetta corpus.

From these you build entries such as:

vikalpa
ordinary Sanskrit: conceptual construction / alternative
Trika philosophical: determinate cognition, differentiation
ritual context: sometimes a different semantic value
associated forms: nirvikalpa, savikalpa, vikalpasaṃskāra
never automatically translate as: "thought"

And do that for thousands of terms.

The important architectural rule is:

Dyczkowski's English gloss is evidence, not the definition.

Store:

Sanskrit lemma → morphology → construction → school → textual locus → Dyczkowski gloss → other scholar glosses → your semantic representation.

That prevents your translator from turning into a Dyczkowski imitation.

2. Leap immediately into Krama/Kālīkula

This is probably the highest-value next jump.

Why? Because you retain a tremendous amount of the Trika semantic architecture—saṃvid, krama, śakti, khecarī, vyāpti, uccāra, cakra, kula, śūnya, saṃhāra, etc.—but enter a genuinely different theological/ritual universe.

And importantly, actual machine-readable material exists.

The Kramasadbhāva, for example, is available online in Sanskrit, and recent scholarship treats it together with texts such as the Yonigahvara and Devīpañcaśataka/Kālīkulapañcaśataka.

Your Krama cluster should be something like:

Kramasadbhāva
↓
Devīpañcaśataka / Kālīkulapañcaśataka
↓
Yonigahvara
↓
Kālīkulakrama / Kālīkulakramārcana materials
↓
Jayadrathayāmala

The NGMPP catalogue alone shows manuscripts catalogued under Kālīkulakrama, Kālīkulakramārcana, Kālikākulapañcaśataka, Guhyasiddhi(krama) and multiple Jayadrathayāmala witnesses.

This is where your corpus gets interesting because you can start learning semantic transformations between schools:

krama in generic Sanskrit
≠ krama in Abhinavagupta
≠ Krama as Kālī sequence/process
≠ krama in Kubjikā ritual

That's exactly the information an LLM normally obliterates.

3. Then Kubjikā — and go much deeper than the Kubjikāmata

Kubjikā should probably become your first huge specialised subcorpus.

The reason I would put it after a little Krama rather than immediately after Trika is that Kubjikā contains both familiar Śaiva/Kaula language and extremely idiosyncratic ritual/mantric systems. The preceding corpora give your model enough scaffolding to recognize what is inherited versus Kubjikā-specific.

Begin with the Kubjikāmatatantra because you already have a clean electronic Sanskrit text based on the Goudriaan/Schoterman edition.

Then move outward:

Kubjikāmatatantra
→ Ṣaṭsāhasrasaṃhitā
→ Śrīmatottara
→ Ciñciṇīmatasārasamuccaya
→ Manthānabhairavatantra corpus
→ Kubjikā paddhatis and Nepalese ritual literature.

This gets extraordinarily good for your project.

For example, Śrīmatottara is explicitly an expanded development of Kubjikāmatatantra material, and NGMPP records both an incomplete palm-leaf witness and a 339-folio complete Newari-script manuscript, NAK 2/214.

And notice what happens lexically. The Tantric Studies dictionary project's sample page cross-references one technical phonemic sequence across:

Mālinīvijayottara
Tantrāloka
Tantrasadbhāva
Kubjikāmata
Triśirobhairava
Ṣaṭsāhasrasaṃhitā
Śrīmatottara
Kulālikāmnāyaratnoddyota

That's almost exactly the cross-tradition graph you want to computationally reconstruct.

You could literally model:

technical concept
      │
      ├── MVT
      ├── Tantrasadbhāva
      ├── Tantrāloka/Jayaratha
      ├── Kubjikāmata
      ├── Ṣaṭsāhasra
      ├── Śrīmatottara
      └── later Kubjikā exegesis

and ask how its meaning mutates through the network.

That becomes more valuable than "an AI Sanskrit translator."

4. The killer bridge corpus: Ciñciṇīmatasārasamuccaya

I would flag this one especially.

It isn't merely another obscure Kubjikā text. It appears to belong to a historical phase in which Trika, Krama and Kubjikā were being conceptualised as complementary tantric transmissions rather than isolated systems. Scholarship on the corpus describes precisely this movement toward a unified multi-āmnāya model.

That makes the Ciñciṇīmatasārasamuccaya almost tailor-made for your project.

Think:

Trika vocabulary → Krama vocabulary → Kubjikā vocabulary → text that knows all three.

At that point your translation system can start discovering equivalence mappings rather than merely inheriting them.

It is also known from manuscript/online transcription circulation; references identify NAK manuscript 1-245 / NGMPP A 1177/7, although the surviving/transcribed material requires textual-critical care.

I'd put this very high on your eventual translation list.

5. Then attack the Jayadrathayāmala universe

This is where the scope becomes enormous.

The Jayadrathayāmala connects you into a sprawling Bhairava/Śākta world and intersects especially productively with Kālī/vidyāpīṭha developments. NGMPP records several separate witnesses/catalogue entries.

But I wouldn't start here.

A big yāmala is exactly where a naive LLM will confidently hallucinate the meaning of:

deity names,
mantra terminology,
coded ritual language,
obscure verbal forms,
corrupted readings,
lists,
technical classifications.

After you've learned Trika + Krama + Kubjikā, suddenly the system can identify:

this expression also occurs in Kramasadbhāva;
this nyāsa pattern resembles Śrīmatottara;
Abhinava cites a cognate formulation;
this rare term occurs five times in Kubjikā literature.

Then you're doing philology.

6. Then go into the Nepalese Sarvāmnāya world

This might eventually become the most fascinating part of the project.

The later Newar Śākta tradition preserved and recombined streams including Trika, Krama and Kubjikā into multi-āmnāya systems. Recent scholarship is actively working with unpublished Newar ritual manuscripts of this kind.

You'd encounter things like:

Siddhalakṣmī
Guhyakālī
Kubjikā
Kālīkrama
Tripurasundarī
multi-āmnāya ritual systems
paddhatis
pratiṣṭhā
nyāsa systems
ritual digests

This is perfect late-stage training data because it tests whether your semantic model can recognise several traditions being deliberately combined.

Muktabodha is especially important here because many of the rare manuscripts Dyczkowski selected came from Nepal, and their staff were specifically trained by him to transcribe Newari-script manuscripts.

7. Pratyabhijñā should run in parallel, not come afterward

I'd actually have two corpora growing simultaneously:

SCRIPTURAL / RITUAL                    PHILOSOPHICAL / EXEGETICAL

Bhairava Tantra                        Utpaladeva
        ↓                                  ↓
Trika                                Abhinavagupta
        ↓                                  ↓
Krama                               Kṣemarāja
        ↓                                  ↓
Kubjikā                         later Śaiva philosophy
        ↓
Sarvāmnāya

Because philosophical Sanskrit teaches the machine to distinguish propositions much more cleanly than mantra/ritual Sanskrit can.

Utpaladeva is particularly useful because the Pratyabhijñā corpus repeatedly gives you:

claim → objection → distinction → counterexample → conclusion.

That is phenomenal alignment material.

You eventually want your lexicon to know that something like vimarśa can be encountered in philosophical argument and in tantric theological discourse without flattening those uses.

And Muktabodha itself singled out the Īśvarapratyabhijñākārikā among works it prepared/published, showing how closely the philosophical corpus sits alongside its tantric archive.

8. Śaiva Siddhānta is the huge expansion pack

This sounds less exciting for your particular interests, but eventually it's indispensable.

Why?

Because a massive amount of the ritual ontology and technical vocabulary of later nondual Śaivism only becomes intelligible against the wider Mantramārga.

And the digital material is enormous: Muktabodha's collaboration with the French Institute of Pondicherry digitised more than 2,000 predominantly Śaiva Siddhānta texts, from an IFP collection containing thousands of manuscripts.

Once your translator understands:

mantra
dīkṣā
adhvan
kalā
tattva
bhuvana
nyāsa
pratiṣṭhā
śuddhi
pāśa
mala
adhikāra
śakti
mantra-body constructions

across Siddhānta and Bhairava sources, its translations of Abhinava become substantially more historically informed.

So I'd do Siddhānta after your exciting corpus, rather than forcing yourself through it first.

Your practical corpus ladder

If this were my project architecture, I'd therefore do:

Phase A — high-quality semantic seed

Tantrāloka + Dyczkowski → Tantrasāra → Vijñānabhairava → Mālinīvijayottara → Pratyabhijñā

Create perhaps 3,000–5,000 controlled technical entries.

Phase B — first generalization test

Kramasadbhāva → Devīpañcaśataka → related Krama fragments

Now deliberately identify where your Trika glossary fails.

Phase C — Kubjikā

Kubjikāmata → Ṣaṭsāhasra → Śrīmatottara → Manthānabhairava

This could easily become your flagship translated corpus.

Phase D — bridge texts

Ciñciṇīmatasārasamuccaya → other multi-āmnāya texts

Now learn cross-school equivalences.

Phase E — difficult source literature

Jayadrathayāmala + related Vidyāpīṭha/Bhairava materials

Phase F — living Nepalese textual ecology

Kālī/Kubjikā/Siddhalakṣmī/Guhyakālī/Newar paddhatis

Phase G — expand backward/outward

Śaiva Siddhānta → other Mantramārga → Śrīvidyā/Tripurā → Nātha/Kaula

That's a coherent intellectual expansion rather than "translate everything Sanskrit."

And technically, I would not train it as ordinary machine translation

Make every translation produce something like:

SOURCE
ātmā manaś ca mantraś ca śivaḥ śaktis tathaiva ca

PADACCHEDA
ātmā | manaḥ | ca | mantraḥ | ca | śivaḥ | śaktiḥ | tathā eva | ca

MORPHOLOGY
ātmā — nom.sg.m.
manaḥ — nom.sg.n.
...

PARALLELS
Kubjikāmata x.x
Śrīmatottara x.x
Tantrāloka x.x
...

TECHNICAL TERMS
mantra
śakti
śiva

LITERAL
Self, mind, mantra, Śiva and likewise Śakti...

SEMANTIC TRANSLATION
...

UNCERTAINTIES
[śakti syntactically ambiguous?]
[ekībhāva supplied by following pāda]

COMMENTARY
...

The Kubjikāmata itself gives precisely the sort of compact technical formulations that reward this approach—for example passages integrating ātman, mind, mantra, Śiva and Śakti into a single ritual-yogic structure. The electronic edition gives you stable verse identifiers, which is ideal for constructing this kind of retrieval system.

And then never let the model resolve an obscure technical term from its pretrained intuition alone.

Retrieve:

occurrences in same text;
occurrences elsewhere in same tradition;
Dyczkowski;
Tantrikābhidhānakośa;
parallel passages;
historical dictionaries;
commentaries;
neighbouring traditions.

Then translate.

That's how you get something closer to a computational tantric philologist rather than Sanskrit-flavoured ChatGPT.

The four traditions I'd prioritise most

If your aim is interesting + undertranslated + online-accessible + closely connected to Dyczkowski, my ranking is:

1. Krama/Kālīkula — fastest intellectual payoff.
2. Kubjikā — deepest coherent untranslated/undertranslated ecosystem.
3. Multi-āmnāya/Newar Śākta literature — incredibly rich and comparatively unexplored.
4. Jayadrathayāmala/Vidyāpīṭha/Bhairava corpus — harder, but enormous scholarly value.

And the really exciting possibility is that after enough text you can stop thinking of the project as translation.

You can construct a diachronic tantric semantic graph:

Where does khecarī first mean X?
How does krama change between Kālīkula and Kubjikā?
Where does anuttara acquire Abhinava's philosophical loading?
Which Kubjikā passages share formulas with early Trika?
Which passages in Tantrāloka are essentially transformed scriptural language rather than Abhinava's innovations?

That is a genuinely powerful research instrument, and Dyczkowski → Krama → Kubjikā → Sarvāmnāya is probably the best route to building it.
