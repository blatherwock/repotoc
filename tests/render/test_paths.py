"""Tests for the artifact path computation."""

from repodoc.render.paths import (
    directory_chain,
    doc_path,
    index_path,
    is_init,
    parent,
    source_link,
    within_output,
)


def test_is_init_matches_only_the_package_file() -> None:
    """Only `__init__.py` names count as package files."""
    assert is_init("pkg/__init__.py") is True
    assert is_init("pkg/mod.py") is False
    assert is_init("pkg/init.py") is False


def test_doc_path_mirrors_the_source_path() -> None:
    """The doc path swaps the source suffix for `.md` at the same location."""
    assert doc_path("mod.py") == "mod.md"
    assert doc_path("src/pkg/mod.py") == "src/pkg/mod.md"


def test_index_path_sits_inside_the_directory() -> None:
    """The index path places the tool-owned index inside the directory."""
    assert index_path(".") == "repodoc_index.md"
    assert index_path("src/pkg") == "src/pkg/repodoc_index.md"


def test_parent_returns_the_enclosing_directory() -> None:
    """A nested path yields its directory; a top-level path yields the root."""
    assert parent("src/pkg/mod.py") == "src/pkg"
    assert parent("mod.py") == "."


def test_directory_chain_reaches_the_root() -> None:
    """The chain carries the directory and every ancestor up to the root."""
    assert directory_chain(".") == {"."}
    assert directory_chain("src/pkg") == {"src/pkg", "src", "."}


def test_within_output_strips_the_directory_prefix() -> None:
    """A path inside the output tree renders relative to the directory."""
    assert within_output("src/pkg/mod.md", ".") == "src/pkg/mod.md"
    assert within_output("src/pkg/mod.md", "src") == "pkg/mod.md"
    assert within_output("src/pkg/mod.md", "src/pkg") == "mod.md"


def test_source_link_climbs_from_the_base_to_the_target() -> None:
    """The source link climbs out of the base directory, then down."""
    assert source_link("docs/repodoc", "src") == "../../src"
    assert (
        source_link("docs/repodoc/src/pkg", "src/pkg/mod.py")
        == "../../../../src/pkg/mod.py"
    )
    assert source_link("out", "src/pkg/mod.py") == "../src/pkg/mod.py"
