# `tests/test_site_build.py`

> Tests for the site showcase build script.

## `def test_replace_blocks_swaps_only_marker_content() -> None:`

> Replacement touches only the text between one marker pair.

---

## `def test_replace_blocks_is_idempotent() -> None:`

> Embedding the same blocks twice leaves the page unchanged.

---

## `def test_replace_blocks_missing_marker_raises() -> None:`

> A block with no marker pair fails, naming the marker.

---

## `def test_stale_blocks_reports_differing_content() -> None:`

> A block whose embedded text differs is reported by name.

---

## `def test_stale_blocks_missing_marker_raises() -> None:`

> Comparing against a page with no marker pair fails, naming it.

---

## `def test_collect_blocks_reads_and_escapes_every_variant(tmp_path: Path) -> None:`

> Every variant contributes one escaped block, keyed by name.

---

## `def test_collect_blocks_names_a_missing_variant(tmp_path: Path) -> None:`

> A variant without output fails, naming the variant key.

---

## `def test_render_trees_pairs_source_and_doc_rows(tmp_path: Path) -> None:`

> Doc rows sit beside their source rows, with the index first.

---

## `def test_render_trees_collapses_and_highlights(tmp_path: Path) -> None:`

> A collapsed directory is one row; the highlight marks both sides.

---

## `def test_render_trees_escapes_names(tmp_path: Path) -> None:`

> HTML-sensitive characters in names are escaped.

---

## `def test_render_trees_names_a_missing_doc_entry(tmp_path: Path) -> None:`

> A source file without a doc file fails, naming the doc path.

---

## `def test_render_trees_names_a_missing_root(tmp_path: Path) -> None:`

> A missing tree root fails, naming it.

---

## `def test_refresh_rebuilds_variants_and_embeds_them(tmp_path: Path) -> None:`

> Refresh wipes stale variant directories and embeds fresh output.

---

## `def test_refresh_leaves_the_page_unmodified_on_failure(tmp_path: Path) -> None:`

> A failing variant run aborts before any embedding happens.

---

## `def test_check_passes_when_current(tmp_path: Path) -> None:`

> A fresh matrix and matching embedding check clean.

---

## `def test_check_reports_a_stale_artifact(tmp_path: Path) -> None:`

> A variant whose repotoc check exits 1 is reported by key.

---

## `def test_check_reports_a_differing_block(tmp_path: Path) -> None:`

> A page whose embedded text differs from the variants is reported.

---

## `def test_check_raises_on_a_variant_error(tmp_path: Path) -> None:`

> A variant check exiting 2 is an error, not a staleness report.

---

## `def test_render_markdown_renders_the_artifact_grammar() -> None:`

> Headings, docstrings, fences, lists, and inline markup become HTML.

---

## `def test_render_markdown_resolves_links_against_the_doc_directory() -> None:`

> A link relative to its doc file resolves into the published variant.

---

## `def test_render_markdown_closes_an_unterminated_fence() -> None:`

> A fence left open at the end of the text still renders its lines.

---

## `def test_run_repotoc_executes_in_the_examples_directory() -> None:`

> The default runner runs repotoc in site/examples, returning its code.

---

## `def test_main_dispatches_refresh(monkeypatch: pytest.MonkeyPatch) -> None:`

> The refresh command runs refresh and exits cleanly.

---

## `def test_main_exits_one_when_check_is_stale(monkeypatch: pytest.MonkeyPatch) -> None:`

> The check command exits 1 when problems are found.

---

## `def test_main_exits_clean_when_check_passes(monkeypatch: pytest.MonkeyPatch) -> None:`

> The check command exits 0 when everything is current.

---

## `def test_main_exits_two_on_errors(monkeypatch: pytest.MonkeyPatch) -> None:`

> A SiteBuildError surfaces as exit code 2 on stderr.
