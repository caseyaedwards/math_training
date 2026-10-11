// Loads the repository Markdown at build time and renders it to HTML.
// Nothing is copied into site/: the files are read straight from the repo.
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

function rehypeRepoLinks(options) {
  const { repoPath } = options;
  return (tree) => {
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

function rehypeCollectHeadings(options) {
  return (tree) => {
    let title = null;
    const headings = [];
    visit(tree, 'element', (node) => {
      if (!/^h[1-3]$/.test(node.tagName)) return;
      const text = toString(node).trim();
      if (node.tagName === 'h1' && title == null) title = text;
      if (node.tagName === 'h2') headings.push({ id: node.properties?.id, text });
    });
    options.result.title = title;
    options.result.headings = headings;
  };
}

/** Render the Markdown file at repoPath. */
export async function renderSource(repoPath) {
  let md = fs.readFileSync(path.join(REPO_ROOT, repoPath), 'utf8');
  md = md.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, ''); // Ignore front matter if any.
  const result = {};
  const file = await unified()
    .use(remarkParse)
    .use(remarkGfm)
    .use(remarkMath)
    .use(remarkDoubleDollarDisplay)
    .use(remarkRehype, { allowDangerousHtml: true })
    .use(rehypeRaw)
    .use(rehypeSlug)
    .use(rehypeRepoLinks, { repoPath })
    .use(rehypeKatex, { throwOnError: false, strict: 'ignore' })
    .use(rehypeCollectHeadings, { result })
    .use(rehypeStringify)
    .process(md);
  const fallback = path.posix.basename(repoPath, '.md');
  return {
    html: String(file),
    title: result.title || (fallback === 'README' ? path.posix.basename(path.posix.dirname(repoPath)) : fallback),
    headings: result.headings || [],
  };
}

/** Cheap title lookup (first "# " heading) without a full render, for breadcrumbs and prev/next. */
const titleCache = new Map();
export function quickTitle(repoPath) {
  if (titleCache.has(repoPath)) return titleCache.get(repoPath);
  let title = null;
  try {
    const md = fs.readFileSync(path.join(REPO_ROOT, repoPath), 'utf8');
    const m = md.match(/^#\s+(.+?)\s*#*\s*$/m);
    if (m) title = m[1].replace(/[*_`]/g, '').replace(/\[([^\]]*)\]\([^)]*\)/g, '$1');
  } catch {}
  if (!title) {
    const base = path.posix.basename(repoPath, '.md');
    title = base === 'README' ? path.posix.basename(path.posix.dirname(repoPath)) : base;
  }
  titleCache.set(repoPath, title);
  return title;
}

/** Folder that "owns" a page for prev/next purposes. */
function groupOf(repoPath) {
  const dir = path.posix.dirname(repoPath);
  if (path.posix.basename(repoPath) === 'README.md') return dir === '.' ? null : path.posix.dirname(dir);
  return dir;
}

/** Page index with breadcrumbs and neighbours. */
export function buildIndex() {
  const sources = listSources();
  const set = new Set(sources);
  const groups = new Map();
  for (const s of sources) {
    const g = groupOf(s);
    if (g == null) continue;
    if (!groups.has(g)) groups.set(g, []);
    groups.get(g).push(s);
  }
  for (const list of groups.values()) list.sort((a, b) => routeFor(a).localeCompare(routeFor(b)));

  return sources.map((repoPath) => {
    // Breadcrumb: every ancestor folder that has a README page.
    const crumbs = [];
    const parts = repoPath.split('/');
    const isReadme = parts[parts.length - 1] === 'README.md';
    const depth = isReadme ? parts.length - 2 : parts.length - 1;
    if (repoPath !== 'README.md') crumbs.push({ title: 'Home', href: withBase('/') });
    for (let i = 1; i <= depth; i++) {
      const readme = parts.slice(0, i).join('/') + '/README.md';
      if (set.has(readme)) crumbs.push({ title: quickTitle(readme), href: withBase(routeFor(readme)) });
    }
    const g = groupOf(repoPath);
    const siblings = g != null ? groups.get(g) || [] : [];
    const i = siblings.indexOf(repoPath);
    const link = (p) => (p ? { title: quickTitle(p), href: withBase(routeFor(p)) } : null);
    return {
      repoPath,
      route: routeFor(repoPath),
      crumbs,
      prev: siblings.length > 1 && i > 0 ? link(siblings[i - 1]) : null,
      next: siblings.length > 1 && i >= 0 && i < siblings.length - 1 ? link(siblings[i + 1]) : null,
    };
  });
}

export function navItems(nav) {
  return nav
    .filter((n) => fs.existsSync(path.join(REPO_ROOT, n.dir, 'README.md')))
    .map((n) => ({ ...n, href: withBase(n.href ?? (n.dir ? '/' + n.dir + '/' : '/')) }));
}
