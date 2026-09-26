# Spec: docstring collection

## Objective

The collection layer turns source roots into module models: a faithful, presentation-free representation of every module, class, and function definition with its signature and docstring. This is the first of three specs for repodoc; artifact rendering (0002) and the delivery surface (0003) build on these models.

## Requirements

Collection reads Python source files with the stdlib `ast` module. Nothing is imported or executed. Models preserve the source order of definitions, and the model list is ordered by path, so downstream rendering is deterministic.

Collection covers all `*.py` files under the given roots, tests included. The walk skips hidden directories, `__pycache__`, `venv`, `.venv`, `build`, `dist`, and `node_modules`. A file reachable through two roots is collected once.

Models are unfiltered: public and private members are all present, docstrings raw. Presentation (visibility filtering, truncation) belongs to rendering (0002).

The model shape [proposed]:

```
Module(source_path, docstring, members)
Class(name, signature, docstring, decorators, members)
Function(name, signature, docstring, decorators)
```

`signature` is the normalized source form of the definition line, `decorators` the decorator expressions as written, `members` ordered by source appearance. Models carry no AST nodes: rendering (0002) depends only on these fields.

## Decisions

- **Static AST parsing.** Collection uses `ast` over source files; nothing is imported or executed. Rejected: import-time introspection (executing arbitrary repo code is unsafe, slow, and fails on missing dependencies). Python source only, for now.
- **Stdlib `ast`, no parsing library.** `ast.parse` plus a small level-aware visitor covers collection, including signature reconstruction from the AST nodes. Rejected: third-party source parsers and docstring collectors (they add a dependency for nothing stdlib lacks here).
- **Full outline, not docstrings alone.** Every module, class, and function is collected with its full signature (name, parameters, return annotation when present); the docstring is optional. Knowing an undocumented object exists is itself information; hiding it would defeat the table-of-contents purpose. Rejected: collecting only documented objects.
- **Skip function-local definitions and attribute docstrings.** Function-local definitions are closures created at call time, not part of a module's static structure. Class bodies are collected fully, including nested classes. String literals after assignments are ignored.
- **Models are faithful and unfiltered.** Public and private members all appear in models. Rejected: filtering at collection (makes collect config-dependent and withholds information the renderer may be asked to show).
- **Models are resolved dataclasses, not AST nodes.** Each model is a frozen dataclass holding the signature as a normalized source string, the dedented raw docstring, and ordered member lists. Rejected: passing AST nodes between layers (couples rendering to collection internals and re-opens the walk that collection should close).
- **The AST boundary is enforced by ruff, not a new library.** Ruff's `banned-api` rule (TID251) bans `ast` package-wide with a per-file exception for the collector module; it runs in the existing `check` gate. Rejected: import-linter (registry-verified mature and maintained, but four direct dependencies plus transitive ones to express one rule in a three-module package; becomes worth it once several import contracts exist) and a hand-rolled boundary test (duplicates what ruff already does declaratively).
- **Coverage gate: coverage.py plus pytest-cov at 100% line and branch.** All code paths in the package are exercised by unit tests; the gate enforces 100% line and branch coverage on `src/repodoc` (branch coverage is what "all code paths exercised" means). Enforcement rides pytest itself via `addopts`, so the gate follows every test run, recipe or not. Exclusions stay minimal, such as `TYPE_CHECKING` guards. Rejected: plain coverage.py only (the gate would live solely in the test recipe; raw pytest runs would skip enforcement) and covdefaults (registry-stale, last release March 2023).
- **Build backend: uv_build.** The package needs a PEP 517 backend so `uv sync` installs the project and `import repodoc` works without path manipulation. uv_build is the uv default, has no runtime dependencies, and expects the src layout by default (the package lives at `src/repodoc`). It is still 0.x; we accept that risk because swapping a backend is a two-line change in `pyproject.toml`. Rejected: hatchling (five transitive dependencies and capabilities far beyond a three-module package), flit-core (explicit module configuration needed for the src layout), pdm-backend (tied to the PDM ecosystem the project does not use), and setuptools (the heaviest option; nothing here needs it).
- **Decorators are collected.** Decorator expressions are stored in source order on function and class models. Rejected: dropping them (a `@property` would read as a plain method, and framework decorators often carry API meaning).
- **Source order within a module, path order across modules.** Members keep the order of their appearance in the source; the model list is ordered by path. Rejected: alphabetical ordering (breaks the natural reading order of a module and makes diffing against the source harder).
- **Collection scope.** All `*.py` files under the roots, tests included. Rejected: excluding tests (agents navigate test code too) and collecting only packaged code (roots are the caller's choice).

## Testing strategy

Every behavior below is exercised by unit tests; the coverage gate (Decisions) holds the package at 100% line and branch coverage.

### Collection: normal operation

- When a root is scanned, every `*.py` file under it yields one module model, and the models are ordered by path.
- When a module has a docstring, it is attached to the module model; when not, the module model exists without one.
- When a module defines top-level functions and classes, each yields a model with name, full signature, and docstring when present, in source order.
- When a class body defines methods and nested classes, each yields a model under the class, in source order, with signatures.
- When a member is underscore-prefixed, it appears in the model.
- When a member carries decorators, the decorator expressions are stored on the model in source order.

### Collection: failure handling

- When a source file cannot be parsed (syntax error), collection raises a parse error carrying the file path and message; no partial models are returned for that file.
- When a root does not exist, collection raises an error naming the root.

### Collection: edge cases

- When a file is empty or contains no definitions, it yields a module model with no members.
- When a file is reachable through two overlapping roots, it is collected once.
- When a skip-listed directory is encountered, it is skipped entirely.
- When a definition is function-local, it is skipped; when a class is nested in a class, it is collected.
- When a string literal follows an assignment (attribute docstring style), it is ignored.
- When a member carries stacked decorators or decorators with arguments, each expression is stored verbatim.

### Library API (IPO) [proposed]

- Inputs: source roots as paths; the built-in skip list applies.
- Process: walk the roots, parse each file, build models.
- Outputs: a path-ordered list of module models; each model carries the source path, the module docstring, and ordered member models.
- Failure outputs: a parse-error exception carrying path and message; an error naming a missing root.

## Out of scope

- Visibility filtering and docstring truncation: rendering owns them (0002).
- Incremental collection: every run processes every file under the roots.

## Related documents

- Followed by `0002-artifact-rendering.md` (consumes the models) and `0003-delivery-surface.md` (exposes them through a CLI).
