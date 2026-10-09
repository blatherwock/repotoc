# Spec: delivery surface

## Objective

The delivery surface makes the generator usable from a terminal and a pre-commit hook: a `repodoc` CLI whose every flag has a `[tool.repodoc]` key in `pyproject.toml`, a `--check` mode for staleness detection, and a shipped pre-commit hook definition. The package is installable via uv into other projects. This is the last of three specs for repodoc; it requires collection (0001) and rendering (0002).

## Requirements

Config resolution follows precedence: defaults, then the `[tool.repodoc]` section of the `pyproject.toml` in the current directory, then CLI args; the higher layer wins. CLI positional sources replace config sources, they do not merge. Zero-argument invocation runs entirely from config, which is the intended pre-commit form.

Exit codes: 0 on success and on fresh checks; 1 on stale checks, with the list of offending files; 2 on usage, config, filesystem, and parse errors, with messages on stderr.

## Decisions

- **Library-first with a thin CLI.** The importable API is the real interface; the CLI maps flags onto the same config object. Rejected: CLI only (not composable from other tools) and library only (no one-line regeneration).
- **CLI regenerates by default; `--check` compares.** `--check` writes nothing, exits 1 listing missing, differing, or extra `.md` files in the tool-owned output directory (0002). Mirrors the `ruff format --check` pattern. Rejected: hooks that rewrite files on every run (pre-commit retries on changed files) and no check mode (stale detection would need diffing by hand).
- **Config in `pyproject.toml`.** A `[tool.repodoc]` section parsed with stdlib `tomllib`. Every CLI flag has a config key. Rejected: a separate config file (one more file in every consuming project, no added power).
- **`toc_max_depths` takes an int or a list.** TOML has no tuples, so the key accepts a bare int (coerced to a one-element tuple) or a list of ints, coerced to the tuple `RenderConfig` (0002) validates. Rejected: list-only (the single-depth common case reads cleaner as a bare int) and per-level subsections such as `[tool.repodoc.toc_level1]` (the levels are positional, so a list states them directly, and one key keeps every flag's one-key mapping).
- **Sources replace, not merge.** CLI positional sources override config sources entirely. Merging would make a run's inputs depend on where it is invoked from; replacement is predictable.
- **Ship a pre-commit hook definition.** A `.pre-commit-hooks.yaml` in this repo defines a `repodoc` hook: regenerate mode, config-driven, no filenames passed; it runs when tracked `*.py` files or `pyproject.toml` change [proposed]. Consumers wire it with one line.
- **Python floor 3.11, development on 3.14.** `requires-python = ">=3.11"` so projects on older Pythons can install it; this repo develops on 3.14. `tomllib` availability sets the floor. No runtime dependencies.

## Testing strategy

Every behavior below is exercised by unit tests; the package is held at 100% line and branch coverage by the coverage gate defined in `0001-docstring-collection.md`.

### CLI: normal operation

- When `repodoc <sources...>` runs, the artifact folder is regenerated under the output directory (default `docs/repodoc`).
- When `repodoc --check` runs and the output is fresh, it exits 0; when stale, it exits 1 and lists the offending files.
- When `repodoc` runs with no arguments and config defines sources, it generates from config alone.
- When CLI args and config both set a value, the CLI value wins.

### CLI: failure handling

- When no sources come from CLI or config, the run exits 2 with a usage message.
- When `pyproject.toml` is invalid TOML, or a `[tool.repodoc]` value has the wrong type or a value 0002 validation rejects, the run exits 2 naming the offending key.
- When collection or generation raises, the run exits 2 with the exception's message.

### CLI: edge cases

- When the current directory has no `pyproject.toml`, defaults apply and the run proceeds.
- When `pyproject.toml` exists without `[tool.repodoc]`, defaults apply.
- When config sets sources and the CLI passes sources, only the CLI sources are used.

### CLI (IPO)

- Inputs: positional source paths; `-o/--output`; `--check`; one flag per presentation setting (0002: `file_member_depth`, `file_include_privates`, `file_include_signatures`, `toc_max_depths`); extra excluded directory names. Every flag has a `[tool.repodoc]` key.
- Process: resolve config, collect (0001), render (0002), write or compare.
- Outputs: exit 0 on success or fresh check; exit 1 with a stale file list; the artifact folder written in generate mode.
- Failure outputs: exit 2 with stderr messages for usage, config, filesystem, and parse errors.

### Packaging (IPO) [proposed]

- Inputs: none beyond build metadata in `pyproject.toml`.
- Process: a standard build backend builds the wheel.
- Outputs: an installable package exposing the `repodoc` console script and the importable library.
- Failure outputs: build errors from the backend.

## Out of scope

- Publishing to a package index; consumers install via git or path with uv.
- Hook behavior beyond invoking the CLI (the hook is a thin entry).

## Related documents

- Requires `0001-docstring-collection.md` and `0002-artifact-rendering.md`.
