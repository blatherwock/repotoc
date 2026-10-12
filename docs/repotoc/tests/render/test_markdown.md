# `tests/render/test_markdown.py`

> Tests for the Markdown emission helpers.

## `def test_heading_prefaces_the_text_with_the_level() -> None:`

> A heading line carries one hash per level, then the text.

---

## `def test_blockquote_quotes_every_line() -> None:`

> Each source line becomes one blockquote line; blank lines bare quotes.

---

## `def test_horizontal_rule_sits_at_the_left_margin() -> None:`

> A thematic break is three dashes on its own line.

---

## `def test_link_wraps_the_display_in_the_target() -> None:`

> A link renders the display text pointing at the target.

---

## `def test_list_item_indents_one_step_per_level() -> None:`

> A list line indents two spaces per level before the bullet.
