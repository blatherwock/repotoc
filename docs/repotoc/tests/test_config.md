# `tests/test_config.py`

> Tests for config resolution: defaults, `[tool.repotoc]`, and overlays.

## `def test_load_config_defaults_when_no_pyproject_exists(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:`

> A directory without a pyproject file yields the default config.

---

## `def test_load_config_defaults_when_the_section_is_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:`

> A pyproject file without a `[tool.repotoc]` section yields defaults.

---

## `def test_load_config_defaults_when_tool_is_not_a_table(tmp_path: Path) -> None:`

> A pyproject file whose `tool` key is not a table yields defaults.

---

## `def test_load_config_reads_every_key(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:`

> Every `[tool.repotoc]` key loads into the matching config field.

---

## `def test_load_config_coerces_a_bare_toc_depth_to_a_one_element_tuple(tmp_path: Path) -> None:`

> A bare integer `toc_max_depths` loads as a one-element tuple.

---

## `def test_load_config_fails_on_invalid_toml_naming_the_file(tmp_path: Path) -> None:`

> Invalid TOML fails naming the pyproject path.

---

## `def test_load_config_fails_when_the_section_is_not_a_table(tmp_path: Path) -> None:`

> A scalar `tool.repotoc` value fails naming the section.

---

## `def test_load_config_fails_naming_the_offending_key(tmp_path: Path, key: str, value: object) -> None:`

> A wrong-typed, rejected, or unknown value fails naming its key.

---

## `def test_load_config_error_message_describes_the_value(tmp_path: Path, key: str, value: object, fragment: str) -> None:`

> The error message describes the offending value.

---

## `def test_render_config_carries_the_presentation_settings() -> None:`

> `render_config` returns the matching `RenderConfig`.

---

## `def test_merge_lets_set_values_win_and_unset_values_fall_through() -> None:`

> Set override fields win; unset fields keep the base values.

---

## `def test_merge_keeps_the_base_when_no_override_is_set() -> None:`

> An all-unset overlay leaves the base config unchanged.

---

## `def test_merge_replaces_sources_instead_of_merging_them() -> None:`

> Overriding sources drops the base sources entirely.
