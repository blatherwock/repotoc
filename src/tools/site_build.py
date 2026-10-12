"""Refresh and gate the showcase site's example artifacts.

`refresh` runs `repotoc` over the site fixture once per showcase
variant, writing each run under `site/examples/generated/`, then
embeds the variant outputs and the fixture source into marked blocks
in `site/index.html`. `check` compares the same content without
writing: it exits 0 when current, 1 when stale, and 2 on errors.
"""

import argparse
import html
import posixpath
import re
import shutil
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SITE_DIR = _ROOT / "site"
EXAMPLES_DIR = _SITE_DIR / "examples"
INDEX_PATH = _SITE_DIR / "index.html"

FIXTURE_SOURCE = "fixture/arcade/checkers/players/minimax.py"
DOC_FILE = "fixture/arcade/checkers/players/minimax.md"
INDEX_NAME = "repotoc_toc.md"
INDEX_FILE = f"fixture/arcade/{INDEX_NAME}"

# The structure illustration: both trees are rooted at the arcade
# package. The doc tree reads the default-depth index run. Collapsed
# directories render as one line; the highlighted source file and its
# doc file tie the trees to the one-module showcase below them.
TREE_ROOT = "fixture/arcade"
TREE_VARIANT = "toc-6"
COLLAPSED = frozenset({"pong", "checkers/players/strategies"})
HIGHLIGHT = "checkers/players/minimax.py"

Runner = Callable[[list[str]], int]

_FENCE = re.compile(r"^```")
_HEADING = re.compile(r"^(#{1,4}) (.+)$")
_QUOTE = re.compile(r"^>(?: (.*))?$")
_LIST = re.compile(r"^( *)- (.+)$")
_HR = re.compile(r"-{3,}")
_CODE_SPAN = re.compile(r"`([^`]+)`")
_LINK_MD = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_STRONG = re.compile(r"\*\*([^*]+)\*\*")
_EM = re.compile(r"\*([^*]+)\*")


class SiteBuildError(Exception):
    """A failure refreshing or gating the site showcase blocks."""


@dataclass(frozen=True)
class Variant:
    """One repotoc run in the showcase matrix.

    Attributes:
        key: The variant directory under `generated/`, and the name
            of its embed block in `index.html`.
        kind: The panel the variant feeds: `doc` or `index`.
        flags: The repotoc flags configuring the run.
    """

    key: str
    kind: str
    flags: tuple[str, ...] = ()


def _variants() -> tuple[Variant, ...]:
    """Return the showcase matrix: eight doc variants and two indexes.

    The doc variants cross the presentation flags the showcase
    exposes: signatures on or off, privates on or off, and member
    depth unlimited or one. The index variants cover the two table of
    contents depths, six and two.
    """
    signatures = (
        ("s1", ("--file-include-signatures",)),
        ("s0", ("--no-file-include-signatures",)),
    )
    privates = (
        ("p0", ("--no-file-include-privates",)),
        ("p1", ("--file-include-privates",)),
    )
    depths = (
        ("df", ()),
        ("d1", ("--file-member-depth", "1")),
    )
    doc_variants = [
        Variant(f"doc-{s_key}-{p_key}-{d_key}", "doc", s_flags + p_flags + d_flags)
        for s_key, s_flags in signatures
        for p_key, p_flags in privates
        for d_key, d_flags in depths
    ]
    return (
        *doc_variants,
        Variant("toc-6", "index"),
        Variant("toc-2", "index", ("--toc-max-depths", "2")),
    )


VARIANTS = _variants()


def _begin(name: str) -> str:
    """Return the marker line opening a block."""
    return f"<!-- repotoc:begin {name} -->\n"


def _end(name: str) -> str:
    """Return the marker line closing a block."""
    return f"<!-- repotoc:end {name} -->"


def _pattern(name: str) -> re.Pattern[str]:
    """Return the pattern matching one block's full marker span."""
    combined = re.escape(_begin(name)) + r"(.*?)" + re.escape(_end(name))
    return re.compile(combined, re.DOTALL)


def _command(variant: Variant, *, check: bool = False) -> list[str]:
    """Return the repotoc command for one variant's run or check."""
    command = ["repotoc", "fixture", *variant.flags, "-o", f"generated/{variant.key}"]
    if check:
        command.append("--check")
    return command


def _escaped(path: Path) -> str:
    """Return the file's text with HTML-sensitive characters escaped."""
    return html.escape(path.read_text(), quote=False)


