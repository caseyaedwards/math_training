// Astro content loader for Starlight's docs collection. It reads the Markdown
// in the repository folders (not src/content/docs/) and renders each file with
// the unified pipeline in content.mjs, so math, raw HTML, link rewriting and
// display math work as before.
import path from 'node:path';
import { createRenderer, idFor, listSources } from './content.mjs';
import { REPO_ROOT, CONTENT_DIRS, GITHUB_BLOB, BASE } from './config.mjs';

/**
 * Rehype plugins that Starlight and Expressive Code register with Astro's
 * unified Markdown processor (astro.config.mjs sets `markdown.processor`).
 * Running them here gives the pages Starlight's heading anchor links and
 * Expressive Code frames, with the same settings as Markdown in src/.
 */
function configuredRehypePlugins(config) {
  const plugins = config.markdown?.processor?.options?.rehypePlugins;
  return Array.isArray(plugins) ? plugins : [];
}

const notFound = {
  id: '404',
  title: 'Page Not Found',
  html: `<p>This page does not exist yet. The material is still being written, so the link may work later.</p>
<p><a href="${BASE}/">Return to the home page</a>.</p>`,
};

export function repoMarkdownLoader() {
  return {
    name: 'repo-markdown-loader',
    load: async ({ store, parseData, generateDigest, config, logger, watcher }) => {
      const render = createRenderer({ extraRehypePlugins: configuredRehypePlugins(config) });

      const loadOne = async (repoPath) => {
        const { source, html, title, headings } = await render(repoPath);
        const id = idFor(repoPath);
        const data = await parseData({
          id,
          data: { title, editUrl: GITHUB_BLOB + encodeURI(repoPath) },
        });
        store.set({
          id,
          data,
          body: source,
          digest: generateDigest(source),
          rendered: { html, metadata: { headings } },
        });
      };

      const sources = listSources();
      store.clear();
      for (const repoPath of sources) await loadOne(repoPath);

      const data = await parseData({
        id: notFound.id,
        data: { title: notFound.title, editUrl: false, pagefind: false },
      });
      store.set({
        id: notFound.id,
        data,
        digest: generateDigest(notFound.html),
        rendered: { html: notFound.html, metadata: { headings: [] } },
      });
      logger.info(`Loaded ${sources.length} Markdown files`);

      // Development server: re-render a page when its Markdown changes.
      if (watcher) {
        const dirs = CONTENT_DIRS.map((d) => path.join(REPO_ROOT, d));
        watcher.add([path.join(REPO_ROOT, 'README.md'), ...dirs]);
        const onChange = async (file) => {
          if (!file.endsWith('.md')) return;
          const rel = path.relative(REPO_ROOT, file).split(path.sep).join('/');
          if (!listSources().includes(rel)) return;
          await loadOne(rel);
          logger.info(`Reloaded ${rel}`);
        };
        watcher.on('change', onChange);
        watcher.on('add', onChange);
      }
    },
  };
}
