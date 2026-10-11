"""Rendering layer: turn module models into Markdown doc files and indexes."""

from __future__ import annotations

from typing import TYPE_CHECKING

from repotoc.filters import Filters
from repotoc.render import file_renderer, index_renderer, paths

if TYPE_CHECKING:
    from repotoc.filters import RenderConfig
    from repotoc.models import Module


def render(modules: list[Module], config: RenderConfig) -> dict[str, str]:
    """Render the module models into the artifact file set.

    Args:
        modules: The module models, in collection order.
        config: The presentation settings.

    Returns:
        A mapping from output-relative POSIX paths to file texts: one doc file
        per module except memberless `__init__.py` files, and one index per
        directory holding doc files, child indexes, or an `__init__.py`
        docstring. Deterministic for a given input.
    """
    filters = Filters(config)
    files: dict[str, str] = {}
    docs: list[tuple[str, Module]] = []
    inits: dict[str, Module] = {}
    for module in modules:
        if paths.is_init(module.source_path):
            inits[paths.parent(module.source_path)] = module
            if not file_renderer.has_doc(module, filters):
                continue
        doc_path = paths.doc_path(module.source_path)
        files[doc_path] = file_renderer.render_doc(module, filters, config)
        docs.append((doc_path, module))
    directories = _directories(docs, inits)
    for directory in sorted(directories):
        files[paths.index_path(directory)] = index_renderer.render_index(
            directory, docs, directories, inits, config
        )
    return dict(sorted(files.items()))


def _directories(docs: list[tuple[str, Module]], inits: dict[str, Module]) -> set[str]:
    """Return every output directory that gets an index.

    A directory needs an index when it directly holds doc files, holds a child
    index, or directly holds a docstring-bearing `__init__.py`: every ancestor
    of a doc file holds one or the other, and a docstring-bearing `__init__.py`
    makes its directory and every ancestor hold an index even without doc
    files, because the docstring surfaces in those indexes. The root is `.`.
    """
    directories: set[str] = set()
    for doc_path, _ in docs:
        directories |= paths.directory_chain(paths.parent(doc_path))
    for directory, init in inits.items():
        if init.docstring is not None:
            directories |= paths.directory_chain(directory)
    return directories
