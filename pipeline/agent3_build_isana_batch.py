#!/usr/bin/env python3
"""Build the RAW-L0 batch for isanasivagurudevapaddhati v1-v100 (A3 agent output).

Passage order and source_sha256 are taken from
data/corpus/downloads/translations/isanasivagurudevapaddhati.jsonl
(which matches the prompt's VERSE blocks exactly); the TOKENS arrays are the
Vidyut-segmented token lists from the prompt, embedded here in order.
"""
import json

OUT = "/root/projects/patala/docs/corpus/translations/isanasivagurudevapaddhati_p1-p2_v1-100_a3_raw-l0_20260813.json"

# passage_idx (0-based) -> token list (echoed from the prompt)
TOKENS = {
0: ["dūrgāṃ","ca","durgārtiharāṃ","viriñcaṃ","lakṣmīṃ","ca","lakṣmīśamapi","prapadye"],
1: ["mahāmahimnā","mihirānivoditāṃstamomahāmohaharān","nato","smyaham"],
2: ["yāvatsāmarthyamālocya","kariṣye","tantrapaddhatim"],
3: ["ṛddhairvidhānamantrārthairvedyāṃ","śrutimivāparām"],
4: ["citrāṃ","bahugu","āṃ","viṣ","oḥ","śayyāṃ","bhogavatīmiva"],
5: ["sevyāṃ","kāmijanasyeṣṭāṃ","lalitāṃ","pramadāmiva"],
6: ["mantrabimbauṣadhidhyānairvidyāṃ","sañjīvinīmiva"],
7: ["utsādamāra","opāyairda","ḍanītimivāparām"],
8: ["satyabhāmāsamāśliṣṭāṃ","yathā","mūrtiṃ","muradviṣaḥ"],
9: ["kṛtatretādikalpaiśca","śaradaṃ","brahma","o","yathā"],
10: ["yantrairdūrīkṛtānarthāṃ","durgabhūmimivāparām"],
11: ["kaliprasaṅgakaṭukāṃ","kālasyeha","gatiryathā"],
12: ["caturyugakramāyattāṃ","vaidhasīmiva","kalpanām"],
13: ["mūrtiṃ","vināyakasyeva","gajavaktrāṃ","narākṛtim"],
14: ["tadvidāṃ","pratyayāvedyāṃ","muktidāṃ","śaktimaiśvarīm"],
15: ["mokṣaprasādhanīṃ","tattatkramāvedyāṃ","trayīmiva"],
16: ["sacchandomunidigbandhāḥ","sadhyānāḥ","saprayojanāḥ"],
17: ["bījāni","bījamantrāśca","mantrā","mālākhyamantrakāḥ"],
18: ["bījamantrā","daśār","ādho","mantrāḥ","syurviṃśateradhaḥ"],
19: ["prāye","a","bālye","bījāni","siddhiṃ","yacchanti","bhūyasīm"],
20: ["vārddhake","pi","ca","sidhyanti","mālāmantrāḥ","sadaiva","hi"],
21: ["mananatrā","adharmitvaṃ","vācake","daivatasya","tu"],
22: ["mantrarūpā","hi","tacchaktirmananatrā","adharmi","ī"],
23: ["vācyavācakayoraikyamadhigamya","gurāvapi"],
24: ["lipirvai","sarvamantrā","āṃ","śabdānāṃ","caiva","mātṛkā"],
25: ["nirvikalpātmakaṃ","bra","hma","yannityānandavigraham"],
26: ["susūkṣmaṃ","cirddhanaṃ","vyāpi","sarvagaṃ","tada","ora","u"],
27: ["ādisargamukhe","jñānacikīrṣāyatnadhāra","āt"],
28: ["sattvaṃ","rajastamaścaitacchuklaraktāsitaprabham"],
29: ["sā","śaktirbindutāmeti","binduḥ","so","pi","tridhā","bhavet"],
30: ["avyaktāduditaṃ","tattvaṃ","mahānnāma","tribhedakam"],
31: ["vaikārikastaijasaśca","bhūtādiriti","cāparaḥ"],
32: ["muktidaṃ","paramaṃ","divyaṃ","sarvasiddhipradāyakam"],
33: ["hrasvā","brahma","samākhyātā","dīrghā","hyaṅgāni","ṣa","mukha"],
34: ["jāyate","bindusaṃkṣobhādanantasyārthasiddhaye"],
35: ["śaktirnādo","mahāmāyā","vyometi","ca","caturvidham"],
36: ["vaikharī","madhyamā","caiva","paśyantī","cāpi","sūkṣmayā"],
37: ["sūkṣmā","ku","ḍalinīmadhye","jyotirmātrātya","īyasī"],
38: ["svayaṃ","prakāśā","paśyantī","suṣumnāmāśritā","bhavet"],
39: ["antaḥsañjalpamātrā","syādavibhaktordhvagāminī"],
40: ["jihvāmūloṣṭhaniṣṭyūtā","kṛtavar","aparigrahā"],
41: ["hakāraḥ","savikāro","tha","rephe","a","samayujyata"],
42: ["śaktibījaṃ","hi","tadyogāt","prapañcotpattikāra","am"],
43: ["śliṣṭoccāritayoḥ","śābdaṃ","rūpaṃ","tadbījamīritam"],
44: ["īkārastu","bhavenmāyā","bindurīśvara","ucyate"],
45: ["hakāro","vyaktimāpanno","hārdaghoṣavivakṣitaḥ"],
46: ["ūkārāntānyakārādīnyakṣarā","i","ṣaḍasya","tu"],
47: ["īkārabhedatastvāsannekārādyakṣarā","i","ṣaṭ"],
48: ["śaktyaṅgatvāt","kalāste","syuramṛtāṃśukalātmakāḥ"],
49: ["dīrghasvarā","visargāntāḥ","strīliṅgāḥ","somarūpi","aḥ"],
50: ["svarā","āmudayādyaṃ","tu","purastādiha","likhyate"],
51: ["vyomnaḥ","sparśagu","o","vāyuḥ","sparśākhyāḥ","kādayo","bhavan"],
52: ["yādyakṣaracatuṣkaṃ","tu","vāyvagnikṣmāmbhasāṃ","tanuḥ"],
53: ["śeṣāstu","vyāpakāḥ","śādyāḥ","sāgnīṣomāḥ","svaraspṛśaḥ"],
54: ["kādayaḥ","pañcaviṃśār","ā","yādayaḥ","śādayastathā"],
55: ["akārādisvarairyuktahalāṃ","yogānmitho","pi","ca"],
56: ["saiva","śaktirdvidhā","bhūtā","tāro","vāgbhavamityapi"],
57: ["tārākhyaḥ","pra","avo","hyeṣa","śabdabrahmātmako","mataḥ"],
58: ["viśvavāgbhūtidaṃ","tattu","vāgīśvaryāstanurbhavet"],
59: ["śaktibījaṃ","tathā","tāro","vāgbhavaṃ","ca","tataḥ","param"],
60: ["tadbhedajāśca","yā","vāco","deśabhājā","vilakṣa","āḥ"],
61: ["ākāśādīni","bhūtāni","tanmātrā","īndriyā","i","ca"],
62: ["bahunā","kiṃ","pralāpena","yaḥ","śabdārthātmako","khilaḥ"],
63: ["asyāṃ","tu","mātṛkākhyāyāṃ","lipitvaṃ","likhyate","yataḥ"],
64: ["ar","atvamamṛtātmatvādar","o","mbhaḥ","kathyate","yataḥ"],
65: ["upādānāni","viśvātmamātṛkāyāstu","pañca","vai"],
66: ["ṭatavargau","tathā","pādau","pārśvayugmaṃ","paphau","matau"],
67: ["tvagasṛṅmāṃsamedosthimajjāśuklāni","yādayaḥ"],
68: ["sphūrtiḥ","kṣakāraḥ","sakrodho","viśvalokamayī","tanuḥ"],
69: ["brahmādistambaparyantaṃ","mātṛkāyāṃ","vyavasthitam"],
70: ["avargādudgataḥ","sūryaḥ","kavargādapi","bhūsutaḥ"],
71: ["pavargācca","śaniścandro","yavargādabhavad","vibhuḥ"],
72: ["mātṛkākṣarasambhedāt","kathyante","parato","tra","vai"],
73: ["samudgatāstathā","rudraśaktayastatprasaṃkhyayā"],
74: ["oṣadhyaścāpi","pañcāśadaṣṭatriṃśat","kalāstathā"],
75: ["evaṃ","hi","mātṛkotpattirāgamoktā","pradarśitā"],
76: ["atroddhriyante","bījāni","bījamantrāḥ","samantrakāḥ"],
77: ["tataḥ","paraṃ","yathāpāṭhaṃ","vijñeyā","nipu","aiḥ","sphuṭam"],
78: ["yathāvadatra","likhyante","bhagavacchabdasaṃyutāḥ"],
79: ["da","ḍārdhendurbhaved","binduḥ","sargo","bindudvaye","mataḥ"],
80: ["viṣakālau","makāraḥ","syād","dhātavo","yādayo","matāḥ"],
81: ["khaḥ","prā","abhuvaneśākhyo","hakāraḥ","śivasaṃjñitaḥ"],
82: ["paphabāśca","bhamakṣāśca","vyatyayaṃ","te","trayastrayaḥ"],
83: ["svareṣu","vyatyayo","neṣṭastadvad","yuktākṣareṣvapi"],
84: ["tattadakṣaravijñaptyai","saṅketāya","bhavanti","hi"],
85: ["yathāsaṅkhyaṃ","tathā","vidyāt","svarāḥ","sapta","diśo","daśa"],
86: ["vedāścatvāra","eva","syustrayo","rāmāśtrayo","gnayaḥ"],
87: ["uktātyuktā","tathā","madhyā","pratiṣṭhā","supratiṣṭhitā"],
88: ["tṛṣṭup","ca","jagatī","tadvat","tato","tijagatī","matā"],
89: ["dhṛtiścātidhṛtiścaiva","kṛtiḥ","prakṛtirākṛtiḥ"],
90: ["etāsāṃ","chandasāṃ","saṃkhyā","kvacidatra","vidhīyate"],
91: ["tathā","ṣaṭtriṃśadeva","syuḥ","śaive","tattvāni","saṃkhyayā"],
92: ["navabhirnavapañcāṣṭavar","aiḥ","saṃkhyātra","vā","bhavet"],
93: ["sukhāvabodho","hyarthānāṃ","bhavatyeveṣṭasiddhaye"],
94: ["tacchāktaṃ","pra","avākhyabījamakhilaṃ","nyagrodhabījaṃ","viduḥ"],
95: ["iti","śrīmadīśānaśivagurudevamiśraviracite","tantrasārapaddhatau","vastunirdeśamātṛkopapattinir","ayo","nāma","prathamaḥ","paṭalaḥ"],
96: ["aśvīśo","bhārabhūtiśca","tithīśaḥ","sthā","uko","haraḥ"],
97: ["akrūraśca","mahāsenaḥ","ṣoḍaśaite","svareśvarāḥ"],
98: ["ekarudraśca","kūrmaikanetrau","ca","caturānanaḥ"],
99: ["ardhanārīśvaraścomākāntaścāṣaḍiḍi","ḍinau"],
}

