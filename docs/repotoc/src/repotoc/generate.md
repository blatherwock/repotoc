# `src/repotoc/generate.py`

> Generation layer: write and prune the tool-owned artifact output directory.

## `class GenerationReport:`

> The outcome of one generation run.
>
> Attributes:
>     written: The output-relative POSIX paths of the files the run wrote.
>     deleted: The output-relative POSIX paths of the stale Markdown files
>         the run deleted.

---

## `def generate(modules: list[Module], config: RenderConfig) -> GenerationReport:`

> Generate the artifact into the configured output directory.
>
> The output directory is tool-owned: the run writes the rendered file set,
> creating the directory when missing, and deletes `.md` files under it that
> the current run does not produce. Files with other suffixes stay.
>
> Args:
>     modules: The module models, in collection order.
>     config: The presentation settings.
>
> Returns:
>     A report of the written and deleted paths, both sorted.
>
> Raises:
>     GenerationError: The output directory cannot be created, written, or
>         pruned.
