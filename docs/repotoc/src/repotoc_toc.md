# src

- [`repotoc/`](repotoc/repotoc_toc.md) ([source](../../../src/repotoc/__init__.py)): Static docstring and signature collection for Python repositories.
  - [`cli.py`](repotoc/cli.md) ([source](../../../src/repotoc/cli.py)): The `repotoc` command line interface: flags mapped onto the shared config.
  - [`collect.py`](repotoc/collect.md) ([source](../../../src/repotoc/collect.py)): Collection layer: turn source roots into module models via static AST parsing.
  - [`config.py`](repotoc/config.md) ([source](../../../src/repotoc/config.py)): Config resolution: defaults, the `[tool.repotoc]` section, and CLI overlays.
  - [`errors.py`](repotoc/errors.md) ([source](../../../src/repotoc/errors.py)): Error types raised by the config, collection, and generation layers.
  - [`filters.py`](repotoc/filters.md) ([source](../../../src/repotoc/filters.py)): Presentation settings and the visibility filter they drive.
  - [`generate.py`](repotoc/generate.md) ([source](../../../src/repotoc/generate.py)): Generation layer: write and prune the tool-owned artifact output directory.
  - [`models.py`](repotoc/models.md) ([source](../../../src/repotoc/models.py)): Model dataclasses for collected modules, classes, and functions.
  - [`render/`](repotoc/render/repotoc_toc.md) ([source](../../../src/repotoc/render/__init__.py)): Rendering layer: turn module models into Markdown doc files and indexes.
    - [`__init__.py`](repotoc/render/__init__.md) ([source](../../../src/repotoc/render/__init__.py)): Rendering layer: turn module models into Markdown doc files and indexes.
    - [`file_renderer.py`](repotoc/render/file_renderer.md) ([source](../../../src/repotoc/render/file_renderer.py)): Doc file rendering: module models into Markdown doc files.
    - [`index_renderer.py`](repotoc/render/index_renderer.md) ([source](../../../src/repotoc/render/index_renderer.py)): Index rendering: directory contents into Markdown index files.
    - [`markdown.py`](repotoc/render/markdown.md) ([source](../../../src/repotoc/render/markdown.py)): Markdown emission helpers: headings, blockquotes, rules, link and list lines.
    - [`paths.py`](repotoc/render/paths.md) ([source](../../../src/repotoc/render/paths.py)): Doc paths, source links, and directory chains for the artifact layout.
  - [`signatures.py`](repotoc/signatures.md) ([source](../../../src/repotoc/signatures.py)): Normalized source form of function and class definition lines.
- [`tools/`](tools/repotoc_toc.md)
  - [`site_build.py`](tools/site_build.md) ([source](../../../src/tools/site_build.py)): Refresh and gate the showcase site's example artifacts.
