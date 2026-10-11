# tests/render/test_markdown.py

> Tests for the Markdown emission helpers.

## test_heading_prefaces_the_text_with_the_level

> A heading line carries one hash per level, then the text.

```python
def test_heading_prefaces_the_text_with_the_level() -> None:
```

## test_blockquote_quotes_every_line

> Each source line becomes one blockquote line; blank lines bare quotes.

```python
def test_blockquote_quotes_every_line() -> None:
```

## test_code_block_fences_the_text_as_python

> A code block opens and closes with a three-backtick fence.

```python
def test_code_block_fences_the_text_as_python() -> None:
```

## test_code_block_fence_grows_past_backtick_runs

> The fence grows beyond the longest backtick run in the text.

```python
def test_code_block_fence_grows_past_backtick_runs() -> None:
```

## test_link_wraps_the_display_in_the_target

> A link renders the display text pointing at the target.

```python
def test_link_wraps_the_display_in_the_target() -> None:
```

## test_list_item_indents_one_step_per_level

> A list line indents two spaces per level before the bullet.

```python
def test_list_item_indents_one_step_per_level() -> None:
```
