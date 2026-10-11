# tests/render/test_index_renderer.py

> Tests for index rendering.

## test_root_index_title_states_the_output

> A root index with no contents states the output as its title.

```python
def test_root_index_title_states_the_output() -> None:
```

## test_subdirectory_index_title_states_the_directory

> A subdirectory index with no contents states its directory path.

```python
def test_subdirectory_index_title_states_the_directory() -> None:
```

## test_file_entries_link_doc_and_source

> A file entry carries the prefix and links to both files, no suffix.

```python
def test_file_entries_link_doc_and_source() -> None:
```

## test_file_entries_end_with_the_first_docstring_line

> A file entry ends with its module's first docstring line.

```python
def test_file_entries_end_with_the_first_docstring_line() -> None:
```

## test_directory_entries_link_to_the_child_index

> A directory entry expands into its own contents, indented one step.

```python
def test_directory_entries_link_to_the_child_index() -> None:
```

## test_directory_entries_link_to_the_init_file

> A directory entry's source link targets the folder's `__init__.py`.
>
> A directory without one carries no source link.

```python
def test_directory_entries_link_to_the_init_file() -> None:
```

## test_directory_entries_end_with_the_init_first_line

> A directory entry ends with its init docstring's first line.

```python
def test_directory_entries_end_with_the_init_first_line() -> None:
```

## test_init_docstring_renders_in_full_under_the_index_title

> The folder's `__init__.py` docstring renders as the index's prologue.

```python
def test_init_docstring_renders_in_full_under_the_index_title() -> None:
```

## test_childless_index_renders_title_and_blockquote_only

> An index for a directory holding only an init docstring stays bare.

```python
def test_childless_index_renders_title_and_blockquote_only() -> None:
```

## test_depth_limits_the_nested_listing

> A directory at the last depth level is listed but not expanded.

```python
def test_depth_limits_the_nested_listing() -> None:
```

## test_toc_max_depths_apply_per_level

> The root index uses the first setting; later settings apply deeper.

```python
def test_toc_max_depths_apply_per_level() -> None:
```

## test_index_depth_takes_the_last_position_deeper

> Positions past the last setting reuse the last depth.

```python
def test_index_depth_takes_the_last_position_deeper() -> None:
```
