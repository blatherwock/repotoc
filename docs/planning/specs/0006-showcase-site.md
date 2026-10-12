# Spec: showcase site

*Revised in place after the MVP shipped: the structure rework in
`plans/0007-showcase-structure-view.md` and the later content pass are
folded in below, so the spec sits consistent with the shipped page.*

## Objective

Create a GitHub Pages project website for RepoTOC. The site is a showcase, not generated API documentation: a visitor understands within thirty seconds what RepoTOC is, how to install it, and what its output looks like. This spec covers the end-to-end MVP: a hand-written static site committed to the repository, example content refreshed by `just` recipes, and a GitHub Actions workflow that publishes the site when a release tag is pushed.

## Requirements

### Site

The site lives in `site/` at the repository root and is a single page:

- `index.html`, one stylesheet, and committed example files; no other assets required to render.
- The page has five sections:
  - Hero: a one-sentence statement of what RepoTOC does for a coding agent, the install command, and a link to the source.
  - Showcase, in two steps, each reading input to output:
    - Structure: three columns. The fixture source tree, the doc tree RepoTOC writes for it, and the rendered index for `fixture/arcade/`. One toggle above the index sets its depth: 6 (the default) or 2. The doc tree is derived from the source tree by name mapping (`__init__.py` to `repotoc_toc.md`, `x.py` to `x.md`), so its rows line up with the source rows beside it. Fixed collapse rules fold `pong/` and `players/strategies/` to one line each; the highlighted `minimax.py` and `minimax.md` tie the trees to the step below.
    - One module: the fixture source on the left, its generated Markdown on the right, with toggles for signatures, private members, and member depth, corresponding to the presentation flags (`file_include_signatures`, `file_include_privates`, `file_member_depth`).
  - The swap is CSS: native checkboxes and radios plus sibling selectors choose the visible variant. The page ships no JavaScript; the browser never generates.
  - Agents: the `AGENTS.md` snippet from the README that points an agent at the artifact, and links to this repository's own `AGENTS.md` and `docs/repotoc/`.
  - Upkeep: the pre-commit hook, `repotoc --check` for CI, and deterministic output. Settings live under `[tool.repotoc]`; the page points at the README for the list and the exit codes rather than enumerating either.
  - Comparison: a table covering documentation site generators (Sphinx, MkDocs with mkdocstrings), Markdown API generators (lazydocs, pydoc-markdown), and agent context tools (Aider's repo map, Repomix). A closing paragraph covers docstring requirements: those tools work best with structured docstring styles, while RepoTOC writes each docstring as it is and lists members without docstrings.
- External CDN assets are acceptable: fonts, stylesheets, and standard resets. The page ships no JavaScript; a genuine future need reopens the language decision.
- All asset URLs are relative, so the page works at any serving location: the custom domain root and the default `https://blatherwock.github.io/repotoc/` path.
- A `.nojekyll` file sits at the site root so GitHub Pages performs no Jekyll processing.
- The published artifact contains the page and `examples/` only: the workflow uploads `site/` wholesale, and the build script lives outside it (see Decisions). Publishing `examples/` keeps the showcase verifiable against fetchable, diffable files.

The tool's own artifact (`docs/repotoc/`) is unrelated to the site; `repotoc` never reads or writes inside `site/` during its normal run [confirmed].

### Example pipeline

- `site/examples/fixture/` holds a fixture project that reads as a real one: a plausible package name, a nested source tree four directories deep, and files that exercise the full collection surface: modules, classes, functions and methods, with and without docstrings, underscore-prefixed private members, and signature variety. The fixture is themed as a small arcade: a faux implementation of one or two simple games (checkers, chess, pong, and the like), which gives the modules natural domain vocabulary instead of placeholder text. The specific game and module layout is a plan detail; use generic game names. Files stay short and modules narrow so the generated text stays scannable. The fixture is real Python in the tree and passes the repository lint and type checks.
- `site/examples/generated/` holds the committed `repotoc` output for the fixture: the default run, plus one variant per toggle combination the showcase exposes. The exact matrix is a plan detail.
- A small build script (`src/tools/site_build.py`, standard library only) embeds the fixture source, the two tree blocks (`tree-source` and `tree-doc`), and the variant outputs rendered to HTML into marked blocks in `index.html`. Everything outside the marked blocks is untouched.
- Every toggle combination the UI exposes must have a committed variant; the gates validate the matrix is complete.
- Each variant output is its own tool-owned directory: a refresh prunes `.md` files the current runs no longer produce.

### Recipes and gates

- `just site` serves `site/` on localhost for preview.
- `just site-examples` refreshes the pipeline: runs `repotoc` on the fixture, then embeds the results into `index.html`.
- `just fix` also runs the example refresh, so one command makes everything current.
- `just check` gates both layers: the fixture artifact (`repotoc --check` against the fixture) and the embedding (build script `--check`). Both exit 1 naming stale files.
- The `check` job in `tests.yml` gains the same two gates, keeping CI in parity with `just check`.
- `site/build.py` is tested with the repository's pytest suite and joins the 100% coverage gate.

### Deployment

- `.github/workflows/pages.yml` publishes the site using `actions/upload-pages-artifact` and `actions/deploy-pages`, with the `pages` write and `id-token` write permissions and a `github-pages` environment.
- The workflow triggers on push of `v*` tags and on manual dispatch. It does not trigger on pushes to `main`.
- The workflow runs the two freshness gates before uploading; a failing gate aborts the deploy and the live site keeps its previous version.
- `site/CNAME` holds the custom domain `blatherwocky.com/repotoc/`, so the artifact carries the domain on every deploy.
- One-time setup, outside this repository: a DNS `CNAME` record `blatherwocky.com/repotoc/` pointing to `blatherwock.github.io`, Pages source set to GitHub Actions in the repository settings, and HTTPS enforcement enabled once the certificate issues.

## Decisions

**Hand-written static HTML and CSS.** Rejected MkDocs, Sphinx, and other documentation generators: their output reads as generated documentation, which is both the wrong aesthetic for a showcase and too close to the package's own artifact. Rejected a JS-based generator (Astro, Eleventy): it would add a Node toolchain for a page this size.

**Site source lives in `site/` at the repository root.** Rejected `docs/`: that namespace belongs to the generated artifact and to GitHub's branch-based Pages convention, which we do not use.

**The build script lives at `src/tools/site_build.py`, outside the published directory.** Rejected `site/build.py`: the workflow uploads `site/` wholesale, so build machinery would publish with the page. Rejected top-level `tools/`: `src/tools` sits inside the self-artifact's sources (`src` and `tests`), and the artifact is a map of the repo for agents, not only the package API, so surveying tooling belongs there. The script is not packaged for consumers: `uv` builds only `src/repotoc`.

**The site is built by recipes and committed statically.** Rejected deploy-time generation: a coding agent working on `main` could not see the final site source, and the published page would diverge from what is reviewable in the repository.

**Deployment triggers on release tags.** A push of `main` may change site content for unreleased behavior; the live site must reflect the latest tagged release only. Manual dispatch remains available as a deliberate override. Rejected deploying on push to `main`: it would publish unreleased work.

**No version picker in the MVP.** Each tag's `site/` is preserved in git history, so a picker can be added later without groundwork; building one now adds machinery before there is a second version to pick.

**Examples are embedded by the build script, not hand-copied or rendered client-side.** Hand-copied examples drift silently from the tool's output; client-side Markdown rendering needs an external library or a janky custom renderer. The script rewrites only content between the marked blocks, so hand edits elsewhere are safe.

**The site serves at `blatherwocky.com/repotoc/`.** GitHub Pages cannot host a project site at a subpath of a custom domain, so each project takes a whole subdomain. Rejected a shared `workshop` subdomain with per-project subfolders: it needs a proxy layer in front of GitHub, which is out of scope for the MVP; revisit when a second project site exists.

**The swap is CSS-only; the page ships no JavaScript.** Rejected client-side generation: it would re-implement the renderer and could drift from the tool. The same logic keeps Markdown rendering out of the browser: the build script renders the variant outputs to HTML at refresh time, so the swap swaps finished documents. Rejected TypeScript and JS test frameworks: both require a Node toolchain, and compiled output is not the hand-editable source. All logic stays in `src/tools/site_build.py`, inside the repository's unit test and coverage standards. A stateful future feature (for example the version picker) reopens this decision.

**CDN assets are acceptable; the page ships no JavaScript.** A font or a standard CSS reset from a CDN is normal for a marketing page. The page carries no scripts in the MVP; a genuine need reopens the language decision. The page content stays readable if CDN assets fail to load.

**The showcase leads with a structure view, not a view switch.** Rejected one output pane switching between a module doc file and the root index: the panel did two jobs, and the mirrored tree structure never showed. The showcase ships two steps: the source tree, the doc tree, and an index sample; then one module beside its doc file.

**The tree blocks are generated with fixed collapse rules.** Rejected hand-written trees: they would drift from the fixture. `src/tools/site_build.py` derives the doc tree from the source tree by name mapping, folds `pong/` and `players/strategies/` to one line each, and marks `minimax.py` and `minimax.md`.

**The index sample is `fixture/arcade/repotoc_toc.md` at depths 6 and 2.** Rejected the output root's index: its heading is the variant directory name and its first level is a lone `fixture/` entry. Rejected depth 1: at the `arcade` level it showed a single line.

## Testing strategy

All `src/tools/site_build.py` behavior is unit tested under the repository's pytest suite and 100% coverage gate; the showcase swap is CSS and carries no logic of its own.

### Example refresh: normal operation

- When `just site-examples` runs after a fixture change, `site/examples/generated/` matches fresh `repotoc` runs across the toggle matrix, and the marked blocks in `index.html` hold the current fixture source and variant outputs.
- When `just fix` runs, the same refresh happens.

### Example refresh: failure handling

- When `repotoc` fails on the fixture (exit 2), the recipe fails and `index.html` is left unmodified.

### Example refresh: edge cases

- When a fixture file is deleted, each variant output is pruned of its `.md` files, and both tree blocks drop its row.
- When a source entry has no matching doc entry in the generated output, the refresh fails, naming the doc path.
- When the toggle matrix changes, the refresh produces the new variant set in full: old variants are pruned, new ones written.
- When `index.html` is hand-edited outside the marked blocks, the refresh preserves the edits verbatim.

### Freshness gates: normal operation

- When the fixture artifact and embedding are current, both gates pass and `just check` succeeds.

### Freshness gates: failure handling

- When the fixture changed without a refresh, the artifact gate exits 1 and names the stale files.
- When the embedding changed without a refresh, the embedding gate exits 1.

### Freshness gates: edge cases

- When a marked block is missing from `index.html`, the embedding gate fails with a message naming the missing marker, rather than silently skipping.
- When the UI exposes a toggle combination with no committed variant, the gate fails rather than shipping a broken swap.

### Showcase interaction: normal operation

- When a one-module toggle changes, the generated panel swaps to the matching variant without a page reload; the source panel is unchanged.
- When the index depth toggle changes, the index column swaps between the depth 6 and depth 2 variants.
- When the page loads, both steps show their default variant.

### Local preview: normal operation

- When `just site` runs, the site serves on localhost and the page renders with full typography.

### Local preview: edge cases

- When CDN assets fail to load, the page content and layout remain readable; CDN assets only enhance presentation.

### Deployment: normal operation

- When a `v*` tag is pushed, the workflow publishes `site/` as it exists at that tag.
- When the workflow is dispatched manually, it publishes `site/` at the chosen ref.

### Deployment: failure handling

- When a freshness gate fails during a deploy, the workflow aborts and the live site keeps its previous version.

### Deployment: edge cases

- The page loads correctly under any serving location with relative asset URLs: the custom domain root and the default `github.io` path.
- GitHub Pages performs no Jekyll processing on the artifact (`.nojekyll`).

## Out of scope

- Version picker for the site (recorded above as a future addition; needs its own spec).
- Preview deploys for pull requests.
- Custom domain DNS and certificate work (one-time setup described in Deployment; owned by the user, not this change).
- Analytics.
- Consolidating multiple project sites under one shared subdomain; needs a proxy layer and a second project to justify it.
- A JavaScript toolchain (TypeScript, JS test frameworks) and stateful front-end behavior (toggle persistence, URL state); reopened only by a genuine need.
- Additional pages beyond the single-page showcase; content iteration happens after the MVP ships.

## Related documents

- `README.md` holds the install text the hero adapts and the `AGENTS.md` snippet the agents section quotes.
- `docs/planning/plans/0006-showcase-site.md` and `docs/planning/plans/0007-showcase-structure-view.md` record the MVP build and the later structure rework.
- `docs/planning/specs/0005-recipe-commit-gates.md` defines the `just fix` and `just check` gates this change extends.
