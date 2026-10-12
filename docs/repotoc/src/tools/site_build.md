# src/tools/site_build.py

> Refresh and gate the showcase site's example artifacts.
>
> `refresh` runs `repotoc` over the site fixture once per showcase
> variant, writing each run under `site/examples/generated/`, then
> embeds the variant outputs and the fixture source into marked blocks
> in `site/index.html`. `check` compares the same content without
> writing: it exits 0 when current, 1 when stale, and 2 on errors.

## SiteBuildError

> A failure refreshing or gating the site showcase blocks.

```python
class SiteBuildError(Exception):
```

## Variant

> One repotoc run in the showcase matrix.
>
> Attributes:
>     key: The variant directory under `generated/`, and the name
>         of its embed block in `index.html`.
>     kind: The panel the variant feeds: `doc` or `index`.
>     flags: The repotoc flags configuring the run.

```python
@dataclass(frozen=True)
class Variant:
```

## render_markdown

> Return the artifact's Markdown rendered as HTML.
>
> Covers the grammar the artifact emits: headings, blockquote
> docstrings, fenced code blocks, nested lists, and inline markup.
> Link targets resolve against `doc_dir`, the file's directory
> inside its variant, then gain `link_prefix` so they point at the
> published variant tree.

```python
def render_markdown(text: str, *, link_prefix: str='', doc_dir: str='') -> str:
```

## render_trees

> Return the source tree and the doc tree as aligned text blocks.
>
> Both trees list the source tree, with doc names substituted on
> the doc side. Directories named in `collapsed` (paths relative to
> the root) render as one line, and the file at `highlight` is
> wrapped in a mark on both sides.
>
> Raises:
>     SiteBuildError: A root is missing, or a source entry has no
>         doc entry.

```python
def render_trees(source_root: Path, doc_root: Path, collapsed: frozenset[str]=COLLAPSED, highlight: str=HIGHLIGHT) -> tuple[str, str]:
```

## collect_blocks

> Return every embed block's content, read from the variant outputs.
>
> Raises:
>     SiteBuildError: A variant's output file is missing, naming the
>         variant key, so the showcase can never point at a hole; or
>         the structure trees cannot be built.

```python
def collect_blocks(examples_dir: Path, variants: tuple[Variant, ...]) -> dict[str, str]:
```

## replace_blocks

> Return the page with each marked block's content replaced.
>
> Content outside the marker pairs is preserved verbatim.
>
> Raises:
>     SiteBuildError: A block has no marker pair in the page.

```python
def replace_blocks(html_text: str, blocks: dict[str, str]) -> str:
```

## stale_blocks

> Return one problem line per block whose embedded content differs.
>
> Raises:
>     SiteBuildError: A block has no marker pair in the page.

```python
def stale_blocks(html_text: str, blocks: dict[str, str]) -> list[str]:
```

## run_repotoc

> Run one repotoc command in the examples directory; return its code.

```python
def run_repotoc(command: list[str]) -> int:
```

## refresh

> Regenerate every variant and embed the showcase blocks.
>
> The generated directory is rebuilt from scratch: old variant
> directories disappear. When any variant run fails, the page is
> left unmodified.
>
> Raises:
>     SiteBuildError: A variant run failed.

```python
def refresh(index_path: Path=INDEX_PATH, examples_dir: Path=EXAMPLES_DIR, variants: tuple[Variant, ...]=VARIANTS, runner: Runner=run_repotoc) -> None:
```

## check

> Compare every variant and the embedding without writing.
>
> Returns:
>     A problem line per stale artifact or differing block, empty
>     when the showcase is current.
>
> Raises:
>     SiteBuildError: A variant run reported an error (any code
>         other than 0 or 1).

```python
def check(index_path: Path=INDEX_PATH, examples_dir: Path=EXAMPLES_DIR, variants: tuple[Variant, ...]=VARIANTS, runner: Runner=run_repotoc) -> list[str]:
```

## main

> Run the command, exiting 0 on success, 1 on stale, 2 on errors.

```python
def main(argv: list[str] | None=None) -> None:
```
