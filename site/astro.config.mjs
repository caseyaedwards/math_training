// @ts-check
import { defineConfig } from 'astro/config';
import { unified } from '@astrojs/markdown-remark';
import starlight from '@astrojs/starlight';
import contentAssets from './src/lib/assets.mjs';
import { buildSidebar } from './src/lib/sidebar.mjs';
import { SITE, BASE, REPO_ROOT, SITE_TITLE } from './src/lib/config.mjs';

export default defineConfig({
  site: SITE,
  base: BASE,
  trailingSlash: 'always',
  build: { format: 'directory' },
  // The unified processor (not the default Sätteri) lets src/lib/loader.mjs run
  // the rehype plugins that Starlight and Expressive Code register here
  // (heading anchor links and code frames) on the repository Markdown.
  markdown: { processor: unified() },
  integrations: [
    starlight({
      title: SITE_TITLE,
      description: 'Free, self-paced math from arithmetic to proof.',
      favicon: '/favicon.svg',
      // Built from the folders and README index files (src/lib/sidebar.mjs).
      sidebar: buildSidebar(),
      // Starlight's heading links run on Markdown under these folders: the repository root.
      markdown: { processedDirs: [REPO_ROOT] },
      customCss: [
        'katex/dist/katex.min.css',
        './src/styles/theme.css',
        './src/styles/diagrams.css',
        './src/styles/custom.css',
        './src/styles/width.css',
      ],
      // Adds the page width select beside the theme select.
      components: { ThemeSelect: './src/components/ThemeSelect.astro' },
      // Applies the stored page width before first paint (see src/styles/width.css).
      head: [
        {
          tag: 'script',
          content:
            "(function(){var w='medium';try{var s=localStorage.getItem('page-width');if(s==='slim'||s==='wide'||s==='full')w=s}catch(e){}document.documentElement.setAttribute('data-width',w)})()",
        },
      ],
      // Syntax colours: Shiki's vitesse themes, whose muted greens, browns and
      // tans sit with the ivory and clay palette. The first theme is the default
      // (dark); Starlight's dark mode switch shows each theme in the matching site
      // mode. useStarlightUiThemeColors draws the frames from the site tokens
      // (src/styles/theme.css). Expressive Code lifts token colours to
      // minSyntaxHighlightingColorContrast against a fixed reference background;
      // 5.5:1 there keeps every token above 4.5:1 on the frame.
      expressiveCode: {
        themes: ['vitesse-dark', 'vitesse-light'],
        useStarlightDarkModeSwitch: true,
        useStarlightUiThemeColors: true,
        minSyntaxHighlightingColorContrast: 5.5,
        // Keep tabs as written. CSS sets how wide a tab looks.
        tabWidth: 0,
      },
    }),
    contentAssets(),
  ],
  vite: {
    // Allow the dev server to read Markdown and images from the repo root.
    server: { fs: { allow: [REPO_ROOT] } },
  },
});
