# `src/repotoc/filters.py`

> Presentation settings and the visibility filter they drive.

## `class RenderConfig:`

> Presentation settings for rendering the artifact.
>
> The settings are namespaced by domain: `file_*` governs doc files, `toc_*`
> governs indexes.
>
> Attributes:
>     output: The output directory for the artifact.
>     file_member_depth: The outline depth in doc files. None (default) is
>         unlimited; 1 renders module-level members only.
>     file_include_privates: Whether underscore-prefixed members render.
>     file_include_signatures: Whether member source blocks render.
>     toc_max_depths: Per-level nested-list depths for indexes: position 1
>         sets the root index's depth, each later position sets the next
>         level's, and the last position applies to every deeper level.

---

## `class Filters:`

> The visibility filter, bound to one render config.
>
> A stateless function object: construct once per rendering run; every
> method reads the bound config and holds no other state.

### `def __init__(self, config: RenderConfig) -> None:`

> Bind the filter to one render config.

### `def is_visible(self, name: str) -> bool:`

> Return whether a member name passes the visibility filter.
>
> Public names render; `__init__` and `__new__` always render; other
> underscore-prefixed names render only when `file_include_privates` is
> set.

### `def visible_members(self, members: list[Function | Class]) -> list[Function | Class]:`

> Return the members passing the visibility filter, recursively into classes.
>
> Filtered classes keep their other fields; their member list is the filtered one.
