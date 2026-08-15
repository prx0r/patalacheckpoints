"use client";

// /tools/crux — the minimal divergence between two positions.
import React, { useState } from "react";

export default function CruxPage() {
  const [a, setA] = useState("ARG:pt:passage:ipvv:chunkA-svatyandya.md");
  const [b, setB] = useState("ARG:pt:passage:ipvv:chunkB-eligibility-gita.md");
  const [crux, setCrux] = useState<any>(null);
  async function go() {
    const r = await fetch(`/api/products?verb=crux&a=${encodeURIComponent(a)}&b=${encodeURIComponent(b)}`);
    setCrux(await r.json());
  }
  return (
    <main className="min-h-screen bg-zinc-950 px-6 py-12 text-zinc-200">
      <div className="mx-auto max-w-3xl">
        <header className="mb-4">
          <p className="text-[10px] uppercase tracking-[0.3em] text-[color:var(--saffron)]">patala — crux</p>
          <h1 className="mt-1 font-serif text-3xl text-[color:var(--bone)]">Crux Compiler</h1>
          <p className="mt-2 text-sm text-zinc-400">the minimal divergence between two positions — the load-bearing disagreement.</p>
        </header>
        <div className="flex flex-col gap-2">
          <input value={a} onChange={(e) => setA(e.target.value)} className="rounded border border-zinc-700 bg-zinc-900 px-3 py-2 text-xs" />
          <input value={b} onChange={(e) => setB(e.target.value)} className="rounded border border-zinc-700 bg-zinc-900 px-3 py-2 text-xs" />
          <button onClick={go} className="rounded bg-[color:var(--saffron)] px-4 py-2 text-sm text-zinc-950">Compute crux</button>
        </div>
        {crux && (
          <div className="mt-4 rounded border border-zinc-800 p-4 text-xs">
            <p>crux_count: <span className="text-[color:var(--saffron)]">{crux.crux_count}</span></p>
            <p className="mt-2 text-zinc-400">a_asserts: {(crux.crux_a_asserts ?? []).slice(0, 2).join(" · ")}</p>
            <p className="text-zinc-400">b_asserts: {(crux.crux_b_asserts ?? []).slice(0, 2).join(" · ")}</p>
          </div>
        )}
      </div>
    </main>
  );
}
