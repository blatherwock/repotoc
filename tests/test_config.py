"""Tests for config resolution: defaults, `[tool.repodoc]`, and overlays."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from repodoc.config import Config, PartialConfig, load_config, merge
from repodoc.errors import ConfigError
from repodoc.filters import RenderConfig

if TYPE_CHECKING:
    from pathlib import Path


def _write_pyproject(tmp_path: Path, text: str) -> Path:
    """Write a pyproject file in the directory and return its path."""
    path = tmp_path / "pyproject.toml"
    path.write_text(text, encoding="utf-8")
    return path


def _toml(value: object) -> str:
    """Format one Python value as TOML source."""
    if isinstance(value, bool):
        return "true" if value else "false"
    return repr(value)


def test_load_config_defaults_when_no_pyproject_exists(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A directory without a pyproject file yields the default config."""
    monkeypatch.chdir(tmp_path)

    config = load_config()

    assert config == Config()


def test_load_config_defaults_when_the_section_is_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A pyproject file without a `[tool.repodoc]` section yields defaults."""
    monkeypatch.chdir(tmp_path)
    _write_pyproject(tmp_path, "[tool.ruff]\nline-length = 88\n")

    config = load_config()

    assert config == Config()


def test_load_config_defaults_when_tool_is_not_a_table(
    tmp_path: Path,
) -> None:
    """A pyproject file whose `tool` key is not a table yields defaults."""
    pyproject = _write_pyproject(tmp_path, "tool = 5\n")

    config = load_config(pyproject)

    assert config == Config()


def test_load_config_reads_every_key(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Every `[tool.repodoc]` key loads into the matching config field."""
    monkeypatch.chdir(tmp_path)
    _write_pyproject(
        tmp_path,
        """
[tool.repodoc]
sources = ["src", "scripts"]
output = "docs/api"
file_member_depth = 2
file_include_privates = true
file_include_signatures = false
toc_max_depths = [6, 4, 2]
exclude = ["generated", "vendor"]
""",
    )

    config = load_config()

    assert config == Config(
        sources=("src", "scripts"),
        output="docs/api",
        file_member_depth=2,
        file_include_privates=True,
        file_include_signatures=False,
        toc_max_depths=(6, 4, 2),
        exclude=("generated", "vendor"),
    )


def test_load_config_coerces_a_bare_toc_depth_to_a_one_element_tuple(
    tmp_path: Path,
) -> None:
    """A bare integer `toc_max_depths` loads as a one-element tuple."""
    pyproject = _write_pyproject(
        tmp_path, "[tool.repodoc]\ntoc_max_depths = 3\nsources = []\n"
    )

    config = load_config(pyproject)

    assert config.toc_max_depths == (3,)


def test_load_config_fails_on_invalid_toml_naming_the_file(tmp_path: Path) -> None:
    """Invalid TOML fails naming the pyproject path."""
    pyproject = _write_pyproject(tmp_path, "[tool.repodoc\n")

    with pytest.raises(ConfigError) as info:
        load_config(pyproject)

    assert info.value.key == str(pyproject)


def test_load_config_fails_when_the_section_is_not_a_table(tmp_path: Path) -> None:
    """A scalar `tool.repodoc` value fails naming the section."""
    pyproject = _write_pyproject(tmp_path, "[tool]\nrepodoc = 5\n")

    with pytest.raises(ConfigError) as info:
        load_config(pyproject)

    assert info.value.key == "[tool.repodoc]"


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
def test_load_config_fails_naming_the_offending_key(
    tmp_path: Path, key: str, value: object
) -> None:
    """A wrong-typed, rejected, or unknown value fails naming its key."""
    lines = ["[tool.repodoc]", f"{key} = {_toml(value)}"]
    pyproject = _write_pyproject(tmp_path, "\n".join(lines) + "\n")

    with pytest.raises(ConfigError) as info:
        load_config(pyproject)

    assert info.value.key == key


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
def test_load_config_error_message_describes_the_value(
    tmp_path: Path, key: str, value: object, fragment: str
) -> None:
    """The error message describes the offending value."""
    pyproject = _write_pyproject(tmp_path, f"[tool.repodoc]\n{key} = {value!r}\n")

    with pytest.raises(ConfigError) as info:
        load_config(pyproject)

    assert fragment in info.value.message


def test_render_config_carries_the_presentation_settings() -> None:
    """`render_config` returns the matching `RenderConfig`."""
    config = Config(
        sources=("src",),
        output="docs/api",
        file_member_depth=2,
        file_include_privates=True,
        file_include_signatures=False,
        toc_max_depths=(6, 4),
        exclude=("vendor",),
    )

    render_config = config.render_config()

    assert render_config == RenderConfig(
        output="docs/api",
        file_member_depth=2,
        file_include_privates=True,
        file_include_signatures=False,
        toc_max_depths=(6, 4),
    )


def test_merge_lets_set_values_win_and_unset_values_fall_through() -> None:
    """Set override fields win; unset fields keep the base values."""
    base = Config(
        sources=("base-src",),
        output="base-out",
        file_member_depth=2,
        file_include_privates=True,
        file_include_signatures=False,
        toc_max_depths=(6, 4),
        exclude=("vendor",),
    )
    overrides = PartialConfig(
        sources=("cli-src",),
        output="cli-out",
        file_member_depth=1,
        file_include_privates=False,
        file_include_signatures=True,
        toc_max_depths=(3,),
        exclude=("gen",),
    )

    merged = merge(base, overrides)

    assert merged == Config(
        sources=("cli-src",),
        output="cli-out",
        file_member_depth=1,
        file_include_privates=False,
        file_include_signatures=True,
        toc_max_depths=(3,),
        exclude=("gen",),
    )


def test_merge_keeps_the_base_when_no_override_is_set() -> None:
    """An all-unset overlay leaves the base config unchanged."""
    base = Config(
        sources=("src",),
        output="out",
        file_member_depth=2,
        file_include_privates=True,
        file_include_signatures=False,
        toc_max_depths=(6, 4),
        exclude=("vendor",),
    )

    assert merge(base, PartialConfig()) == base


def test_merge_replaces_sources_instead_of_merging_them() -> None:
    """Overriding sources drops the base sources entirely."""
    base = Config(sources=("src", "tests"))
    overrides = PartialConfig(sources=("lib",))

    merged = merge(base, overrides)

    assert merged.sources == ("lib",)