class _Renderer:
    """One Markdown render pass over an artifact file.

    The parser is a line loop whose open constructs, paragraph,
    docstring quote, list nesting, and code fence, each close in
    order when a block of a different kind begins.
    """

    def __init__(self, link_prefix: str, doc_dir: str) -> None:
        """Bind the pass to one variant's published location."""
        self.link_prefix = link_prefix
        self.doc_dir = doc_dir
        self.result: list[str] = []
        self.fence: list[str] | None = None
        self.paragraph: list[str] = []
        self.quote: list[list[str]] = []
        self.levels: list[int] = []

    def resolve(self, href: str) -> str:
        """Return the href pointing at the published variant file.

        The href is relative to its doc file, so the variant prefix
        and the doc directory join with it before normalizing.
        """
        base = self.link_prefix + self.doc_dir
        return posixpath.normpath(posixpath.join(base, href))

    def inline(self, text: str) -> str:
        """Return one line of Markdown text as inline HTML.

        Code spans, links, and emphasis render in that order; link
        hrefs point at the published variant files.
        """
        escaped = html.escape(text, quote=False)
        escaped = _CODE_SPAN.sub(r"<code>\1</code>", escaped)
        escaped = _LINK_MD.sub(
            lambda match: (
                f'<a href="{self.resolve(match.group(2))}">{match.group(1)}</a>'
            ),
            escaped,
        )
        escaped = _STRONG.sub(r"<strong>\1</strong>", escaped)
        return _EM.sub(r"<em>\1</em>", escaped)

    def close_paragraph(self) -> None:
        """Emit the paragraph buffer, joining wrapped lines in one block."""
        if not self.paragraph:
            return
        line = self.inline(" ".join(self.paragraph))
        self.result.append(f"<p>{line}</p>")
        self.paragraph.clear()

    def close_quote(self) -> None:
        """Emit the quote buffer, one block per docstring paragraph."""
        paragraphs = [lines for lines in self.quote if lines]
        self.quote.clear()
        if not paragraphs:
            return
        body = "".join(f"<p>{self.inline(' '.join(lines))}</p>" for lines in paragraphs)
        self.result.append(f"<blockquote>{body}</blockquote>")

    def close_list(self) -> None:
        """Close every open list level."""
        self.result.extend("</li></ul>" for _ in self.levels)
        self.levels.clear()

    def add_list_item(self, level: int, content: str) -> None:
        """Emit one list item, opening or closing nesting as needed."""
        while self.levels and level < self.levels[-1]:
            self.result.append("</li></ul>")
            self.levels.pop()
        if self.levels and level == self.levels[-1]:
            self.result.append("</li>")
        if not self.levels or level > self.levels[-1]:
            self.result.append("<ul>")
            self.levels.append(level)
        self.result.append(f"<li>{self.inline(content)}")

    def close_flow(self) -> None:
        """End the current paragraph, quote, and list."""
        self.close_paragraph()
        self.close_quote()
        self.close_list()

    def emit_fence(self, lines: list[str]) -> None:
        """Emit buffered fence lines as one escaped code block."""
        body = "\n".join(html.escape(line, quote=False) for line in lines)
        self.result.append(f'<pre class="code">{body}</pre>')

    def feed(self, line: str) -> None:
        """Parse one line into the open construct or a new one."""
        if self.fence is not None:
            if not _FENCE.match(line):
                self.fence.append(line)
            else:
                self.emit_fence(self.fence)
                self.fence = None
        elif _FENCE.match(line):
            self.close_flow()
            self.fence = []
        elif (heading := _HEADING.match(line)) is not None:
            self.close_flow()
            depth = len(heading.group(1))
            self.result.append(f"<h{depth}>{self.inline(heading.group(2))}</h{depth}>")
        elif _HR.fullmatch(line.strip()):
            self.close_flow()
            self.result.append("<hr>")
        elif (quote := _QUOTE.match(line)) is not None:
            self.close_paragraph()
            self.close_list()
            self.feed_quote(quote)
        elif (item := _LIST.match(line)) is not None:
            self.close_paragraph()
            self.close_quote()
            self.add_list_item(len(item.group(1)) // 2, item.group(2))
        elif not line.strip():
            self.close_flow()
        else:
            self.close_quote()
            self.close_list()
            self.paragraph.append(line)

    def feed_quote(self, quote: re.Match[str]) -> None:
        """Route one quote line: text joins, a bare line splits paragraphs."""
        if quote.group(1):
            if not self.quote:
                self.quote.append([])
            self.quote[-1].append(quote.group(1))
        else:
            self.quote.append([])

    def render(self, text: str) -> str:
        """Return the whole file rendered as HTML."""
        for line in text.splitlines():
            self.feed(line)
        self.close_flow()
        if self.fence is not None:
            self.emit_fence(self.fence)
        return "\n".join(self.result)


def render_markdown(text: str, *, link_prefix: str = "", doc_dir: str = "") -> str:
    """Return the artifact's Markdown rendered as HTML.

    Covers the grammar the artifact emits: headings, blockquote
    docstrings, fenced code blocks, thematic breaks, nested lists,
    and inline markup.
    Link targets resolve against `doc_dir`, the file's directory
    inside its variant, then gain `link_prefix` so they point at the
    published variant tree.
    """
    return _Renderer(link_prefix, doc_dir).render(text)


def _tree_label(name: str, *, suffix: str = "", marked: bool = False) -> str:
    """Return one tree row's escaped name, wrapped in a mark when highlighted."""
    label = html.escape(name, quote=False)
    return f"<mark>{label}</mark>{suffix}" if marked else f"{label}{suffix}"


def _doc_name(name: str) -> str:
    """Return the doc file RepoTOC writes for a source file."""
    if name == "__init__.py":
        return INDEX_NAME
    return Path(name).with_suffix(".md").name


@dataclass(frozen=True)
class _TreeMarks:
    """Which tree rows collapse and which highlight.

    Attributes:
        collapsed: Directory paths, relative to the tree root, shown
            as one line.
        highlight: The relative path of the source file to mark.
    """

    collapsed: frozenset[str]
    highlight: str


def _walk_trees(
    source_dir: Path,
    doc_dir: Path,
    relative: str,
    prefix: str,
    marks: _TreeMarks,
) -> tuple[list[str], list[str]]:
    """Return the source and doc tree rows below one directory.

    Rows pair up: each source entry's doc row sits at the same line,
    with `__init__.py` paired to the directory index.

    Raises:
        SiteBuildError: A source entry has no matching doc entry.
    """
    entries = sorted(
        (
            entry
            for entry in source_dir.iterdir()
            if entry.name != "__pycache__" and (entry.is_dir() or entry.suffix == ".py")
        ),
        key=lambda entry: entry.name,
    )
    source_rows: list[str] = []
    doc_rows: list[str] = []
    for position, entry in enumerate(entries):
        last = position == len(entries) - 1
        branch = prefix + ("└── " if last else "├── ")
        child_prefix = prefix + ("    " if last else "│   ")
        path = f"{relative}{entry.name}"
        if entry.is_dir():
            doc_path = doc_dir / entry.name
            suffix = " …" if path in marks.collapsed else ""
            source_rows.append(branch + _tree_label(f"{entry.name}/", suffix=suffix))
            doc_rows.append(branch + _tree_label(f"{entry.name}/", suffix=suffix))
            if not suffix:
                below_source, below_doc = _walk_trees(
                    entry, doc_path, f"{path}/", child_prefix, marks
                )
                source_rows.extend(below_source)
                doc_rows.extend(below_doc)
        else:
            doc_path = doc_dir / _doc_name(entry.name)
            marked = path == marks.highlight
            source_rows.append(branch + _tree_label(entry.name, marked=marked))
            doc_rows.append(branch + _tree_label(doc_path.name, marked=marked))
        if not doc_path.exists():
            message = f"missing tree output: {doc_path}"
            raise SiteBuildError(message)
    return source_rows, doc_rows


def render_trees(
    source_root: Path,
    doc_root: Path,
    collapsed: frozenset[str] = COLLAPSED,
    highlight: str = HIGHLIGHT,
) -> tuple[str, str]:
    """Return the source tree and the doc tree as aligned text blocks.

    Both trees list the source tree, with doc names substituted on
    the doc side. Directories named in `collapsed` (paths relative to
    the root) render as one line, and the file at `highlight` is
    wrapped in a mark on both sides.

    Raises:
        SiteBuildError: A root is missing, or a source entry has no
            doc entry.
    """
    for root in (source_root, doc_root):
        if not root.is_dir():
            message = f"missing tree root: {root}"
            raise SiteBuildError(message)
    source_rows, doc_rows = _walk_trees(
        source_root, doc_root, "", "", _TreeMarks(collapsed, highlight)
    )
    head = _tree_label(f"{source_root.name}/")
    return "\n".join([head, *source_rows]), "\n".join([head, *doc_rows])


def collect_blocks(examples_dir: Path, variants: tuple[Variant, ...]) -> dict[str, str]:
    """Return every embed block's content, read from the variant outputs.

    Raises:
        SiteBuildError: A variant's output file is missing, naming the
            variant key, so the showcase can never point at a hole; or
            the structure trees cannot be built.
    """
    blocks = {"source": _escaped(examples_dir / FIXTURE_SOURCE)}
    for variant in variants:
        relative = INDEX_FILE if variant.kind == "index" else DOC_FILE
        path = examples_dir / "generated" / variant.key / relative
        if not path.is_file():
            relative_to_root = path.relative_to(examples_dir)
            message = f"missing variant output: {variant.key} ({relative_to_root})"
            raise SiteBuildError(message)
        blocks[variant.key] = render_markdown(
            path.read_text(),
            link_prefix=f"examples/generated/{variant.key}/",
            doc_dir=posixpath.dirname(relative),
        )
    blocks["tree-source"], blocks["tree-doc"] = render_trees(
        examples_dir / TREE_ROOT,
        examples_dir / "generated" / TREE_VARIANT / TREE_ROOT,
    )
    return blocks


def _match_or_raise(html_text: str, name: str) -> re.Match[str]:
    """Return the block's marker match, failing when the pair is absent.

    Raises:
        SiteBuildError: The page holds no marker pair for the block.
    """
    match = _pattern(name).search(html_text)
    if match is None:
        message = f"missing markers: {name}"
        raise SiteBuildError(message)
    return match


def replace_blocks(html_text: str, blocks: dict[str, str]) -> str:
    """Return the page with each marked block's content replaced.

    Content outside the marker pairs is preserved verbatim.

    Raises:
        SiteBuildError: A block has no marker pair in the page.
    """
    for name, content in blocks.items():
        match = _match_or_raise(html_text, name)
        start = match.start() + len(_begin(name))
        end = match.end() - len(_end(name))
        html_text = html_text[:start] + content + html_text[end:]
    return html_text


def stale_blocks(html_text: str, blocks: dict[str, str]) -> list[str]:
    """Return one problem line per block whose embedded content differs.

    Raises:
        SiteBuildError: A block has no marker pair in the page.
    """
    problems = []
    for name, content in blocks.items():
        current = _match_or_raise(html_text, name).group(1)
        if current != content:
            problems.append(f"differing: {name}")
    return problems


def run_repotoc(command: list[str]) -> int:
    """Run one repotoc command in the examples directory; return its code."""
    completed = subprocess.run(command, cwd=EXAMPLES_DIR, check=False)
    return completed.returncode


def refresh(
    index_path: Path = INDEX_PATH,
    examples_dir: Path = EXAMPLES_DIR,
    variants: tuple[Variant, ...] = VARIANTS,
    runner: Runner = run_repotoc,
) -> None:
    """Regenerate every variant and embed the showcase blocks.

    The generated directory is rebuilt from scratch: old variant
    directories disappear. When any variant run fails, the page is
    left unmodified.

    Raises:
        SiteBuildError: A variant run failed.
    """
    shutil.rmtree(examples_dir / "generated", ignore_errors=True)
    for variant in variants:
        code = runner(_command(variant))
        if code != 0:
            message = f"repotoc failed for {variant.key} (exit {code})"
            raise SiteBuildError(message)
    blocks = collect_blocks(examples_dir, variants)
    index_path.write_text(replace_blocks(index_path.read_text(), blocks))


def check(
    index_path: Path = INDEX_PATH,
    examples_dir: Path = EXAMPLES_DIR,
    variants: tuple[Variant, ...] = VARIANTS,
    runner: Runner = run_repotoc,
) -> list[str]:
    """Compare every variant and the embedding without writing.

    Returns:
        A problem line per stale artifact or differing block, empty
        when the showcase is current.

    Raises:
        SiteBuildError: A variant run reported an error (any code
            other than 0 or 1).
    """
    problems = []
    for variant in variants:
        code = runner(_command(variant, check=True))
        if code == 1:
            problems.append(f"stale artifact: {variant.key}")
        elif code != 0:
            message = f"repotoc failed for {variant.key} (exit {code})"
            raise SiteBuildError(message)
    blocks = collect_blocks(examples_dir, variants)
    problems.extend(stale_blocks(index_path.read_text(), blocks))
    return problems


def main(argv: list[str] | None = None) -> None:
    """Run the command, exiting 0 on success, 1 on stale, 2 on errors."""
    parser = argparse.ArgumentParser(
        prog="site_build",
        description="Refresh or gate the site showcase blocks.",
    )
    parser.add_argument("command", choices=("refresh", "check"), help="what to do")
    command = parser.parse_args(argv).command
    try:
        if command == "refresh":
            refresh()
        elif problems := check():
            print("\n".join(problems))
            sys.exit(1)
    except SiteBuildError as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
