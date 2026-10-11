"""Generation layer: write and prune the tool-owned artifact output directory."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from repotoc.errors import GenerationError
from repotoc.render import render

if TYPE_CHECKING:
    from repotoc.filters import RenderConfig
    from repotoc.models import Module


@dataclass(frozen=True)
class GenerationReport:
    """The outcome of one generation run.

    Attributes:
        written: The output-relative POSIX paths of the files the run wrote.
        deleted: The output-relative POSIX paths of the stale Markdown files
            the run deleted.
    """

    written: list[str]
    deleted: list[str]


def generate(modules: list[Module], config: RenderConfig) -> GenerationReport:
    """Generate the artifact into the configured output directory.

    The output directory is tool-owned: the run writes the rendered file set,
    creating the directory when missing, and deletes `.md` files under it that
    the current run does not produce. Files with other suffixes stay.

    Args:
        modules: The module models, in collection order.
        config: The presentation settings.

    Returns:
        A report of the written and deleted paths, both sorted.

    Raises:
        GenerationError: The output directory cannot be created, written, or
            pruned.
    """
    files = render(modules, config)
    output = Path(config.output)
    _create(output)
    written = []
    for path in sorted(files):
        _write(output / path, files[path])
        written.append(path)
    deleted = []
    for path in sorted(output.rglob("*.md")):
        relative = path.relative_to(output).as_posix()
        if relative in files:
            continue
        _delete(path)
        deleted.append(relative)
    return GenerationReport(written=written, deleted=deleted)


def _create(output: Path) -> None:
    """Create the output directory, its parents included."""
    try:
        output.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        raise GenerationError(str(output), _reason(error)) from error


def _write(path: Path, text: str) -> None:
    """Write one artifact file as UTF-8 text, creating its directories."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    except OSError as error:
        raise GenerationError(str(path), _reason(error)) from error


def _delete(path: Path) -> None:
    """Delete one stale Markdown file."""
    try:
        path.unlink()
    except OSError as error:
        raise GenerationError(str(path), _reason(error)) from error


def _reason(error: OSError) -> str:
    """Return the filesystem's message for the error."""
    return error.strerror or str(error)
