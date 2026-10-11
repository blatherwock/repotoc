"""Tests for the rendering presentation filters and render config."""

import pytest

from repotoc.filters import Filters, RenderConfig
from repotoc.models import Class, Function


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


def _filters(config: RenderConfig | None = None) -> Filters:
    """Build filters bound to the given config, or a default one."""
    if config is None:
        config = RenderConfig(output="out")
    return Filters(config)


def test_config_defaults_show_the_full_outline() -> None:
    """A fresh config caps nothing, hides privates, and shows signatures."""
    config = RenderConfig(output="out")

    assert config.output == "out"
    assert config.file_member_depth is None
    assert config.file_include_privates is False
    assert config.file_include_signatures is True
    assert config.toc_max_depths == (6,)


def test_empty_toc_max_depths_are_rejected() -> None:
    """An empty per-level depth list fails validation."""
    with pytest.raises(ValueError, match="toc_max_depths"):
        RenderConfig(output="out", toc_max_depths=())


def test_non_positive_toc_max_depths_are_rejected() -> None:
    """A per-level depth below one fails validation."""
    with pytest.raises(ValueError, match="toc_max_depths"):
        RenderConfig(output="out", toc_max_depths=(6, 0))


def test_non_positive_file_member_depth_is_rejected() -> None:
    """A member depth below one fails validation."""
    with pytest.raises(ValueError, match="file_member_depth"):
        RenderConfig(output="out", file_member_depth=0)


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


def test_file_include_privates_makes_underscore_names_visible() -> None:
    """With the private flag, underscore-prefixed names pass the filter."""
    filters = _filters(RenderConfig(output="out", file_include_privates=True))

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
