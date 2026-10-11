"""Config resolution: defaults, the `[tool.repotoc]` section, and CLI overlays."""

from __future__ import annotations

import tomllib
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import TYPE_CHECKING

from repotoc.errors import ConfigError
from repotoc.filters import RenderConfig

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping
    from typing import NoReturn


@dataclass(frozen=True)
class Config:
    """The effective settings for one run.

    Every field is a `[tool.repotoc]` key and a CLI flag. The presentation
    fields mirror `RenderConfig`; `sources` and `exclude` drive collection.

    Attributes:
        sources: The source root directories to scan.
        output: The output directory for the artifact.
        file_member_depth: The outline depth in doc files; None is unlimited.
        file_include_privates: Whether underscore-prefixed members render.
        file_include_signatures: Whether member source blocks render.
        toc_max_depths: Per-level nested-list depths for indexes.
        exclude: Extra directory names collection never scans.
    """

    sources: tuple[str, ...] = ()
    output: str = "docs/repotoc"
    file_member_depth: int | None = None
    file_include_privates: bool = False
    file_include_signatures: bool = True
    toc_max_depths: tuple[int, ...] = (6,)
    exclude: tuple[str, ...] = ()

    def render_config(self) -> RenderConfig:
        """Return the presentation settings for the render layer."""
        return RenderConfig(
            output=self.output,
            file_member_depth=self.file_member_depth,
            file_include_privates=self.file_include_privates,
            file_include_signatures=self.file_include_signatures,
            toc_max_depths=self.toc_max_depths,
        )


@dataclass(frozen=True)
class PartialConfig:
    """Config values one layer sets; None means the layer leaves the key unset.

    Attributes:
        sources: The source root directories, or None.
        output: The output directory, or None.
        file_member_depth: The outline depth, or None.
        file_include_privates: The private-member switch, or None.
        file_include_signatures: The signature switch, or None.
        toc_max_depths: The per-level depths, or None.
        exclude: The extra skipped directory names, or None.
    """

    sources: tuple[str, ...] | None = None
    output: str | None = None
    file_member_depth: int | None = None
    file_include_privates: bool | None = None
    file_include_signatures: bool | None = None
    toc_max_depths: tuple[int, ...] | None = None
    exclude: tuple[str, ...] | None = None


def load_config(path: Path | None = None) -> Config:
    """Load config from the `[tool.repotoc]` section of a pyproject file.

    Args:
        path: The pyproject file to read; None reads `pyproject.toml` in the
            current directory.

    Returns:
        The config, with defaults for every key the file leaves unset.

    Raises:
        ConfigError: The file is invalid TOML, the section is not a table, or
            a key holds a value of the wrong type or one `RenderConfig`
            rejects; the message names the offending key.
    """
    pyproject = path if path is not None else Path("pyproject.toml")
    if not pyproject.is_file():
        return Config()
    try:
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        raise ConfigError(str(pyproject), f"invalid TOML: {error}") from error
    tool = data.get("tool")
    if not isinstance(tool, dict):
        return Config()
    section = tool.get("repotoc")
    if section is None:
        return Config()
    if not isinstance(section, dict):
        _expected("[tool.repotoc]", "a table", section)
    return _config_from_section(section)


def merge(base: Config, overrides: PartialConfig) -> Config:
    """Overlay one layer's set values onto a base config.

    Keys the overriding layer leaves unset keep the base value; keys it sets
    win. Set list values (`sources`, `exclude`) replace the base values, they
    do not merge with them.

    Args:
        base: The lower-precedence config.
        overrides: The higher-precedence values, unset fields None.

    Returns:
        The effective config.
    """
    changes = {
        name: value for name, value in asdict(overrides).items() if value is not None
    }
    return replace(base, **changes)


def _config_from_section(section: Mapping[str, object]) -> Config:
    """Build a config from a `[tool.repotoc]` section, validating every key."""
    config = Config()
    for key, value in section.items():
        parser = _PARSERS.get(key)
        if parser is None:
            message = "unknown config key"
            raise ConfigError(key, message)
        config = replace(config, **{key: parser(key, value)})
    return config


def _expected(key: str, description: str, value: object) -> NoReturn:
    """Raise a config error naming what the key expected and the value's type."""
    message = f"expected {description}, got {type(value).__name__}"
    raise ConfigError(key, message)


def _parse_string_tuple(key: str, value: object) -> tuple[str, ...]:
    """Parse a list of strings into a tuple: the source roots or excluded names."""
    if not isinstance(value, list) or any(
        isinstance(item, bool) or not isinstance(item, str) for item in value
    ):
        _expected(key, "a list of strings", value)
    return tuple(value)


def _parse_output(key: str, value: object) -> str:
    """Parse the output directory: a path string."""
    if not isinstance(value, str):
        _expected(key, "a string", value)
    return value


def _parse_bool(key: str, value: object) -> bool:
    """Parse a boolean switch."""
    if not isinstance(value, bool):
        _expected(key, "a boolean", value)
    return value


def _parse_member_depth(key: str, value: object) -> int:
    """Parse the doc-file outline depth: a positive integer."""
    if isinstance(value, bool) or not isinstance(value, int):
        _expected(key, "an integer", value)
    if value < 1:
        message = f"must be positive, got {value}"
        raise ConfigError(key, message)
    return value


def _parse_toc_depths(key: str, value: object) -> tuple[int, ...]:
    """Parse the per-level index depths: an integer or a list of integers.

    TOML has no tuples, so a bare integer coerces to a one-element tuple, the
    form `RenderConfig` validates.
    """
    if isinstance(value, bool):
        _expected(key, "an integer or a list of integers", value)
    if isinstance(value, int):
        depths = (value,)
    elif isinstance(value, list):
        if any(
            isinstance(depth, bool) or not isinstance(depth, int) for depth in value
        ):
            _expected(key, "a list of integers", value)
        depths = tuple(value)
    else:
        _expected(key, "an integer or a list of integers", value)
    if not depths or any(depth < 1 for depth in depths):
        message = f"must be non-empty and positive, got {list(depths)}"
        raise ConfigError(key, message)
    return depths


_PARSERS: dict[str, Callable[[str, object], object]] = {
    "sources": _parse_string_tuple,
    "output": _parse_output,
    "exclude": _parse_string_tuple,
    "file_include_privates": _parse_bool,
    "file_include_signatures": _parse_bool,
    "file_member_depth": _parse_member_depth,
    "toc_max_depths": _parse_toc_depths,
}
