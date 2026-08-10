"use client";

import React, { useState, useCallback, useEffect } from "react";

// ── types (mirror of the API shape) ─────────────────────────────────────────
interface SourceSpan { id: string; passage_id: string; text: string; start?: number; end?: number; }
interface TargetSpan { id: string; translation_version_id: string; text: string; }
interface Alignment { id: string; source_span_ids: string[]; target_span_ids: string[]; type: string; decision_ids: string[]; method?: string; }
interface EvidenceItem { id: string; resource_id: string; locator?: string; excerpt?: string; verification: string; }
interface EvidenceUse { evidence_id: string; role: string; note?: string; }
interface TranslationDecision {
  id: string; claim: string; surface_rendering: string; adjudicated_reading?: string;
  alternatives: string[]; status: string; evidence_state: string; editorial_status: string;
  method: string; reason: string; evidence: EvidenceUse[]; review_events: string[];
  source_span_ids: string[]; target_span_ids: string[];
}
interface PublishedTranslation {
  text: string; source_spans: SourceSpan[]; target_spans: TargetSpan[];
  alignments: Alignment[]; decisions: TranslationDecision[]; evidence: EvidenceItem[];
  review_state: string; provenance: { edition: string; base_source: string };
}
interface DecisionDetail {
  id: string; claim: string; surface_rendering: string; adjudicated_reading: string | null;
  alternatives: string[]; status: string; evidence_state: string; editorial_status: string;
  method: string; reason: string; evidence: { use: EvidenceUse; item: EvidenceItem }[];
  unresolved_evidence: string[]; reviews: any[];
}

const STATUS_LABEL: Record<string, string> = {
  CONSTRAINED: "The source effectively forces this reading.",
  PREFERRED: "Best reading, though alternatives are plausible.",
  OPEN: "More than one serious reading remains.",
  RECONSTRUCTED: "Requires textual intervention.",
};

// ── helpers ─────────────────────────────────────────────────────────────────
function buildIndexes(pub: PublishedTranslation) {
  // spanId -> list of decision ids (from alignments)
  const spanToDecision = new Map<string, string[]>();
  for (const a of pub.alignments) {
    for (const sid of a.source_span_ids) {
      spanToDecision.set(sid, a.decision_ids);
    }
    for (const tid of a.target_span_ids) {
      spanToDecision.set(tid, a.decision_ids);
    }
  }
  // spanId -> aligned span ids (source<->target via alignments)
  const spanToAligned = new Map<string, string[]>();
  for (const a of pub.alignments) {
    for (const s of a.source_span_ids) {
      const cur = spanToAligned.get(s) ?? [];
      spanToAligned.set(s, [...cur, ...a.target_span_ids]);
    }
    for (const t of a.target_span_ids) {
      const cur = spanToAligned.get(t) ?? [];
      spanToAligned.set(t, [...cur, ...a.source_span_ids]);
    }
  }
  const decisionById = new Map(pub.decisions.map((d) => [d.id, d]));
  return { spanToDecision, spanToAligned, decisionById };
}

