"""Tests for generating the artifact into the output directory."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from repodoc.errors import GenerationError
from repodoc.filters import RenderConfig
from repodoc.generate import GenerationReport, generate
from repodoc.models import Module

if TYPE_CHECKING:
    from pathlib import Path


def _module(source_path: str, docstring: str | None = "Summary.") -> Module:
    """Build a module model with the given source path."""
    return Module(source_path=source_path, docstring=docstring, members=[])


def test_generation_writes_the_file_set_creating_the_output_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Generation creates the missing output directory and writes every file."""
    monkeypatch.chdir(tmp_path)
    config = RenderConfig(output="out")

    report = generate([_module("src/mod.py", "Does things.")], config)

    assert report.written == [
        "repodoc_index.md",
        "src/mod.md",
        "src/repodoc_index.md",
    ]
    assert report.deleted == []
    assert (tmp_path / "out" / "src" / "mod.md").read_text(encoding="utf-8") == (
        "# src/mod.py\n\n> Does things.\n"
    )
    assert (tmp_path / "out" / "repodoc_index.md").read_text(encoding="utf-8") == (
        "# out\n"
        "\n"
        "- dir: [`src/`](src/repodoc_index.md)\n"
        "  - file: [`mod.py`](src/mod.md) ([source](../src/mod.py))"
        ": Does things.\n"
    )


def test_generation_prunes_stale_markdown_and_keeps_other_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Generation deletes unproduced .md files and leaves other suffixes."""
    monkeypatch.chdir(tmp_path)
    out = tmp_path / "out"
    (out / "src").mkdir(parents=True)
    (out / "src" / "stale.md").write_text("stale", encoding="utf-8")
    (out / "root-stale.md").write_text("stale", encoding="utf-8")
    (out / "notes.txt").write_text("keep", encoding="utf-8")

    report = generate([_module("src/mod.py")], RenderConfig(output="out"))

    assert report.deleted == ["root-stale.md", "src/stale.md"]
    assert not (out / "src" / "stale.md").exists()
    assert not (out / "root-stale.md").exists()
    assert (out / "notes.txt").read_text(encoding="utf-8") == "keep"


def test_generation_without_modules_writes_only_the_output_directory(
    tmp_path: Path,
) -> None:
    """An empty module set writes nothing and prunes every .md file."""
    output = tmp_path / "out"
    output.mkdir()
    (output / "stale.md").write_text("stale", encoding="utf-8")

    report = generate([], RenderConfig(output=str(output)))

    assert report == GenerationReport(written=[], deleted=["stale.md"])
    assert not (output / "stale.md").exists()


def test_generation_is_idempotent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A second run writes the same set and deletes nothing."""
    monkeypatch.chdir(tmp_path)
    modules = [_module("src/mod.py", "Does things.")]
    config = RenderConfig(output="out")

    first = generate(modules, config)
    second = generate(modules, config)

    assert second.written == first.written
    assert second.deleted == []


def test_generation_fails_when_the_output_path_is_a_file(tmp_path: Path) -> None:
    """A file where the output directory belongs fails naming the path."""
    output = tmp_path / "out"
    output.write_text("occupied", encoding="utf-8")

    with pytest.raises(GenerationError) as info:
        generate([_module("mod.py")], RenderConfig(output=str(output)))

    assert info.value.path == str(output)
    assert info.value.message == "File exists"


def test_generation_fails_when_a_doc_path_is_a_directory(tmp_path: Path) -> None:
    """A directory where a doc file belongs fails naming the path."""
    output = tmp_path / "out"
    doc = output / "src" / "mod.md"
    doc.mkdir(parents=True)

    with pytest.raises(GenerationError) as info:
        generate([_module("src/mod.py")], RenderConfig(output=str(output)))

    assert info.value.path == str(doc)


def test_generation_fails_when_a_stale_markdown_path_is_a_directory(
    tmp_path: Path,
) -> None:
    """A directory squatting on a stale .md path fails naming the path."""
    output = tmp_path / "out"
    output.mkdir()
    (output / "stale.md").mkdir()

    with pytest.raises(GenerationError) as info:
        generate([], RenderConfig(output=str(output)))

    assert info.value.path == str(output / "stale.md")
