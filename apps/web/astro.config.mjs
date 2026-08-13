import { defineConfig } from "astro/config";
import react from "@astrojs/react";

// Pāṭala web — Astro + React islands (frontend-architecture.md)
// Astro owns documents; React owns interactions; Pāṭala objects own semantics.
// Static output for reading surfaces (fast, cacheable, JS-off readable).
// Adopt `output: "server"` + a Cloudflare adapter only when dynamic routes require it.
export default defineConfig({
  output: "static",
  integrations: [react()],
});
