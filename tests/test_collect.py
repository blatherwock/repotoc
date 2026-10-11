"""Tests for the collection layer."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import pytest

import repodoc.signatures as signatures_module
from repodoc.collect import collect
from repodoc.errors import MissingRootError, ParseError
from repodoc.models import Class, Function

if TYPE_CHECKING:
    from pathlib import Path


def _write(root: Path, name: str, source: str) -> Path:
    """Write a source file under a root, creating parent directories."""
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    return path


def test_collect_returns_module_models_ordered_by_path(tmp_path: Path) -> None:
    """Every Python file under a root yields a model, ordered by path."""
    _write(tmp_path, "b.py", "")
    _write(tmp_path, "a.py", "")
    _write(tmp_path, "pkg/c.py", "")

    modules = collect([tmp_path])

    assert [module.source_path for module in modules] == [
        str(tmp_path / "a.py"),
        str(tmp_path / "b.py"),
        str(tmp_path / "pkg" / "c.py"),
    ]


def test_files_order_by_numeric_value(tmp_path: Path) -> None:
    """Digit runs in paths sort by value, so b2 precedes b10."""
    _write(tmp_path, "b10.py", "")
    _write(tmp_path, "b2.py", "")

    modules = collect([tmp_path])

    assert [module.source_path for module in modules] == [
        str(tmp_path / "b2.py"),
        str(tmp_path / "b10.py"),
    ]


def test_pep263_coding_cookie_is_honored(tmp_path: Path) -> None:
    """A source file declaring a non-UTF-8 encoding is decoded correctly."""
    path = tmp_path / "m.py"
    path.write_bytes(
        """# -*- coding: latin-1 -*-
'''café'''
""".encode("latin-1")
    )

    modules = collect([tmp_path])

    assert modules[0].docstring == "caf\u00e9"


def test_module_docstring_is_attached(tmp_path: Path) -> None:
    """A module docstring is stored on the module model."""
    _write(tmp_path, "m.py", '"""Module doc."""\n')

    modules = collect([tmp_path])

    assert modules[0].docstring == "Module doc."


def test_docstrings_are_stripped_of_surrounding_whitespace(tmp_path: Path) -> None:
    """Collected docstrings carry no leading or trailing whitespace."""
    _write(
        tmp_path,
        "m.py",
        '''"""  Module doc.  """


def first():
    """  First.   """


class Second:
    """Second.  """
''',
    )

    modules = collect([tmp_path])

    (first, second) = modules[0].members
    assert modules[0].docstring == "Module doc."
    assert first.docstring == "First."
    assert second.docstring == "Second."


def test_whitespace_only_docstring_counts_as_undocumented(tmp_path: Path) -> None:
    """A docstring holding only whitespace is stored as None."""
    _write(tmp_path, "m.py", 'def first():\n    """   """\n')

    modules = collect([tmp_path])

    assert modules[0].members[0].docstring is None


def test_module_without_docstring_has_none(tmp_path: Path) -> None:
    """A module without a docstring yields a model without one."""
    _write(tmp_path, "m.py", "x = 1\n")

    modules = collect([tmp_path])

    assert modules[0].docstring is None


@pytest.mark.parametrize("source", ["", "x = 1\n"])
def test_file_without_definitions_yields_module_without_members(
    tmp_path: Path, source: str
) -> None:
    """An empty file or a file without definitions yields a bare module model."""
    _write(tmp_path, "m.py", source)

    modules = collect([tmp_path])

    assert modules[0].members == []


def test_top_level_members_keep_source_order_with_signatures(
    tmp_path: Path,
) -> None:
    """Top-level definitions yield models in source order with signatures."""
    _write(
        tmp_path,
        "m.py",
        '''"""Module."""

def first(a, b=1):
    """First."""

class Second:
    """Second."""

async def third() -> None:
    ...
''',
    )

    (module,) = collect([tmp_path])

    first, second, third = module.members
    assert [member.name for member in module.members] == ["first", "Second", "third"]
    assert isinstance(first, Function)
    assert first.signature == "def first(a, b=1):"
    assert first.docstring == "First."
    assert isinstance(second, Class)
    assert second.signature == "class Second:"
    assert second.docstring == "Second."
    assert isinstance(third, Function)
    assert third.signature == "async def third() -> None:"
    assert third.docstring is None


def test_signature_covers_all_parameter_kinds(tmp_path: Path) -> None:
    """A signature keeps every parameter kind."""
    _write(
        tmp_path,
        "m.py",
        """def f(a, b: int = 1, /, c=2, *args: str, d, e: int = 3, **kw: float) -> bool:
    ...
""",
    )

    (module,) = collect([tmp_path])

    assert module.members[0].signature == (
        "def f(a, b: int=1, /, c=2, *args: str, d, e: int=3, **kw: float) -> bool:"
    )


def test_class_signature_includes_bases_and_keywords(tmp_path: Path) -> None:
    """A class signature keeps its bases and keyword arguments such as metaclass."""
    _write(
        tmp_path,
        "m.py",
        """class C(Base, metaclass=Meta):
    ...
""",
    )

    (module,) = collect([tmp_path])

    assert module.members[0].signature == "class C(Base, metaclass=Meta):"


def test_class_members_keep_source_order(tmp_path: Path) -> None:
    """Methods and nested classes yield member models in source order."""
    _write(
        tmp_path,
        "m.py",
        """class Outer:
    class Inner:
        ...
    def method(self, x: int) -> str:
        ...
