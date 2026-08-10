"use client";

import React, { useState } from "react";
import { audited } from "@/data/atlas";
import { seed } from "@/data/atlas";
import { BibliographyRecord, BibTranslation, BibSource, BibScholarship, ResourceTier } from "@/data/atlas";

const TIER_LABEL: Record<ResourceTier, string> = {
  A: "A critical",
  B: "B text-repo",
  C: "C discovery",
  D: "D niche",
  E: "E mirror",
};

const STATUS_STYLE: Record<string, { badge: string; dot: string }> = {
  complete: { badge: "border-emerald-800/60 text-emerald-300/90", dot: "bg-emerald-400" },
  partial: { badge: "border-amber-800/60 text-amber-300/90", dot: "bg-amber-400" },
  none: { badge: "border-zinc-700/60 text-zinc-400", dot: "bg-zinc-500" },
};

function Tier({ t }: { t?: ResourceTier }) {
  if (!t) return null;
  return (
    <span className="rounded border border-zinc-700/40 px-1 text-[9px] uppercase tracking-wider text-zinc-500">
      {TIER_LABEL[t]}
    </span>
  );
}

function TranslationItem({ tr }: { tr: BibTranslation }) {
  return (
    <li className="flex flex-wrap items-baseline gap-x-2 gap-y-0.5">
      <span className="text-[10px] uppercase tracking-wider text-zinc-500">{tr.language}</span>
      <span className="font-serif text-zinc-200">{tr.translator}</span>
      {tr.work && <span className="italic text-zinc-400">{tr.work}</span>}
      {tr.coverage && <span className="text-zinc-500">· {tr.coverage}</span>}
      <span className="text-[10px] uppercase tracking-wider text-zinc-500">{tr.type}</span>
      {tr.year && <span className="text-zinc-500">· {tr.year}</span>}
      <Tier t={tr.tier} />
      {tr.url && (
        <a href={tr.url} target="_blank" rel="noreferrer" className="text-[color:var(--saffron)] hover:underline">→</a>
      )}
      {tr.note && <span className="w-full text-[11px] text-zinc-500">{tr.note}</span>}
    </li>
  );
}

function SourceItem({ s }: { s: BibSource }) {
  return (
    <li className="flex flex-wrap items-baseline gap-x-2 gap-y-0.5">
      <span className="text-[10px] uppercase tracking-wider text-zinc-500">{s.type}</span>
      {s.coverage && <span className="text-zinc-400">{s.coverage}</span>}
      {s.editor && <span className="text-zinc-300">{s.editor}</span>}
      {s.year && <span className="text-zinc-500">· {s.year}</span>}
      {s.provider && <span className="text-zinc-500">· {s.provider}</span>}
      <Tier t={s.tier} />
      {s.url && <a href={s.url} target="_blank" rel="noreferrer" className="text-[color:var(--saffron)] hover:underline">→</a>}
      {s.note && <span className="w-full text-[11px] text-zinc-500">{s.note}</span>}
    </li>
  );
}

function ScholarshipItem({ s }: { s: BibScholarship }) {
  return (
    <li className="flex flex-wrap items-baseline gap-x-2 gap-y-0.5">
      {s.author && <span className="text-zinc-300">{s.author}</span>}
      <span className="italic text-zinc-400">{s.work}</span>
      {s.year && <span className="text-zinc-500">· {s.year}</span>}
      {s.kind && <span className="text-[10px] uppercase tracking-wider text-zinc-500">{s.kind}</span>}
      <Tier t={s.tier} />
      {s.url && <a href={s.url} target="_blank" rel="noreferrer" className="text-[color:var(--saffron)] hover:underline">→</a>}
    </li>
  );
}

function AuditedRecord({ r }: { r: BibliographyRecord }) {
  const st = STATUS_STYLE[r.translationStatus];
  const [open, setOpen] = useState(false);
  return (
    <li className="border-b border-zinc-800/70 py-4">
      <button onClick={() => setOpen(!open)} className="w-full text-left">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <span className="font-serif text-[15px] text-[color:var(--bone)]">{r.work}</span>
          <div className="flex items-center gap-2">
            <span className={`inline-flex items-center gap-1.5 rounded border px-2 py-0.5 text-[10px] ${st.badge}`}>
              <span className={`h-1.5 w-1.5 rounded-full ${st.dot}`} />{r.translationStatus}
            </span>
            <span className="text-[10px] text-zinc-500">{open ? "▾" : "▸"}</span>
          </div>
        </div>
        <p className="mt-1 text-[12px] text-zinc-400">{r.statusLabel}</p>
        <div className="mt-1 flex flex-wrap items-center gap-1.5 text-[10px] text-zinc-500">
          {r.traditions.map((t) => <span key={t} className="rounded border border-zinc-700/60 px-1.5 py-0.5 uppercase tracking-wider text-zinc-400">{t}</span>)}
          <span>checked {r.statusChecked}</span>
        </div>
      </button>
      {open && (
        <div className="mt-3 space-y-3 border-t border-zinc-800/50 pt-3">
          {r.statusEvidence && (
            <p className="rounded border border-zinc-800 bg-zinc-900/40 p-2 text-[12px] text-zinc-400">
              <span className="uppercase tracking-wider text-zinc-500">Evidence: </span>{r.statusEvidence}
            </p>
          )}
          {r.translations.length > 0 && (
            <div>
              <p className="mb-1 text-[10px] uppercase tracking-[0.2em] text-zinc-500">Translations</p>
              <ul className="space-y-1"><TranslationItem key={0} tr={r.translations[0]} />{r.translations.slice(1).map((t, i) => <TranslationItem key={i} tr={t} />)}</ul>
            </div>
          )}
          {r.textSources.length > 0 && (
            <div>
              <p className="mb-1 text-[10px] uppercase tracking-[0.2em] text-zinc-500">Sanskrit sources</p>
              <ul className="space-y-1">{r.textSources.map((s, i) => <SourceItem key={i} s={s} />)}</ul>
            </div>
          )}
          {r.scholarship && r.scholarship.length > 0 && (
            <div>
              <p className="mb-1 text-[10px] uppercase tracking-[0.2em] text-zinc-500">Scholarship</p>
              <ul className="space-y-1">{r.scholarship.map((s, i) => <ScholarshipItem key={i} s={s} />)}</ul>
            </div>
          )}
          {r.notes && r.notes.length > 0 && (
            <p className="text-[11px] text-zinc-500">{r.notes.join(" ")}</p>
          )}
        </div>
      )}
    </li>
  );
}

