"""Tests for the site showcase build script."""

import importlib.util
from pathlib import Path

import pytest

# The CLI exit codes: success, stale check, and error.
_EXIT_SUCCESS = 0
_EXIT_STALE = 1
_EXIT_ERROR = 2

_SCRIPT = Path(__file__).resolve().parents[1] / "src" / "tools" / "site_build.py"

_spec = importlib.util.spec_from_file_location("site_build", _SCRIPT)
if _spec is None or _spec.loader is None:
    message = f"cannot load site_build from {_SCRIPT}"
    raise RuntimeError(message)
site_build = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(site_build)


def _index_page() -> str:
    """Return a page holding every marker pair with placeholder content."""
    names = [
        "source",
        "tree-source",
        "tree-doc",
        *(variant.key for variant in site_build.VARIANTS),
    ]
    blocks = "".join(
        f"<!-- repotoc:begin {name} -->\nplaceholder for {name}\n"
        f"<!-- repotoc:end {name} -->\n"
        for name in names
    )
    return f"<!-- header -->\n{blocks}<!-- footer -->\n"


def _write_fixture_source(examples: Path) -> None:
    """Write a fake fixture source file under a fake examples directory."""
    path = examples / site_build.FIXTURE_SOURCE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("def board():\n    return '<b>raw</b>'\n")


def _fake_runner(
    examples: Path, codes: dict[str, int] | None = None
) -> "site_build.Runner":
    """Return a runner writing fake variant outputs, honoring set codes.

    Each command's variant key comes from its `-o` argument. A key in
    `codes` returns its code without writing; every other key writes
    its output file and returns 0.
    """
    codes = codes or {}

    def run(command: list[str]) -> int:
        key = command[command.index("-o") + 1].removeprefix("generated/")
        if key in codes:
            return codes[key]
        variant = next(item for item in site_build.VARIANTS if item.key == key)
        relative = (
            site_build.INDEX_FILE if variant.kind == "index" else site_build.DOC_FILE
        )
        # Index runs also write the module doc file the trees pair with.
        files = [relative, site_build.DOC_FILE]
        for name in files if variant.kind == "index" else files[:1]:
            path = examples / "generated" / key / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"output for {key}\n")
        return 0

    return run


def test_replace_blocks_swaps_only_marker_content() -> None:
    """Replacement touches only the text between one marker pair."""
    page = "head\n<!-- repotoc:begin a -->\nold\n<!-- repotoc:end a -->\ntail\n"
    result = site_build.replace_blocks(page, {"a": "new"})
    assert result == "head\n<!-- repotoc:begin a -->\nnew<!-- repotoc:end a -->\ntail\n"


def test_replace_blocks_is_idempotent() -> None:
    """Embedding the same blocks twice leaves the page unchanged."""
    page = _index_page()
    blocks = {"source": "content\n"}
    once = site_build.replace_blocks(page, blocks)
    assert site_build.replace_blocks(once, blocks) == once


def test_replace_blocks_missing_marker_raises() -> None:
    """A block with no marker pair fails, naming the marker."""
    with pytest.raises(site_build.SiteBuildError, match="missing markers: a"):
        site_build.replace_blocks("nothing here\n", {"a": "new"})


def test_stale_blocks_reports_differing_content() -> None:
    """A block whose embedded text differs is reported by name."""
    page = "head\n<!-- repotoc:begin a -->\nnew\n<!-- repotoc:end a -->\ntail\n"
    assert site_build.stale_blocks(page, {"a": "different\n"}) == ["differing: a"]
    assert site_build.stale_blocks(page, {"a": "new\n"}) == []


def test_stale_blocks_missing_marker_raises() -> None:
    """Comparing against a page with no marker pair fails, naming it."""
    with pytest.raises(site_build.SiteBuildError, match="missing markers: a"):
        site_build.stale_blocks("nothing here\n", {"a": "new"})


