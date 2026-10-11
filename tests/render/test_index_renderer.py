"""Tests for index rendering."""

from __future__ import annotations

from typing import TYPE_CHECKING

from builders import module

from repotoc.filters import RenderConfig
from repotoc.render import index_renderer

if TYPE_CHECKING:
    from repotoc.models import Module

# Per-level depths used by the per-level depth test.
_ROOT_DEPTH = 2
_DEEPER_DEPTH = 4


def _render_index(
    directory: str,
    docs: list[tuple[str, Module]] | None = None,
    directories: set[str] | None = None,
    inits: dict[str, Module] | None = None,
    config: RenderConfig | None = None,
) -> str:
    """Render one index with empty defaults for the parts a test leaves out."""
    return index_renderer.render_index(
        directory,
        docs or [],
        directories if directories is not None else {"."},
        inits or {},
        config if config is not None else RenderConfig(output="out"),
    )


def test_root_index_title_states_the_output() -> None:
    """A root index with no contents states the output as its title."""
    assert _render_index(".") == "# out\n"


def test_subdirectory_index_title_states_the_directory() -> None:
    """A subdirectory index with no contents states its directory path."""
    assert _render_index("src/pkg") == "# src/pkg\n"


def test_file_entries_link_doc_and_source() -> None:
    """A file entry carries the prefix and links to both files, no suffix."""
    docs = [("mod.md", module("mod.py"))]

    text = _render_index(".", docs)

    assert text == "# out\n\n- file: [`mod.py`](mod.md) ([source](../mod.py))\n"


def test_file_entries_end_with_the_first_docstring_line() -> None:
    """A file entry ends with its module's first docstring line."""
    docs = [("mod.md", module("mod.py", docstring="Does things.\n\nMore."))]

    text = _render_index(".", docs)

    assert text == (
        "# out\n\n- file: [`mod.py`](mod.md) ([source](../mod.py)): Does things.\n"
    )


def test_directory_entries_link_to_the_child_index() -> None:
    """A directory entry expands into its own contents, indented one step."""
    docs = [("src/pkg/mod.md", module("src/pkg/mod.py"))]
    directories = {"src/pkg", "src", "."}

    text = _render_index(".", docs, directories)

    assert text == (
        "# out\n"
        "\n"
        "- dir: [`src/`](src/repotoc_toc.md)\n"
        "  - dir: [`pkg/`](src/pkg/repotoc_toc.md)\n"
        "    - file: [`mod.py`](src/pkg/mod.md) ([source](../src/pkg/mod.py))\n"
    )


def test_directory_entries_link_to_the_init_file() -> None:
    """A directory entry's source link targets the folder's `__init__.py`.

    A directory without one carries no source link.
    """
    docs = [("src/pkg/mod.md", module("src/pkg/mod.py"))]
    inits = {"src/pkg": module("src/pkg/__init__.py")}

    text = _render_index(".", docs, {"src/pkg", "src", "."}, inits)

    assert "- dir: [`src/`](src/repotoc_toc.md)\n" in text
    assert (
        "  - dir: [`pkg/`](src/pkg/repotoc_toc.md)"
        " ([source](../src/pkg/__init__.py))\n" in text
    )


def test_directory_entries_end_with_the_init_first_line() -> None:
    """A directory entry ends with its init docstring's first line."""
    docs = [("src/pkg/mod.md", module("src/pkg/mod.py"))]
    directories = {"src/pkg", "src", "."}
    inits = {"src/pkg": module("src/pkg/__init__.py", docstring="Package doc.\nMore.")}

    text = _render_index(".", docs, directories, inits)

    assert "- dir: [`src/`](src/repotoc_toc.md)\n" in text
    assert (
        "  - dir: [`pkg/`](src/pkg/repotoc_toc.md)"
        " ([source](../src/pkg/__init__.py)): Package doc.\n" in text
    )


def test_init_docstring_renders_in_full_under_the_index_title() -> None:
    """The folder's `__init__.py` docstring renders as the index's prologue."""
    docs = [("src/pkg/mod.md", module("src/pkg/mod.py"))]
    inits = {
        "src/pkg": module(
            "src/pkg/__init__.py", docstring="Package doc.\n\nMore detail."
        )
    }

    text = _render_index("src/pkg", docs, {"src/pkg", "src", "."}, inits)

    assert text == (
        "# src/pkg\n"
        "\n"
        "> Package doc.\n"
        ">\n"
        "> More detail.\n"
        "\n"
        "- file: [`mod.py`](mod.md) ([source](../../../src/pkg/mod.py))\n"
    )


def test_childless_index_renders_title_and_blockquote_only() -> None:
    """An index for a directory holding only an init docstring stays bare."""
    inits = {"pkg": module("pkg/__init__.py", docstring="Package doc.")}

    text = _render_index("pkg", None, {"pkg", "."}, inits)

    assert text == "# pkg\n\n> Package doc.\n"


def test_depth_limits_the_nested_listing() -> None:
    """A directory at the last depth level is listed but not expanded."""
    docs = [("src/pkg/mod.md", module("src/pkg/mod.py"))]
    directories = {"src/pkg", "src", "."}
    config = RenderConfig(output="out", toc_max_depths=(2,))

    text = _render_index(".", docs, directories, None, config)

    assert "- dir: [`pkg/`](src/pkg/repotoc_toc.md)\n" in text
    assert "file:" not in text


def test_toc_max_depths_apply_per_level() -> None:
    """The root index uses the first setting; later settings apply deeper."""
    docs = [("src/a/b/mod.md", module("src/a/b/mod.py"))]
    directories = {"src/a/b", "src/a", "src", "."}
    config = RenderConfig(output="out", toc_max_depths=(1, 3))

    root = _render_index(".", docs, directories, None, config)
    assert "- dir: [`src/`](src/repotoc_toc.md)\n" in root
    assert "\n  " not in root

    src = _render_index("src", docs, directories, None, config)
    assert (
        "    - file: [`mod.py`](a/b/mod.md) ([source](../../src/a/b/mod.py))\n" in src
    )


def test_index_depth_takes_the_last_position_deeper() -> None:
    """Positions past the last setting reuse the last depth."""
    config = RenderConfig(output="out", toc_max_depths=(_ROOT_DEPTH, _DEEPER_DEPTH))

    assert index_renderer.index_depth(config, ".") == _ROOT_DEPTH
    assert index_renderer.index_depth(config, "src") == _DEEPER_DEPTH
    assert index_renderer.index_depth(config, "src/a/b") == _DEEPER_DEPTH
