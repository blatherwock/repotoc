# Implementation plan: docstring collection

## Overview

Implements `docs/planning/specs/0001-docstring-collection.md`: the collection layer turns source roots into module models via static AST parsing. This plan also lays the foundations later plans depend on: the `src/repodoc` package skeleton, the ruff AST-boundary enforcement, and the coverage gate. No runtime dependencies.

## Task list

### Phase 1: Foundations

- [x] Task 1: Package skeleton and gates
  - Add the uv_build build backend and package config to `pyproject.toml`; create `src/repodoc/__init__.py`, `models.py`, and `collect.py`. Add `pytest-cov` and `coverage` to the dev group; configure `[tool.coverage.run]` (branch on, source `src/repodoc`) and `[tool.coverage.report]` (fail under 100, show missing); set pytest `addopts` so every pytest run enforces the gate. Add a smoke test importing the package so the gate has something to measure.
  - Satisfies spec scenarios: enables all; enforces the coverage-gate and build-backend decisions.
- [x] Task 2: AST boundary enforcement
  - Add ruff TID251 `banned-api` banning `ast`, with per-file exceptions for `src/repodoc/collect.py` and `src/repodoc/signatures.py`. Verify positively (clean gate) and negatively (a temporary `import ast` in `models.py` must fail the gate, then revert).
  - Satisfies spec scenarios: enforces the "Models are resolved dataclasses, not AST nodes" decision.

### Checkpoint: Foundations

- [x] `just check` passes; `just test` runs green at 100% coverage; `uv run python -c "import repodoc"` succeeds.

### Phase 2: Models and collector

- [x] Task 3: Model dataclasses
  - Implement frozen dataclasses in `models.py` per the spec model shape: `Module(source_path, docstring, members)`, `Class(name, signature, docstring, decorators, members)`, `Function(name, signature, docstring, decorators)`. Plain strings and lists only; no AST nodes.
  - Satisfies spec scenarios: model shape requirement; foundation for all collection scenarios.
- [x] Task 4: Signature reconstruction
  - Build the signature string for `def`, `async def`, and `class` definitions in `src/repodoc/signatures.py`: decorators extracted in source order as written expressions, signature as the normalized source form of the definition line (prefer `ast.unparse`; fall back to manual reconstruction from the argument, base, and type-parameter nodes if the unparsed form is malformed). Cover posonly, kwonly, vararg, kwarg, defaults, annotations, return annotations, bases, keywords such as `metaclass`, and PEP 695 type parameters.
  - Satisfies spec scenarios: Collection normal operation (signatures, decorators); Collection edge cases (stacked decorators, decorator arguments).
- [x] Task 5: Collection walker
  - Walk the roots with `pathlib`, apply the skip list (hidden directories, `__pycache__`, `venv`, `.venv`, `build`, `dist`, `node_modules`), dedupe files reachable through overlapping roots, order results by natural path order (digit runs compared numerically). Parse each file with `ast.parse`; module docstring via `ast.get_docstring`; visit module-level and class-level `FunctionDef`, `AsyncFunctionDef`, and `ClassDef` in source order; never descend into function bodies; ignore attribute-style string literals. Raise a parse error carrying path and message on syntax errors; raise an error naming a missing root; the error types live in `src/repodoc/errors.py`. Public API: `collect(roots)`.
  - Satisfies spec scenarios: Collection normal operation; Collection failure handling; Collection edge cases; Library API (IPO).

### Checkpoint: Collector complete

- [x] `just test` green at 100% line and branch coverage across all collection scenarios; `just check` clean.

## Risks and mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| `ast.unparse` yields odd or multi-line signature forms | Med | Lock expected signature strings in tests; fall back to manual reconstruction; signatures are data, so the fallback is contained |
| Ruff per-file-ignores pattern misses the real file | Low | Negative verification in Task 2: a deliberate violation must fail the gate |
| 100% branch coverage demands exhaustive walker fixtures | Med | Spec edge-case lists map one to one onto test fixtures |

## Related documents

- Implements `docs/planning/specs/0001-docstring-collection.md`
- Followed by `0002-artifact-rendering.md` and `0003-delivery-surface.md` (plans)