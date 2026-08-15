"use client";

// /queue — what needs review next (the prioritized review queue).
import React, { useEffect, useState } from "react";

export default function QueuePage() {
  const [data, setData] = useState<any>(null);
  useEffect(() => {
    fetch("/api/products?verb=review_queue").then((r) => r.json()).then(setData).catch(() => setData({ error: "queue unavailable" }));
  }, []);
  return (
    <main className="min-h-screen bg-zinc-950 px-6 py-12 text-zinc-200">
      <div className="mx-auto max-w-3xl">
        <header className="mb-4">
          <p className="text-[10px] uppercase tracking-[0.3em] text-[color:var(--saffron)]">patala — review queue</p>
          <h1 className="mt-1 font-serif text-3xl text-[color:var(--bone)]">What Needs Review</h1>
          <p className="mt-2 text-sm text-zinc-400">
            a prioritized queue (uncertainty × blast-radius × centrality / cost) — not a flat list.
          </p>
        </header>
        {!data && <p className="text-sm text-zinc-500">loading…</p>}
        {data?.error && <p className="text-sm text-red-400">{data.error}</p>}
        {data?.queue?.length ? (
          <ul className="space-y-2">
            {data.queue.map((q: any, i: number) => (
              <li key={i} className="rounded border border-zinc-800 p-3 text-xs">
                <div className="flex justify-between">
                  <span className="text-[color:var(--bone)]">{q.object_id.slice(0, 50)}</span>
                  <span className="text-[color:var(--saffron)]">priority {q.priority}</span>
                </div>
                <div className="mt-1 text-zinc-500">
                  {q.layer} · state {q.state} · blast_radius {q.blast_radius}
                </div>
              </li>
            ))}
          </ul>
        ) : data && !data.error ? <p className="text-sm text-zinc-500">no queue.</p> : null}
      </div>
    </main>
  );
}
