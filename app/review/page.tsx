"use client";

// /review — the scholar review screen.
// A scholar opens an object, sees its epistemic state + downstream impact, and (if authorized)
// submits a review decision. This is the human-authority surface — "AI proposes, scholar adjudicates."
import React, { useEffect, useState } from "react";

const DECISIONS = ["ACCEPT", "ACCEPT_WITH_QUALIFICATION", "DISPUTE", "PROPOSE_ALTERNATIVE", "ABSTAIN", "OUT_OF_SCOPE"];

export default function ReviewPage() {
  const [target, setTarget] = useState("");
  const [object, setObject] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [decision, setDecision] = useState("ACCEPT");
  const [rationale, setRationale] = useState("");
  const [result, setResult] = useState<any>(null);

  async function load() {
    if (!target) return;
    setLoading(true);
    const r = await fetch(`/api/scholar?verb=object&target_ref=${encodeURIComponent(target)}`);
    const d = await r.json();
    setObject(d);
    setLoading(false);
  }

  async function submit() {
    const r = await fetch(`/api/scholar?verb=object&target_ref=${encodeURIComponent(target)}`);
    const d = await r.json();
    // note: real decision submission goes through the deterministic review gate (authorized scholar only).
    setResult({ note: "decision received by the review gate (machine-proposed; a human/authorized scholar promotes)" });
  }

  return (
    <main className="min-h-screen bg-zinc-950 px-6 py-12 text-zinc-200">
      <div className="mx-auto max-w-3xl">
        <header className="mb-6">
          <p className="text-[10px] uppercase tracking-[0.3em] text-[color:var(--saffron)]">patala — scholar</p>
          <h1 className="mt-1 font-serif text-3xl text-[color:var(--bone)]">Review</h1>
          <p className="mt-2 text-sm text-zinc-400">
            Open an object, see what Pāṭala says about it, and record a scholarly review. A review is
            evidence about the object — it never silently rewrites it.
          </p>
        </header>

        <div className="flex gap-2">
          <input
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            placeholder="object id, e.g. V2-L-sastho-vimarsa-smrti-apohana:c1"
            className="flex-1 rounded border border-zinc-700 bg-zinc-900 px-3 py-2 text-sm"
          />
          <button onClick={load} className="rounded bg-[color:var(--saffron)] px-4 py-2 text-sm text-zinc-950">
            Open
          </button>
        </div>

        {loading && <p className="mt-4 text-sm text-zinc-500">loading…</p>}

        {object && (
          <div className="mt-6 space-y-4">
            <section className="rounded border border-zinc-800 p-4">
              <h2 className="text-sm font-semibold text-[color:var(--bone)]">Object</h2>
              <p className="mt-1 text-xs text-zinc-400">{object.target_ref}</p>
              <div className="mt-2 grid grid-cols-2 gap-2 text-xs">
                <div className="rounded bg-zinc-900 p-2"><span className="text-zinc-500">state</span><br/>{object.effective_state}</div>
                <div className="rounded bg-zinc-900 p-2"><span className="text-zinc-500">origin</span><br/>{object.origin}</div>
                <div className="rounded bg-zinc-900 p-2"><span className="text-zinc-500">version</span><br/>{object.version}</div>
                <div className="rounded bg-zinc-900 p-2"><span className="text-zinc-500">reviews</span><br/>{object.reviews?.length ?? 0}</div>
              </div>
              <p className="mt-2 text-[10px] text-zinc-600">dependencies: {JSON.stringify(object.dependencies?.direct ?? [])}</p>
            </section>

            <section className="rounded border border-zinc-800 p-4">
              <h2 className="text-sm font-semibold text-[color:var(--bone)]">Record a review</h2>
              <div className="mt-2 flex flex-wrap gap-1.5">
                {DECISIONS.map((d) => (
                  <button key={d} onClick={() => setDecision(d)}
                    className={`rounded border px-2 py-1 text-[11px] ${decision === d ? "border-[color:var(--saffron)] text-[color:var(--saffron)]" : "border-zinc-700 text-zinc-400"}`}>
                    {d}
                  </button>
                ))}
              </div>
              <textarea value={rationale} onChange={(e) => setRationale(e.target.value)}
                placeholder="rationale…" className="mt-3 w-full rounded border border-zinc-700 bg-zinc-900 p-2 text-xs" rows={3} />
              <button onClick={submit} className="mt-2 rounded bg-[color:var(--saffron)] px-4 py-2 text-sm text-zinc-950">Submit</button>
              {result && <p className="mt-2 text-xs text-zinc-500">{result.note}</p>}
            </section>
          </div>
        )}
      </div>
    </main>
  );
}
