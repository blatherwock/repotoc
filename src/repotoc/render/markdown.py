"""Markdown emission helpers: headings, blockquotes, rules, link and list lines."""

from __future__ import annotations


def heading(text: str, level: int) -> str:
    """Return the text as a Markdown heading of the given level."""
    return f"{'#' * level} {text}"


def blockquote(text: str) -> str:
    """Return the text as a Markdown blockquote, one quote line per source line."""
    return "\n".join(_quote_line(line) for line in text.split("\n"))


def _quote_line(line: str) -> str:
    """Return one docstring line as a blockquote line."""
    return ">" if line == "" else f"> {line}"


def horizontal_rule() -> str:
    """Return a thematic break at the left margin."""
    return "---"


def link(text: str, target: str) -> str:
    """Return a Markdown link carrying the text as its display."""
    return f"[{text}]({target})"


def list_item(text: str, level: int) -> str:
    """Return the text as a bullet line, indented one step per list level."""
    return f"{'  ' * level}- {text}"