def test_collect_blocks_reads_and_escapes_every_variant(tmp_path: Path) -> None:
    """Every variant contributes one escaped block, keyed by name."""
    examples = tmp_path / "examples"
    _write_fixture_source(examples)
    runner = _fake_runner(examples)
    for variant in site_build.VARIANTS:
        runner(["repotoc", "fixture", "-o", f"generated/{variant.key}"])

    blocks = site_build.collect_blocks(examples, site_build.VARIANTS)

    assert set(blocks) == {
        "source",
        "tree-source",
        "tree-doc",
        *(variant.key for variant in site_build.VARIANTS),
    }
    assert "<b>raw</b>" not in blocks["source"]
    assert "&lt;b&gt;raw&lt;/b&gt;" in blocks["source"]
    assert blocks["toc-2"] == "<p>output for toc-2</p>"


def test_collect_blocks_names_a_missing_variant(tmp_path: Path) -> None:
    """A variant without output fails, naming the variant key."""
    examples = tmp_path / "examples"
    _write_fixture_source(examples)
    runner = _fake_runner(examples)
    for variant in site_build.VARIANTS:
        runner(["repotoc", "fixture", "-o", f"generated/{variant.key}"])
    (examples / "generated" / "toc-6" / site_build.INDEX_FILE).unlink()

    with pytest.raises(
        site_build.SiteBuildError, match="missing variant output: toc-6"
    ):
        site_build.collect_blocks(examples, site_build.VARIANTS)


def _write_tree(root: Path, names: list[str]) -> None:
    """Create empty files at the given paths below a root."""
    for name in names:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()


def test_render_trees_pairs_source_and_doc_rows(tmp_path: Path) -> None:
    """Doc rows sit beside their source rows, with the index first."""
    source, docs = tmp_path / "src" / "arcade", tmp_path / "docs" / "arcade"
    _write_tree(source, ["__init__.py", "game.py", "readme.txt", "__pycache__/x.py"])
    _write_tree(docs, ["repotoc_toc.md", "game.md"])

    source_tree, doc_tree = site_build.render_trees(source, docs, frozenset(), "")

    assert source_tree == "arcade/\n├── __init__.py\n└── game.py"
    assert doc_tree == "arcade/\n├── repotoc_toc.md\n└── game.md"


def test_render_trees_collapses_and_highlights(tmp_path: Path) -> None:
    """A collapsed directory is one row; the highlight marks both sides."""
    source, docs = tmp_path / "src" / "arcade", tmp_path / "docs" / "arcade"
    _write_tree(source, ["pong/ball.py", "checkers/minimax.py", "last.py"])
    _write_tree(docs, ["pong/ball.md", "checkers/minimax.md", "last.md"])

    source_tree, doc_tree = site_build.render_trees(
        source, docs, frozenset({"pong"}), "checkers/minimax.py"
    )

    assert source_tree.splitlines() == [
        "arcade/",
        "├── checkers/",
        "│   └── <mark>minimax.py</mark>",
        "├── last.py",
        "└── pong/ …",
    ]
    assert "│   └── <mark>minimax.md</mark>" in doc_tree.splitlines()
    assert "ball" not in doc_tree


def test_render_trees_escapes_names(tmp_path: Path) -> None:
    """HTML-sensitive characters in names are escaped."""
    source, docs = tmp_path / "src" / "arcade", tmp_path / "docs" / "arcade"
    _write_tree(source, ["a&b.py"])
    _write_tree(docs, ["a&b.md"])

    source_tree, _ = site_build.render_trees(source, docs, frozenset(), "")

    assert "a&amp;b.py" in source_tree


def test_render_trees_names_a_missing_doc_entry(tmp_path: Path) -> None:
    """A source file without a doc file fails, naming the doc path."""
    source, docs = tmp_path / "src" / "arcade", tmp_path / "docs" / "arcade"
    _write_tree(source, ["game.py"])
    docs.mkdir(parents=True)

    with pytest.raises(
        site_build.SiteBuildError, match=r"missing tree output: .*game\.md"
    ):
        site_build.render_trees(source, docs, frozenset(), "")


