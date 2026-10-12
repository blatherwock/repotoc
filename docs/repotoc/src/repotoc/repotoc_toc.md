# src/repotoc

> Static docstring and signature collection for Python repositories.

- file: [`cli.py`](cli.md) ([source](../../../../src/repotoc/cli.py)): The `repotoc` command line interface: flags mapped onto the shared config.
- file: [`collect.py`](collect.md) ([source](../../../../src/repotoc/collect.py)): Collection layer: turn source roots into module models via static AST parsing.
- file: [`config.py`](config.md) ([source](../../../../src/repotoc/config.py)): Config resolution: defaults, the `[tool.repotoc]` section, and CLI overlays.
- file: [`errors.py`](errors.md) ([source](../../../../src/repotoc/errors.py)): Error types raised by the config, collection, and generation layers.
- file: [`filters.py`](filters.md) ([source](../../../../src/repotoc/filters.py)): Presentation settings and the visibility filter they drive.
- file: [`generate.py`](generate.md) ([source](../../../../src/repotoc/generate.py)): Generation layer: write and prune the tool-owned artifact output directory.
- file: [`models.py`](models.md) ([source](../../../../src/repotoc/models.py)): Model dataclasses for collected modules, classes, and functions.
- dir: [`render/`](render/repotoc_toc.md) ([source](../../../../src/repotoc/render/__init__.py)): Rendering layer: turn module models into Markdown doc files and indexes.
  - file: [`__init__.py`](render/__init__.md) ([source](../../../../src/repotoc/render/__init__.py)): Rendering layer: turn module models into Markdown doc files and indexes.
  - file: [`file_renderer.py`](render/file_renderer.md) ([source](../../../../src/repotoc/render/file_renderer.py)): Doc file rendering: module models into Markdown doc files.
  - file: [`index_renderer.py`](render/index_renderer.md) ([source](../../../../src/repotoc/render/index_renderer.py)): Index rendering: directory contents into Markdown index files.
  - file: [`markdown.py`](render/markdown.md) ([source](../../../../src/repotoc/render/markdown.py)): Markdown emission helpers: headings, blockquotes, rules, link and list lines.
  - file: [`paths.py`](render/paths.md) ([source](../../../../src/repotoc/render/paths.py)): Doc paths, source links, and directory chains for the artifact layout.
- file: [`signatures.py`](signatures.md) ([source](../../../../src/repotoc/signatures.py)): Normalized source form of function and class definition lines.