# gloss dicts per passage index
G = {}
G[0] = {
 "dūrgāṃ": "Durgā (the goddess), acc. sg. f.",
 "ca": "and",
 "durgārtiharāṃ": "remover of the affliction (ārti) of those in difficulty (durgā) — durgā-ārti-hara, acc. sg. f.",
 "viriñcaṃ": "Viriñca (Brahmā), acc. sg. m.",
 "lakṣmīṃ": "Lakṣmī, acc. sg. f.",
 "ca": "and",
 "lakṣmīśamapi": "also the Lord of Lakṣmī (lakṣmī-īśa = Viṣṇu) + api, acc. sg. m.",
 "prapadye": "I take refuge in / I resort to (1sg. pres. middle)",
}
G[0]["close"] = "I take refuge in Durgā, who removes the affliction of those in distress, and in Viriñca, and in Lakṣmī, and also in Lakṣmī's Lord."
G[0]["uncertain"] = []

G[1] = {
 "mahāmahimnā": "by great majesty (mahā-mahiman), instr. sg.",
 "mihirānivoditāṃstamomahāmohaharān": "risen like suns, dispelling darkness and great delusion (mihira-iva-udita + tamas-mahā-moha-hara), acc. pl. m.",
 "nato": "bowed, prostrated (nata, ppp.), nom. sg. m.",
 "smyaham": "asmi + aham: 'I am — I' (with nataḥ: 'I bow')",
}
G[1]["close"] = "By their great majesty, risen like suns, dispelling darkness and the great delusion — I bow to them."
G[1]["uncertain"] = []

G[2] = {
 "yāvatsāmarthyamālocya": "having considered (ālocya) the capacity (sāmarthya) to the extent (yāvat) [possible], gerund",
 "kariṣye": "I will make / compose (1sg. fut.)",
 "tantrapaddhatim": "the Tantrapaddhati (this ritual manual), acc. sg. f.",
}
G[2]["close"] = "Having considered my capacity as far as it goes, I will compose the Tantrapaddhati."
G[2]["uncertain"] = []

G[3] = {
 "ṛddhairvidhānamantrārthairvedyāṃ": "to be known (vedyā) through successful (ṛddha) ritual prescriptions (vidhāna) and mantra-meanings (mantr-artha), acc. sg. f. + instr. pl.",
 "śrutimivāparām": "like (iva) another (aparā) Śruti (Veda), acc. sg. f.",
}
G[3]["close"] = "(It shall be) like another Śruti, to be known through efficacious prescriptions and mantra-meanings."
G[3]["uncertain"] = []

G[4] = {
 "citrāṃ": "wonderful, variegated, acc. sg. f.",
 "bahugu": "many- (bahuguṇa-, 'having many qualities') [fragment of bahuguṇāṃ]",
 "āṃ": "f. acc. sg. ending (-ṇāṃ) [fragment of bahuguṇāṃ]",
 "viṣ": "Viṣṇu- [fragment of viṣṇoḥ]",
 "oḥ": "gen. sg. ending (-ṇoḥ) [fragment of viṣṇoḥ]",
 "śayyāṃ": "couch / bed, acc. sg. f.",
 "bhogavatīmiva": "like the serpent-couch (bhogavatī, i.e. Śeṣa) + iva, acc. sg. f.",
}
G[4]["close"] = "Like the wonderful, many-qualitied serpent-couch (Śeṣa) of Viṣṇu."
G[4]["uncertain"] = []

G[5] = {
 "sevyāṃ": "to be served / waited upon, acc. sg. f.",
 "kāmijanasyeṣṭāṃ": "desired (iṣṭā) by people of passion (kāmi-janasya), acc. sg. f.",
 "lalitāṃ": "lovely, graceful, acc. sg. f.",
 "pramadāmiva": "like a young woman (pramadā) + iva, acc. sg. f.",
}
G[5]["close"] = "Like a lovely young woman, to be served, desired by men of passion."
G[5]["uncertain"] = []

G[6] = {
 "mantrabimbauṣadhidhyānairvidyāṃ": "the lore (vidyā) [attained] through mantra, image, herb, and meditation (mantra-bimba-oṣadhi-dhyāna), acc. sg. f. + instr. pl.",
 "sañjīvinīmiva": "like the reviving (sañjīvinī, the life-restoring science) + iva, acc. sg. f.",
}
G[6]["close"] = "Like the reviving lore (sañjīvinī-vidyā), (attained) through mantras, images, herbs, and meditations."
G[6]["uncertain"] = []

G[7] = {
 "utsādamāra": "uprooting (utsāda) and killing (māraṇa) [fragment of utsādamāraṇopāyair]",
 "opāyairda": "by means (upāyaiḥ) [fragment of utsādamāraṇopāyair]",
 "ḍanītimivāparām": "like another treatise on statecraft (daṇḍa-nītim iva aparām) [fragment]",
}
G[7]["close"] = "Like another treatise on polity (daṇḍanīti), (equipped) with means of suppression and execution."
G[7]["uncertain"] = []

G[8] = {
 "satyabhāmāsamāśliṣṭāṃ": "embraced (samāśliṣṭā) by Satyabhāmā, acc. sg. f.",
 "yathā": "as, just as",
 "mūrtiṃ": "the form / image, acc. sg. f.",
 "muradviṣaḥ": "of the enemy of Mura (mura-dviṣ = Viṣṇu/Kṛṣṇa), gen. sg.",
}
G[8]["close"] = "Just as the form of Mura's foe (Kṛṣṇa) embraced by Satyabhāmā."
G[8]["uncertain"] = []

G[9] = {
 "kṛtatretādikalpaiśca": "and by kalpas beginning with the Kṛta and Tretā (ages) (kṛta-tretā-ādi-kalpa + ca), instr. pl.",
 "śaradaṃ": "autumn, acc. sg. f.",
 "brahma": "Brahmā (brahman, gen. 'brahmaṇaḥ') [fragment of brahmaṇo]",
 "o": "gen. sg. ending (-ṇo) [fragment of brahmaṇo]",
 "yathā": "as, just as",
}
G[9]["close"] = "Just as the autumns of Brahmā, (counted) by kalpas beginning with the Kṛta and Tretā (ages)."
G[9]["uncertain"] = []

