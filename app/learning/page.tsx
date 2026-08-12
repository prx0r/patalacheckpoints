"use client";

import React, { useState } from "react";
import { traditions } from "@/data/atlas";
import type { AtlasEntity } from "@/lib/atlas";

const SHARED_FOUNDATIONS = [
  {
    title: "Consciousness is primary",
    body: "Across every school, reality begins with consciousness — not with matter that somehow produces mind. This is the premise granted by the tradition (and examined, never merely assumed). The question is never 'how does matter become conscious?' but 'how does consciousness produce the appearance of matter, bodies, subjects, and worlds?'",
    concepts: ["prakāśa", "vimarśa", "saṃvit"],
  },
  {
    title: "Manifestation is self-knowing",
    body: "Consciousness is not a passive lamp that illuminates objects. It has two inseparable poles: prakāśa (appearing) and vimarśa (reflexively knowing that it appears). A light that did not know its own shining would be a stone, not consciousness. This pair is the engine of the whole metaphysics.",
    concepts: ["prakāśa", "vimarśa"],
  },
  {
    title: "The world is differentiation, not illusion",
    body: "The ordinary world is not dismissed as unreal. It is one region of manifestation — the gross, determinate, bounded end of a hierarchy. 'Māyā' is not 'illusion'; it is the power by which consciousness manifests its own contents as apparently other than itself. The world is real, but its ultimate nature is not something outside consciousness.",
    concepts: ["māyā", "āveśa", "śūnya"],
  },
  {
    title: "Contraction generates the finite subject",
    body: "To produce a finite first-person perspective, unrestricted consciousness must constrain itself: a viewpoint (here), restricted knowledge and agency, time, space, causality, and lack. These constraints are the kañcukas, and their result is the localized experiencer (puruṣa). The schools differ on details, but all share this: the subject is a contracted configuration of consciousness, not a separate entity.",
    concepts: ["puruṣa", "krama"],
  },
  {
    title: "Liberation is recognition, not escape",
    body: "Awakening is not the disappearance of the self or the world. It is the recognition that this apparently finite center was never ontologically separate from the consciousness through which the entire field manifests. The schools differ on how this is achieved (knowledge, devotion, the Goddess, the pulse), but the destination is shared.",
    concepts: ["recognition", "svātantrya"],
  },
  {
    title: "Recognition is felt, and it adds nothing",
    body: "In the Pratyabhijñā — the school of Utpaladeva and Abhinavagupta — recognition (pratyabhijñā) is the felt re-cognition of the self: the self, already established, re-cognizes itself as the Lord. It is a change in where the self stands (from a thing lost in the world to the primary thing seen), not an addition of new content. The essence of light is vimarśa, the felt reflexive-awareness; its re-cognition is camatkāra, the savouring. Abhinavagupta's great commentary, the Īśvarapratyabhijñāvivṛtivimarśinī, is the deepest source of this thesis.",
    concepts: ["recognition", "vimarśa", "camatkara", "prakāśa"],
  },
];

// The compact timeline, from the canonical reference map. The dates distinguish
// (where possible) between authors' activity, texts' probable existence, and the
// date of surviving witnesses — these are not interchangeable.
const TIMELINE = [
  { period: "c. 7th–8th c.", label: "Bhairava / Vidyāpīṭha — the Yoginī cult environment", kind: "stratum" },
  { period: "By early 9th c.", label: "Kaula Trika established in Kashmir (Eastern Transmission)", kind: "stratum" },
  { period: "1st half 9th c.", label: "Jñānanetra / Śivānanda — chartable Krama history begins", kind: "stratum" },
  { period: "9th c.", label: "Śivasūtra / Spanda — the Vasugupta–Kallaṭa milieu", kind: "stratum" },
  { period: "9th–10th c.", label: "Krama scriptures: Devīpañcaśataka, Kramasadbhāva", kind: "text" },
  { period: "c. 900–950", label: "Somānanda — the Śivadṛṣṭi", kind: "person" },
  { period: "c. 925–975", label: "Utpaladeva — Īśvarapratyabhijñā", kind: "person" },
  { period: "c. 975–1025", label: "Abhinavagupta — the Tantrāloka, Pratyabhijñā exegesis", kind: "person" },
  { period: "11th c.", label: "earliest recovered Kubjikā manuscripts (Kathmandu Valley)", kind: "text" },
  { period: "c. 1000–1050", label: "Kṣemarāja — the Spanda/Trika synthesis", kind: "person" },
  { period: "1002 CE", label: "Nepalese witness mentioning Vimalaprabodha (Kālīkulakramārcana)", kind: "text" },
  { period: "11th–13th c.", label: "the enlarged Kubjikā corpus: Ṣaṭsāhasra, Śrīmatottara, Manthānabhairava", kind: "text" },
  { period: "c. 1225–1275", label: "Jayaratha — the Tantrāloka commentary (Viveka)", kind: "person" },
  { period: "Medieval", label: "Nepal — the multi-āmnāya synthesis, Sarvāmnāya / Newar Śākta systems", kind: "stratum" },
];

