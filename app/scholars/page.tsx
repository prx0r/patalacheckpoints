"use client";

// /scholars — the contribution ledger: what scholars have reviewed/attested.
// Humans read; agents call the same via MCP (patala_scholar_profile / patala_scholar_publication).
import React, { useEffect, useState } from "react";

export default function ScholarsPage() {
  const [data, setData] = useState<any>(null);
  useEffect(() => {
    fetch("/api/scholar?verb=audit").then((r) => r.json()).then(setData).catch(() => setData({ error: "scholar API unavailable" }));
  }, []);
  return (
    <main className="min-h-screen bg-zinc-950 px-6 py-12 text-zinc-200">
      <div className="mx-auto max-w-3xl">
        <header className="mb-4">
          <p className="text-[10px] uppercase tracking-[0.3em] text-[color:var(--saffron)]">patala — scholars</p>
          <h1 className="mt-1 font-serif text-3xl text-[color:var(--bone)]">Scholars</h1>
          <p className="mt-2 text-sm text-zinc-400">
            the contribution ledger — a map of what kind of scholarship each scholar does. Reviews and
            attestations are append-only and citable.
          </p>
        </header>
        {!data && <p className="text-sm text-zinc-500">loading…</p>}
        {data?.error && <p className="text-sm text-red-400">{data.error}</p>}
        {data && (
          <div className="rounded border border-zinc-800 p-4 text-xs">
            <p><span className="text-zinc-500">objects:</span> {data.objects}</p>
            <p><span className="text-zinc-500">reviews in ledger:</span> {data.reviews_in_ledger}</p>
            <p><span className="text-zinc-500">attestations signed:</span> {data.attestations_signed}</p>
            <p><span className="text-zinc-500">unreviewed objects:</span> {data.unreviewed_objects}</p>
            <div className="mt-2">
              <span className="text-zinc-500">layers:</span>
              <div className="mt-1 flex flex-wrap gap-1">
                {Object.entries(data.layers ?? {}).map(([k, v]) => (
                  <span key={k} className="rounded bg-zinc-900 px-2 py-0.5">{k}={v}</span>
                ))}
              </div>
            </div>
          </div>
        )}
        <p className="mt-4 text-xs text-zinc-600">
          To see a scholar's full contribution profile (reviews by decision, attestations), your AI can
          call <code>patala_scholar_profile</code> — or the review screen shows individual objects.
        </p>
      </div>
    </main>
  );
}
