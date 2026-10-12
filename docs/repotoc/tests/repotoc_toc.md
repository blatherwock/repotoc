# tests

- [`render/`](render/repotoc_toc.md)
  - [`builders.py`](render/builders.md) ([source](../../../tests/render/builders.py)): Model builders shared by the rendering tests.
  - [`test_file_renderer.py`](render/test_file_renderer.md) ([source](../../../tests/render/test_file_renderer.py)): Tests for doc file rendering.
  - [`test_index_renderer.py`](render/test_index_renderer.md) ([source](../../../tests/render/test_index_renderer.py)): Tests for index rendering.
  - [`test_markdown.py`](render/test_markdown.md) ([source](../../../tests/render/test_markdown.py)): Tests for the Markdown emission helpers.
  - [`test_paths.py`](render/test_paths.md) ([source](../../../tests/render/test_paths.py)): Tests for the artifact path computation.
  - [`test_render.py`](render/test_render.md) ([source](../../../tests/render/test_render.py)): Tests for the rendering entry point: module models into the artifact set.
- [`test_cli.py`](test_cli.md) ([source](../../../tests/test_cli.py)): Tests for the command line interface.
- [`test_collect.py`](test_collect.md) ([source](../../../tests/test_collect.py)): Tests for the collection layer.
- [`test_config.py`](test_config.md) ([source](../../../tests/test_config.py)): Tests for config resolution: defaults, `[tool.repotoc]`, and overlays.
- [`test_filters.py`](test_filters.md) ([source](../../../tests/test_filters.py)): Tests for the rendering presentation filters and render config.
- [`test_generate.py`](test_generate.md) ([source](../../../tests/test_generate.py)): Tests for generating the artifact into the output directory.
- [`test_models.py`](test_models.md) ([source](../../../tests/test_models.py)): Tests for the collection model dataclasses.
- [`test_site_build.py`](test_site_build.md) ([source](../../../tests/test_site_build.py)): Tests for the site showcase build script.
- [`test_smoke.py`](test_smoke.md) ([source](../../../tests/test_smoke.py)): Smoke test: the package is importable.
