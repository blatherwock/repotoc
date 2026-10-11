# src/repotoc/cli.py

> The `repotoc` command line interface: flags mapped onto the shared config.

## main

> Run the CLI, raising SystemExit with the run's exit code.
>
> Exit codes: 0 on success and on fresh checks; 1 on stale checks; 2 on
> usage, config, filesystem, and parse errors.
>
> Args:
>     argv: The command line arguments; None reads `sys.argv`.

```python
def main(argv: Sequence[str] | None=None) -> None:
```
