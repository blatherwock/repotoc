# src/repotoc/render/markdown.py

> Markdown emission helpers: headings, fences, blockquotes, link and list lines.

## heading

> Return the text as a Markdown heading of the given level.

```python
def heading(text: str, level: int) -> str:
```

## blockquote

> Return the text as a Markdown blockquote, one quote line per source line.

```python
def blockquote(text: str) -> str:
```

## code_block

> Return the text as a fenced Python block at the left margin.
>
> The fence grows past the longest backtick run in the text so that backticks
> inside decorator string literals cannot close the block.

```python
def code_block(text: str) -> str:
```

## link

> Return a Markdown link carrying the text as its display.

```python
def link(text: str, target: str) -> str:
```

## list_item

> Return the text as a bullet line, indented one step per list level.

```python
def list_item(text: str, level: int) -> str:
```
