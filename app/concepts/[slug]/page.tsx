"use client";

import React, { useEffect, useState } from "react";
import { concepts, getEntity, getRelationsFor } from "@/data/atlas";
import type { AtlasEntity } from "@/lib/atlas";

export default function ConceptPage({ params }: { params: Promise<{ slug: string }> }) {
  const [slug, setSlug] = useState<string>("");
  const [c, setC] = useState<AtlasEntity | null>(null);

  useEffect(() => {
    params.then((p) => {
      setSlug(p.slug);
      const found = getEntity(p.slug);
      setC(found && found.type === "concept" ? found : null);
    });
  }, [params]);

  if (!slug) return <main className="min-h-screen bg-zinc-950 px-6 py-12 text-zinc-500">Loading…</main>;
  if (!c) {
    return (
      <main className="min-h-screen bg-zinc-950 px-6 py-12 text-zinc-300">
        <p className="text-zinc-500">No concept <code>{slug}</code>.</p>
        <a href="/concepts" className="mt-3 inline-block text-sm text-[color:var(--saffron)] hover:underline">← All concepts</a>
      </main>
    );
  }

  const related = (c.concepts ?? []).map((id) => getEntity(id)).filter(Boolean) as AtlasEntity[];
  const relations = getRelationsFor(c.id);

  return (
    <main className="min-h-screen bg-zinc-950 px-6 py-12 text-zinc-200">
      <div className="mx-auto max-w-3xl">
        <header className="mb-6">
          <p className="text-[10px] uppercase tracking-[0.3em] text-[color:var(--saffron)]">concept</p>
          <div className="mt-1 flex items-baseline gap-3">
            <h1 className="font-serif text-3xl text-[color:var(--bone)]">{c.title}</h1>
            {c.sanskrit && <span className="text-xl text-zinc-500">{c.sanskrit}</span>}
          </div>
          {c.period && (
            <p className="mt-1 text-[12px] text-zinc-500">
              {c.period.start ?? ""}–{c.period.end ?? ""} {c.period.approximate ? "≈" : ""}
            </p>
          )}
          <div className="mt-3">
            <a href="/concepts" className="text-sm text-zinc-400 hover:text-[color:var(--saffron)]">← All concepts</a>
          </div>
        </header>

        <section className="mb-6">
          <p className="text-[15px] leading-relaxed text-zinc-200">{c.summary}</p>
        </section>

        {c.dossier && (
          <div className="mb-6 space-y-4 rounded border border-zinc-800 bg-zinc-900/30 p-5">
            <p className="text-[10px] uppercase tracking-[0.2em] text-[color:var(--saffron)]">Dossier</p>
            {c.dossier.systemicFunction && (
              <p className="text-[13px] leading-relaxed text-zinc-300">{c.dossier.systemicFunction}</p>
            )}
            {c.dossier.doctrinalCore && c.dossier.doctrinalCore.length > 0 && (
              <div>
                <p className="mb-1 text-[10px] uppercase tracking-wider text-zinc-500">Doctrinal core</p>
                <ul className="space-y-1">
                  {c.dossier.doctrinalCore.map((d, i) => (
                    <li key={i} className="flex items-start gap-2 text-[13px] text-zinc-300">
                      <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-[color:var(--saffron)]" />
                      {d}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {c.dossier.outputs && c.dossier.outputs.length > 0 && (
              <div>
                <p className="mb-1 text-[10px] uppercase tracking-wider text-zinc-500">Outputs</p>
                <ul className="space-y-1">
                  {c.dossier.outputs.map((o, i) => (
                    <li key={i} className="text-[12px] text-zinc-400">{o}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {related.length > 0 && (
          <section className="mb-6">
            <p className="mb-2 text-[10px] uppercase tracking-[0.2em] text-zinc-500">Related concepts</p>
            <div className="flex flex-wrap gap-2">
              {related.map((r) => (
                <a key={r.id} href={`/concepts/${r.id}`} className="rounded border border-zinc-700/60 px-2 py-0.5 text-[12px] text-zinc-300 hover:border-[color:var(--saffron)] hover:text-[color:var(--saffron)]">
                  {r.title}
                </a>
              ))}
            </div>
          </section>
        )}

        {c.resources && c.resources.length > 0 && (
          <section className="mb-6">
            <p className="mb-2 text-[10px] uppercase tracking-[0.2em] text-zinc-500">Resources</p>
            <ul className="space-y-1">
              {c.resources.map((r, i) => (
                <li key={i}>
                  <a href={r.href} className="text-[13px] text-zinc-300 hover:text-[color:var(--saffron)]">
                    {r.title} <span className="text-[10px] uppercase text-zinc-600">· {r.type}</span> →
                  </a>
                </li>
              ))}
            </ul>
          </section>
        )}

        {relations.length > 0 && (
          <section className="mb-6">
            <p className="mb-2 text-[10px] uppercase tracking-[0.2em] text-zinc-500">Relations in the atlas</p>
            <ul className="space-y-1">
              {relations.map((r, i) => (
                <li key={i} className="text-[12px] text-zinc-400">
                  {r.source === c.id ? c.title : r.source} → {r.type} → {r.target === c.id ? c.title : r.target}
                </li>
              ))}
            </ul>
          </section>
        )}

        <footer className="mt-10 border-t border-zinc-800 pt-4 text-[11px] text-zinc-500">
          The dossier is the deep content — the sense-trajectory, the doctrine, the loci. Every
          claim resolves to passages and decisions in the reader.
        </footer>
      </div>
    </main>
  );
}
