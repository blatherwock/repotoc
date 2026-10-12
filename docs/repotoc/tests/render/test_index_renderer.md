# `tests/render/test_index_renderer.py`

> Tests for index rendering.

## `def test_root_index_title_states_the_output() -> None:`

> A root index with no contents states the output as its title.

---

## `def test_subdirectory_index_title_states_the_directory() -> None:`

> A subdirectory index with no contents states its directory path.

---

## `def test_file_entries_link_doc_and_source() -> None:`

> A file entry carries the prefix and links to both files, no suffix.

---

## `def test_file_entries_end_with_the_first_docstring_line() -> None:`

> A file entry ends with its module's first docstring line.

---

## `def test_directory_entries_link_to_the_child_index() -> None:`

> A directory entry expands into its own contents, indented one step.

---

## `def test_directory_entries_link_to_the_init_file() -> None:`

> A directory entry's source link targets the folder's `__init__.py`.
>
> A directory without one carries no source link.

---

## `def test_directory_entries_end_with_the_init_first_line() -> None:`

> A directory entry ends with its init docstring's first line.

---

## `def test_init_docstring_renders_in_full_under_the_index_title() -> None:`

> The folder's `__init__.py` docstring renders as the index's prologue.

---

## `def test_childless_index_renders_title_and_blockquote_only() -> None:`

> An index for a directory holding only an init docstring stays bare.

---

## `def test_depth_limits_the_nested_listing() -> None:`

> A directory at the last depth level is listed but not expanded.

---

## `def test_toc_max_depths_apply_per_level() -> None:`

> The root index uses the first setting; later settings apply deeper.

---

## `def test_index_depth_takes_the_last_position_deeper() -> None:`

> Positions past the last setting reuse the last depth.
