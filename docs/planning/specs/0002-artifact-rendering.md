# Spec: artifact rendering

## Objective

The rendering layer turns module models (0001) into the artifact: a folder of Markdown doc files mirroring the source tree, plus index files. The artifact gives agents a "table of contents" of a repository without scanning, grepping, or loading source files. This is the second of three specs for repodoc; it requires the collection models and precedes the delivery surface (0003).

## Requirements

For each module model, one doc file at the mirrored path: source `src/foo/bar.py` produces `<output>/src/foo/bar.md`. Doc files outline every rendered member in model order, each as a signature code line followed by its docstring in a fenced block. A directory containing doc files or child indexes gets an `index.md` listing modules and subdirectories by path; each entry links to the doc file and the source file. The root index is the scanning entry point.

Rendering is deterministic: the same models and presentation config always produce byte-identical files.

Presentation settings: member visibility (public plus `__init__` and `__new__` by default; a flag includes underscore-private members) and per-kind docstring truncation (module, class, function; three booleans, default full).

The output directory is owned by the tool: generation writes the current file set and deletes `.md` files it no longer produces.

## Decisions

- **Markdown artifacts for agents.** The artifact is a set of Markdown files holding all extracted docstrings. Rejected: a JSON dump (the consumer reads rather than parses, and Markdown is the cheapest form for an agent to read) and HTML (templating weight, no benefit to the consumer).
- **Output mirrors the source tree.** One doc file per module at the mirrored relative path. Rejected: a single combined file (context bloat on large repos) and per-package files (bloat within a big package).
- **Index files at every directory level.** A directory containing doc files or child indexes gets an `index.md`; entries list by path and link to both the doc file and the source file, so an agent can scan at any depth and jump to either. Rejected: a single root index only (deep trees force scanning the whole index) and no indexes (per-module files alone give no entry point).
- **Public members plus `__init__` and `__new__` by default.** Underscore-prefixed members are omitted; a flag includes them. `__init__` and `__new__` carry the constructor contract, so they stay. Rejected: everything (dunder boilerplate adds noise) and public-only (constructors would vanish).
- **Truncation is per kind.** Three booleans reduce module, class, or function docstrings to their first line independently. A single global switch cannot express differing noise tolerance per kind; module docstrings are usually longer than a useful function summary.
- **Raw docstring text in fenced blocks.** Docstrings pass through unmodified inside fenced code blocks; the fence extends when the text contains a fence marker. No Google, NumPy, or reST convention parsing. Rejected: structured parsing (conventions vary across repos and the consumer tolerates raw text).
- **Hand-rolled Markdown emission, no Markdown library.** The Markdown surface is four constructs: headings, fenced code blocks, links, and bullet lists. All f-string work. Rejected: a Markdown emitter library (a dependency carrying constructs we do not use, and the mainstream Markdown packages are parsers, the wrong direction for emission). Hand-rolling also keeps byte-level determinism under direct control, which `--check` (0003) depends on.
- **Signatures as code lines.** Each member renders as a fenced Python signature line followed by its docstring block; undocumented members render as bare signature lines.
- **Byte-determinism.** The same models and config always produce byte-identical files. Required for the `--check` mode (0003) to be meaningful.
- **The output directory is tool-owned.** Generation deletes `.md` files under the output directory that the current run does not produce. Rejected: additive writes only (a renamed module would leave a stale file forever).

## Testing strategy

### Rendering: normal operation

- When a module model is rendered, its doc file states the source path, renders the module docstring per truncation config, then the outline in model order.
- When a member is public, or is `__init__` or `__new__`, it renders; when it is underscore-prefixed and the private flag is off, it is omitted.
- When a docstring kind has truncation on, only its first line renders; other kinds render in full.
- When a directory contains doc files or child indexes, its `index.md` lists modules and subdirectories by path, each entry linking to the doc file and the source file.
- When the same models are rendered twice, the outputs are byte-identical.

### Rendering: edge cases

- When a docstring contains Markdown or backticks, it passes through unchanged inside its block.
- When a truncated first line is empty or whitespace, the member renders as if undocumented.

### Output: normal operation

- When generation completes, the output directory contains exactly the generated doc files and indexes.
- When a previously generated file is no longer produced, generation deletes it from the output directory.
- When the output directory does not exist, it is created.

### Output: failure handling

- When the output directory cannot be created or written (permissions), generation fails with the offending path.

### Library API (IPO) [proposed]

- Inputs: module models plus presentation config (output path, include-private, per-kind truncation).
- Process: render models to file texts; write the output directory; prune stale files.
- Outputs: the rendered file set; a generation report of written and deleted paths.
- Failure outputs: an exception carrying the offending path for filesystem problems.

## Out of scope

- Collection: 0001. Config resolution, CLI, and check mode: 0003.
- Artifacts other than Markdown (JSON, HTML) and convention parsing: future specs if wanted.

## Related documents

- Requires `0001-docstring-collection.md`; followed by `0003-delivery-surface.md`.
