# tests

- dir: [`render/`](render/repotoc_index.md)
  - file: [`builders.py`](render/builders.md) ([source](../../../tests/render/builders.py)): Model builders shared by the rendering tests.
  - file: [`test_file_renderer.py`](render/test_file_renderer.md) ([source](../../../tests/render/test_file_renderer.py)): Tests for doc file rendering.
  - file: [`test_index_renderer.py`](render/test_index_renderer.md) ([source](../../../tests/render/test_index_renderer.py)): Tests for index rendering.
  - file: [`test_markdown.py`](render/test_markdown.md) ([source](../../../tests/render/test_markdown.py)): Tests for the Markdown emission helpers.
  - file: [`test_paths.py`](render/test_paths.md) ([source](../../../tests/render/test_paths.py)): Tests for the artifact path computation.
  - file: [`test_render.py`](render/test_render.md) ([source](../../../tests/render/test_render.py)): Tests for the rendering entry point: module models into the artifact set.
- file: [`test_cli.py`](test_cli.md) ([source](../../../tests/test_cli.py)): Tests for the command line interface.
- file: [`test_collect.py`](test_collect.md) ([source](../../../tests/test_collect.py)): Tests for the collection layer.
- file: [`test_config.py`](test_config.md) ([source](../../../tests/test_config.py)): Tests for config resolution: defaults, `[tool.repotoc]`, and overlays.
- file: [`test_filters.py`](test_filters.md) ([source](../../../tests/test_filters.py)): Tests for the rendering presentation filters and render config.
- file: [`test_generate.py`](test_generate.md) ([source](../../../tests/test_generate.py)): Tests for generating the artifact into the output directory.
- file: [`test_models.py`](test_models.md) ([source](../../../tests/test_models.py)): Tests for the collection model dataclasses.
- file: [`test_smoke.py`](test_smoke.md) ([source](../../../tests/test_smoke.py)): Smoke test: the package is importable.
