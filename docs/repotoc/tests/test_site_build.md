# tests/test_site_build.py

> Tests for the site showcase build script.

## test_replace_blocks_swaps_only_marker_content

> Replacement touches only the text between one marker pair.

```python
def test_replace_blocks_swaps_only_marker_content() -> None:
```

## test_replace_blocks_is_idempotent

> Embedding the same blocks twice leaves the page unchanged.

```python
def test_replace_blocks_is_idempotent() -> None:
```

## test_replace_blocks_missing_marker_raises

> A block with no marker pair fails, naming the marker.

```python
def test_replace_blocks_missing_marker_raises() -> None:
```

## test_stale_blocks_reports_differing_content

> A block whose embedded text differs is reported by name.

```python
def test_stale_blocks_reports_differing_content() -> None:
```

## test_stale_blocks_missing_marker_raises

> Comparing against a page with no marker pair fails, naming it.

```python
def test_stale_blocks_missing_marker_raises() -> None:
```

## test_collect_blocks_reads_and_escapes_every_variant

> Every variant contributes one escaped block, keyed by name.

```python
def test_collect_blocks_reads_and_escapes_every_variant(tmp_path: Path) -> None:
```

## test_collect_blocks_names_a_missing_variant

> A variant without output fails, naming the variant key.

```python
def test_collect_blocks_names_a_missing_variant(tmp_path: Path) -> None:
```

## test_render_trees_pairs_source_and_doc_rows

> Doc rows sit beside their source rows, with the index first.

```python
def test_render_trees_pairs_source_and_doc_rows(tmp_path: Path) -> None:
```

## test_render_trees_collapses_and_highlights

> A collapsed directory is one row; the highlight marks both sides.

```python
def test_render_trees_collapses_and_highlights(tmp_path: Path) -> None:
```

## test_render_trees_escapes_names

> HTML-sensitive characters in names are escaped.

```python
def test_render_trees_escapes_names(tmp_path: Path) -> None:
```

## test_render_trees_names_a_missing_doc_entry

> A source file without a doc file fails, naming the doc path.

```python
def test_render_trees_names_a_missing_doc_entry(tmp_path: Path) -> None:
```

## test_render_trees_names_a_missing_root

> A missing tree root fails, naming it.

```python
def test_render_trees_names_a_missing_root(tmp_path: Path) -> None:
```

## test_refresh_rebuilds_variants_and_embeds_them

> Refresh wipes stale variant directories and embeds fresh output.

```python
def test_refresh_rebuilds_variants_and_embeds_them(tmp_path: Path) -> None:
```

## test_refresh_leaves_the_page_unmodified_on_failure

> A failing variant run aborts before any embedding happens.

```python
def test_refresh_leaves_the_page_unmodified_on_failure(tmp_path: Path) -> None:
```

## test_check_passes_when_current

> A fresh matrix and matching embedding check clean.

```python
def test_check_passes_when_current(tmp_path: Path) -> None:
```

## test_check_reports_a_stale_artifact

> A variant whose repotoc check exits 1 is reported by key.

```python
def test_check_reports_a_stale_artifact(tmp_path: Path) -> None:
```

## test_check_reports_a_differing_block

> A page whose embedded text differs from the variants is reported.

```python
def test_check_reports_a_differing_block(tmp_path: Path) -> None:
```

## test_check_raises_on_a_variant_error

> A variant check exiting 2 is an error, not a staleness report.

```python
def test_check_raises_on_a_variant_error(tmp_path: Path) -> None:
```

## test_render_markdown_renders_the_artifact_grammar

> Headings, docstrings, fences, lists, and inline markup become HTML.

```python
def test_render_markdown_renders_the_artifact_grammar() -> None:
```

## test_render_markdown_resolves_links_against_the_doc_directory

> A link relative to its doc file resolves into the published variant.

```python
def test_render_markdown_resolves_links_against_the_doc_directory() -> None:
```

## test_render_markdown_closes_an_unterminated_fence

> A fence left open at the end of the text still renders its lines.

```python
def test_render_markdown_closes_an_unterminated_fence() -> None:
```

## test_run_repotoc_executes_in_the_examples_directory

> The default runner runs repotoc in site/examples, returning its code.

```python
def test_run_repotoc_executes_in_the_examples_directory() -> None:
```

## test_main_dispatches_refresh

> The refresh command runs refresh and exits cleanly.

```python
def test_main_dispatches_refresh(monkeypatch: pytest.MonkeyPatch) -> None:
```

## test_main_exits_one_when_check_is_stale

> The check command exits 1 when problems are found.

```python
def test_main_exits_one_when_check_is_stale(monkeypatch: pytest.MonkeyPatch) -> None:
```

## test_main_exits_clean_when_check_passes

> The check command exits 0 when everything is current.

```python
def test_main_exits_clean_when_check_passes(monkeypatch: pytest.MonkeyPatch) -> None:
```

## test_main_exits_two_on_errors

> A SiteBuildError surfaces as exit code 2 on stderr.

```python
def test_main_exits_two_on_errors(monkeypatch: pytest.MonkeyPatch) -> None:
```
