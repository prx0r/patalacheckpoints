"use client";

import React, { useMemo, useState } from "react";
import { concepts } from "@/data/atlas";
import type { AtlasEntity } from "@/lib/atlas";

function ConceptCard({ c }: { c: AtlasEntity }) {
  return (
    <li className="border-b border-zinc-800/70 py-3">
      <a href={`/concepts/${c.id}`} className="block">
        <div className="flex items-baseline justify-between">
          <span className="font-serif text-[15px] text-[color:var(--bone)]">{c.title}</span>
          {c.sanskrit && <span className="text-[13px] text-zinc-500">{c.sanskrit}</span>}
        </div>
        <p className="mt-1 line-clamp-2 text-[12px] leading-relaxed text-zinc-400">{c.summary}</p>
        {c.period && (
          <p className="mt-1 text-[10px] text-zinc-600">
            {c.period.start ?? ""}–{c.period.end ?? ""} {c.period.approximate ? "≈" : ""}
          </p>
        )}
      </a>
    </li>
  );
}

export default function ConceptsPage() {
  const [q, setQ] = useState("");
  const sorted = useMemo(() => [...concepts].sort((a, b) => a.title.localeCompare(b.title)), []);
  const filtered = q ? sorted.filter((c) => c.title.toLowerCase().includes(q.toLowerCase()) || (c.sanskrit ?? "").includes(q)) : sorted;

  return (
    <main className="min-h-screen bg-zinc-950 px-6 py-12 text-zinc-200">
      <div className="mx-auto max-w-3xl">
        <header className="mb-2">
          <p className="text-[10px] uppercase tracking-[0.3em] text-[color:var(--saffron)]">patala — tantra hub</p>
          <h1 className="mt-1 font-serif text-3xl text-[color:var(--bone)]">Concepts</h1>
          <p className="mt-2 text-sm text-zinc-400">
            The key terms of the corpus, each with its sense-trajectory across traditions — the
            semantic web that connects the texts. Every concept carries its dossier: what it does,
            its doctrinal core, and where it runs through the canon.
          </p>
          <div className="mt-3">
            <a href="/" className="inline-block rounded border border-zinc-600 px-3 py-1.5 text-[12px] text-zinc-300 hover:border-[color:var(--saffron)] hover:text-[color:var(--saffron)]">← Atlas</a>
          </div>
        </header>

        <div className="mb-6">
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Filter concepts…"
            className="w-full rounded border border-zinc-700 bg-zinc-900/50 px-3 py-2 text-sm text-zinc-200 placeholder-zinc-600 focus:border-[color:var(--saffron)] focus:outline-none"
          />
        </div>

        <section>
          <p className="mb-2 text-[10px] uppercase tracking-[0.2em] text-zinc-500">{filtered.length} concepts</p>
          <ul>{filtered.map((c) => <ConceptCard key={c.id} c={c} />)}</ul>
        </section>

        <footer className="mt-10 border-t border-zinc-800 pt-4 text-[11px] text-zinc-500">
          Each concept is a node in the atlas graph — its edges are the lemma-trajectories, the
          citations, and the semantic shifts that connect the corpus.
        </footer>
      </div>
    </main>
  );
}
