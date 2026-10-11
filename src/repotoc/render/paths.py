"""Doc paths, source links, and directory chains for the artifact layout."""

from __future__ import annotations

import os
from pathlib import PurePosixPath

# Name of the index file inside every rendered directory; chosen to be unlikely
# to collide with a file already in a documented repository.
_INDEX_NAME = "repotoc_index.md"


def is_init(source_path: str) -> bool:
    """Return whether the source path is a package `__init__.py` file."""
    return PurePosixPath(source_path).name == "__init__.py"


def doc_path(source_path: str) -> str:
    """Return the output doc path mirroring the source path."""
    return PurePosixPath(source_path).with_suffix(".md").as_posix()


def index_path(directory: str) -> str:
    """Return the index path inside the output directory."""
    return (PurePosixPath(directory) / _INDEX_NAME).as_posix()


def parent(path: str) -> str:
    """Return the path's parent directory; `.` for a top-level path."""
    return PurePosixPath(path).parent.as_posix()


def directory_chain(directory: str) -> set[str]:
    """Return the directory and every ancestor directory, including the root."""
    chain = {directory}
    current = directory
    while current != ".":
        current = parent(current)
        chain.add(current)
    return chain


def within_output(path: str, directory: str) -> str:
    """Return the path relative to the directory, both inside the output tree."""
    if directory == ".":
        return path
    return PurePosixPath(path).relative_to(directory).as_posix()


def source_link(base: str, target: str) -> str:
    """Return the filesystem-relative link from the base directory to the target."""
    return os.path.relpath(target, base).replace(os.sep, "/")
