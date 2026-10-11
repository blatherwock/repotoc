# Spec: artifact rendering

## Objective

The rendering layer turns module models (0001) into the artifact: a folder of Markdown doc files mirroring the source tree, plus index files. The artifact gives agents a "table of contents" of a repository without scanning, grepping, or loading source files. This is the second of three specs for repotoc; it requires the collection models and precedes the delivery surface (0003).

## Requirements

For each module model, one doc file at the mirrored path: source `src/foo/bar.py` produces `<output>/src/foo/bar.md`. `__init__.py` is the exception: a doc file renders only when the module has visible members (after the visibility filter). A docstring-only or import-only `__init__.py` gets no doc file, because its docstring surfaces in the index files instead.

A doc file states the source path as a heading, then outlines members in model order. The member-depth setting caps the outline; the default is unlimited. Each member renders as a section: a heading naming it, its docstring as a blockquote, then its source as a fenced Python block (decorators above the signature line) when `file_include_signatures` is on. Heading level mirrors nesting depth: module-level members render H2, members of classes render one level deeper, clamped at H6.

A directory containing doc files, child indexes, or an `__init__.py` docstring gets a `repotoc_index.md`. The index renders the folder's `__init__.py` docstring in full as a blockquote under the title, then the folder contents as a nested list. Entries carry a `file: ` or `dir: ` prefix and link to the doc file (or child index) and to the source: a file entry links to its source file, a directory entry to its `__init__.py`; a directory without one carries no source link. An `__init__.py` without a doc file gets no `file: ` entry. Each entry ends with `: <first line>`, the first line of the target's docstring: a module contributes its own docstring, and a directory takes the docstring of the `__init__.py` directly inside it. Entries whose target has no docstring render without the suffix. The root index is the scanning entry point.

List depth comes from `toc_max_depths`, one depth per index level: position 1 sets the root index's depth, each later position sets the next level's, and the last position applies to every deeper level. Depth counts list-indentation levels; a directory at the last level is listed but not expanded. The default depth is 6.

Rendering is deterministic: the same models and presentation config always produce byte-identical files.

Presentation settings are namespaced by domain: `file_*` applies to doc files (member levels), `toc_*` applies to indexes (directory levels under the output root).

- `file_member_depth`: outline depth in doc files. None (default) unlimited; 1 renders module-level members only; values below 1 rejected.
- `file_include_privates`: bool, default False. False omits underscore-private members; `__init__` and `__new__` always render; True shows all.
- `file_include_signatures`: bool, default True. False omits the fenced source block after each member section: documented members render heading and docstring blockquote only, undocumented members become bare headings.
- `toc_max_depths`: per-level list depths for indexes, as defined above. Default `(6,)`.

`RenderConfig` validates these at construction: an empty depth tuple, a depth below 1, or a member depth below 1 is rejected.

The output directory is owned by the tool: generation writes the current file set and deletes `.md` files it no longer produces.

## Decisions

