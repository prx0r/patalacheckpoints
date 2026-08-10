"use client";

import React, { useMemo, useState } from "react";
import { resources } from "@/data/atlas/resources";
import { Resource, ResourceType, TYPE_LABEL, Tradition } from "@/data/atlas/resourcesTypes";

const ACCESS_LABEL: Record<Resource["access"], string> = {
  free: "Free",
  free_donation: "Free / donation",
  mixed: "Mixed",
  paid: "Paid",
};

const RIGHTS_LABEL: Record<string, string> = {
  open: "Open",
  public_domain: "Public domain",
  permission: "Permission needed",
  restricted: "Restricted",
  mixed: "Mixed rights",
  unknown: "Unknown",
};

function TypePill({ t, active, onClick }: { t: ResourceType; active: boolean; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`rounded border px-2 py-0.5 text-[10px] uppercase tracking-wider transition-colors ${
        active
          ? "border-[color:var(--saffron)] bg-[color:var(--saffron)]/10 text-[color:var(--saffron)]"
          : "border-zinc-700/60 text-zinc-400 hover:border-zinc-500 hover:text-zinc-200"
      }`}
    >
      {TYPE_LABEL[t]}
    </button>
  );
}

function TradPill({ t, active, onClick }: { t: Tradition; active: boolean; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`rounded border px-2 py-0.5 text-[10px] uppercase tracking-wider transition-colors ${
        active
          ? "border-emerald-800/60 bg-emerald-900/20 text-emerald-300"
          : "border-zinc-800/80 text-zinc-500 hover:border-zinc-600 hover:text-zinc-300"
      }`}
    >
      {t}
    </button>
  );
}