G[10] = {
 "yantrairdūrīkṛtānarthāṃ": "whose misfortunes (anartha) have been removed (dūrīkṛta) by yantras, acc. sg. f.",
 "durgabhūmimivāparām": "like (iva) another (aparā) fortress-land (durga-bhūmi), acc. sg. f.",
}
G[10]["close"] = "Like a fortress-land whose dangers have been driven away by yantras."
G[10]["uncertain"] = []

G[11] = {
 "kaliprasaṅgakaṭukāṃ": "bitter (kaṭukā) through contact (prasaṅga) with the Kali (age), acc. sg. f.",
 "kālasyeha": "of Time here (kālasya + iha), gen. sg.",
 "gatiryathā": "as the course (gatiḥ) + yathā, acc./nom. sg. f.",
}
G[11]["close"] = "Like the course of Time here, made bitter by contact with the Kali age."
G[11]["uncertain"] = []

G[12] = {
 "caturyugakramāyattāṃ": "dependent (āyattā) on the sequence (krama, order) of the four ages (catur-yuga), acc. sg. f.",
 "vaidhasīmiva": "like that of Vidhi/Brahmā (vaidhasī) + iva, acc. sg. f.",
 "kalpanām": "the creation / cosmic ordering, acc. sg. f.",
}
G[12]["close"] = "Like the creation of Brahmā, dependent on the sequence of the four ages."
G[12]["uncertain"] = []

G[13] = {
 "mūrtiṃ": "the form / image, acc. sg. f.",
 "vināyakasyeva": "as of Vināyaka (Gaṇeśa) (vināyakasya + iva), gen. sg.",
 "gajavaktrāṃ": "elephant-faced (gaja-vaktra), acc. sg. f.",
 "narākṛtim": "having a human body (nara-ākṛti), acc. sg. f.",
}
G[13]["close"] = "Like the image of Vināyaka — elephant-faced, of human form."
G[13]["uncertain"] = []

G[14] = {
 "tadvidāṃ": "of those who know that (tad-vid), gen. pl.",
 "pratyayāvedyāṃ": "to be known with certainty (pratyaya-āvedya), acc. sg. f.",
 "muktidāṃ": "granting liberation (mukti-da), acc. sg. f.",
 "śaktimaiśvarīm": "the sovereign Śakti (aiśvarī śakti, power of the Lord), acc. sg. f.",
}
G[14]["close"] = "The sovereign Śakti, liberation-granting, to be known with certainty by those who know it."
G[14]["uncertain"] = []

G[15] = {
 "mokṣaprasādhanīṃ": "accomplishing liberation (mokṣa-prasādhana), acc. sg. f.",
 "tattatkramāvedyāṃ": "to be known through the sequence (krama, order) of this and that (tat-tat, the various procedures), acc. sg. f.",
 "trayīmiva": "like the triple Veda (trayī) + iva, acc. sg. f.",
}
G[15]["close"] = "Like the triple Veda, which accomplishes liberation and is to be known through the sequence of its various (procedures)."
G[15]["uncertain"] = []

G[16] = {
 "sacchandomunidigbandhāḥ": "endowed with true meters (sat-chandas), bounded by the sages' directions (muni-dig-bandha), nom. pl. m.",
 "sadhyānāḥ": "together with meditation (sa-dhyāna), nom. pl. m.",
 "saprayojanāḥ": "with purpose / accompanied by their application (sa-prayojana), nom. pl. m.",
}
G[16]["close"] = "Possessing true meters, bounded by the sages' directions, accompanied by meditation, and purposeful."
G[16]["uncertain"] = []

G[17] = {
 "bījāni": "the seed-syllables (bīja), nom. pl. n.",
 "bījamantrāśca": "and the bīja-mantras (bīja-mantra + ca), nom. pl. m.",
 "mantrā": "the mantras, nom. pl. m.",
 "mālākhyamantrakāḥ": "mantras called mālā ('garland') (mālā-ākhya-mantraka), nom. pl. m.",
}
G[17]["close"] = "The bījas, the bīja-mantras, and the mantras known as mālā-mantras."
G[17]["uncertain"] = []

G[18] = {
 "bījamantrā": "the bīja-mantras, nom. pl. m.",
 "daśār": "ten syllables (daśa-arṇa-) [fragment of daśārṇādhaḥ]",
 "ādho": "below (adhaḥ) [fragment of daśārṇādhaḥ]",
 "mantrāḥ": "the mantras, nom. pl. m.",
 "syurviṃśateradhaḥ": "would be (syuḥ) below twenty (viṃśateḥ adhaḥ)",
}
G[18]["close"] = "Bīja-mantras (are those) below ten syllables; (full) mantras would be those below twenty."
G[18]["uncertain"] = []

G[19] = {
 "prāye": "for the most part (prāyeṇa) [fragment]",
 "a": "instr. sg. ending -ṇa [fragment of prāyeṇa]",
 "bālye": "in childhood, loc. sg.",
 "bījāni": "the seed-syllables, nom. pl. n.",
 "siddhiṃ": "success, accomplishment, acc. sg. f.",
 "yacchanti": "they give / yield (3pl. pres.)",
 "bhūyasīm": "abundant, greater, acc. sg. f.",
}
G[19]["close"] = "For the most part, the bījas yield abundant success in childhood."
G[19]["uncertain"] = []

G[20] = {
 "vārddhake": "in old age, loc. sg. n.",
 "pi": "even (api) [fragment of 'pi]",
 "ca": "and",
 "sidhyanti": "they succeed / are accomplished (3pl. pres.)",
 "mālāmantrāḥ": "the mālā-mantras, nom. pl. m.",
 "sadaiva": "always (sadā eva)",
 "hi": "indeed, for",
}
G[20]["close"] = "And even in old age, the mālā-mantras always succeed."
G[20]["uncertain"] = []

G[21] = {
 "mananatrā": "thinking and protecting (manana-trāṇa-) [fragment of mananatrāṇadharmitvaṃ]",
 "adharmitvaṃ": "the state of possessing the property (-dharmitva) [fragment of mananatrāṇadharmitvaṃ]",
 "vācake": "in the signifier (vācaka, i.e. the mantra), loc. sg.",
 "daivatasya": "of the deity, gen. sg.",
 "tu": "but, however",
}
G[21]["close"] = "But the property of thinking-and-protecting belongs to the signifier (the mantra) of the deity."
G[21]["uncertain"] = []

G[22] = {
 "mantrarūpā": "having the form of mantra (mantra-rūpā), nom. sg. f.",
 "hi": "for, indeed",
 "tacchaktirmananatrā": "that Śakti, (consisting of) thinking-and-protecting (tac-chaktiḥ manana-trāṇa-) [fragment]",
 "adharmi": "possessed of the property (-dharmiṇī) [fragment]",
 "ī": "fem. ending -ī [fragment]",
}
G[22]["close"] = "For that Śakti, having the form of a mantra, is possessed of thinking-and-protecting."
G[22]["uncertain"] = []

G[23] = {
 "vācyavācakayoraikyamadhigamya": "having understood (adhigamya) the unity (aikya) of the signified and the signifier (vācya-vācakayoḥ), gerund",
 "gurāvapi": "even in the guru (gurau + api), loc. sg.",
}
G[23]["close"] = "Having grasped the unity of the signified and the signifier, even in the guru..."
G[23]["uncertain"] = []

G[24] = {
 "lipirvai": "indeed (vai) the script (lipiḥ)",
 "sarvamantrā": "of all mantras (sarva-mantrāṇāṃ) [fragment]",
 "āṃ": "gen. pl. ending (-ṇāṃ) [fragment of sarvamantrāṇāṃ]",
 "śabdānāṃ": "of sounds / words, gen. pl. m.",
 "caiva": "and also (ca eva)",
 "mātṛkā": "the Mātṛkā (the phonemic Mother-matrix, power embodied in letters), nom. sg. f.",
}
G[24]["close"] = "Indeed, the script (lipi) is the Mātṛkā of all mantras and of all sounds."
G[24]["uncertain"] = []

G[25] = {
 "nirvikalpātmakaṃ": "whose nature is free from conceptual construction (nirvikalpa-ātmaka), acc. sg. n.",
 "bra": "bra(hma), 'Brahman' [fragment — source reads bra(hma)]",
 "hma": "(-hma) [fragment]",
 "yannityānandavigraham": "which (yat) has eternal bliss as its body (nitya-ānanda-vigraha), acc. sg. n.",
}
G[25]["close"] = "Brahman, whose nature is without conceptual construction, which has eternal bliss as its body."
G[25]["uncertain"] = []