- **Markdown artifacts for agents.** The artifact is a set of Markdown files holding all extracted docstrings. Rejected: a JSON dump (the consumer reads rather than parses, and Markdown is the cheapest form for an agent to read) and HTML (templating weight, no benefit to the consumer).
- **Output mirrors the source tree.** One doc file per module at the mirrored relative path, except docstring-only or import-only `__init__` files (see the `__init__` decision below). Rejected: a single combined file (context bloat on large repos) and per-package files (bloat within a big package).
- **Namespaced presentation settings.** Each setting applies to exactly one domain, so the prefix carries the meaning: `file_*` settings govern doc files, `toc_*` settings govern indexes. Rejected: flat names (an unnamespaced surface drifts as features grow and leaves "which hierarchy?" ambiguity on every setting).
- **Member depth unlimited by default.** `file_member_depth` defaults to unlimited: collect and show a lot; heavy repos dial it back (1 renders module-level members only). The collector never descends into function bodies and never collects variables or attributes, so the ladder is clean: module members at depth 1, class members (methods and inner classes alike) at 2, inner-class members at 3. Rejected: default 1 (the common path wants the file's API surface; dialing back is the exception) and per-tree-level file settings (an aesthetic choice per repo, not per folder).
- **Nested index lists.** An index lists its folder contents as a nested list: files prefixed `file: `, directories `dir: `. Each entry links to the doc file (or child index) and to the source, so an agent can scan at any depth and jump to either: a file entry to its source file, a directory entry to its `__init__.py`. A directory without an `__init__.py` carries no source link (links to directories fail in some editors). Rejected: flat direct-children-only lists (deep trees force opening child indexes to see anything).
- **`__init__` docstring under the index title.** A folder's `__init__.py` docstring renders in full under the title, so the index describes its root before the contents.
- **Per-level list depth.** `toc_max_depths` sets the depth per index level: position 1 sets the root index's depth, each later position sets the next level's, and the last position applies to every deeper level. A one-element tuple applies the same depth everywhere; per-level values exist for repos that want the root index shallower than the deeper indexes. The TOML encoding (bare int or list, coerced) is a 0003 decision. Rejected: a single global depth (a shallow root index and a deep package index want different reaches).
- **Tool-owned index file name.** The index file is `repotoc_index.md`, so a repository's own `index.md` cannot collide with a rendered file.
- **First-line summaries on entries.** Each entry ends with the target's first docstring line, so an agent can grasp the contents without opening the files.
- **Public members plus `__init__` and `__new__` by default.** Underscore-prefixed members are omitted; `file_include_privates` includes them. `__init__` and `__new__` carry the constructor contract, so they stay. Rejected: everything (dunder boilerplate adds noise) and public-only (constructors would vanish).
- **Doc files always render full docstrings.** The truncation booleans are gone: doc files are the complete reference, and the index entry suffixes carry the summary duty. Two views, two jobs. Rejected: a global truncate switch and per-kind truncation (the suffixes already summarize, so doc-file truncation served no distinct view). Reintroducing truncation is cheap if doc files prove too noisy.
- **Raw docstring text in blockquotes.** Docstrings pass through unmodified as blockquote lines; a blank docstring line renders as a bare `>`. No Google, NumPy, or reST convention parsing. Rejected: fenced blocks (raw text could contain fence markers, forcing the fence to grow, and blockquotes read better for prose) and structured parsing (conventions vary across repos and the consumer tolerates raw text).
- **`__init__` doc files only when they define something.** An `__init__.py` with visible members renders like any module. A docstring-only or import-only one gets no doc file: its docstring already surfaces in the indexes (full blockquote under the title, first-line suffix on the directory entry), and definitions are what make a doc file worthwhile. The criterion is visible members, so `file_include_privates` decides whether a private-only `__init__.py` emits. Rejected: always emitting (empty outlines and dunder-heavy noise for import-only files).
- **Hand-rolled Markdown emission, no Markdown library.** The Markdown surface is five constructs: headings, fenced code blocks, blockquotes, links, and bullet lists. All f-string work. Rejected: a Markdown emitter library (a dependency carrying constructs we do not use, and the mainstream Markdown packages are parsers, the wrong direction for emission). Hand-rolling also keeps byte-level determinism under direct control, which `--check` (0003) depends on.
- **Headings per member, source below.** Each member renders as a section: a heading naming it, its docstring blockquote, then a fenced Python block carrying its decorators and signature, like a footnote. Heading level mirrors nesting depth: module-level members H2, members of classes H3, clamped at H6. Decorators render above the signature line in source order. Undocumented members render heading and source block only. Rejected: signatures above docstrings (the heading already carries the name, so the signature reads as reference detail, not as the title).
- **Byte-determinism.** The same models and config always produce byte-identical files. Required for the `--check` mode (0003) to be meaningful.
- **The output directory is tool-owned.** Generation deletes `.md` files under the output directory that the current run does not produce. Rejected: additive writes only (a renamed module would leave a stale file forever).

## Testing strategy

Every behavior below is exercised by unit tests; the package is held at 100% line and branch coverage by the coverage gate defined in `0001-docstring-collection.md`.

### Rendering: normal operation

- When a module model is rendered, its doc file states the source path, renders the module docstring in full, then the outline in model order.
- When a member is public, or is `__init__` or `__new__`, it renders; when it is underscore-prefixed and `file_include_privates` is off, it is omitted.
- When a member carries decorators, they render above its signature line in source order.
- When `file_member_depth` caps the outline, members below the cap are omitted: 1 renders module-level members only.
- When `file_include_signatures` is off, documented members render heading and docstring blockquote only, and undocumented members become bare headings.
- When a directory contains doc files or child indexes, its `repotoc_index.md` renders its contents as a nested list: entries carry the `file: ` or `dir: ` prefix, link to the doc file (or child index) and to the source (the module's file, or the directory's `__init__.py`), and end with the target's first docstring line. A directory takes its summary from its `__init__.py`.
- When a folder's `__init__.py` has a docstring, the folder's index renders it in full as a blockquote under the title.
- When an `__init__.py` has visible members, its doc file renders like any module's and its `file: ` entry appears in the index. When it has none, neither renders.
- When an index list reaches its depth setting, a directory entry is listed but not expanded.
- When `toc_max_depths` gives index levels their own depths, the root index uses position 1, the next level down uses position 2, and the last position applies to every deeper level.
- When the same models are rendered twice, the outputs are byte-identical.

### Rendering: edge cases

- When a docstring contains Markdown or backticks, it passes through unchanged inside its blockquote.
- When an entry's target has no docstring, the index entry renders without the summary suffix.
- When a directory has no `__init__.py`, its entry carries no source link.
- When a directory holds no doc files, no child indexes, and no `__init__.py` docstring, it gets no index and no entry in its parent's list.

### Config: failure handling

- When `RenderConfig` is constructed with an empty `toc_max_depths`, a `toc_max_depths` entry below 1, or a `file_member_depth` below 1, construction is rejected.

### Output: normal operation

- When generation completes, the output directory contains exactly the generated doc files and indexes.
- When a previously generated file is no longer produced, generation deletes it from the output directory.
- When the output directory does not exist, it is created.

### Output: failure handling

- When the output directory cannot be created or written (permissions), generation fails with the offending path.

### Library API (IPO) [proposed]

- Inputs: module models plus presentation config (output path, `file_member_depth`, `file_include_privates`, `file_include_signatures`, `toc_max_depths`).
- Process: render models to file texts; write the output directory; prune stale files.
- Outputs: the rendered file set; a generation report of written and deleted paths.
- Failure outputs: an exception carrying the offending path for filesystem problems.

## Out of scope

- Collection: 0001. Config resolution, CLI, and check mode: 0003.
- Artifacts other than Markdown (JSON, HTML) and convention parsing: future specs if wanted.

## Related documents

- Requires `0001-docstring-collection.md`; followed by `0003-delivery-surface.md`.
