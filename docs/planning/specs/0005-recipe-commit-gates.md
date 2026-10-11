# Spec: recipe commit gates

Supersedes the pre-commit hook wiring of `0004-self-consumption.md`; the freshness gate and `just fix` recipes of 0004 remain in force.

## Objective

Commit gates run the repository's own recipes instead of a self-referential pre-commit install: `just fix` then `just check`, as repo-local pre-commit hooks. The gates always exercise the working tree, so changed repotoc behavior applies before it is committed. The shipped `.pre-commit-hooks.yaml` is unchanged; consumers are unaffected, and this repository no longer dogfoods the shipped hook.

## Requirements

`.pre-commit-config.yaml` holds exactly two repo-local `language: system` hooks, in order: `just fix` then `just check`, both `pass_filenames: false` and unfiltered, so every commit with staged files runs both. No pre-commit-managed python environment remains: the `repo: ./` entry and the `default_language_version` pin are gone, and with them the host's `uv python install` step; tools and interpreter come from the recipes' environment.

When `just fix` changes files, pre-commit fails the commit with "files were modified by this hook" and leaves the fixes unstaged; re-staging passes. When `just check` fails (type errors, unfixable lint, stale docs), the commit is blocked with the recipe's output.

The justfile's `docker_run` is non-interactive, so the gates run from pre-commit's no-tty context; recipes that need interactivity (`shell`, `pi`) add `-it` themselves.

Host setup is `just` and docker with the built image, plus uvx-installed pre-commit and `just hooks`.

## Decisions

- **Recipe gates replace self-consumption.** One definition of done: the commit gates are the recipes run by hand. The `repo: ./` wiring made this repository consume its shipped hook, but a self-reference cannot provide the one property development needs, running changed behavior before it is committed, and it dragged in mutable-rev machinery, interpreter pinning, and a pre-commit-managed duplicate of the uv environment. Rejected: keeping `repo: ./` (its working-tree pickup is real, but the rest of the machinery remains).
- **The gates are unfiltered.** Every commit with staged files runs both hooks, so the commit gate matches the definition of done exactly; a commit changing only recipes or planning docs is still gated. The docker startup cost per commit is the accepted price. Rejected: filtering to `(\.py$|^pyproject\.toml$)` (faster, but commits the gate should catch would slip through).
- **Two hooks, fix before check.** `just fix` applies format, safe lint fixes, and doc regeneration; `just check` then verifies everything, including what fix cannot fix. pre-commit runs both even when the first fails, so a failing run reports all findings.
- **`docker_run` drops `-it`.** pre-commit supplies no tty, and docker fails on `-it` without one; interactivity moves to the recipes that need it.

## Testing strategy

Verified by command in the container (where the recipes run via uv directly); the host docker path is verified by the first gated commit.

### Gates: normal operation

- When a commit stages any files, both hooks run; with a clean, fresh tree both pass.
- When the staged changes need fixes, `just fix` applies them, fails the commit with "files were modified by this hook", and leaves the fixes unstaged; re-staging passes.

### Gates: failure handling

- When an unfixable lint violation, type error, or stale doc is staged, `just check` fails and blocks the commit with the recipe's output.
- When the docker image is missing on the host, `_require-image` fails the hook with the build hint.

### Gates: edge cases

- When repotoc's own behavior changes in the working tree, the gates use the changed behavior, committed or not.
- The fix hook runs against the whole tree (the recipes are repo-wide), matching `just fix` run by hand; pre-commit's stash dance keeps unstaged work out of the run.

## Out of scope

- Running the test suite at commit time; `just test` stays the test gate.
- Any consumer-facing surface; `.pre-commit-hooks.yaml` is untouched.

## Related documents

- `docs/planning/specs/0004-self-consumption.md` — the freshness gate and fix recipe this change reuses; its hook wiring is superseded here.
