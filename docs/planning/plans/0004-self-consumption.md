# Implementation plan: pre-commit self-consumption

## Overview

Implements `docs/planning/specs/0004-self-consumption.md`: wire the repository to consume its own shipped pre-commit hook. No package code changes: a `[tool.repotoc]` section in `pyproject.toml`, a `.pre-commit-config.yaml` that consumes the shipped hook definition and runs the repo's other checks as repo-local hooks, the generated initial artifact under `docs/repotoc`, and `justfile` updates (freshness gate in `check`, doc regeneration in `fix`, and a `hooks` recipe for host setup).

## Task list

### Phase 1: Config and artifact

- [x] Task 1: Add the `[tool.repotoc]` section to `pyproject.toml`
  - Set `sources = ["src", "tests"]` and no other keys; defaults (output `docs/repotoc`, presentation settings) carry over. Verify with `uv run repotoc`, which must generate entirely from config.
  - Satisfies spec scenarios: hook normal operation (config-driven regeneration); freshness gate (config for `--check`).
- [x] Task 2: Generate the initial artifact
  - Run `uv run repotoc` and inspect `docs/repotoc`; it must cover `src` and `tests` and be byte-stable on a rerun. The artifact files are left for the user to commit with the change (per the repo rule, we never commit); tracking is what makes hook enforcement work.
  - Satisfies spec scenarios: the tracked-artifact decision (initial commit).
- [x] Task 3: Add `.pre-commit-config.yaml`
  - A `repo: ./` entry with `rev: HEAD` and hook `id: repotoc`, no overrides: pre-commit installs this repository from its own path and consumes the shipped `.pre-commit-hooks.yaml` verbatim (entry, language, file filter, `pass_filenames`). Pin `default_language_version: python: python3.14`, since pre-commit resolves the default interpreter by PATH lookup and never reads `.python-version`; hosts link the pinned interpreter with `uv python install 3.14`. Before the doc hook, repo-local `language: system` hooks run `uv run ruff format`, `uv run ruff check --fix`, and `uv run ty check`, with the tool versions from `uv.lock`; the ruff hooks fix staged violations and pre-commit leaves the fixes unstaged behind a "files were modified by this hook" failure. A comment records that the mutable-reference warning is expected. Verified in the container: the hook env builds as `py_env-python3.14`, planted violations are fixed and left unstaged, and unsafe fixes (F401 in `__init__.py`) block without rewriting.
  - Satisfies spec scenarios: hook normal operation, failure handling, edge cases.

### Checkpoint: config and artifact

- [x] `uv run repotoc --check` exits 0 (fresh artifact, src and tests covered).
- [x] `just check` passes (no regressions from the pyproject edit).

### Phase 2: Tooling

- [x] Task 4: Add freshness handling to `just check` and `just fix`
  - `just check` ends with `uv run repotoc --check`, so the definition-of-done gate matches the host hook's outcome; `just fix` ends with `uv run repotoc`, the gate's write counterpart, clearing every staleness class the gate reports (differing, extra, missing).
  - Satisfies spec scenarios: freshness gate (all three).
- [x] Task 5: Add the `hooks` recipe
  - A host-only recipe (guard with `host_only_error`; the container mounts `.git` read-only) running `uvx pre-commit install`.
  - Satisfies spec scenarios: host setup requirement.

### Checkpoint: definition of done

- [x] `just check` passes end to end, including the freshness gate.
- [x] `just test` passes (no package code touched; confirms the gate did not break the container recipes).
- [x] Staleness probe: a temporary docstring edit makes the gate exit 1 naming the differing file; restoring it returns exit 0.
- [x] Host verification: the initial artifact commit on the host exercised the doc hook and regeneration worked. The repo-local ruff/ty hooks were added after that commit, so their first host run is the next commit.

## Risks and mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Host python older than the package floor 3.11 for the hook env | Med | Pinned `default_language_version: python: python3.14` in `.pre-commit-config.yaml`; hosts link the interpreter with `uv python install 3.14` |
| Docs-only commits can hand-edit the artifact without the hook running | Low | The `just check` gate reports the file as stale |
| pre-commit's mutable-reference warning confuses contributors | Low | The config comment states it is expected |

## Open questions

- None.

## Related documents

- `docs/planning/specs/0004-self-consumption.md` — the spec this plan implements.