// Geography: claimed revelation, historical center, and manuscript survival are
// deliberately distinct — the reference map's warning against a single "location" field.
const GEOGRAPHY = [
  { place: "Oḍḍiyāna / Swat", role: "claimed revelation", note: "tradition memories surrounding the northern Kālī / Krama lineages" },
  { place: "Kashmir", role: "historical center", note: "Trika · Krama exegesis · Spanda · Somānanda→Utpaladeva→Abhinavagupta · Jayaratha" },
  { place: "Nepal / Kathmandu Valley", role: "where the manuscripts survive", note: "Kubjikā · Guhyakālī / northern materials · Newar ritual continuity · the later Sarvāmnāya synthesis" },
];


export default function LearningPage() {
  const [showNote, setShowNote] = useState(false);
  const order = ["trika", "krama", "kubjika", "kaula", "spanda", "pratyabhijna", "sarvamnyaya"];
  const schoolMap = new Map(traditions.map((t) => [t.id, t]));

  return (
    <main className="min-h-screen bg-zinc-950 px-6 py-12 text-zinc-200">
      <div className="mx-auto max-w-3xl">
        <header className="mb-6">
          <p className="text-[10px] uppercase tracking-[0.3em] text-[color:var(--saffron)]">patala — tantra hub</p>
          <h1 className="mt-1 font-serif text-3xl text-[color:var(--bone)]">Learn</h1>
          <p className="mt-2 text-sm text-zinc-400">
            A school-by-school introduction, built from the shared foundations upward. Each
            school is a dialect of one common premise — consciousness is primary. The goal is
            not to memorize a chart but to be able to open the texts and understand them.
          </p>
        </header>

        {/* Shared foundations */}
        <section className="mb-8">
          <div className="flex items-center justify-between">
            <h2 className="font-serif text-xl text-[color:var(--saffron)]">The shared foundations</h2>
            <button
              onClick={() => setShowNote(!showNote)}
              className="rounded border border-zinc-700 px-2 py-0.5 text-[10px] uppercase tracking-wider text-zinc-400 hover:border-[color:var(--saffron)] hover:text-[color:var(--saffron)]"
            >
              {showNote ? "hide the caveat" : "the caveat"}
            </button>
          </div>
          {showNote && (
            <p className="mt-2 rounded border border-zinc-800 bg-zinc-900/50 p-3 text-[12px] leading-relaxed text-zinc-400">
              These foundations are a reconstruction of the <span className="text-zinc-300">nondual
              Śaiva/Trika worldview</span> — especially the trajectory culminating in Utpaladeva and
              Abhinavagupta — not a single doctrine every Tantra shares. And they are offered as
              the tradition's own claim, not as established fact: modern science has not established
              consciousness as fundamental. Treat this as "what the tradition says and why," examined
              rather than assumed.
            </p>
          )}
          <div className="mt-4 space-y-4">
            {SHARED_FOUNDATIONS.map((f, i) => (
              <div key={i} className="rounded border border-zinc-800 bg-zinc-900/30 p-4">
                <p className="mb-1 font-serif text-[15px] text-[color:var(--bone)]">{i + 1}. {f.title}</p>
                <p className="text-[13px] leading-relaxed text-zinc-300">{f.body}</p>
                <div className="mt-2 flex flex-wrap gap-1.5">
                  {f.concepts.map((c) => (
                    <a key={c} href={`/concepts/${c}`} className="rounded border border-zinc-700/60 px-1.5 py-0.5 text-[10px] text-zinc-400 hover:border-[color:var(--saffron)] hover:text-[color:var(--saffron)]">
                      {c} →
                    </a>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* The timeline */}
        <section className="mb-8">
          <h2 className="mb-2 font-serif text-xl text-[color:var(--saffron)]">The timeline</h2>
          <p className="mb-3 text-[12px] text-zinc-500">
            From the compact timeline in the canonical reference map. Dates distinguish authors'
            activity, texts' probable existence, and the date of surviving witnesses — these are
            not interchangeable.
          </p>
          <ol className="relative space-y-2 border-l border-zinc-800 pl-4">
            {TIMELINE.map((t, i) => (
              <li key={i} className="relative">
                <span className="absolute -left-[21px] top-1.5 h-2 w-2 rounded-full bg-[color:var(--saffron)]/70" />
                <div className="flex flex-wrap items-baseline gap-x-2">
                  <span className="font-mono text-[11px] text-[color:var(--saffron)]">{t.period}</span>
                  <span className={`text-[10px] uppercase tracking-wider ${t.kind === "person" ? "text-zinc-400" : t.kind === "text" ? "text-zinc-500" : "text-zinc-600"}`}>{t.kind}</span>
                </div>
                <p className="text-[13px] text-zinc-300">{t.label}</p>
              </li>
            ))}
          </ol>
        </section>

        {/* The geography */}
        <section className="mb-8">
          <h2 className="mb-2 font-serif text-xl text-[color:var(--saffron)]">Where it happened</h2>
          <p className="mb-3 text-[12px] text-zinc-500">
            The place of claimed revelation, the historical center, and where the manuscripts
            survive are deliberately kept distinct.
          </p>
          <div className="space-y-3">
            {GEOGRAPHY.map((g, i) => (
              <div key={i} className="rounded border border-zinc-800 bg-zinc-900/30 p-3">
                <div className="flex items-baseline justify-between">
                  <span className="font-serif text-[14px] text-[color:var(--bone)]">{g.place}</span>
                  <span className="text-[10px] uppercase tracking-wider text-zinc-500">{g.role}</span>
                </div>
                <p className="mt-1 text-[12px] text-zinc-400">{g.note}</p>
              </div>
            ))}
          </div>
        </section>

        {/* The schools */}
        <section>
          <h2 className="mb-3 font-serif text-xl text-[color:var(--saffron)]">The schools</h2>
          <p className="mb-4 text-[13px] text-zinc-400">
            Each is the shared premise lived in a particular key. Start anywhere; the links go to
            the concepts and the texts.
          </p>
          <div className="space-y-3">
            {order.map((id) => {
              const s = schoolMap.get(id);
              if (!s) return null;
              return (
                <a key={id} href={`/traditions/${id}`} className="block rounded border border-zinc-800 bg-zinc-900/30 p-4 transition-colors hover:border-[color:var(--saffron)]">
                  <div className="flex items-baseline justify-between">
                    <span className="font-serif text-[16px] text-[color:var(--bone)]">{s.title}</span>
                    {s.sanskrit && <span className="text-[12px] text-zinc-500">{s.sanskrit}</span>}
                  </div>
                  <p className="mt-1 text-[13px] leading-relaxed text-zinc-300">{s.summary}</p>
                  {s.dossier?.doctrinalCore && (
                    <div className="mt-2 flex flex-wrap gap-1.5">
                      {s.dossier.doctrinalCore.slice(0, 3).map((d, i) => (
                        <span key={i} className="rounded border border-zinc-700/50 px-1.5 py-0.5 text-[10px] text-zinc-500">{d}</span>
                      ))}
                    </div>
                  )}
                </a>
              );
            })}
          </div>
        </section>

        <footer className="mt-10 border-t border-zinc-800 pt-4 text-[11px] text-zinc-500">
          Every concept here links down to its dossier and, through the reader, to the audited
          verses and their decisions. This is the learning layer — the translations are its source.
        </footer>
      </div>
    </main>
  );
}