// ── the reader ──────────────────────────────────────────────────────────────
export default function PassageReaderPage({ params }: { params: Promise<{ work: string; locator: string }> }) {
  const [work, setWork] = useState("");
  const [locator, setLocator] = useState("");
  const [pub, setPub] = useState<PublishedTranslation | null>(null);
  const [hovered, setHovered] = useState<string | null>(null);       // span id hovered
  const [selectedDecision, setSelectedDecision] = useState<string | null>(null);
  const [decision, setDecision] = useState<DecisionDetail | null>(null);
  const [auditMode, setAuditMode] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    params.then((p) => {
      setWork(p.work);
      setLocator(p.locator);
      const id = `${p.work}:${p.locator}`;
      fetch(`/api/passages/${id}/translation`)
        .then((r) => (r.ok ? r.json() : Promise.reject("not found")))
        .then((d) => { setPub(d); setSelectedDecision(null); })
        .catch(() => setError("no published auditable translation for this passage yet"));
    });
  }, [params]);

  const fetchDecision = useCallback((id: string) => {
    fetch(`/api/decisions/${id}`).then((r) => (r.ok ? r.json() : null)).then((d) => setDecision(d));
  }, []);

  const { spanToDecision, spanToAligned, decisionById } = pub ? buildIndexes(pub) : { spanToDecision: new Map(), spanToAligned: new Map(), decisionById: new Map() };

  const clickSpan = useCallback((spanId: string) => {
    const decisionIds = spanToDecision.get(spanId) ?? [];
    if (decisionIds.length) {
      setSelectedDecision(decisionIds[0]);
      fetchDecision(decisionIds[0]);
    }
  }, [spanToDecision, fetchDecision]);

  const isDecisionSpan = (spanId: string) => (spanToDecision.get(spanId) ?? []).length > 0;
  const decisionFor = (spanId: string) => {
    const ids = spanToDecision.get(spanId) ?? [];
    return ids.length ? decisionById.get(ids[0]) : undefined;
  };

  if (error) {
    return (
      <main className="min-h-screen bg-zinc-950 px-6 py-16 text-zinc-300">
        <p className="text-zinc-500">{error}</p>
        <p className="mt-2 text-sm text-zinc-600">e.g. <code>/read/kramasadbhava/1.8</code></p>
      </main>
    );
  }
  if (!pub) {
    return <main className="min-h-screen bg-zinc-950 px-6 py-16 text-zinc-500">Loading…</main>;
  }

  // prev/next within the unit (Kramasadbhāva 1.1–1.28)
  const isKs = work === "kramasadbhava";
  const verse = parseInt(locator.split(".")[1] ?? locator, 10);
  const prevNext = isKs ? {
    prev: verse > 1 ? `/read/kramasadbhava/1.${verse - 1}` : null,
    next: verse < 28 ? `/read/kramasadbhava/1.${verse + 1}` : null,
  } : { prev: null, next: null };

  return (
    <main className="min-h-screen bg-zinc-950 px-6 py-10 text-zinc-200">
      <div className="mx-auto flex max-w-6xl gap-8">
        {/* left: the reading column */}
        <div className="min-w-0 flex-1">
          <header className="mb-6">
            <div className="flex items-center gap-3">
              <p className="text-[10px] uppercase tracking-[0.3em] text-[color:var(--saffron)]">
                {work} · {locator}
              </p>
              <div className="ml-auto flex items-center gap-2 text-[11px]">
                {prevNext.prev && <a href={prevNext.prev} className="rounded border border-zinc-700 px-2 py-0.5 text-zinc-400 hover:border-[color:var(--saffron)] hover:text-[color:var(--saffron)]">← prev</a>}
                {prevNext.next && <a href={prevNext.next} className="rounded border border-zinc-700 px-2 py-0.5 text-zinc-400 hover:border-[color:var(--saffron)] hover:text-[color:var(--saffron)]">next →</a>}
              </div>
            </div>
            <h1 className="mt-1 font-serif text-2xl text-[color:var(--bone)]">
              Kramasadbhāva {locator.replace(".", ".")}
            </h1>
            <div className="mt-2 flex items-center gap-3 text-[11px] text-zinc-500">
              <span>ed. {pub.provenance.edition}</span>
              <span>· review: {pub.review_state}</span>
              <button
                onClick={() => setAuditMode(!auditMode)}
                className="ml-auto rounded border border-zinc-700 px-2 py-0.5 text-[10px] uppercase tracking-wider text-zinc-400 hover:border-[color:var(--saffron)] hover:text-[color:var(--saffron)]"
              >
                {auditMode ? "AUDIT" : "READ"} mode
              </button>
            </div>
          </header>

          {/* Sanskrit */}
          <div className="mb-6 rounded border border-zinc-800/70 bg-zinc-900/40 p-5">
            <p className="mb-2 text-[10px] uppercase tracking-[0.2em] text-zinc-500">Sanskrit</p>
            <div className="flex flex-wrap gap-x-1 gap-y-0.5 font-serif text-lg leading-relaxed text-zinc-100">
              {pub.source_spans.map((s) => (
                <span
                  key={s.id}
                  onMouseEnter={() => setHovered(s.id)}
                  onMouseLeave={() => setHovered(null)}
                  onClick={() => clickSpan(s.id)}
                  className={[
                    "cursor-default rounded px-0.5 transition-colors",
                    hovered && (spanToAligned.get(hovered) ?? []).includes(s.id) ? "bg-[color:var(--saffron)]/25" : "",
                    isDecisionSpan(s.id) && auditMode ? "border-b border-dotted border-[color:var(--saffron)]" : "",
                  ].join(" ")}
                >
                  {s.text}
                </span>
              ))}
            </div>
          </div>

          {/* Translation */}
          <div className="mb-6 rounded border border-zinc-800/70 bg-zinc-900/40 p-5">
            <p className="mb-2 text-[10px] uppercase tracking-[0.2em] text-zinc-500">Translation</p>
            <div className="flex flex-wrap gap-x-1 gap-y-0.5 text-lg leading-relaxed text-zinc-100">
              {pub.target_spans.map((t) => {
                const dec = decisionFor(t.id);
                return (
                  <span
                    key={t.id}
                    onMouseEnter={() => setHovered(t.id)}
                    onMouseLeave={() => setHovered(null)}
                    onClick={() => clickSpan(t.id)}
                    className={[
                      "cursor-pointer rounded px-0.5 transition-colors",
                      hovered && (spanToAligned.get(hovered) ?? []).includes(t.id) ? "bg-[color:var(--saffron)]/25" : "",
                      dec && auditMode
                        ? `border-b border-dotted ${dec.status === "OPEN" ? "border-red-400" : dec.status === "CONSTRAINED" ? "border-emerald-400" : "border-[color:var(--saffron)]"}`
                        : "",
                    ].join(" ")}
                  >
                    {t.text}
                  </span>
                );
              })}
            </div>
            {auditMode && (
              <div className="mt-4 space-y-1 border-t border-zinc-800/60 pt-3 text-[11px] text-zinc-400">
                {pub.decisions.map((d) => (
                  <div key={d.id} className="flex items-center gap-2">
                    <span className="w-24 truncate font-mono text-zinc-500">{d.claim}</span>
                    <span className={`rounded px-1.5 py-0.5 text-[9px] uppercase ${d.status === "OPEN" ? "bg-red-950/60 text-red-300" : d.status === "CONSTRAINED" ? "bg-emerald-950/60 text-emerald-300" : "bg-amber-950/60 text-amber-300"}`}>
                      {d.status}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Commentary placeholder */}
          <div className="rounded border border-zinc-800/50 p-5 text-[13px] leading-relaxed text-zinc-400">
            <p className="mb-1 text-[10px] uppercase tracking-[0.2em] text-zinc-600">Commentary</p>
            <p>Commentary (C1) for this passage to appear here — written by the editorial model with anchored evidence, not auto-generated prose.</p>
          </div>
        </div>

        {/* right: the decision panel */}
        <div className="w-80 shrink-0">
          {selectedDecision && decision ? (
            <DecisionPanel decision={decision} onClose={() => { setSelectedDecision(null); setDecision(null); }} />
          ) : (
            <div className="rounded border border-dashed border-zinc-800 p-5 text-[12px] text-zinc-600">
              Click a phrase in the translation to inspect its decision.
            </div>
          )}
        </div>
      </div>
    </main>
  );
}

// ── the decision panel ──────────────────────────────────────────────────────
function DecisionPanel({ decision, onClose }: { decision: DecisionDetail; onClose: () => void }) {
  return (
    <div className="rounded-lg border border-zinc-700/60 bg-zinc-900/70 p-5">
      <div className="mb-3 flex items-start justify-between">
        <p className="text-[10px] uppercase tracking-[0.2em] text-[color:var(--saffron)]">Translation decision</p>
        <button onClick={onClose} className="text-zinc-500 hover:text-zinc-300">✕</button>
      </div>

      {/* phrase */}
      <p className="mb-1 font-serif text-xl text-[color:var(--bone)]">{decision.surface_rendering}</p>
      <p className="mb-4 text-[12px] text-zinc-500">{decision.claim}</p>

      {/* status */}
      <div className="mb-4">
        <span className={`inline-block rounded px-2 py-0.5 text-[10px] uppercase tracking-wider ${decision.status === "OPEN" ? "bg-red-950/70 text-red-300" : decision.status === "CONSTRAINED" ? "bg-emerald-950/70 text-emerald-300" : "bg-amber-950/70 text-amber-300"}`}>
          {decision.status}
        </span>
        <p className="mt-1.5 text-[12px] text-zinc-400">{STATUS_LABEL[decision.status] ?? ""}</p>
      </div>

      {/* alternatives */}
      {decision.alternatives.length > 0 && (
        <div className="mb-4">
          <p className="mb-1 text-[10px] uppercase tracking-wider text-zinc-500">Alternative</p>
          {decision.alternatives.map((a, i) => (
            <p key={i} className="text-[13px] text-zinc-300">{a}</p>
          ))}
        </div>
      )}

      {/* why */}
      <div className="mb-4">
        <p className="mb-1 text-[10px] uppercase tracking-wider text-zinc-500">Why</p>
        <p className="text-[12px] leading-relaxed text-zinc-300">{decision.reason}</p>
      </div>

      {/* evidence */}
      <div className="mb-4">
        <p className="mb-1 text-[10px] uppercase tracking-wider text-zinc-500">Evidence</p>
        <div className="space-y-2">
          {decision.evidence.map(({ use, item }) => (
            <div key={item.id} className="rounded border border-zinc-800 bg-zinc-950/50 p-2">
              <div className="flex items-center gap-2 text-[11px]">
                <span className="uppercase text-[color:var(--saffron)]">{use.role}</span>
                <span className="font-mono text-zinc-500">{item.resource_id.split(":").slice(-2).join(":")}</span>
              </div>
              {item.locator && <p className="text-[11px] text-zinc-500">{item.locator}</p>}
              {item.excerpt && <p className="mt-1 text-[11px] italic text-zinc-400">“{item.excerpt}”</p>}
              <span className={`mt-1 inline-block text-[9px] uppercase ${item.verification === "verified" ? "text-emerald-400" : "text-amber-400"}`}>
                {item.verification}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* review */}
      <div className="rounded border border-zinc-800 bg-zinc-950/50 p-2 text-[11px]">
        <p className="text-[10px] uppercase tracking-wider text-zinc-500">Review</p>
        <p className="mt-1 text-zinc-400">{decision.editorial_status === "proposed" ? "Machine proposal · not yet reviewed by a specialist" : decision.editorial_status}</p>
      </div>
    </div>
  );
}
