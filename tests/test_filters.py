"""Tests for the rendering presentation filters and render config."""

from repodoc.filters import Filters, RenderConfig
from repodoc.models import Class, Function, Module


def _function(name: str, docstring: str | None = "Doc.") -> Function:
    """Build a function model with the given name."""
    return Function(
        name=name, signature=f"def {name}():", docstring=docstring, decorators=[]
    )


def _class(
    name: str,
    members: list[Function | Class] | None = None,
    docstring: str | None = "Class doc.",
) -> Class:
    """Build a class model with the given name."""
    return Class(
        name=name,
        signature=f"class {name}:",
        docstring=docstring,
        decorators=[],
        members=members or [],
    )


def _config(**overrides: bool) -> RenderConfig:
    """Build a config with default output and the given flag overrides."""
    return RenderConfig(output="out", **overrides)


def _filters(**overrides: bool) -> Filters:
    """Build filters bound to a config with the given flag overrides."""
    return Filters(_config(**overrides))


def test_config_defaults_are_full_docstrings_and_private_members_hidden() -> None:
    """A fresh config hides private members and truncates nothing."""
    config = _config()

    assert config.output == "out"
    assert config.include_private is False
    assert config.truncate_module is False
    assert config.truncate_class is False
    assert config.truncate_function is False


def test_public_names_are_visible() -> None:
    """A name without an underscore prefix passes the visibility filter."""
    filters = _filters()

    assert filters.is_visible("run") is True


def test_underscore_names_are_not_visible_by_default() -> None:
    """An underscore-prefixed name fails the visibility filter by default."""
    filters = _filters()

    assert filters.is_visible("_helper") is False


def test_init_and_new_are_visible_without_the_private_flag() -> None:
    """`__init__` and `__new__` pass the visibility filter despite their prefix."""
    filters = _filters()

    assert filters.is_visible("__init__") is True
    assert filters.is_visible("__new__") is True


def test_include_private_makes_underscore_names_visible() -> None:
    """With the private flag, underscore-prefixed names pass the filter."""
    filters = _filters(include_private=True)

    assert filters.is_visible("_helper") is True
    assert filters.is_visible("__init__") is True


def test_visible_members_keeps_public_and_omits_private() -> None:
    """The member list keeps public members and drops private ones."""
    filters = _filters()

    members = filters.visible_members([_function("public"), _function("_private")])

    assert [member.name for member in members] == ["public"]


def test_visible_members_always_keeps_constructors() -> None:
    """`__init__` renders in a member list without the private flag."""
    filters = _filters()

    members = filters.visible_members([_function("__init__"), _function("_private")])

    assert [member.name for member in members] == ["__init__"]


def test_visibility_applies_recursively_through_class_bodies() -> None:
    """Private members inside classes, at any nesting depth, are filtered too."""
    filters = _filters()
    nested = _class("Inner", members=[_function("visible"), _function("_hidden")])
    outer = _class("Outer", members=[nested, _function("_helper")])

    members = filters.visible_members([outer])

    outer_visible = members[0]
    assert isinstance(outer_visible, Class)
    assert [member.name for member in outer_visible.members] == ["Inner"]
    inner_visible = outer_visible.members[0]
    assert isinstance(inner_visible, Class)
    assert [member.name for member in inner_visible.members] == ["visible"]


def test_filtered_class_keeps_its_other_fields() -> None:
    """Filtering a class preserves its signature, docstring, and decorators."""
    filters = _filters()
    klass = Class(
        name="C",
        signature="class C(Base):",
        docstring="Class doc.",
        decorators=["dataclass"],
        members=[_function("_hidden")],
    )

    members = filters.visible_members([klass])

    assert members[0].signature == "class C(Base):"
    assert members[0].docstring == "Class doc."
    assert members[0].decorators == ["dataclass"]


def _module(docstring: str | None) -> Module:
    """Build a module model with the given docstring."""
    return Module(source_path="mod.py", docstring=docstring, members=[])


def test_truncation_off_passes_docstring_through() -> None:
    """With no truncation flag, a docstring renders in full."""
    filters = _filters()
    function = _function("f", docstring="First line.\n\n    Second line.")

    result = filters.truncate_docstring(function)

    assert result == "First line.\n\n    Second line."


def test_truncation_selects_the_flag_by_model_type() -> None:
    """Each model type selects its own truncation flag."""
    filters = _filters(truncate_class=True)

    assert filters.truncate_docstring(_class("C")) == "Class doc."
    assert filters.truncate_docstring(_module("First.\nSecond.")) == "First.\nSecond."
    assert (
        filters.truncate_docstring(_function("f", docstring="First.\nSecond."))
        == "First.\nSecond."
    )


def test_truncation_of_each_kind_uses_its_own_flag() -> None:
    """Module, class, and function flags act independently."""
    module_filters = _filters(truncate_module=True)
    class_filters = _filters(truncate_class=True)
    function_filters = _filters(truncate_function=True)

    assert module_filters.truncate_docstring(_module("First.\nSecond.")) == "First."
    assert (
        class_filters.truncate_docstring(_class("C", docstring="First.\nSecond."))
        == "First."
    )
    assert (
        function_filters.truncate_docstring(_function("f", docstring="First.\nSecond."))
        == "First."
    )


def test_truncation_takes_only_the_first_line() -> None:
    """A truncated docstring renders its first line only."""
    filters = _filters(truncate_function=True)

    assert (
        filters.truncate_docstring(_function("f", docstring="First.\nSecond."))
        == "First."
    )


def test_missing_docstring_stays_missing_through_truncation() -> None:
    """A None docstring is None whether or not truncation applies."""
    filters = _filters(truncate_function=True)

    assert filters.truncate_docstring(_function("f", docstring=None)) is None
