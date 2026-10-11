# Implementation plan: delivery surface

## Overview

Implements `docs/planning/specs/0003-delivery-surface.md`: config resolution from `[tool.repodoc]` with CLI-over-pyproject precedence, the `repodoc` CLI (generate plus `--check`, exit codes 0/1/2), the console entry point, packaging with the 3.11 floor, and the pre-commit hook definition. Consumes `collect` (plan 0001) and `generate` (plan 0002); extends `collect` with an exclusions parameter so the CLI flag and its config key reach collection.

## Task list

### Phase 1: Config resolution

- [x] Task 1: Config model and pyproject loading
  - Add `config.py` holding the full config dataclass (sources, output, truncation flags, include-private, excluded directories) and `load_config(path)` reading `[tool.repodoc]` with stdlib `tomllib`. Coerce `toc_max_depths` from an int or a list of ints to the tuple `RenderConfig` (0002) validates. Type validation errors name the offending key; a missing file or a missing section yields defaults.
  - Satisfies spec scenarios: CLI edge cases (no `pyproject.toml`, no `[tool.repodoc]`); CLI failure handling (invalid TOML, wrong type naming the key).
- [x] Task 2: Precedence and sources semantics
  - Resolve the effective config: defaults, then pyproject, then CLI args; the higher layer wins. CLI positional sources replace config sources, they do not merge. Expose the merge so `cli.py` and tests share it.
  - Satisfies spec scenarios: CLI normal operation (CLI value wins, zero-argument run from config); CLI edge cases (sources replace).
- [x] Task 3: Python floor flip
  - Change `requires-python` to `>=3.11` and regenerate `uv.lock`; confirm the dev environment still runs 3.14.
  - Implementation note: the flip surfaced two 3.12-only assumptions. `signatures.py` read `ast` `type_params` unconditionally and now guards it with a version check; a `.python-version` pin (copied by the Dockerfile) holds development on 3.14. The test suite was verified green on both 3.14 and 3.11.
  - Satisfies spec scenarios: enforces the Python-floor decision.

### Checkpoint: Config

- [x] Config scenario tests green; `uv lock` consistent; `just check` clean; 100% coverage held.

### Phase 2: CLI

- [x] Task 4: Collection exclusions
  - Extend `collect` (0001) with an `exclude` parameter taking extra excluded directory names, merged with the built-in skip list at walk time; the parameter defaults to empty, keeping the existing calls compatible. Cover the merge and the walk-time skipping with unit tests.
  - Satisfies spec scenarios: CLI (IPO) inputs (extra excluded directory names reach collection).
- [x] Task 5: Argument parser and command wiring
  - Add `cli.py` with argparse mapping every flag to a config key: positional sources, `-o/--output` (default `docs/repodoc`), `--check`, per-kind truncation flags, `--include-private`, extra excluded directories. Wire the resolved config through collect, render, and generate. Structure `main()` for in-process testing.
  - Satisfies spec scenarios: CLI (IPO) inputs and process; zero-argument run.
- [x] Task 6: Check mode and exit codes
  - `--check` renders in memory and compares against the output directory: missing, differing, and extra `.md` files are stale; list them and exit 1; fresh exits 0. Usage, config, filesystem, and parse errors exit 2 with messages on stderr. Success exits 0.
  - Satisfies spec scenarios: CLI normal operation (`--check` outcomes); CLI failure handling (no sources, config errors, mapped exceptions); CLI (IPO) outputs and failure outputs.
- [x] Task 7: Entry point and build
  - Add the `repodoc` console script entry point; `uv build` produces a wheel; install into a scratch venv and smoke-run a generation.
  - Satisfies spec scenarios: Packaging (IPO).

### Checkpoint: CLI

- [x] CLI scenario tests green with exit codes asserted in-process; the wheel builds and installs; the smoke run regenerates a scratch artifact folder; `just test` and `just check` clean at 100% coverage.

### Phase 3: Pre-commit

- [x] Task 8: Hook definition and end-to-end
  - Add `.pre-commit-hooks.yaml` defining the `repodoc` hook: `entry: repodoc`, `language: python`, regenerate mode, config-driven, no filenames passed, running when tracked `*.py` files or `pyproject.toml` change. Verify end to end in a scratch project: wire the hook from a scratch git clone of this repo, confirm a commit regenerates the folder and `--check` flags staleness.
  - Satisfies spec scenarios: enforces the pre-commit decision.

### Checkpoint: Delivery

- [x] Scratch-project end-to-end passes; `just test` and `just check` clean at 100% coverage.

## Risks and mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Pre-commit's hook environment ships a Python below the 3.11 floor | Med | The hook definition states the floor; consumers pin `language_version` when their system Python is older |
| Subprocess CLI tests erode coverage accounting | Low | Assert exit codes in-process via `SystemExit`; keep subprocess use to a few smoke tests |
| Argparse usage errors already exit 2 | Low | Aligns with the exit scheme; no extra mapping |

## Open questions

- None open. The hook entry resolved to `entry: repodoc` with `language: python`: pre-commit installs this repo at the consumer's pinned `rev` into its own environment, so consumers reference us once and need no tooling beyond pre-commit. Recorded in the spec's hook decision; `uv run repodoc` with `language: system` and a bare-PATH entry were considered and rejected.

## Related documents

- Implements `docs/planning/specs/0003-delivery-surface.md`
- Requires plans `0001-docstring-collection.md` and `0002-artifact-rendering.md`