# `src/repotoc/render/index_renderer.py`

> Index rendering: directory contents into Markdown index files.

## `def render_index(directory: str, docs: list[tuple[str, Module]], directories: set[str], inits: dict[str, Module], config: RenderConfig) -> str:`

> Render one directory's index file text.
>
> The index opens with the folder's `__init__.py` docstring in full as a
> blockquote when it has one, then lists the folder contents as a nested
> list. The list grows one indentation step per level; a directory at the
> last level is listed but not expanded. Links stay relative to the index
> file's own directory, not to the directory being expanded. Each entry ends
> with its target's first docstring line when it has one; a directory entry
> links to its folder's `__init__.py` as the source, or carries no source
> link when the folder has none.

---

## `def index_depth(config: RenderConfig, directory: str) -> int:`

> Return the list depth for the directory's index level.
>
> Position 1 of the per-level settings sets the root index's depth, each
> later position sets the next level's, and the last position applies to
> every deeper level.
