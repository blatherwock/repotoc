# Contributing to repotoc

## Setup

Development runs through just recipes in a docker container. The host needs `just`, docker, and uvx-installed pre-commit.

```
just build    # Build the container image
just hooks    # Install the git hooks
```

Every recipe then runs inside the container; no local Python or uv is needed. To explore interactively, `just shell` opens a bash prompt in it.

## Recipes

```
just test    # Run the test suite on the dev and floor Pythons
just check   # Format, lint, types, and artifact freshness (read-only)
just fix     # Apply fixes and regenerate the artifact
```

`just check` is the definition-of-done gate. It verifies formatting (ruff), lint (ruff), types (ty), and artifact freshness (`repotoc --check`); it writes nothing. `just fix` is its write counterpart: it formats, applies safe lint fixes, and regenerates the Markdown artifact.

The test suite runs twice: once on the dev Python with the coverage gate, once on the floor Python (3.11) pass-only, because version-guarded branches cannot be covered there. The project pins 100% line and branch coverage, enforced on every test run.

## Commit gates

Commits are gated by two repo-local pre-commit hooks: `just fix` then `just check`. The gates always exercise the working tree, so changed behavior applies before it is committed.

When `just fix` changes files, pre-commit fails the commit and leaves the fixes unstaged; re-staging passes. When `just check` fails (type errors, unfixable lint, stale docs), the commit is blocked with the recipe's output.

## Design documents

`docs/planning/` holds the design record: the specs describe collection, rendering, and the delivery surface, and the plans record the implementation steps. A spec records what was built at the time of building; to learn the current behavior, read the source.
