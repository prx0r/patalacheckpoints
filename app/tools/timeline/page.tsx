"use client";

// /tools/timeline — the diachronic Śiva source-tree (school genealogy).
import React, { useState } from "react";

export default function TimelinePage() {
  const [school, setSchool] = useState("trika");
  const [data, setData] = useState<any>(null);
  async function go() {
    const r = await fetch(`/api/products?verb=timeline&op=lineage&id=${encodeURIComponent(school)}`);
    setData(await r.json());
  }
  return (
    <main className="min-h-screen bg-zinc-950 px-6 py-12 text-zinc-200">
      <div className="mx-auto max-w-3xl">
        <header className="mb-4">
          <p className="text-[10px] uppercase tracking-[0.3em] text-[color:var(--saffron)]">patala — timeline</p>
          <h1 className="mt-1 font-serif text-3xl text-[color:var(--bone)]">The Śiva Source-Tree</h1>
          <p className="mt-2 text-sm text-zinc-400">the diachronic genealogy of a school's tradition.</p>
        </header>
        <div className="flex gap-2">
          <input value={school} onChange={(e) => setSchool(e.target.value)} className="rounded border border-zinc-700 bg-zinc-900 px-3 py-2 text-sm" />
          <button onClick={go} className="rounded bg-[color:var(--saffron)] px-4 py-2 text-sm text-zinc-950">Trace lineage</button>
        </div>
        {data && data.length > 0 && (
          <ol className="mt-4 space-y-1">
            {data.map((s: any, i: number) => (
              <li key={i} className="rounded border border-zinc-800 p-2 text-xs">
                <span className="text-[color:var(--bone)]">{s.name}</span>
                <span className="text-zinc-600"> — {s.id}</span>
                <span className="ml-2 text-zinc-500">[{JSON.stringify(s.period)}]</span>
              </li>
            ))}
          </ol>
        )}
      </div>
    </main>
  );
}
