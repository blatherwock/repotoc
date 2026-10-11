"""Tests for the collection model dataclasses."""

from dataclasses import FrozenInstanceError

import pytest

from repotoc.models import Class, Function, Module


def _function() -> Function:
    """Build a representative function model."""
    return Function(
        name="f",
        signature="def f(x):",
        docstring="Function doc.",
        decorators=["decorator"],
    )


def test_module_carries_source_path_docstring_and_members() -> None:
    """A module model holds its path, docstring, and ordered members."""
    function = _function()

    module = Module(
        source_path="pkg/mod.py",
        docstring="Module doc.",
        members=[function],
    )

    assert module.source_path == "pkg/mod.py"
    assert module.docstring == "Module doc."
    assert module.members == [function]


def test_function_carries_name_signature_docstring_and_decorators() -> None:
    """A function model holds its name, signature, docstring, and decorators."""
    function = _function()

    assert function.name == "f"
    assert function.signature == "def f(x):"
    assert function.docstring == "Function doc."
    assert function.decorators == ["decorator"]


def test_class_carries_name_signature_docstring_decorators_and_members() -> None:
    """A class model holds its name, signature, docstring, decorators, and members."""
    function = _function()

    klass = Class(
        name="C",
        signature="class C(Base):",
        docstring="Class doc.",
        decorators=["decorator"],
        members=[function],
    )

    assert klass.name == "C"
    assert klass.signature == "class C(Base):"
    assert klass.docstring == "Class doc."
    assert klass.decorators == ["decorator"]
    assert klass.members == [function]


def test_models_are_frozen() -> None:
    """Assigning to a model field fails."""
    module = Module(source_path="mod.py", docstring=None, members=[])
    field = "source_path"

    with pytest.raises(FrozenInstanceError):
        setattr(module, field, "other.py")
