// Astro integration: serves and copies non-Markdown assets (SVG diagrams,
// images, data files, Go sources) from the content folders so that relative
// image paths in the Markdown resolve on the site.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { REPO_ROOT, CONTENT_DIRS, ASSET_EXTS, BASE } from './config.mjs';

const MIME = {
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.webp': 'image/webp',
  '.tsv': 'text/tab-separated-values; charset=utf-8',
  '.csv': 'text/csv; charset=utf-8',
  '.go': 'text/plain; charset=utf-8',
};

function* walkAssets(dir) {
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return;
  }
  for (const e of entries) {
    if (e.name.startsWith('.') || e.name === 'node_modules') continue;
    const full = path.join(dir, e.name);
    if (e.isDirectory()) yield* walkAssets(full);
    else if (e.isFile() && ASSET_EXTS.has(path.extname(e.name).toLowerCase())) yield full;
  }
}

function isServable(rel) {
  const top = rel.split('/')[0];
  return CONTENT_DIRS.includes(top) && ASSET_EXTS.has(path.extname(rel).toLowerCase()) && !rel.split('/').includes('..');
}

function serveAssets(server) {
  server.middlewares.use((req, res, next) => {
    const url = decodeURIComponent((req.url || '').split('?')[0]);
    // Depending on the Vite version, the base may already be stripped.
    const rel = (url.startsWith(BASE + '/') ? url.slice(BASE.length) : url).replace(/^\/+/, '');
    if (!isServable(rel)) return next();
    const file = path.join(REPO_ROOT, rel);
    if (!fs.existsSync(file)) return next();
    res.setHeader('Content-Type', MIME[path.extname(file).toLowerCase()] || 'application/octet-stream');
    fs.createReadStream(file).pipe(res);
  });
}

export default function contentAssets() {
  return {
    name: 'content-assets',
    hooks: {
      'astro:config:setup': ({ updateConfig }) => {
        // A Vite plugin middleware runs before the Astro page router in dev.
        updateConfig({ vite: { plugins: [{ name: 'content-assets-dev', configureServer: serveAssets }] } });
      },
      'astro:build:done': ({ dir, logger }) => {
        const out = fileURLToPath(dir);
        let count = 0;
        for (const top of CONTENT_DIRS) {
          for (const file of walkAssets(path.join(REPO_ROOT, top))) {
            const rel = path.relative(REPO_ROOT, file);
            const dest = path.join(out, rel);
            fs.mkdirSync(path.dirname(dest), { recursive: true });
            fs.copyFileSync(file, dest);
            count++;
          }
        }
        logger.info(`Copied ${count} content assets`);
      },
    },
  };
}
