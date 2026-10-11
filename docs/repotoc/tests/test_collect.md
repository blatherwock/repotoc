# tests/test_collect.py

> Tests for the collection layer.

## test_collect_returns_module_models_ordered_by_path

> Every Python file under a root yields a model, ordered by path.

```python
def test_collect_returns_module_models_ordered_by_path(tmp_path: Path) -> None:
```

## test_files_order_by_numeric_value

> Digit runs in paths sort by value, so b2 precedes b10.

```python
def test_files_order_by_numeric_value(tmp_path: Path) -> None:
```

## test_pep263_coding_cookie_is_honored

> A source file declaring a non-UTF-8 encoding is decoded correctly.

```python
def test_pep263_coding_cookie_is_honored(tmp_path: Path) -> None:
```

## test_module_docstring_is_attached

> A module docstring is stored on the module model.

```python
def test_module_docstring_is_attached(tmp_path: Path) -> None:
```

## test_docstrings_are_stripped_of_surrounding_whitespace

> Collected docstrings carry no leading or trailing whitespace.

```python
def test_docstrings_are_stripped_of_surrounding_whitespace(tmp_path: Path) -> None:
```

## test_whitespace_only_docstring_counts_as_undocumented

> A docstring holding only whitespace is stored as None.

```python
def test_whitespace_only_docstring_counts_as_undocumented(tmp_path: Path) -> None:
```

## test_module_without_docstring_has_none

> A module without a docstring yields a model without one.

```python
def test_module_without_docstring_has_none(tmp_path: Path) -> None:
```

## test_file_without_definitions_yields_module_without_members

> An empty file or a file without definitions yields a bare module model.

```python
@pytest.mark.parametrize("source", ["", "x = 1\n"])
def test_file_without_definitions_yields_module_without_members(tmp_path: Path, source: str) -> None:
```

## test_top_level_members_keep_source_order_with_signatures

> Top-level definitions yield models in source order with signatures.

```python
def test_top_level_members_keep_source_order_with_signatures(tmp_path: Path) -> None:
```

## test_signature_covers_all_parameter_kinds

> A signature keeps every parameter kind.

```python
def test_signature_covers_all_parameter_kinds(tmp_path: Path) -> None:
```

## test_class_signature_includes_bases_and_keywords

> A class signature keeps its bases and keyword arguments such as metaclass.

```python
def test_class_signature_includes_bases_and_keywords(tmp_path: Path) -> None:
```

## test_class_members_keep_source_order

> Methods and nested classes yield member models in source order.

```python
def test_class_members_keep_source_order(tmp_path: Path) -> None:
```

## test_private_members_are_included

> Underscore-prefixed members appear in the model.

```python
def test_private_members_are_included(tmp_path: Path) -> None:
```

## test_decorators_are_stored_verbatim_in_source_order

> Decorators are stored as written, in source order.

```python
def test_decorators_are_stored_verbatim_in_source_order(tmp_path: Path) -> None:
```

## test_function_local_definitions_are_skipped

> Definitions inside a function body are not collected.

```python
def test_function_local_definitions_are_skipped(tmp_path: Path) -> None:
```

## test_attribute_style_string_literals_are_ignored

> A string literal after an assignment is not treated as a docstring.

```python
def test_attribute_style_string_literals_are_ignored(tmp_path: Path) -> None:
```

## test_skip_listed_directories_are_skipped

> Source files under skipped or hidden directories are not collected.

```python
@pytest.mark.parametrize(
    "directory",
    ["__pycache__", "venv", ".venv", "build", "dist", "node_modules", ".hidden"],
)
def test_skip_listed_directories_are_skipped(tmp_path: Path, directory: str) -> None:
```

## test_excluded_directories_merge_with_the_builtin_skip_list

> Extra excluded names skip at walk time and the built-ins stay skipped.

```python
def test_excluded_directories_merge_with_the_builtin_skip_list(tmp_path: Path) -> None:
```

## test_exclude_defaults_keep_existing_calls_unchanged

> Without `exclude`, every non-hidden directory still gets scanned.

```python
def test_exclude_defaults_keep_existing_calls_unchanged(tmp_path: Path) -> None:
```

## test_file_reachable_through_overlapping_roots_is_collected_once

> A file reachable through two roots yields one model.

```python
def test_file_reachable_through_overlapping_roots_is_collected_once(tmp_path: Path) -> None:
```

## test_missing_root_raises_error_naming_the_root

> A root that does not exist raises a missing-root error naming the root.

```python
def test_missing_root_raises_error_naming_the_root(tmp_path: Path) -> None:
```

## test_syntax_error_raises_parse_error_with_path_and_message

> A syntax error raises a parse error carrying path and message.

```python
def test_syntax_error_raises_parse_error_with_path_and_message(tmp_path: Path) -> None:
```

## test_signature_falls_back_when_unparse_is_malformed

> A malformed unparsed definition falls back to manual reconstruction.

```python
def test_signature_falls_back_when_unparse_is_malformed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
```
