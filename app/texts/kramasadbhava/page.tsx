// /texts/kramasadbhava — the work overview page (unit summary + per-passage read links).
// Summarizes the actual scholarly state of the work: passages, decisions, OPEN cruxes,
// evidence gaps. Each passage links to its auditable reader.
import { listUnitPassages } from "@/data/corpus/published";

export const dynamic = "force-static";

export default function KramasadbhavaPage() {
  const passages = listUnitPassages("kramasadbhava");
  const open = passages.reduce((n, p) => n + p.open_decisions, 0);
  const withTr = passages.filter((p) => p.has_translation).length;
  const withDec = passages.filter((p) => p.decisions > 0).length;

  return (
    <main className="min-h-screen bg-zinc-950 px-6 py-12 text-zinc-200">
      <div className="mx-auto max-w-3xl">
        <header className="mb-8">
          <p className="text-[10px] uppercase tracking-[0.3em] text-[color:var(--saffron)]">patala — tantra hub</p>
          <h1 className="mt-1 font-serif text-3xl text-[color:var(--bone)]">Kramasadbhāva</h1>
          <p className="mt-2 text-sm text-zinc-400">
            Krama · the opening stuti · Dyczkowski ed., Muktabodha (NGMPP A 209/23)
          </p>
          <div className="mt-3 flex flex-wrap gap-2 text-[11px] text-zinc-400">
            <span className="rounded border border-zinc-700 px-2 py-0.5">{passages.length} passages published</span>
            <span className="rounded border border-zinc-700 px-2 py-0.5">{withTr} with working translation</span>
            <span className="rounded border border-zinc-700 px-2 py-0.5">{withDec} with decisions</span>
            <span className="rounded border border-red-900/60 px-2 py-0.5 text-red-300">{open} OPEN cruxes</span>
            <span className="rounded border border-zinc-700 px-2 py-0.5">0 specialist reviewed</span>
          </div>
        </header>

        <section>
          <h2 className="mb-2 font-serif text-lg text-[color:var(--saffron)]">Chapter 1 — the stuti</h2>
          <ul className="divide-y divide-zinc-800/60 rounded border border-zinc-800/60">
            {passages.map((p) => {
              const loc = p.locator;
              return (
                <li key={p.passage_id} className="flex items-center gap-3 px-4 py-2.5 text-[13px] hover:bg-zinc-900/40">
                  <a href={`/read/kramasadbhava/${loc}`} className="min-w-0 flex-1 text-zinc-300 hover:text-[color:var(--saffron)]">
                    <span className="font-mono text-zinc-500">1.{loc}</span>
                    <span className="ml-3">{p.has_translation ? "" : "· no translation yet"}</span>
                  </a>
                  <span className="flex items-center gap-2 text-[10px]">
                    {p.open_decisions > 0 && <span className="rounded bg-red-950/60 px-1.5 py-0.5 text-red-300">{p.open_decisions} OPEN</span>}
                    {p.decisions > 0 && <span className="rounded bg-zinc-800 px-1.5 py-0.5 text-zinc-400">{p.decisions} dec</span>}
                    <span className="text-zinc-600">Read →</span>
                  </span>
                </li>
              );
            })}
          </ul>
        </section>

        <p className="mt-8 text-[12px] text-zinc-500">
          Working translations are AI-assisted and not peer-reviewed. Decisions are
          proposals until a specialist reviews them.
        </p>
      </div>
    </main>
  );
}