G[26] = {
 "susūkṣmaṃ": "exceedingly subtle (su-sūkṣma), acc. sg. n.",
 "cirddhanaṃ": "whose treasure is consciousness (cid-dhana; source reads cirddhana), acc. sg. n.",
 "vyāpi": "pervasive, acc. sg. n.",
 "sarvagaṃ": "going everywhere, all-pervading (sarva-ga), acc. sg. n.",
 "tada": "that (tad) [fragment of tadaṇoraṇu]",
 "ora": "than the subtle (aṇoḥ, gen. of comparison) [fragment of tadaṇoraṇu]",
 "u": "the subtle (aṇu) [fragment of tadaṇoraṇu]",
}
G[26]["close"] = "Exceedingly subtle, having consciousness as its treasure, pervasive, all-pervading — that (is) subtler than the subtle."
G[26]["uncertain"] = ["cirddhanaṃ"]

G[27] = {
 "ādisargamukhe": "at the beginning (mukhe) of the first creation (ādi-sarga), loc. sg.",
 "jñānacikīrṣāyatnadhāra": "the sustaining (dhāraṇa) of knowledge, will-to-make, and effort (jñāna-cikīrṣā-yatna-) [fragment of jñānacikīrṣāyatnadhāraṇāt]",
 "āt": "abl. sg. ending (-ṇāt) [fragment]",
}
G[27]["close"] = "From the sustaining of knowledge, will, and effort at the outset of the first creation..."
G[27]["uncertain"] = []

G[28] = {
 "sattvaṃ": "sattva (the principle of goodness/purity), nom. sg. n.",
 "rajastamaścaitacchuklaraktāsitaprabham": "and rajas and tamas — this (etat), having white, red, and black radiance (rajas-tamas + ca + etat + śukla-rakta-asita-prabham), nom. sg. n.",
}
G[28]["close"] = "Sattva, rajas, and tamas — this (triad) with white, red, and black radiance."
G[28]["uncertain"] = []

G[29] = {
 "sā": "that, nom. sg. f.",
 "śaktirbindutāmeti": "the Śakti attains the state of a bindu (śaktiḥ bindu-tām eti)",
 "binduḥ": "the bindu (the seed-point), nom. sg. m.",
 "so": "that (saḥ), nom. sg. m.",
 "pi": "too (api)",
 "tridhā": "threefold (adv.)",
 "bhavet": "would be / becomes (3sg. opt.)",
}
G[29]["close"] = "That Śakti attains the state of a bindu; that bindu, too, becomes threefold."
G[29]["uncertain"] = []

G[30] = {
 "avyaktāduditaṃ": "arisen (udita) from the Unmanifest (avyaktāt), acc. sg. n.",
 "tattvaṃ": "the principle (tattva), acc. sg. n.",
 "mahānnāma": "named the Great (mahān nāma), acc. sg. n.",
 "tribhedakam": "having three divisions (tri-bhedaka), acc. sg. n.",
}
G[30]["close"] = "From the Unmanifest arose the principle named the Great (Mahat), which has three divisions."
G[30]["uncertain"] = []

G[31] = {
 "vaikārikastaijasaśca": "the Vaikārika and the Taijasa (vaikārikaḥ taijasaḥ ca, first two forms of ahaṃkāra), nom. sg. m.",
 "bhūtādiriti": "and the Bhūtādi — thus (bhūtādi iti), nom. sg. m.",
 "cāparaḥ": "and the other (ca aparaḥ, the third), nom. sg. m.",
}
G[31]["close"] = "The Vaikārika, the Taijasa, and the Bhūtādi — thus the other one (the threefold ahaṃkāra)."
G[31]["uncertain"] = []

G[32] = {
 "muktidaṃ": "granting liberation (mukti-da), acc. sg. n.",
 "paramaṃ": "supreme, acc. sg. n.",
 "divyaṃ": "divine, acc. sg. n.",
 "sarvasiddhipradāyakam": "bestowing all accomplishments (sarva-siddhi-pradāyaka), acc. sg. n.",
}
G[32]["close"] = "(The bindu is) liberation-granting, supreme, divine, bestowing every accomplishment."
G[32]["uncertain"] = []

G[33] = {
 "hrasvā": "the short (vowels), nom. pl. f.",
 "brahma": "Brahman, nom./acc. sg. n.",
 "samākhyātā": "are declared / named (samākhyāta), nom. pl. f.",
 "dīrghā": "the long (vowels), nom. pl. f.",
 "hyaṅgāni": "verily the limbs (hi aṅgāni), nom. pl. n.",
 "ṣa": "ṣaṇ, 'six' [fragment of ṣaṇmukha]",
 "mukha": "mukha, 'face' (→ Ṣaṇmukha, the Six-Faced) [fragment]",
}
G[33]["close"] = "The short (vowels) are declared to be Brahman; the long ones, verily, are the limbs of Ṣaṇmukha (the Six-Faced)."
G[33]["uncertain"] = []

G[34] = {
 "jāyate": "is born / arises (3sg. pres.)",
 "bindusaṃkṣobhādanantasyārthasiddhaye": "from the agitation of the bindu (bindu-saṃkṣobhāt), for the accomplishment of the aims (artha-siddhaye) of the Infinite (anantasya)",
}
G[34]["close"] = "For the accomplishment of the aims of the Infinite One, (the universe) is born from the agitation of the bindu."
G[34]["uncertain"] = []

G[35] = {
 "śaktirnādo": "Śakti and Nāda (śaktiḥ nādaḥ), nom. sg. m.",
 "mahāmāyā": "Mahāmāyā (the Great Māyā), nom. sg. f.",
 "vyometi": "and Vyoman (space) — thus (vyoma iti), nom. sg. n.",
 "ca": "and",
 "caturvidham": "fourfold, acc./nom. sg. n.",
}
G[35]["close"] = "Śakti, Nāda, Mahāmāyā, and Vyoman — thus the fourfold (division)."
G[35]["uncertain"] = []

G[36] = {
 "vaikharī": "Vaikharī (the fully articulated level of speech), nom. sg. f.",
 "madhyamā": "Madhyamā (the middle level), nom. sg. f.",
 "caiva": "and also (ca eva)",
 "paśyantī": "Paśyantī (the 'seeing' level), nom. sg. f.",
 "cāpi": "and also (ca api)",
 "sūkṣmayā": "with the subtle one (sūkṣmā = Parā, the supreme level), instr. sg. f.",
}
G[36]["close"] = "Vaikharī, Madhyamā, and Paśyantī — and also the subtle (Parā)."
G[36]["uncertain"] = []

G[37] = {
 "sūkṣmā": "the subtle one, nom. sg. f.",
 "ku": "ku- [fragment of kuṇḍalinīmadhye]",
 "ḍalinīmadhye": "in the middle of the Kuṇḍalinī (-ḍalinī-madhye) [fragment]",
 "jyotirmātrātya": "a measure of light, exceedingly (jyotir-mātrā-ati-) [fragment of jyotirmātrātyaṇīyasī]",
 "īyasī": "-aṇīyasī, extremely fine [fragment]",
}
G[37]["close"] = "The subtle one (Parā), in the middle of the Kuṇḍalinī, is an exceedingly minute measure of light."
G[37]["uncertain"] = []

G[38] = {
 "svayaṃ": "self (svayam, by itself)",
 "prakāśā": "luminous / self-illuminating, nom. sg. f.",
 "paśyantī": "Paśyantī (the 'seeing' level of speech), nom. sg. f.",
 "suṣumnāmāśritā": "resting on (āśritā) the Suṣumnā (suṣumnām), nom. sg. f.",
 "bhavet": "would be (3sg. opt.)",
}
G[38]["close"] = "Paśyantī is self-luminous; she abides in the Suṣumnā."
G[38]["uncertain"] = []

G[39] = {
 "antaḥsañjalpamātrā": "consisting only of inner articulation (antaḥ-sañjalpa-mātrā), nom. sg. f.",
 "syādavibhaktordhvagāminī": "would be (syāt) undivided (avibhakta), moving upward (ūrdhva-gāminī)",
}
G[39]["close"] = "She (Madhyamā) would be only inner articulation — undivided, moving upward."
G[39]["uncertain"] = []

G[40] = {
 "jihvāmūloṣṭhaniṣṭyūtā": "emitted / thrust forth at the root of the tongue and the lips (jihvā-mūla-oṣṭha-niṣṭyūta), nom. sg. f.",
 "kṛtavar": "having made the phonemes (kṛta-varṇa-) [fragment of kṛtavarṇaparigrahā]",
 "aparigrahā": "taking hold of (-parigrahā) [fragment of kṛtavarṇaparigrahā]",
}
G[40]["close"] = "(Vaikharī is) thrust forth from the tongue-root and lips, having taken possession of the phonemes."
G[40]["uncertain"] = []

