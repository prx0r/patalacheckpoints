"use client";

import React, { useEffect, useState } from "react";
import { traditions, getEntity, getRelationsFor } from "@/data/atlas";
import type { AtlasEntity } from "@/lib/atlas";

export default function TraditionPage({ params }: { params: Promise<{ slug: string }> }) {
  const [slug, setSlug] = useState<string>("");
  const [t, setT] = useState<AtlasEntity | null>(null);

  useEffect(() => {
    params.then((p) => {
      setSlug(p.slug);
      const found = getEntity(p.slug);
      setT(found && found.type === "tradition" ? found : null);
    });
  }, [params]);

  if (!slug) return <main className="min-h-screen bg-zinc-950 px-6 py-12 text-zinc-500">Loading…</main>;
  if (!t) {
    return (
      <main className="min-h-screen bg-zinc-950 px-6 py-12 text-zinc-300">
        <p className="text-zinc-500">No tradition <code>{slug}</code>.</p>
        <a href="/learning" className="mt-3 inline-block text-sm text-[color:var(--saffron)] hover:underline">← Learning</a>
      </main>
    );
  }

  const related = (t.concepts ?? []).map((id) => getEntity(id)).filter(Boolean) as AtlasEntity[];
  const relations = getRelationsFor(t.id);

  return (
    <main className="min-h-screen bg-zinc-950 px-6 py-12 text-zinc-200">
      <div className="mx-auto max-w-3xl">
        <header className="mb-6">
          <p className="text-[10px] uppercase tracking-[0.3em] text-[color:var(--saffron)]">tradition</p>
          <div className="mt-1 flex items-baseline gap-3">
            <h1 className="font-serif text-3xl text-[color:var(--bone)]">{t.title}</h1>
            {t.sanskrit && <span className="text-xl text-zinc-500">{t.sanskrit}</span>}
          </div>
          {t.period && (
            <p className="mt-1 text-[12px] text-zinc-500">
              {t.period.start ?? ""}–{t.period.end ?? ""} {t.period.approximate ? "≈" : ""}
            </p>
          )}
          <div className="mt-3">
            <a href="/learning" className="text-sm text-zinc-400 hover:text-[color:var(--saffron)]">← Learning</a>
          </div>
        </header>

        <section className="mb-6">
          <p className="text-[15px] leading-relaxed text-zinc-200">{t.summary}</p>
        </section>

        {t.dossier && (
          <div className="mb-6 space-y-4 rounded border border-zinc-800 bg-zinc-900/30 p-5">
            <p className="text-[10px] uppercase tracking-[0.2em] text-[color:var(--saffron)]">Dossier</p>
            {t.dossier.systemicFunction && (
              <p className="text-[13px] leading-relaxed text-zinc-300">{t.dossier.systemicFunction}</p>
            )}
            {t.dossier.doctrinalCore && t.dossier.doctrinalCore.length > 0 && (
              <div>
                <p className="mb-1 text-[10px] uppercase tracking-wider text-zinc-500">Doctrinal core</p>
                <ul className="space-y-1">
                  {t.dossier.doctrinalCore.map((d, i) => (
                    <li key={i} className="flex items-start gap-2 text-[13px] text-zinc-300">
                      <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-[color:var(--saffron)]" />
                      {d}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {t.dossier.outputs && t.dossier.outputs.length > 0 && (
              <div>
                <p className="mb-1 text-[10px] uppercase tracking-wider text-zinc-500">Outputs</p>
                <ul className="space-y-1">
                  {t.dossier.outputs.map((o, i) => (
                    <li key={i} className="text-[12px] text-zinc-400">{o}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {related.length > 0 && (
          <section className="mb-6">
            <p className="mb-2 text-[10px] uppercase tracking-[0.2em] text-zinc-500">Key concepts</p>
            <div className="flex flex-wrap gap-2">
              {related.map((r) => (
                <a key={r.id} href={`/concepts/${r.id}`} className="rounded border border-zinc-700/60 px-2 py-0.5 text-[12px] text-zinc-300 hover:border-[color:var(--saffron)] hover:text-[color:var(--saffron)]">
                  {r.title} →
                </a>
              ))}
            </div>
          </section>
        )}

        {t.resources && t.resources.length > 0 && (
          <section className="mb-6">
            <p className="mb-2 text-[10px] uppercase tracking-[0.2em] text-zinc-500">Read &amp; study</p>
            <ul className="space-y-1">
              {t.resources.map((r, i) => (
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
                  {r.source === t.id ? t.title : r.source} → {r.type} → {r.target === t.id ? t.title : r.target}
                </li>
              ))}
            </ul>
          </section>
        )}

        <footer className="mt-10 border-t border-zinc-800 pt-4 text-[11px] text-zinc-500">
          The tradition is a dialect of the shared foundations — the same premise lived in a
          particular key, with its own texts, concepts, and path.
        </footer>
      </div>
    </main>
  );
}
