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

The build reads Markdown from these locations:

* `README.md` at the repository root becomes the home page.
* Every `.md` file under `course/`, `tracks/`, `workshops/`, `history/`, `resources/` and `docs/` becomes a page.

The page address follows the file path:

| File | Page |
|---|---|
| `course/README.md` | `/math_training/course/` |
| `course/101/01-place-value-and-the-number-line/README.md` | `/math_training/course/101/01-place-value-and-the-number-line/` |
| `course/101/checkpoint.md` | `/math_training/course/101/checkpoint/` |

During the build, the site does the following:

* Rewrites links between Markdown files to page addresses: `x/README.md` becomes `x/` and `y.md` becomes `y/`.
* Copies images and data files (`.svg`, `.png`, `.jpg`, `.tsv`, `.csv`, `.go`) to the same path on the site, so `img/foo.svg` resolves.
* Sends links to `obsidian/`, `svg/` and code files such as `.py` and `.go` to the file on GitHub.
* Renders math between `$...$` and `$$...$$` with KaTeX.
* Keeps raw HTML such as `<details>` and drops HTML comments.

A missing folder or a broken link does not stop the build. A broken link leads to the site 404 page.

## Code Layout

| Path | Purpose |
|---|---|
| `astro.config.mjs` | Site address, base path `/math_training` and the asset integration |
| `src/lib/config.mjs` | Content folders, asset types, navigation and GitHub addresses |
| `src/lib/content.mjs` | Finds the Markdown, renders it, rewrites links, builds breadcrumbs and previous and next links |
| `src/lib/assets.mjs` | Serves assets in development and copies them into `dist/` after the build |
| `src/pages/[...slug].astro` | Creates one page per Markdown file |
| `src/layouts/Page.astro` | Page frame: navigation, breadcrumb, contents list, footer |
| `src/styles/site.css` | All styles, with light and dark mode |

## How Deployment Works

The workflow in [.github/workflows/pages.yml](../.github/workflows/pages.yml) publishes the site:

1. A push to `main`, or a manual run from the Actions tab, starts the workflow.
2. The build job installs the packages with `npm ci`, runs `npm run build` in `site/` and uploads `site/dist/` as the Pages artifact.
3. The deploy job publishes the artifact to GitHub Pages.

Before the first deployment, open the repository settings on GitHub, go to **Pages**, and set **Source** to **GitHub Actions**.

## Update Dependencies

The package versions in `package.json` are exact. To upgrade, change the version numbers, run `npm install` to refresh `package-lock.json`, and run `npm run build` to confirm that the site still builds.

## Diagram Showcase

CI runs `python3 -m svgmath showcase --out ../site/public/diagrams` from `svg-generator/` before the build. The site serves the result at `/diagrams/`. To preview it locally, run the same command first. The output is about 42 MB and stays out of git.
