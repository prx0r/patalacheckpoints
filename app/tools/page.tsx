"use client";

// /tools — the research-tools hub: the products a scholar opens to explore the corpus.
// Each card links to a working tool or the API. Humans read; agents call the same via MCP.
import React from "react";

const TOOLS = [
  { name: "Find tensions", href: "/tools/tensions", desc: "where interpretations diverge (contradictions, cruxes, doctrinal shifts) — where papers come from." },
  { name: "Crux between positions", href: "/tools/crux", desc: "the minimal divergence between two arguments." },
  { name: "Term trajectories", href: "/tools/terminology", desc: "how a lemma's sense shifts across traditions and periods." },
  { name: "Timeline", href: "/tools/timeline", desc: "the diachronic Śiva source-tree — school genealogy." },
  { name: "Review", href: "/review", desc: "open an object, see its state, record a scholarly review." },
  { name: "Bibliography", href: "/bibliography", desc: "the 69-work bibliography." },
  { name: "Concepts", href: "/concepts", desc: "the key terms with their sense-trajectories." },
];

export default function ToolsPage() {
  return (
    <main className="min-h-screen bg-zinc-950 px-6 py-12 text-zinc-200">
      <div className="mx-auto max-w-3xl">
        <header className="mb-6">
          <p className="text-[10px] uppercase tracking-[0.3em] text-[color:var(--saffron)]">patala — research tools</p>
          <h1 className="mt-1 font-serif text-3xl text-[color:var(--bone)]">Research Tools</h1>
          <p className="mt-2 text-sm text-zinc-400">
            Explore the corpus, find where interpretations diverge, and review scholarship. The same
            capabilities your AI assistant can call directly (via MCP).
          </p>
        </header>
        <ul className="space-y-2">
          {TOOLS.map((t) => (
            <li key={t.name}>
              <a href={t.href} className="block rounded border border-zinc-800 p-3 hover:border-[color:var(--saffron)]">
                <div className="text-sm font-semibold text-[color:var(--bone)]">{t.name}</div>
                <p className="mt-1 text-xs text-zinc-500">{t.desc}</p>
              </a>
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
}
