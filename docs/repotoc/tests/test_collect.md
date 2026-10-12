# `tests/test_collect.py`

> Tests for the collection layer.

## `def test_collect_returns_module_models_ordered_by_path(tmp_path: Path) -> None:`

> Every Python file under a root yields a model, ordered by path.

---

## `def test_files_order_by_numeric_value(tmp_path: Path) -> None:`

> Digit runs in paths sort by value, so b2 precedes b10.

---

## `def test_pep263_coding_cookie_is_honored(tmp_path: Path) -> None:`

> A source file declaring a non-UTF-8 encoding is decoded correctly.

---

## `def test_module_docstring_is_attached(tmp_path: Path) -> None:`

> A module docstring is stored on the module model.

---

## `def test_docstrings_are_stripped_of_surrounding_whitespace(tmp_path: Path) -> None:`

> Collected docstrings carry no leading or trailing whitespace.

---

## `def test_whitespace_only_docstring_counts_as_undocumented(tmp_path: Path) -> None:`

> A docstring holding only whitespace is stored as None.

---

## `def test_module_without_docstring_has_none(tmp_path: Path) -> None:`

> A module without a docstring yields a model without one.

---

## `def test_file_without_definitions_yields_module_without_members(tmp_path: Path, source: str) -> None:`

> An empty file or a file without definitions yields a bare module model.

---

## `def test_top_level_members_keep_source_order_with_signatures(tmp_path: Path) -> None:`

> Top-level definitions yield models in source order with signatures.

---

## `def test_signature_covers_all_parameter_kinds(tmp_path: Path) -> None:`

> A signature keeps every parameter kind.

---

## `def test_class_signature_includes_bases_and_keywords(tmp_path: Path) -> None:`

> A class signature keeps its bases and keyword arguments such as metaclass.

---

## `def test_class_members_keep_source_order(tmp_path: Path) -> None:`

> Methods and nested classes yield member models in source order.

---

## `def test_private_members_are_included(tmp_path: Path) -> None:`

> Underscore-prefixed members appear in the model.

---

## `def test_decorators_are_stored_verbatim_in_source_order(tmp_path: Path) -> None:`

> Decorators are stored as written, in source order.

---

## `def test_function_local_definitions_are_skipped(tmp_path: Path) -> None:`

> Definitions inside a function body are not collected.

---

## `def test_attribute_style_string_literals_are_ignored(tmp_path: Path) -> None:`

> A string literal after an assignment is not treated as a docstring.

---

## `def test_skip_listed_directories_are_skipped(tmp_path: Path, directory: str) -> None:`

> Source files under skipped or hidden directories are not collected.

---

## `def test_excluded_directories_merge_with_the_builtin_skip_list(tmp_path: Path) -> None:`

> Extra excluded names skip at walk time and the built-ins stay skipped.

---

## `def test_exclude_defaults_keep_existing_calls_unchanged(tmp_path: Path) -> None:`

> Without `exclude`, every non-hidden directory still gets scanned.

---

## `def test_file_reachable_through_overlapping_roots_is_collected_once(tmp_path: Path) -> None:`

> A file reachable through two roots yields one model.

---

## `def test_missing_root_raises_error_naming_the_root(tmp_path: Path) -> None:`

> A root that does not exist raises a missing-root error naming the root.

---

## `def test_syntax_error_raises_parse_error_with_path_and_message(tmp_path: Path) -> None:`

> A syntax error raises a parse error carrying path and message.

---

## `def test_signature_falls_back_when_unparse_is_malformed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:`

> A malformed unparsed definition falls back to manual reconstruction.
