"""Collection layer: turn source roots into module models via static AST parsing."""

import ast
import re
import tokenize
from pathlib import Path
from typing import TYPE_CHECKING, cast

from repodoc.errors import MissingRootError, ParseError
from repodoc.models import Class, Function, Module
from repodoc.signatures import signature

if TYPE_CHECKING:
    from collections.abc import Iterable

# Directory names never scanned for source files.
_SKIP_DIRECTORIES = frozenset(
    {"__pycache__", "venv", ".venv", "build", "dist", "node_modules"}
)

# Splits a path into alternating non-digit and digit runs for natural ordering.
_NUMBER_SPLIT = re.compile(r"(\d+)")


def collect(roots: Iterable[str | Path]) -> list[Module]:
    """Collect module models from every Python file under the given roots.

    Args:
        roots: Source root directories to scan.

    Returns:
        The module models, ordered by source path.

    Raises:
        MissingRootError: A root does not exist.
        ParseError: A source file has a syntax error.
    """
    files: dict[Path, Path] = {}
    for root in roots:
        root_path = Path(root)
        if not root_path.is_dir():
            raise MissingRootError(str(root_path))
        for path in root_path.rglob("*.py"):
            if _is_skipped(path, root_path):
                continue
            files.setdefault(path.resolve(), path)
    return [
        _collect_module(path) for path in sorted(files.values(), key=_path_sort_key)
    ]


def _path_sort_key(path: Path) -> tuple[int | str, ...]:
    """Return a key that orders digit runs by numeric value, not lexicographically."""
    return tuple(
        int(part) if part.isdigit() else part for part in _NUMBER_SPLIT.split(str(path))
    )


def _is_skipped(path: Path, root: Path) -> bool:
    """Return whether a source path sits under a skipped directory."""
    relative = path.relative_to(root)
    return any(_is_skip_directory(part) for part in relative.parts[:-1])


def _is_skip_directory(name: str) -> bool:
    """Return whether a directory name is hidden or on the skip list."""
    return name in _SKIP_DIRECTORIES or name.startswith(".")


def _collect_module(path: Path) -> Module:
    """Parse one source file into a module model."""
    source = _read_source(path)
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as error:
        raise ParseError(str(path), error.msg) from error
    return Module(
        source_path=str(path),
        docstring=ast.get_docstring(tree, clean=True),
        members=_collect_members(tree.body, source),
    )


def _read_source(path: Path) -> str:
    """Read a source file using its PEP 263 coding declaration."""
    with tokenize.open(path) as file:
        return file.read()


def _collect_members(body: list[ast.stmt], source: str) -> list[Function | Class]:
    """Collect the definitions defined directly in a module or class body."""
    members: list[Function | Class] = []
    for node in body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            members.append(_collect_function(node, source))
        elif isinstance(node, ast.ClassDef):
            members.append(_collect_class(node, source))
    return members


def _collect_function(
    node: ast.FunctionDef | ast.AsyncFunctionDef, source: str
) -> Function:
    """Build a function model from a function definition node."""
    return Function(
        name=node.name,
        signature=signature(node),
        docstring=ast.get_docstring(node, clean=True),
        decorators=_decorators(node, source),
    )


def _collect_class(node: ast.ClassDef, source: str) -> Class:
    """Build a class model from a class definition node."""
    return Class(
        name=node.name,
        signature=signature(node),
        docstring=ast.get_docstring(node, clean=True),
        decorators=_decorators(node, source),
        members=_collect_members(node.body, source),
    )


def _decorators(
    node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef, source: str
) -> list[str]:
    """Return the decorator expressions as written in source order."""
    return [
        cast("str", ast.get_source_segment(source, decorator))
        for decorator in node.decorator_list
    ]
