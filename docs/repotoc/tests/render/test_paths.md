# tests/render/test_paths.py

> Tests for the artifact path computation.

## test_is_init_matches_only_the_package_file

> Only `__init__.py` names count as package files.

```python
def test_is_init_matches_only_the_package_file() -> None:
```

## test_doc_path_mirrors_the_source_path

> The doc path swaps the source suffix for `.md` at the same location.

```python
def test_doc_path_mirrors_the_source_path() -> None:
```

## test_index_path_sits_inside_the_directory

> The index path places the tool-owned index inside the directory.

```python
def test_index_path_sits_inside_the_directory() -> None:
```

## test_parent_returns_the_enclosing_directory

> A nested path yields its directory; a top-level path yields the root.

```python
def test_parent_returns_the_enclosing_directory() -> None:
```

## test_directory_chain_reaches_the_root

> The chain carries the directory and every ancestor up to the root.

```python
def test_directory_chain_reaches_the_root() -> None:
```

## test_within_output_strips_the_directory_prefix

> A path inside the output tree renders relative to the directory.

```python
def test_within_output_strips_the_directory_prefix() -> None:
```

## test_source_link_climbs_from_the_base_to_the_target

> The source link climbs out of the base directory, then down.

```python
def test_source_link_climbs_from_the_base_to_the_target() -> None:
```
