# `tests/test_filters.py`

> Tests for the rendering presentation filters and render config.

## `def test_config_defaults_show_the_full_outline() -> None:`

> A fresh config caps nothing, hides privates, and shows signatures.

---

## `def test_empty_toc_max_depths_are_rejected() -> None:`

> An empty per-level depth list fails validation.

---

## `def test_non_positive_toc_max_depths_are_rejected() -> None:`

> A per-level depth below one fails validation.

---

## `def test_non_positive_file_member_depth_is_rejected() -> None:`

> A member depth below one fails validation.

---

## `def test_public_names_are_visible() -> None:`

> A name without an underscore prefix passes the visibility filter.

---

## `def test_underscore_names_are_not_visible_by_default() -> None:`

> An underscore-prefixed name fails the visibility filter by default.

---

## `def test_init_and_new_are_visible_without_the_private_flag() -> None:`

> `__init__` and `__new__` pass the visibility filter despite their prefix.

---

## `def test_file_include_privates_makes_underscore_names_visible() -> None:`

> With the private flag, underscore-prefixed names pass the filter.

---

## `def test_visible_members_keeps_public_and_omits_private() -> None:`

> The member list keeps public members and drops private ones.

---

## `def test_visible_members_always_keeps_constructors() -> None:`

> `__init__` renders in a member list without the private flag.

---

## `def test_visibility_applies_recursively_through_class_bodies() -> None:`

> Private members inside classes, at any nesting depth, are filtered too.

---

## `def test_filtered_class_keeps_its_other_fields() -> None:`

> Filtering a class preserves its signature, docstring, and decorators.
