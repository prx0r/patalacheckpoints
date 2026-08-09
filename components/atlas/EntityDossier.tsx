"use client";

import { motion, AnimatePresence } from "framer-motion";
import { X, ScrollText, GitFork, CircleDot, Network, ChevronRight } from "lucide-react";
import { AtlasEntity } from "@/lib/atlas";
import { getRelationsFor, getEntity, relationMeta, typeColor } from "@/data/atlas";

const TYPE_HEADER: Record<string, string> = {
  tradition: "SAMPRA-DĀYA · TRADITION",
  text: "GRANTHA · TEXT",
  person: "ĀCĀRYA · AUTHOR",
  concept: "SAMJÑĀ · CONCEPT",
};

export function EntityDossier({
  entity,
  onClose,
  onNavigate,
}: {
  entity: AtlasEntity;
  onClose: () => void;
  onNavigate: (id: string) => void;
}) {
  const rels = getRelationsFor(entity.id);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-[100] bg-[#11100d]/95 backdrop-blur-xl flex items-center justify-center p-4 md:p-8 font-mono"
      onClick={onClose}
    >
      <div
        className="relative w-full max-w-[1100px] h-[88vh] flex flex-col bg-[#e8dfcc] border-2 border-[#3c3342] shadow-[40px_40px_0px_rgba(0,0,0,0.5)] overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Title bar */}
        <div className="retro-title-bar px-6 py-4 flex justify-between items-center border-b-2 border-[#3c3342]">
          <div className="flex items-center gap-3 text-[12px] font-black uppercase tracking-[0.3em] text-bone">
            <span className="text-[16px] text-saffron">{entity.sanskrit || "◈"}</span>
            <span>{entity.title}</span>
            <span className="text-[9px] text-ash tracking-widest">{TYPE_HEADER[entity.type]}</span>
          </div>
          <div
            className="retro-button w-9 h-9 flex items-center justify-center cursor-pointer hover:bg-[#8b3528] hover:text-bone transition-colors"
            onClick={onClose}
          >
            <X size={18} />
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-10 custom-scrollbar bg-[#e8dfcc]">
          <div className="max-w-full mx-auto space-y-10">
            {/* Header */}
            <div className="border-b-[3px] border-[#3c3342] pb-8">
              <div className="flex items-center gap-3 mb-4">
                <span
                  className="px-2 py-0.5 text-[10px] font-black uppercase tracking-widest border"
                  style={{ color: typeColor[entity.type], borderColor: typeColor[entity.type] }}
                >
                  {entity.id}
                </span>
                {entity.period && (entity.period.start || entity.period.end) && (
                  <span className="text-[10px] text-ink-muted">
                    {entity.period.start ?? "?"}–{entity.period.end ?? "?"}
                    {entity.period.approximate ? " (approx.)" : ""}
                  </span>
                )}
              </div>
              <div className="flex items-end gap-4">
                <div>
                  <h1 className="text-[#1b1915] text-5xl font-black uppercase tracking-tighter leading-none mb-3">
                    {entity.title}
                  </h1>
                  {entity.sanskrit && (
                    <div className="text-[22px] text-[#75552b] mb-3">{entity.sanskrit}</div>
                  )}
                </div>
              </div>
              <p className="text-[#5a5145] text-[14px] leading-relaxed font-sans max-w-3xl">
                {entity.summary}
              </p>
            </div>

            {/* Dossier sections */}
            {entity.dossier && (
              <div className="grid grid-cols-2 gap-8">
                {entity.dossier.systemicFunction && (
                  <DossierSection title="Systemic Function" icon={ScrollText}>
                    <p className="text-[13px] leading-relaxed text-ink">{entity.dossier.systemicFunction}</p>
                  </DossierSection>
                )}
                {entity.dossier.doctrinalCore && (
                  <DossierSection title="Doctrinal Core" icon={CircleDot}>
                    <ul className="space-y-3">
                      {entity.dossier.doctrinalCore.map((d, i) => (
                        <li key={i} className="text-[12px] text-ink flex gap-3">
                          <span className="text-[#8b3528] font-black shrink-0">•</span>
                          <span>{d}</span>
                        </li>
                      ))}
                    </ul>
                  </DossierSection>
                )}
                {entity.dossier.problems && (
                  <DossierSection title="Open Problems" icon={GitFork}>
                    <ul className="space-y-2">
                      {entity.dossier.problems.map((p, i) => (
                        <li key={i} className="text-[12px] text-ink-muted flex gap-2">
                          <span className="text-[#75552b]">[X]</span>
                          <span>{p}</span>
                        </li>
                      ))}
                    </ul>
                  </DossierSection>
                )}
                {entity.dossier.outputs && (
                  <DossierSection title="Outputs" icon={Network}>
                    <ul className="space-y-2">
                      {entity.dossier.outputs.map((o, i) => (
                        <li key={i} className="text-[12px] text-ink flex gap-2">
                          <ChevronRight size={12} className="text-[#75552b] shrink-0 mt-0.5" />
                          <span>{o}</span>
                        </li>
                      ))}
                    </ul>
                  </DossierSection>
                )}
              </div>
            )}

            {/* Relations */}
            <div>
              <div className="manuscript-rule mb-4" />
              <div className="text-[10px] font-black uppercase tracking-[0.3em] text-[#71695b] mb-4">
                RELATIONS · {rels.length}
              </div>
              <div className="grid grid-cols-2 gap-3">
                {rels.map((r, i) => {
                  const meta = relationMeta[r.type] ?? { label: "RELATES", color: "#928873" };
                  const otherId = r.source === entity.id ? r.target : r.source;
                  const other = getEntity(otherId);
                  return (
                    <button
                      key={i}
                      onClick={() => onNavigate(otherId)}
                      className="text-left px-4 py-3 bg-[#efe6d2] border border-[#c9bda0] hover:border-[#8b3528] transition-colors flex items-center gap-3 group"
                    >
                      <span
                        className="text-[9px] font-black uppercase tracking-widest px-1.5 py-0.5 border shrink-0"
                        style={{ color: meta.color, borderColor: meta.color }}
                      >
                        {meta.label}
                      </span>
                      <span className="flex-1">
                        <span className="block text-[11px] font-bold text-ink group-hover:text-[#8b3528]">
                          {other?.title ?? otherId}
                        </span>
                        <span className="block text-[9px] text-ink-muted uppercase tracking-wider">
                          {r.confidence} · {r.type}
                        </span>
                      </span>
                      <span className="text-[#8b3528] opacity-0 group-hover:opacity-100">→</span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Resources */}
            {entity.resources && entity.resources.length > 0 && (
              <div>
                <div className="manuscript-rule mb-4" />
                <div className="text-[10px] font-black uppercase tracking-[0.3em] text-[#71695b] mb-4">
                  RESOURCES
                </div>
                <div className="flex flex-wrap gap-3">
                  {entity.resources.map((res, i) => (
                    <a
                      key={i}
                      href={res.href}
                      className="px-4 py-2 bg-[#1b1a2e] text-[#e7dbc0] text-[10px] font-black uppercase tracking-widest hover:bg-[#272641] transition-colors flex items-center gap-2"
                    >
                      <span className="text-[#c58b36]">{res.type === "translation" ? "◈" : res.type === "scholarship" ? "✎" : "◎"}</span>
                      {res.title}
                    </a>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="bg-[#1b1a2e] border-t-[3px] border-[#3c3342] p-3 px-6 flex justify-between items-center text-[10px] font-black text-[#928873] uppercase tracking-[0.3em]">
          <span className="flex items-center gap-2">
            <span className="bindu" />
            ŚAIVA-TANTRA-ATLAS · v0.1
          </span>
          <span>EVIDENCE-LAYER: ACTIVE</span>
        </div>
      </div>
    </motion.div>
  );
}

function DossierSection({
  title,
  icon: Icon,
  children,
}: {
  title: string;
  icon: React.ComponentType<{ size?: number }>;
  children: React.ReactNode;
}) {
  return (
    <div className="relative border border-[#b3a488] bg-[#efe6d2] p-5">
      <div className="flex items-center gap-2 mb-3 pb-2 border-b border-[#c9bda0]">
        <span className="text-[#8b3528]">
          <Icon size={14} />
        </span>
        <span className="text-[10px] font-black uppercase tracking-[0.2em] text-[#1b1915]">{title}</span>
      </div>
      <div className="text-[#4a4338]">{children}</div>
    </div>
  );
}