def test_render_trees_names_a_missing_root(tmp_path: Path) -> None:
    """A missing tree root fails, naming it."""
    with pytest.raises(
        site_build.SiteBuildError, match=r"missing tree root: .*nowhere"
    ):
        site_build.render_trees(tmp_path / "nowhere", tmp_path)


def test_refresh_rebuilds_variants_and_embeds_them(tmp_path: Path) -> None:
    """Refresh wipes stale variant directories and embeds fresh output."""
    examples = tmp_path / "examples"
    _write_fixture_source(examples)
    leftover = examples / "generated" / "leftover"
    leftover.mkdir(parents=True)
    index_path = tmp_path / "index.html"
    index_path.write_text(_index_page())

    site_build.refresh(
        index_path, examples, site_build.VARIANTS, _fake_runner(examples)
    )

    assert not leftover.exists()
    page = index_path.read_text()
    assert "<!-- header -->" in page and "<!-- footer -->" in page
    assert "placeholder for doc-s1-p0-df" not in page
    assert "output for doc-s1-p0-df" in page
    assert "output for toc-2" in page


def test_refresh_leaves_the_page_unmodified_on_failure(tmp_path: Path) -> None:
    """A failing variant run aborts before any embedding happens."""
    examples = tmp_path / "examples"
    _write_fixture_source(examples)
    index_path = tmp_path / "index.html"
    index_path.write_text(_index_page())
    before = index_path.read_text()

    def failing(_command: list[str]) -> int:
        return _EXIT_ERROR

    with pytest.raises(
        site_build.SiteBuildError, match=r"repotoc failed for doc-s1-p0-df \(exit 2\)"
    ):
        site_build.refresh(index_path, examples, site_build.VARIANTS, failing)
    assert index_path.read_text() == before


def test_check_passes_when_current(tmp_path: Path) -> None:
    """A fresh matrix and matching embedding check clean."""
    examples = tmp_path / "examples"
    _write_fixture_source(examples)
    index_path = tmp_path / "index.html"
    index_path.write_text(_index_page())
    runner = _fake_runner(examples)
    site_build.refresh(index_path, examples, site_build.VARIANTS, runner)

    problems = site_build.check(index_path, examples, site_build.VARIANTS, runner)

    assert problems == []


def test_check_reports_a_stale_artifact(tmp_path: Path) -> None:
    """A variant whose repotoc check exits 1 is reported by key."""
    examples = tmp_path / "examples"
    _write_fixture_source(examples)
    index_path = tmp_path / "index.html"
    index_path.write_text(_index_page())
    site_build.refresh(
        index_path, examples, site_build.VARIANTS, _fake_runner(examples)
    )

    stale = _fake_runner(examples, codes={"toc-2": 1})
    problems = site_build.check(index_path, examples, site_build.VARIANTS, stale)

    assert "stale artifact: toc-2" in problems


def test_check_reports_a_differing_block(tmp_path: Path) -> None:
    """A page whose embedded text differs from the variants is reported."""
    examples = tmp_path / "examples"
    _write_fixture_source(examples)
    index_path = tmp_path / "index.html"
    index_path.write_text(_index_page())
    runner = _fake_runner(examples)
    site_build.refresh(index_path, examples, site_build.VARIANTS, runner)
    index_path.write_text(_index_page())

    problems = site_build.check(index_path, examples, site_build.VARIANTS, runner)

    assert "differing: source" in problems


def test_check_raises_on_a_variant_error(tmp_path: Path) -> None:
    """A variant check exiting 2 is an error, not a staleness report."""
    examples = tmp_path / "examples"
    _write_fixture_source(examples)
    index_path = tmp_path / "index.html"
    index_path.write_text(_index_page())

    broken = _fake_runner(examples, codes={"doc-s1-p0-df": 2})
    with pytest.raises(
        site_build.SiteBuildError, match=r"repotoc failed for doc-s1-p0-df \(exit 2\)"
    ):
        site_build.check(index_path, examples, site_build.VARIANTS, broken)


