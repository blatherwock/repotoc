# Implementation plan: pre-commit self-consumption

## Overview

Implements `docs/planning/specs/0004-self-consumption.md`: wire this repository to consume its own shipped pre-commit hook. Four additions, no package code changes: a `[tool.repotoc]` section in `pyproject.toml`, a `.pre-commit-config.yaml` referencing the repository by local path, the generated initial artifact under `docs/repotoc`, and `justfile` updates (freshness gate in `check`, a `hooks` recipe for host setup).

## Task list

### Phase 1: Config and artifact

- [x] Task 1: Add the `[tool.repotoc]` section to `pyproject.toml`
  - Set `sources = ["src", "tests"]` and no other keys; defaults (output `docs/repotoc`, presentation settings) carry over. Verify with `uv run repotoc`, which must generate entirely from config.
  - Satisfies spec scenarios: hook normal operation (config-driven regeneration); freshness gate (config for `--check`).
- [x] Task 2: Generate the initial artifact
  - Run `uv run repotoc` and inspect `docs/repotoc`; it must cover `src` and `tests` and be byte-stable on a rerun. The artifact files are left for the user to commit with the change (per the repo rule, we never commit); tracking is what makes hook enforcement work.
  - Satisfies spec scenarios: the tracked-artifact decision (initial commit).
- [x] Task 3: Add `.pre-commit-config.yaml`
  - One entry: `repo: ./`, `rev: HEAD`, hook `id: repotoc`, no overrides; the shipped `.pre-commit-hooks.yaml` supplies entry, language, file filter, and `pass_filenames`. Include a one-line comment that the mutable-reference warning is expected and benign. Amended during host setup: pinned `default_language_version: python: python3.14` because pre-commit resolves the default interpreter by PATH lookup (it landed on the host's 3.9, below the package floor) and never reads `.python-version`; host setup runs `uv python install 3.14` to link the interpreter. Verified: the hook env builds as `py_env-python3.14` on 3.14.8.
  - Satisfies spec scenarios: hook normal operation, failure handling, edge cases.

### Checkpoint: config and artifact

- [x] `uv run repotoc --check` exits 0 (fresh artifact, src and tests covered).
- [x] `just check` passes (no regressions from the pyproject edit).

### Phase 2: Tooling

- [x] Task 4: Add the freshness gate to `just check`
  - Append `uv run repotoc --check` to the `check` recipe so the definition-of-done gate matches the host hook's outcome. Amended during review: `just fix` gained the write counterpart, `uv run repotoc`, which clears every staleness class the gate reports (verified for differing and extra files).
  - Satisfies spec scenarios: freshness gate (all three).
- [x] Task 5: Add the `hooks` recipe
  - A host-only recipe (guard with `host_only_error`; the container mounts `.git` read-only) running `uvx pre-commit install`.
  - Satisfies spec scenarios: host setup requirement.

### Checkpoint: definition of done

- [x] `just check` passes end to end, including the freshness gate.
- [x] `just test` passes (no package code touched; confirms the gate did not break the container recipes).
- [x] Staleness probe: a temporary docstring edit makes the gate exit 1 naming the differing file; restoring it returns exit 0.
- [ ] Host verification, run by the user: `uv python install 3.14`, `uv tool install pre-commit` (or run via uvx), `just hooks`, then stage a docstring edit and confirm the hook fails with "files were modified by this hook"; re-stage and confirm the commit passes.

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
