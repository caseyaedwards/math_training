# Website

This folder holds the [Astro](https://astro.build/) project that publishes the repository as a static website at <https://caseyaedwards.github.io/math_training/>.

The site has no content of its own. The build reads the Markdown in the repository folders and turns each file into a page.

## Run the Site Locally

Install [Node.js](https://nodejs.org/) 22.12 or later, then run these commands from the `site` folder:

```sh
npm install
npm run dev
```

Open <http://localhost:4321/math_training/> in a browser. The development server rebuilds a page when you save its Markdown file.

When Astro starts the development server in the background, `npx astro dev stop` stops it and `npx astro dev logs` shows its output.

To build the full site and preview the result:

```sh
npm run build
npm run preview
```

The build writes the finished site to `site/dist/`.

## How Pages Are Made

The site uses [Starlight](https://starlight.astro.build/), the Astro documentation theme. Starlight supplies the page frame: the header with search, the theme select and the page width select, the sidebar on the left, the **On this page** list on the right, and the previous and next links.

The build reads Markdown from these locations:

* `README.md` at the repository root becomes the home page.
* Every `.md` file under `course/`, `tracks/`, `workshops/`, `history/`, `resources/` and `docs/` becomes a page.

The page address follows the file path:

| File | Page |
|---|---|
| `course/README.md` | `/math_training/course/` |
| `course/101/01-place-value-and-the-number-line/README.md` | `/math_training/course/101/01-place-value-and-the-number-line/` |
| `course/101/checkpoint.md` | `/math_training/course/101/checkpoint/` |

A content loader (`src/lib/loader.mjs`) fills the Starlight `docs` collection from these files. It does not use `src/content/docs/`. For each file, the loader does the following:

* Takes the first `#` heading as the page title and removes it from the body, because Starlight prints the title above the page.
* Collects the `##` and `###` headings for the **On this page** list.
* Renders the Markdown to HTML with its own unified pipeline (`src/lib/content.mjs`).
* Sets the **Edit page** link to the file on GitHub.

The pipeline does the following:

* Rewrites links between Markdown files to page addresses: `x/README.md` becomes `x/` and `y.md` becomes `y/`.
* Sends links to `obsidian/`, `svg/` and code files such as `.py` and `.go` to the file on GitHub.
* Renders math between `$...$` and `$$...$$` with KaTeX. A `$$...$$` formula on one line renders as display math, as on GitHub.
* Keeps raw HTML such as `<details>` and drops HTML comments.
* Runs the rehype plugins that Starlight and Expressive Code register with Astro, so headings get anchor links and code blocks get Expressive Code frames. For this reason `astro.config.mjs` sets the Markdown processor to `unified()`.

The `content-assets` integration copies images and data files (`.svg`, `.png`, `.jpg`, `.tsv`, `.csv`, `.go`) to the same path on the site, so `img/foo.svg` resolves.

A missing folder or a broken link does not stop the build. A broken link leads to the site 404 page.

## Sidebar

`src/lib/sidebar.mjs` builds the sidebar from the folders and their `README.md` index files, so a new page appears without a configuration change:

| Group | Source |
|---|---|
| Start Here | The home page and `docs/STUDY_PLAN.md` |
| Course | One group per level folder (`course/101/` and so on): the level overview, the lessons in folder order, and the checkpoint |
| Tracks | One group per `##` section of `tracks/README.md`, with the tracks that the section links to |
| Workshops | Each workshop folder |
| History | The era chapters, **Story of an Idea** and **Biographies**, in the order that each `README.md` links to them |
| Resources | Each file and folder in `resources/` |
| Contributing | The other files in `docs/` |
| Diagram Showcase | A link to `/math_training/diagrams/` |

Notes in `img/` and `code/` folders become pages but stay out of the sidebar. Starlight opens the group that holds the current page. The other groups below **Course** start collapsed.

## Theme

The theme matches the [Full-Stack Engineer Path](https://caseyaedwards.github.io/fullstack-engineer-training/) site:

| File | Purpose |
|---|---|
| `src/styles/theme.css` | Ivory and clay colors for light and dark mode, as Starlight color variables |
| `src/styles/custom.css` | Serif headings, answer blocks (`<details>`), KaTeX spacing and code tab width |
| `src/styles/diagrams.css` | A paper card for each SVG diagram in both modes |
| `src/styles/width.css` | Content widths for the page width select |
| `src/components/ThemeSelect.astro` | Adds the page width select beside the theme select |

Code blocks use Expressive Code with the `vitesse-dark` and `vitesse-light` themes. The KaTeX style sheet loads on every page.

## Page Width

The header has a page width select: **Slim** is 38rem, **Medium** is 45rem and the default, **Wide** is 60rem, and **Full** fills the window. The browser remembers the choice in `localStorage` under `page-width`. A script in the page head applies the choice before the first paint.

## Code Layout

| Path | Purpose |
|---|---|
| `astro.config.mjs` | Site address, base path `/math_training`, Starlight settings and the asset integration |
| `src/content.config.ts` | Defines the Starlight `docs` collection with the repository loader |
| `src/lib/config.mjs` | Content folders, asset types and GitHub addresses |
| `src/lib/content.mjs` | Finds the Markdown, renders it and rewrites links |
| `src/lib/loader.mjs` | Content loader for the `docs` collection, including the 404 page |
| `src/lib/sidebar.mjs` | Builds the sidebar |
| `src/lib/assets.mjs` | Serves assets in development and copies them into `dist/` after the build |

Starlight builds the search index with Pagefind after each build.

## How Deployment Works

The workflow in [.github/workflows/pages.yml](../.github/workflows/pages.yml) publishes the site:

1. A push to `main`, or a manual run from the Actions tab, starts the workflow.
2. The build job installs the packages with `npm ci`, builds the diagram showcase, runs `npm run build` in `site/` and uploads `site/dist/` as the Pages artifact.
3. The deploy job publishes the artifact to GitHub Pages.

Before the first deployment, open the repository settings on GitHub, go to **Pages**, and set **Source** to **GitHub Actions**.

## Update Dependencies

The package versions in `package.json` are exact. The `@astrojs/markdown-remark` package provides the `unified()` processor that `astro.config.mjs` uses. To upgrade, change the version numbers, run `npm install` to refresh `package-lock.json`, and run `npm run build` to confirm that the site still builds.

## Diagram Showcase

CI runs `python3 -m svgmath showcase --out ../site/public/diagrams` from `svg-generator/` before the build. The site serves the result at `/diagrams/`. To preview it locally, run the same command first. The output is about 42 MB and stays out of git.