G[41] = {
 "hakāraḥ": "the letter ha, nom. sg. m.",
 "savikāro": "with modification (sa-vikāraḥ), nom. sg. m.",
 "tha": "then (atha) [fragment of 'tha]",
 "rephe": "with repha (r) (repha-) [fragment of repheṇa]",
 "a": "instr. sg. ending -ṇa [fragment of repheṇa]",
 "samayujyata": "was joined (sam-yuj, 3sg. impf. passive)",
}
G[41]["close"] = "Then the letter ha, modified, was joined with repha (the letter r)."
G[41]["uncertain"] = []

G[42] = {
 "śaktibījaṃ": "the Śakti-bīja (the seed-mantra of Śakti, i.e. HRĪM), nom. sg. n.",
 "hi": "for, indeed",
 "tadyogāt": "from union with it (tad-yoga), abl. sg.",
 "prapañcotpattikāra": "the cause of the arising of the phenomenal world (prapañca-utpatti-kāraṇa-) [fragment of prapañcotpattikāraṇam]",
 "am": "acc. sg. ending (-ṇam) [fragment]",
}
G[42]["close"] = "For the Śakti-bīja, through union with it, is the cause of the arising of the phenomenal world."
G[42]["uncertain"] = []

G[43] = {
 "śliṣṭoccāritayoḥ": "of the two uttered in close conjunction (śliṣṭa-uccārita), gen. dual",
 "śābdaṃ": "verbal, consisting of sound, acc. sg. n.",
 "rūpaṃ": "the form, acc. sg. n.",
 "tadbījamīritam": "that (tad) is declared (īrita) the bīja (bījam), acc. sg. n.",
}
G[43]["close"] = "When the two are uttered in coalescence, that sound-form is declared to be the bīja."
G[43]["uncertain"] = []

G[44] = {
 "īkārastu": "but the letter ī (īkāraḥ tu), nom. sg. m.",
 "bhavenmāyā": "would be Māyā (bhavet māyā)",
 "bindurīśvara": "the bindu (is) Īśvara (binduḥ īśvaraḥ)",
 "ucyate": "is called (3sg. pres. passive)",
}
G[44]["close"] = "The letter ī would be Māyā; the bindu is called Īśvara."
G[44]["uncertain"] = []

G[45] = {
 "hakāro": "the letter ha, nom. sg. m.",
 "vyaktimāpanno": "having attained manifestation (vyaktim āpannaḥ), nom. sg. m.",
 "hārdaghoṣavivakṣitaḥ": "intended to express the inner sound (hārda-ghoṣa-vivakṣita), nom. sg. m.",
}
G[45]["close"] = "The letter ha, having become manifest, is meant to convey the inner sound."
G[45]["uncertain"] = []

G[46] = {
 "ūkārāntānyakārādīnyakṣarā": "the phonemes beginning with a and ending with ū (ūkārāntāni akārādīni akṣarāṇi) [fragment of ūkārāntānyakārādīnyakṣarāṇi]",
 "i": "nom. pl. ending (-ṇi) [fragment]",
 "ṣaḍasya": "its six (ṣaṭ asya), nom. pl. n.",
 "tu": "but",
}
G[46]["close"] = "But its six phonemes, beginning with a and ending with ū..."
G[46]["uncertain"] = []

G[47] = {
 "īkārabhedatastvāsannekārādyakṣarā": "but from the differentiation of ī, the phonemes beginning with e are adjacent (īkāra-bhedataḥ tu āsanna ekārādi akṣarāṇi) [fragment]",
 "i": "nom. pl. ending (-ṇi) [fragment]",
 "ṣaṭ": "six",
}
G[47]["close"] = "But through the differentiation of the ī, the six syllables beginning with e are adjacent."
G[47]["uncertain"] = []

G[48] = {
 "śaktyaṅgatvāt": "because of being limbs of Śakti (śakti-aṅgatva), abl. sg.",
 "kalāste": "those (te) kalās (kalāḥ, digits/portions)",
 "syuramṛtāṃśukalātmakāḥ": "would be (syuḥ) having the nature of the digits of the immortal-rayed (amṛtāṃśu = moon) (kalā-ātmaka), nom. pl. m.",
}
G[48]["close"] = "Because they are members of Śakti, they would be kalās, of the nature of the digits of the immortal-rayed (moon)."
G[48]["uncertain"] = []

G[49] = {
 "dīrghasvarā": "the long vowels (dīrgha-svara), nom. pl. m.",
 "visargāntāḥ": "ending in visarga (the emission-mark 'ḥ') (visarga-anta), nom. pl. m.",
 "strīliṅgāḥ": "feminine in gender (strī-liṅga), nom. pl. m.",
 "somarūpi": "having the form of Soma (soma-rūpi-) [fragment of somarūpiṇaḥ]",
 "aḥ": "nom. pl. ending (-ṇaḥ) [fragment]",
}
G[49]["close"] = "The long vowels, ending in visarga, are feminine and of Soma's (lunar) form."
G[49]["uncertain"] = []

G[50] = {
 "svarā": "of the vowels (svarāṇām) [fragment of svarāṇāmudayādyaṃ]",
 "āmudayādyaṃ": "the first emergence (-ṇām udaya-ādyaṃ) [fragment of svarāṇāmudayādyaṃ]",
 "tu": "but, now",
 "purastādiha": "here in front (purastāt + iha)",
 "likhyate": "is written (3sg. pres. passive)",
}
G[50]["close"] = "But the first arising of the vowels is written here at the beginning."
G[50]["uncertain"] = []

G[51] = {
 "vyomnaḥ": "from space / ether (vyoman), abl. sg.",
 "sparśagu": "having touch as its quality (sparśa-guṇa-) [fragment of sparśaguṇo]",
 "o": "nom. sg. ending (-ṇo) [fragment]",
 "vāyuḥ": "wind, nom. sg. m.",
 "sparśākhyāḥ": "called sparśa ('touch', i.e. stops) (sparśa-ākhya), nom. pl. m.",
 "kādayo": "the (consonants) beginning with ka (kādayaḥ), nom. pl. m.",
 "bhavan": "came to be (abhavan, 3pl. impf.)",
}
G[51]["close"] = "From space (arose) wind, whose quality is touch; the consonants beginning with ka, called sparśas, came into being."
G[51]["uncertain"] = []

G[52] = {
 "yādyakṣaracatuṣkaṃ": "the group of four phonemes beginning with ya (yādi-akṣara-catuṣka), nom. sg. n.",
 "tu": "but, now",
 "vāyvagnikṣmāmbhasāṃ": "of wind, fire, earth, and water (vāyu-agni-kṣmā-ambhas), gen. pl.",
 "tanuḥ": "the body, nom. sg. f.",
}
G[52]["close"] = "But the four phonemes beginning with ya are the body of wind, fire, earth, and water."
G[52]["uncertain"] = []

G[53] = {
 "śeṣāstu": "but the rest (śeṣāḥ tu), nom. pl. m.",
 "vyāpakāḥ": "pervasive, nom. pl. m.",
 "śādyāḥ": "beginning with śa (śādi, i.e. the remaining letters śa…ha), nom. pl. m.",
 "sāgnīṣomāḥ": "endowed with Agni and Soma (sa-agni-ṣoma), nom. pl. m.",
 "svaraspṛśaḥ": "touching the vowels (svara-spṛś), nom. pl. m.",
}
G[53]["close"] = "But the rest, beginning with śa, are pervasive, endowed with Agni and Soma, in contact with the vowels."
G[53]["uncertain"] = []

G[54] = {
 "kādayaḥ": "the (group) beginning with ka, nom. pl. m.",
 "pañcaviṃśār": "twenty-five phonemes (pañcaviṃśa-arṇa-) [fragment of pañcaviṃśārṇāḥ]",
 "ā": "nom. pl. ending (-āḥ) [fragment]",
 "yādayaḥ": "the (group) beginning with ya, nom. pl. m.",
 "śādayastathā": "likewise the (group) beginning with śa (śādayaḥ tathā)",
}
G[54]["close"] = "The ka-group (numbers) twenty-five phonemes; likewise the ya-group and the śa-group."
G[54]["uncertain"] = []

G[55] = {
 "akārādisvarairyuktahalāṃ": "the consonants joined with the vowels beginning with a (akārādi-svaraiḥ yukta-hal), acc. sg. f.",
 "yogānmitho": "from mutual (mithaḥ) combination (yogāt), abl. sg.",
 "pi": "also (api)",
 "ca": "and",
}
G[55]["close"] = "And (the count arises from) the consonants joined with the vowels beginning with a, and also from their mutual combination."
G[55]["uncertain"] = []

