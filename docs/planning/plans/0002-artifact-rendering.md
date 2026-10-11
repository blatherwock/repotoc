# Implementation plan: artifact rendering

## Overview

Implements `docs/planning/specs/0002-artifact-rendering.md`: module models become the Markdown artifact folder. A pure `filters.py` holds the namespaced presentation settings and the visibility filter they drive. A `render` package holds rendering: `file_renderer.py` renders doc files, `index_renderer.py` renders indexes, `markdown.py` holds the emission helpers (fences, blockquotes, link and list lines, no model knowledge), `paths.py` computes doc paths and source links, and `render/__init__.py` exposes the public `render()` entry point. `generate.py` writes and prunes the tool-owned output directory.

`filters.py` and `models.py` stay single top-level modules; they earn a package only when they grow. No runtime dependencies; no AST imports (TID251 guards the boundary).

## Task list

### Phase 1: Presentation filters

- [x] Task 1: Render config and visibility filter
  - Add `RenderConfig(output, include_private, truncate_module, truncate_class, truncate_function)` and `Filters(config)`, a frozen object binding one config; visibility and truncation are its methods. Public names plus `__init__` and `__new__` render; `include_private` adds underscore-prefixed members; applied recursively through class bodies. Module docstrings are never filtered by visibility.
  - Satisfies spec scenarios: Rendering normal operation (visibility rules).
- [x] Task 2: Truncation
  - Reduce a docstring to its first line per kind when the flag is set. Collected docstrings are stripped of surrounding whitespace (collection-side), so a whitespace-only first line cannot occur.
  - Satisfies spec scenarios: Rendering normal operation (truncation); Rendering edge cases (empty first line).

### Checkpoint: Filters

- [x] `just test` green for filter scenarios; 100% line and branch coverage held.

### Phase 2: Doc files and indexes

- [x] Task 3: Doc file rendering
  - For each `Module`: state the source path as a heading, render the module docstring as a blockquote (per truncation config), then outline members in model order. Each member renders as a section: a heading naming it (module-level members H2, one level deeper per enclosing class, clamped at H6), its docstring as a blockquote, then its source as a fenced Python block with decorator lines above the signature line. The fence extends past any backtick run inside the text. Undocumented members render heading and source block only. Markdown in docstrings passes through unchanged.
  - Satisfies spec scenarios: Rendering normal operation (doc file structure, headings, decorators, truncation); Rendering edge cases (Markdown passthrough, fence extension).
