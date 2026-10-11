# repotoc

repotoc generates a Markdown table of contents for a Python repository. It statically collects the signature and docstring of every module, class, and function, then renders a folder of Markdown files that mirrors the source tree. The artifact lets a person or an AI agent survey a codebase without scanning, grepping, or loading source files.

Collection reads source with the stdlib `ast` module. Nothing is imported or executed, so the tool is safe to run on any repository. Rendering is deterministic: the same source and settings always produce byte-identical output.

## The artifact

For each Python module, one doc file at the mirrored path: `src/foo/bar.py` produces `<output>/src/foo/bar.md`. A doc file states the source path as a heading, then outlines each member as a section with its docstring and, optionally, its signature as a fenced Python block. Each directory also gets a `repotoc_toc.md` that lists its contents as a nested, linked outline with one-line summaries. The root index is the entry point for scanning the whole repository.

The default output directory is `docs/repotoc`. The directory is owned by the tool: regeneration writes the current file set and deletes `.md` files it no longer produces.

## For AI agents

The artifact is written for agents, so a consuming repository can point its agents at it with a short directive in its `AGENTS.md` (or equivalent instruction file):

```markdown
Consult the table of contents under `docs/repotoc/` before searching or
reading source files: start at `docs/repotoc/repotoc_toc.md`, the linked
outline of the whole repository with one-line summaries, and open a module's
doc file to survey its API before reading the source itself.
```

Adjust the paths when the output directory is configured differently.

## Usage

Install with uv, then run the `repotoc` command from the repository root:

```
uv run repotoc
```

Zero-argument invocation runs entirely from config, which is the intended pre-commit form.

## Pre-commit

The package ships a pre-commit hook definition (`.pre-commit-hooks.yaml`). Consumers reference this repository at a pinned `rev` and select the `repotoc` hook. The hook runs in regenerate mode, driven by the consuming project's config, and triggers when tracked `*.py` files or `pyproject.toml` change. The package requires Python >= 3.11.

## Configuration

Every flag has a `[tool.repotoc]` key in `pyproject.toml`; CLI arguments override the config file, which overrides the defaults.

```toml
[tool.repotoc]
sources = ["src", "tests"]
output = "docs/repotoc"
```

| Key | CLI flag | Default | Meaning |
| --- | --- | --- | --- |
| `sources` | positional | none | Source root directories to scan |
| `output` | `-o, --output` | `docs/repotoc` | Output directory for the artifact |
| `exclude` | `--exclude` | none | Extra directory names to skip |
| `file_member_depth` | `--file-member-depth` | unlimited | Outline depth in doc files |
| `file_include_privates` | `--file-include-privates` | off | Render underscore-prefixed members |
| `file_include_signatures` | `--file-include-signatures` | on | Render member signatures (decorators and definition line) |
| `toc_max_depths` | `--toc-max-depths` | `6` | Per-level list depths for indexes |

`toc_max_depths` takes a bare integer or a list of integers: position 1 sets the root index's depth, each later position sets the next level's, and the last position applies to every deeper level.

Exit codes: 0 on success and on fresh checks; 1 on stale checks; 2 on usage, config, filesystem, and parse errors.

## Staleness checks

`--check` compares the rendered artifact against the output directory without writing anything. It exits 1 and lists the offending files when any are missing, differing, or extra. This mirrors the `ruff format --check` pattern and pairs with a pre-commit hook or CI gate.

## License

MIT. See [LICENSE](LICENSE).

## Development

Development runs in a docker container through just recipes, and commits are gated by `just fix` and `just check`. See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, recipes, and the commit workflow.