function ResourceCard({ r }: { r: Resource }) {
  const [open, setOpen] = useState(false);
  const shown = r.types.slice(0, 3);
  const rest = r.types.slice(3);
  return (
    <li className="border-b border-zinc-800/70 py-4">
      <button onClick={() => setOpen(!open)} className="w-full text-left">
        <div className="flex items-center justify-between gap-2">
          <span className="font-serif text-[15px] text-[color:var(--bone)]">
            {r.essential && <span title="essential">● </span>}
            {r.name}
          </span>
          <span className="text-[10px] text-zinc-500">{open ? "▾" : "▸"}</span>
        </div>
        <div className="mt-1 flex flex-wrap items-center gap-1.5 text-[10px] text-zinc-500">
          <span className={`rounded px-1.5 py-0.5 uppercase tracking-wider ${
            r.status === "public"
              ? "border border-emerald-800/50 text-emerald-400/80"
              : "border border-amber-800/50 text-amber-400/80"
          }`}>
            {r.status}
          </span>
          <span className="text-zinc-600">·</span>
          <span>{ACCESS_LABEL[r.access]}</span>
          {r.machine_readable && <span className="text-zinc-600">· machine-readable</span>}
          {r.essential && <span className="text-[color:var(--saffron)]">· essential</span>}
        </div>
        <p className="mt-1.5 line-clamp-2 text-[12px] leading-relaxed text-zinc-400">{r.note}</p>
      </button>
      {open && (
        <div className="mt-3 space-y-3 border-t border-zinc-800/50 pt-3">
          <p className="text-[12px] leading-relaxed text-zinc-400">{r.note}</p>

          <div className="flex flex-wrap gap-1.5">
            {r.types.map((t) => <TypePill key={t} t={t} active={false} onClick={() => {}} />)}
            {shown.length < r.types.length && null}
          </div>
          {rest.length > 0 && <span className="text-[10px] text-zinc-600">… +{rest.length} more types</span>}

          <div className="flex flex-wrap gap-1.5">
            {r.traditions.map((t) => <TradPill key={t} t={t} active={false} onClick={() => {}} />)}
          </div>

          <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-[11px] text-zinc-500">
            {r.access && <span>Access: <span className="text-zinc-300">{ACCESS_LABEL[r.access]}</span></span>}
            {r.rights && <span>Rights: <span className="text-zinc-300">{RIGHTS_LABEL[r.rights]}</span></span>}
            {r.machine_readable && <span>Machine-readable: yes</span>}
            <span>Rehostable: <span className="text-zinc-300">{r.can_rehost ? "yes" : "no — index/link only"}</span></span>
          </div>

          <div className="space-y-1">
            {r.url && (
              <a href={r.url} target="_blank" rel="noreferrer" className="block text-[13px] text-[color:var(--saffron)] hover:underline">
                ↗ {r.url.replace(/^https?:\/\//, "")}
              </a>
            )}
            {r.links?.map((l) => (
              <a key={l.url} href={l.url} target="_blank" rel="noreferrer" className="block text-[12px] text-zinc-300 hover:text-[color:var(--saffron)]">
                {l.label || l.url.replace(/^https?:\/\//, "")} →
              </a>
            ))}
          </div>

          {r.works && r.works.length > 0 && (
            <div>
              <p className="mb-1 text-[10px] uppercase tracking-[0.2em] text-zinc-500">Curated texts</p>
              <ul className="space-y-0.5">
                {r.works.map((w) => (
                  <li key={w.url}>
                    <a href={w.url} target="_blank" rel="noreferrer" className="text-[12px] text-zinc-300 hover:text-[color:var(--saffron)]">
                      {w.label} →
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </li>
  );
}

export default function ResourcesPage() {
  const [typeFilter, setTypeFilter] = useState<ResourceType | null>(null);
  const [tradFilter, setTradFilter] = useState<Tradition | null>(null);

  const allTypes = useMemo(() => Array.from(new Set(resources.flatMap((r) => r.types))).sort(), []);
  const allTrads = useMemo(() => Array.from(new Set(resources.flatMap((r) => r.traditions))).sort(), []);
  const essentialCount = resources.filter((r) => r.essential).length;

  const filtered = useMemo(() => {
    return resources.filter((r) => {
      if (typeFilter && !r.types.includes(typeFilter)) return false;
      if (tradFilter && !r.traditions.includes(tradFilter)) return false;
      return true;
    });
  }, [typeFilter, tradFilter]);

  const essentialOnly = resources.filter((r) => r.essential);

  return (
    <main className="min-h-screen bg-zinc-950 px-6 py-12 text-zinc-200">
      <div className="mx-auto max-w-3xl">
        <header className="mb-2">
          <p className="text-[10px] uppercase tracking-[0.3em] text-[color:var(--saffron)]">patala — tantra hub</p>
          <h1 className="mt-1 font-serif text-3xl text-[color:var(--bone)]">Resources</h1>
          <p className="mt-2 text-sm text-zinc-400">
            A living federation of the external sources for the Śaiva textual landscape — joined here rather than rehosted.
            Every resource is typed and tagged by tradition, and carries an access, rights, and rehosting note.
          </p>
          <div className="mt-3 flex flex-wrap items-center gap-2">
            <a href="/bibliography" className="inline-block rounded border border-zinc-600 px-3 py-1.5 text-[12px] text-zinc-300 hover:border-[color:var(--saffron)] hover:text-[color:var(--saffron)]">
              ← Bibliography
            </a>
            <a href="/texts/kramasadbhava" className="inline-block rounded border border-zinc-600 px-3 py-1.5 text-[12px] text-zinc-300 hover:border-[color:var(--saffron)] hover:text-[color:var(--saffron)]">
              Kramasadbhāva overview →
            </a>
          </div>
        </header>

        <div className="mb-6 flex flex-wrap gap-4 text-[12px] text-zinc-400">
          <span>{resources.length} sources indexed</span>
          <span className="text-zinc-600">·</span>
          <span className="flex items-center gap-1.5">
            <span className="inline-block h-2 w-2 rounded-full border border-[color:var(--saffron)]" /> {essentialCount} essential
          </span>
          <span className="text-zinc-600">·</span>
          <span>machine-readable: {resources.filter((r) => r.machine_readable).length}</span>
        </div>

        <p className="mb-6 rounded border border-zinc-800 bg-zinc-900/50 p-3 text-[12px] leading-relaxed text-zinc-400">
          <span className="text-zinc-300">Public</span> resources are verified and published.{" "}
          <span className="text-zinc-300">Discovery</span> resources need individual review before being treated as authoritative.
          Several sources (SanskritDocuments, ShivaShakti, Wisdom Library) explicitly ask not to be rehosted — we{" "}
          <span className="text-zinc-300">index and deep-link</span> by default. This is the start of the join layer: the same
          sources appear contextually on text pages ("read / study / related") rather than only here.
        </p>

        <div className="mb-4">
          <p className="mb-1.5 text-[10px] uppercase tracking-[0.2em] text-zinc-500">Filter by type</p>
          <div className="flex flex-wrap gap-1.5">
            <TypePill t="primary_text" active={typeFilter === "primary_text"} onClick={() => setTypeFilter(typeFilter === "primary_text" ? null : "primary_text")} />
            {allTypes.filter((t) => t !== "primary_text").map((t) => (
              <TypePill key={t} t={t} active={typeFilter === t} onClick={() => setTypeFilter(typeFilter === t ? null : t)} />
            ))}
          </div>
        </div>

        <div className="mb-6">
          <p className="mb-1.5 text-[10px] uppercase tracking-[0.2em] text-zinc-500">Filter by tradition</p>
          <div className="flex flex-wrap gap-1.5">
            {allTrads.map((t) => (
              <TradPill key={t} t={t} active={tradFilter === t} onClick={() => setTradFilter(tradFilter === t ? null : t)} />
            ))}
          </div>
        </div>

        <section>
          <h2 className="mb-2 font-serif text-lg text-[color:var(--saffron)]">
            {typeFilter || tradFilter ? `Filtered (${filtered.length})` : `All sources (${resources.length})`}
          </h2>
          <ul>{filtered.map((r) => <ResourceCard key={r.id} r={r} />)}</ul>
        </section>

        {!typeFilter && !tradFilter && (
          <section className="mt-10">
            <h2 className="mb-2 font-serif text-lg text-[color:var(--saffron)]">Essential ({essentialCount})</h2>
            <p className="mb-3 text-[12px] text-zinc-500">
              The starting set worth indexing deeply: Muktabodha, GRETIL, Viśvāsa, SanskritDocuments, IFP, OCHS, NGMPP,
              Kaula Studies, Mahānaya, Sanskrit-Trika-Śaivism, ShivaShakti, Ambā, Anuttara Trika Kula, Lakshmanjoo Academy,
              Wisdom Library, SARIT, Internet Archive/KSTS, EFEO, Sanderson, INDOLOGY.
            </p>
            <ul>
              {essentialOnly.map((r) => (
                <li key={r.id} className="flex flex-wrap items-center gap-2 border-b border-zinc-800/60 py-2 text-[13px]">
                  <span className="text-[color:var(--saffron)]">●</span>
                  <span className="text-zinc-300">{r.name}</span>
                  <span className="ml-auto text-[10px] text-zinc-500">
                    {r.types.slice(0, 2).map((t) => TYPE_LABEL[t]).join(" · ")}
                  </span>
                </li>
              ))}
            </ul>
          </section>
        )}

        <footer className="mt-12 border-t border-zinc-800 pt-4 text-[11px] text-zinc-500">
          The resource register is the federation: manuscript → Sanskrit → translation → scholarship → lecture → commentary → AI retrieval.
          Nothing here is rehosted without permission — we join the landscape, we don't extract it.
        </footer>
      </div>
    </main>
  );
}
