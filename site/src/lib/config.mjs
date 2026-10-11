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

// Top navigation. An entry appears only when its README.md exists.
export const NAV = [
  { label: 'Home', dir: '' },
  { label: 'Course', dir: 'course' },
  { label: 'Tracks', dir: 'tracks' },
  { label: 'Workshops', dir: 'workshops' },
  { label: 'History', dir: 'history' },
  { label: 'Resources', dir: 'resources' },
];