def test_render_markdown_renders_the_artifact_grammar() -> None:
    """Headings, docstrings, fences, lists, and inline markup become HTML."""
    text = (
        "# fixture/mod.py\n"
        "\n"
        "> A module docstring.\n"
        ">\n"
        "> Second paragraph.\n"
        "\n"
        "## `class Board:`\n"
        "\n"
        "```python\n"
        "class Board:\n"
        "    x = '<b>raw</b>'\n"
        "```\n"
        "\n"
        "---\n"
        "\n"
        "- [`arcade/`](arcade/repotoc_toc.md): A tiny arcade.\n"
        "  - [`game.py`](arcade/game.md): The shared types.\n"
        "- [`x.py`](x.md)\n"
        "\n"
        "Plain paragraph with `code` and **bold**.\n"
    )

    rendered = site_build.render_markdown(text, link_prefix="examples/generated/toc-6/")

    assert "<h1>fixture/mod.py</h1>" in rendered
    assert (
        "<blockquote><p>A module docstring.</p><p>Second paragraph.</p></blockquote>"
        in rendered
    )
    assert "<h2><code>class Board:</code></h2>" in rendered
    assert (
        "<pre class=\"code\">class Board:\n    x = '&lt;b&gt;raw&lt;/b&gt;'</pre>"
        in rendered
    )
    assert "<hr>" in rendered
    assert (
        '<li><a href="examples/generated/toc-6/arcade/repotoc_toc.md">'
        "<code>arcade/</code></a>: A tiny arcade." in rendered
    )
    assert "<ul><li><a href=" not in rendered  # nesting stays inside the parent item
    assert (
        "Plain paragraph with <code>code</code> and <strong>bold</strong>." in rendered
    )


def test_render_markdown_resolves_links_against_the_doc_directory() -> None:
    """A link relative to its doc file resolves into the published variant."""
    rendered = site_build.render_markdown(
        "- [`m.py`](../../game.py)\n",
        link_prefix="examples/generated/doc-s1-p0-df/",
        doc_dir="fixture/arcade/checkers/players",
    )

    assert 'href="examples/generated/doc-s1-p0-df/fixture/arcade/game.py"' in rendered


def test_render_markdown_closes_an_unterminated_fence() -> None:
    """A fence left open at the end of the text still renders its lines."""
    rendered = site_build.render_markdown("```python\nclass Board:\n")

    assert '<pre class="code">class Board:</pre>' in rendered


def test_run_repotoc_executes_in_the_examples_directory() -> None:
    """The default runner runs repotoc in site/examples, returning its code."""
    code = site_build.run_repotoc(
        ["repotoc", "fixture", "-o", "generated/_selfcheck", "--check"]
    )
    assert code == _EXIT_STALE


def test_main_dispatches_refresh(monkeypatch: pytest.MonkeyPatch) -> None:
    """The refresh command runs refresh and exits cleanly."""
    calls = []
    monkeypatch.setattr(site_build, "refresh", lambda: calls.append("refresh"))
    site_build.main(["refresh"])
    assert calls == ["refresh"]


def test_main_exits_one_when_check_is_stale(monkeypatch: pytest.MonkeyPatch) -> None:
    """The check command exits 1 when problems are found."""
    monkeypatch.setattr(site_build, "check", lambda: ["differing: source"])
    with pytest.raises(SystemExit) as excinfo:
        site_build.main(["check"])
    assert excinfo.value.code == _EXIT_STALE


def test_main_exits_clean_when_check_passes(monkeypatch: pytest.MonkeyPatch) -> None:
    """The check command exits 0 when everything is current."""
    monkeypatch.setattr(site_build, "check", lambda: [])
    site_build.main(["check"])


def test_main_exits_two_on_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    """A SiteBuildError surfaces as exit code 2 on stderr."""
    monkeypatch.setattr(
        site_build,
        "refresh",
        lambda: pytest.fail("refresh should not run"),
    )

    def broken() -> list[str]:
        message = "boom"
        raise site_build.SiteBuildError(message)

    monkeypatch.setattr(site_build, "check", broken)
    with pytest.raises(SystemExit) as excinfo:
        site_build.main(["check"])
    assert excinfo.value.code == _EXIT_ERROR
