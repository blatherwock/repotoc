# Implementation plan: showcase site

## Overview

Implements `docs/planning/specs/0006-showcase-site.md`: a single-page GitHub Pages showcase committed under `site/`, a fixture arcade project whose `repotoc` outputs are pre-generated into a toggle matrix and embedded by `src/tools/site_build.py`, a CSS-only showcase swap with no JavaScript, `just` recipes for refresh and gating, and a tag-triggered Actions workflow publishing to `blatherwocky.com/repotoc/`. Four phases: fixture, build script, page, wiring.

## Task list

### Phase 1: Fixture

- [x] Task 1: Tooling allowances for site code
  - `pyproject.toml`: ruff per-file-ignores for `site/examples/fixture/**` relaxing the missing-docstring rules (`D100` through `D105`, `D107`), so the fixture can demonstrate docstring-less members; coverage widened from `--cov=src/repotoc` to `--cov=src` in pytest addopts (with `[tool.coverage.run] source = ["src"]` kept in sync), so `src/tools/site_build.py` joins the 100% gate. Fixture files sit outside `src` and are never swept. Verify `just check` and `just test` stay green with the config change alone.
  - Satisfies spec scenarios: fixture lint and type requirements (supporting).
- [x] Task 2: Author the fixture arcade
  - A tree under `site/examples/fixture/` reading as a real project: plausible package name (`arcade`), at least four directories deep, generic game names (checkers and pong), one game with a nested subpackage to give the index real depth. Exercise the full collection surface: modules, classes with methods, functions, members with and without docstrings, underscore-prefixed private members, varied signatures. Files short, modules narrow. Passes `just check` (ruff, ty) with the Task 1 allowances.
  - Satisfies spec scenarios: example refresh normal operation (input side); fixture requirement.

### Checkpoint: fixture

- [x] `just check` and `just test` green; a manual run produces a complete artifact (verified 2025-01: run from `site/examples` with `repotoc fixture -o ...` roots the tree at `fixture/`, which the showcase index panel uses).

### Phase 2: Build script

- [x] Task 3: Embedding engine in `src/tools/site_build.py`
  - Standard library only. Marker pairs `<!-- repotoc:begin NAME -->` / `<!-- repotoc:end NAME -->` in `index.html`; the engine replaces only the content between markers, errors naming any missing marker, preserves everything outside markers verbatim, and produces deterministic output. A `check` comparison reports each block that differs, exiting 1.
  - Satisfies spec scenarios: freshness gates edge cases (missing marker); example refresh edge cases (hand edits preserved).
- [x] Task 4: Variant matrix and refresh/check commands
  - Matrix in `src/tools/site_build.py` as data: eight doc-file variants (cross product of `file_include_signatures` on/off, `file_include_privates` on/off, `file_member_depth` full/1) plus one run with `--toc-max-depths 1` for the shallow index view; nine `repotoc` runs total, into keyed directories under `site/examples/generated/`. `refresh` wipes the generated directory, runs every variant, then embeds the showcase module source, the eight doc-file renderings, and the two index renderings; any `repotoc` failure aborts before embedding so `index.html` stays unmodified. `check` runs `repotoc --check` per variant plus the embedding comparison, exiting 1 and naming stale files or blocks. Matrix validation: every combination the UI exposes must exist before embedding proceeds.
  - Satisfies spec scenarios: example refresh normal operation, failure handling (repotoc exit 2), edge cases (pruning, matrix change); freshness gates normal operation, failure handling, edge cases (matrix gap).
- [x] Task 5: Unit tests and coverage for the build script
  - `tests/test_site_build.py`, loading `src/tools/site_build.py` by file path with `importlib.util.spec_from_file_location` and registering it under the module name `site_build`; the `src` layout keeps `tools` off the import path (it is not an installed package), so tests load it by path. Cover: marker parsing and replacement, idempotence (embed twice, identical bytes), hand-edit preservation, missing-marker error, matrix-gap validation failure, check mode exits, refresh aborts without embedding on a failing run. `site_build.py` reaches 100% coverage via the Task 1 config. `just fix` regenerates the self-artifact so the new test module and `src/tools` itself appear in `docs/repotoc`.
  - Satisfies spec scenarios: all build script behavior under the testing strategy.

### Checkpoint: pipeline

- [x] `just test` green with `site_build.py` at 100% coverage (178 tests, 100% of `src`). The real-tree refresh idempotence and staleness checks need `index.html` from Task 6; they run at the Phase 3 checkpoint.

### Phase 3: Page

- [x] Task 6: `index.html` skeleton
  - The five sections (hero, showcase, configuration, CI gate, alternatives stub), toggle inputs (checkboxes: signatures, privates; radios: member depth, view, toc depth; defaults matching the tool), marker blocks for every embed (showcase source, eight doc variants, two index variants, each wrapped with a `data-variant` key), CDN font and reset links, `site/CNAME` with `blatherwocky.com/repotoc/`, and `site/.nojekyll`. Relative asset URLs throughout.
  - Satisfies spec scenarios: site section requirements.
