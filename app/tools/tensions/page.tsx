"use client";

// /tools/tensions — where interpretations diverge (the tension finder).
// Reads the real tension surface from the API.
import React, { useEffect, useState } from "react";

export default function TensionsPage() {
  const [data, setData] = useState<any>(null);
  useEffect(() => {
    fetch("/api/products?verb=tension").then((r) => r.json()).then(setData).catch(() => setData({ error: "tension_finder unavailable" }));
  }, []);
  return (
    <main className="min-h-screen bg-zinc-950 px-6 py-12 text-zinc-200">
      <div className="mx-auto max-w-3xl">
        <header className="mb-4">
          <p className="text-[10px] uppercase tracking-[0.3em] text-[color:var(--saffron)]">patala — tension finder</p>
          <h1 className="mt-1 font-serif text-3xl text-[color:var(--bone)]">Interesting Tensions</h1>
          <p className="mt-2 text-sm text-zinc-400">where interpretations diverge — the places papers come from.</p>
        </header>
        {!data && <p className="text-sm text-zinc-500">loading…</p>}
        {data?.error && <p className="text-sm text-red-400">{data.error}</p>}
        <ul className="space-y-2">
          {(data?.tensions ?? []).slice(0, 20).map((t: any, i: number) => (
            <li key={i} className="rounded border border-zinc-800 p-3">
              <div className="flex justify-between text-xs">
                <span className="text-[color:var(--saffron)]">{t.kind}</span>
                <span className="text-zinc-600">score {t.score}</span>
              </div>
              <p className="mt-1 text-sm text-[color:var(--bone)]">
                {(t.passage_id || t.term || t.note || "").slice(0, 120)}
              </p>
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
}
