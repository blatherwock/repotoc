# `src/repotoc/collect.py`

> Collection layer: turn source roots into module models via static AST parsing.

## `def collect(roots: Iterable[str | Path], exclude: Iterable[str]=()) -> list[Module]:`

> Collect module models from every Python file under the given roots.
>
> Args:
>     roots: Source root directories to scan.
>     exclude: Extra directory names to skip, merged with the built-in skip
>         list at walk time.
>
> Returns:
>     The module models, ordered by source path.
>
> Raises:
>     MissingRootError: A root does not exist.
>     ParseError: A source file has a syntax error.
