// Shared settings for the site build. Plain JavaScript so that both
// astro.config.mjs and the page code can import it.
import path from 'node:path';

export const SITE = 'https://caseyaedwards.github.io';
export const BASE = '/math_training';
export const GITHUB_BLOB = 'https://github.com/caseyaedwards/math_training/blob/main/';
export const GITHUB_TREE = 'https://github.com/caseyaedwards/math_training/tree/main/';

// Repository root: one level above site/. Astro runs with site/ as the
// working directory, and bundled page code cannot rely on import.meta.url.
export const REPO_ROOT = process.env.MT_REPO_ROOT
  ? path.resolve(process.env.MT_REPO_ROOT)
  : path.resolve(process.cwd(), '..');

// Folders whose Markdown becomes pages. The root README.md becomes the home page.
export const CONTENT_DIRS = ['course', 'tracks', 'workshops', 'history', 'resources', 'docs'];

// Non-Markdown files served from the site at the same relative path.
export const ASSET_EXTS = new Set(['.svg', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.tsv', '.csv', '.go']);

// Site title in the header and the browser tab.
export const SITE_TITLE = 'Math Training';

// The diagram showcase is generated into public/diagrams/ by svg-generator in CI.
export const DIAGRAMS_PATH = '/diagrams/';
