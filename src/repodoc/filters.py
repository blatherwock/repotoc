"""Presentation settings and the visibility filter they drive."""

from __future__ import annotations

from dataclasses import dataclass, replace

from repodoc.models import Class, Function

_CONSTRUCTORS = frozenset({"__init__", "__new__"})


@dataclass(frozen=True)
class RenderConfig:
    """Presentation settings for rendering the artifact.

    The settings are namespaced by domain: `file_*` governs doc files, `toc_*`
    governs indexes.

    Attributes:
        output: The output directory for the artifact.
        file_member_depth: The outline depth in doc files. None (default) is
            unlimited; 1 renders module-level members only.
        file_include_privates: Whether underscore-prefixed members render.
        file_include_signatures: Whether member source blocks render.
        toc_max_depths: Per-level nested-list depths for indexes: position 1
            sets the root index's depth, each later position sets the next
            level's, and the last position applies to every deeper level.
    """

    output: str
    file_member_depth: int | None = None
    file_include_privates: bool = False
    file_include_signatures: bool = True
    toc_max_depths: tuple[int, ...] = (6,)

    def __post_init__(self) -> None:
        """Validate the config: member depth and every toc depth stay positive."""
        if self.file_member_depth is not None and self.file_member_depth < 1:
            message = "file_member_depth must be None or positive"
            raise ValueError(message)
        if not self.toc_max_depths or any(depth < 1 for depth in self.toc_max_depths):
            message = "toc_max_depths must be non-empty and positive"
            raise ValueError(message)


class Filters:
    """The visibility filter, bound to one render config.

    A stateless function object: construct once per rendering run; every
    method reads the bound config and holds no other state.
    """

    def __init__(self, config: RenderConfig) -> None:
        """Bind the filter to one render config."""
        self._config = config

    def is_visible(self, name: str) -> bool:
        """Return whether a member name passes the visibility filter.

        Public names render; `__init__` and `__new__` always render; other
        underscore-prefixed names render only when `file_include_privates` is
        set.
        """
        if not name.startswith("_"):
            return True
        return name in _CONSTRUCTORS or self._config.file_include_privates

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
