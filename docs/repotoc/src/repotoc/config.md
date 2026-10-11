# src/repotoc/config.py

> Config resolution: defaults, the `[tool.repotoc]` section, and CLI overlays.

## Config

> The effective settings for one run.
>
> Every field is a `[tool.repotoc]` key and a CLI flag. The presentation
> fields mirror `RenderConfig`; `sources` and `exclude` drive collection.
>
> Attributes:
>     sources: The source root directories to scan.
>     output: The output directory for the artifact.
>     file_member_depth: The outline depth in doc files; None is unlimited.
>     file_include_privates: Whether underscore-prefixed members render.
>     file_include_signatures: Whether member source blocks render.
>     toc_max_depths: Per-level nested-list depths for indexes.
>     exclude: Extra directory names collection never scans.

```python
@dataclass(frozen=True)
class Config:
```

### render_config

> Return the presentation settings for the render layer.

```python
    def render_config(self) -> RenderConfig:
```

## PartialConfig

> Config values one layer sets; None means the layer leaves the key unset.
>
> Attributes:
>     sources: The source root directories, or None.
>     output: The output directory, or None.
>     file_member_depth: The outline depth, or None.
>     file_include_privates: The private-member switch, or None.
>     file_include_signatures: The signature switch, or None.
>     toc_max_depths: The per-level depths, or None.
>     exclude: The extra skipped directory names, or None.

```python
@dataclass(frozen=True)
class PartialConfig:
```

## load_config

> Load config from the `[tool.repotoc]` section of a pyproject file.
>
> Args:
>     path: The pyproject file to read; None reads `pyproject.toml` in the
>         current directory.
>
> Returns:
>     The config, with defaults for every key the file leaves unset.
>
> Raises:
>     ConfigError: The file is invalid TOML, the section is not a table, or
>         a key holds a value of the wrong type or one `RenderConfig`
>         rejects; the message names the offending key.

```python
def load_config(path: Path | None=None) -> Config:
```

## merge

> Overlay one layer's set values onto a base config.
>
> Keys the overriding layer leaves unset keep the base value; keys it sets
> win. Set list values (`sources`, `exclude`) replace the base values, they
> do not merge with them.
>
> Args:
>     base: The lower-precedence config.
>     overrides: The higher-precedence values, unset fields None.
>
> Returns:
>     The effective config.

```python
def merge(base: Config, overrides: PartialConfig) -> Config:
```
