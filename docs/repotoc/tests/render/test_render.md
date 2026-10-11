# tests/render/test_render.py

> Tests for the rendering entry point: module models into the artifact set.

## test_no_modules_render_no_files

> An empty module list produces no files, not even a root index.

```python
def test_no_modules_render_no_files() -> None:
```

## test_plain_module_renders_doc_file_and_root_index

> A plain module yields its doc file plus the root index.

```python
def test_plain_module_renders_doc_file_and_root_index() -> None:
```

## test_indexes_exist_at_every_ancestor_directory

> Each directory on the way to a doc file gets an index.

```python
def test_indexes_exist_at_every_ancestor_directory() -> None:
```

## test_docstring_only_init_renders_index_instead_of_doc_file

> A memberless init surfaces its docstring in the indexes only.

```python
def test_docstring_only_init_renders_index_instead_of_doc_file() -> None:
```

## test_memberless_init_without_docstring_leaves_no_trace

> A directory holding only a docstring-less memberless init disappears.

```python
def test_memberless_init_without_docstring_leaves_no_trace() -> None:
```

## test_root_init_docstring_renders_under_the_root_index_title

> A source-root init docstring surfaces in the root index.

```python
def test_root_init_docstring_renders_under_the_root_index_title() -> None:
```

## test_init_with_visible_members_renders_a_doc_file_like_any_module

> An init with members renders a doc file and a file entry.

```python
def test_init_with_visible_members_renders_a_doc_file_like_any_module() -> None:
```

## test_index_lists_multiple_modules_sorted_by_name

> Modules in one directory render as sorted index entries.

```python
def test_index_lists_multiple_modules_sorted_by_name() -> None:
```

## test_rendering_is_byte_deterministic

> Rendering the same models twice yields byte-identical file texts.

```python
def test_rendering_is_byte_deterministic() -> None:
```