export default function BibliographyPage() {
  const complete = audited.filter((r) => r.translationStatus === "complete").length;
  const partial = audited.filter((r) => r.translationStatus === "partial").length;
  const none = audited.filter((r) => r.translationStatus === "none").length;

  return (
    <main className="min-h-screen bg-zinc-950 px-6 py-12 text-zinc-200">
      <div className="mx-auto max-w-3xl">
        <header className="mb-2">
          <p className="text-[10px] uppercase tracking-[0.3em] text-[color:var(--saffron)]">patala — tantra hub</p>
          <h1 className="mt-1 font-serif text-3xl text-[color:var(--bone)]">The Tantra Hub — Bibliography</h1>
          <p className="mt-2 text-sm text-zinc-400">
            A living register of the Śaiva textual landscape: what exists, where to read it, what has been translated, how scholars understand it.
          </p>
          <div className="mt-3 flex flex-wrap items-center gap-2">
            <a href="/read/kramasadbhava/1.8" className="inline-block rounded border border-[color:var(--saffron)] px-3 py-1.5 text-[12px] text-[color:var(--saffron)] hover:bg-[color:var(--saffron)] hover:text-zinc-950">
              → Read Kramasadbhāva 1.8 (auditable reader)
            </a>
            <a href="/texts/kramasadbhava" className="inline-block rounded border border-zinc-600 px-3 py-1.5 text-[12px] text-zinc-300 hover:border-[color:var(--saffron)] hover:text-[color:var(--saffron)]">
              Kramasadbhāva overview →
            </a>
            <a href="/resources" className="inline-block rounded border border-zinc-600 px-3 py-1.5 text-[12px] text-zinc-300 hover:border-[color:var(--saffron)] hover:text-[color:var(--saffron)]">
              External resources →
            </a>
            <a href="/concepts" className="inline-block rounded border border-zinc-600 px-3 py-1.5 text-[12px] text-zinc-300 hover:border-[color:var(--saffron)] hover:text-[color:var(--saffron)]">
              Concepts →
            </a>
            <a href="/learning" className="inline-block rounded border border-zinc-600 px-3 py-1.5 text-[12px] text-zinc-300 hover:border-[color:var(--saffron)] hover:text-[color:var(--saffron)]">
              Learn →
            </a>
          </div>
        </header>

        <div className="mb-6 flex flex-wrap gap-4 text-[12px] text-zinc-400">
          <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-full bg-emerald-400" /> {complete} complete</span>
          <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-full bg-amber-400" /> {partial} partial</span>
          <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-full bg-zinc-500" /> {none} no complete EN located</span>
          <span className="text-zinc-600">· {seed.length} seed records (not yet audited)</span>
        </div>

        <p className="mb-6 rounded border border-zinc-800 bg-zinc-900/50 p-3 text-[12px] leading-relaxed text-zinc-400">
          <span className="text-zinc-300">Audited records</span> distinguish root vs commentary, complete vs selected-chapter coverage,
          scholarly vs traditional/independent translation style, and language. Every resource carries a{" "}
          <span className="text-zinc-300">provenance tier</span> (A critical · B text-repo · C discovery · D niche · E mirror) — a provenance
          class, not intellectual quality. Status phrasing is deliberate: <span className="text-zinc-300">"No complete English translation
          located"</span>, not "Untranslated." This is the Trika-10 pass; the remaining schools are audited next.
        </p>

        <section>
          <h2 className="mb-2 font-serif text-lg text-[color:var(--saffron)]">Audited (Trika-10)</h2>
          <ul>{audited.map((r) => <AuditedRecord key={r.id} r={r} />)}</ul>
        </section>

        <section className="mt-10">
          <h2 className="mb-2 font-serif text-lg text-[color:var(--saffron)]">Seed — full-depth records, not yet gold-audited ({seed.length})</h2>
          <p className="mb-3 text-[12px] text-zinc-500">
            These carry the same full-depth structure as the audited Trika-10 (sources, translations, coverage, tiers) but verified:false — they await the per-school audit (Siddhānta → Bhairava → Kaula → Krama → Kubjikā → Pratyabhijñā).
          </p>
          <ul>
            {seed.map((r) => (
              <li key={r.id} className="flex flex-wrap items-center gap-2 border-b border-zinc-800/60 py-2 text-[13px]">
                <span className="text-zinc-300">{r.work}</span>
                {r.traditions.map((t: string) => <span key={t} className="text-[9px] uppercase tracking-wider text-zinc-500">{t}</span>)}
                <span className="ml-auto text-[10px] text-zinc-500">{r.statusLabel}</span>
              </li>
            ))}
          </ul>
        </section>

        <footer className="mt-12 border-t border-zinc-800 pt-4 text-[11px] text-zinc-500">
          The bibliography is the index joining everything together: manuscript → Sanskrit → published translation → working translation → scholarship → lecture → commentary → AI retrieval.
        </footer>
      </div>
    </main>
  );
}
