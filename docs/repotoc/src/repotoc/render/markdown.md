# `src/repotoc/render/markdown.py`

> Markdown emission helpers: headings, blockquotes, rules, link and list lines.

## `def heading(text: str, level: int) -> str:`

> Return the text as a Markdown heading of the given level.

---

## `def blockquote(text: str) -> str:`

> Return the text as a Markdown blockquote, one quote line per source line.

---

## `def horizontal_rule() -> str:`

> Return a thematic break at the left margin.

---

## `def link(text: str, target: str) -> str:`

> Return a Markdown link carrying the text as its display.

---

## `def list_item(text: str, level: int) -> str:`

> Return the text as a bullet line, indented one step per list level.