G[56] = {
 "saiva": "that very (sā eva), nom. sg. f.",
 "śaktirdvidhā": "the Śakti twofold (śaktiḥ dvidhā)",
 "bhūtā": "become (bhūta, ppp.), nom. sg. f.",
 "tāro": "the Tāra (tāraḥ, the praṇava OM), nom. sg. m.",
 "vāgbhavamityapi": "and the Vāgbhava — thus too (vāgbhavam iti api), acc. sg. n.",
}
G[56]["close"] = "That very Śakti has become twofold: the Tāra and the Vāgbhava."
G[56]["uncertain"] = []

G[57] = {
 "tārākhyaḥ": "called Tāra (tāra-ākhya), nom. sg. m.",
 "pra": "pra- [fragment of praṇavo]",
 "avo": "-ṇavaḥ, the praṇava [fragment]",
 "hyeṣa": "for this (hi eṣa)",
 "śabdabrahmātmako": "having the nature of Sound-Brahman (śabda-brahma-ātmaka), nom. sg. m.",
 "mataḥ": "considered / held (mata), nom. sg. m.",
}
G[57]["close"] = "This praṇava, called Tāra, is held to be of the nature of Sound-Brahman."
G[57]["uncertain"] = []

G[58] = {
 "viśvavāgbhūtidaṃ": "bestowing all speech and prosperity (viśva-vāk-bhūti-da), acc. sg. n.",
 "tattu": "and that (tat tu)",
 "vāgīśvaryāstanurbhavet": "would be the body (tanuḥ) of Vāgīśvarī (vāgīśvaryāḥ), 3sg. opt.",
}
G[58]["close"] = "And that, which bestows all speech and prosperity, would be the body of Vāgīśvarī."
G[58]["uncertain"] = []

G[59] = {
 "śaktibījaṃ": "the Śakti-bīja, nom. sg. n.",
 "tathā": "likewise",
 "tāro": "the Tāra, nom. sg. m.",
 "vāgbhavaṃ": "the Vāgbhava, nom. sg. n.",
 "ca": "and",
 "tataḥ": "thereafter (adv.)",
 "param": "after / next (adv.)",
}
G[59]["close"] = "The Śakti-bīja, then the Tāra, then the Vāgbhava, and thereafter..."
G[59]["uncertain"] = []

G[60] = {
 "tadbhedajāśca": "and born from their differentiation (tad-bheda-ja + ca), nom. pl. f.",
 "yā": "which, nom. pl. f.",
 "vāco": "the utterances / speech (vācaḥ), nom. pl. f.",
 "deśabhājā": "by division of place (deśa-bhājā, i.e. articulatory position), instr. sg. f.",
 "vilakṣa": "distinguished (vilakṣaṇa-) [fragment of vilakṣaṇāḥ]",
 "āḥ": "nom. pl. ending (-ṇāḥ) [fragment]",
}
G[60]["close"] = "And the utterances born from their differentiation, which are distinguished by (articulatory) place."
G[60]["uncertain"] = []

G[61] = {
 "ākāśādīni": "beginning with space (ākāśa-ādi), nom. pl. n.",
 "bhūtāni": "the (gross) elements, nom. pl. n.",
 "tanmātrā": "the subtle elements (tanmātrā-) [fragment of tanmātrāṇīndriyāṇi]",
 "īndriyā": "the sense-organs (indriyāṇi) [fragment of tanmātrāṇīndriyāṇi]",
 "i": "nom. pl. ending (-ṇi) [fragment]",
 "ca": "and",
}
G[61]["close"] = "The elements beginning with space, the tanmātras, and the sense-organs..."
G[61]["uncertain"] = []

G[62] = {
 "bahunā": "with much (bahunā, i.e. much prattle), instr. sg. n.",
 "kiṃ": "what (kim, interrogative)",
 "pralāpena": "with prattle / chatter, instr. sg. m.",
 "yaḥ": "which / who, nom. sg. m.",
 "śabdārthātmako": "having the nature of word and meaning (śabda-artha-ātmaka), nom. sg. m.",
 "khilaḥ": "the whole (akhilaḥ) [fragment]",
}
G[62]["close"] = "What (need) of much prattle — (that) which is the whole, of the nature of word and meaning?"
G[62]["uncertain"] = []

G[63] = {
 "asyāṃ": "in this, loc. sg. f.",
 "tu": "but, now",
 "mātṛkākhyāyāṃ": "called Mātṛkā (mātṛkā-ākhyā), loc. sg. f.",
 "lipitvaṃ": "the state of being script (lipi-tva), acc. sg. n.",
 "likhyate": "is written (3sg. pres. passive)",
 "yataḥ": "because / since",
}
G[63]["close"] = "And in this (system) called the Mātṛkā, the property of being script is written, because..."
G[63]["uncertain"] = []

G[64] = {
 "ar": "ar- [fragment of arṇatvāt]",
 "atvamamṛtātmatvādar": "the phoneme-ness and the immortal-nature (arṇatvam amṛtātmatvāt) [fragment]",
 "o": "arṇo, 'the phoneme' [fragment]",
 "mbhaḥ": "ambhaḥ, 'water' [fragment]",
 "kathyate": "is called (3sg. pres. passive)",
 "yataḥ": "because / since",
}
G[64]["close"] = "Because the phoneme is called 'water' (ambhas) owing to its being a phoneme and owing to its immortal nature."
G[64]["uncertain"] = []

G[65] = {
 "upādānāni": "the material causes (upādāna), nom. pl. n.",
 "viśvātmamātṛkāyāstu": "but of the Mātṛkā whose self is the universe (viśva-ātma-mātṛkāyāḥ tu), gen. sg. f.",
 "pañca": "five",
 "vai": "indeed",
}
G[65]["close"] = "But the material causes of the Mātṛkā, whose self is the universe, are indeed five."
G[65]["uncertain"] = []

G[66] = {
 "ṭatavargau": "the ṭa-group and the ta-group (ṭa-ta-varga), nom. dual m.",
 "tathā": "likewise",
 "pādau": "the two feet (pāda), nom. dual m.",
 "pārśvayugmaṃ": "the pair of sides (pārśva-yugma), nom. sg. n.",
 "paphau": "pa and pha (paphau), nom. dual m.",
 "matau": "considered (mata), nom. dual m.",
}
G[66]["close"] = "The ṭa- and ta-groups are the two feet; pa and pha, likewise, are the pair of flanks — so they are held."
G[66]["uncertain"] = []

G[67] = {
 "tvagasṛṅmāṃsamedosthimajjāśuklāni": "skin, blood, flesh, fat, bone, marrow, (and) semen (tvag-asṛk-māṃsa-medas-astthi-majjā-śukla), nom. pl. n.",
 "yādayaḥ": "the (group) beginning with ya, nom. pl. m.",
}
G[67]["close"] = "The ya-group (are) skin, blood, flesh, fat, bone, marrow, and semen."
G[67]["uncertain"] = []

G[68] = {
 "sphūrtiḥ": "the throb / flash of manifestation (sphūrti), nom. sg. f.",
 "kṣakāraḥ": "the letter kṣa, nom. sg. m.",
 "sakrodho": "with anger (sa-krodhaḥ), nom. sg. m.",
 "viśvalokamayī": "consisting of the whole world (viśva-loka-mayī), nom. sg. f.",
 "tanuḥ": "the body, nom. sg. f.",
}
G[68]["close"] = "The letter kṣa is the pulsation, together with wrath; (it is) the body consisting of the whole world."
G[68]["uncertain"] = []

G[69] = {
 "brahmādistambaparyantaṃ": "from Brahmā down to a clump of grass (brahmādi-stamba-paryanta), acc. sg. n.",
 "mātṛkāyāṃ": "in the Mātṛkā, loc. sg. f.",
 "vyavasthitam": "established (vyavasthita, ppp.), acc. sg. n.",
}
G[69]["close"] = "Everything from Brahmā up to a blade of grass is established in the Mātṛkā."
G[69]["uncertain"] = []

G[70] = {
 "avargādudgataḥ": "risen from the a-group (avarga-udgata), nom. sg. m.",
 "sūryaḥ": "the sun, nom. sg. m.",
 "kavargādapi": "also from the ka-group (kavargāt api)",
 "bhūsutaḥ": "the son of Earth (bhū-suta = Mars), nom. sg. m.",
}
G[70]["close"] = "From the a-group has risen the Sun; from the ka-group, the son of Earth (Mars)."
G[70]["uncertain"] = []

G[71] = {
 "pavargācca": "and from the pa-group (pavargāt ca)",
 "śaniścandro": "Saturn and the Moon (śaniḥ candraḥ), nom. sg. m.",
 "yavargādabhavad": "from the ya-group arose (yavargāt abhavat)",
 "vibhuḥ": "the omnipresent (Lord), nom. sg. m.",
}
G[71]["close"] = "From the pa-group, Saturn and the Moon; from the ya-group arose the omnipresent (Vibhu)."
G[71]["uncertain"] = []

