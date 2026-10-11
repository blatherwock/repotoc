# RepoTOC

[![tests](https://github.com/blatherwock/repotoc/actions/workflows/tests.yml/badge.svg)](https://github.com/blatherwock/repotoc/actions/workflows/tests.yml)

RepoTOC generates a Markdown table of contents for a Python repository. It collects the signature and docstring of every module, class, and function, then renders them as a folder of Markdown files that mirrors the source tree. A person or an AI agent can read this artifact to survey a codebase without opening its source files.

RepoTOC parses source with the standard library `ast` module and never imports or executes it, so it is safe to run on any repository. Output is deterministic: the same source and settings always produce byte-identical files.

## Output

Each Python module gets one doc file at its mirrored path: `src/foo/bar.py` produces `<output>/src/foo/bar.md`. A doc file opens with the source path as its heading, followed by the module docstring. Each member then gets a section with its docstring and, optionally, its signature in a fenced Python block.

Each directory also gets a `repotoc_toc.md` index: a nested, linked outline of its contents, with each entry summarized by the first line of its docstring. The root index is the entry point to the whole repository.

The tool owns the output directory (`docs/repotoc` by default). Regeneration writes the current file set and deletes any `.md` files it no longer produces. Files with other suffixes stay.

## Installation

RepoTOC requires Python 3.11 or later. Add it to a project as a development dependency:

```
uv add --dev git+https://github.com/blatherwock/repotoc
```

## Usage

Run `repotoc` from the repository root:

```
uv run repotoc
```

With no arguments, RepoTOC reads every setting from `pyproject.toml` (see [Configuration](#configuration)). The pre-commit hook runs this form.

To verify the artifact without writing, pass `--check`. It prints each stale file as `missing:`, `differing:`, or `extra:` and exits 1 when it finds any. Like `ruff format --check`, it suits a CI gate.

Exit codes:

- 0: success, or a check found the artifact current
- 1: a check found stale files
- 2: a usage, config, filesystem, or parse error

## Configuration

Settings live in the `[tool.repotoc]` section of `pyproject.toml`:

```toml
[tool.repotoc]
sources = ["src", "tests"]
output = "docs/repotoc"
```

Each key has a matching CLI flag. Flags override the config file, and the config file overrides the defaults. A list given on the command line replaces the configured list instead of extending it.

| Key | CLI flag | Default | Meaning |
| --- | --- | --- | --- |
| `sources` | positional | none (required) | Source root directories to scan |
| `output` | `-o`, `--output` | `docs/repotoc` | Output directory for the artifact |
| `exclude` | `--exclude` | none | Extra directory names to skip |
| `file_member_depth` | `--file-member-depth` | unlimited | Outline depth in doc files |
| `file_include_privates` | `--[no-]file-include-privates` | off | Render underscore-prefixed members |
| `file_include_signatures` | `--[no-]file-include-signatures` | on | Render member signatures (decorators and definition line) |
| `toc_max_depths` | `--toc-max-depths` | `6` | Per-level list depths for indexes |

RepoTOC always skips hidden directories and `__pycache__`, `venv`, `build`, `dist`, and `node_modules`; `exclude` adds names to this list.

`toc_max_depths` takes an integer or a list of integers (space-separated on the command line). The first value sets the depth of the root index, each later value sets the depth one directory level down, and the last value applies to every deeper level.

## Pre-commit

This repository ships a pre-commit hook. Reference it at a pinned `rev` in `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/blatherwock/repotoc
    rev: <commit SHA or tag>
    hooks:
      - id: repotoc
```

The hook regenerates the artifact from the project's config whenever a commit changes a `.py` file or `pyproject.toml`. When the artifact changes, pre-commit fails the commit; stage the updated files and commit again. If pre-commit's default Python is older than 3.11, set `language_version` on the hook.

## Using the artifact with AI agents

To point an agent at the artifact, add a short directive to the repository's `AGENTS.md` or equivalent instruction file:

```markdown
Consult the table of contents under `docs/repotoc/` before searching or
reading source files: start at `docs/repotoc/repotoc_toc.md`, the linked
outline of the whole repository with one-line summaries, and open a module's
doc file to survey its API before reading the source itself.
```

Adjust the paths if you configure a different output directory.

## Development

Development runs through just recipes in a docker container, and `just fix` and `just check` gate every commit. See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, recipes, and the commit workflow.

## License

MIT. See [LICENSE](LICENSE).
