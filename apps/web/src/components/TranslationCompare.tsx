// apps/web/src/components/TranslationCompare.tsx
// A React island: renders canonical Translation/TranslationDecision objects.
// The canonical data lives in Pāṭala objects; this component only queries/renders them
// (frontend-architecture.md: "TranslationCompareBundle → React component", never the reverse).

import { useState } from "react";

export interface TranslationOption {
  id: string;
  label: string;
  text: string;
}

export interface TranslationCompareProps {
  translations: TranslationOption[];
}

export default function TranslationCompare({ translations }: TranslationCompareProps) {
  const [active, setActive] = useState(translations[0]?.id ?? "");
  const current = translations.find((t) => t.id === active) ?? translations[0];

  return (
    <section>
      <h3>Translations</h3>
      <div style={{ display: "flex", gap: "0.5rem", marginBottom: "0.5rem" }}>
        {translations.map((t) => (
          <button
            key={t.id}
            onClick={() => setActive(t.id)}
            style={{
              padding: "0.25rem 0.75rem",
              border: active === t.id ? "2px solid #8b3528" : "1px solid #ccc",
              background: active === t.id ? "#8b3528" : "transparent",
              color: active === t.id ? "#fff" : "#1a1a1a",
              cursor: "pointer",
              borderRadius: "4px",
            }}
          >
            {t.label}
          </button>
        ))}
      </div>
      <blockquote style={{ margin: 0, borderLeft: "3px solid #ccc", paddingLeft: "1rem" }}>
        {current?.text}
      </blockquote>
      <p style={{ color: "#666", fontSize: "0.85rem" }}>TranslationDecision <code>{current?.id}</code></p>
    </section>
  );
}
