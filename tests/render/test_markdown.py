"""Tests for the Markdown emission helpers."""

from repodoc.render.markdown import blockquote, code_block, heading, link, list_item


def test_heading_prefaces_the_text_with_the_level() -> None:
    """A heading line carries one hash per level, then the text."""
    assert heading("Title", 1) == "# Title"
    assert heading("Member", 4) == "#### Member"


def test_blockquote_quotes_every_line() -> None:
    """Each source line becomes one blockquote line; blank lines bare quotes."""
    assert blockquote("First.\n\nSecond.") == "> First.\n>\n> Second."


def test_code_block_fences_the_text_as_python() -> None:
    """A code block opens and closes with a three-backtick fence."""
    assert code_block("def run():") == "```python\ndef run():\n```"


def test_code_block_fence_grows_past_backtick_runs() -> None:
    """The fence grows beyond the longest backtick run in the text."""
    assert code_block("tag('```code```')") == "````python\ntag('```code```')\n````"


def test_link_wraps_the_display_in_the_target() -> None:
    """A link renders the display text pointing at the target."""
    assert link("`mod.py`", "mod.md") == "[`mod.py`](mod.md)"


def test_list_item_indents_one_step_per_level() -> None:
    """A list line indents two spaces per level before the bullet."""
    assert list_item("file: a", 0) == "- file: a"
    assert list_item("file: a", 2) == "    - file: a"