- [x] Task 7: `style.css` and the CSS-only swap
  - `:has()`-based selectors map toggle states to `data-variant` blocks: three toggles select among the eight doc variants, the view and toc depth radios select among the two index variants, default variant visible on load. System font stack and reset fallbacks so content stays readable when CDN assets fail. Styled panels for the split view: source left, generated right.
  - Satisfies spec scenarios: showcase interaction normal operation (default on load, swap without reload); local preview edge cases (CDN failure).
- [x] Task 8: Populate and write copy
  - Run the refresh to embed real variants. Write the hero (one sentence, install command), one entry per `[tool.repotoc]` key with a one-line effect, the CI gate section with the exit-code table from the README, and the alternatives stub (Sphinx, MkDocs: what they do that RepoTOC does not, the reverse, when to choose which). Review in a browser via the Task 9 preview recipe.
  - Post-checkpoint change (user request): the variant panels render as styled Markdown instead of raw text. `site_build.py` gained a stdlib renderer for the artifact's grammar, with its own tests; rendered links resolve to the published variant files. The source pane stays raw code. Recorded in the spec.
  - Satisfies spec scenarios: hero, configuration, CI gate, alternatives content requirements.

### Checkpoint: page

- [x] Verified: HTML parses clean, zero `<script>` tags, page serves over http with relative assets. The real refresh is idempotent (two runs, identical bytes), `check` passes after refresh, and a forced fixture edit makes `check` exit 1 naming the stale items (reverted after). Every toggle effect was verified in the generated variants: signatures on/off (3 vs 0 code blocks), privates on/off (`_search` section present or absent), depth full/1 (2 vs 0 nested headings), toc depth 6/1 (19 vs 3 index lines). Full `just check` and `just test` green.

### Phase 4: Wiring

- [x] Task 9: justfile recipes and gates
  - `site`: serve `site/` from the container with the port published to the host; a host-only recipe in the `pi` and `shell` pattern (dedicated docker run with `-p 127.0.0.1:8000:8000` and `-it` for Ctrl+C) running `python3 -m http.server 8000 --directory site`. No Dockerfile change: the image already carries Python and `http.server` binds all container interfaces. `site-examples`: `uv run python src/tools/site_build.py refresh`. Add `site-examples` to `fix`, and `uv run python src/tools/site_build.py check` to `check`.
  - Satisfies spec scenarios: recipes and gates requirements; local preview normal operation.
- [x] Task 10: CI parity in `tests.yml`
  - The `check` job gains `uv run python src/tools/site_build.py check` after the existing `repotoc --check`, keeping CI in parity with `just check`.
  - Satisfies spec scenarios: recipes and gates (CI parity) requirement.
- [x] Task 11: `pages.yml` deployment workflow
  - Triggers: push of `v*` tags and `workflow_dispatch`, never pushes to `main`. Permissions `pages: write` and `id-token: write`, environment `github-pages`, concurrency group. Steps: checkout, `setup-uv`, `uv sync --frozen`, the `site_build.py check` gate, `upload-pages-artifact` with path `site`, `deploy-pages`. A failing gate aborts before upload.
  - Satisfies spec scenarios: deployment normal operation, failure handling.

### Checkpoint: end to end

- [x] From the working tree: `just fix`, `just check`, `just site-examples`, and `just test` all green (178 tests, 100% of `src`); `just site` correctly refuses inside the container per its host-only guard. The workflow mirrors the `actions/deploy-pages` documented shape with the repo's existing action versions (`checkout@v5`, `setup-uv@v6`). One-time user setup remains (DNS CNAME, Pages source, HTTPS enforcement); first publish lands on the next `v*` tag or a manual dispatch.

## Risks and mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| CSS-only swap grows unwieldy across four toggles | Med | Decoupled matrices (eight doc blocks keyed by three toggles, two index blocks keyed by two radios) with `data-variant` keys; one selector rule per toggle |
| Docstring-less fixture members violate pydocstyle | Med | Per-file-ignores scoped tightly to `site/examples/fixture/**` |
| Coverage extension sweeps fixture files into the 100% gate | Med | `omit` for `site/examples/**`; checkpoint verifies the gate stays green |
| `src` layout keeps `tools` off the import path, so tests cannot import `site_build.py` normally | Low | Load by file path via `importlib`, registering as `site_build` |
| Committed variant volume bloats diffs | Low | Narrow fixture; wipe-and-regenerate keeps the set exact |
| Container preview unreachable from the host browser | Low | Publish the port with `-p 127.0.0.1:8000:8000`; loopback binding keeps the dev server off the network |
| Pages DNS or certificate misconfiguration blocks launch | Med | One-time steps documented in the spec; verify with a manual dispatch before relying on the release tag |
| `:has()` unsupported in older browsers | Low | Acceptable for a showcase; the page degrades to showing every variant panel stacked, still readable |

## Related documents

- `docs/planning/specs/0006-showcase-site.md` is the behavior contract this plan implements.
- `docs/planning/specs/0005-recipe-commit-gates.md` defines the `just fix` and `just check` gates this change extends.
- `README.md` holds the install command and exit-code table the page adapts.
