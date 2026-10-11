// Builds the Starlight sidebar from the repository folders and their README
// index files, so a new lesson, track or biography shows up without a config
// change. Order follows the README links where a README lists its children,
// and the file names otherwise.
import fs from 'node:fs';
import path from 'node:path';
import { REPO_ROOT, DIAGRAMS_PATH } from './config.mjs';
import { idFor, quickTitle } from './content.mjs';

const exists = (rel) => fs.existsSync(path.join(REPO_ROOT, rel));
const readText = (rel) => (exists(rel) ? fs.readFileSync(path.join(REPO_ROOT, rel), 'utf8') : '');

/** Folders that hold figures or code for a page. Their notes stay out of the sidebar. */
const SUPPORT_DIRS = new Set(['img', 'code']);

function subdirs(dir) {
  let entries = [];
  try {
    entries = fs.readdirSync(path.join(REPO_ROOT, dir), { withFileTypes: true });
  } catch {
    return [];
  }
  return entries
    .filter((e) => e.isDirectory() && !e.name.startsWith('.') && !SUPPORT_DIRS.has(e.name))
    .map((e) => e.name)
    .sort();
}

function markdownFiles(dir) {
  let entries = [];
  try {
    entries = fs.readdirSync(path.join(REPO_ROOT, dir), { withFileTypes: true });
  } catch {
    return [];
  }
  return entries
    .filter((e) => e.isFile() && e.name.endsWith('.md') && e.name !== 'README.md')
    .map((e) => e.name)
    .sort();
}

/** Repo paths of the Markdown pages that a file links to, in the order of the links. */
function linkedPages(rel) {
  const out = [];
  const dir = path.posix.dirname(rel);
  for (const m of readText(rel).matchAll(/\]\(([^)\s#]+\.md)(?:#[^)]*)?\)/g)) {
    const target = path.posix.normalize(path.posix.join(dir, decodeURI(m[1])));
    if (!out.includes(target)) out.push(target);
  }
  return out;
}

/** Sort repo paths by where the folder README links to them, then by name. */
function byReadmeOrder(dir, paths) {
  const order = linkedPages(`${dir}/README.md`);
  const rank = (p) => {
    const i = order.indexOf(p);
    return i === -1 ? Infinity : i;
  };
  return [...paths].sort((a, b) => rank(a) - rank(b) || a.localeCompare(b));
}

const page = (rel, label) => (label ? { label, slug: idFor(rel) } : { slug: idFor(rel) });
const overview = (dir) => (exists(`${dir}/README.md`) ? [page(`${dir}/README.md`, 'Overview')] : []);

/** Child pages of a folder: its other Markdown files and the README of each subfolder. */
function childPages(dir) {
  const files = markdownFiles(dir).map((f) => `${dir}/${f}`);
  const folders = subdirs(dir)
    .map((d) => `${dir}/${d}/README.md`)
    .filter(exists);
  return byReadmeOrder(dir, [...files, ...folders]);
}

/** A folder as a sidebar group: its README as the overview, then its child pages. */
function folderGroup(label, dir, { collapsed = true } = {}) {
  return { label, collapsed, items: [...overview(dir), ...childPages(dir).map((p) => page(p))] };
}

// ---------- Course ----------

function levelLabel(dir) {
  const title = quickTitle(`${dir}/README.md`);
  return title.replace(/^(?:Course|Level)\s+/i, '').replace(/^(\d{3}):?\s*/, '$1 ');
}

function courseGroup() {
  const levels = subdirs('course').filter((d) => /^\d{3}$/.test(d));
  return {
    label: 'Course',
    items: [
      ...overview('course'),
      ...levels.map((level) => {
        const dir = `course/${level}`;
        const lessons = subdirs(dir)
          .filter((d) => /^\d{2}-/.test(d) && exists(`${dir}/${d}/README.md`))
          .map((d) => page(`${dir}/${d}/README.md`, `${Number(d.slice(0, 2))}. ${quickTitle(`${dir}/${d}/README.md`)}`));
        const checkpoint = exists(`${dir}/checkpoint.md`) ? [page(`${dir}/checkpoint.md`, 'Checkpoint')] : [];
        return { label: levelLabel(dir), collapsed: true, items: [...overview(dir), ...lessons, ...checkpoint] };
      }),
    ],
  };
}

// ---------- Tracks ----------

/** Groups from the "## Section" headings of tracks/README.md, each with the tracks it links to, labelled with the link text. */
function tracksGroup() {
  const groups = [];
  const listed = new Set();
  let current = null;
  for (const line of readText('tracks/README.md').split('\n')) {
    const h = line.match(/^##\s+(.+?)\s*$/);
    if (h) {
      current = { label: h[1], collapsed: true, items: [] };
      groups.push(current);
      continue;
    }
    if (!current) continue;
    // The link text is the short track name ("Calculus"), some page titles add "Track".
    for (const m of line.matchAll(/\[([^\]]+)\]\(([^)\s#]+\/README\.md)\)/g)) {
      const rel = path.posix.normalize(`tracks/${m[2]}`);
      if (!exists(rel) || listed.has(rel)) continue;
      listed.add(rel);
      current.items.push(page(rel, m[1].replace(/[*_`]/g, '')));
    }
  }
  const rest = subdirs('tracks')
    .map((d) => `tracks/${d}/README.md`)
    .filter((rel) => exists(rel) && !listed.has(rel));
  if (rest.length) groups.push({ label: 'More Tracks', collapsed: true, items: rest.map((rel) => page(rel)) });
  return { label: 'Tracks', collapsed: true, items: [...overview('tracks'), ...groups.filter((g) => g.items.length)] };
}

// ---------- History ----------

function historyGroup() {
  const eras = subdirs('history')
    .filter((d) => /^\d{2}-/.test(d) && exists(`history/${d}/README.md`))
    .map((d) => page(`history/${d}/README.md`));
  const items = [...overview('history')];
  if (eras.length) items.push({ label: 'Eras', collapsed: true, items: eras });
  if (exists('history/story-of-an-idea/README.md')) items.push(folderGroup('Story of an Idea', 'history/story-of-an-idea'));
  if (exists('history/biographies/README.md')) items.push(folderGroup('Biographies', 'history/biographies'));
  return { label: 'History', collapsed: true, items };
}

// ---------- Whole sidebar ----------

export function buildSidebar() {
  const sidebar = [];
  const startHere = [];
  if (exists('README.md')) startHere.push(page('README.md', 'Home'));
  if (exists('docs/STUDY_PLAN.md')) startHere.push(page('docs/STUDY_PLAN.md'));
  if (startHere.length) sidebar.push({ label: 'Start Here', items: startHere });
  if (exists('course/README.md')) sidebar.push(courseGroup());
  if (exists('tracks/README.md')) sidebar.push(tracksGroup());
  if (exists('workshops/README.md')) sidebar.push(folderGroup('Workshops', 'workshops'));
  if (exists('history/README.md')) sidebar.push(historyGroup());
  if (exists('resources/README.md')) sidebar.push(folderGroup('Resources', 'resources'));
  // Writing guides for contributors, except the study plan already under Start Here.
  const docs = markdownFiles('docs')
    .filter((f) => f !== 'STUDY_PLAN.md')
    .map((f) => page(`docs/${f}`));
  if (docs.length) sidebar.push({ label: 'Contributing', collapsed: true, items: docs });
  sidebar.push({ label: 'Diagram Showcase', link: DIAGRAMS_PATH });
  return sidebar;
}
