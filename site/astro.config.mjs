// @ts-check
import { defineConfig } from 'astro/config';
import contentAssets from './src/lib/assets.mjs';
import { SITE, BASE, REPO_ROOT } from './src/lib/config.mjs';

export default defineConfig({
  site: SITE,
  base: BASE,
  trailingSlash: 'always',
  build: { format: 'directory' },
  integrations: [contentAssets()],
  vite: {
    // Allow the dev server to read Markdown and images from the repo root.
    server: { fs: { allow: [REPO_ROOT] } },
  },
});
