"use client";

// /tools/terminology — a lemma's sense-trajectory across traditions.
import React, { useState } from "react";

export default function TerminologyPage() {
  const [lemma, setLemma] = useState("kula");
  const [data, setData] = useState<any>(null);
  async function go() {
    const r = await fetch(`/api/products?verb=terminology&lemma=${encodeURIComponent(lemma)}&op=trajectory`);
    setData(await r.json());
  }
  return (
    <main className="min-h-screen bg-zinc-950 px-6 py-12 text-zinc-200">
      <div className="mx-auto max-w-3xl">
        <header className="mb-4">
          <p className="text-[10px] uppercase tracking-[0.3em] text-[color:var(--saffron)]">patala — terminology</p>
          <h1 className="mt-1 font-serif text-3xl text-[color:var(--bone)]">Term Trajectories</h1>
          <p className="mt-2 text-sm text-zinc-400">how a lemma's sense shifts across traditions and periods.</p>
        </header>
        <div className="flex gap-2">
          <input value={lemma} onChange={(e) => setLemma(e.target.value)} className="rounded border border-zinc-700 bg-zinc-900 px-3 py-2 text-sm" />
          <button onClick={go} className="rounded bg-[color:var(--saffron)] px-4 py-2 text-sm text-zinc-950">Trace</button>
        </div>
        <ul className="mt-4 space-y-2">
          {(data?.trajectory ?? []).map((s: any, i: number) => (
            <li key={i} className="rounded border border-zinc-800 p-3 text-xs">
              <span className="text-[color:var(--bone)]">{s.period}</span>
              <span className="text-zinc-500"> → {s.sense_id}</span>
              <span className="ml-2 text-zinc-600">({s.status}/{s.certainty})</span>
              <p className="mt-1 text-zinc-400">{s.claim}</p>
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
}
