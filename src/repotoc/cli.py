"""The `repotoc` command line interface: flags mapped onto the shared config."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from repotoc.collect import collect
from repotoc.config import PartialConfig, load_config, merge
from repotoc.errors import CollectionError, ConfigError, GenerationError
from repotoc.generate import generate
from repotoc.render import render

if TYPE_CHECKING:
    from collections.abc import Sequence

    from repotoc.config import Config
    from repotoc.models import Module


def main(argv: Sequence[str] | None = None) -> None:
    """Run the CLI, raising SystemExit with the run's exit code.

    Exit codes: 0 on success and on fresh checks; 1 on stale checks; 2 on
    usage, config, filesystem, and parse errors.

    Args:
        argv: The command line arguments; None reads `sys.argv`.
    """
    raise SystemExit(_run(argv))


def _run(argv: Sequence[str] | None) -> int:
    """Parse the arguments, resolve the config, and execute the run."""
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        config = merge(load_config(), _partial(args))
        if not config.sources:
            parser.error("no source directories given and none configured")
        modules = collect(config.sources, config.exclude)
        if args.check:
            return _report_stale(_check(modules, config))
        generate(modules, config.render_config())
        return 0
    except (ConfigError, CollectionError, GenerationError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


def _build_parser() -> argparse.ArgumentParser:
    """Build the argument parser, one flag per config key."""
    parser = argparse.ArgumentParser(
        prog="repotoc",
        description="Regenerate the repotoc Markdown artifact.",
    )
    parser.add_argument(
        "sources",
        nargs="*",
        metavar="SOURCE",
        help="source root directories to scan; replaces the config sources",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="DIR",
        help="output directory (default: docs/repotoc)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare the artifact without writing; exit 1 when stale",
    )
    parser.add_argument(
        "--file-member-depth",
        type=_positive_int,
        metavar="N",
        help="outline depth in doc files (default: unlimited)",
    )
    parser.add_argument(
        "--file-include-privates",
        action=argparse.BooleanOptionalAction,
        help="render underscore-prefixed members (default: no)",
    )
    parser.add_argument(
        "--file-include-signatures",
        action=argparse.BooleanOptionalAction,
        help="render member source blocks (default: yes)",
    )
    parser.add_argument(
        "--toc-max-depths",
        nargs="+",
        type=_positive_int,
        metavar="DEPTH",
        help="per-level nested-list depths for indexes (default: 6)",
    )
    parser.add_argument(
        "--exclude",
        nargs="+",
        metavar="DIR",
        help="extra directory names to skip, replacing the config value",
    )
    return parser


def _positive_int(text: str) -> int:
    """Parse a positive integer argument."""
    try:
        value = int(text)
    except ValueError:
        message = f"expected an integer, got {text!r}"
        raise argparse.ArgumentTypeError(message) from None
    if value < 1:
        message = f"must be positive, got {value}"
        raise argparse.ArgumentTypeError(message)
    return value


def _partial(args: argparse.Namespace) -> PartialConfig:
    """Map the parsed arguments onto the CLI config layer.

    An absent flag is None, meaning the layer leaves the key to the config
    file; absent list flags are empty lists, normalized to None the same way.
    """
    return PartialConfig(
        sources=tuple(args.sources) or None,
        output=args.output,
        file_member_depth=args.file_member_depth,
        file_include_privates=args.file_include_privates,
        file_include_signatures=args.file_include_signatures,
        toc_max_depths=tuple(args.toc_max_depths) if args.toc_max_depths else None,
        exclude=tuple(args.exclude) if args.exclude else None,
    )


def _check(modules: list[Module], config: Config) -> list[str]:
    """Compare the rendered artifact against the output directory.

    Returns:
        The stale entries, one line each: `missing:` for rendered files the
        directory lacks, `differing:` for files whose text differs, and
        `extra:` for `.md` files the current run does not produce. Sorted by
        path.
    """
    files = render(modules, config.render_config())
    output = Path(config.output)
    stale: list[tuple[str, str]] = []
    for path, text in sorted(files.items()):
        on_disk = output / path
        if not on_disk.is_file():
            stale.append((path, "missing"))
        elif on_disk.read_bytes() != text.encode("utf-8"):
            stale.append((path, "differing"))
    if output.is_dir():
        for path in sorted(output.rglob("*.md")):
            relative = path.relative_to(output).as_posix()
            if relative not in files:
                stale.append((relative, "extra"))
    return [f"{kind}: {path}" for path, kind in sorted(stale)]


def _report_stale(stale: list[str]) -> int:
    """Print the stale entries and return the check exit code."""
    for line in stale:
        print(line)
    return 1 if stale else 0
