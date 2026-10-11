# src/repotoc/render/__init__.py

> Rendering layer: turn module models into Markdown doc files and indexes.

## render

> Render the module models into the artifact file set.
>
> Args:
>     modules: The module models, in collection order.
>     config: The presentation settings.
>
> Returns:
>     A mapping from output-relative POSIX paths to file texts: one doc file
>     per module except memberless `__init__.py` files, and one index per
>     directory holding doc files, child indexes, or an `__init__.py`
>     docstring. Deterministic for a given input.

```python
def render(modules: list[Module], config: RenderConfig) -> dict[str, str]:
```
