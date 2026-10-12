"""Index rendering: directory contents into Markdown index files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import TYPE_CHECKING

from repotoc.render import markdown, paths

if TYPE_CHECKING:
    from repotoc.filters import RenderConfig
    from repotoc.models import Module


@dataclass(frozen=True)
class _Child:
    """One index entry: a module doc file or a child index directory.

    Attributes:
        name: The display name: the file name, or the directory name with a
            trailing slash.
        doc_path: The linked doc path: the module's doc file, or the child
            index.
        source_path: The linked source path: the module's source file, or the
            directory's `__init__.py`. None for a directory without one, so
            the entry renders without a source link.
        is_directory: Whether the entry is a child index directory.
        summary: The target's first docstring line, or None without one.
    """

    name: str
    doc_path: str
    source_path: str | None
    is_directory: bool
    summary: str | None


def render_index(
    directory: str,
    docs: list[tuple[str, Module]],
    directories: set[str],
    inits: dict[str, Module],
    config: RenderConfig,
) -> str:
    """Render one directory's index file text.

    The index opens with the folder's `__init__.py` docstring in full as a
    blockquote when it has one, then lists the folder contents as a nested
    list. The list grows one indentation step per level; a directory at the
    last level is listed but not expanded. Links stay relative to the index
    file's own directory, not to the directory being expanded. Each entry ends
    with its target's first docstring line when it has one; a directory entry
    links to its folder's `__init__.py` as the source, or carries no source
    link when the folder has none.
    """
    children = _children(docs, directories, inits)
    source_base = config.output if directory == "." else f"{config.output}/{directory}"
    depth = index_depth(config, directory)

    def entries(current: str, level: int) -> list[str]:
        """Return the nested list lines for one directory's contents."""
        lines = []
        for child in children.get(current, []):
            doc_link = paths.within_output(child.doc_path, directory)
            source_link = (
                None
                if child.source_path is None
                else paths.source_link(source_base, child.source_path)
            )
            lines.append(_entry_line(child, doc_link, source_link, level))
            if child.is_directory and level + 1 < depth:
                lines += entries(paths.parent(child.doc_path), level + 1)
        return lines

    title = config.output if directory == "." else directory
    init = inits.get(directory)
    sections = [markdown.heading(title, 1)]
    if init is not None and init.docstring is not None:
        sections.append(markdown.blockquote(init.docstring))
    body = "\n".join(entries(directory, 0))
    if body:
        sections.append(body)
    return "\n\n".join(sections) + "\n"


def index_depth(config: RenderConfig, directory: str) -> int:
    """Return the list depth for the directory's index level.

    Position 1 of the per-level settings sets the root index's depth, each
    later position sets the next level's, and the last position applies to
    every deeper level.
    """
    level = 0 if directory == "." else directory.count("/") + 1
    return config.toc_max_depths[min(level, len(config.toc_max_depths) - 1)]


def _entry_line(
    child: _Child, doc_link: str, source_link: str | None, level: int
) -> str:
    """Return one index entry line, summary suffix included when present.

    The display name carries the kind: the trailing slash marks a directory
    and the file extension marks a file.
    """
    name = f"{child.name}/" if child.is_directory else child.name
    entry = markdown.link(f"`{name}`", doc_link)
    if source_link is not None:
        entry = f"{entry} ({markdown.link('source', source_link)})"
    line = markdown.list_item(entry, level)
    if child.summary is not None:
        line = f"{line}: {child.summary}"
    return line


def _children(
    docs: list[tuple[str, Module]],
    directories: set[str],
    inits: dict[str, Module],
) -> dict[str, list[_Child]]:
    """Map every output directory to its direct children, sorted by name.

    File children carry the module doc path and source path; directory
    children carry the child index path and the init source path, or no
    source when the folder has no `__init__.py`. Each child ends with its
    target's first docstring line: a module's own, or its directory's
    `__init__.py` docstring. The output root itself is never a child.
    """
    grouped: dict[str, list[_Child]] = {}
    for doc_path, module in docs:
        grouped.setdefault(paths.parent(doc_path), []).append(
            _Child(
                name=PurePosixPath(module.source_path).name,
                doc_path=doc_path,
                source_path=module.source_path,
                is_directory=False,
                summary=_first_line(module.docstring),
            )
        )
    for directory in directories:
        if directory == ".":
            continue
        init = inits.get(directory)
        grouped.setdefault(paths.parent(directory), []).append(
            _Child(
                name=PurePosixPath(directory).name,
                doc_path=paths.index_path(directory),
                source_path=None if init is None else init.source_path,
                is_directory=True,
                summary=None if init is None else _first_line(init.docstring),
            )
        )
    return {
        parent: sorted(children, key=lambda child: child.name)
        for parent, children in grouped.items()
    }


def _first_line(docstring: str | None) -> str | None:
    """Return the docstring's first line, or None when there is no docstring.

    Collected docstrings are stripped, so the first line is never empty.
    """
    if docstring is None:
        return None
    return docstring.split("\n", 1)[0]
