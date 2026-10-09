"""Markdown emission helpers: headings, fences, blockquotes, link and list lines."""

from __future__ import annotations

import re

# Shortest fence Markdown accepts.
_MIN_FENCE = 3

# Matches runs of backticks inside fenced code text.
_BACKTICK_RUN = re.compile(r"`+")


def heading(text: str, level: int) -> str:
    """Return the text as a Markdown heading of the given level."""
    return f"{'#' * level} {text}"


def blockquote(text: str) -> str:
    """Return the text as a Markdown blockquote, one quote line per source line."""
    return "\n".join(_quote_line(line) for line in text.split("\n"))


def _quote_line(line: str) -> str:
    """Return one docstring line as a blockquote line."""
    return ">" if line == "" else f"> {line}"


def code_block(text: str) -> str:
    """Return the text as a fenced Python block at the left margin.

    The fence grows past the longest backtick run in the text so that backticks
    inside decorator string literals cannot close the block.
    """
    longest = max((len(run) for run in _BACKTICK_RUN.findall(text)), default=2)
    fence = "`" * max(_MIN_FENCE, longest + 1)
    return "\n".join([f"{fence}python", text, fence])


def link(text: str, target: str) -> str:
    """Return a Markdown link carrying the text as its display."""
    return f"[{text}]({target})"


def list_item(text: str, level: int) -> str:
    """Return the text as a bullet line, indented one step per list level."""
    return f"{'  ' * level}- {text}"
