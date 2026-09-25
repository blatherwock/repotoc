# Spec: docstring collection

## Objective

The collection layer turns source roots into module models: a faithful, presentation-free representation of every module, class, and function definition with its signature and docstring. This is the first of three specs for repodoc; artifact rendering (0002) and the delivery surface (0003) build on these models.

## Requirements

Collection reads Python source files with the stdlib `ast` module. Nothing is imported or executed. Models preserve the source order of definitions, and the model list is ordered by path, so downstream rendering is deterministic.

Collection covers all `*.py` files under the given roots, tests included. The walk skips hidden directories, `__pycache__`, `venv`, `.venv`, `build`, `dist`, and `node_modules`. A file reachable through two roots is collected once.

Models are unfiltered: public and private members are all present, docstrings raw. Presentation (visibility filtering, truncation) belongs to rendering (0002).

## Decisions

- **Static AST parsing.** Collection uses `ast` over source files; nothing is imported or executed. Rejected: import-time introspection (executing arbitrary repo code is unsafe, slow, and fails on missing dependencies). Python source only, for now.
- **Stdlib `ast`, no parsing library.** `ast.parse` plus a small level-aware visitor covers collection, including signature reconstruction from the AST nodes. Rejected: third-party source parsers and docstring collectors (they add a dependency for nothing stdlib lacks here).
- **Full outline, not docstrings alone.** Every module, class, and function is collected with its full signature (name, parameters, return annotation when present); the docstring is optional. Knowing an undocumented object exists is itself information; hiding it would defeat the table-of-contents purpose. Rejected: collecting only documented objects.
- **Skip function-local definitions and attribute docstrings.** Function-local definitions are closures created at call time, not part of a module's static structure. Class bodies are collected fully, including nested classes. String literals after assignments are ignored.
- **Models are faithful and unfiltered.** Public and private members all appear in models. Rejected: filtering at collection (makes collect config-dependent and withholds information the renderer may be asked to show).
- **Source order within a module, path order across modules.** Members keep the order of their appearance in the source; the model list is ordered by path. Rejected: alphabetical ordering (breaks the natural reading order of a module and makes diffing against the source harder).
- **Collection scope.** All `*.py` files under the roots, tests included. Rejected: excluding tests (agents navigate test code too) and collecting only packaged code (roots are the caller's choice).

## Testing strategy

### Collection: normal operation

- When a root is scanned, every `*.py` file under it yields one module model, and the models are ordered by path.
- When a module has a docstring, it is attached to the module model; when not, the module model exists without one.
- When a module defines top-level functions and classes, each yields a model with name, full signature, and docstring when present, in source order.
- When a class body defines methods and nested classes, each yields a model under the class, in source order, with signatures.
- When a member is underscore-prefixed, it appears in the model.

### Collection: failure handling

- When a source file cannot be parsed (syntax error), collection raises a parse error carrying the file path and message; no partial models are returned for that file.
- When a root does not exist, collection raises an error naming the root.

### Collection: edge cases

- When a file is empty or contains no definitions, it yields a module model with no members.
- When a file is reachable through two overlapping roots, it is collected once.
- When a skip-listed directory is encountered, it is skipped entirely.
- When a definition is function-local, it is skipped; when a class is nested in a class, it is collected.
- When a string literal follows an assignment (attribute docstring style), it is ignored.

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
