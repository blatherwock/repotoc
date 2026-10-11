# Implementation plan: recipe commit gates

## Overview

Implements `docs/planning/specs/0005-recipe-commit-gates.md`: replace the self-referential pre-commit wiring with the repository's own recipes as commit gates. Three edits: the justfile makes `docker_run` non-interactive (moving `-it` to the `shell` and `pi` recipes), `.pre-commit-config.yaml` becomes two repo-local hooks (`just fix` then `just check`), and spec 0004 gets a superseded pointer.

## Task list

### Phase 1: Wiring

- [x] Task 1: Make `docker_run` non-interactive in the justfile
  - Drop `-it` from `docker_run`; add `-it` to the `shell` and `pi` recipes, the only ones needing a tty. pre-commit supplies no tty, so the gates cannot run through an `-it` docker run.
  - Satisfies spec scenarios: gates failure handling (missing image), edge cases (no-tty context).
- [x] Task 2: Rewrite `.pre-commit-config.yaml` as two recipe hooks
  - `repo: local` with `just fix` then `just check`, both `language: system`, `pass_filenames: false`, unfiltered so every commit is gated. Remove the `repo: ./` entry and the `default_language_version` pin. Comments state the working-tree property and the shipped hook's consumer-only role.
  - Satisfies spec scenarios: gates normal operation, failure handling.
- [x] Task 3: Add the superseded pointer to spec 0004
  - One line under 0004's title naming 0005 as the successor of its hook wiring.
  - Satisfies spec scenarios: none (record keeping).

### Checkpoint: definition of done

- [x] `uvx pre-commit run --all-files` passes in the container (both hooks run `just` against the uv path).
- [x] Planted violation: `just-fix` fixes and fails with "files were modified by this hook"; the follow-up run passes.
- [x] `just check` and `just test` pass.
- [ ] Host verification: the first gated commit on the host runs both hooks through docker (the no-tty path this container cannot exercise).

## Risks and mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| The no-tty docker change breaks `shell` or `pi` on the host | Med | `-it` restored on exactly those recipes; host verification at the first gated commit |
| Whole-tree docker cost on every commit | Low | Accepted per the unfiltered-gates decision; re-add a filter if it bites |
| Fix hook's whole-tree fixes surprise during partial commits | Low | pre-commit's stash keeps unstaged work out; fixes surface unstaged for review, same as the ruff hooks before |

## Open questions

- None.

## Related documents

- `docs/planning/specs/0005-recipe-commit-gates.md` — the spec this plan implements.
