# tests/test_config.py

> Tests for config resolution: defaults, `[tool.repotoc]`, and overlays.

## test_load_config_defaults_when_no_pyproject_exists

> A directory without a pyproject file yields the default config.

```python
def test_load_config_defaults_when_no_pyproject_exists(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
```

## test_load_config_defaults_when_the_section_is_missing

> A pyproject file without a `[tool.repotoc]` section yields defaults.

```python
def test_load_config_defaults_when_the_section_is_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
```

## test_load_config_defaults_when_tool_is_not_a_table

> A pyproject file whose `tool` key is not a table yields defaults.

```python
def test_load_config_defaults_when_tool_is_not_a_table(tmp_path: Path) -> None:
```

## test_load_config_reads_every_key

> Every `[tool.repotoc]` key loads into the matching config field.

```python
def test_load_config_reads_every_key(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
```

## test_load_config_coerces_a_bare_toc_depth_to_a_one_element_tuple

> A bare integer `toc_max_depths` loads as a one-element tuple.

```python
def test_load_config_coerces_a_bare_toc_depth_to_a_one_element_tuple(tmp_path: Path) -> None:
```

## test_load_config_fails_on_invalid_toml_naming_the_file

> Invalid TOML fails naming the pyproject path.

```python
def test_load_config_fails_on_invalid_toml_naming_the_file(tmp_path: Path) -> None:
```

## test_load_config_fails_when_the_section_is_not_a_table

> A scalar `tool.repotoc` value fails naming the section.

```python
def test_load_config_fails_when_the_section_is_not_a_table(tmp_path: Path) -> None:
```

## test_load_config_fails_naming_the_offending_key

> A wrong-typed, rejected, or unknown value fails naming its key.

```python
@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("sources", 5),
        ("sources", ["src", 1]),
        ("output", 1),
        ("output", ["docs"]),
        ("file_member_depth", "2"),
        ("file_member_depth", True),
        ("file_member_depth", 0),
        ("file_include_privates", "yes"),
        ("file_include_signatures", 1),
        ("toc_max_depths", "6"),
        ("toc_max_depths", [6, "4"]),
        ("toc_max_depths", []),
        ("toc_max_depths", [6, 0]),
        ("toc_max_depths", True),
        ("exclude", "vendor"),
        ("exclude", [1]),
        ("unknown_key", 1),
    ],
)
def test_load_config_fails_naming_the_offending_key(tmp_path: Path, key: str, value: object) -> None:
```

## test_load_config_error_message_describes_the_value

> The error message describes the offending value.

```python
@pytest.mark.parametrize(
    ("key", "value", "fragment"),
    [
        ("sources", 5, "expected a list of strings"),
        ("file_member_depth", 0, "must be positive"),
        ("file_member_depth", "2", "expected an integer"),
        ("toc_max_depths", [], "must be non-empty and positive"),
        ("toc_max_depths", [6, 0], "must be non-empty and positive"),
        ("toc_max_depths", "6", "expected an integer or a list of integers"),
        ("toc_max_depths", [6, "4"], "expected a list of integers"),
    ],
)
def test_load_config_error_message_describes_the_value(tmp_path: Path, key: str, value: object, fragment: str) -> None:
```

## test_render_config_carries_the_presentation_settings

> `render_config` returns the matching `RenderConfig`.

```python
def test_render_config_carries_the_presentation_settings() -> None:
```

## test_merge_lets_set_values_win_and_unset_values_fall_through

> Set override fields win; unset fields keep the base values.

```python
def test_merge_lets_set_values_win_and_unset_values_fall_through() -> None:
```

## test_merge_keeps_the_base_when_no_override_is_set

> An all-unset overlay leaves the base config unchanged.

```python
def test_merge_keeps_the_base_when_no_override_is_set() -> None:
```

## test_merge_replaces_sources_instead_of_merging_them

> Overriding sources drops the base sources entirely.

```python
def test_merge_replaces_sources_instead_of_merging_them() -> None:
```
