"""Tests for the rendering entry point: module models into the artifact set."""

from builders import function, klass, module

from repotoc.filters import RenderConfig
from repotoc.render import render


def test_no_modules_render_no_files() -> None:
    """An empty module list produces no files, not even a root index."""
    assert render([], RenderConfig(output="out")) == {}


def test_plain_module_renders_doc_file_and_root_index() -> None:
    """A plain module yields its doc file plus the root index."""
    files = render([module("mod.py")], RenderConfig(output="out"))

    assert set(files) == {"mod.md", "repotoc_toc.md"}
    assert files["mod.md"].startswith("# `mod.py`\n")
    assert "- [`mod.py`](mod.md) ([source](../mod.py))\n" in files["repotoc_toc.md"]


def test_indexes_exist_at_every_ancestor_directory() -> None:
    """Each directory on the way to a doc file gets an index."""
    files = render([module("src/a/b/mod.py")], RenderConfig(output="out"))

    assert set(files) == {
        "src/a/b/mod.md",
        "src/a/b/repotoc_toc.md",
        "src/a/repotoc_toc.md",
        "src/repotoc_toc.md",
        "repotoc_toc.md",
    }


def test_docstring_only_init_renders_index_instead_of_doc_file() -> None:
    """A memberless init surfaces its docstring in the indexes only."""
    modules = [module("pkg/__init__.py", docstring="Package doc.")]

    files = render(modules, RenderConfig(output="out"))

    assert set(files) == {"pkg/repotoc_toc.md", "repotoc_toc.md"}
    assert files["pkg/repotoc_toc.md"] == "# pkg\n\n> Package doc.\n"
    assert (
        "- [`pkg/`](pkg/repotoc_toc.md)"
        " ([source](../pkg/__init__.py)): Package doc.\n" in files["repotoc_toc.md"]
    )


def test_memberless_init_without_docstring_leaves_no_trace() -> None:
    """A directory holding only a docstring-less memberless init disappears."""
    modules = [module("pkg/__init__.py"), module("mod.py")]

    files = render(modules, RenderConfig(output="out"))

    assert set(files) == {"mod.md", "repotoc_toc.md"}
    assert "pkg" not in files["repotoc_toc.md"]


def test_root_init_docstring_renders_under_the_root_index_title() -> None:
    """A source-root init docstring surfaces in the root index."""
    modules = [module("__init__.py", docstring="Root doc.")]
    files = render(modules, RenderConfig(output="out"))

    assert set(files) == {"repotoc_toc.md"}
    assert files["repotoc_toc.md"] == "# out\n\n> Root doc.\n"


def test_init_with_visible_members_renders_a_doc_file_like_any_module() -> None:
    """An init with members renders a doc file and a file entry."""
    init = module(
        "pkg/__init__.py", docstring="Package doc.", members=[function("run")]
    )

    files = render([init], RenderConfig(output="out"))

    assert "# `pkg/__init__.py`\n" in files["pkg/__init__.md"]
    assert "## `def run():`\n" in files["pkg/__init__.md"]
    assert (
        "- [`__init__.py`](__init__.md) ([source](../../pkg/__init__.py))"
        ": Package doc.\n" in files["pkg/repotoc_toc.md"]
    )


def test_index_lists_multiple_modules_sorted_by_name() -> None:
    """Modules in one directory render as sorted index entries."""
    modules = [module("src/mod.py"), module("src/util.py")]

    files = render(modules, RenderConfig(output="out"))

    text = files["src/repotoc_toc.md"]
    assert "- [`mod.py`](mod.md) ([source](../../src/mod.py))\n" in text
    assert "- [`util.py`](util.md) ([source](../../src/util.py))\n" in text
    assert text.index("mod.py") < text.index("util.py")


def test_rendering_is_byte_deterministic() -> None:
    """Rendering the same models twice yields byte-identical file texts."""
    modules = [
        module("src/pkg/__init__.py", docstring="Package doc."),
        module(
            "src/pkg/mod.py",
            docstring="Module `doc`.",
            members=[
                function("run", decorators=["cache"]),
                klass("Thing", members=[function("__init__")]),
                function("_hidden"),
            ],
        ),
    ]
    config = RenderConfig(output="out", file_member_depth=2)

    first = render(modules, config)
    second = render(modules, config)

    assert list(first) == list(second)
    for key in first:
        assert first[key].encode() == second[key].encode()