- [x] Task 4: Index files
  - Generate one `repotoc_index.md` per directory containing doc files, child indexes, or an `__init__.py` docstring. The index renders the folder's `__init__.py` docstring in full as a blockquote under the title (regardless of truncation config), then the folder contents as a nested list: entries prefixed `file: ` or `dir: `, each linking to the doc file (or child index) and the source file via relative paths, and ending with `: <first line>`, the target's first docstring line (a module's own docstring; a directory takes its `__init__.py` docstring; no docstring, no suffix). An `__init__.py` without visible members gets no doc file and no `file: ` entry. List depth comes from `RenderConfig.index_depths` (default `(6,)`): position 1 sets the root index's depth, each later position sets the next level's, and the last extends deeper; a directory at the last level is listed but not expanded. The root index is the scanning entry point.
  - Satisfies spec scenarios: Rendering normal operation (index structure, nesting, depth, links, summaries, `__init__` handling); Rendering edge cases (missing docstrings, empty directories).
- [x] Task 5: Determinism
  - Guarantee byte-identical output for the same models and config: no timestamps, no environment-derived text, stable ordering. Test by rendering twice and comparing bytes.
  - Satisfies spec scenarios: Rendering normal operation (byte-determinism).

### Checkpoint: Rendering

- [x] Rendering scenarios green; determinism test green; 100% line and branch coverage held.

### Phase 3: Generation

- [x] Task 6: generate
  - Write the rendered file set into the output directory, creating it when missing; delete `.md` files under the output directory that the current run does not produce; return a report of written and deleted paths; filesystem errors fail with the offending path.
  - Satisfies spec scenarios: Output normal operation; Output failure handling; Library API (IPO) outputs and failure outputs.
- [x] Task 7: Dogfood
  - Generate repotoc's own artifact folder from `src` into `docs/repotoc` via a library call; inspect manually. Do not commit unless decided.
  - Satisfies spec scenarios: end-to-end proof of the spec objective.

### Checkpoint: Generation

- [x] `just test` green at 100% coverage; `just check` clean; `docs/repotoc` exists and mirrors `src` (left uncommitted pending the open question below).

### Addendum: render package (post-phase-2 review)

May run before or after phase 3; it is a refactor with no behavior change.

- [x] Task 8: Split `render.py` into a package
  - Turn `src/repotoc/render.py` into the `render` package. `file_renderer.py` holds doc file rendering; `index_renderer.py` holds index rendering; `markdown.py` holds the Markdown emission helpers (headings, fences, blockquotes, link and list lines) with no knowledge of the models; `paths.py` holds doc-path and source-link computation; `render/__init__.py` exposes the public `render()` entry point. `filters.py` and `models.py` stay top-level single modules. Mirror the split in `tests/render/`.
  - Satisfies: emission isolated from traversal and content decisions; no behavior change (rendered outputs byte-identical to the pre-split output).

### Checkpoint: render package

- [x] `just test` green at 100% coverage; `just check` clean; rendered output byte-identical to the pre-split output.

### Addendum: namespaced config surface (post-phase-2 review)

The post-phase-2 review locked the namespaced presentation settings: `file_*` settings govern doc files, `toc_*` settings govern indexes, doc files always render full docstrings (truncation is gone), and the index entry suffixes carry the summary duty. Phase 2 was implemented against the pre-revision spec, so its checked-off tasks predate the revised `__init__` and summary behaviors their descriptions now carry. These tasks brought the implementation to the revised spec in full: the config surface, the file-domain settings, `toc_max_depths`, and the `__init__` doc-file rule, index prologue blockquote, and entry summary suffixes from the revised Task 4 text. The config-surface reshaping alone leaves default rendering unchanged; those `__init__` and summary behaviors change the output as the revised spec prescribes. They may run before or after phase 3.

- [x] Task 9: Namespaced config surface
  - Reshape `RenderConfig` to `RenderConfig(output, file_member_depth, file_include_privates, file_include_signatures, toc_max_depths)`. Defaults: `file_member_depth` None (unlimited) or a positive int, `file_include_privates` False, `file_include_signatures` True, `toc_max_depths` `(6,)` with the per-level semantics `index_depths` already has. Remove the three truncation booleans and the truncation filter. Reject at construction: an empty `toc_max_depths`, a `toc_max_depths` entry below 1, or a `file_member_depth` below 1.
  - Satisfies spec scenarios: Config failure handling (validation); enforces the namespaced-settings decision.
- [x] Task 10: File-domain settings in doc file rendering
  - `file_member_depth` caps the outline: 1 renders module-level members only; members below the cap are omitted entirely. `file_include_privates` keeps the old private-flag semantics. `file_include_signatures` off omits the fenced source block: documented members render heading and docstring blockquote only; undocumented members become bare headings. Docstrings always render in full.
  - Satisfies spec scenarios: Rendering normal operation (member depth, signature toggle, privates, members below the cap).
- [x] Task 11: `toc_max_depths` in index rendering
  - Replace `index_depths` with `toc_max_depths` (identical per-level semantics; the last position extends deeper). The `__init__` blockquote clause "regardless of truncation config" becomes simply "always full".
  - Satisfies spec scenarios: Rendering normal operation (per-level depth); Rendering edge cases (missing docstrings).

### Checkpoint: config surface

- [x] `just test` green at 100% coverage; `just check` clean; the config-surface reshaping renders byte-identically to the pre-revision output at default settings; the `__init__` and summary behaviors render per the revised spec.

### Addendum: directory source links (post-dogfood review)

Dogfooding in an editor surfaced that directory entries linked to source directories, which some editors fail to open when clicked.

- [x] Task 12: Directory source links
  - A `dir: ` entry's source link targets the directory's `__init__.py`; when the folder has none, the entry carries no source link. File entries keep their source links. Directories learn their init from the module models, so a docstring-less or memberless `__init__.py` still links.
  - Satisfies spec scenarios: Rendering normal operation (index links); Rendering edge cases (directories without an `__init__.py`).

### Checkpoint: directory source links

- [x] `just test` green at 100% coverage; `just check` clean; `docs/repotoc` regenerated.

## Risks and mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Backtick runs inside fenced source blocks break the code block | Med | The fence-extension function picks a longer fence than any backtick run in the text; tested against pathological decorator string literals. Docstrings are blockquotes and cannot break the emission |
| Relative links to source files are wrong at nesting depths | Med | Unit-test the path computation at several depths |
| Pruning deletes user files if output points at the wrong directory | High | Owned-directory contract is spec'd; default output is `docs/repotoc`; prune only `.md` files; the generation report lists every deletion |

## Open questions

- Should this repository commit its own generated `docs/repotoc` folder? Affects the dogfood checkpoint only; decide at review.

## Related documents

- Implements `docs/planning/specs/0002-artifact-rendering.md`
- Requires plan `0001-docstring-collection.md` (models)
- Followed by `0003-delivery-surface.md` (plan)