G[72] = {
 "mātṛkākṣarasambhedāt": "from the differentiation of the Mātṛkā's phonemes (mātṛkā-akṣara-sambheda), abl. sg.",
 "kathyante": "they are spoken / declared (3pl. pres. passive)",
 "parato": "hereafter (parataḥ)",
 "tra": "here (atra) [fragment]",
 "vai": "indeed",
}
G[72]["close"] = "From the differentiation of the Mātṛkā's phonemes, (the following) are indeed declared below, here."
G[72]["uncertain"] = []

G[73] = {
 "samudgatāstathā": "likewise emerged (samudgatāḥ tathā), nom. pl. f.",
 "rudraśaktayastatprasaṃkhyayā": "the Rudra-Śaktis, by that enumeration (rudra-śaktayaḥ tat-prasaṃkhyayā), nom. pl. f.",
}
G[73]["close"] = "Likewise have emerged the Rudra-Śaktis, according to that enumeration."
G[73]["uncertain"] = []

G[74] = {
 "oṣadhyaścāpi": "and also the herbs (oṣadhyaḥ ca api), nom. pl. f.",
 "pañcāśadaṣṭatriṃśat": "fifty, and thirty-eight (pañcāśat aṣṭatriṃśat)",
 "kalāstathā": "and likewise the kalās (kalāḥ tathā)",
}
G[74]["close"] = "And the herbs — fifty — and the kalās, thirty-eight, likewise."
G[74]["uncertain"] = []

G[75] = {
 "evaṃ": "thus",
 "hi": "for, indeed",
 "mātṛkotpattirāgamoktā": "the origin of the Mātṛkā as declared in the Āgama (mātṛkā-utpattiḥ āgama-uktā), nom. sg. f.",
 "pradarśitā": "has been shown (pradarśita, ppp.), nom. sg. f.",
}
G[75]["close"] = "Thus has been shown the origin of the Mātṛkā, as declared in the Āgama."
G[75]["uncertain"] = []

G[76] = {
 "atroddhriyante": "here are extracted / drawn out (atra + uddhriyante, 3pl. pres. passive)",
 "bījāni": "the seed-syllables, nom. pl. n.",
 "bījamantrāḥ": "the bīja-mantras, nom. pl. m.",
 "samantrakāḥ": "together with their mantras (sa-mantraka), nom. pl. m.",
}
G[76]["close"] = "Here are extracted the bījas — the bīja-mantras together with their (full) mantras."
G[76]["uncertain"] = []

G[77] = {
 "tataḥ": "thereafter",
 "paraṃ": "after (adv.)",
 "yathāpāṭhaṃ": "according to the reading / as in the text (yathā-pāṭham)",
 "vijñeyā": "to be known (vijñeya), nom. pl. f.",
 "nipu": "skilled (nipuṇa-) [fragment of nipuṇaiḥ]",
 "aiḥ": "instr. pl. ending (-ṇaiḥ) [fragment]",
 "sphuṭam": "clearly (adv.)",
}
G[77]["close"] = "Thereafter they are to be known clearly by the expert, according to the text."
G[77]["uncertain"] = []

G[78] = {
 "yathāvadatra": "here, as appropriate (yathāvat + atra)",
 "likhyante": "they are written (3pl. pres. passive)",
 "bhagavacchabdasaṃyutāḥ": "joined with the word 'bhagavat' (bhagavat-śabda-saṃyuta), nom. pl. m.",
}
G[78]["close"] = "Here they are written as appropriate, joined with the word 'Lord' (bhagavat)."
G[78]["uncertain"] = []

G[79] = {
 "da": "da- [fragment of daṇḍārdhendurbhaved]",
 "ḍārdhendurbhaved": "would be staff-and-half-moon (daṇḍa-ardhendu + bhavet) [fragment]",
 "binduḥ": "the bindu, nom. sg. m.",
 "sargo": "the emission (sargaḥ — here the visarga), nom. sg. m.",
 "bindudvaye": "in the pair of bindus (bindu-dvaya), loc. sg.",
 "mataḥ": "considered (mata), nom. sg. m.",
}
G[79]["close"] = "The bindu would be a staff (with) a half-moon; the visarga is held (to consist of) the two bindus."
G[79]["uncertain"] = []

G[80] = {
 "viṣakālau": "poison and Time (viṣa-kāla), nom. dual m.",
 "makāraḥ": "the letter ma, nom. sg. m.",
 "syād": "would be (3sg. opt.)",
 "dhātavo": "the (bodily) elements / constituents (dhātavaḥ), nom. pl. m.",
 "yādayo": "the (group) beginning with ya (yādayaḥ), nom. pl. m.",
 "matāḥ": "considered (mata), nom. pl. m.",
}
G[80]["close"] = "The letter ma would be poison and Time; the ya-group are held to be the bodily elements."
G[80]["uncertain"] = []

G[81] = {
 "khaḥ": "the letter kha, nom. sg. m.",
 "prā": "prāṇa-, 'vital breath' [fragment of prāṇabhuvaneśākhyo]",
 "abhuvaneśākhyo": "-bhuvaneśākhyaḥ, called the lord of the (vital) worlds [fragment]",
 "hakāraḥ": "the letter ha, nom. sg. m.",
 "śivasaṃjñitaḥ": "denominated 'Śiva' (śiva-saṃjñita), nom. sg. m.",
}
G[81]["close"] = "Kha is called the lord of the vital worlds; ha is denominated Śiva."
G[81]["uncertain"] = []

G[82] = {
 "paphabāśca": "and pa, pha, ba (pa-pha-ba + ca), nom. pl. m.",
 "bhamakṣāśca": "and bha, ma, kṣa (bha-ma-kṣa + ca), nom. pl. m.",
 "vyatyayaṃ": "interchange (acc. sg. m.)",
 "te": "they, nom. pl. m.",
 "trayastrayaḥ": "three and three (trayas trayas), nom. pl. m.",
}
G[82]["close"] = "And (the sets) pa-pha-ba and bha-ma-kṣa — those (groups of) three and three undergo interchange."
G[82]["uncertain"] = []

G[83] = {
 "svareṣu": "in the vowels, loc. pl. m.",
 "vyatyayo": "interchange (vyatyayaḥ), nom. sg. m.",
 "neṣṭastadvad": "is not approved (na iṣṭaḥ), likewise (tadvat)",
 "yuktākṣareṣvapi": "also in the conjunct phonemes (yuktākṣareṣu api), loc. pl.",
}
G[83]["close"] = "Interchange is not approved among the vowels, nor likewise among the conjunct phonemes."
G[83]["uncertain"] = []

G[84] = {
 "tattadakṣaravijñaptyai": "for the making-known of this-and-that phoneme (tat-tad-akṣara-vijñapti), dat. sg.",
 "saṅketāya": "as a convention (saṅketa), dat. sg.",
 "bhavanti": "they are / serve (3pl. pres.)",
 "hi": "for, indeed",
}
G[84]["close"] = "For they serve as a convention for signalling each particular phoneme."
G[84]["uncertain"] = []

G[85] = {
 "yathāsaṅkhyaṃ": "according to the count (yathā-saṅkhyam)",
 "tathā": "so, thus",
 "vidyāt": "one should know (3sg. opt.)",
 "svarāḥ": "the vowels, nom. pl. m.",
 "sapta": "seven",
 "diśo": "the directions (diśaḥ), nom. pl. f.",
 "daśa": "ten",
}
G[85]["close"] = "Correspondingly, one should know: the vowels are seven, the directions ten."
G[85]["uncertain"] = []

G[86] = {
 "vedāścatvāra": "the Vedas, four (vedāḥ catvāraḥ), nom. pl. m.",
 "eva": "indeed",
 "syustrayo": "would be three (syuḥ trayaḥ)",
 "rāmāśtrayo": "three are the Rāmas (rāmāḥ trayaḥ)",
 "gnayaḥ": "the fires (agnayaḥ) [fragment]",
}
G[86]["close"] = "The Vedas are indeed four; three are the Rāmas; three are the fires."
G[86]["uncertain"] = []

G[87] = {
 "uktātyuktā": "Uktā and Atyuktā (uktā atyuktā, meter names), nom. sg. f.",
 "tathā": "likewise",
 "madhyā": "Madhyā (meter name), nom. sg. f.",
 "pratiṣṭhā": "Pratiṣṭhā (meter name), nom. sg. f.",
 "supratiṣṭhitā": "Supratiṣṭhitā (meter name), nom. sg. f.",
}
G[87]["close"] = "Uktā, Atyuktā, and likewise Madhyā, Pratiṣṭhā, Supratiṣṭhitā."
G[87]["uncertain"] = []

