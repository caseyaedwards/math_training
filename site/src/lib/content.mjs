// Finds the repository Markdown and renders it to HTML at build time.
// Nothing is copied into site/: the files are read straight from the repo.
// src/lib/loader.mjs feeds the result to Starlight's docs collection.
import fs from 'node:fs';
import path from 'node:path';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import remarkRehype from 'remark-rehype';
import rehypeRaw from 'rehype-raw';
import rehypeSlug from 'rehype-slug';
import rehypeKatex from 'rehype-katex';
import rehypeStringify from 'rehype-stringify';
import { visit, SKIP } from 'unist-util-visit';
import { VFile } from 'vfile';
import { toString } from 'hast-util-to-string';
import { REPO_ROOT, CONTENT_DIRS, ASSET_EXTS, BASE, GITHUB_BLOB, GITHUB_TREE } from './config.mjs';

const CODE_EXTS = new Set(['.go', '.py', '.js', '.mjs', '.ts', '.sh', '.c', '.rs', '.ipynb']);

const toPosix = (p) => p.split(path.sep).join('/');

/** Repo path (posix, relative) of a Markdown file -> site path without base, for example "/course/101/". */
export function routeFor(repoPath) {
  let p = repoPath;
  if (p === 'README.md') return '/';
  if (p.endsWith('/README.md')) p = p.slice(0, -'README.md'.length);
  else if (p.endsWith('.md')) p = p.slice(0, -'.md'.length) + '/';
  return '/' + p;
}

export const withBase = (route) => BASE + route;

/** Repo path of a Markdown file -> Starlight entry id, for example "course/101". The root README.md is "index". */
export function idFor(repoPath) {
  if (repoPath === 'README.md') return 'index';
  if (repoPath.endsWith('/README.md')) return repoPath.slice(0, -'/README.md'.length);
  return repoPath.replace(/\.md$/, '');
}

function* walkMarkdown(dir) {
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return; // A missing section is fine: other writers may not have created it yet.
  }
  for (const e of entries) {
    if (e.name.startsWith('.') || e.name === 'node_modules') continue;
    const full = path.join(dir, e.name);
    if (e.isDirectory()) yield* walkMarkdown(full);
    else if (e.isFile() && e.name.toLowerCase().endsWith('.md')) yield full;
  }
}

/** All source Markdown files as repo-relative posix paths, sorted. */
export function listSources() {
  const out = [];
  if (fs.existsSync(path.join(REPO_ROOT, 'README.md'))) out.push('README.md');
  for (const top of CONTENT_DIRS) {
    for (const file of walkMarkdown(path.join(REPO_ROOT, top))) {
      // img/README.md and similar notes inside asset folders still become pages.
      out.push(toPosix(path.relative(REPO_ROOT, file)));
    }
  }
  return out.sort();
}

// ---------- link rewriting ----------

function isContentPath(p) {
  return p === 'README.md' || CONTENT_DIRS.includes(p.split('/')[0]);
}

