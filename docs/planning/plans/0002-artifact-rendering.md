# Implementation plan: artifact rendering

## Overview

Implements `docs/planning/specs/0002-artifact-rendering.md`: module models become the Markdown artifact folder. A pure `filters.py` holds presentation config, visibility and truncation filters; `render.py` holds doc file rendering and index rendering; `generate.py` writes and prunes the tool-owned output directory. No runtime dependencies; no AST imports (TID251 guards the boundary).

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

- [ ] Task 3: Doc file rendering
  - For each `Module`: state the source path, render the module docstring (per truncation config), then outline members in model order. Each member renders as a fenced Python block: decorator lines above the signature line, docstring as a fenced block whose fence extends past any backtick run inside the text. Undocumented members render as bare signature blocks. Markdown in docstrings passes through unchanged.
  - Satisfies spec scenarios: Rendering normal operation (doc file structure, decorators, truncation); Rendering edge cases (Markdown passthrough, fence extension).
- [ ] Task 4: Index files
  - Generate one `index.md` per directory containing doc files or child indexes, listing modules and subdirectories by path; each entry links to both the doc file and the source file, computed as relative paths. The root index is the scanning entry point.
  - Satisfies spec scenarios: Rendering normal operation (index structure and links).
- [ ] Task 5: Determinism
  - Guarantee byte-identical output for the same models and config: no timestamps, no environment-derived text, stable ordering. Test by rendering twice and comparing bytes.
  - Satisfies spec scenarios: Rendering normal operation (byte-determinism).

### Checkpoint: Rendering

- [ ] Rendering scenarios green; determinism test green; 100% line and branch coverage held.

### Phase 3: Generation

- [ ] Task 6: generate
  - Write the rendered file set into the output directory, creating it when missing; delete `.md` files under the output directory that the current run does not produce; return a report of written and deleted paths; filesystem errors fail with the offending path.
  - Satisfies spec scenarios: Output normal operation; Output failure handling; Library API (IPO) outputs and failure outputs.
- [ ] Task 7: Dogfood
  - Generate repodoc's own artifact folder from `src` into `docs/repodoc` via a library call; inspect manually. Do not commit unless decided.
  - Satisfies spec scenarios: end-to-end proof of the spec objective.

### Checkpoint: Generation

- [ ] `just test` green at 100% coverage; `just check` clean; `docs/repodoc` exists and mirrors `src`.

## Risks and mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Fence markers inside docstrings break code blocks | Med | Fence-extension function picks a longer fence than any backtick run in the text; tested against pathological docstrings |
| Relative links to source files are wrong at nesting depths | Med | Unit-test the path computation at several depths |
| Pruning deletes user files if output points at the wrong directory | High | Owned-directory contract is spec'd; default output is `docs/repodoc`; prune only `.md` files; the generation report lists every deletion |

## Open questions

- Should this repository commit its own generated `docs/repodoc` folder? Affects the dogfood checkpoint only; decide at review.

## Related documents

- Implements `docs/planning/specs/0002-artifact-rendering.md`
- Requires plan `0001-docstring-collection.md` (models)
- Followed by `0003-delivery-surface.md` (plan)