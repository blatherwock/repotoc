"""Tests for the Markdown emission helpers."""

from repotoc.render.markdown import (
    blockquote,
    heading,
    horizontal_rule,
    link,
    list_item,
)


def test_heading_prefaces_the_text_with_the_level() -> None:
    """A heading line carries one hash per level, then the text."""
    assert heading("Title", 1) == "# Title"
    assert heading("Member", 4) == "#### Member"


def test_blockquote_quotes_every_line() -> None:
    """Each source line becomes one blockquote line; blank lines bare quotes."""
    assert blockquote("First.\n\nSecond.") == "> First.\n>\n> Second."


def test_horizontal_rule_sits_at_the_left_margin() -> None:
    """A thematic break is three dashes on its own line."""
    assert horizontal_rule() == "---"


def test_link_wraps_the_display_in_the_target() -> None:
    """A link renders the display text pointing at the target."""
    assert link("`mod.py`", "mod.md") == "[`mod.py`](mod.md)"


def test_list_item_indents_one_step_per_level() -> None:
    """A list line indents two spaces per level before the bullet."""
    assert list_item("file: a", 0) == "- file: a"
    assert list_item("file: a", 2) == "    - file: a"
