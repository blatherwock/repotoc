# `tests/render/test_paths.py`

> Tests for the artifact path computation.

## `def test_is_init_matches_only_the_package_file() -> None:`

> Only `__init__.py` names count as package files.

---

## `def test_doc_path_mirrors_the_source_path() -> None:`

> The doc path swaps the source suffix for `.md` at the same location.

---

## `def test_index_path_sits_inside_the_directory() -> None:`

> The index path places the tool-owned index inside the directory.

---

## `def test_parent_returns_the_enclosing_directory() -> None:`

> A nested path yields its directory; a top-level path yields the root.

---

## `def test_directory_chain_reaches_the_root() -> None:`

> The chain carries the directory and every ancestor up to the root.

---

## `def test_within_output_strips_the_directory_prefix() -> None:`

> A path inside the output tree renders relative to the directory.

---

## `def test_source_link_climbs_from_the_base_to_the_target() -> None:`

> The source link climbs out of the base directory, then down.
