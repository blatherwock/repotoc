"""Presentation config and the filters driven by it: visibility and truncation."""

from __future__ import annotations

from dataclasses import dataclass, replace

from repodoc.models import Class, Function, Module

_CONSTRUCTORS = frozenset({"__init__", "__new__"})


@dataclass(frozen=True)
class RenderConfig:
    """Presentation settings for rendering the artifact.

    Attributes:
        output: The output directory for the artifact.
        include_private: Whether underscore-prefixed members render.
        truncate_module: Whether module docstrings render as their first line only.
        truncate_class: Whether class docstrings render as their first line only.
        truncate_function: Whether function docstrings render as their first line only.
    """

    output: str
    include_private: bool = False
    truncate_module: bool = False
    truncate_class: bool = False
    truncate_function: bool = False


class Filters:
    """The presentation filters, bound to one render config.

    A stateless function object: construct once per rendering run; every
    method reads the bound config and holds no other state.
    """

    def __init__(self, config: RenderConfig) -> None:
        """Bind the filters to one render config."""
        self._config = config

    def is_visible(self, name: str) -> bool:
        """Return whether a member name passes the visibility filter.

        Public names render; `__init__` and `__new__` always render; other
        underscore-prefixed names render only when `include_private` is set.
        """
        if not name.startswith("_"):
            return True
        return name in _CONSTRUCTORS or self._config.include_private

    def visible_members(
        self, members: list[Function | Class]
    ) -> list[Function | Class]:
        """Return the members passing the visibility filter, recursively into classes.

        Filtered classes keep their other fields; their member list is the filtered one.
        """
        visible: list[Function | Class] = []
        for member in members:
            if not self.is_visible(member.name):
                continue
            if isinstance(member, Class):
                filtered = replace(member, members=self.visible_members(member.members))
                visible.append(filtered)
            else:
                visible.append(member)
        return visible

    def truncate_docstring(self, member: Module | Class | Function) -> str | None:
        """Return the member's docstring, first line only when its flag is set.

        The member's model type selects the truncation flag: module, class, or
        function. Collected docstrings are stripped, so the first line is never
        whitespace-only.
        """
        docstring = member.docstring
        if docstring is None:
            return None
        if not self._truncation_flag(member):
            return docstring
        return docstring.split("\n", 1)[0]

    def _truncation_flag(self, member: Module | Class | Function) -> bool:
        """Return the truncation flag selected by the member's model type."""
        if isinstance(member, Module):
            return self._config.truncate_module
        if isinstance(member, Class):
            return self._config.truncate_class
        return self._config.truncate_function