""",
    )

    (module,) = collect([tmp_path])

    outer = module.members[0]
    assert isinstance(outer, Class)
    inner, method = outer.members
    assert [member.name for member in outer.members] == ["Inner", "method"]
    assert isinstance(inner, Class)
    assert inner.signature == "class Inner:"
    assert isinstance(method, Function)
    assert method.signature == "def method(self, x: int) -> str:"


def test_private_members_are_included(tmp_path: Path) -> None:
    """Underscore-prefixed members appear in the model."""
    _write(
        tmp_path,
        "m.py",
        """def _private():
    ...
""",
    )

    (module,) = collect([tmp_path])

    assert module.members[0].name == "_private"


def test_decorators_are_stored_verbatim_in_source_order(tmp_path: Path) -> None:
    """Decorators are stored as written, in source order."""
    _write(
        tmp_path,
        "m.py",
        """@first
@second( 1,  key = 2 )
def f():
    ...

@wrap
class C:
    ...
""",
    )

    (module,) = collect([tmp_path])

    function, klass = module.members
    assert function.decorators == ["first", "second( 1,  key = 2 )"]
    assert klass.decorators == ["wrap"]


def test_function_local_definitions_are_skipped(tmp_path: Path) -> None:
    """Definitions inside a function body are not collected."""
    _write(
        tmp_path,
        "m.py",
        """def outer():
    def inner():
        ...
    class Local:
        ...
    return inner
""",
    )

    (module,) = collect([tmp_path])

    assert [member.name for member in module.members] == ["outer"]


def test_attribute_style_string_literals_are_ignored(tmp_path: Path) -> None:
    """A string literal after an assignment is not treated as a docstring."""
    _write(
        tmp_path,
        "m.py",
        '''"""Module."""
x = 1
"""Attribute doc."""
def f():
    ...
''',
    )

    (module,) = collect([tmp_path])

    assert module.docstring == "Module."
    assert [member.name for member in module.members] == ["f"]


@pytest.mark.parametrize(
    "directory",
    ["__pycache__", "venv", ".venv", "build", "dist", "node_modules", ".hidden"],
)
def test_skip_listed_directories_are_skipped(tmp_path: Path, directory: str) -> None:
    """Source files under skipped or hidden directories are not collected."""
    _write(tmp_path, f"{directory}/junk.py", "def hidden():\n    ...\n")
    _write(tmp_path, "keep.py", "")

    modules = collect([tmp_path])

    assert [module.source_path for module in modules] == [str(tmp_path / "keep.py")]


def test_excluded_directories_merge_with_the_builtin_skip_list(
    tmp_path: Path,
) -> None:
    """Extra excluded names skip at walk time and the built-ins stay skipped."""
    _write(tmp_path, "generated/junk.py", "")
    _write(tmp_path, "__pycache__/junk.py", "")
    _write(tmp_path, "keep.py", "")

    modules = collect([tmp_path], exclude=["generated"])

    assert [module.source_path for module in modules] == [str(tmp_path / "keep.py")]


def test_exclude_defaults_keep_existing_calls_unchanged(tmp_path: Path) -> None:
    """Without `exclude`, every non-hidden directory still gets scanned."""
    _write(tmp_path, "generated/keep.py", "")
    _write(tmp_path, "root.py", "")

    modules = collect([tmp_path])

    assert [module.source_path for module in modules] == [
        str(tmp_path / "generated" / "keep.py"),
        str(tmp_path / "root.py"),
    ]


def test_file_reachable_through_overlapping_roots_is_collected_once(
    tmp_path: Path,
) -> None:
    """A file reachable through two roots yields one model."""
    _write(tmp_path, "pkg/c.py", "")

    modules = collect([tmp_path, tmp_path / "pkg"])

    assert [module.source_path for module in modules] == [
        str(tmp_path / "pkg" / "c.py")
    ]


def test_missing_root_raises_error_naming_the_root(tmp_path: Path) -> None:
    """A root that does not exist raises a missing-root error naming the root."""
    missing = tmp_path / "missing"

    with pytest.raises(MissingRootError) as excinfo:
        collect([missing])

    assert excinfo.value.root == str(missing)
    assert str(missing) in str(excinfo.value)


def test_syntax_error_raises_parse_error_with_path_and_message(
    tmp_path: Path,
) -> None:
    """A syntax error raises a parse error carrying path and message."""
    path = _write(tmp_path, "bad.py", "def f(:\n")

    with pytest.raises(ParseError) as excinfo:
        collect([tmp_path])

    assert excinfo.value.path == str(path)
    assert excinfo.value.message
    assert str(path) in str(excinfo.value)


def test_signature_falls_back_when_unparse_is_malformed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A malformed unparsed definition falls back to manual reconstruction."""
    # PEP 695 generic syntax parses from Python 3.12 only.
    generics = (
        """class Gen[T: Bound]:
    ...
def generic[T](x: T) -> T:
    ...
"""
        if sys.version_info >= (3, 12)
        else ""
    )
    _write(
        tmp_path,
        "m.py",
        """class C(Base, metaclass=Meta):
    ...
class D:
    ...
"""
        + generics
        + """def sync(a=1) -> int:
    ...
async def aio():
    ...
""",
    )
    real_unparse = signatures_module.ast.unparse

    def fake_unparse(node: signatures_module.ast.AST) -> str:
        definitions = (
            signatures_module.ast.FunctionDef,
            signatures_module.ast.AsyncFunctionDef,
            signatures_module.ast.ClassDef,
        )
        if isinstance(node, definitions):
            return "not a definition"
        return real_unparse(node)

    monkeypatch.setattr(signatures_module.ast, "unparse", fake_unparse)

    (module,) = collect([tmp_path])

    expected = ["class C(Base, metaclass=Meta):", "class D:"]
    if sys.version_info >= (3, 12):
        expected += ["class Gen[T: Bound]:", "def generic[T](x: T) -> T:"]
    expected += ["def sync(a=1) -> int:", "async def aio():"]
    assert [member.signature for member in module.members] == expected
