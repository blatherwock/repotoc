# src/repotoc/render/file_renderer.py

> Doc file rendering: module models into Markdown doc files.

## has_doc

> Return whether the module renders a doc file.
>
> Every module renders one except `__init__.py` without visible members: a
> docstring-only or import-only package file surfaces its docstring in the
> indexes instead, and definitions are what make a doc file worthwhile. The
> criterion is visible members, so `file_include_privates` decides whether a
> private-only `__init__.py` emits.

```python
def has_doc(module: Module, filters: Filters) -> bool:
```

## render_doc

> Render one module model into its doc file text.
>
> The doc file states the source path as a heading, renders the module
> docstring in full as a blockquote, then outlines the visible members in
> model order.

```python
def render_doc(module: Module, filters: Filters, config: RenderConfig) -> str:
```