G[88] = {
 "tṛṣṭup": "the Triṣṭubh (meter), nom. sg. f.",
 "ca": "and",
 "jagatī": "the Jagatī (meter), nom. sg. f.",
 "tadvat": "likewise",
 "tato": "thereafter (tataḥ)",
 "tijagatī": "the Atijagatī (meter) (atijagatī) [fragment]",
 "matā": "considered (mata), nom. sg. f.",
}
G[88]["close"] = "And Triṣṭubh, and likewise Jagatī; after that, Atijagatī is recognized."
G[88]["uncertain"] = []

G[89] = {
 "dhṛtiścātidhṛtiścaiva": "Dhṛti and Atidhṛti (dhṛtiḥ ca atidhṛtiḥ ca eva, meter names), nom. sg. f.",
 "kṛtiḥ": "Kṛti (meter name), nom. sg. f.",
 "prakṛtirākṛtiḥ": "Prakṛti and Ākṛti (prakṛtiḥ ākṛtiḥ, meter names), nom. sg. f.",
}
G[89]["close"] = "Dhṛti, and Atidhṛti, Kṛti, Prakṛti, Ākṛti."
G[89]["uncertain"] = []

G[90] = {
 "etāsāṃ": "of these, gen. pl. f.",
 "chandasāṃ": "of the meters (chandas), gen. pl. n.",
 "saṃkhyā": "the count, nom. sg. f.",
 "kvacidatra": "here somewhere (kvacit + atra)",
 "vidhīyate": "is prescribed (3sg. pres. passive)",
}
G[90]["close"] = "The count of these meters is prescribed here somewhere."
G[90]["uncertain"] = []

G[91] = {
 "tathā": "likewise",
 "ṣaṭtriṃśadeva": "thirty-six indeed (ṣaṭtriṃśat eva)",
 "syuḥ": "would be (3pl. opt.)",
 "śaive": "in the Śaiva (doctrine), loc. sg.",
 "tattvāni": "the tattvas / principles, nom. pl. n.",
 "saṃkhyayā": "in number (instr. sg. f.)",
}
G[91]["close"] = "Likewise, in the Śaiva (system), the tattvas would be thirty-six in number."
G[91]["uncertain"] = []

G[92] = {
 "navabhirnavapañcāṣṭavar": "by nines, by (groups of) nine, five, (and) eight phonemes (navabhiḥ nava-pañca-aṣṭa-varṇa-) [fragment of navabhirnavapañcāṣṭavarṇaiḥ]",
 "aiḥ": "instr. pl. ending (-ṇaiḥ) [fragment]",
 "saṃkhyātra": "the count here (saṃkhyā atra)",
 "vā": "or",
 "bhavet": "would be (3sg. opt.)",
}
G[92]["close"] = "Or the count here could be by nines — by (groups of) nine, five, and eight phonemes."
G[92]["uncertain"] = ["navabhirnavapañcāṣṭavarṇaiḥ"]

G[93] = {
 "sukhāvabodho": "easy comprehension (sukha-avabodha), nom. sg. m.",
 "hyarthānāṃ": "for of the meanings (hi + arthānām), gen. pl. m.",
 "bhavatyeveṣṭasiddhaye": "indeed becomes, for the accomplishment of the desired (bhavati eva iṣṭa-siddhaye)",
}
G[93]["close"] = "For easy comprehension of the meanings indeed serves the accomplishment of what is desired."
G[93]["uncertain"] = []

G[94] = {
 "tacchāktaṃ": "that Śākta (tat śākta, belonging to Śakti), acc. sg. n.",
 "pra": "pra- [fragment of praṇavākhyabījamakhilaṃ]",
 "avākhyabījamakhilaṃ": "-ṇavākhya-bījam, the seed called praṇava, the whole (akhilam) [fragment]",
 "nyagrodhabījaṃ": "a banyan-seed (nyagrodha-bīja), acc. sg. n.",
 "viduḥ": "they know (3pl. perf.)",
}
G[94]["close"] = "They know that Śākta seed called the Praṇava — the whole (world) — as a banyan seed."
G[94]["uncertain"] = []

G[95] = {
 "iti": "thus",
 "śrīmadīśānaśivagurudevamiśraviracite": "composed by the revered Īśānaśivagurudevamiśra (śrīmat-īśāna-śiva-gurudeva-miśra-viracita), loc. sg. n.",
 "tantrasārapaddhatau": "in the Tantrasārapaddhati, loc. sg. f.",
 "vastunirdeśamātṛkopapattinir": "the determination (nirṇaya) of the genesis (upapatti) of the Mātṛkā in the exposition of the subject-matter (vastu-nirdeśa-mātṛkā-upapatti-nirṇaya-) [fragment of vastunirdeśamātṛkopapattinirṇayo]",
 "ayo": "nom. sg. ending (-ṇayo) [fragment]",
 "nāma": "named (adv.)",
 "prathamaḥ": "the first, nom. sg. m.",
 "paṭalaḥ": "chapter, nom. sg. m.",
}
G[95]["close"] = "Thus, in the Tantrasārapaddhati composed by the revered Īśānaśivagurudevamiśra, (this is) the first chapter named 'The Determination of the Genesis of the Mātṛkā in the Exposition of the Subject-Matter'."
G[95]["uncertain"] = []

G[96] = {
 "aśvīśo": "Aśvīśa (the Lord of the Horses), nom. sg. m.",
 "bhārabhūtiśca": "and Bhārabhūti (bhāra-bhūtiḥ ca), nom. sg. m.",
 "tithīśaḥ": "Tithīśa (the Lord of the lunar days), nom. sg. m.",
 "sthā": "sthā- [fragment of sthāṇuko]",
 "uko": "-ṇukaḥ, Sthāṇuka [fragment]",
 "haraḥ": "Hara, nom. sg. m.",
}
G[96]["close"] = "Aśvīśa, Bhārabhūti, Tithīśa, Sthāṇuka, Hara."
G[96]["uncertain"] = []

G[97] = {
 "akrūraśca": "and Akrūra (akrūraḥ ca), nom. sg. m.",
 "mahāsenaḥ": "Mahāsena, nom. sg. m.",
 "ṣoḍaśaite": "these sixteen (ṣoḍaśa ete), nom. pl. m.",
 "svareśvarāḥ": "the lords of the vowels (svara-īśvara), nom. pl. m.",
}
G[97]["close"] = "And Akrūra and Mahāsena — these sixteen are the lords of the vowels."
G[97]["uncertain"] = []

G[98] = {
 "ekarudraśca": "and Ekarudra (eka-rudraḥ ca), nom. sg. m.",
 "kūrmaikanetrau": "Kūrma and Ekanetra (kūrma-ekanetrau), nom. dual m.",
 "ca": "and",
 "caturānanaḥ": "Caturānana (the Four-Faced), nom. sg. m.",
}
G[98]["close"] = "And Ekarudra, Kūrma and Ekanetra (the two), and Caturānana."
G[98]["uncertain"] = []

G[99] = {
 "ardhanārīśvaraścomākāntaścāṣaḍiḍi": "and Ardhanārīśvara, and Umākānta, and the two Ṣaḍiḍiṇḍin (ardhanārīśvaraḥ ca umākāntaḥ ca ṣaḍiḍiṇḍin-) [fragment of ardhanārīśvaraścomākāntaścāṣaḍiḍiṇḍinau]",
 "ḍinau": "-ḍiṇḍinau, the two (nom. dual m.) [fragment]",
}
G[99]["close"] = "And Ardhanārīśvara, and Umākānta, and the two Ṣaḍiḍiṇḍins."
G[99]["uncertain"] = []

# ---- assemble ----
src = [json.loads(l) for l in open(
    "/root/projects/patala/data/corpus/downloads/translations/isanasivagurudevapaddhati.jsonl")]
assert len(src) == 100, len(src)

translations = []
for i in range(100):
    d = src[i]
    assert d["verse_idx"] == i
    toks = TOKENS[i]
    g = G[i]
    glosses = {t: g[t] for t in toks}  # keys in prompt order
    missing = [t for t in toks if t not in g]
    assert not missing, (i, missing)
    extra = [k for k in g if k not in ("close", "uncertain") and k not in toks]
    assert not extra, (i, extra)
    translations.append({
        "passage_id": f"isanasivagurudevapaddhati:v{i+1}",
        "source_sha256": d["source_sha256"],
        "tokens": glosses,
        "close": g["close"],
        "uncertain": g["uncertain"],
    })

out = {"batch_id": "isanasivagurudevapaddhati_p1-p2_v1-100_a3_raw-l0_20260813",
       "translations": translations}

with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)

# validation report
n_tok = sum(len(t["tokens"]) for t in translations)
print(f"passages: {len(translations)}")
print(f"tokens:   {n_tok}")
print(f"file:     {OUT}")
