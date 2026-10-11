# tests/test_filters.py

> Tests for the rendering presentation filters and render config.

## test_config_defaults_show_the_full_outline

> A fresh config caps nothing, hides privates, and shows signatures.

```python
def test_config_defaults_show_the_full_outline() -> None:
```

## test_empty_toc_max_depths_are_rejected

> An empty per-level depth list fails validation.

```python
def test_empty_toc_max_depths_are_rejected() -> None:
```

## test_non_positive_toc_max_depths_are_rejected

> A per-level depth below one fails validation.

```python
def test_non_positive_toc_max_depths_are_rejected() -> None:
```

## test_non_positive_file_member_depth_is_rejected

> A member depth below one fails validation.

```python
def test_non_positive_file_member_depth_is_rejected() -> None:
```

## test_public_names_are_visible

> A name without an underscore prefix passes the visibility filter.

```python
def test_public_names_are_visible() -> None:
```

## test_underscore_names_are_not_visible_by_default

> An underscore-prefixed name fails the visibility filter by default.

```python
def test_underscore_names_are_not_visible_by_default() -> None:
```

## test_init_and_new_are_visible_without_the_private_flag

> `__init__` and `__new__` pass the visibility filter despite their prefix.

```python
def test_init_and_new_are_visible_without_the_private_flag() -> None:
```

## test_file_include_privates_makes_underscore_names_visible

> With the private flag, underscore-prefixed names pass the filter.

```python
def test_file_include_privates_makes_underscore_names_visible() -> None:
```

## test_visible_members_keeps_public_and_omits_private

> The member list keeps public members and drops private ones.

```python
def test_visible_members_keeps_public_and_omits_private() -> None:
```

## test_visible_members_always_keeps_constructors

> `__init__` renders in a member list without the private flag.

```python
def test_visible_members_always_keeps_constructors() -> None:
```

## test_visibility_applies_recursively_through_class_bodies

> Private members inside classes, at any nesting depth, are filtered too.

```python
def test_visibility_applies_recursively_through_class_bodies() -> None:
```

## test_filtered_class_keeps_its_other_fields

> Filtering a class preserves its signature, docstring, and decorators.

```python
def test_filtered_class_keeps_its_other_fields() -> None:
```
