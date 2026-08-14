// astro.config.mjs — the OG patala static site (0-JS reading, performance-optimized)
import { defineConfig } from 'astro/config';

// The site serves the compiled projections (web/static/*.json) built from the REAL patala data
// (bibliography 254, clusters 9, IPVV passages 49). Output static → Cloudflare Pages/Workers.
// Reading pages are 0-JS, semantically marked up, canonical, with JSON-LD. The perf doctrine:
// compute on write, read from CDN.
export default defineConfig({
  output: 'static',
  site: 'https://patala.org',
  compressHTML: true,
  build: {
    inlineStylesheets: 'auto',
  },
  // islands only where interaction genuinely exists (none on reading pages)
});