/** Rewrite one relative URL found in the Markdown file at repoPath. Returns null to leave it alone. */
export function rewriteUrl(url, repoPath, { isImage = false } = {}) {
  if (!url) return null;
  if (/^[a-z][a-z0-9+.-]*:/i.test(url) || url.startsWith('//') || url.startsWith('#') || url.startsWith('/')) return null;
  const m = url.match(/^([^?#]*)([?#].*)?$/);
  const rawPath = m[1];
  const suffix = m[2] || '';
  if (!rawPath) return null;
  let decoded;
  try {
    decoded = decodeURI(rawPath);
  } catch {
    decoded = rawPath;
  }
  const fromDir = path.posix.dirname(repoPath);
  const target = path.posix.normalize(path.posix.join(fromDir, decoded));
  if (target.startsWith('..')) return null; // Outside the repo: leave as written.
  const trailingSlash = decoded.endsWith('/');
  const clean = target.replace(/\/$/, '');
  const ext = path.posix.extname(clean).toLowerCase();
  const enc = (p) => encodeURI(p);

  // Pages on the site.
  if (ext === '.md' && isContentPath(clean)) return withBase(routeFor(clean)) + suffix;
  if (!ext && isContentPath(clean) && clean !== '.') {
    const readme = path.join(REPO_ROOT, clean, 'README.md');
    if (fs.existsSync(readme) || !fs.existsSync(path.join(REPO_ROOT, clean))) {
      return withBase('/' + enc(clean) + '/') + suffix;
    }
  }
  if (clean === '.' ) return withBase('/') + suffix;
  // Source code reads best on GitHub, with highlighting and history.
  if (!isImage && CODE_EXTS.has(ext)) return GITHUB_BLOB + enc(clean) + suffix;
  // Assets served by the site at the same relative path.
  if (ASSET_EXTS.has(ext) && isContentPath(clean)) return withBase('/' + enc(clean)) + suffix;
  if (isImage) return withBase('/' + enc(clean)) + suffix;
  // Everything else (obsidian/, svg/, code files, folders without a README): GitHub.
  const isDir = !ext || trailingSlash;
  return (isDir ? GITHUB_TREE : GITHUB_BLOB) + enc(clean) + suffix;
}

function rehypeRepoLinks() {
  return (tree, file) => {
    const { repoPath } = file.data;
    visit(tree, (node, index, parent) => {
      if (node.type === 'comment' && parent && index != null) {
        parent.children.splice(index, 1); // Drop <!-- diagram: ... --> and other comments.
        return [SKIP, index];
      }
      if (node.type !== 'element') return;
      const props = node.properties || {};
      if (node.tagName === 'a' && typeof props.href === 'string') {
        const next = rewriteUrl(props.href, repoPath);
        if (next) props.href = next;
        if (/^https?:/.test(props.href) && !props.href.startsWith('https://caseyaedwards.github.io/')) {
          props.rel = ['noopener'];
        }
      }
      if ((node.tagName === 'img' || node.tagName === 'source') && typeof props.src === 'string') {
        const next = rewriteUrl(props.src, repoPath, { isImage: true });
        if (next) props.src = next;
        if (node.tagName === 'img') {
          props.loading = 'lazy';
          const cls = Array.isArray(props.className) ? props.className : [];
          if (/\.svg($|[?#])/i.test(props.src)) props.className = [...cls, 'diagram'];
        }
      }
    });
  };
}

/**
 * GitHub renders `$$...$$` written on one line as display math. remark-math
 * parses it as inline math, so mark those nodes for display mode.
 */
function remarkDoubleDollarDisplay() {
  return (tree, file) => {
    const src = String(file.value);
    visit(tree, 'inlineMath', (node) => {
      const start = node.position?.start?.offset;
      if (start == null || !src.startsWith('$$', start)) return;
      node.data = node.data || {};
      node.data.hProperties = { ...(node.data.hProperties || {}), className: ['language-math', 'math-display'] };
    });
  };
}

/**
 * Takes the first H1 as the page title and removes it from the body, because
 * Starlight prints the title above the content. Collects H2 and H3 headings for
 * the "On this page" list. Runs before KaTeX so that heading text keeps the
 * plain TeX source instead of the rendered markup.
 */
function rehypeTitleAndHeadings() {
  return (tree, file) => {
    let title = null;
    const headings = [];
    visit(tree, 'element', (node, index, parent) => {
      if (!/^h[1-6]$/.test(node.tagName)) return;
      const text = toString(node).replace(/\s+/g, ' ').trim();
      if (node.tagName === 'h1' && title == null) {
        title = text;
        if (parent && index != null) {
          parent.children.splice(index, 1);
          return [SKIP, index];
        }
        return;
      }
      const depth = Number(node.tagName[1]);
      if ((depth === 2 || depth === 3) && node.properties?.id) {
        headings.push({ depth, slug: String(node.properties.id), text });
      }
    });
    file.data.title = title;
    file.data.headings = headings;
  };
}

/**
 * KaTeX writes each formula twice: MathML for screen readers and HTML for the
 * eye. Pagefind would index both, so search excerpts would repeat every
 * formula as garbled text. Keep only the TeX source (the MathML annotation)
 * in the search index.
 */
function rehypeKatexSearchText() {
  return (tree) => {
    visit(tree, 'element', (node) => {
      const cls = node.properties?.className;
      if (Array.isArray(cls) && cls.includes('katex-html')) {
        node.properties.dataPagefindIgnore = '';
        return SKIP;
      }
      if (node.tagName === 'semantics') {
        for (const child of node.children) {
          if (child.type === 'element' && child.tagName !== 'annotation') {
            child.properties = { ...child.properties, dataPagefindIgnore: '' };
          }
        }
        return SKIP;
      }
    });
  };
}

/**
 * Build the Markdown to HTML processor. extraRehypePlugins run last, on the
 * finished HTML tree: the loader passes the plugins that Starlight and
 * Expressive Code register with Astro (heading anchor links, code frames).
 */
export function createRenderer({ extraRehypePlugins = [] } = {}) {
  const processor = unified()
    .use(remarkParse)
    .use(remarkGfm)
    .use(remarkMath)
    .use(remarkDoubleDollarDisplay)
    .use(remarkRehype, { allowDangerousHtml: true })
    .use(rehypeRaw)
    .use(rehypeSlug)
    .use(rehypeTitleAndHeadings)
    .use(rehypeRepoLinks)
    .use(rehypeKatex, { throwOnError: false, strict: 'ignore' })
    .use(rehypeKatexSearchText);
  for (const plugin of extraRehypePlugins) {
    if (Array.isArray(plugin)) processor.use(plugin[0], plugin[1]);
    else processor.use(plugin);
  }
  processor.use(rehypeStringify).freeze();

  /** Render the Markdown file at repoPath. */
  return async function renderSource(repoPath) {
    const full = path.join(REPO_ROOT, repoPath);
    let md = fs.readFileSync(full, 'utf8');
    md = md.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, ''); // Ignore front matter if any.
    // The absolute path lets Starlight's plugins check markdown.processedDirs.
    const file = new VFile({ value: md, path: full, data: { repoPath } });
    const out = await processor.process(file);
    return {
      source: md,
      html: String(out),
      title: file.data.title || fallbackTitle(repoPath),
      headings: file.data.headings || [],
    };
  };
}

function fallbackTitle(repoPath) {
  const base = path.posix.basename(repoPath, '.md');
  return base === 'README' ? path.posix.basename(path.posix.dirname(repoPath)) : base;
}

/** Cheap title lookup (first "# " heading) without a full render, for the sidebar. */
const titleCache = new Map();
export function quickTitle(repoPath) {
  if (titleCache.has(repoPath)) return titleCache.get(repoPath);
  let title = null;
  try {
    const md = fs.readFileSync(path.join(REPO_ROOT, repoPath), 'utf8');
    const m = md.match(/^#\s+(.+?)\s*#*\s*$/m);
    if (m) title = m[1].replace(/[*_`]/g, '').replace(/\[([^\]]*)\]\([^)]*\)/g, '$1');
  } catch {}
  if (!title) title = fallbackTitle(repoPath);
  titleCache.set(repoPath, title);
  return title;
}
