import { defineCollection } from 'astro:content';
import { docsSchema } from '@astrojs/starlight/schema';
import { repoMarkdownLoader } from './lib/loader.mjs';

// Starlight's docs collection, filled from the repository Markdown instead of
// src/content/docs/ (see src/lib/loader.mjs).
export const collections = {
  docs: defineCollection({ loader: repoMarkdownLoader(), schema: docsSchema() }),
};
